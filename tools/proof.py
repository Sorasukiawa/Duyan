#!/usr/bin/env python3
"""造字软件那样的预览：左边是实心字，右边是轮廓、节点和控制柄，检查出的问题用红圈标出。

用法：python3 tools/proof.py 输出.png [字符…] [--scale 0.5] [--cols 4]
节点：方块是角点，圆点是光滑点，绿色是应该藏起来的点（hid），橙色是有意的尖（tip）。
"""
import argparse
import os
import sys

import numpy as np
from PIL import Image, ImageDraw, ImageFont

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "tools"))
import glyphs  # noqa: E402
from check import check, _poly, winding  # noqa: E402

FONT = "/System/Library/Fonts/Hiragino Sans GB.ttc"


def raster(shapes, sc, ox, oy, w, h):
    acc = np.zeros((h, w), np.int16)
    for s in shapes:
        p = _poly(s, True)
        pts = [(ox + x * sc, oy - y * sc) for x, y in p]
        layer = Image.new("L", (w, h), 0)
        ImageDraw.Draw(layer).polygon(pts, fill=1)
        # 屏幕 y 向下：逆时针（正面积）的外轮廓在屏幕上是顺时针
        a = sum(pts[i][0] * pts[(i + 1) % len(pts)][1] - pts[(i + 1) % len(pts)][0] * pts[i][1] for i in range(len(pts)))
        acc += np.array(layer, np.int16) * (1 if a < 0 else -1)
    return acc != 0


def panel(ch, shapes, adv, sc):
    pad = 60
    x0, y1 = -60, 900
    W = int((adv + 120) * sc) + 2 * pad
    H = int(1150 * sc) + 2 * pad
    ox, oy = pad - x0 * sc, pad + y1 * sc
    im = Image.new("RGB", (W * 2, H), "white")
    d = ImageDraw.Draw(im)
    for y, c in ((0, (170, 170, 200)), (540, (210, 210, 230)), (720, (210, 210, 230)), (-220, (225, 225, 235)), (760, (225, 225, 235))):
        for k in (0, W):
            d.line([(k + 10, oy - y * sc), (k + W - 10, oy - y * sc)], fill=c)
    ink = raster(shapes, sc, ox, oy, W, H)
    solid = Image.fromarray(np.where(ink, 0, 255).astype(np.uint8)).convert("RGB")
    im.paste(solid.crop((0, 0, W, H)), (0, 0), Image.fromarray((ink * 255).astype(np.uint8)))
    ghost = Image.fromarray(np.where(ink, 228, 255).astype(np.uint8)).convert("RGB")
    im.paste(ghost, (W, 0), Image.fromarray((ink * 255).astype(np.uint8)))
    P = lambda x, y: (W + ox + x * sc, oy - y * sc)
    colors = [(30, 30, 30), (40, 90, 200), (150, 60, 160), (0, 120, 120), (160, 100, 0)]
    for k, s in enumerate(shapes):
        col = colors[k % len(colors)]
        pts = [P(*q) for q in s.flatten(3)]
        d.line(pts + [pts[0]], fill=col, width=2)
        for seg in s.segments():
            if seg[0] == "curve":
                d.line([P(*seg[1]), P(*seg[2])], fill=(150, 150, 150))
                d.line([P(*seg[4]), P(*seg[3])], fill=(150, 150, 150))
                for h in (seg[2], seg[3]):
                    hx, hy = P(*h)
                    d.ellipse((hx - 2, hy - 2, hx + 2, hy + 2), outline=(120, 120, 120))
        for q in s.nodes:
            x, y = P(q.x, q.y)
            c = (0, 160, 60) if q.hid else (230, 120, 0) if q.tip else col
            r = 4
            if q.corner:
                d.rectangle((x - r, y - r, x + r, y + r), fill=c)
            else:
                d.ellipse((x - r, y - r, x + r, y + r), fill=c)
    font = ImageFont.truetype(FONT, 18)
    issues = check(shapes)
    for kind, x, y, msg in issues:
        for base in (0, W):
            cx, cy = base + ox + x * sc, oy - y * sc
            d.ellipse((cx - 14, cy - 14, cx + 14, cy + 14), outline=(230, 30, 30), width=3)
    d.text((10, 8), ch, fill=(80, 80, 80), font=ImageFont.truetype(FONT, 28))
    for i, (kind, x, y, msg) in enumerate(issues[:8]):
        d.text((W + 10, 8 + i * 22), f"{kind} ({x:.0f},{y:.0f}) {msg}", fill=(200, 30, 30), font=font)
    return im, issues


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("chars", nargs="?", default=None)
    ap.add_argument("--scale", type=float, default=0.5)
    ap.add_argument("--cols", type=int, default=3)
    a = ap.parse_args()
    table = glyphs.collect()
    chars = a.chars or "".join(table)
    panels = []
    total = 0
    for ch in chars:
        if ch not in table:
            continue
        shapes, adv = table[ch]
        im, issues = panel(ch, shapes, adv, a.scale)
        total += len(issues)
        for kind, x, y, msg in issues:
            print(ch, kind, f"({x:.0f},{y:.0f})", msg)
        panels.append(im)
    cols = a.cols
    rows = [panels[i:i + cols] for i in range(0, len(panels), cols)]
    W = max(sum(p.width for p in r) for r in rows)
    H = sum(max(p.height for p in r) for r in rows)
    sheet = Image.new("RGB", (W, H), "white")
    y = 0
    for r in rows:
        x = 0
        for p in r:
            sheet.paste(p, (x, y))
            x += p.width
        y += max(p.height for p in r)
    sheet.save(a.out)
    print("问题合计", total, sheet.size)


if __name__ == "__main__":
    main()
