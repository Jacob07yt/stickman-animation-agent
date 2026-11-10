"""Upload a finished video to YouTube with the YouTube Data API v3 (standard library only).

Credentials come from environment variables (set by the channel owner in the cloud environment settings):
  YT_CLIENT_ID, YT_CLIENT_SECRET, YT_REFRESH_TOKEN

Usage:
  python src/publish/youtube_upload.py <upload.json>          # upload one video
  python src/publish/youtube_upload.py --check                 # verify credentials, print channel name

upload.json:
{
  "key": "2026-11-10-cuban-missile-crisis",      # unique; used to refuse double uploads
  "video": "projects/<slug>/output/<slug>.mp4",
  "title": "...", "description": "...", "tags": ["..."],
  "category": "27",                               # 27 = Education
  "privacy": "public" | "private" | "unlisted",
  "publish_at": "2026-11-11T17:00:00Z",           # optional: schedule (video uploads as private, goes public at this time)
  "thumbnail": "projects/<slug>/output/thumbnail.jpg",   # optional
  "captions": "projects/<slug>/output/<slug>.srt",       # optional
  "made_for_kids": false
}
Appends a line to channel/upload-log.md and prints the video URL.
Note: until Google approves the API project's audit, YouTube locks API uploads to private.
"""
import json, os, sys, uuid, urllib.error, urllib.parse, urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LOG = ROOT / "channel" / "upload-log.md"
API = "https://www.googleapis.com"


def http(method, url, data=None, headers=None, timeout=600):
    req = urllib.request.Request(url, data=data, method=method, headers=headers or {})
    try:
        with urllib.request.urlopen(req, timeout=timeout) as r:
            return r.status, dict(r.headers), r.read()
    except urllib.error.HTTPError as e:
        return e.code, dict(e.headers), e.read()


def access_token():
    missing = [k for k in ("YT_CLIENT_ID", "YT_CLIENT_SECRET", "YT_REFRESH_TOKEN") if not os.environ.get(k)]
    if missing:
        sys.exit(f"Missing environment variables: {', '.join(missing)} (add them in the environment settings, then start a new session)")
    body = urllib.parse.urlencode({
        "client_id": os.environ["YT_CLIENT_ID"], "client_secret": os.environ["YT_CLIENT_SECRET"],
        "refresh_token": os.environ["YT_REFRESH_TOKEN"], "grant_type": "refresh_token"}).encode()
    st, _, raw = http("POST", "https://oauth2.googleapis.com/token", body, {"Content-Type": "application/x-www-form-urlencoded"})
    if st != 200:
        sys.exit(f"Token refresh failed ({st}): {raw.decode(errors='replace')[:300]}")
    return json.loads(raw)["access_token"]


def channel(tok):
    st, _, raw = http("GET", f"{API}/youtube/v3/channels?part=snippet&mine=true", headers={"Authorization": f"Bearer {tok}"})
    if st != 200:
        sys.exit(f"Channel lookup failed ({st}): {raw.decode(errors='replace')[:300]}")
    items = json.loads(raw).get("items", [])
    return (items[0]["id"], items[0]["snippet"]["title"]) if items else (None, None)


def already_uploaded(key):
    return LOG.exists() and f"| {key} |" in LOG.read_text(encoding="utf-8")


def log(key, title, vid, privacy, publish_at):
    if not LOG.exists():
        LOG.write_text("# Upload log\n\n| Uploaded (UTC) | Key | Title | Video | Privacy | Publish at |\n|---|---|---|---|---|---|\n", encoding="utf-8")
    with LOG.open("a", encoding="utf-8") as f:
        f.write(f"| {datetime.now(timezone.utc):%Y-%m-%d %H:%M} | {key} | {title} | https://youtu.be/{vid} | {privacy} | {publish_at or '-'} |\n")


def upload(spec):
    tok = access_token()
    cid, cname = channel(tok)
    print(f"Channel: {cname} ({cid})")
    if spec.get("expect_channel") and spec["expect_channel"].lower() not in (cname or "").lower():
        sys.exit(f"Refusing to upload: signed-in channel is {cname!r}, expected {spec['expect_channel']!r}")
    if already_uploaded(spec["key"]):
        sys.exit(f"Already uploaded (see {LOG}): {spec['key']}")
    video = (ROOT / spec["video"]) if not os.path.isabs(spec["video"]) else Path(spec["video"])
    size = video.stat().st_size
    status = {"privacyStatus": spec.get("privacy", "private"), "selfDeclaredMadeForKids": bool(spec.get("made_for_kids", False)),
              "containsSyntheticMedia": bool(spec.get("synthetic_media", False))}
    if spec.get("publish_at"):
        status["privacyStatus"] = "private"; status["publishAt"] = spec["publish_at"]
    meta = {"snippet": {"title": spec["title"][:100], "description": spec.get("description", "")[:5000],
                        "tags": spec.get("tags", []), "categoryId": str(spec.get("category", "27")),
                        "defaultLanguage": "en", "defaultAudioLanguage": "en"}, "status": status}
    st, hdr, raw = http("POST", f"{API}/upload/youtube/v3/videos?uploadType=resumable&part=snippet,status",
                        json.dumps(meta).encode(), {"Authorization": f"Bearer {tok}", "Content-Type": "application/json; charset=UTF-8",
                                                    "X-Upload-Content-Length": str(size), "X-Upload-Content-Type": "video/mp4"})
    loc = hdr.get("Location") or hdr.get("location")
    if st != 200 or not loc:
        sys.exit(f"Upload session failed ({st}): {raw.decode(errors='replace')[:500]}")
    st, _, raw = http("PUT", loc, video.read_bytes(), {"Authorization": f"Bearer {tok}", "Content-Type": "video/mp4"}, timeout=3600)
    if st not in (200, 201):
        sys.exit(f"Video upload failed ({st}): {raw.decode(errors='replace')[:500]}")
    res = json.loads(raw); vid = res["id"]
    print(f"Uploaded: https://youtu.be/{vid} (privacy {res['status'].get('privacyStatus')}, upload status {res['status'].get('uploadStatus')})")
    log(spec["key"], spec["title"], vid, status["privacyStatus"], spec.get("publish_at"))

    if spec.get("thumbnail"):
        th = ROOT / spec["thumbnail"]
        st, _, raw = http("POST", f"{API}/upload/youtube/v3/thumbnails/set?videoId={vid}&uploadType=media", th.read_bytes(),
                          {"Authorization": f"Bearer {tok}", "Content-Type": "image/jpeg"})
        print("Thumbnail:", "ok" if st == 200 else f"failed ({st}) {raw.decode(errors='replace')[:300]}")
    if spec.get("captions"):
        cap = (ROOT / spec["captions"]).read_bytes(); b = uuid.uuid4().hex
        body = (f"--{b}\r\nContent-Type: application/json; charset=UTF-8\r\n\r\n"
                + json.dumps({"snippet": {"videoId": vid, "language": "en", "name": "English", "isDraft": False}})
                + f"\r\n--{b}\r\nContent-Type: application/octet-stream\r\n\r\n").encode() + cap + f"\r\n--{b}--\r\n".encode()
        st, _, raw = http("POST", f"{API}/upload/youtube/v3/captions?uploadType=multipart&part=snippet", body,
                          {"Authorization": f"Bearer {tok}", "Content-Type": f"multipart/related; boundary={b}"})
        print("Captions:", "ok" if st == 200 else f"failed ({st}) {raw.decode(errors='replace')[:300]}")
    return vid


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--check":
        cid, cname = channel(access_token()); print(f"Credentials OK. Channel: {cname} ({cid})")
    elif len(sys.argv) == 2:
        upload(json.loads(Path(sys.argv[1]).read_text(encoding="utf-8")))
    else:
        sys.exit(__doc__)
