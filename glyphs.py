"""把西文、汉字的轮廓收集起来，摆好位置：西文按左右边距排，汉字步进 1000、从设计坐标压到字身里。"""
import importlib

import layout
from outline import bounds

CAP_SIDE = 50               # 大写字母的默认左右边距（小写、数字、标点用 latin.SIDE）
WEIGHT = {}                 # 每个汉字画的时候用过的减细档位（collect() 填，结构检查核对）


def _optional(mod):
    """按名字导入一组字；这个文件还没建时返回 None。文件里面的导入出错照常报出来，不能让一整批字悄悄消失。"""
    try:
        return importlib.import_module(mod)
    except ModuleNotFoundError as e:
        if e.name != mod:
            raise
        return None


def collect():
    """返回 {字符: (轮廓列表, 步进宽度)}。"""
    out = {}
    latin = importlib.import_module("latin")
    table = dict(latin.GLYPHS)
    for mod in ("caps", "figures"):
        m = _optional(mod)
        if m:
            table.update(m.GLYPHS)
    for ch, fn in table.items():
        shapes, extra_l, extra_r = fn()
        x0, _, x1, _ = bounds(shapes)
        side = CAP_SIDE if ch.isupper() else latin.SIDE
        lsb, rsb = side + extra_l, side + extra_r
        out[ch] = ([s.moved(lsb - x0) for s in shapes], round(x1 - x0 + lsb + rsb))
    han = _optional("han")
    if han is None:
        return out
    table = dict(han.GLYPHS)
    for mod in ("chars", "chars2", "chars3", "chars4", "chars5", "chars6"):          # 第一批到第六批常用字
        m = _optional(mod)
        if m:
            table.update(m.GLYPHS)
    # 汉字在设计坐标里画，这里整字纵向压扁、中心对到字身中心（见 layout.HAN_SY）
    sy, by = layout.HAN_SY, layout.EM_CY - layout.HAN_CY * layout.HAN_SY
    for ch, fn in table.items():
        with han.drawing(sy) as used:
            shapes = fn()
        WEIGHT[ch] = sorted(set(used)) or [1.0]
        out[ch] = ([s.mapped(ay=sy, by=by) for s in shapes], 1000)
    return out
