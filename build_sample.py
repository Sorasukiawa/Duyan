#!/usr/bin/env python3
"""把 latin.py、han.py 里画好的字装配成小样字体 sample/Duyan-Sample.ttf。"""
import importlib
import os
import sys

from fontTools.fontBuilder import FontBuilder
from fontTools.pens.ttGlyphPen import TTGlyphPen

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pen  # noqa: E402

UPM = 1000


def glyph_name(ch):
    return {".": "period", "，": "uni_comma_cjk", "。": "uni_period_cjk", " ": "space"}.get(
        ch, ch if ch.isascii() and ch.isalnum() else "uni%04X" % ord(ch))


def collect():
    """返回 [(字符, 轮廓, 步进宽度)]。"""
    out = []
    latin = importlib.import_module("latin")
    for ch, fn in latin.GLYPHS.items():
        cs, extra_l, extra_r = fn()
        x0, _, x1, _ = pen.bounds(cs)
        lsb, rsb = latin.SIDE + extra_l, latin.SIDE + extra_r
        cs = [c.moved(lsb - x0) for c in cs]
        out.append((ch, cs, round(x1 - x0 + lsb + rsb)))
    try:
        han = importlib.import_module("han")
        for ch, fn in han.GLYPHS.items():
            out.append((ch, fn(), 1000))
    except ModuleNotFoundError:
        pass
    return out


def main():
    glyphs = collect()
    order = [".notdef", "space"] + [glyph_name(ch) for ch, _, _ in glyphs]
    fb = FontBuilder(UPM, isTTF=True)
    fb.setupGlyphOrder(order)
    cmap = {32: "space"}
    cmap.update({ord(ch): glyph_name(ch) for ch, _, _ in glyphs})
    fb.setupCharacterMap(cmap)
    ttg, metrics = {}, {}
    empty = TTGlyphPen(None)
    empty.moveTo((60, 0)); empty.lineTo((440, 0)); empty.lineTo((440, 700)); empty.lineTo((60, 700)); empty.closePath()
    ttg[".notdef"] = empty.glyph()
    metrics[".notdef"] = (500, 60)
    ttg["space"] = TTGlyphPen(None).glyph()
    metrics["space"] = (230, 0)
    for ch, cs, adv in glyphs:
        p = TTGlyphPen(None)
        pen.draw(cs, p)
        g = p.glyph()
        g.recalcBounds(None)
        name = glyph_name(ch)
        ttg[name] = g
        metrics[name] = (adv, getattr(g, "xMin", 0))
    fb.setupGlyf(ttg)
    fb.setupHorizontalMetrics(metrics)
    fb.setupHorizontalHeader(ascent=1000, descent=-280)
    fb.setupNameTable({"familyName": "Duyan Sample", "styleName": "Regular", "psName": "DuyanSample-Regular",
                       "version": "Version 0.001", "copyright": "Copyright 2026 The Duyan Project Authors"})
    fb.setupOS2(sTypoAscender=880, sTypoDescender=-120, sTypoLineGap=0, usWinAscent=1000, usWinDescent=280,
                sxHeight=540, sCapHeight=720, achVendID="NONE")
    fb.setupPost()
    # 笔画是互相叠压的轮廓，打上标记让各平台按「叠压」处理
    for name, g in fb.font["glyf"].glyphs.items():
        if g.numberOfContours > 0:
            g.flags[0] |= 0x40
    os.makedirs(os.path.join(HERE, "sample"), exist_ok=True)
    out = os.path.join(HERE, "sample", "Duyan-Sample.ttf")
    fb.save(out)
    print("已生成", os.path.relpath(out, HERE), len(glyphs), "个字")


if __name__ == "__main__":
    main()
