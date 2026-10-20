#!/usr/bin/env python3
"""生成小克体的文字标、单字图标和宣传封面，全部用小克体自己的字形。

- brand/logo.svg、logo-dark.svg：文字标。「小克体」三个字各写在一个田字格里（小朋友练字的格子），后面跟西文 Xiaoke。
- brand/mark.svg：田字格里一个「克」，透明底；brand/icon.svg：纸色圆角方块上的同一个图案（头像、网站图标用）。
- brand/cover.png：宣传封面 / GitHub 社交预览图，由 brand/cover.html 截图得到。

SVG 里的字直接取 sample/Xiaoke-Sample.otf 的轮廓，不依赖装字体；PNG 用无界面的 Chrome 截图导出
（脚本自己起一个本地网页服务）。先跑 build.py 出字体，再跑：

    python3 tools/brand.py
"""
import functools
import http.server
import os
import re
import subprocess
import sys
import tempfile
import threading

from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.svgPathPen import SVGPathPen
from fontTools.ttLib import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
import kern  # noqa: E402

OUT = os.path.join(ROOT, "brand")
FONT = os.path.join(ROOT, "sample", "Xiaoke-Sample.otf")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

INK, PAPER, ACCENT = "#1D1C1A", "#F4F1EA", "#21505C"          # 黛青：呼应「渡」的水色
INK_DARK, ACCENT_DARK = "#ECE9E2", "#7FB3BE"
GRID, GRID_DARK = "#9DB3B8", "#4E6A70"     # 田字格中间的虚线：黛青兑上纸色

_font = TTFont(FONT)
_gs, _cmap, _hmtx = _font.getGlyphSet(), _font.getBestCmap(), _font["hmtx"]
_kern = kern.pairs()


def _glyph(ch):
    if ord(ch) not in _cmap:
        sys.exit(f"字体里还没有「{ch}」")
    return _cmap[ord(ch)]


def text(s, size, x0, y0, fill):
    """一行字：返回 (SVG 片段, 宽度, 墨的上下沿)。x0, y0 是基线起点，字距按 kern.py。"""
    k = size / 1000
    x, prev, parts = 0, None, []
    top, bottom = -1e9, 1e9
    for ch in s:
        if ch == " ":
            x += _hmtx["space"][0]
            prev = None
            continue
        g = _glyph(ch)
        x += _kern.get((prev, ch), 0) if prev else 0
        pen = SVGPathPen(_gs)
        _gs[g].draw(pen)
        b = BoundsPen(_gs)
        _gs[g].draw(b)
        top, bottom = max(top, b.bounds[3]), min(bottom, b.bounds[1])
        parts.append(f'<path transform="translate({x0 + x * k:.2f} {y0:.2f}) scale({k:.5f} {-k:.5f})" '
                     f'd="{pen.getCommands()}"/>')
        x += _hmtx[g][0]
        prev = ch
    return f'<g fill="{fill}">{"".join(parts)}</g>', x * k, (y0 - top * k, y0 - bottom * k)


def mark(x, y, size, ch="渡", fill=ACCENT, fit=0.8):
    """单字：字形墨框居中放进 size × size 的方框。"""
    b = BoundsPen(_gs)
    _gs[_glyph(ch)].draw(b)
    x0, y0, x1, y1 = b.bounds
    k = size * fit / max(x1 - x0, y1 - y0)
    g, _, _ = text(ch, k * 1000, x + size / 2 - (x0 + x1) / 2 * k, y + size / 2 + (y0 + y1) / 2 * k, fill)
    return g


def tianzige(x, y, size, line=ACCENT, dash=GRID):
    """田字格：外框实线，中间一横一竖虚线。"""
    sw = max(2.0, size * 0.022)
    d = size * 0.06
    return (f'<g fill="none"><rect x="{x + sw / 2:.2f}" y="{y + sw / 2:.2f}" width="{size - sw:.2f}" height="{size - sw:.2f}" '
            f'stroke="{line}" stroke-width="{sw:.2f}"/>'
            f'<path d="M{x + size / 2:.2f} {y + sw:.2f}V{y + size - sw:.2f}M{x + sw:.2f} {y + size / 2:.2f}H{x + size - sw:.2f}" '
            f'stroke="{dash}" stroke-width="{sw * 0.6:.2f}" stroke-dasharray="{d:.2f} {d * 0.8:.2f}"/></g>')


def svg(w, h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:.0f}" height="{h:.0f}" '
            f'viewBox="0 0 {w:.0f} {h:.0f}">{body}</svg>\n')


def write(name, content):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as fh:
        fh.write(content)
    print("已生成", f"brand/{name}")


def check_cover():
    """封面上的字都要是小克体已经有的字，不然会悄悄换成系统字体。"""
    html = open(os.path.join(OUT, "cover.html"), encoding="utf-8").read()
    body = re.sub(r"<style.*?</style>|<title>.*?</title>|<[^>]+>", "", html, flags=re.S)
    missing = sorted({c for c in body if not c.isspace() and ord(c) not in _cmap})
    if missing:
        sys.exit("封面上有字体里还没有的字：" + " ".join(missing))


def serve():
    class Quiet(http.server.SimpleHTTPRequestHandler):
        def log_message(self, *a):
            pass
    httpd = http.server.ThreadingHTTPServer(("127.0.0.1", 0), functools.partial(Quiet, directory=ROOT))
    threading.Thread(target=httpd.serve_forever, daemon=True).start()
    return httpd, f"http://127.0.0.1:{httpd.server_address[1]}"


def screenshot(url, out, w, h, scale=2, transparent=False):
    with tempfile.TemporaryDirectory() as profile:
        cmd = [CHROME, "--headless=new", f"--user-data-dir={profile}", "--hide-scrollbars",
               f"--window-size={w},{h}", f"--force-device-scale-factor={scale}",
               f"--screenshot={out}", "--virtual-time-budget=5000"]
        if transparent:
            cmd.append("--default-background-color=00000000")
        subprocess.run(cmd + [url], check=True, capture_output=True)
    print("已生成", os.path.relpath(out, ROOT))


def main():
    os.makedirs(OUT, exist_ok=True)
    check_cover()

    # 1. 文字标：「小克体」三个字各占一个田字格，后面跟 Xiaoke
    box, gap = 150, 12
    boxes = "".join(tianzige(k * (box + gap), 0, box) + mark(k * (box + gap), 0, box, ch, INK, fit=0.74)
                    for k, ch in enumerate("小克体"))
    x0 = 3 * box + 2 * gap + 44
    en, ew, (et, eb) = text("Xiaoke", 118, x0, box * 0.74, INK)
    w, h = x0 + ew + 8, box
    body = boxes + en
    write("logo.svg", svg(w, h, body))
    write("logo-dark.svg", svg(w, h, body.replace(INK, INK_DARK).replace(ACCENT, ACCENT_DARK).replace(GRID, GRID_DARK)))

    # 2. 单字图标：田字格里一个「克」
    write("mark.svg", svg(512, 512, tianzige(8, 8, 496) + mark(8, 8, 496, "克", INK, fit=0.76)))
    write("icon.svg", svg(512, 512, f'<rect width="512" height="512" rx="96" fill="{PAPER}"/>'
                                    + tianzige(72, 72, 368) + mark(72, 72, 368, "克", INK, fit=0.76)))

    # 3. PNG 和封面
    httpd, base = serve()
    try:
        for name, ww, hh in (("logo", w, h), ("mark", 512, 512), ("icon", 512, 512)):
            screenshot(f"{base}/brand/{name}.svg", os.path.join(OUT, f"{name}.png"), round(ww), round(hh),
                       transparent=True)
        screenshot(f"{base}/brand/cover.html", os.path.join(OUT, "cover.png"), 1280, 640)
    finally:
        httpd.shutdown()


if __name__ == "__main__":
    main()
