"""把西文、汉字的轮廓收集起来，摆好位置：西文按左右边距排，汉字步进 1000。"""
import importlib

from outline import bounds

CAP_SIDE = 50               # 大写字母的默认左右边距（小写、数字、标点用 latin.SIDE）


def collect():
    """返回 {字符: (轮廓列表, 步进宽度)}。"""
    out = {}
    latin = importlib.import_module("latin")
    table = dict(latin.GLYPHS)
    for mod in ("caps", "figures"):
        try:
            table.update(importlib.import_module(mod).GLYPHS)
        except ModuleNotFoundError:
            pass
    for ch, fn in table.items():
        shapes, extra_l, extra_r = fn()
        x0, _, x1, _ = bounds(shapes)
        side = CAP_SIDE if ch.isupper() else latin.SIDE
        lsb, rsb = side + extra_l, side + extra_r
        out[ch] = ([s.moved(lsb - x0) for s in shapes], round(x1 - x0 + lsb + rsb))
    try:
        han = importlib.import_module("han")
    except ModuleNotFoundError:
        return out
    table = dict(han.GLYPHS)
    for mod in ("chars", "chars2"):          # 第一批、第二批常用字
        try:
            table.update(importlib.import_module(mod).GLYPHS)
        except ModuleNotFoundError:
            pass
    for ch, fn in table.items():
        out[ch] = (fn(), 1000)
    return out
