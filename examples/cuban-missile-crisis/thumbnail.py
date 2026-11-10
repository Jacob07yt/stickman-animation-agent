"""YouTube thumbnail (1280x720) in the coloured history sketch style."""
import sys
from pathlib import Path
PROJ = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJ.parents[1] / "src" / "sketch"))
from kit import *  # noqa
from kit import _font

svg = f'''<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 1920 1080">
<defs><pattern id="lines" width="1920" height="54" patternUnits="userSpaceOnUse"><line x1="0" y1="53" x2="1920" y2="53" stroke="{LINE}" stroke-width="2"/></pattern></defs>
<rect width="1920" height="1080" fill="{BG}"/><rect width="1920" height="1080" fill="url(#lines)"/>
<rect x="0" y="0" width="960" height="1080" fill="{US}" opacity=".12"/><rect x="960" y="0" width="960" height="1080" fill="{SU}" opacity=".12"/>
{flag("f1", "us", 100, 430, 1.4, hidden=False)}{flag("f2", "su", 1600, 440, 1.4, hidden=False)}
{person("jfk", 470, 790, 1.9, "jfk", label="", arms="M-30,-20 L-58,40 M30,-20 L120,60 L200,90", face="flat", hidden=False)}
{person("khr", 1450, 800, 1.85, "khrushchev", label="", arms="M30,-20 L58,40 M-30,-20 L-120,60 L-200,90", face="frown", hidden=False)}
<g transform="translate(960,930)"><rect x="-260" y="-70" width="520" height="140" rx="10" fill="#fff" stroke="{INK}" stroke-width="8" transform="rotate(-4)"/>
  <text y="22" text-anchor="middle" font-family="Cav" font-weight="700" font-size="84" fill="{SU}" transform="rotate(-4)">TOP SECRET</text></g>
<text x="960" y="200" text-anchor="middle" font-family="Cav" font-weight="700" font-size="190" fill="{INK}" stroke="{BG}" stroke-width="14" paint-order="stroke">THE SECRET DEAL</text>
<text x="960" y="330" text-anchor="middle" font-family="Cav" font-weight="700" font-size="92" fill="{SU}" stroke="{BG}" stroke-width="10" paint-order="stroke">that ended the Cuban Missile Crisis</text>
</svg>'''
html = f'''<!doctype html><html><head><style>@font-face{{font-family:Cav;src:url(data:font/ttf;base64,{_font(700)}) format('truetype');font-weight:700}}
body{{margin:0}} svg{{display:block;width:1280px;height:720px}}</style></head><body>{svg}</body></html>'''
(PROJ / "output" / "thumbnail.html").write_text(html, encoding="utf-8")
