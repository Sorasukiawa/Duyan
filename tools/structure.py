#!/usr/bin/env python3
"""量汉字的结构：字面、重心、灰度、部件间距，按 docs/STRUCTURE.md 的规范报出超标的字。

    python3 tools/structure.py              # 列出所有汉字的数据和超标项
    python3 tools/structure.py sheet.png    # 另外出一张总览图：字面框、重心十字、部件间距

字面：墨的外框（按轮廓量，不受光栅范围限制）。重心：墨的面积中心。灰度：墨占字面框的比例。
部件间距：用 lr()、tb() 拼出来的字，两个部件之间最近的距离（部件互相碰到时是 0），和 layout.fit 用的是同一把尺。
减细：这个字画的时候用的 weight() 档位，和按轮廓条数该用的档位（layout.weight_for）比。
都按出字体后的坐标量（汉字已经从设计坐标压到字身里，见 layout.HAN_SY）。
"""
import os
import sys

import numpy as np
from PIL import Image, ImageDraw

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
sys.path.insert(0, HERE)
import glyphs  # noqa: E402
import layout  # noqa: E402
from outline import bounds  # noqa: E402

PX = 4                         # 光栅化时一个像素 = 4 单位
TOP, BOTTOM = 880, -120        # 汉字的字身（1000 × 1000）


def raster(shapes):
    w = h = 1000 // PX
    im = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(im)
    for hole in (False, True):
        for s in shapes:
            if s.hole == hole:
                d.polygon([(x / PX, (TOP - y) / PX) for x, y in s.flatten(4)], fill=0 if hole else 255)
    return np.asarray(im, dtype=float) / 255


def measure(shapes):
    a = raster(shapes)
    face = bounds(shapes)          # 光栅只画字身那么大，出了字身的墨会被裁掉，字面要按轮廓量
    m = a.sum()
    yy, xx = np.mgrid[0:a.shape[0], 0:a.shape[1]]
    cx = (xx * a).sum() / m * PX + PX / 2
    cy = TOP - ((yy * a).sum() / m * PX + PX / 2)
    area = (face[2] - face[0]) * (face[3] - face[1])
    return {"face": face, "center": (cx, cy), "gray": m * PX * PX / area}


def part_gap(shapes):
    """两个部件之间最近的距离和关系（右 / 下）；不是 lr()、tb() 拼的字返回 (None, None)。"""
    groups = {}
    for s in shapes:
        if getattr(s, "part", None):
            groups.setdefault(s.part, []).append(s)
    if set(groups) == {"左", "右"}:
        return layout.gap(groups["左"], groups["右"], "right"), "右"
    if set(groups) == {"上", "下"}:
        return layout.gap(groups["上"], groups["下"], "bottom"), "下"
    if set(groups) == {"外", "内"}:
        return layout.gap(groups["外"], groups["内"], "any"), "内"
    return None, None


def problems(ch, r):
    out = []
    x0, y0, x1, y1 = r["face"]
    fx0, fy0, fx1, fy1 = layout.FACE
    if x0 < fx0 or x1 > fx1 or y0 < fy0 or y1 > fy1:
        out.append(f"出了字面框 {layout.FACE}：{tuple(round(v) for v in r['face'])}")
    w = r.get("weight")
    if w is not None and ch not in layout.WEIGHT_EXCEPT:
        want = layout.weight_for(r["n"], r["composed"])
        if len(w) > 1:
            out.append(f"一个字里用了几档减细 {w}")
        elif abs(w[0] - want) > 1e-9:
            out.append(f"减细 {w[0]}，{r['n']} 条轮廓{'（拼的字）' if r['composed'] else ''}应为 {want}")
    g, kind = r.get("gap"), r.get("kind")
    if g is not None:
        lo, hi = {"右": layout.LR_GAP_RANGE, "下": layout.TB_GAP_RANGE, "内": layout.BAO_GAP_RANGE}[kind]
        if g == 0:
            out.append("两个部件碰在一起")
        elif not lo <= g <= hi:
            out.append(f"部件间距 {g:.0f}，应在 {lo}–{hi}")
        cx, cy = r["center"]
        if ch in layout.CENTER_EXCEPT:
            pass
        elif kind == "右" and not layout.LR_CENTER_X[0] <= cx <= layout.LR_CENTER_X[1]:
            out.append(f"重心横坐标 {cx:.0f}，应在 {layout.LR_CENTER_X[0]}–{layout.LR_CENTER_X[1]}")
        if kind == "下" and not layout.TB_CENTER_Y[0] <= cy <= layout.TB_CENTER_Y[1]:
            out.append(f"重心纵坐标 {cy:.0f}，应在 {layout.TB_CENTER_Y[0]}–{layout.TB_CENTER_Y[1]}")
    return out


def han_table():
    t = glyphs.collect()
    return {ch: sh for ch, (sh, adv) in t.items() if 0x4E00 <= ord(ch) <= 0x9FFF}


def run(table=None):
    """table 是 glyphs.collect() 的结果；不给就自己 collect 一遍。"""
    if table is None:
        table = glyphs.collect()
    rows = {}
    for ch, (sh, adv) in table.items():
        if not 0x4E00 <= ord(ch) <= 0x9FFF:
            continue
        r = measure(sh)
        r["gap"], r["kind"] = part_gap(sh)
        r["weight"], r["n"] = glyphs.WEIGHT.get(ch), len(sh)
        r["composed"] = any(getattr(s, "part", None) for s in sh)
        rows[ch] = r
    return rows


def sheet(rows, path, cols=10, cell=150):
    t = han_table()
    n = len(rows)
    im = Image.new("RGB", (cols * cell, (n + cols - 1) // cols * cell), "white")
    d = ImageDraw.Draw(im)
    k = cell / 1000 * 0.9
    for i, (ch, r) in enumerate(rows.items()):
        ox, oy = (i % cols) * cell + cell * 0.05, (i // cols) * cell + cell * 0.05
        P = lambda x, y: (ox + x * k, oy + (TOP - y) * k)
        d.rectangle([P(layout.FACE[0], layout.FACE[3]), P(layout.FACE[2], layout.FACE[1])], outline=(205, 215, 230))
        for hole in (False, True):
            for s in t[ch]:
                if s.hole == hole:
                    d.polygon([P(x, y) for x, y in s.flatten(6)], fill="white" if hole else (40, 40, 40))
        cx, cy = P(*r["center"])
        bad = problems(ch, r)
        col = (220, 50, 50) if bad else (40, 140, 220)
        d.line([cx - 6, cy, cx + 6, cy], fill=col, width=2)
        d.line([cx, cy - 6, cx, cy + 6], fill=col, width=2)
        if bad:
            d.rectangle([ox - 3, oy - 3, ox + 1000 * k + 3, oy + 1000 * k + 3], outline=(220, 50, 50), width=2)
    im.save(path)


if __name__ == "__main__":
    rows = run()
    bad = 0
    for ch, r in rows.items():
        p = problems(ch, r)
        x0, y0, x1, y1 = r["face"]
        g = "" if r["gap"] is None else f" 部件间距 {r['gap']:.0f}"
        line = f"{ch} 字面 {x0:.0f},{y0:.0f}–{x1:.0f},{y1:.0f} 重心 {r['center'][0]:.0f},{r['center'][1]:.0f} 灰度 {r['gray']:.2f}{g}"
        if p:
            bad += 1
            line += "  ← " + "；".join(p)
        print(line)
    print(f"{len(rows)} 个汉字，{bad} 个超标")
    if len(sys.argv) > 1:
        sheet(rows, sys.argv[1])
