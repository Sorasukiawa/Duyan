#!/usr/bin/env python3
"""生成渡言的文字标、单字图标和宣传封面，全部用渡言自己的字形。

- brand/logo.svg、logo-dark.svg：文字标「Duyan 渡言」（西文墨色，汉字黛青）。
- brand/mark.svg：单字图标「渡」，透明底；brand/icon.svg：纸色圆角方块上的「渡」（头像、网站图标用）。
- brand/cover.png：宣传封面 / GitHub 社交预览图，由 brand/cover.html 截图得到。

SVG 里的字直接取 sample/Duyan-Sample.otf 的轮廓，不依赖装字体；PNG 用无界面的 Chrome 截图导出
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
FONT = os.path.join(ROOT, "sample", "Duyan-Sample.otf")
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

INK, PAPER, ACCENT = "#1D1C1A", "#F4F1EA", "#21505C"          # 黛青：呼应「渡」的水色
INK_DARK, ACCENT_DARK = "#ECE9E2", "#7FB3BE"

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


def svg(w, h, body):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{w:.0f}" height="{h:.0f}" '
            f'viewBox="0 0 {w:.0f} {h:.0f}">{body}</svg>\n')


def write(name, content):
    with open(os.path.join(OUT, name), "w", encoding="utf-8") as fh:
        fh.write(content)
    print("已生成", f"brand/{name}")


def check_cover():
    """封面上的字都要是渡言已经有的字，不然会悄悄换成系统字体。"""
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

    # 1. 文字标：Duyan 渡言。汉字和西文同字号，汉字的字面本来就比大写略高，正好压得住
    size, pad = 120, 6
    en, ew, (et, eb) = text("Duyan", size, 0, 0, INK)
    gap = size * 0.3
    zh, zw, (zt, zb) = text("渡言", size, ew + gap, 0, ACCENT)
    top, bottom = min(et, zt) - pad, max(eb, zb) + pad
    w, h = ew + gap + zw + pad, bottom - top
    body = f'<g transform="translate(0 {-top:.2f})">{en}{zh}</g>'
    write("logo.svg", svg(w, h, body))
    write("logo-dark.svg", svg(w, h, body.replace(INK, INK_DARK).replace(ACCENT, ACCENT_DARK)))

    # 2. 单字图标
    write("mark.svg", svg(512, 512, mark(0, 0, 512, fit=0.86)))
    write("icon.svg", svg(512, 512, f'<rect width="512" height="512" rx="96" fill="{PAPER}"/>' + mark(64, 64, 384)))

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
