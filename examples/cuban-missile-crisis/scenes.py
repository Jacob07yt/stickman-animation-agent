"""Cuban Missile Crisis: How It Really Happened - scene builder (coloured history sketch style).

Builds compositions/scene-NN.html for every scene, with animation cues synced to
the word timestamps in timestamps/scene-NN.json.

    python scenes.py            # all scenes
    python scenes.py 03 07      # selected scenes
"""
import sys
from pathlib import Path

PROJ = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJ.parents[1] / "src" / "sketch"))
from kit import *  # noqa

OUT = PROJ / "compositions"
PAD = 0.5  # silence after each scene (matches the audio padding at assembly)


def W(n):
    return Words(PROJ / f"timestamps/scene-{n}.json")


def build(n, svg, js, **kw):
    w = W(n)
    (OUT / f"scene-{n}.html").write_text(page(n, round(w.duration + PAD, 3), svg, js, **kw), encoding="utf-8")


# =============================================================== 01 - the myth
def s01():
    w = W("01")
    svg = f'''
{text("t_oct", 880, 130, "OCTOBER", 110)}{text("t_year", 1180, 130, "1962", 110, SU)}
{text("t_sub", 960, 215, "13 days. The closest the world ever came to nuclear war.", 56, INK2, 400)}
{text("t_school", 960, 140, "The story you probably know...", 60, INK2, 400)}
<g id="scene" filter="url(#rough)">
  {table("table", 960, 760)}
  {flag("fus", "us", 330, 250, 1.2)}{flag("fsu", "su", 1520, 260, 1.2)}
  {person("jfk", 520, 560, 1.5, "jfk")}{person("khr", 1400, 575, 1.45, "khrushchev")}
  {dashed_arrow("stare", "M610,375 L1290,385", INK, 4, head="M1270,370 L1296,385 L1270,400 M630,360 L604,375 L630,390")}
  {text("stare_t", 950, 345, "the staring contest", 46)}
  <g id="sweat" opacity="0"><path d="M1470,380 C1462,396 1462,406 1470,410 C1478,406 1478,396 1470,380 Z" fill="#8ec3e6" stroke="{INK}" stroke-width="3"/></g>
  {text("t_win", 520, 140, "AMERICA WINS!", 80, USD)}
</g>
{text("t_end", 960, 540, "THE END?", 150, INK, 700, extra='transform="rotate(-6 960 540)"')}
{person("stick", 960, 700, 1.5, "stick", arms=WAVE_R)}
{text("t_not", 960, 200, "...that's NOT how it happened.", 110, SU)}'''
    js = f'''
prep("#table, #fus, #fsu, #jfk, #khr, #stare, #stick");
fadeIn("#t_oct", 0.0, 0.5); pop("#t_year", {w("1962")}, 0.5);
fadeIn("#t_sub", {w("13")}, 0.6);
fadeOut("#t_oct, #t_year, #t_sub", {w("and") - 0.3}, 0.3);
fadeIn("#t_school", {w("probably")}, 0.5);
drawIn("#table", {w("know")}, 0.7);
drawIn("#fus", {w("kennedy") - 0.3}, 0.5); drawIn("#jfk", {w("kennedy") - 0.2}, 0.8);
drawIn("#fsu", {w("khrushchev") - 0.3}, 0.5); drawIn("#khr", {w("khrushchev") - 0.2}, 0.8);
drawIn("#stare", {w("stares")}, 0.8); fadeIn("#stare_t", {w("down")}, 0.3);
zoom(1400, 420, 1.9, {w("khrushchev", 2) - 0.3}, 0.5);
blink("#khr", {w("blinks")});
tl.fromTo("#sweat", {{ opacity: 0 }}, {{ opacity: 1, y: "+=30", duration: 0.6 }}, {w("blinks") + 0.2});
zoom(960, 540, 1.0, {w("america") - 0.2}, 0.35);
pop("#t_win", {w("america")}, 0.35);
fadeOut("#scene, #t_school", {w("end") - 0.15}, 0.2);
stampIn("#t_end", {w("end") - 0.05});
fadeOut("#t_end", {w("except") - 0.05}, 0.15);
drawIn("#stick", {w("except")}, 0.4);
pop("#t_not", {w("not") - 0.1}, 0.35); shake({w("not")});
wobble("#stick .arms", {w("how")}, 3, 8, "30px -20px");
'''
    build("01", svg, js)


# =============================================================== 02 - the teaser
def s02():
    w = W("02")
    svg = f'''
{text("t_q", 960, 150, "What REALLY happened:", 80)}
{person("stick", 300, 720, 1.5, "stick", arms=POINT_R)}
{envelope("i1", 760, 500, 1.4, "a secret deal")}
<g id="i2" transform="translate(1160,500)" opacity="0"><g transform="scale(3)">{missile_shape()}</g>
  <text x="60" y="-40" font-family="Cav" font-weight="700" font-size="110" fill="{SU}">?</text>
  <text x="0" y="150" text-anchor="middle" font-family="Cav" font-weight="700" font-size="44" fill="{INK}">hidden missiles</text></g>
{submarine_icon("i3", 1580, 500, 0.9, label="")}
{text("i3t", 1580, 650, "a submarine officer", 44)}
{rewind("rw", 960, 560, 1.3)}
{text("rwt", 960, 800, "REWIND", 90, SU)}'''
    js = f'''
prep("#stick");
drawIn("#stick", 0.0, 0.6); fadeIn("#t_q", 0.2, 0.4);
pop("#i1", {w("secret")}, 0.45);
pop("#i2", {w("missiles")}, 0.45);
pop("#i3", {w("submarine")}, 0.45); fadeIn("#i3t", {w("officer")}, 0.3);
wobble("#i3", {w("saved")}, 2, 5);
tl.to("#i1, #i2, #i3, #i3t, #t_q", {{ opacity: 0, rotation: -200, scale: 0.2, transformOrigin: "50% 50%", duration: 0.6, ease: "power2.in" }}, {w("rewind") - 0.3});
pop("#rw", {w("rewind")}, 0.4); tl.to("#rw", {{ rotation: -360, transformOrigin: "50% 50%", duration: 1.2, ease: "none" }}, {w("rewind")});
fadeIn("#rwt", {w("few")}, 0.3);
'''
    build("02", svg, js)


# =============================================================== 03 - the arms race
def s03():
    w = W("03")
    blue = "".join(f'<g transform="translate({-150 + (i % 10) * 34},{-30 - (i // 10) * 50}) scale(0.55)">{missile_shape(US)}</g>' for i in range(40))
    red = "".join(f'<g transform="translate({-30 + i * 34},-30) scale(0.55)">{missile_shape(SU)}</g>' for i in range(3))
    svg = f'''{world_map()}
{text("t_cold", 960, 640, "THE COLD WAR", 100, INK)}
{text("t_1962", 960, 640, "1962", 120, SU)}
<g id="chart" opacity="0"><rect x="560" y="620" width="800" height="400" rx="20" fill="{BG}" stroke="{INK}" stroke-width="5"/>
  <text x="960" y="680" text-anchor="middle" font-family="Cav" font-weight="700" font-size="48" fill="{INK}">Missiles that could reach the other side</text>
  <g id="bluepile" opacity="0" transform="translate(820,960)">{blue}<text x="0" y="45" text-anchor="middle" font-family="Cav" font-weight="700" font-size="44" fill="{USD}">USA: hundreds</text></g>
  <g id="redpile" opacity="0" transform="translate(1180,960)">{red}<text x="0" y="45" text-anchor="middle" font-family="Cav" font-weight="700" font-size="44" fill="{SUD}">USSR: a few dozen</text></g>
</g>
{person("khr", 1680, 780, 1.15, "khrushchev", label="")}
{person("jfk", 240, 780, 1.15, "jfk", label="", face="smile")}'''
    js = f'''
prep("#map, #khr, #jfk");
tl.set("#map", {{ opacity: 1 }}, 0);
tl.to("#map .d", {{ strokeDashoffset: 0, duration: 1.4, ease: "power1.inOut" }}, 0);
tl.to("#map .d", {{ fillOpacity: 1, duration: 0.6 }}, 1.0);
fadeIn("#t_cold", 0.3, 0.4);
fadeIn("#worldlabels", {w("united")}, 0.4);
bob("#worldlabels", {w("building")}, 2, 8);
fadeOut("#t_cold", {w("1962") - 0.3}, 0.2); pop("#t_1962", {w("1962")}, 0.4);
fadeOut("#t_1962", {w("america") - 0.2}, 0.2);
fadeIn("#chart", {w("america")}, 0.4);
drawIn("#jfk", {w("ahead") - 0.3}, 0.6);
pop("#redpile", {w("dozen") - 0.2}, 0.4);
drawIn("#khr", {w("missiles") - 0.2}, 0.6);
tl.fromTo("#bluepile > g", {{ opacity: 0, y: "+=40" }}, {{ opacity: 1, y: "-=40", duration: 0.25, stagger: 0.02 }}, {w("hundreds") - 0.4});
tl.set("#bluepile", {{ opacity: 1 }}, {w("hundreds") - 0.4});
blink("#khr", {w("hundreds") + 0.8});
wobble("#khr", {w("soviet", 2)}, 2, 5);
'''
    build("03", svg, js, lines=False)


# =============================================================== 04 - missiles in Turkey
def s04():
    w = W("04")
    ms = "".join(missile(f"tm{i}", 560 + i * 110, 760, 1.5, US) for i in range(3))
    svg = f'''{turkey_map()}
{ms}
{dashed_arrow("arrow", "M670,700 C760,520 1000,330 1170,210", SU, 7, head="M1140,215 L1172,206 L1172,240")}
{card("minutes", 1240, 380, 360, 110, [("in minutes!", SU)], size=64)}
{person("khr", 1650, 700, 1.25, "khrushchev")}
{steam("st1", 1595, 470, 1.2)}{steam("st2", 1715, 470, 1.2)}
{lightbulb("bulb", 1650, 400, 1.6)}
{bubble("joke", 1560, 520, "A taste of their own medicine!", 46, tail="right")}'''
    js = f'''
prep("#map, #khr");
tl.set("#map", {{ opacity: 1 }}, 0);
tl.to("#map .d", {{ strokeDashoffset: 0, duration: 1.2 }}, 0); tl.to("#map .d", {{ fillOpacity: 1, duration: 0.5 }}, 0.8);
fadeIn("#tklabels", {w("soviet")}, 0.4);
tl.fromTo("#tm0, #tm1, #tm2", {{ opacity: 0, y: "+=40" }}, {{ opacity: 1, y: "-=40", duration: 0.35, stagger: 0.15, ease: "back.out(2)" }}, {w("turkey") - 0.1});
pop("#moscow", {w("moscow") - 0.4}, 0.4);
drawIn("#arrow", {w("hit") - 0.2}, 0.6);
pop("#minutes", {w("minutes")}, 0.35);
fadeOut("#minutes", {w("khrushchev") - 0.3}, 0.2);
drawIn("#khr", {w("khrushchev") - 0.3}, 0.6);
pop("#st1", {w("hated")}, 0.3); pop("#st2", {w("hated") + 0.1}, 0.3);
bob("#st1, #st2", {w("hated") + 0.3}, 3, 12);
fadeOut("#st1, #st2", {w("reportedly")}, 0.2);
pop("#bulb", {w("joked")}, 0.35);
fadeOut("#bulb", {w("giving")}, 0.2);
pop("#joke", {w("giving") + 0.1}, 0.4);
'''
    build("04", svg, js, lines=False)


# =============================================================== 05 - Cuba and the Bay of Pigs
def s05():
    w = W("05")
    boats = "".join(ship(f"b{i}", 820 + i * 90, 1030, US, 0.7) for i in range(3))
    svg = f'''{caribbean_map()}
{dashed_arrow("d90", "M1166,702 L1166,832", INK, 5)}{text("t90", 1146, 760, "90 miles", 46, INK, 700, "end")}
{person("castro", 1010, 740, 0.75, "castro", label="")}{flag("fcu", "cu", 1090, 560, 0.6)}
{dashed_arrow("supp", "M1920,420 C1700,560 1500,700 1260,790", SU, 7, head="M1290,770 L1258,792 L1294,806")}
{text("supp_t", 1700, 470, "Soviet support", 48, SUD)}
{datecard("date59", "JANUARY", "1959")}
{card("bop", 60, 50, 680, 110, [("Bay of Pigs, 1961", INK)], size=64)}
{boats}
{stamp("failed", 960, 980, "FAILED", SU, 90)}
<g id="pages" opacity="0">{"".join(f'<rect x="{290 + i*6}" y="{612 - i*14}" width="240" height="280" fill="#fff" stroke="{INK}" stroke-width="3" transform="rotate(-6 400 760)"/>' for i in range(5))}</g>
{letter("plans", 400, 760, "CIA PLANS", "", 1.0, -6, US)}
{text("angry", 620, 400, "America: not happy", 56, USD)}'''
    js = f'''
prep("#map, #castro");
tl.set("#map", {{ opacity: 1 }}, 0);
tl.to("#map .d", {{ strokeDashoffset: 0, duration: 1.0 }}, 0); tl.to("#map .d", {{ fillOpacity: 1, duration: 0.5 }}, 0.6);
fadeIn("#maplabels, #seanames", {w("90") - 0.2}, 0.3);
drawIn("#d90", {w("90")}, 0.4); fadeIn("#t90", {w("miles")}, 0.3);
fadeOut("#d90, #t90", {w("1959") - 0.3}, 0.2);
pop("#date59", {w("1959")}, 0.4);
drawIn("#castro", {w("fidel")}, 0.7); drawIn("#fcu", {w("castro")}, 0.5);
drawIn("#supp", {w("soviet")}, 0.6); fadeIn("#supp_t", {w("support")}, 0.3);
fadeIn("#angry", {w("america")}, 0.3); wobble("#angry", {w("happy")}, 2, 3);
fadeOut("#angry, #date59", {w("1961") - 0.3}, 0.2);
pop("#bop", {w("1961")}, 0.4);
tl.set("#b0, #b1, #b2", {{ opacity: 1 }}, {w("invasion") - 0.4});
move("#b0, #b1, #b2", {w("invasion") - 0.4}, 0, -140, 1.6, "power1.out");
tl.to("#b0, #b1, #b2", {{ rotation: 35, y: "+=60", opacity: 0, duration: 0.6, stagger: 0.1 }}, {w("failed")});
stampIn("#failed", {w("failed") + 0.1});
fadeOut("#failed, #bop", {w("cia", 2) - 0.3}, 0.2);
pop("#plans", {w("cia", 2)}, 0.4);
tl.fromTo("#pages", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.2 }}, {w("plotting")});
tl.fromTo("#pages rect", {{ opacity: 0 }}, {{ opacity: 1, duration: 0.1, stagger: 0.18 }}, {w("plotting")});
'''
    build("05", svg, js, lines=False)


# =============================================================== 06 - the secret plan
def s06():
    w = W("06")
    mapcard = (f'<g id="mapcard" transform="translate(960,690)" opacity="0"><rect x="-150" y="-60" width="300" height="110" fill="#f7f1e2" stroke="{INK}" stroke-width="4" transform="rotate(-3)"/>'
               f'<path d="M-110,10 q40,-40 90,-20 M40,30 q30,-10 60,0" stroke="{CUD}" stroke-width="6" fill="none"/>'
               f'<path d="M100,-40 C40,-50 -20,-20 -60,10" stroke="{SU}" stroke-width="5" stroke-dasharray="10 8" fill="none"/>'
               f'<g transform="translate(-60,10) scale(0.5)">{missile_shape()}</g></g>')
    svg = f'''
{table("table", 960, 760, 1.0)}
{mapcard}
{person("castro", 560, 600, 1.35, "castro")}
{person("khr", 1360, 600, 1.35, "khrushchev")}
{bubble("b_prot", 640, 380, "Protect us!", 48)}
{bubble("b_odds", 1300, 380, "Even the odds...", 48, tail="right")}
{lightbulb("bulb", 960, 300, 1.8)}
{stamp("secret", 960, 160, "TOP SECRET", SU, 80)}
{bubble("sh1", 650, 380, "shhh...", 52)}{bubble("sh2", 1270, 380, "shhh...", 52, tail="right")}
{text("door", 960, 980, "...right on America's doorstep", 64, SU)}'''
    js = f'''
prep("#table, #castro, #khr");
drawIn("#table", 0.0, 0.6);
drawIn("#castro", {w("castro") - 0.2}, 0.7); pop("#b_prot", {w("protection")}, 0.35);
drawIn("#khr", {w("khrushchev") - 0.2}, 0.7); pop("#b_odds", {w("odds") - 0.2}, 0.35);
fadeOut("#b_prot, #b_odds", {w("put")}, 0.2);
move("#castro", {w("together") - 0.3}, 120, 0, 0.5); move("#khr", {w("together") - 0.3}, -120, 0, 0.5);
pop("#bulb", {w("bold")}, 0.4); wobble("#bulb", {w("idea")}, 2, 6, "50% 100%");
fadeOut("#bulb", {w("secretly") - 0.2}, 0.2);
stampIn("#secret", {w("secretly")});
pop("#sh1", {w("ship")}, 0.3); pop("#sh2", {w("ship") + 0.15}, 0.3);
pop("#mapcard", {w("missiles") - 0.2}, 0.4);
fadeIn("#door", {w("doorstep") - 0.4}, 0.4);
'''
    build("06", svg, js)


# =============================================================== 07 - Operation in secret
def s07():
    w = W("07")
    convoy = "".join(ship(f"c{i}", 1520 + i * 70, 430 + i * 40, SU, 0.9, flip=True, cargo=True) for i in range(5))
    svg = f'''{atlantic_map()}
{dashed_arrow("route", "M1500,440 C1200,520 900,640 600,720", SU, 5)}
{convoy}
{card("count", 640, 40, 640, 250, [("missiles", SU), ("nuclear warheads", SU), ("~40,000 troops", SU)], size=58)}
<g id="gag" opacity="0">
  <rect x="300" y="150" width="1320" height="820" rx="30" fill="#fdf3d6" stroke="{INK}" stroke-width="6"/>
  <circle cx="1450" cy="300" r="70" fill="{GOLD}" stroke="{INK}" stroke-width="4"/>
  <path d="M300,820 C600,790 1300,800 1620,820 L1620,970 L300,970 Z" fill="#f1d58f" stroke="{INK}" stroke-width="5"/>
  {palm("palm", 520, 860, 1.5, hidden=False)}
  {person("soldier", 960, 700, 1.3, "soldier", arms=SHRUG, face="frown", hidden=False)}
  {skis("skis", 1140, 720, 1.0, hidden=False)}
  {text("gagt", 960, 250, "Packed for... snow?", 72, INK, 700, hidden=False)}
</g>
{person("stick", 1700, 900, 0.9, "stick", arms=SHRUG)}'''
    js = f'''
prep("#map, #stick");
tl.set("#map", {{ opacity: 1 }}, 0);
tl.to("#map .d", {{ strokeDashoffset: 0, duration: 1.0 }}, 0); tl.to("#map .d", {{ fillOpacity: 1, duration: 0.5 }}, 0.6);
fadeIn("#atlabels", 0.6, 0.4);
drawIn("#route", {w("dozens") - 0.3}, 0.8);
tl.set(".ship", {{ opacity: 1 }}, {w("ships") - 0.2});
tl.to(".ship", {{ x: "-=900", y: "+=280", duration: 5.5, ease: "power1.inOut", stagger: 0.25 }}, {w("ships") - 0.2});
tl.set("#count", {{ opacity: 1 }}, {w("missiles") - 0.1});
tl.set("#count rect", {{ opacity: 1 }}, {w("missiles") - 0.1});
tl.fromTo("#count text", {{ opacity: 0 }}, {{ opacity: 0, duration: 0.01 }}, 0);
tl.to("#count text:nth-of-type(1)", {{ opacity: 1, duration: 0.2 }}, {w("missiles")});
tl.to("#count text:nth-of-type(2)", {{ opacity: 1, duration: 0.2 }}, {w("warheads")});
tl.to("#count text:nth-of-type(3)", {{ opacity: 1, duration: 0.2 }}, {w("40")});
fadeOut("#count", {w("keep")}, 0.3);
pop("#gag", {w("winter") - 0.3}, 0.5);
wobble("#soldier", {w("gear")}, 3, 4);
drawIn("#stick", {w("somewhere") - 0.4}, 0.4);
'''
    build("07", svg, js, lines=False)


# =============================================================== 08 - the U-2 finds the missiles
def s08():
    w = W("08")
    ms = "".join(missile(f"m{i}", x, y, 1.0) for i, (x, y) in enumerate([(860, 800), (960, 812), (1100, 834)]))
    flashes = "".join(f'<circle id="fl{i}" cx="{760 + i*160}" cy="{800 + (i%2)*20}" r="60" fill="#fff" opacity="0"/>' for i in range(4))
    svg = f'''{caribbean_map()}
{ms}
{datecard("date", "OCTOBER 14")}
{u2("plane", -200, 700, 0.9)}
{flashes}
<circle id="ring1" cx="980" cy="815" r="760" fill="none" stroke="{SU}" stroke-width="6" stroke-dasharray="22 16" opacity="0"/>
<g id="kpanel" opacity="0"><rect x="160" y="160" width="1600" height="760" rx="30" fill="{BG}" stroke="{INK}" stroke-width="6"/>
  {person("jfk", 520, 640, 1.4, "jfk", arms=HOLD, face="flat", hidden=False)}
  {photo("photo", 1150, 520, 1.6, hidden=False)}
  {magnifier("mag", 1000, 450, 1.2, hidden=False)}
</g>
{card("min", 1180, 400, 420, 110, [("in minutes", SU)], size=64)}'''
    js = f'''
tl.set("#map", {{ opacity: 1 }}, 0);
show("#maplabels, #seanames, #legend", 0, 0.3);
tl.set("#m0, #m1, #m2", {{ opacity: 1 }}, 0);
pop("#date", {w("october")}, 0.4);
tl.set("#plane", {{ opacity: 1 }}, {w("american") - 0.2});
move("#plane", {w("american") - 0.2}, 2300, 0, 3.6, "none");
tl.to("[id^='fl']", {{ opacity: 0.9, duration: 0.05, stagger: 0.15, yoyo: true, repeat: 1 }}, {w("photos") - 0.4});
fadeOut("#date", {w("two") - 0.3}, 0.2);
pop("#kpanel", {w("two")}, 0.5);
tl.to("#mag", {{ x: "+=80", y: "+=40", duration: 0.8, yoyo: true, repeat: 1, ease: "sine.inOut" }}, {w("pictures")});
tl.to("#photo text", {{ scale: 1.25, transformOrigin: "50% 50%", duration: 0.2, yoyo: true, repeat: 1 }}, {w("missile")});
blink("#jfk", {w("sites") + 0.2});
fadeOut("#kpanel", {w("missiles") - 0.2}, 0.3);
show("#dc", {w("missiles")}, 0.3);
tl.fromTo("#ring1", {{ opacity: 0, scale: 0.1, svgOrigin: "980 815" }}, {{ opacity: 1, scale: 1, duration: 0.9, ease: "power2.out" }}, {w("reach")});
pop("#min", {w("minutes") - 0.1}, 0.3);
'''
    build("08", svg, js, lines=False)


# =============================================================== 09 - the advisers
def s09():
    w = W("09")
    dom = "".join(domino(f"dm{i}", 560 + i * 400, 900, lab, 1.4) for i, lab in enumerate(["CUBA", "BERLIN", "NUCLEAR WAR"]))
    svg = f'''
{text("t_sec", 960, 110, "Top secret meeting", 64, INK2, 400)}
<g id="room">
  {person("rfk", 520, 560, 1.25, "rfk")}
  {person("jfk", 960, 540, 1.35, "jfk", arms="M-30,-20 L-58,40 M30,-20 L58,40")}
  {person("gen", 1400, 560, 1.3, "general", arms="M-30,-20 L-58,40 M30,-20 L90,-30")}
  {table("table", 960, 800, 1.3)}
  {bubble("b_bomb", 1330, 300, "BOMB THEM!", 56, tail="right")}
  {bubble("b_inv", 1330, 300, "...then INVADE!", 56, tail="right")}
  {bubble("b_q", 1000, 260, "What does Khrushchev do next?", 50)}
</g>
{dom}
{text("then", 960, 300, "...and then what?", 80, SU)}'''
    js = f'''
prep("#table, #rfk, #jfk, #gen");
fadeIn("#t_sec", 0.1, 0.4);
drawIn("#jfk", 0.0, 0.7); drawIn("#table", 0.3, 0.5);
drawIn("#rfk", {w("advisors") - 0.3}, 0.6);
drawIn("#gen", {w("generals") - 0.3}, 0.6);
pop("#b_bomb", {w("bomb")}, 0.3); wobble("#gen .arms", {w("bomb")}, 3, 10, "30px -20px"); shake({w("bomb")}, 2);
fadeOut("#b_bomb", {w("invade") - 0.15}, 0.1); pop("#b_inv", {w("invade")}, 0.3);
fadeOut("#b_inv", {w("kennedy", 2)}, 0.2);
pop("#b_q", {w("what")}, 0.4);
fadeOut("#room, #t_sec", {w("bomb", 2) - 0.3}, 0.3);
slideIn("#dm0", {w("cuba", 2)}, 0, -60, 0.35);
slideIn("#dm1", {w("berlin") - 0.1}, 0, -60, 0.35);
slideIn("#dm2", {w("respond") - 0.2}, 0, -60, 0.35);
tl.to("#dm0 .tile", {{ rotation: 62, transformOrigin: "50px 0px", duration: 0.35, ease: "power2.in" }}, {w("what", 2) - 0.5});
tl.to("#dm1 .tile", {{ rotation: 62, transformOrigin: "50px 0px", duration: 0.35, ease: "power2.in" }}, {w("what", 2) - 0.25});
tl.to("#dm2 .tile", {{ rotation: 62, transformOrigin: "50px 0px", duration: 0.35, ease: "power2.in" }}, {w("what", 2)});
pop("#then", {w("what", 2)}, 0.35); shake({w("what", 2) + 0.35}, 3);
'''
    build("09", svg, js)


# =============================================================== 10 - the quarantine
def quarantine_layer(ships_hidden=True):
    ships = "".join(ship(f"us{i}", *qpos(a), US, 0.9, hidden=ships_hidden) for i, a in enumerate(Q_ANGLES))
    return f'''
<circle id="ring1" cx="980" cy="815" r="430" fill="none" stroke="{SU}" stroke-width="5" stroke-dasharray="22 16" opacity="0"/>
<circle id="ring2" cx="980" cy="815" r="760" fill="none" stroke="{SU}" stroke-width="4" stroke-dasharray="10 16" opacity="0"/>
<text id="rangelabel" x="1420" y="430" font-family="Cav" font-weight="700" font-size="40" fill="{SU}" transform="rotate(-28 1420 430)" opacity="0">missile range</text>
<ellipse id="qline" cx="{Q_CENTER[0]}" cy="{Q_CENTER[1]}" rx="{Q_RX}" ry="{Q_RY}" fill="none" stroke="{US}" stroke-width="6" stroke-dasharray="4 18" stroke-linecap="round" opacity="0"/>
<text id="qlabel" x="560" y="1040" font-family="Cav" font-weight="700" font-size="40" fill="{USD}" opacity="0">US Navy "quarantine" line</text>
{missile("m1", 860, 800)}{missile("m2", 960, 812)}{missile("m3", 1100, 834)}
{ships}'''


def s10():
    w = W("10")
    tvjfk = person("tvjfk", -35, 50, 0.62, "jfk", label="", arms="M-30,-20 L-62,30 M30,-20 L72,-50", hidden=False)
    svg = f'''{caribbean_map()}{quarantine_layer()}
{datecard("date", "OCTOBER 22")}
{tv("tv", 1460, 540, 1.0, inner='<rect x="-215" y="80" width="360" height="40" fill="' + WOOD + '" stroke="' + INK + '" stroke-width="4"/>' + tvjfk)}
{card("w_q", 560, 70, 800, 130, [('"QUARANTINE"', USD)], stroke=US, size=84)}
{card("w_b", 520, 225, 880, 90, [('not a "blockade" = an act of war', INK)], size=60, sw=3)}'''
    js = f'''
prep("#map");
tl.set("#map", {{ opacity: 1 }}, 0);
tl.to("#usa, #cuba", {{ strokeDashoffset: 0, duration: 1.2, ease: "power1.inOut" }}, 0);
tl.to("#usa, #cuba", {{ fillOpacity: 1, duration: 0.6 }}, 0.8);
fadeIn("#maplabels, #seanames", 1.0, 0.5); fadeIn("#legend", 1.2, 0.4); fadeIn("#dc", 1.3, 0.4);
pop("#date", {w("october")}, 0.45);
pop("#tv", {w("kennedy") - 0.1}, 0.5);
wobble("#tvjfk .arms", {w("told")}, 4, -10, "30px -20px");
tl.fromTo("#m1, #m2, #m3", {{ opacity: 0, y: "+=30" }}, {{ opacity: 1, y: "-=30", duration: 0.35, stagger: 0.15, ease: "back.out(2)" }}, {w("missiles") - 0.2});
tl.fromTo("#ring1", {{ opacity: 0, scale: 0.1, svgOrigin: "980 815" }}, {{ opacity: 1, scale: 1, duration: 0.7, ease: "power2.out" }}, {w("missiles") + 0.3});
tl.fromTo("#ring2", {{ opacity: 0, scale: 0.1, svgOrigin: "980 815" }}, {{ opacity: 0.6, scale: 1, duration: 0.8, ease: "power2.out" }}, {w("missiles") + 0.6});
fadeIn("#rangelabel", {w("missiles") + 1.1}, 0.3);
fadeOut("#tv", {w("navy") - 0.2}, 0.3);
tl.fromTo(".ship[id^='us']", {{ opacity: 0, y: "-=60" }}, {{ opacity: 1, y: "+=60", duration: 0.5, stagger: 0.12, ease: "power2.out" }}, {w("navy")});
show("#qline", {w("navy") + 0.4}, 0.8); fadeIn("#qlabel", {w("navy") + 1.0}, 0.4);
fadeOut("#date", {w("quarantine") - 0.4}, 0.2);
pop("#w_q", {w("quarantine")}, 0.4);
fadeIn("#w_b", {w("blockade")}, 0.4);
tl.to("#w_b text", {{ fill: "{SU}", duration: 0.2 }}, {w("war")});
'''
    build("10", svg, js, lines=False)


# =============================================================== 11 - the ships turn back
def s11():
    w = W("11")
    svg = f'''{caribbean_map()}{quarantine_layer(ships_hidden=False)}
{ship("su1", 2060, 960, SU, 1.1, True, hidden=False)}{ship("su2", 2200, 1010, SU, 1.0, True, hidden=False)}{ship("su3", 2150, 900, SU, 0.95, True, hidden=False)}
{datecard("date", "OCTOBER 24")}
{card("breath", 560, 90, 800, 110, [("the world holds its breath...", INK)], size=64)}
<g id="eyeq" opacity="0">
  <rect x="160" y="250" width="1600" height="580" rx="30" fill="{BG}" stroke="{INK}" stroke-width="6"/>
  <g transform="translate(500,540)"><ellipse rx="190" ry="120" fill="#fff" stroke="{INK}" stroke-width="7"/>
    <circle r="70" fill="{US}" stroke="{INK}" stroke-width="5"/><circle r="32" fill="{INK}"/><circle cx="-18" cy="-20" r="10" fill="#fff"/>
    <path id="lid" d="M-190,0 C-120,-130 120,-130 190,0 C120,130 -120,130 -190,0 Z" fill="{SKIN}" stroke="{INK}" stroke-width="7" transform="scale(1,0)"/></g>
  <text x="1230" y="460" text-anchor="middle" font-family="Cav" font-weight="700" font-size="64" fill="{INK}">"We're eyeball to eyeball...</text>
  <text x="1230" y="560" text-anchor="middle" font-family="Cav" font-weight="700" font-size="64" fill="{INK}">and I think the other fellow</text>
  <text x="1230" y="660" text-anchor="middle" font-family="Cav" font-weight="700" font-size="64" fill="{SU}">just blinked."</text>
  <text x="1230" y="760" text-anchor="middle" font-family="Cav" font-weight="400" font-size="48" fill="{INK2}">- Dean Rusk, US Secretary of State</text>
</g>'''
    js = f'''
gsap.set("#map, #legend, #maplabels, #seanames, #dc, #qline, #qlabel, #m1, #m2, #m3, #rangelabel", {{ opacity: 1 }});
gsap.set("#ring1", {{ opacity: 1 }}); gsap.set("#ring2", {{ opacity: 0.6 }});
tl.to("#su1", {{ x: "-=400", duration: {w("stopped") - 0.2}, ease: "power1.out" }}, 0);
tl.to("#su2", {{ x: "-=470", duration: {w("stopped") - 0.2}, ease: "power1.out" }}, 0);
tl.to("#su3", {{ x: "-=450", duration: {w("stopped") - 0.2}, ease: "power1.out" }}, 0);
zoom(1560, 900, 1.6, {w("line") - 0.3}, 1.6);
pop("#breath", {w("world")}, 0.4); fadeOut("#breath", {w("october") - 0.4}, 0.2);
pop("#date", {w("october")}, 0.4);
tl.to("#su1 .hull, #su2 .hull, #su3 .hull", {{ scaleX: function (i, el) {{ return -gsap.getProperty(el, "scaleX"); }}, duration: 0.35, ease: "power2.inOut" }}, {w("turned") - 0.1});
tl.to("#su1, #su2, #su3", {{ x: "+=700", duration: 3.0, ease: "power1.in" }}, {w("around")});
zoom(960, 540, 1.0, {w("we") - 0.4}, 0.6);
fadeOut("#date", {w("we") - 0.3}, 0.2);
pop("#eyeq", {w("we") + 0.1}, 0.45);
tl.to("#lid", {{ scaleY: 1, duration: 0.12, yoyo: true, repeat: 1 }}, {w("blinked")});
'''
    build("11", svg, js, lines=False)


# =============================================================== 12 - racing to finish / the UN
def s12():
    w = W("12")
    flakes = "".join(snowflake(f"sf{i}", 300 + i * 330, 140 + (i % 2) * 60, 1.0) for i in range(5))
    svg = f'''{caribbean_map()}{quarantine_layer(ships_hidden=False)}
{progress("prog", 960, 240, "Missiles in Cuba: nearly ready...", 700)}
<g id="un" opacity="0">
  <rect width="1920" height="1080" fill="{BG}"/><rect width="1920" height="1080" fill="url(#lines)"/>
  <ellipse cx="960" cy="1000" rx="900" ry="120" fill="#cfdbe8" stroke="{INK}" stroke-width="5"/>
  {card("untitle", 560, 40, 800, 110, [("UNITED NATIONS - OCT 25", INK)], size=60, hidden=False)}
  {easel("easel", 960, 520, 1.1, hidden=False)}
  {person("usamb", 450, 640, 1.25, "stevenson", arms=POINT_R, hidden=False)}
  {person("suamb", 1480, 640, 1.25, "dobrynin", label="Soviet UN Ambassador", face="frown", hidden=False)}
  {bubble("wait", 520, 380, "I'll wait until hell freezes over!", 46)}
  {flakes}
</g>'''
    js = f'''
gsap.set("#map, #legend, #maplabels, #seanames, #dc, #qline, #qlabel, #m1, #m2, #m3, #rangelabel", {{ opacity: 1 }});
gsap.set("#ring1", {{ opacity: 1 }}); gsap.set("#ring2", {{ opacity: 0.6 }});
zoom(980, 820, 1.7, 0.0, 1.2);
bob("#m1, #m2, #m3", {w("still")}, 3, 10);
pop("#prog", {w("racing") - 0.2}, 0.35);
tl.to("#prog .fill", {{ scaleX: 0.85, duration: 1.6, ease: "power1.out" }}, {w("racing")});
zoom(960, 540, 1.0, {w("next") - 0.3}, 0.4);
fadeOut("#prog", {w("next") - 0.3}, 0.2);
show("#un", {w("united") - 0.4}, 0.4);
wobble("#usamb .arms", {w("showed")}, 3, -6, "30px -20px");
tl.to("#easel", {{ scale: 1.08, transformOrigin: "50% 50%", duration: 0.25, yoyo: true, repeat: 1 }}, {w("photos")});
blink("#suamb", {w("soviet") + 0.2});
pop("#wait", {w("wait") - 0.2}, 0.4);
tl.fromTo("[id^='sf']", {{ opacity: 0, y: "-=60" }}, {{ opacity: 1, y: "+=60", duration: 0.5, stagger: 0.1 }}, {w("hell")});
'''
    build("12", svg, js, lines=False)


# =============================================================== 13 - the first letter / knot of war
def s13():
    w = W("13")
    svg = f'''
{datecard("date", "OCTOBER 26")}
<g id="desk">
  {table("dtable", 960, 820, 1.2)}
  {desk_lamp("lamp", 1280, 620, 1.2)}
  {person("khr1", 760, 640, 1.3, "khrushchev", arms="M-30,-20 L-58,40 M30,-20 L70,30 L110,40")}
  {letter("l1", 1050, 560, "Letter #1", "from Khrushchev", 1.1, 4)}
  {text("emo", 1500, 330, "emotional... almost desperate", 52, SU)}
</g>
<g id="tug" opacity="0">
  {person("jfk", 380, 640, 1.2, "jfk", arms="M-30,-20 L40,0 L120,-10 M30,-20 L60,0 L120,-6", hidden=False)}
  {person("khr", 1540, 640, 1.2, "khrushchev", arms="M30,-20 L-40,0 L-120,-10 M-30,-20 L-60,0 L-120,-6", hidden=False)}
  <path id="rope" d="M520,620 C760,640 1160,640 1400,620" stroke="#8a6a3a" stroke-width="12" fill="none" stroke-linecap="round"/>
  <g id="knot" transform="translate(960,632)"><g class="k"><circle r="40" fill="#8a6a3a" stroke="{INK}" stroke-width="5"/>
    <text y="15" text-anchor="middle" font-family="Cav" font-weight="700" font-size="40" fill="#fff">WAR</text></g></g>
  {text("tight", 960, 470, "the harder they pull, the tighter the knot", 58, SU)}
</g>
{card("offer", 360, 820, 1200, 200, [("The offer: Soviets remove the missiles", SUD), ("if America never invades Cuba", USD)], size=56)}'''
    js = f'''
prep("#dtable, #lamp, #khr1");
pop("#date", 0.0, 0.4);
drawIn("#dtable", 0.2, 0.5); drawIn("#lamp", 0.4, 0.5);
drawIn("#khr1", {w("khrushchev") - 0.4}, 0.7);
pop("#l1", {w("letter")}, 0.4);
wobble("#khr1 .arms", {w("arrived")}, 4, 6, "30px -20px");
fadeIn("#emo", {w("emotional")}, 0.4);
fadeOut("#desk, #date", {w("said") - 0.2}, 0.3);
show("#tug", {w("said")}, 0.4);
tl.to("#jfk", {{ x: "-=30", duration: 0.3, yoyo: true, repeat: 5 }}, {w("pulling")});
tl.to("#khr", {{ x: "+=30", duration: 0.3, yoyo: true, repeat: 5 }}, {w("pulling")});
tl.fromTo("#knot .k", {{ scale: 0.6, transformOrigin: "50% 50%" }}, {{ scale: 1.0, duration: 0.4 }}, {w("knot")});
fadeIn("#tight", {w("harder")}, 0.4);
tl.to("#knot .k", {{ scale: 1.9, duration: 1.2, ease: "power2.in" }}, {w("tighter") - 0.4});
shake({w("get")}, 2);
tl.to("#tug", {{ opacity: 0.25, duration: 0.3 }}, {w("offer") - 0.2});
pop("#offer", {w("offer")}, 0.45);
'''
    build("13", svg, js)


# =============================================================== 14 - the second message / Black Saturday
def s14():
    w = W("14")
    svg = f'''
{radio("radio", 420, 560, 1.4)}
{text("mosr", 420, 360, "Moscow Radio", 60, SUD)}
{letter("l1", 1180, 600, "Letter #1", "no invasion", 0.9, -8)}
{letter("l2", 1500, 600, "Message #2", "+ Turkey!", 0.9, 8)}
{person("jfk", 1340, 720, 1.2, "jfk", arms="M-30,-20 L-110,-60 M30,-20 L110,-60", face="open")}
{text("q", 1340, 300, "?", 140, SU)}
{text("bs1", 960, 470, "BLACK SATURDAY", 150, SU)}
{text("bs2", 960, 600, "October 27, 1962", 72, "#f3e9d8", 400)}'''
    js = f'''
prep("#jfk");
pop("#radio", 0.0, 0.45); fadeIn("#mosr", {w("moscow") - 0.3}, 0.4);
wobble("#radio", {w("radio")}, 4, 3);
pop("#l2", {w("more") - 0.2}, 0.4);
tl.to("#l2 text:last-of-type", {{ scale: 1.3, transformOrigin: "50% 50%", duration: 0.2, yoyo: true, repeat: 1 }}, {w("turkey")});
fadeOut("#radio, #mosr", {w("same") - 0.2}, 0.3);
drawIn("#jfk", {w("and") - 0.2}, 0.6);
pop("#l1", {w("and")}, 0.35);
move("#l1", {w("same")}, -60, -40, 0.4); move("#l2", {w("same")}, 60, -40, 0.4);
pop("#q", {w("everything")}, 0.3); wobble("#jfk", {w("wrong")}, 2, 4);
darken({w("historians") - 0.3}, 0.8, 0.8);
tl.to("#bs1, #bs2", {{ opacity: 0, duration: 0.01 }}, 0);
stampIn("#bs1", {w("black")}); fadeIn("#bs2", {w("saturday") + 0.2}, 0.4);
tl.set("#bs1, #bs2", {{ attr: {{ "data-front": 1 }} }}, 0);
'''
    # Black Saturday title must sit above the dark shade: put it in the overlay layer
    build("14", svg.replace(text("bs1", 960, 470, "BLACK SATURDAY", 150, SU), "").replace(text("bs2", 960, 600, "October 27, 1962", 72, "#f3e9d8", 400), ""),
          js, overlay=text("bs1", 960, 470, "BLACK SATURDAY", 150, SU) + text("bs2", 960, 600, "October 27, 1962", 72, "#f3e9d8", 400))


# =============================================================== 15 - two spy planes
def s15():
    w = W("15")
    svg = f'''<g id="carib">{caribbean_map()}</g>
{u2("plane1", 400, 600, 0.9)}
{missile("sam", 960, 820, 1.0)}
{explosion("boom", 1000, 600, 1.4)}
{card("anderson", 560, 60, 800, 120, [("Major Rudolf Anderson", INK)], size=64)}
<g id="arctic" opacity="0">{arctic_map()}</g>
{u2("plane2", 300, 520, 0.8, rot=10)}
{jet("j1", 1900, 650, 0.9, rot=200)}{jet("j2", 1960, 780, 0.9, rot=190)}
{card("wrong", 460, 900, 1000, 120, [("One wrong move...", SU)], size=72)}'''
    js = f'''
gsap.set("#map, #maplabels, #seanames, #legend", {{ opacity: 1 }});
darken(0, 0.25, 0.01);
tl.set("#plane1", {{ opacity: 1 }}, 0);
move("#plane1", 0, 600, 0, 1.6, "none");
tl.set("#sam", {{ opacity: 1 }}, {w("missile") - 0.4});
tl.to("#sam", {{ y: "-=220", x: "+=40", duration: 0.6, ease: "power1.in" }}, {w("missile") - 0.4});
tl.set("#sam", {{ opacity: 0 }}, {w("shot")});
pop("#boom", {w("shot")}, 0.25); shake({w("shot")}, 3);
tl.to("#plane1", {{ rotation: 70, y: "+=300", opacity: 0, transformOrigin: "50% 50%", duration: 1.2, ease: "power1.in" }}, {w("shot") + 0.1});
fadeOut("#boom", {w("down") + 0.3}, 0.3);
pop("#anderson", {w("major")}, 0.4);
fadeOut("#anderson", {w("over", 2) - 0.3}, 0.2);
fadeOut("#carib", {w("arctic") - 0.4}, 0.3);
show("#arctic", {w("arctic") - 0.4}, 0.4);
prep("#arctic #map"); tl.set("#arctic #map", {{ opacity: 1 }}, {w("arctic") - 0.4});
tl.to("#arctic #map .d", {{ strokeDashoffset: 0, duration: 0.6 }}, {w("arctic") - 0.4});
tl.to("#arctic #map .d", {{ fillOpacity: 1, duration: 0.4 }}, {w("arctic") - 0.1});
show("#border, #arclabels", {w("arctic")}, 0.4);
tl.set("#plane2", {{ opacity: 1 }}, {w("another") - 0.2});
tl.to("#plane2", {{ x: "+=900", y: "-=40", rotation: 25, duration: 3.0, ease: "sine.inOut" }}, {w("another") - 0.2});
tl.set("#j1, #j2", {{ opacity: 1 }}, {w("fighter") - 0.3});
tl.to("#j1", {{ x: "-=520", y: "-=120", duration: 1.6, ease: "power2.out" }}, {w("fighter") - 0.3});
tl.to("#j2", {{ x: "-=520", y: "-=180", duration: 1.6, ease: "power2.out" }}, {w("fighter") - 0.1});
tl.to("#plane2", {{ x: "-=700", rotation: 190, duration: 2.2, ease: "power1.inOut" }}, {w("catch") - 0.2});
pop("#wrong", {w("one") - 0.1}, 0.4); shake({w("war") - 0.1}, 3);
'''
    build("15", svg, js, lines=False)


# =============================================================== 16 - submarine B-59
def s16():
    w = W("16")
    charges = "".join(f'<g id="dc{i}" transform="translate({620 + i*230},{300})" opacity="0"><rect x="-16" y="-20" width="32" height="40" rx="8" fill="{INK2}" stroke="{INK}" stroke-width="3"/></g>' for i in range(4))
    booms = "".join(explosion(f"bm{i}", 620 + i * 230, 620 + (i % 2) * 60, 0.8) for i in range(4))
    svg = f'''
<rect width="1920" height="300" fill="#e8eef0"/>
<rect y="300" width="1920" height="780" fill="#5f8aa0"/>
<path d="M0,300 Q60,285 120,300 T240,300 T360,300 T480,300 T600,300 T720,300 T840,300 T960,300 T1080,300 T1200,300 T1320,300 T1440,300 T1560,300 T1680,300 T1800,300 T1920,300" fill="none" stroke="{INK}" stroke-width="5"/>
{destroyer("d1", 600, 260, 1.0)}{destroyer("d2", 1350, 260, 1.0)}
{charges}{booms}
{submarine_icon("sub", 960, 760, 1.5, c="#6d6f6a", label="")}
{text("b59", 960, 900, "Soviet submarine B-59", 60, "#f3e9d8")}
{card("nocon", 120, 380, 560, 110, [("No contact with Moscow", SU)], size=54)}
{thermometer("therm", 1640, 700, 1.3)}
{text("hot", 1640, 480, "boiling hot", 56, "#f3e9d8")}
<g id="torp" transform="translate(960,560)" opacity="0"><rect x="-200" y="-34" width="400" height="68" rx="34" fill="#7f8a8f" stroke="{INK}" stroke-width="5"/>
  <path d="M200,0 l40,-34 v68 Z" fill="#7f8a8f" stroke="{INK}" stroke-width="5"/>
  <text x="-10" y="16" text-anchor="middle" font-family="Cav" font-weight="700" font-size="50" fill="{GOLD}">NUCLEAR</text></g>
<rect id="alarm" width="1920" height="1080" fill="{SU}" opacity="0"/>'''
    js = f'''
slideIn("#sub", 0.2, -400, 0, 1.4);
fadeIn("#b59", {w("b")}, 0.4);
fadeOut("#b59", {w("hunted")}, 0.2);
slideIn("#d1", {w("destroyers") - 0.4}, -300, 0, 0.8); slideIn("#d2", {w("destroyers") - 0.2}, 300, 0, 0.8);
tl.set("[id^='dc']", {{ opacity: 1 }}, {w("dropped")});
tl.to("[id^='dc']", {{ y: "+=320", duration: 0.9, stagger: 0.2, ease: "power1.in" }}, {w("dropped")});
tl.set("[id^='dc']", {{ opacity: 0 }}, {w("charges") + 0.6});
tl.fromTo("[id^='bm']", {{ opacity: 0, scale: 0.2, transformOrigin: "50% 50%" }}, {{ opacity: 1, scale: 1, duration: 0.2, stagger: 0.2 }}, {w("depth") + 0.5});
tl.to("[id^='bm']", {{ opacity: 0, duration: 0.3, stagger: 0.2 }}, {w("depth") + 0.9});
tl.to("#sub", {{ rotation: 3, transformOrigin: "50% 50%", yoyo: true, repeat: 7, duration: 0.1 }}, {w("depth") + 0.5});
shake({w("charges") + 0.4}, 3);
pop("#nocon", {w("contact") - 0.2}, 0.4);
pop("#therm", {w("boiling") - 0.2}, 0.35); fadeIn("#hot", {w("hot")}, 0.3);
tl.fromTo("#therm .mercury", {{ scaleY: 0.3, transformOrigin: "50% 100%" }}, {{ scaleY: 2.2, duration: 1.4, ease: "power1.in" }}, {w("boiling")});
fadeOut("#nocon, #therm, #hot", {w("on") - 0.3}, 0.3);
zoom(960, 700, 1.5, {w("torpedo") - 0.6}, 0.8);
pop("#torp", {w("torpedo")}, 0.4);
tl.to("#alarm", {{ opacity: 0.25, duration: 0.25, yoyo: true, repeat: 3 }}, {w("nuclear")});
'''
    build("16", svg, js, lines=False)


# =============================================================== 17 - Arkhipov says no
def s17():
    w = W("17")
    pipes = "".join(f'<path d="M0,{120 + i*40} H1920" stroke="#4b5560" stroke-width="14"/>' for i in range(2))
    svg = f'''
<g id="inside"><rect width="1920" height="1080" fill="#3a4550"/>{pipes}
  <rect x="0" y="900" width="1920" height="180" fill="#2c343c"/>
  <circle id="lamp" cx="960" cy="230" r="34" fill="{SU}" stroke="{INK}" stroke-width="5"/>
  <g transform="translate(960,1000)"><rect x="-260" y="-40" width="520" height="80" rx="40" fill="#7f8a8f" stroke="{INK}" stroke-width="5"/>
    <text y="16" text-anchor="middle" font-family="Cav" font-weight="700" font-size="48" fill="{GOLD}">NUCLEAR TORPEDO</text></g>
  {person("cap", 560, 600, 1.4, "savitsky", arms="M-30,-20 L-58,40 M30,-20 L100,40 L150,90", face="shout", lc="#f3e9d8")}
  {person("ark", 1360, 600, 1.4, "arkhipov", arms="M30,-20 L58,40 M-30,-20 L-90,-20", lc="#f3e9d8")}
  {bubble("fire", 500, 340, "FIRE IT!", 60)}
  {bubble("no", 1420, 340, "No.", 72, tail="right")}
  <path id="spot" d="M1360,-20 L1100,1080 L1620,1080 Z" fill="url(#spot)" opacity="0"/>
</g>
{card("acc", 560, 40, 800, 100, [("according to accounts decades later", INK2)], size=48)}
{card("rule", 460, 960, 1000, 100, [("launch needed the senior officers to agree", "#f3e9d8")], size=48, bg="#2c343c", stroke="#f3e9d8")}
<g id="surface" opacity="0"><rect width="1920" height="1080" fill="#5f8aa0"/><rect width="1920" height="380" fill="#e8eef0"/>
  <path d="M0,380 Q60,365 120,380 T240,380 T360,380 T480,380 T600,380 T720,380 T840,380 T960,380 T1080,380 T1200,380 T1320,380 T1440,380 T1560,380 T1680,380 T1800,380 T1920,380" fill="none" stroke="{INK}" stroke-width="5"/>
  {submarine_icon("sub", 960, 800, 1.5, c="#6d6f6a", hidden=False)}</g>
<g id="name" opacity="0"><rect width="1920" height="1080" fill="{BG}"/><rect width="1920" height="1080" fill="url(#lines)"/>
  <ellipse cx="960" cy="760" rx="380" ry="60" fill="#f6e7a8"/>
  {person("ark2", 960, 600, 1.5, "arkhipov", label="", face="smile", hidden=False)}
  {text("n1", 960, 180, "Vasili Arkhipov", 110, SUD, hidden=False)}
  {text("n2", 960, 960, "the man who said no", 72, INK, 400, hidden=False)}</g>'''
    js = f'''
prep("#cap, #ark");
pop("#acc", 0.0, 0.4);
tl.to("#lamp", {{ opacity: 0.3, duration: 0.3, yoyo: true, repeat: 30 }}, 0);
drawIn("#cap", {w("captain") - 0.3}, 0.6);
fadeOut("#acc", {w("captain")}, 0.2);
pop("#fire", {w("fire") - 0.1}, 0.3); wobble("#cap .arms", {w("fire")}, 3, 8, "30px -20px");
fadeOut("#fire", {w("launching")}, 0.2);
fadeIn("#rule", {w("launching")}, 0.4);
fadeOut("#rule", {w("one") - 0.2}, 0.2);
drawIn("#ark", {w("vasily") - 0.4}, 0.6);
show("#spot", {w("arkhipov")}, 0.5);
pop("#no", {w("no")}, 0.3);
tl.to("#ark .head", {{ rotation: 8, transformOrigin: "50% 100%", yoyo: true, repeat: 3, duration: 0.15 }}, {w("no") + 0.1});
tl.to("#cap", {{ x: "+=10", duration: 0.4 }}, {w("calmed")});
tl.to("#cap .arms", {{ rotation: 20, transformOrigin: "30px -20px", duration: 0.5 }}, {w("calmed")});
show("#surface", {w("submarine", 2) - 0.2}, 0.4);
move("#sub", {w("submarine", 2)}, 0, -390, 1.2, "power2.out");
show("#name", {w("most") - 0.2}, 0.5);
'''
    build("17", svg, js, lines=False)


# =============================================================== 18 - the secret deal
def s18():
    w = W("18")
    svg = f'''
<rect x="960" width="960" height="1080" fill="#3b3f46" id="darkside" opacity="0"/>
<line id="split" x1="960" y1="0" x2="960" y2="1080" stroke="{INK}" stroke-width="6" opacity="0"/>
{text("pub", 480, 110, "PUBLIC", 80, USD)}{text("sec", 1440, 110, "IN SECRET", 80, GOLD)}
{person("jfk", 480, 520, 1.25, "jfk", arms="M-30,-20 L-58,40 M30,-20 L80,-60")}
{podium("pod", 480, 700, 1.1)}
{letter("l1", 640, 330, "Letter #1", "no invasion", 0.6, 8)}
{card("pubdeal", 120, 870, 720, 160, [("Remove the missiles,", INK), ("and we won't invade Cuba", USD)], size=50)}
{desk_lamp("lamp", 1440, 260, 0.9)}
{person("rfk", 1220, 620, 1.2, "rfk", arms="M-30,-20 L-58,40 M30,-20 L90,10", lc="#c9d8f0")}
{person("dob", 1680, 620, 1.2, "dobrynin", arms="M30,-20 L58,40 M-30,-20 L-90,10", lc="#f0c9c4")}
{card("tk", 1140, 840, 600, 130, [("Turkey missiles go too...", INK), ("in a few months", INK2)], size=48)}
{stamp("ts", 1440, 360, "TOP SECRET", SU, 72)}'''
    js = f'''
prep("#jfk, #pod, #rfk, #dob, #lamp");
fadeIn("#pub", {w("publicly") - 0.6}, 0.3);
drawIn("#pod", {w("kennedy") - 0.2}, 0.5); drawIn("#jfk", {w("kennedy")}, 0.6);
wobble("#jfk", {w("clever")}, 2, 4);
pop("#l1", {w("first")}, 0.4);
pop("#pubdeal", {w("removed") - 0.1}, 0.4);
show("#darkside, #split", {w("but") - 0.2}, 0.4); fadeIn("#sec", {w("evening")}, 0.3);
drawIn("#lamp", {w("evening")}, 0.4);
drawIn("#rfk", {w("brother")}, 0.6); drawIn("#dob", {w("soviet")}, 0.6);
move("#rfk", {w("offered")}, 60, 0, 0.4); move("#dob", {w("offered")}, -60, 0, 0.4);
pop("#tk", {w("turkey") - 0.3}, 0.4);
tl.to("#tk text:last-of-type", {{ fill: "{SU}", duration: 0.2 }}, {w("not") - 0.1});
stampIn("#ts", {w("secret", 2) - 0.1});
'''
    build("18", svg, js)


# =============================================================== 19 - Khrushchev announces / the headlines
def s19():
    w = W("19")
    cargo = "".join(ship(f"rs{i}", 200 + i * 330, 930 + (i % 2) * 40, SU, 1.8, cargo=True) for i in range(3))
    svg = f'''
{datecard("date", "OCTOBER 28")}
{person("khr", 560, 560, 1.3, "khrushchev", arms="M-30,-20 L-58,40 M30,-20 L70,10", face="flat")}
{mic("mic", 760, 520, 1.0)}
{radio("radio", 1320, 450, 1.0)}
{text("home", 1320, 650, "&quot;The missiles are coming home.&quot;", 56, SUD)}
<g id="sea" opacity="0"><rect y="880" width="1920" height="260" fill="{SEA}"/></g>
{cargo}
{stamp("over", 960, 320, "CRISIS OVER", US, 100, -4)}
{newspaper("np1", 620, 560, "SOVIETS BACK DOWN!", 1.3, -6)}
{newspaper("np2", 1300, 600, "KENNEDY STANDS FIRM", 1.3, 5)}'''
    js = f'''
prep("#khr, #mic");
pop("#date", 0.0, 0.4);
drawIn("#mic", {w("khrushchev") - 0.4}, 0.4); drawIn("#khr", {w("khrushchev") - 0.3}, 0.6);
pop("#radio", {w("moscow") - 0.2}, 0.35); wobble("#radio", {w("radio")}, 3, 3);
fadeIn("#home", {w("missiles") - 0.2}, 0.4);
show("#sea", {w("home") - 0.3}, 0.3);
tl.set("[id^='rs']", {{ opacity: 1 }}, {w("home") - 0.3});
tl.to("[id^='rs']", {{ x: "+=1700", duration: 4.5, ease: "power1.in" }}, {w("home") - 0.3});
stampIn("#over", {w("over") - 0.1});
fadeOut("#over, #khr, #mic, #radio, #home, #date", {w("world") - 0.3}, 0.3);
tl.fromTo("#np1", {{ opacity: 0, rotation: -40, scale: 0.3, transformOrigin: "50% 50%" }}, {{ opacity: 1, rotation: 0, scale: 1, duration: 0.5, ease: "back.out(1.5)" }}, {w("looked")});
tl.fromTo("#np2", {{ opacity: 0, rotation: 40, scale: 0.3, transformOrigin: "50% 50%" }}, {{ opacity: 1, rotation: 0, scale: 1, duration: 0.5, ease: "back.out(1.5)" }}, {w("stood") - 0.2});
'''
    build("19", svg, js)


# =============================================================== 20 - it was a trade / the scariest part
def s20():
    w = W("20")
    nukes = "".join(nuke(f"nk{i}", 760 + i * 140, 790 + (i % 2) * 30, 0.7) for i in range(4))
    svg = f'''
<g id="trade">
  {table("table", 960, 780, 1.1, cloth="#f3f0e8")}
  {person("jfk", 520, 560, 1.35, "jfk", arms="M-30,-20 L-58,40 M30,-20 L120,120")}
  {person("khr", 1400, 575, 1.35, "khrushchev", arms="M30,-20 L58,40 M-30,-20 L-120,120")}
  <g id="under" opacity="0"><rect x="720" y="800" width="480" height="100" fill="#3b3f46"/>
    {envelope("e1", 820, 850, 0.5, hidden=False)}{envelope("e2", 1100, 850, 0.5, hidden=False)}</g>
  {text("lab1", 760, 960, "Turkey missiles", 40, USD)}{text("lab2", 1160, 960, "Cuba missiles", 40, SUD)}
  {person("stick", 160, 760, 1.0, "stick", arms=POINT_R)}
  {card("tr", 610, 60, 700, 120, [("It was a TRADE.", SU)], size=80)}
  {card("hid", 560, 200, 800, 100, [("kept secret for decades", INK2)], size=52)}
</g>
<g id="nums" opacity="0">
  {text("n10", 560, 360, "US estimate: 10,000 troops", 70, USD, hidden=False)}
  <path id="strike" d="M190,350 L930,345" stroke="{SU}" stroke-width="12" stroke-linecap="round" opacity="0"/>
  {text("n40", 1360, 360, "Reality: 40,000+", 90, SU)}
  <g id="minimap" opacity="0"><path d="{CARIB_CUBA}" transform="translate(-60,-20)" fill="{CULAND}" stroke="{INK}" stroke-width="6"/>
    {text("cb", 960, 920, "+ short-range nuclear weapons", 64, SUD, hidden=False)}</g>
  {nukes}
</g>
{text("day1", 960, 150, "...nuclear on day one", 110, SU)}'''
    js = f'''
prep("#table, #jfk, #khr, #stick");
drawIn("#table", 0.0, 0.4); drawIn("#jfk", 0.0, 0.5); drawIn("#khr", 0.1, 0.5); drawIn("#stick", 0.2, 0.4);
pop("#tr", {w("trade") - 0.1}, 0.4);
tl.to("#table .d:last-of-type", {{ y: "-=60", opacity: 0.15, duration: 0.4 }}, {w("both") - 0.1});
show("#under", {w("both")}, 0.3);
move("#e1", {w("gave")}, 280, 0, 0.8); move("#e2", {w("gave")}, -280, 0, 0.8);
fadeIn("#lab1, #lab2", {w("gave")}, 0.4);
pop("#hid", {w("hidden") - 0.2}, 0.4);
fadeOut("#trade", {w("scariest") - 0.3}, 0.3);
show("#nums", {w("time")}, 0.3);
fadeIn("#n10", {w("10") - 0.2}, 0.4);
show("#strike", {w("40") - 0.2}, 0.15);
pop("#n40", {w("40")}, 0.4);
show("#minimap", {w("short") - 0.3}, 0.4);
tl.fromTo("[id^='nk']", {{ opacity: 0, scale: 0.2, transformOrigin: "50% 50%" }}, {{ opacity: 1, scale: 1, duration: 0.3, stagger: 0.12, ease: "back.out(2)" }}, {w("nuclear")});
fadeOut("#n10, #strike", {w("kennedy") - 0.2}, 0.2);
pop("#day1", {w("gone") - 0.2}, 0.4); shake({w("day")}, 4);
'''
    build("20", svg, js)


# =============================================================== 21 - aftermath
def s21():
    w = W("21")
    svg = f'''
{person("jfk", 380, 600, 1.25, "jfk", arms="M-30,-20 L-58,40 M30,-20 L70,-30 L60,-110", face="flat")}
{person("khr", 1540, 600, 1.25, "khrushchev", arms="M30,-20 L58,40 M-30,-20 L-70,-30 L-60,-110", face="flat")}
{phone("ph1", 640, 820, 1.0, US)}{phone("ph2", 1280, 820, 1.0, SU)}
{dashed_arrow("cord", "M700,840 C820,980 1100,980 1220,840", INK, 6)}
{card("hl", 510, 60, 900, 110, [("The Washington - Moscow hotline (1963)", INK)], size=56)}
{scroll("treaty", 960, 470, "Nuclear Test Ban Treaty", "signed 1963", 1.2)}
{text("hum", 1540, 280, "&quot;a humiliation&quot;", 60, SUD)}
{text("y64", 1540, 950, "forced out - 1964", 64, SUD)}'''
    js = f'''
prep("#jfk, #khr, #cord");
drawIn("#jfk", 0.0, 0.6); drawIn("#khr", 0.2, 0.6);
blink("#jfk", {w("shaken") - 0.3}); blink("#khr", {w("shaken")});
pop("#ph1", {w("hotline") - 0.3}, 0.35); pop("#ph2", {w("hotline") - 0.1}, 0.35);
drawIn("#cord", {w("between")}, 0.7); pop("#hl", {w("washington")}, 0.4);
bob("#ph1 .handset, #ph2 .handset", {w("talk")}, 3, 10);
fadeOut("#hl", {w("within") - 0.3}, 0.2);
pop("#treaty", {w("treaty") - 0.2}, 0.45);
fadeOut("#treaty, #ph1, #ph2, #cord, #jfk", {w("khrushchev") - 0.3}, 0.3);
move("#khr", {w("khrushchev")}, -580, 0, 0.6);
fadeIn("#hum", {w("humiliation") - 0.3}, 0.4);
tl.to("#hum", {{ x: "-=580", duration: 0.01 }}, 0);
tl.to("#khr", {{ x: "+=1300", rotation: 20, duration: 1.0, ease: "power2.in" }}, {w("forced") - 0.1});
pop("#y64", {w("forced")}, 0.4); tl.to("#y64", {{ x: "-=580", duration: 0.01 }}, 0);
'''
    build("21", svg, js)


# =============================================================== 22 - wrap-up
def s22():
    w = W("22")
    svg = f'''
{calendar("cal", 960, 400, "13", "DAYS", 1.6)}
{text("notst", 960, 150, "not a staring contest...", 70, INK2, 400)}
{envelope("ic1", 460, 520, 1.3, "a secret deal")}
<g id="ic2" transform="translate(960,520)" opacity="0">{clover("cl", 0, -20, 1.6, hidden=False).replace(' opacity="0"', '')}
  <text x="0" y="170" text-anchor="middle" font-family="Cav" font-weight="700" font-size="44" fill="{INK}">a lot of luck</text></g>
<g id="ic3" transform="translate(1460,560)" opacity="0">{red_button("btn", 0, 0, 1.2, hidden=False).replace(' opacity="0"', '')}
  <text x="0" y="130" text-anchor="middle" font-family="Cav" font-weight="700" font-size="44" fill="{INK}">people who said NO</text></g>
<g id="end" opacity="0"><rect width="1920" height="1080" fill="{BG}"/><rect width="1920" height="1080" fill="url(#lines)"/>
  {person("stick", 480, 700, 1.6, "stick", arms=WAVE_R, hidden=False)}
  <text x="1180" y="420" text-anchor="middle" font-family="Cav" font-weight="700" font-size="140" fill="{INK}">Stick to <tspan fill="{SU}">History</tspan></text>
  <g id="sub" transform="translate(1180,600)"><rect x="-200" y="-60" width="400" height="110" rx="20" fill="{SU}" stroke="{INK}" stroke-width="5"/>
    <text y="18" text-anchor="middle" font-family="Cav" font-weight="700" font-size="64" fill="#fff">SUBSCRIBE</text></g>
  <text x="1180" y="790" text-anchor="middle" font-family="Cav" font-weight="400" font-size="56" fill="{INK2}">see you in the next one</text></g>'''
    js = f'''
pop("#cal", {w("13") - 0.1}, 0.45);
tl.to("#cal", {{ x: "-=0", duration: 0.01 }}, 0);
fadeIn("#notst", {w("staring") - 0.3}, 0.4);
tl.to("#cal", {{ opacity: 0, scale: 0.4, y: "-=200", transformOrigin: "50% 50%", duration: 0.4 }}, {w("survived") - 0.3});
fadeOut("#notst", {w("survived") - 0.3}, 0.2);
pop("#ic1", {w("secret") - 0.1}, 0.4);
pop("#ic2", {w("luck") - 0.2}, 0.4);
pop("#ic3", {w("people") - 0.2}, 0.4);
tl.to("#btn .hand", {{ y: "+=60", duration: 0.35, ease: "power1.in" }}, {w("push") - 0.2});
tl.to("#btn .hand", {{ y: "-=90", duration: 0.35, ease: "power2.out" }}, {w("button")});
show("#end", {w("i'm") - 0.2}, 0.4);
wobble("#end #stick .arms", {w("stick")}, 4, 8, "30px -20px");
tl.fromTo("#sub", {{ scale: 0.6, transformOrigin: "50% 50%" }}, {{ scale: 1, duration: 0.4, ease: "back.out(2)" }}, {w("history") - 0.2});
bob("#sub", {w("see")}, 3, 8);
'''
    build("22", svg, js)


SCENES = {f"{i:02d}": globals()[f"s{i:02d}"] for i in range(1, 23)}

if __name__ == "__main__":
    OUT.mkdir(exist_ok=True)
    for n in (sys.argv[1:] or SCENES):
        SCENES[n]()
        print("built scene", n)
