#!/usr/bin/env python3
"""把 glyphs.collect() 里的轮廓装配成小样字体 sample/Duyan-Sample.otf（CFF，直接存三次曲线）。

装配前先跑一遍 tools/check.py（轮廓）和 tools/structure.py（结构，规范见 docs/STRUCTURE.md）：
有问题就列出来；加 --strict 时有问题就不出字体。
出字体后在 macOS 上再用 tools/render_check.py 核对系统渲染。
"""
import argparse
import os
import sys

from fontTools.agl import UV2AGL
from fontTools.fontBuilder import FontBuilder
from fontTools.pens.boundsPen import BoundsPen
from fontTools.pens.t2CharStringPen import T2CharStringPen

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(HERE, "tools"))
import glyphs  # noqa: E402
from check import check  # noqa: E402

UPM = 1000


def glyph_name(ch):
    """标准字形名：西文用 Adobe 字形表里的名字（zero、comma、quoteright……），其余用 uniXXXX。"""
    return UV2AGL.get(ord(ch)) if ord(ch) < 0x2100 and ord(ch) in UV2AGL else "uni%04X" % ord(ch)


def kern_feature(table):
    """把 kern.py 里的字对写成 OpenType 的 kern 特性（只收录两边字形都存在的字对）。"""
    import kern
    names = {ch: glyph_name(ch) for ch in table}
    lines = []
    for (a, b), v in kern.pairs().items():
        if a in names and b in names and v:
            lines.append(f"    pos {names[a]} {names[b]} {v};")
    return "languagesystem DFLT dflt;\nlanguagesystem latn dflt;\n\nfeature kern {\n" + "\n".join(lines) + "\n} kern;\n", len(lines)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--strict", action="store_true")
    a = ap.parse_args()
    table = glyphs.collect()
    problems = 0
    for ch, (shapes, adv) in table.items():
        for kind, x, y, msg in check(shapes):
            problems += 1
            print(f"{ch} {kind} ({x:.0f},{y:.0f}) {msg}")
    import structure
    for ch, r in structure.run().items():
        for msg in structure.problems(ch, r):
            problems += 1
            print(f"{ch} 结构 {msg}")
    if problems and a.strict:
        sys.exit(f"有 {problems} 处问题，没有生成字体")

    order = [".notdef", "space"] + [glyph_name(ch) for ch in table]
    fb = FontBuilder(UPM, isTTF=False)
    fb.setupGlyphOrder(order)
    cmap = {32: "space"}
    cmap.update({ord(ch): glyph_name(ch) for ch in table})
    fb.setupCharacterMap(cmap)
    charstrings, metrics = {}, {}
    pen = T2CharStringPen(500, None)
    pen.moveTo((60, 0)); pen.lineTo((60, 700)); pen.lineTo((440, 700)); pen.lineTo((440, 0)); pen.closePath()
    charstrings[".notdef"] = pen.getCharString()
    metrics[".notdef"] = (500, 60)
    charstrings["space"] = T2CharStringPen(230, None).getCharString()
    metrics["space"] = (230, 0)
    for ch, (shapes, adv) in table.items():
        name = glyph_name(ch)
        pen = T2CharStringPen(adv, None)
        bp = BoundsPen(None)
        for s in shapes:
            s.draw(pen)
            s.draw(bp)
        charstrings[name] = pen.getCharString()
        metrics[name] = (adv, round(bp.bounds[0]) if bp.bounds else 0)
    fb.setupCFF("DuyanSample-Regular", {"FullName": "Duyan Sample Regular"}, charstrings, {})
    fb.setupHorizontalMetrics(metrics)
    fb.setupHorizontalHeader(ascent=1000, descent=-280)
    fb.setupNameTable({"familyName": {"en": "Duyan Sample", "zh": "渡言 小样"}, "styleName": "Regular",
                       "fullName": {"en": "Duyan Sample Regular", "zh": "渡言 小样 Regular"},
                       "psName": "DuyanSample-Regular",
                       "version": "Version 0.010",
                       "copyright": "Copyright 2026 The Duyan Project Authors (https://github.com/Sorasukiawa/Duyan)",
                       "designer": "Sora", "vendorURL": "https://github.com/Sorasukiawa/Duyan",
                       "licenseDescription": "This Font Software is licensed under the SIL Open Font License, Version 1.1. "
                                             "This license is available with a FAQ at: https://openfontlicense.org",
                       "licenseInfoURL": "https://openfontlicense.org"})
    # fsType 0：可安装嵌入。开源字体不限制嵌入（fontTools 默认是 4，「只许预览和打印」，浏览器存 PDF 时会把字转成图形）
    fb.setupOS2(sTypoAscender=880, sTypoDescender=-120, sTypoLineGap=0, usWinAscent=1000, usWinDescent=280,
                sxHeight=540, sCapHeight=720, achVendID="NONE", fsType=0)
    fb.setupPost()
    fea, kerned = kern_feature(table)
    fb.addOpenTypeFeatures(fea)
    out = os.path.join(HERE, "sample", "Duyan-Sample.otf")
    fb.save(out)
    print("已生成", os.path.relpath(out, HERE), len(table), "个字", f"{kerned} 个字距对", f"（检查出 {problems} 处问题）")
    import render_check
    bad = render_check.run(out)
    if bad:
        for ch, flipped in bad:
            print(f"{ch} 第 {', '.join(str(i + 1) for i in flipped)} 条轮廓被系统渲染当成了字怀")
    elif bad is not None:
        print("系统渲染核对通过")


if __name__ == "__main__":
    main()
