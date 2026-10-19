#!/usr/bin/env python3
"""找毛刺、小缺口和窄缝：把每个字按 1 像素 = 1 单位渲染，
开运算（先腐蚀再膨胀）去掉的细突起算毛刺，闭运算（先膨胀再腐蚀）填上的细凹缝算缺口；
两块不相连的墨（比如点和横）之间最近处不到 --gap 单位，算窄缝（看着像没对齐的细缝）。

用法：python3 tools/defects.py sample/Duyan-Sample.ttf [字符…] [--crops 输出目录]
笔画本来就有的尖（撇尾、捺脚、喙尖、v 的底尖、衬线尖）也会被开运算削掉一点，
所以只报告「面积够大、而且不在笔画尖端」的点：尖端的特征是突起本身很长很细。
"""
import argparse
import os

import numpy as np
from scipy import ndimage
from fontTools.pens.basePen import BasePen
from fontTools.ttLib import TTFont
from PIL import Image, ImageDraw, ImageFilter

PAD = 200


class FlatPen(BasePen):
    def __init__(self, gs):
        super().__init__(gs)
        self.polys, self.cur = [], []

    def _moveTo(self, p):
        self.cur = [p]

    def _lineTo(self, p):
        self.cur.append(p)

    def _qCurveToOne(self, a, b):
        p0 = self.cur[-1]
        n = max(10, int((abs(a[0] - p0[0]) + abs(a[1] - p0[1]) + abs(b[0] - a[0]) + abs(b[1] - a[1])) / 2))
        for i in range(1, n + 1):
            t = i / n
            self.cur.append(((1 - t) ** 2 * p0[0] + 2 * (1 - t) * t * a[0] + t * t * b[0],
                             (1 - t) ** 2 * p0[1] + 2 * (1 - t) * t * a[1] + t * t * b[1]))

    def _curveToOne(self, a, b, c):
        p0 = self.cur[-1]
        for i in range(1, 15):
            t = i / 14
            self.cur.append(tuple((1 - t) ** 3 * p0[k] + 3 * (1 - t) ** 2 * t * a[k] + 3 * (1 - t) * t * t * b[k] + t ** 3 * c[k]
                                  for k in range(2)))

    def _closePath(self):
        self.polys.append(self.cur)
        self.cur = []


def raster(gs, name, w=1400, h=1400, oy=1000):
    """非零环绕填充：每条轮廓按方向加减。返回 bool 数组（True 是墨）。"""
    pen = FlatPen(gs)
    gs[name].draw(pen)
    acc = np.zeros((h, w), np.int16)
    for poly in pen.polys:
        pts = [(x + PAD, oy - y) for x, y in poly]
        area = sum(pts[i][0] * pts[(i + 1) % len(pts)][1] - pts[(i + 1) % len(pts)][0] * pts[i][1] for i in range(len(pts)))
        layer = Image.new("L", (w, h), 0)
        ImageDraw.Draw(layer).polygon(pts, fill=1)
        acc += np.array(layer, np.int16) * (1 if area > 0 else -1)
    return acc != 0


def morph(ink, size, kind):
    img = Image.fromarray((ink * 255).astype(np.uint8))
    if kind == "open":
        img = img.filter(ImageFilter.MinFilter(size)).filter(ImageFilter.MaxFilter(size))
    else:
        img = img.filter(ImageFilter.MaxFilter(size)).filter(ImageFilter.MinFilter(size))
    return np.array(img) > 127


def blobs(mask, min_area):
    """简单的连通区域：返回 [(面积, 中心 x, 中心 y, 外框宽, 外框高)]。"""
    seen = np.zeros_like(mask)
    out = []
    ys, xs = np.nonzero(mask)
    for y0, x0 in zip(ys, xs):
        if seen[y0, x0]:
            continue
        stack, pts = [(y0, x0)], []
        seen[y0, x0] = True
        while stack:
            y, x = stack.pop()
            pts.append((y, x))
            for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                ny, nx = y + dy, x + dx
                if 0 <= ny < mask.shape[0] and 0 <= nx < mask.shape[1] and mask[ny, nx] and not seen[ny, nx]:
                    seen[ny, nx] = True
                    stack.append((ny, nx))
        if len(pts) >= min_area:
            py, px = zip(*pts)
            out.append((len(pts), sum(px) / len(px), sum(py) / len(py), max(px) - min(px) + 1, max(py) - min(py) + 1))
    return out


def narrow_gaps(ink, gap):
    """两两比较不相连的墨块，最近距离小于 gap 的报出来：返回 [(距离, x, y)]，x、y 是最近两点的中点。"""
    labels, n = ndimage.label(ink)
    out = []
    for i in range(1, n + 1):
        dist, (iy, ix) = ndimage.distance_transform_edt(labels != i, return_indices=True)
        for j in range(i + 1, n + 1):
            m = labels == j
            d = np.where(m, dist, np.inf)
            k = np.unravel_index(np.argmin(d), d.shape)
            if d[k] < gap:
                y0, x0 = k
                y1, x1 = iy[k], ix[k]
                out.append((round(float(d[k])), round((x0 + x1) / 2 - PAD), round(1000 - (y0 + y1) / 2)))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("font")
    ap.add_argument("chars", nargs="?", default=None)
    ap.add_argument("--size", type=int, default=9, help="检测窗口（单位），默认 9：比约 8 单位还细的突起 / 凹缝")
    ap.add_argument("--min-area", type=int, default=6)
    ap.add_argument("--gap", type=int, default=34, help="不相连的两笔之间至少要留的空（单位）")
    ap.add_argument("--crops", default=None)
    args = ap.parse_args()
    f = TTFont(args.font)
    gs, cmap = f.getGlyphSet(), f.getBestCmap()
    chars = args.chars or "".join(chr(u) for u in sorted(cmap) if u > 32)
    total = 0
    for ch in chars:
        name = cmap.get(ord(ch))
        if not name:
            continue
        ink = raster(gs, name)
        spurs = ink & ~morph(ink, args.size, "open")
        notches = morph(ink, args.size, "close") & ~ink
        found = []
        for kind, m in (("毛刺", spurs), ("缺口", notches)):
            for area, cx, cy, bw, bh in blobs(m, args.min_area):
                # 笔画尖端：被削掉的部分细长（长宽比大）而且面积大，多半是有意的尖，不算毛刺
                if kind == "毛刺" and max(bw, bh) > 3.2 * args.size and area > 60:
                    continue
                found.append((kind, area, round(cx - PAD), round(1000 - cy), bw, bh))
        for d, x, y in narrow_gaps(ink, args.gap):
            found.append(("窄缝", d, x, y, 0, 0))
        total += len(found)
        if found:
            print(ch, " ".join(f"{k}@({x},{y}) {'距离' if k == '窄缝' else '面积'}{a}" for k, a, x, y, bw, bh in found))
            if args.crops:
                os.makedirs(args.crops, exist_ok=True)
                img = Image.fromarray(np.where(ink, 0, 255).astype(np.uint8)).convert("RGB")
                d = ImageDraw.Draw(img)
                for k, a, x, y, bw, bh in found:
                    X, Y = x + PAD, 1000 - y
                    color = {"毛刺": (220, 40, 40), "缺口": (40, 90, 220)}.get(k, (230, 150, 0))
                    d.ellipse([X - 26, Y - 26, X + 26, Y + 26], outline=color, width=4)
                img.resize((img.width // 2, img.height // 2)).save(os.path.join(args.crops, f"U{ord(ch):04X}.png"))
    print("合计", total)


if __name__ == "__main__":
    main()
