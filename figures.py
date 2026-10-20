"""小克体的数字（5 在 latin.py 里）和西文标点。

数字是等高的齐线数字，高 700，圆的地方上下各过冲 14；粗笔 100、细笔 50，收笔的球和小写 a、c 一样。
标点里的点都是同一个圆点（半径 60），逗号、引号是圆点拖一条尖尾巴。
"""
import math

from latin import CAP, HAIR, STEM, TIP, BR, XH, foot, ring
from outline import D, L, R, U, Shape, circle, n

FH, FO_ = 700, 14           # 数字高度、过冲
DOT = 60                    # 句点半径


def _ball_cw(bx, by, r, start):
    """球形收笔的三个节点（顺时针绕球）：start 是先经过的那一侧：'left'、'right'、'top'、'bottom'。"""
    pts = {"left": (bx - r, by, U), "top": (bx, by + r, R), "right": (bx + r, by, D), "bottom": (bx, by - r, L)}
    order = ["left", "top", "right", "bottom"]
    i = order.index(start)
    seq = [order[(i + k) % 4] for k in range(3)]
    return [n(pts[k][0], pts[k][1], pts[k][2], t=0.5523) for k in seq]


def teardrop(tip, center, r, bend=0):
    """圆点拖一条尖尾巴（逗号、引号）。tip 是尾巴尖，center、r 是圆点。bend 让尾巴往一侧弯。"""
    dx, dy = center[0] - tip[0], center[1] - tip[1]
    k = math.hypot(dx, dy)
    d = (dx / k, dy / k)
    nl = (-d[1], d[0])
    a = (center[0] + nl[0] * r, center[1] + nl[1] * r)
    b = (center[0] + d[0] * r, center[1] + d[1] * r)
    c = (center[0] - nl[0] * r, center[1] - nl[1] * r)
    da = math.degrees(math.atan2(d[1], d[0])) % 360
    chord_a = math.degrees(math.atan2(a[1] - tip[1], a[0] - tip[0])) % 360
    chord_c = math.degrees(math.atan2(tip[1] - c[1], tip[0] - c[0])) % 360
    out = (2 * chord_a - da + bend) % 360
    inn = (2 * chord_c - (da + 180) + bend) % 360
    return Shape([n(*tip, din=inn, dout=out, tip=True), n(*a, da, t=0.5523), n(*b, (da - 90) % 360, t=0.5523),
                  n(*c, (da + 180) % 360)], name="点尾")


# ───────── 数字 ─────────

def g_0():
    return ring(0, 476, -FO_, FH + FO_, thick=STEM, thin=HAIR, name="0"), 0, 0


def g_1():
    """1：竖（顶上一面往左下斜的旗）连脚衬线。"""
    x, w = 180, 104
    return [Shape([
        n(x, FH - 150, U), n(x - 120, FH - 120, din=200), n(x - 128, FH - 98),
        n(x + w, FH + 12, t="line"),
    ] + foot(x, w, 0, 92, 92), name="1")], 0, 0


def g_2():
    """2：左上收成球，顶上的弧绕到右边，脊往左下落到底横，底横右端往上一个小喙。"""
    r = 50
    bx, by = 92, 532
    return [Shape([
        n(bx - r, by, U),                          # 球左，顺着外沿上去
        n(244, FH + FO_, R, t=0.58),               # 外沿顶
        n(446, 516, D, t=0.6),                     # 外沿右
        n(250, 196, 226),                          # 脊外沿
        n(150, 56, din=232),                       # 脊碰到底横顶：夹角
        n(396, 56), n(452, 160, tip=True), n(460, 0), n(24, 0), n(24, 40, dout=50),
        n(196, 270, 52),                           # 脊内沿
        n(346, 516, U, t=0.6),                     # 内沿右
        n(240, FH + FO_ - HAIR, L),                # 内沿顶
        n(bx + r, by, D),                          # 球右
        n(bx, by - r, L, t=0.5523),                # 球底
    ], name="2")], 0, 0


def g_3():
    """3：上小下大两个弯，左上、左下都收成球；中间一道横在左端收成尖。"""
    r = 48
    return [Shape([
        n(36, 562, U),                              # 上球左
        n(228, FH + FO_, R, t=0.58),                # 外沿顶
        n(412, 556, D, t=0.6),                      # 上弯外沿右
        n(372, 398, din=226, dout=-16),             # 两个弯相接的腰
        n(454, 196, D, t=0.6),                      # 下弯外沿右
        n(232, -FO_, L),                            # 外沿底
        n(30, 128, U),                              # 下球左
        n(30 + r, 128 + r, R, t=0.5523),            # 下球顶
        n(30 + 2 * r, 128, D),                      # 下球右，往下卷进内沿
        n(238, -FO_ + HAIR, R),                     # 内沿底
        n(354, 196, U, t=0.6),                      # 下弯内沿右
        n(232, 352, L),                             # 下弯内沿顶
        n(132, 378, tip=True),                      # 中间那道横的尖
        n(228, 404, R),                             # 上弯内沿底
        n(318, 556, U, t=0.6),                      # 上弯内沿右
        n(222, FH + FO_ - HAIR, L),                 # 内沿顶
        n(36 + 2 * r, 562, D),                      # 上球右
        n(36 + r, 562 - r, L, t=0.5523),            # 上球底
    ], name="3")], 0, 0


def g_4():
    """4：斜笔、竖、横一条外轮廓，中间是三角形的字怀。竖底带脚，横往右伸出竖外。"""
    xs, w = 300, 104
    yb, yt = 196, 248                               # 横的下沿、上沿
    tw = 66                                         # 斜笔的水平宽度
    k = (xs - 20) / (FH - yt)                       # 斜笔每升高 1 往右 k
    return [Shape([
        n(xs, FH), n(xs + w, FH),
        n(xs + w, yt), n(470, yt), n(470, yb), n(xs + w, yb, t="line"),
    ] + foot(xs, w, 0, 70, 70) + [
        n(xs, yb), n(20, yb), n(20, yt, t="line"),
    ], name="4"), Shape([
        n(xs, yt), n(xs, FH - tw / k), n(20 + tw, yt),
    ], hole=True, name="4 字怀")], 0, 0


def g_6():
    """6：底下一个圈；左边往上的一笔绕到右上，收成挂着的球。"""
    r = 46
    bx, by = 382, 616
    return [Shape([
        n(30, 250, U, t=0.58),                      # 外沿左（圈和上去那一笔共用）
        n(290, FH + FO_, R),                        # 外沿顶
        n(bx + r, by, D, t=0.6),                    # 球右
        n(bx, by - r, L, t=0.5523),                 # 球底
        n(bx - r, by, U),                           # 球左，往上卷进内沿
        n(290, FH + FO_ - HAIR, L),                 # 内沿顶
        n(132, 420, D),                             # 上去那一笔的内沿
        n(140, 360, din=280, dout=24),              # 和圈的外沿顶相接
        n(282, 446, R, t=0.6),                      # 圈外沿顶
        n(470, 216, D, t=0.6),                      # 圈外沿右
        n(250, -FO_, L, t=0.6),                     # 外沿底
    ], name="6"), Shape([
        n(260, 396, R, t=0.58), n(370, 216, D, t=0.58), n(250, -FO_ + HAIR, L, t=0.58), n(130, 216, U, t=0.58),
    ], hole=True, name="6 字怀")], 0, 0


def g_9():
    """9：6 绕中心转 180°。"""
    shapes, _, _ = g_6()
    cx, cy = 250, FH / 2
    out = []
    for s in shapes:
        out.append(Shape([n(2 * cx - q.x, 2 * cy - q.y, din=None if q.din is None else (q.din + 180) % 360,
                            dout=None if q.dout is None else (q.dout + 180) % 360, hid=q.hid, tip=q.tip, t=q.t)
                          for q in s.nodes], s.tension, s.hole, "9"))
    return out, 0, 0


def g_7():
    """7：顶横（左端往下一个小喙）和往左下落的粗笔一条轮廓。"""
    return [Shape([
        n(30, FH), n(456, FH, dout=254),            # 顶横右端直接转进粗笔的右边沿
        n(256, 0, din=258),                         # 粗笔底右
        n(146, 0, dout=74),                         # 粗笔底左
        n(356, FH - HAIR, din=62),                  # 粗笔左边沿碰到顶横底
        n(82, FH - HAIR), n(28, FH - 132, tip=True),
    ], name="7")], 0, 0


def g_8():
    """8：上小下大两个圈叠起来，腰在中间收紧。"""
    return [Shape([
        n(240, FH + FO_, R, t=0.58),
        n(420, 552, D, t=0.6),
        n(372, 384, din=224, dout=-24),             # 右腰
        n(456, 196, D, t=0.6),
        n(240, -FO_, L, t=0.58),
        n(24, 196, U, t=0.6),
        n(108, 384, din=24, dout=136),              # 左腰
        n(60, 552, U, t=0.6),
    ], name="8"), Shape([
        n(240, FH + FO_ - HAIR, R, t=0.58), n(330, 556, D, t=0.6), n(240, 412, L, t=0.6), n(150, 556, U, t=0.6),
    ], hole=True, name="8 上字怀"), Shape([
        n(240, 356, R, t=0.58), n(356, 196, D, t=0.6), n(240, -FO_ + HAIR, L, t=0.58), n(124, 196, U, t=0.6),
    ], hole=True, name="8 下字怀")], 0, 0


# ───────── 标点 ─────────

def g_comma():
    return [teardrop((34, -150), (78, 56), DOT)], 6, 0


def g_colon():
    return [circle(70, 62, DOT, name="冒号下"), circle(70, XH - 70, DOT, name="冒号上")], 8, 8


def g_semicolon():
    return [circle(78, XH - 70, DOT, name="分号上"), teardrop((34, -150), (78, 56), DOT)], 8, 8


def g_exclam():
    """感叹号：上粗下细的一竖（顶是圆的）加一个圆点。"""
    return [Shape([
        n(30, 640, U, t=0.5523), n(80, CAP, R, t=0.5523), n(130, 640, D),
        n(92, 240, din=264), n(68, 240, dout=96),
    ], name="叹号竖"), circle(80, 62, DOT, name="叹号点")], 10, 10


def g_question():
    """问号：左上收成球的弯钩，绕到右边落下来变成一小段竖，下面一个圆点。"""
    r = 50
    bx, by = 82, 560
    return [Shape([
        n(bx - r, by, U),                          # 球左
        n(220, CAP + FO_, R, t=0.58),               # 外沿顶
        n(400, 548, D, t=0.6),                      # 外沿右
        n(270, 368, 238),                           # 往下落
        n(254, 240, din=262), n(210, 240, dout=90),
        n(214, 330, 70),
        n(304, 548, U, t=0.6),                      # 内沿右
        n(220, CAP + FO_ - HAIR, L),                # 内沿顶
        n(bx + r, by, D),                           # 球右
        n(bx, by - r, L, t=0.5523),                 # 球底
    ], name="问号钩"), circle(232, 62, DOT, name="问号点")], 0, 0


def _bar(x0, x1, y0, y1, name):
    return Shape([n(x0, y0), n(x1, y0), n(x1, y1), n(x0, y1)], name=name)


def g_hyphen():
    return [_bar(0, 260, 232, 292, "连字符")], 10, 10


def g_endash():
    return [_bar(0, 500, 238, 288, "短横")], 0, 0


def g_emdash():
    return [_bar(0, 1000, 238, 288, "长横")], -34, -34


def g_rsquo():
    return [teardrop((40, 470), (82, 666), DOT * .86)], 4, 4


def g_lsquo():
    return [teardrop((122, 772), (80, 576), DOT * .86)], 4, 4


def g_rdquo():
    return [teardrop((40, 470), (82, 666), DOT * .86), teardrop((210, 470), (252, 666), DOT * .86)], 4, 4


def g_ldquo():
    return [teardrop((122, 772), (80, 576), DOT * .86), teardrop((292, 772), (250, 576), DOT * .86)], 4, 4


def g_quotesingle():
    return [Shape([n(30, CAP), n(118, CAP), n(92, 470), n(56, 470)], name="直引号")], 12, 12


def g_quotedbl():
    return [Shape([n(30, CAP), n(118, CAP), n(92, 470), n(56, 470)], name="直引号左"),
            Shape([n(190, CAP), n(278, CAP), n(252, 470), n(216, 470)], name="直引号右")], 12, 12


def g_parenleft():
    """左括号：外沿往左鼓，中间粗、两头细，两头是小斜切。"""
    return [Shape([
        n(296, 788, din=56), n(322, 770, dout=236), n(178, 290, D, t=0.62),
        n(322, -190, din=304), n(296, -208, dout=124), n(86, 290, U, t=0.62),
    ], name="左括号")], 0, 0


def g_parenright():
    shapes, _, _ = g_parenleft()
    s = shapes[0]
    return [Shape([n(400 - q.x, q.y, din=None if q.din is None else (180 - q.din) % 360,
                     dout=None if q.dout is None else (180 - q.dout) % 360, t=q.t) for q in s.nodes], name="右括号")], 0, 0


def g_slash():
    return [Shape([n(0, -150), n(74, -150), n(400, 770), n(326, 770)], name="斜杠")], 0, 0


GLYPHS = {
    "0": g_0, "1": g_1, "2": g_2, "3": g_3, "4": g_4, "6": g_6, "7": g_7, "8": g_8, "9": g_9,
    ",": g_comma, ":": g_colon, ";": g_semicolon, "!": g_exclam, "?": g_question,
    "-": g_hyphen, "–": g_endash, "—": g_emdash,
    "’": g_rsquo, "‘": g_lsquo, "”": g_rdquo, "“": g_ldquo, "'": g_quotesingle, '"': g_quotedbl,
    "(": g_parenleft, ")": g_parenright, "/": g_slash,
}
