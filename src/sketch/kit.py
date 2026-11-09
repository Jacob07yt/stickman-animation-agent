"""Coloured history sketch kit.

Reusable SVG drawing parts (characters, flags, maps, props) and a GSAP animation
helper layer for building HyperFrames-compatible scene compositions in the
"coloured history sketch" style: parchment page, ink outlines, flat colour fills
by faction, Caveat handwriting.

Usage (from a project's scene builder):
    import sys; sys.path.insert(0, "<repo>/src/sketch"); from kit import *
    html = page("01", duration, svg_body, js)

Positioned parts are nested as <g id transform="translate"> <g transform="scale">
so GSAP can pop/scale/move the outer group without losing the inner scale.
Any element with class "d" is drawn in (stroke-dash animation); other shapes in a
drawn group fade in at the end of the draw.
"""
import base64, json, math, re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

# ---------------------------------------------------------------- palette
INK = "#1A1A1A"; INK2 = "#4A4A4A"; BG = "#EFE8DC"; LINE = "#DDD3C3"
US = "#3D6DB5"; USD = "#2B4F86"; USLAND = "#BFD0EA"
SU = "#C0392B"; SUD = "#8E2A20"; SULAND = "#E8B4AC"
CU = "#4E8A4B"; CUD = "#356a33"; CULAND = "#A9CFA2"
TR = "#D9C27A"; SEA = "#CFE0E3"; SKIN = "#FBF6EE"; GOLD = "#E5B83B"; WOOD = "#B98A5A"; GREY = "#9AA3A8"

_FONTS = {}


def _font(w):
    if w not in _FONTS:
        _FONTS[w] = base64.b64encode((ROOT / f"assets/fonts/Caveat-{w}.ttf").read_bytes()).decode()
    return _FONTS[w]


def _gsap():
    return (ROOT / "node_modules/gsap/dist/gsap.min.js").read_text()


# ---------------------------------------------------------------- word timing
class Words:
    """Look up when a word is spoken: W("missiles") -> start time, W("the", 3) -> 3rd 'the'."""

    def __init__(self, ts_path):
        d = json.loads(Path(ts_path).read_text())
        self.duration = d["duration"]
        self.words = [(re.sub(r"[^a-z0-9']", "", w["word"].lower()), w["start"], w["end"]) for w in d["words"]]

    def __call__(self, word, n=1, end=False):
        key = re.sub(r"[^a-z0-9']", "", word.lower())
        hits = [w for w in self.words if w[0] == key] or [w for w in self.words if w[0].startswith(key)]
        if len(hits) < n:
            raise KeyError(f"word {word!r} #{n} not found in {[w[0] for w in self.words]}")
        return round(hits[n - 1][2 if end else 1], 2)


# ---------------------------------------------------------------- primitives
def g(gid, x, y, s, inner, cls="", hidden=True):
    op = ' opacity="0"' if hidden else ""
    c = f' class="{cls}"' if cls else ""
    return f'<g id="{gid}"{c} transform="translate({x},{y})"{op}><g transform="scale({s})">{inner}</g></g>'


def text(tid, x, y, s, size=60, fill=INK, weight=700, anchor="middle", extra="", hidden=True):
    op = ' opacity="0"' if hidden else ""
    return (f'<text id="{tid}" x="{x}" y="{y}" text-anchor="{anchor}" font-family="Cav" font-weight="{weight}" '
            f'font-size="{size}" fill="{fill}"{op} {extra}>{s}</text>')


def card(cid, x, y, w, h, lines, stroke=INK, size=56, fill=INK, bg=BG, sw=4, hidden=True):
    """Rounded box with one or more centred text lines. lines: [(text, colour)] or str."""
    if isinstance(lines, str):
        lines = [(lines, fill)]
    lh = size * 1.15
    y0 = y + h / 2 - lh * (len(lines) - 1) / 2 + size * 0.33
    t = "".join(f'<text x="{x + w/2}" y="{y0 + i*lh}" text-anchor="middle" font-family="Cav" font-weight="700" font-size="{size}" fill="{c}">{s}</text>'
                for i, (s, c) in enumerate(lines))
    op = ' opacity="0"' if hidden else ""
    return f'<g id="{cid}"{op}><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="16" fill="{bg}" stroke="{stroke}" stroke-width="{sw}"/>{t}</g>'


def datecard(cid, label, year="1962"):
    return card(cid, 60, 50, 600, 110, [(f'{label}, <tspan fill="{SU}">{year}</tspan>', INK)], size=64)


def stamp(sid, x, y, label, color=SU, size=80, rot=-8):
    w = len(label) * size * 0.52 + 60
    return (f'<g id="{sid}" transform="translate({x},{y})" opacity="0"><g transform="rotate({rot})">'
            f'<rect x="{-w/2}" y="{-size*0.75}" width="{w}" height="{size*1.3}" rx="10" fill="none" stroke="{color}" stroke-width="8"/>'
            f'<text x="0" y="{size*0.3}" text-anchor="middle" font-family="Cav" font-weight="700" font-size="{size}" fill="{color}">{label}</text></g></g>')


def bubble(bid, x, y, label, size=48, w=None, tail="left", hidden=True):
    """Speech bubble with its tail tip at (x, y)."""
    w = w or len(label) * size * 0.48 + 50
    h = size * 1.6
    bx = x - 30 if tail == "left" else x - w + 30
    by = y - h - 30
    tx = x
    return (f'<g id="{bid}"{" opacity=\"0\"" if hidden else ""}><path d="M{bx+14},{by} h{w-28} a14,14 0 0 1 14,14 v{h-28} a14,14 0 0 1 -14,14 '
            f'H{tx+18} L{tx},{y} L{tx+4},{by+h} H{bx+14} a14,14 0 0 1 -14,-14 v{-(h-28)} a14,14 0 0 1 14,-14 Z" fill="#fff" stroke="{INK}" stroke-width="4"/>'
            f'<text x="{bx + w/2}" y="{by + h/2 + size*0.33}" text-anchor="middle" font-family="Cav" font-weight="700" font-size="{size}" fill="{INK}">{label}</text></g>')


# ---------------------------------------------------------------- characters
def _person(torso, hair="", extra="", arms="M-30,-20 L-62,40 M30,-20 L62,40", face="smile", glasses=False,
            legs="M-14,70 L-22,150 M14,70 L22,150", skin=SKIN, head_extra=""):
    mouth = {"smile": "M-16,-112 Q0,-100 16,-112", "flat": "M-14,-108 L14,-108",
             "frown": "M-16,-102 Q0,-114 16,-102", "open": "M-10,-110 Q0,-96 10,-110 Q0,-104 -10,-110",
             "shout": "M-14,-112 Q0,-86 14,-112 Z"}[face]
    gl = ('<circle class="d" cx="-18" cy="-122" r="16" fill="none" stroke-width="4"/><circle class="d" cx="18" cy="-122" r="16" fill="none" stroke-width="4"/>'
          '<path class="d" d="M-2,-122 h4" stroke-width="4"/>') if glasses else ""
    return f'''<g class="body" stroke="{INK}" stroke-width="5" stroke-linecap="round" stroke-linejoin="round">
  <path class="d legs" d="{legs}" fill="none"/><path class="d" d="M-30,148 h-18 M30,148 h18" fill="none"/>
  <path class="d arms" d="{arms}" fill="none"/>
  <path class="d" d="M-34,-40 C-40,10 -34,70 -24,80 L24,80 C34,70 40,10 34,-40 C20,-56 -20,-56 -34,-40 Z" fill="{torso}"/>
  {extra}
  <g class="head"><circle class="d" cx="0" cy="-118" r="52" fill="{skin}"/>
  <g class="eyes"><circle cx="-17" cy="-124" r="5" fill="{INK}" stroke="none"/><circle cx="17" cy="-124" r="5" fill="{INK}" stroke="none"/></g>
  <g class="eyes-shut" opacity="0"><path d="M-25,-123 Q-17,-117 -9,-123 M9,-123 Q17,-117 25,-123" fill="none" stroke-width="4"/></g>
  <path class="d mouth" d="{mouth}" fill="{INK if face == 'shout' else 'none'}" stroke-width="4"/>{gl}{hair}{head_extra}</g></g>'''


def _tie(c):
    return f'<path d="M0,-52 L-10,-20 L0,30 L10,-20 Z" fill="{c}" stroke-width="3"/><path d="M-14,-52 L0,-36 L14,-52" fill="#fff" stroke-width="3"/>'


def _label(s, c, y=205):
    return f'<text class="label" x="0" y="{y}" text-anchor="middle" font-family="Cav" font-size="42" font-weight="700" fill="{c}">{s}</text>' if s else ""


CROSSED = "M-30,-20 C-20,10 10,10 30,-6 M30,-20 C20,10 -10,10 -30,-6"
POINT_R = "M-30,-20 L-56,40 M30,-20 L80,-50 L130,-70"
POINT_L = "M30,-20 L56,40 M-30,-20 L-80,-50 L-130,-70"
WAVE_R = "M-30,-20 L-56,40 M30,-20 L70,-70 L76,-110"
HOLD = "M-30,-20 L-50,20 L-20,30 M30,-20 L50,20 L20,30"
SHRUG = "M-30,-20 L-70,-10 L-80,-50 M30,-20 L70,-10 L80,-50"
CHEER = "M-30,-20 L-60,-80 M30,-20 L60,-80"

HAIR_JFK = '<path class="d" d="M-50,-140 C-44,-176 30,-184 52,-146 C30,-160 -10,-162 -50,-140 Z" fill="#6B4A2B"/>'
HAIR_RFK = '<path class="d" d="M-50,-138 C-46,-178 34,-182 52,-140 C40,-150 30,-138 10,-150 C-10,-140 -30,-150 -50,-138 Z" fill="#8a6a3a"/>'
HAIR_STICK = '<path class="d" d="M-24,-168 L-20,-188 M0,-170 L2,-192 M22,-168 L28,-188" fill="none"/>'
HAIR_SIDE = '<path class="d" d="M-50,-130 C-48,-150 -40,-160 -30,-164 M50,-130 C48,-150 40,-160 30,-164" fill="none" stroke-width="6"/>'
CASTRO_HEAD = (f'<path class="d" d="M-50,-128 C-52,-92 -30,-62 0,-60 C30,-62 52,-92 50,-128 C40,-100 20,-92 0,-92 C-20,-92 -40,-100 -50,-128 Z" fill="#3a2e22"/>'
               f'<path class="d" d="M-48,-150 C-40,-186 40,-186 48,-150 L56,-146 L-56,-146 Z" fill="{CU}"/>')
HELMET = f'<path class="d" d="M-56,-138 C-52,-190 52,-190 56,-138 Z" fill="#6f7d4f"/><path class="d" d="M-62,-138 h124" fill="none"/>'
NAVY_CAP = f'<path class="d" d="M-50,-150 C-46,-182 46,-182 50,-150 Z" fill="#fff"/><path class="d" d="M-56,-150 h112 l-10,10 h-92 Z" fill="{INK}"/>'
FUR_HAT = f'<path class="d" d="M-54,-140 C-58,-196 58,-196 54,-140 Z" fill="#7a5a3a"/><path class="d" d="M-60,-150 h120 v18 h-120 Z" fill="#a07a50"/>'


def person(pid, x, y, s, who, label=None, arms=None, face=None, hidden=True, lc=None):
    """who: jfk, rfk, khrushchev, castro, general, dobrynin, stevenson, savitsky, arkhipov, soldier, stick, officer"""
    P = {
        "jfk": dict(torso=US, hair=HAIR_JFK, extra=_tie(SU), face="flat", lab=("JFK", USD)),
        "rfk": dict(torso="#5a83c4", hair=HAIR_RFK, extra=_tie(US), face="flat", lab=("Robert Kennedy", USD)),
        "khrushchev": dict(torso=SU, extra=_tie(GOLD), face="frown", lab=("Khrushchev", SUD)),
        "castro": dict(torso=CU, hair=CASTRO_HEAD, extra='<path d="M-20,-30 h16 v14 h-16 Z M6,-30 h16 v14 h-16 Z" fill="#3f6f3c" stroke-width="3"/>', lab=("Castro", CUD)),
        "general": dict(torso="#6f7d4f", hair=HELMET, extra=f'<path d="M-24,-30 h14 M-24,-20 h14" stroke="{GOLD}" stroke-width="5"/>', face="frown", lab=("The Generals", "#4f5a35")),
        "dobrynin": dict(torso="#a3433a", hair=HAIR_SIDE, extra=_tie(INK), glasses=True, face="flat", lab=("Soviet Ambassador", SUD)),
        "stevenson": dict(torso="#2f5a96", hair=HAIR_SIDE, extra=_tie(SU), face="flat", lab=("US Ambassador", USD)),
        "savitsky": dict(torso="#30475e", hair=NAVY_CAP, extra=f'<path d="M-34,-10 h68 M-36,20 h72 M-34,50 h68" stroke="#fff" stroke-width="5"/>', face="frown", lab=("The Captain", SUD)),
        "arkhipov": dict(torso="#30475e", hair=NAVY_CAP, extra=f'<path d="M-20,-30 l8,8 l8,-8" stroke="{GOLD}" stroke-width="4" fill="none"/>', face="flat", lab=("Vasili Arkhipov", SUD)),
        "officer": dict(torso="#30475e", hair=NAVY_CAP, face="flat", lab=("", INK)),
        "soldier": dict(torso="#6f7d4f", hair=FUR_HAT, face="flat", lab=("", INK)),
        "stick": dict(torso="#E9E2D4", hair=HAIR_STICK, glasses=True, face="smile", lab=("", INK)),
    }[who]
    lab = P["lab"] if label is None else (label, P["lab"][1])
    if lc:
        lab = (lab[0], lc)
    inner = _person(P["torso"], hair=P.get("hair", ""), extra=P.get("extra", ""),
                    arms=arms or ("M-30,-20 L-56,40 M30,-20 L56,40" if who == "stick" else CROSSED if who in ("jfk", "khrushchev") else "M-30,-20 L-58,40 M30,-20 L58,40"),
                    face=face or P.get("face", "smile"), glasses=P.get("glasses", False)) + _label(*lab)
    return g(pid, x, y, s, inner, cls="char", hidden=hidden)


# ---------------------------------------------------------------- flags
def flag(fid, kind, x, y, s=1.0, pole=True, hidden=True):
    if kind == "us":
        cloth = "".join(f'<rect x="0" y="{i*12}" width="150" height="12" fill="{SU if i % 2 == 0 else "#fff"}"/>' for i in range(7))
        cloth += f'<rect x="0" y="0" width="62" height="48" fill="{US}"/>' + "".join(
            f'<circle cx="{10+(i%4)*14}" cy="{10+(i//4)*14}" r="2.5" fill="#fff"/>' for i in range(12))
        cloth += f'<rect x="0" y="0" width="150" height="84" fill="none" stroke="{INK}" stroke-width="4"/>'
    elif kind == "su":
        cloth = (f'<rect x="0" y="0" width="150" height="90" fill="{SU}" stroke="{INK}" stroke-width="4"/>'
                 f'<path d="M24,14 l4,10 l10,0 l-8,6 l3,10 l-9,-6 l-9,6 l3,-10 l-8,-6 l10,0 Z" fill="{GOLD}"/>'
                 f'<path d="M22,48 q14,10 26,-6 M30,40 l14,16" stroke="{GOLD}" stroke-width="5" fill="none" stroke-linecap="round"/>')
    elif kind == "cu":
        cloth = "".join(f'<rect x="0" y="{i*18}" width="150" height="18" fill="{US if i % 2 == 0 else "#fff"}"/>' for i in range(5))
        cloth += (f'<path d="M0,0 L66,45 L0,90 Z" fill="{SU}"/><path d="M20,36 l4,8 l9,0 l-7,6 l3,9 l-9,-6 l-8,6 l3,-9 l-7,-6 l9,0 Z" fill="#fff"/>'
                  f'<rect x="0" y="0" width="150" height="90" fill="none" stroke="{INK}" stroke-width="4"/>')
    elif kind == "tr":
        cloth = (f'<rect x="0" y="0" width="150" height="90" fill="{SU}" stroke="{INK}" stroke-width="4"/>'
                 f'<circle cx="58" cy="45" r="24" fill="#fff"/><circle cx="66" cy="45" r="19" fill="{SU}"/>'
                 f'<path d="M92,36 l3,7 l8,0 l-6,5 l2,8 l-7,-5 l-7,5 l2,-8 l-6,-5 l8,0 Z" fill="#fff"/>')
    p = f'<line x1="-4" y1="-6" x2="-4" y2="220" stroke="{INK}" stroke-width="6" stroke-linecap="round"/>' if pole else ""
    return g(fid, x, y, s, f'<g transform="rotate(-3)">{p}<g class="cloth">{cloth}</g></g>', hidden=hidden)


# ---------------------------------------------------------------- props
def ship(sid, x, y, c, s=1.0, flip=False, cargo=False, hidden=True):
    f = -1 if flip else 1
    cg = (f'<path d="M14,-4 C18,-10 26,-10 30,-4 Z M18,-4 L30,-26 L34,-24 L24,-4" fill="{SU}" stroke="{INK}" stroke-width="3"/>' if cargo else "")
    op = ' opacity="0"' if hidden else ""
    return (f'<g id="{sid}" class="ship" transform="translate({x},{y})"{op}><g class="hull" transform="scale({f*s},{s})">'
            f'<path d="M-46,0 L46,0 L32,20 L-34,20 Z" fill="{c}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
            f'<path d="M-14,0 v-20 h22 v20 M-4,-20 v-14" fill="none" stroke="{INK}" stroke-width="4"/>{cg}</g></g>')


def missile_shape(c=SU):
    return (f'<path d="M0,-40 C8,-28 9,-10 9,14 L-9,14 C-9,-10 -8,-28 0,-40 Z" fill="{c}" stroke="{INK}" stroke-width="3.5"/>'
            f'<path d="M-9,6 L-17,20 L-9,16 M9,6 L17,20 L9,16" fill="{c}" stroke="{INK}" stroke-width="3.5" stroke-linejoin="round"/>')


def missile(mid, x, y, s=1.1, c=SU, rot=0, hidden=True):
    return g(mid, x, y, s, f'<g transform="rotate({rot})">{missile_shape(c)}</g>', hidden=hidden)


def nuke(nid, x, y, s=1.0, hidden=True):
    blades = "".join(f'<path d="M0,0 L{30*math.cos(math.radians(a-30)):.1f},{30*math.sin(math.radians(a-30)):.1f} A30,30 0 0 1 {30*math.cos(math.radians(a+30)):.1f},{30*math.sin(math.radians(a+30)):.1f} Z" fill="{INK}"/>' for a in (-90, 30, 150))
    return g(nid, x, y, s, f'<circle r="36" fill="{GOLD}" stroke="{INK}" stroke-width="4"/>{blades}<circle r="8" fill="{GOLD}" stroke="{INK}" stroke-width="3"/>', hidden=hidden)


def table(tid, x, y, s=1.0, cloth=None, hidden=True):
    c = f'<path class="d" d="M-250,-20 L250,-20 L262,70 L-262,70 Z" fill="{cloth}"/>' if cloth else ""
    return g(tid, x, y, s, f'<g stroke="{INK}" stroke-width="6" stroke-linejoin="round" stroke-linecap="round">'
             f'<path class="d" d="M-200,0 L200,0 L240,-40 L-240,-40 Z" fill="{WOOD}"/><path class="d" d="M-200,0 V140 M200,0 V140" fill="none" stroke-width="7"/>{c}</g>', hidden=hidden)


def desk_lamp(lid, x, y, s=1.0, hidden=True):
    return g(lid, x, y, s, f'<path d="M-80,40 C-40,-60 60,-60 100,40 Z" fill="#fff6c8" opacity=".55"/>'
             f'<path d="M-30,0 h60 M0,0 V-90 L40,-140" stroke="{INK}" stroke-width="6" fill="none" stroke-linecap="round"/>'
             f'<path d="M20,-160 L80,-120 L50,-100 Z" fill="{GOLD}" stroke="{INK}" stroke-width="4"/>', hidden=hidden)


def tv(tid, x, y, s=1.0, inner="", hidden=True):
    return g(tid, x, y, s, f'''<rect x="-280" y="-210" width="560" height="420" rx="40" fill="#8A6A4A" stroke="{INK}" stroke-width="6"/>
  <rect x="-245" y="-175" width="420" height="320" rx="30" fill="#DCE6E4" stroke="{INK}" stroke-width="5"/>
  <circle cx="230" cy="-120" r="18" fill="#cbb" stroke="{INK}" stroke-width="4"/><circle cx="230" cy="-60" r="18" fill="#cbb" stroke="{INK}" stroke-width="4"/>
  <path d="M-160,-210 L-220,-290 M60,-210 L140,-290" stroke="{INK}" stroke-width="5" stroke-linecap="round"/>{inner}''', hidden=hidden)


def radio(rid, x, y, s=1.0, hidden=True):
    grille = "".join(f'<path d="M-110,{-40+i*16} h120" stroke="{INK}" stroke-width="3"/>' for i in range(6))
    return g(rid, x, y, s, f'<rect x="-150" y="-90" width="300" height="180" rx="30" fill="{WOOD}" stroke="{INK}" stroke-width="6"/>'
             f'<rect x="-120" y="-60" width="140" height="120" rx="12" fill="#e9dcc0" stroke="{INK}" stroke-width="4"/>{grille}'
             f'<circle cx="80" cy="-20" r="26" fill="#e9dcc0" stroke="{INK}" stroke-width="4"/><circle cx="80" cy="45" r="18" fill="#e9dcc0" stroke="{INK}" stroke-width="4"/>'
             f'<g class="waves" stroke="{INK}" stroke-width="5" fill="none" stroke-linecap="round"><path d="M170,-60 q30,60 0,120"/><path d="M200,-90 q45,90 0,180"/></g>', hidden=hidden)


def letter(lid, x, y, label, sub="", s=1.0, rot=0, color=SU, hidden=True):
    lines = "".join(f'<path d="M-90,{-30+i*24} h{180 - (i % 3) * 30}" stroke="{GREY}" stroke-width="4" stroke-linecap="round"/>' for i in range(5))
    return g(lid, x, y, s, f'<g transform="rotate({rot})"><path d="M-120,-140 h240 v280 h-240 Z" fill="#fff" stroke="{INK}" stroke-width="5"/>'
             f'<text x="0" y="-80" text-anchor="middle" font-family="Cav" font-weight="700" font-size="44" fill="{color}">{label}</text>{lines}'
             f'<text x="0" y="120" text-anchor="middle" font-family="Cav" font-weight="700" font-size="36" fill="{INK}">{sub}</text></g>', hidden=hidden)


def envelope(eid, x, y, s=1.0, label="", hidden=True):
    return g(eid, x, y, s, f'<rect x="-90" y="-60" width="180" height="120" rx="8" fill="#fff" stroke="{INK}" stroke-width="5"/>'
             f'<path d="M-90,-60 L0,10 L90,-60" fill="none" stroke="{INK}" stroke-width="5"/><circle cx="0" cy="10" r="16" fill="{SU}" stroke="{INK}" stroke-width="3"/>'
             + (f'<text x="0" y="110" text-anchor="middle" font-family="Cav" font-weight="700" font-size="44" fill="{INK}">{label}</text>' if label else ""), hidden=hidden)


def submarine_icon(sid, x, y, s=1.0, c="#4f5d66", label="", hidden=True):
    return g(sid, x, y, s, f'<path d="M-150,0 C-150,-40 150,-40 170,0 C150,40 -150,40 -150,0 Z" fill="{c}" stroke="{INK}" stroke-width="5"/>'
             f'<path d="M-20,-28 v-40 h60 v40" fill="{c}" stroke="{INK}" stroke-width="5"/><path d="M10,-68 v-30 h20" fill="none" stroke="{INK}" stroke-width="5"/>'
             f'<path d="M-150,0 l-30,-26 v52 Z" fill="{c}" stroke="{INK}" stroke-width="5"/>'
             + "".join(f'<circle cx="{-80+i*50}" cy="0" r="9" fill="#cfe0e3" stroke="{INK}" stroke-width="3"/>' for i in range(4))
             + (f'<text x="0" y="80" text-anchor="middle" font-family="Cav" font-weight="700" font-size="44" fill="{INK}">{label}</text>' if label else ""), hidden=hidden)


def destroyer(did, x, y, s=1.0, hidden=True):
    return g(did, x, y, s, f'<path d="M-140,0 L150,0 L120,40 L-120,40 Z" fill="{US}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
             f'<path d="M-60,0 v-40 h70 v40 M-30,-40 v-40 M40,0 v-24 h50 v24" fill="{GREY}" stroke="{INK}" stroke-width="5"/>', hidden=hidden)


def u2(pid, x, y, s=1.0, rot=0, hidden=True):
    return g(pid, x, y, s, f'<g transform="rotate({rot})"><path d="M-110,0 C-60,-12 80,-12 120,0 C80,12 -60,12 -110,0 Z" fill="#8f9aa0" stroke="{INK}" stroke-width="4"/>'
             f'<path d="M-10,-6 L-40,-140 L-20,-140 L30,-6 M-10,6 L-40,140 L-20,140 L30,6" fill="#aeb8bd" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/>'
             f'<path d="M-100,-2 L-130,-40 L-118,-40 L-86,-4 M-100,2 L-130,40 L-118,40 L-86,4" fill="#aeb8bd" stroke="{INK}" stroke-width="4"/>'
             f'<path d="M80,-6 q14,6 0,12" fill="#cfe0e3" stroke="{INK}" stroke-width="3"/></g>', hidden=hidden)


def jet(jid, x, y, s=1.0, rot=0, c=SU, hidden=True):
    return g(jid, x, y, s, f'<g transform="rotate({rot})"><path d="M-60,0 L60,-6 L80,0 L60,6 Z" fill="{c}" stroke="{INK}" stroke-width="4"/>'
             f'<path d="M0,-4 L-30,-50 L-12,-50 L24,-4 M0,4 L-30,50 L-12,50 L24,4 M-50,-2 L-70,-26 L-58,-26 L-40,-2" fill="{c}" stroke="{INK}" stroke-width="4" stroke-linejoin="round"/></g>', hidden=hidden)


def explosion(xid, x, y, s=1.0, hidden=True):
    pts = " ".join(f"{(70 if i % 2 == 0 else 36)*math.cos(math.radians(i*30)):.1f},{(70 if i % 2 == 0 else 36)*math.sin(math.radians(i*30)):.1f}" for i in range(12))
    pts2 = " ".join(f"{(40 if i % 2 == 0 else 20)*math.cos(math.radians(i*30+15)):.1f},{(40 if i % 2 == 0 else 20)*math.sin(math.radians(i*30+15)):.1f}" for i in range(12))
    return g(xid, x, y, s, f'<polygon points="{pts}" fill="#F2A33A" stroke="{INK}" stroke-width="4"/><polygon points="{pts2}" fill="#FCE38A"/>', hidden=hidden)


def lightbulb(lid, x, y, s=1.0, hidden=True):
    rays = "".join(f'<path d="M{48*math.cos(math.radians(a)):.0f},{-20+48*math.sin(math.radians(a)):.0f} l{14*math.cos(math.radians(a)):.0f},{14*math.sin(math.radians(a)):.0f}" stroke="{INK}" stroke-width="4"/>' for a in range(-180, 1, 45))
    return g(lid, x, y, s, f'<path d="M-26,0 C-50,-30 -30,-64 0,-64 C30,-64 50,-30 26,0 Z" fill="#FCE38A" stroke="{INK}" stroke-width="4"/>'
             f'<rect x="-16" y="0" width="32" height="20" fill="{GREY}" stroke="{INK}" stroke-width="4"/>{rays}', hidden=hidden)


def steam(sid, x, y, s=1.0, hidden=True):
    return g(sid, x, y, s, f'<g fill="#fff" stroke="{INK}" stroke-width="3"><circle cx="0" cy="0" r="14"/><circle cx="16" cy="-18" r="18"/><circle cx="-8" cy="-40" r="20"/></g>', hidden=hidden)


def thermometer(tid, x, y, s=1.0, hidden=True):
    return g(tid, x, y, s, f'<rect x="-18" y="-160" width="36" height="180" rx="18" fill="#fff" stroke="{INK}" stroke-width="5"/>'
             f'<circle cx="0" cy="40" r="34" fill="{SU}" stroke="{INK}" stroke-width="5"/>'
             f'<rect class="mercury" x="-8" y="-40" width="16" height="70" fill="{SU}"/>', hidden=hidden)


def progress(pid, x, y, label, w=600, hidden=True):
    return (f'<g id="{pid}" transform="translate({x},{y})"{" opacity=\"0\"" if hidden else ""}><text x="0" y="-24" text-anchor="middle" font-family="Cav" font-weight="700" font-size="48" fill="{SU}">{label}</text>'
            f'<rect x="{-w/2}" y="0" width="{w}" height="50" rx="14" fill="#fff" stroke="{INK}" stroke-width="5"/>'
            f'<rect class="fill" x="{-w/2+6}" y="6" width="{w-12}" height="38" rx="10" fill="{SU}" transform="scale(0,1)" transform-origin="{-w/2+6} 0"/></g>')


def newspaper(nid, x, y, head, s=1.0, rot=0, hidden=True):
    lines = "".join(f'<path d="M-170,{30+i*26} h{150 if i % 2 else 340}" stroke="{GREY}" stroke-width="5" stroke-linecap="round"/>' for i in range(5))
    return g(nid, x, y, s, f'<g transform="rotate({rot})"><rect x="-190" y="-130" width="380" height="290" fill="#fbf8f0" stroke="{INK}" stroke-width="5"/>'
             f'<text x="0" y="-95" text-anchor="middle" font-family="Cav" font-weight="700" font-size="30" fill="{INK2}">THE DAILY NEWS - OCT 29, 1962</text>'
             f'<path d="M-170,-80 h340" stroke="{INK}" stroke-width="3"/>'
             f'<text x="0" y="-20" text-anchor="middle" font-family="Cav" font-weight="700" font-size="46" fill="{INK}">{head}</text>{lines}</g>', hidden=hidden)


def phone(pid, x, y, s=1.0, c=SU, hidden=True):
    return g(pid, x, y, s, f'<path d="M-70,30 L-50,-10 H50 L70,30 Z" fill="{c}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>'
             f'<path class="handset" d="M-70,-30 C-70,-56 70,-56 70,-30 L50,-20 C30,-34 -30,-34 -50,-20 Z" fill="{c}" stroke="{INK}" stroke-width="5"/>'
             f'<circle cx="0" cy="8" r="12" fill="#fff" stroke="{INK}" stroke-width="3"/>', hidden=hidden)


def scroll(sid, x, y, title, sub="", s=1.0, hidden=True):
    return g(sid, x, y, s, f'<path d="M-200,-120 H200 V120 H-200 Z" fill="#fbf3dc" stroke="{INK}" stroke-width="5"/>'
             f'<path d="M-200,-120 c-30,0 -30,30 0,30 M200,120 c30,0 30,-30 0,-30" fill="#e9d9b0" stroke="{INK}" stroke-width="5"/>'
             f'<text x="0" y="-40" text-anchor="middle" font-family="Cav" font-weight="700" font-size="40" fill="{INK}">{title}</text>'
             f'<text x="0" y="20" text-anchor="middle" font-family="Cav" font-weight="400" font-size="38" fill="{INK2}">{sub}</text>'
             f'<path d="M60,80 c20,-30 40,20 70,-10" stroke="{US}" stroke-width="4" fill="none"/><path d="M-140,80 c20,-30 40,20 70,-10" stroke="{SU}" stroke-width="4" fill="none"/>', hidden=hidden)


def calendar(cid, x, y, label, sub="", s=1.0, hidden=True):
    return g(cid, x, y, s, f'<rect x="-120" y="-110" width="240" height="230" rx="16" fill="#fff" stroke="{INK}" stroke-width="5"/>'
             f'<path d="M-120,-110 h240 v60 h-240 Z" fill="{SU}" stroke="{INK}" stroke-width="5"/>'
             f'<text x="0" y="-66" text-anchor="middle" font-family="Cav" font-weight="700" font-size="40" fill="#fff">{sub}</text>'
             f'<text class="num" x="0" y="70" text-anchor="middle" font-family="Cav" font-weight="700" font-size="120" fill="{INK}">{label}</text>', hidden=hidden)


def clover(cid, x, y, s=1.0, hidden=True):
    leaves = "".join(f'<circle cx="{26*math.cos(math.radians(a)):.0f}" cy="{26*math.sin(math.radians(a)):.0f}" r="26" fill="#5fae55" stroke="{INK}" stroke-width="4"/>' for a in (45, 135, 225, 315))
    return g(cid, x, y, s, f'<path d="M0,0 C10,40 20,60 40,80" stroke="{INK}" stroke-width="6" fill="none"/>{leaves}', hidden=hidden)


def red_button(bid, x, y, s=1.0, hidden=True):
    return g(bid, x, y, s, f'<rect x="-90" y="10" width="180" height="40" rx="10" fill="{GREY}" stroke="{INK}" stroke-width="5"/>'
             f'<path d="M-60,10 C-60,-40 60,-40 60,10 Z" fill="{SU}" stroke="{INK}" stroke-width="5"/>'
             f'<g class="hand"><path d="M-20,-200 C-24,-150 -20,-120 -10,-90 L14,-90 C20,-120 24,-150 20,-200 Z" fill="{SKIN}" stroke="{INK}" stroke-width="5"/></g>', hidden=hidden)


def palm(pid, x, y, s=1.0, hidden=True):
    leaves = "".join(f'<path d="M0,-200 q{60*math.cos(math.radians(a))},{-30+60*math.sin(math.radians(a))} {120*math.cos(math.radians(a)):.0f},{120*math.sin(math.radians(a))+20:.0f}" stroke="#3f8a3a" stroke-width="16" fill="none" stroke-linecap="round"/>' for a in (-160, -120, -60, -20, 200))
    return g(pid, x, y, s, f'<path d="M0,0 C-10,-80 10,-140 0,-200" stroke="#8a6a3a" stroke-width="22" fill="none" stroke-linecap="round"/>{leaves}', hidden=hidden)


def skis(sid, x, y, s=1.0, hidden=True):
    return g(sid, x, y, s, f'<path d="M-20,60 L-10,-160 q2,-20 10,-10 M20,60 L30,-160 q2,-20 10,-10" stroke="{SU}" stroke-width="12" fill="none" stroke-linecap="round"/>', hidden=hidden)


def snowflake(sid, x, y, s=1.0, hidden=True):
    arms = "".join(f'<path d="M0,0 L{40*math.cos(math.radians(a)):.0f},{40*math.sin(math.radians(a)):.0f}" stroke="#7fb3d5" stroke-width="7" stroke-linecap="round"/>' for a in range(0, 360, 60))
    return g(sid, x, y, s, arms, hidden=hidden)


def magnifier(mid, x, y, s=1.0, hidden=True):
    return g(mid, x, y, s, f'<circle r="70" fill="#ffffff55" stroke="{INK}" stroke-width="10"/><path d="M50,50 L130,130" stroke="{WOOD}" stroke-width="22" stroke-linecap="round"/>', hidden=hidden)


def photo(pid, x, y, s=1.0, caption="MISSILE SITE", hidden=True):
    blobs = "".join(f'<ellipse cx="{-60+i*60}" cy="{10+(i%2)*20}" rx="24" ry="8" fill="#ece6d4" stroke="{INK}" stroke-width="2"/>' for i in range(3))
    return g(pid, x, y, s, f'<rect x="-180" y="-130" width="360" height="260" fill="#fff" stroke="{INK}" stroke-width="5"/>'
             f'<rect x="-160" y="-110" width="320" height="180" fill="#8f9a86"/>{blobs}'
             f'<path d="M-140,-80 q60,20 120,-10 t120,20" stroke="#6f7a66" stroke-width="6" fill="none"/>'
             f'<text x="0" y="110" text-anchor="middle" font-family="Cav" font-weight="700" font-size="38" fill="{SU}">{caption}</text>', hidden=hidden)


def domino(did, x, y, label, s=1.0, hidden=True):
    return (f'<g id="{did}" transform="translate({x},{y})"{" opacity=\"0\"" if hidden else ""}><g class="tile" transform="scale({s})">'
            f'<rect x="-50" y="-220" width="100" height="220" rx="10" fill="#fff" stroke="{INK}" stroke-width="6"/>'
            f'<text x="0" y="-100" text-anchor="middle" font-family="Cav" font-weight="700" font-size="40" fill="{SU}" transform="rotate(-90 0 -100)">{label}</text></g></g>')


def podium(pid, x, y, s=1.0, hidden=True):
    return g(pid, x, y, s, f'<path d="M-90,0 L90,0 L70,160 L-70,160 Z" fill="{WOOD}" stroke="{INK}" stroke-width="6"/>'
             f'<path d="M-30,0 V-40 M30,0 V-40" stroke="{INK}" stroke-width="5"/><circle cx="-30" cy="-46" r="9" fill="{INK}"/><circle cx="30" cy="-46" r="9" fill="{INK}"/>'
             f'<circle cx="0" cy="70" r="30" fill="#fff" stroke="{INK}" stroke-width="4"/><path d="M-12,70 l8,10 l16,-20" stroke="{US}" stroke-width="4" fill="none"/>', hidden=hidden)


def easel(eid, x, y, s=1.0, hidden=True):
    return g(eid, x, y, s, f'<path d="M-120,200 L-40,-120 M120,200 L40,-120 M0,-150 V200" stroke="{WOOD}" stroke-width="12" stroke-linecap="round"/>'
             + photo("", 0, -10, 1.0, hidden=False).replace('id=""', ''), hidden=hidden)


def mic(mid, x, y, s=1.0, hidden=True):
    return g(mid, x, y, s, f'<path d="M0,0 V140 M-50,140 h100" stroke="{INK}" stroke-width="8" stroke-linecap="round"/>'
             f'<rect x="-28" y="-80" width="56" height="90" rx="28" fill="{GREY}" stroke="{INK}" stroke-width="5"/>'
             + "".join(f'<path d="M-20,{-56+i*18} h40" stroke="{INK}" stroke-width="3"/>' for i in range(4)), hidden=hidden)


def rewind(rid, x, y, s=1.0, hidden=True):
    return g(rid, x, y, s, f'<circle r="130" fill="#fff" stroke="{INK}" stroke-width="8"/><path d="M10,-60 L-60,0 L10,60 Z M80,-60 L10,0 L80,60 Z" fill="{SU}" stroke="{INK}" stroke-width="5" stroke-linejoin="round"/>', hidden=hidden)


def binoculars(bid, x, y, s=1.0, hidden=True):
    return g(bid, x, y, s, f'<rect x="-50" y="-26" width="40" height="52" rx="12" fill="{INK2}" stroke="{INK}" stroke-width="4"/><rect x="10" y="-26" width="40" height="52" rx="12" fill="{INK2}" stroke="{INK}" stroke-width="4"/><rect x="-14" y="-12" width="28" height="20" fill="{INK2}" stroke="{INK}" stroke-width="4"/>', hidden=hidden)


def dashed_arrow(aid, d, color=SU, width=6, head=None, hidden=True):
    hd = f'<path d="{head}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round"/>' if head else ""
    return (f'<g id="{aid}"{" opacity=\"0\"" if hidden else ""}><path class="d" d="{d}" fill="none" stroke="{color}" stroke-width="{width}" stroke-linecap="round"/>{hd}</g>')


# ---------------------------------------------------------------- maps
CARIB_USA = ("M0,0 L1920,0 L1920,210 C1790,240 1660,270 1560,330 C1470,380 1400,420 1330,450 C1290,470 1265,510 1250,560 "
             "C1250,560 1236,620 1220,660 C1206,692 1182,700 1164,692 C1140,680 1124,640 1110,600 C1096,560 1070,520 1040,505 "
             "C1020,496 1005,494 990,492 C900,480 800,470 700,480 C560,494 420,520 300,540 C180,560 80,560 0,550 Z")
CARIB_CUBA = ("M640,792 C700,770 780,764 860,772 C930,778 990,790 1050,808 C1110,826 1170,842 1230,846 C1280,850 1330,862 1350,880 "
              "C1320,890 1270,884 1220,878 C1150,870 1080,860 1010,846 C930,830 850,818 780,814 C720,810 670,808 640,792 Z")
Q_CENTER, Q_RX, Q_RY = (990, 895), 540, 185
Q_ANGLES = [190, 215, 245, 295, 325, 350, 20]


def qpos(a):
    return Q_CENTER[0] + Q_RX * math.cos(math.radians(a)), Q_CENTER[1] + Q_RY * math.sin(math.radians(a)) + 10


def caribbean_map(labels=True, dc=True, sea_names=True):
    """Florida/Cuba map. ids: map, usa, cuba, maplabels, seanames, dc, legend."""
    return f'''<rect width="1920" height="1080" fill="{SEA}"/>
<g id="map" filter="url(#rough)">
  <path id="usa" class="d" d="{CARIB_USA}" fill="{USLAND}" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>
  <path id="cuba" class="d" d="{CARIB_CUBA}" fill="{CULAND}" stroke="{INK}" stroke-width="6" stroke-linejoin="round"/>
</g>
<g id="seanames" font-family="Cav" font-weight="400" font-style="italic" font-size="42" fill="#5d7f86" opacity="0"><text x="420" y="700">Gulf of Mexico</text><text x="1560" y="560">Atlantic Ocean</text></g>
<g id="maplabels" font-family="Cav" font-weight="700" opacity="0">
  <text x="620" y="300" text-anchor="middle" font-size="96" fill="{USD}">USA</text>
  <text x="1330" y="640" text-anchor="middle" font-size="44" fill="{USD}">Florida</text>
  <text x="1000" y="935" text-anchor="middle" font-size="64" fill="{CUD}">CUBA</text>
</g>
<g id="dc" opacity="0"><path transform="translate(1520,150)" d="M0,-22 l6,14 l16,0 l-12,10 l5,15 l-15,-9 l-15,9 l5,-15 l-12,-10 l16,0 Z" fill="{SU}" stroke="{INK}" stroke-width="3"/>
  <text x="1520" y="215" text-anchor="middle" font-family="Cav" font-weight="700" font-size="44" fill="{INK}">Washington D.C.</text></g>
{legend()}'''


def legend(entries=None):
    entries = entries or [(USLAND, "United States"), (SU, "Soviet Union"), (CULAND, "Cuba")]
    h = 30 + 40 * len(entries)
    rows = "".join(f'<rect x="1585" y="{64+i*40}" width="34" height="24" fill="{c}" stroke="{INK}" stroke-width="3"/><text x="1632" y="{86+i*40}" fill="{INK}">{t}</text>'
                   for i, (c, t) in enumerate(entries))
    return f'<g id="legend" font-family="Cav" font-weight="700" font-size="34" opacity="0"><rect x="1560" y="40" width="320" height="{h}" rx="12" fill="{BG}" stroke="{INK}" stroke-width="3"/>{rows}</g>'


# Stylised world (not to scale): Americas left, Europe/USSR right
WORLD_NA = ("M120,180 C220,120 420,110 560,150 C640,170 700,230 690,300 C680,360 620,400 600,450 C590,500 560,540 520,560 "
            "C480,580 450,610 430,650 C410,690 380,700 360,670 C330,620 290,590 250,560 C200,520 170,450 160,380 C150,300 110,240 120,180 Z")
WORLD_SA = "M470,700 C520,690 590,720 620,780 C650,840 620,920 580,980 C550,1030 520,1060 500,1040 C480,980 470,900 460,840 C450,780 440,720 470,700 Z"
WORLD_EU = ("M960,250 C1000,220 1060,210 1100,230 C1120,260 1110,300 1080,320 C1050,340 1060,380 1040,410 C1010,440 970,430 950,400 "
            "C930,370 940,330 930,300 C925,280 940,262 960,250 Z")
WORLD_USSR = ("M1100,180 C1250,120 1500,100 1700,130 C1820,150 1880,200 1870,260 C1860,320 1780,350 1680,360 C1560,372 1440,380 1340,400 "
              "C1260,416 1180,420 1130,400 C1090,380 1080,340 1090,300 C1100,260 1080,220 1100,180 Z")
WORLD_AF = "M980,470 C1060,450 1150,470 1190,530 C1230,600 1210,700 1160,780 C1120,850 1080,900 1050,880 C1010,820 990,740 960,680 C930,620 930,520 980,470 Z"
WORLD_CU = "M470,640 C500,632 540,634 570,646 C540,652 500,650 470,640 Z"
WORLD_TR = "M1110,430 C1150,420 1210,420 1250,432 C1240,452 1190,460 1140,456 C1120,452 1108,444 1110,430 Z"


def world_map():
    return f'''<rect width="1920" height="1080" fill="{SEA}"/>
<g id="map" filter="url(#rough)" stroke="{INK}" stroke-width="5" stroke-linejoin="round">
  <path id="w_na" class="d" d="{WORLD_NA}" fill="{USLAND}"/><path class="d" d="{WORLD_SA}" fill="#e7dcc6"/>
  <path class="d" d="{WORLD_EU}" fill="#e7dcc6"/><path class="d" d="{WORLD_AF}" fill="#e7dcc6"/>
  <path id="w_ussr" class="d" d="{WORLD_USSR}" fill="{SULAND}"/><path id="w_cu" class="d" d="{WORLD_CU}" fill="{CULAND}"/>
  <path id="w_tr" class="d" d="{WORLD_TR}" fill="{TR}"/>
</g>
<g id="worldlabels" font-family="Cav" font-weight="700" opacity="0">
  <text x="400" y="330" text-anchor="middle" font-size="80" fill="{USD}">USA</text>
  <text x="1500" y="270" text-anchor="middle" font-size="80" fill="{SUD}">SOVIET UNION</text>
</g>'''


TURKEY = ("M380,700 C520,660 760,650 980,660 C1160,668 1360,690 1520,720 C1560,760 1520,820 1440,840 C1300,870 1100,880 900,870 "
          "C720,862 540,850 420,820 C360,800 340,740 380,700 Z")
BLACK_SEA = "M560,600 C640,520 860,470 1100,480 C1300,490 1460,540 1480,610 C1420,650 1250,650 1050,640 C850,632 680,650 560,600 Z"


def turkey_map():
    """Close-up: Soviet Union above the Black Sea, Turkey below."""
    return f'''<rect width="1920" height="1080" fill="{SULAND}"/>
<g id="map" filter="url(#rough)" stroke="{INK}" stroke-width="6" stroke-linejoin="round">
  <path class="d" d="{BLACK_SEA}" fill="{SEA}"/>
  <path id="turkey" class="d" d="{TURKEY}" fill="{TR}"/>
  <path class="d" d="M0,930 C300,900 700,920 1000,950 C1300,980 1600,960 1920,940 L1920,1080 L0,1080 Z" fill="{SEA}"/>
</g>
<g id="tklabels" font-family="Cav" font-weight="700" opacity="0">
  <text x="1180" y="790" text-anchor="middle" font-size="72" fill="#7a6420">TURKEY</text>
  <text x="1000" y="580" text-anchor="middle" font-size="44" font-style="italic" font-weight="400" fill="#5d7f86">Black Sea</text>
  <text x="400" y="200" text-anchor="middle" font-size="72" fill="{SUD}">SOVIET UNION</text>
</g>
<g id="moscow" opacity="0"><path transform="translate(1180,170)" d="M0,-26 l7,16 l18,0 l-14,11 l6,17 l-17,-10 l-17,10 l6,-17 l-14,-11 l18,0 Z" fill="{SUD}" stroke="{INK}" stroke-width="3"/>
  <text x="1180" y="240" text-anchor="middle" font-family="Cav" font-weight="700" font-size="54" fill="{INK}">Moscow</text></g>'''


ATL_USA = "M0,0 L760,0 C720,120 640,220 560,300 C500,360 470,420 430,480 C410,520 380,540 340,520 C300,500 260,470 200,470 C120,470 60,500 0,520 Z"
ATL_CUBA = "M220,700 C280,684 360,686 420,700 C470,712 520,730 560,746 C520,756 460,748 400,738 C330,726 260,720 220,700 Z"
ATL_EU = "M1300,0 L1920,0 L1920,700 C1850,690 1780,640 1720,600 C1660,560 1620,500 1560,470 C1500,440 1440,420 1400,380 C1360,330 1330,260 1320,200 C1310,120 1300,60 1300,0 Z"


def atlantic_map():
    return f'''<rect width="1920" height="1080" fill="{SEA}"/>
<g id="map" filter="url(#rough)" stroke="{INK}" stroke-width="6" stroke-linejoin="round">
  <path class="d" d="{ATL_USA}" fill="{USLAND}"/><path class="d" d="{ATL_CUBA}" fill="{CULAND}"/>
  <path class="d" d="{ATL_EU}" fill="{SULAND}"/>
</g>
<g id="atlabels" font-family="Cav" font-weight="700" opacity="0">
  <text x="300" y="250" text-anchor="middle" font-size="72" fill="{USD}">USA</text>
  <text x="390" y="800" text-anchor="middle" font-size="56" fill="{CUD}">CUBA</text>
  <text x="1660" y="250" text-anchor="middle" font-size="64" fill="{SUD}">SOVIET UNION</text>
  <text x="1000" y="560" text-anchor="middle" font-size="56" font-style="italic" font-weight="400" fill="#5d7f86">Atlantic Ocean</text>
</g>'''


ARC_ALASKA = "M0,300 C120,280 260,300 360,360 C420,400 470,470 520,560 C560,640 600,720 620,820 L620,1080 L0,1080 Z"
ARC_USSR = "M1100,1080 C1100,940 1140,820 1200,720 C1260,620 1340,540 1440,480 C1560,410 1720,380 1920,370 L1920,1080 Z"


def arctic_map():
    return f'''<rect width="1920" height="1080" fill="#dfeaf0"/>
<g id="map" filter="url(#rough)" stroke="{INK}" stroke-width="6" stroke-linejoin="round">
  <path class="d" d="M0,0 L1920,0 L1920,260 C1600,230 1300,250 1000,220 C700,190 400,220 0,200 Z" fill="#ffffff"/>
  <path class="d" d="{ARC_ALASKA}" fill="{USLAND}"/><path class="d" d="{ARC_USSR}" fill="{SULAND}"/>
</g>
<path id="border" d="M860,1080 C880,800 900,560 940,260" stroke="{INK}" stroke-width="5" stroke-dasharray="18 14" fill="none" opacity="0"/>
<g id="arclabels" font-family="Cav" font-weight="700" opacity="0">
  <text x="250" y="560" text-anchor="middle" font-size="64" fill="{USD}">ALASKA (USA)</text>
  <text x="1560" y="700" text-anchor="middle" font-size="64" fill="{SUD}">SOVIET UNION</text>
  <text x="960" y="130" text-anchor="middle" font-size="56" font-style="italic" font-weight="400" fill="#5d7f86">The Arctic</text>
</g>'''


# ---------------------------------------------------------------- page shell + JS helpers
HELPERS = r"""
var tl = gsap.timeline({ paused: true });
gsap.set("#cam", { svgOrigin: "0 0" });
var SHAPES = "path,circle,rect,line,ellipse,polygon,polyline,text";
function prep(sel) {
  document.querySelectorAll(sel).forEach(function (root) {
    root.style.opacity = 0;
    root.querySelectorAll(SHAPES).forEach(function (el) {
      if (el.closest(".eyes-shut")) return;
      if (el.classList.contains("d") && el.getTotalLength) {
        var len = el.getTotalLength(); el.style.strokeDasharray = len + " " + len; el.style.strokeDashoffset = len;
        var f = el.getAttribute("fill"); if (f && f !== "none") el.style.fillOpacity = 0;
      } else if (!el.closest(".d")) { el.classList.add("late"); el.style.opacity = 0; }
    });
  });
}
function drawIn(sel, t, d) {
  d = d || 1.0;
  tl.set(sel, { opacity: 1 }, t);
  tl.to(sel + " .d", { strokeDashoffset: 0, duration: d, ease: "power1.inOut", stagger: d / 14 }, t);
  tl.to(sel + " .d", { fillOpacity: 1, duration: d * 0.45 }, t + d * 0.6);
  tl.to(sel + " .late", { opacity: 1, duration: d * 0.35 }, t + d * 0.65);
}
function pop(sel, t, d) { tl.fromTo(sel, { opacity: 0, scale: 0.2, transformOrigin: "50% 50%" }, { opacity: 1, scale: 1, duration: d || 0.45, ease: "back.out(2)" }, t); }
function popOut(sel, t, d) { tl.to(sel, { opacity: 0, scale: 0.2, transformOrigin: "50% 50%", duration: d || 0.3, ease: "back.in(2)" }, t); }
function fadeIn(sel, t, d) { tl.fromTo(sel, { opacity: 0, y: "+=14" }, { opacity: 1, y: "-=14", duration: d || 0.4, ease: "power2.out" }, t); }
function show(sel, t, d) { tl.fromTo(sel, { opacity: 0 }, { opacity: 1, duration: d || 0.35 }, t); }
function fadeOut(sel, t, d) { tl.to(sel, { opacity: 0, duration: d || 0.3 }, t); }
function slideIn(sel, t, dx, dy, d) { tl.fromTo(sel, { opacity: 0, x: "+=" + (dx || 0), y: "+=" + (dy || 0) }, { opacity: 1, x: "-=" + (dx || 0), y: "-=" + (dy || 0), duration: d || 0.5, ease: "power2.out" }, t); }
function move(sel, t, dx, dy, d, ease) { tl.to(sel, { x: "+=" + (dx || 0), y: "+=" + (dy || 0), duration: d || 1, ease: ease || "power1.inOut" }, t); }
function stampIn(sel, t) { tl.fromTo(sel, { opacity: 0, scale: 2.4, transformOrigin: "50% 50%" }, { opacity: 1, scale: 1, duration: 0.22, ease: "power3.in" }, t); }
function wobble(sel, t, n, deg, origin) { tl.to(sel, { rotation: deg || 8, transformOrigin: origin || "50% 100%", yoyo: true, repeat: (n || 3) * 2 - 1, duration: 0.14, ease: "sine.inOut" }, t); }
function bob(sel, t, n, dy) { tl.to(sel, { y: "-=" + (dy || 14), yoyo: true, repeat: (n || 3) * 2 - 1, duration: 0.18, ease: "sine.inOut" }, t); }
function blink(sel, t) {
  tl.set(sel + " .eyes", { opacity: 0 }, t); tl.set(sel + " .eyes-shut", { opacity: 1 }, t);
  tl.set(sel + " .eyes", { opacity: 1 }, t + 0.22); tl.set(sel + " .eyes-shut", { opacity: 0 }, t + 0.22);
}
function zoom(x, y, s, t, d) {
  var tx = s <= 1 ? (1 - s) * 960 : Math.min(0, Math.max(1920 - 1920 * s, 960 - x * s));
  var ty = s <= 1 ? (1 - s) * 540 : Math.min(0, Math.max(1080 - 1080 * s, 540 - y * s));
  tl.to("#cam", { scale: s, x: tx, y: ty, duration: d || 0.8, ease: "power2.inOut" }, t);
}
function shake(t, n) { tl.to("#cam", { x: "+=10", duration: 0.04, yoyo: true, repeat: (n || 4) * 2 - 1, ease: "none" }, t); }
function darken(t, a, d) { tl.to("#shade", { opacity: a, duration: d || 0.6 }, t); }
"""


def page(scene_id, duration, svg_body, js, bg=BG, lines=True, overlay=""):
    """Full HTML document. svg_body goes inside the camera group; overlay sits above it (screen space)."""
    ruled = '<rect width="1920" height="1080" fill="url(#lines)"/>' if lines else ""
    return f'''<!DOCTYPE html><html lang="en"><head><meta charset="UTF-8"><title>Scene {scene_id}</title>
<script>{_gsap()}</script>
<style>@font-face{{font-family:Cav;src:url(data:font/ttf;base64,{_font(700)}) format('truetype');font-weight:700}}
@font-face{{font-family:Cav;src:url(data:font/ttf;base64,{_font(400)}) format('truetype');font-weight:400}}
*{{margin:0;padding:0}} body{{width:1920px;height:1080px;overflow:hidden;background:{bg}}} svg{{display:block}}</style></head>
<body data-composition-id="scene-{scene_id}" data-width="1920" data-height="1080" data-fps="30" data-duration="{duration}" data-start="0">
<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 1920 1080">
<defs><filter id="rough"><feTurbulence type="fractalNoise" baseFrequency="0.025" numOctaves="2" seed="3"/><feDisplacementMap in="SourceGraphic" scale="3"/></filter>
<pattern id="lines" width="1920" height="54" patternUnits="userSpaceOnUse"><line x1="0" y1="53" x2="1920" y2="53" stroke="{LINE}" stroke-width="2"/></pattern>
<radialGradient id="spot" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="#fff8d0" stop-opacity=".9"/><stop offset="100%" stop-color="#fff8d0" stop-opacity="0"/></radialGradient></defs>
<rect width="1920" height="1080" fill="{bg}"/>{ruled}
<g id="cam">{svg_body}</g>
<rect id="shade" width="1920" height="1080" fill="#20242a" opacity="0" pointer-events="none"/>
{overlay}
</svg>
<script>{HELPERS}
{js}
window.__timelines = window.__timelines || {{}}; window.__timelines["scene-{scene_id}"] = tl;
</script></body></html>'''
