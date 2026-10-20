#!/usr/bin/env python3
"""用 macOS 的系统渲染核对字体：有没有轮廓被它当成字怀反过来画。

CoreText 会按嵌套关系「纠正」轮廓方向：一条轮廓整个落在另一条里面，就被当成字怀。
「月」框里的短横两头都藏进同一条外框时就是这样，重叠处被画成镂空，FreeType 却画得好好的，
所以光看自己的预览图发现不了。这里把 CoreText 读出来的每条轮廓方向和字体文件里的比一比。
只在 macOS 上能跑（要用 swiftc 编译一个小工具）。

python3 tools/render_check.py [字体文件]
"""
import os
import subprocess
import sys

from fontTools.pens.areaPen import AreaPen
from fontTools.pens.recordingPen import RecordingPen
from fontTools.ttLib import TTFont

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "ct_contours.swift")
BIN = os.path.join(HERE, ".build", "ct_contours")


def _areas(glyphset, name):
    rec = RecordingPen()
    glyphset[name].draw(rec)
    out, pen = [], AreaPen()
    for op, args in rec.value:
        getattr(pen, op)(*args)
        if op in ("closePath", "endPath"):
            out.append(pen.value)
            pen = AreaPen()
    return out


def run(font):
    """返回 [(字, 被反过来的轮廓序号)]。不是 macOS 时返回 None。"""
    if sys.platform != "darwin":
        return None
    if not os.path.exists(BIN) or os.path.getmtime(BIN) < os.path.getmtime(SRC):
        os.makedirs(os.path.dirname(BIN), exist_ok=True)
        subprocess.run(["swiftc", "-O", "-o", BIN, SRC], check=True)
    f = TTFont(font)
    cmap = {chr(c): g for c, g in f.getBestCmap().items() if c > 32}
    gs = f.getGlyphSet()
    out = subprocess.run([BIN, font, "".join(cmap)], check=True, capture_output=True, text=True).stdout
    bad = []
    for line in out.splitlines():
        ch, _, rest = line.partition("\t")
        ct = [float(v) for v in rest.split()]
        ft = _areas(gs, cmap[ch])
        same = [(a > 0) == (b > 0) for a, b in zip(ct, ft)]
        if len(set(same)) > 1 or len(ct) != len(ft):
            flipped = [i for i, ok in enumerate(same) if ok != same[0]]   # 以第一条轮廓为准
            bad.append((ch, flipped))
    return bad


if __name__ == "__main__":
    font = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, "..", "sample", "Xiaoke-Sample.otf")
    bad = run(font)
    if bad is None:
        print("不是 macOS，跳过")
    elif bad:
        for ch, flipped in bad:
            print(f"{ch} 第 {', '.join(str(i + 1) for i in flipped)} 条轮廓被系统渲染当成了字怀，重叠处会变成镂空")
        sys.exit(1)
    else:
        print("系统渲染核对通过")
