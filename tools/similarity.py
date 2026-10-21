#!/usr/bin/env python3
"""原创性核对：把渡言的每个字和本机的现成字体逐字比较，看整体和单字有没有「像得过头」。

    python3 tools/similarity.py                    # 汉字和西文都比，字体用 sample/Duyan-Sample.otf
    python3 tools/similarity.py --han              # 只比汉字（--latin 只比西文）
    python3 tools/similarity.py --ref 某字体.otf    # 再加参考字体，.ttc 写成 路径:序号，可以写多个

参考字体只在内存里渲染、算数字，不保存也不输出它们的图，更不碰它们的轮廓。
参考字体用 macOS 自带的（缺哪款就跳过），在别的系统上用 --ref 指定。

每个字按墨的外框裁出来、拉到 128×128（去掉字面大小和宽窄的差别，只比笔画本身），比三个数（0～1，越大越像）：
  墨：两边的墨重合了多少（交集 / 并集）
  轮廓线：两边的轮廓线有多少落在对方 2 像素以内
  骨架：把笔画细化成一像素宽的中线，中线有多少落在对方 2 像素以内（不受粗细影响，看的是笔画摆在哪）

结论看「最近邻」：每款字体的每个字，和其余字体里最像的那款比，取所有字的中位数。渡言和参考字体用同一把尺，
参考字体之间的数就是基准线（2026-10-21 在 macOS 上量）：汉字里宋体、明朝体之间约 0.8（Songti SC 和 STSong
同属一个家族，也在这一档），楷体、仿宋这种写法完全不同的约 0.45～0.55；西文衬线之间 0.71～0.96。
渡言的最近邻到了参考字体的中位数，就是「和某款现成字体像得跟一般字体之间一样」，程序报错退出。
单字报出「轮廓线比任何两款参考字体之间都高」的字，要放大看笔形——
横画多的简单字（产、十、干）按外框拉齐后横线位置天然重合，数会偏高，多半是巧合。
"""
import argparse
import glob
import os
import sys

import numpy as np
from fontTools.ttLib import TTCollection, TTFont
from PIL import Image, ImageDraw, ImageFont

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
N = 128                        # 每个字拉到 N×N 再比
TOL = 2                        # 轮廓线、骨架相差 TOL 像素以内算吻合（约字面的 1.6%）
SIZE = 360                     # 渲染字号（像素）

SYS = "/System/Library/Fonts"
SUP = SYS + "/Supplemental"
ASSET = "/System/Library/AssetsV2/com_apple_MobileAsset_Font*/*/AssetData/"
# (名字, 路径或通配, 序号)
HAN_REFS = [
    ("宋·Songti SC", SUP + "/Songti.ttc", 6), ("宋·STSong", SUP + "/Songti.ttc", 4),
    ("宋·SimSong", ASSET + "SimSong.ttc", 0), ("明·Hiragino Mincho", SYS + "/ヒラギノ明朝 ProN.ttc", 0),
    ("仿·STFangsong", ASSET + "STFANGSO.ttf", 0), ("楷·Kaiti SC", ASSET + "Kaiti.ttc", 0),
    ("黑·Hiragino Sans GB", SYS + "/Hiragino Sans GB.ttc", 0),
]
LATIN_REFS = [
    ("Times New Roman", SUP + "/Times New Roman.ttf", 0), ("Georgia", SUP + "/Georgia.ttf", 0),
    ("Baskerville", SUP + "/Baskerville.ttc", 0), ("Big Caslon", SUP + "/BigCaslon.ttf", 0),
    ("Charter", SUP + "/Charter.ttc", 0), ("Iowan Old Style", SUP + "/Iowan Old Style.ttc", 0),
    ("Hoefler Text", SUP + "/Hoefler Text.ttc", 0), ("Palatino", SYS + "/Palatino.ttc", 0),
    ("PT Serif", SUP + "/PTSerif.ttc", 0), ("STIX Two Text", SUP + "/STIXTwoText.ttf", 0),
    ("New York", SYS + "/NewYork.ttf", 0), ("Athelas", SUP + "/Athelas.ttc", 0),
    ("Cochin", SUP + "/Cochin.ttc", 0), ("Didot", SUP + "/Didot.ttc", 0), ("Bodoni 72", SUP + "/Bodoni 72.ttc", 0),
]

_DISK = [(dy, dx) for dy in range(-TOL, TOL + 1) for dx in range(-TOL, TOL + 1) if dy * dy + dx * dx <= TOL * TOL]


def _shift(a, dy, dx):
    p = np.pad(a, TOL)
    return p[TOL + dy:TOL + dy + a.shape[0], TOL + dx:TOL + dx + a.shape[1]]


def _near(a):
    """离 a 不到 TOL 像素的地方。"""
    out = np.zeros_like(a)
    for dy, dx in _DISK:
        out |= _shift(a, dy, dx)
    return out


def _edge(a):
    inner = a.copy()
    inner[1:-1, 1:-1] = a[1:-1, 1:-1] & a[:-2, 1:-1] & a[2:, 1:-1] & a[1:-1, :-2] & a[1:-1, 2:]
    return a & ~inner


def _thin(a):
    """Zhang-Suen 细化：把笔画削成一像素宽的中线。"""
    im = a.astype(np.uint8)
    while True:
        changed = False
        for step in (0, 1):
            P = np.pad(im, 1)
            p2, p3, p4, p5 = P[:-2, 1:-1], P[:-2, 2:], P[1:-1, 2:], P[2:, 2:]
            p6, p7, p8, p9 = P[2:, 1:-1], P[2:, :-2], P[1:-1, :-2], P[:-2, :-2]
            ring = [p2, p3, p4, p5, p6, p7, p8, p9, p2]
            b = sum(x.astype(int) for x in ring[:8])
            t = sum(((ring[i] == 0) & (ring[i + 1] == 1)).astype(int) for i in range(8))
            if step == 0:
                c = (p2 * p4 * p6 == 0) & (p4 * p6 * p8 == 0)
            else:
                c = (p2 * p4 * p8 == 0) & (p2 * p6 * p8 == 0)
            m = (im == 1) & (b >= 2) & (b <= 6) & (t == 1) & c
            if m.any():
                im[m] = 0
                changed = True
        if not changed:
            return im.astype(bool)


class Face:
    def __init__(self, name, path, index=0):
        self.name = name
        self.font = ImageFont.truetype(path, SIZE, index=index)
        f = TTCollection(path).fonts[index] if path.lower().endswith(".ttc") else TTFont(path, lazy=True)
        self.cmap = set(f.getBestCmap() or {})
        self.cache = {}

    def get(self, ch):
        """(墨, 轮廓线, 轮廓线附近, 骨架, 骨架附近)；字体里没有这个字时返回 None。"""
        if ch not in self.cache:
            self.cache[ch] = self._feat(ch) if ord(ch) in self.cmap else None
        return self.cache[ch]

    def _feat(self, ch):
        im = Image.new("L", (SIZE * 2, SIZE * 2), 0)
        ImageDraw.Draw(im).text((SIZE // 2, int(SIZE * 1.4)), ch, font=self.font, fill=255, anchor="ls")
        bb = im.getbbox()
        if not bb or bb[2] - bb[0] < 4 or bb[3] - bb[1] < 4:
            return None
        ink = np.asarray(im.crop(bb).resize((N, N), Image.LANCZOS)) > 127
        edge, skel = _edge(ink), _thin(ink)
        return ink, edge, _near(edge), skel, _near(skel)


def _f1(a, a_near, b, b_near):
    if not a.any() or not b.any():
        return 0.0
    p, q = b_near[a].mean(), a_near[b].mean()
    return 0.0 if p + q == 0 else 2 * p * q / (p + q)


def score(fa, fb, ch):
    """(墨, 轮廓线, 骨架)；有一边没有这个字时返回 None。"""
    a, b = fa.get(ch), fb.get(ch)
    if a is None or b is None:
        return None
    return ((a[0] & b[0]).sum() / max(1, (a[0] | b[0]).sum()), _f1(a[1], a[2], b[1], b[2]), _f1(a[3], a[4], b[3], b[4]))


def load_refs(table, extra):
    faces = []
    for name, pattern, index in table:
        hits = sorted(glob.glob(pattern))
        if hits:
            faces.append(Face(name, hits[0], index))
    for spec in extra:
        path, _, index = spec.rpartition(":")
        if not index.isdigit():                        # 没写序号
            path, index = spec, "0"
        faces.append(Face(os.path.basename(path), path, int(index)))
    return faces


def compare(title, duyan, refs, chars, top):
    faces = [duyan] + refs
    chars = [c for c in chars if duyan.get(c) is not None and sum(f.get(c) is not None for f in refs) >= 2]
    s = {}
    for i, fa in enumerate(faces):
        for fb in faces[i + 1:]:
            for c in chars:
                r = score(fa, fb, c)
                if r is not None:
                    s[fa.name, fb.name, c] = s[fb.name, fa.name, c] = r

    print(f"\n【{title}】{len(chars)} 个字，参考字体 {len(refs)} 款：{'、'.join(f.name for f in refs)}")
    print(f"  {'字体':22s} {'骨架':>6s} {'轮廓线':>6s} {'墨':>6s}   最常撞上的")
    nn = {}
    for f in faces:
        sk, ed, ink, who = [], [], [], {}
        for c in chars:
            got = [(s[f.name, g.name, c], g.name) for g in faces if g is not f and (f.name, g.name, c) in s]
            if not got:
                continue
            best = max(got, key=lambda x: x[0][2])
            sk.append(best[0][2])
            who[best[1]] = who.get(best[1], 0) + 1
            ed.append(max(x[0][1] for x in got))
            ink.append(max(x[0][0] for x in got))
        if not sk:
            continue
        nn[f.name] = float(np.median(sk))
        top_who = max(who, key=who.get)
        print(f"  {f.name:22s} {np.median(sk):6.3f} {np.median(ed):6.3f} {np.median(ink):6.3f}   {top_who}（{who[top_who]}/{len(sk)}）")

    ref_nn = [v for k, v in nn.items() if k != duyan.name]
    if duyan.name not in nn or not ref_nn:
        return None
    mid = float(np.median(ref_nn))
    print(f"  → 渡言的骨架最近邻 {nn[duyan.name]:.3f}；参考字体之间 {min(ref_nn):.3f}～{max(ref_nn):.3f}，中位 {mid:.3f}")

    # 单字：轮廓线比任何两款参考字体之间都高的
    flagged = []
    for c in chars:
        mine = [(s[duyan.name, g.name, c][1], g.name) for g in refs if (duyan.name, g.name, c) in s]
        theirs = [s[a.name, b.name, c][1] for i, a in enumerate(refs) for b in refs[i + 1:] if (a.name, b.name, c) in s]
        if mine and theirs:
            e, who = max(mine)
            if e > max(theirs):
                flagged.append((e, c, who, max(theirs)))
    flagged.sort(reverse=True)
    if flagged:
        print(f"  轮廓线比任何两款参考字体之间都高的字（{len(flagged)} 个，放大看笔形）：")
        for e, c, who, m in flagged[:top]:
            print(f"    {c}  {e:.3f}  ← {who}（参考字体之间最高 {m:.3f}）")
    return title if nn[duyan.name] >= mid else None


def main():
    ap = argparse.ArgumentParser(description="渡言和本机现成字体的逐字相似度")
    ap.add_argument("--font", default=os.path.join(ROOT, "sample", "Duyan-Sample.otf"))
    ap.add_argument("--han", action="store_true", help="只比汉字")
    ap.add_argument("--latin", action="store_true", help="只比西文")
    ap.add_argument("--ref", action="append", default=[], help="再加一款参考字体（.ttc 写成 路径:序号）")
    ap.add_argument("--top", type=int, default=12, help="单字最多列几个")
    a = ap.parse_args()
    duyan = Face("渡言", a.font)
    cps = sorted(duyan.cmap)
    too_close = []
    if not a.latin:
        han = [chr(c) for c in cps if 0x4E00 <= c <= 0x9FFF]
        too_close.append(compare("汉字", duyan, load_refs(HAN_REFS, a.ref), han, a.top))
    if not a.han:
        latin = [chr(c) for c in cps if c < 128 and chr(c).isalnum()]
        too_close.append(compare("西文", duyan, load_refs(LATIN_REFS, a.ref), latin, a.top))
    too_close = [t for t in too_close if t]
    if too_close:
        sys.exit(f"{'、'.join(too_close)}和现成字体的最近邻到了参考字体之间的中位数，要逐字查")
    print("\n通过：渡言和最像的现成字体之间，也比一般字体之间更不像")


if __name__ == "__main__":
    main()
