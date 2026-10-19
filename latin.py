"""渡言的西文：轮廓优先。每个字母画成一条外轮廓（加字怀），笔画之间不叠补丁。

比例参考 Anthropic Serif（只量数字，不碰轮廓）：x 高度 540、大写 720，主干 100、细线 50，
衬线短而利落（楔形、末端 12、托角 42）。
所有外轮廓都按顺时针写（墨在走向的右边）：顶边向右、右边向下、底边向左、左边向上。
竖和拱、竖和碗相接的地方直接放一个角点，角点的位置和走向就是设计本身。
"""
import math

from outline import D, L, R, U, Shape, circle, n

XH, OS = 540, 12            # x 高度、圆形字母的过冲
CAP, OSC = 720, 14
ASC, DESC = 760, -220
STEM, HAIR = 100, 50
CSTEM, CHAIR = 108, 52
SO, TIP, BR = 54, 12, 42    # 衬线：伸出长度、末端厚度、托角高度
FO, FD, FT, FB = 58, 38, 12, 58   # 小写竖顶的楔形入笔：伸出、下斜、末端厚度、托角
SIDE = 34                   # 默认左右边距


# ───────── 零件（都按顺时针给节点）─────────

def flag(x, top, w=STEM):
    """小写竖顶的楔形入笔：从竖的左边沿往上进来，从右边沿往下出去。"""
    return [n(x, top - FD - FT - FB, U), n(x - FO, top - FD - FT, din=L), n(x - FO, top - FD), n(x + w, top, t="line")]


def head(x, top, w=CSTEM, ol=SO + 4, orr=SO + 4):
    """大写竖顶的衬线。"""
    N = [n(x, top - TIP - BR, U), n(x - ol, top - TIP, din=L), n(x - ol, top)] if ol else [n(x, top)]
    N += [n(x + w + orr, top), n(x + w + orr, top - TIP, dout=L), n(x + w, top - TIP - BR, D, t="line")] if orr \
        else [n(x + w, top, t="line")]
    return N


def foot(x, w=STEM, y=0, ol=SO, orr=SO):
    """竖底的衬线：从右边沿往下进来，从左边沿往上出去。"""
    N = [n(x + w, y + TIP + BR, D), n(x + w + orr, y + TIP, din=R), n(x + w + orr, y)] if orr else [n(x + w, y)]
    N += [n(x - ol, y), n(x - ol, y + TIP, dout=R), n(x, y + TIP + BR, U, t="line")] if ol else [n(x, y, t="line")]
    return N


def shoulder(x0, top=XH):
    """拱（或 r 的臂）从竖的右边沿分出的那个点：沿竖往下走到这里，转向右上。"""
    return n(x0, top - 64, dout=52)


def crotch(x0, top=XH, y=None):
    """拱的内沿落回竖右边沿的夹角：从左上方下来，转成沿竖往下。"""
    return n(x0, top - 168 if y is None else y, din=244, t="line")


def arch_outer(x0, xr, top=XH, w=STEM):
    """拱的外沿：肩 → 外拱顶 → 右竖右边沿（往下）。x0 左竖右缘，xr 右竖左缘。"""
    return [shoulder(x0, top), n((x0 + xr + w) / 2, top + OS, R, t=0.6), n(xr + w, top - 150, D, t="line")]


def arch_inner(x0, xr, top=XH):
    """拱的内沿：右竖左边沿（往上）→ 内拱顶 → 夹角。"""
    return [n(xr, top - 160, U), n((x0 + xr) / 2 + 24, top + OS - HAIR - 2, L), crotch(x0, top)]


def ring(xl, xr, yb, yt, thick=STEM, thin=HAIR, tension=0.58, name="o"):
    """o 那样的圈：外轮廓和字怀。"""
    cx, cy = (xl + xr) / 2, (yb + yt) / 2
    return [Shape([n(cx, yt, R), n(xr, cy, D), n(cx, yb, L), n(xl, cy, U)], tension, name=name),
            Shape([n(cx, yt - thin, R), n(xr - thick, cy, D), n(cx, yb + thin, L), n(xl + thick, cy, U)],
                  tension - 0.02, hole=True, name=name + " 字怀")]


def counter(xs, side, yb, yt, x_far, thin=HAIR, thick=STEM, ct=None, cb=None, ang=55, tension=0.58, name="字怀"):
    """连在竖上的碗的字怀（d、p、a）。xs 是竖靠碗那一侧的边，side=-1 碗在左、+1 碗在右；
    x_far 是碗外沿最远处。字怀从竖边上的上下两个夹角出来，绕一圈回去；ang 是夹角处内沿和水平线的夹角。"""
    ct = yt - thin - 64 if ct is None else ct
    cb = yb + thin + 64 if cb is None else cb
    x_in = x_far - thick * side                   # 字怀离竖最远的那一边
    cx = (xs + x_in) / 2 + 8 * side               # 字怀的顶和底稍微偏向竖那一侧
    cy = (yb + yt) / 2
    if side < 0:
        nodes = [n(xs, ct, dout=180 - ang), n(cx, yt - thin, L), n(x_in, cy, D), n(cx, yb + thin, R),
                 n(xs, cb, din=ang, t="line")]
    else:
        nodes = [n(xs, cb, dout=360 - ang), n(cx, yb + thin, R), n(x_in, cy, U), n(cx, yt - thin, L),
                 n(xs, ct, din=180 + ang, t="line")]
    return Shape(nodes, tension - 0.02, hole=True, name=name)


# ───────── 小写 ─────────

def g_l():
    x = SO
    return [Shape(flag(x, ASC) + foot(x), name="l")], 0, 0


def g_i():
    x = SO
    return [Shape(flag(x, XH) + foot(x), name="i"), circle(x + STEM / 2 + 4, XH + 168, 56, name="i 点")], 0, 0


def _n_like(top_left):
    x, c = SO, 236
    x0, xr = x + STEM, x + STEM + c
    return [Shape(flag(x, top_left) + arch_outer(x0, xr) + foot(xr, ol=SO - 8) + arch_inner(x0, xr)
                  + foot(x, orr=SO - 8), name="n")]


def g_n():
    return _n_like(XH), 0, 0


def g_h():
    return _n_like(ASC), 0, 0


def g_m():
    x, c = SO, 214
    x0 = x + STEM
    r1 = x0 + c
    r2 = r1 + STEM + c
    a1 = arch_outer(x0, r1)
    a2 = arch_outer(r1 + STEM, r2)
    # 第二个拱从第一个拱的右肩上分出来：第一个拱的外沿落到那里就转向
    split = n(r1 + STEM - 4, XH - 64, din=282, dout=52)
    return [Shape(flag(x, XH) + a1[:-1] + [split] + a2[1:] + foot(r2, ol=SO - 10) + arch_inner(r1 + STEM, r2)
                  + foot(r1, ol=SO - 10, orr=SO - 10) + arch_inner(x0, r1) + foot(x, orr=SO - 10), name="m")], 0, 0


def g_u():
    """u：n 的拱倒过来。左竖从入笔往下转进碗底，碗的内沿在右竖左边沿形成夹角。"""
    x, c = SO, 236
    x1, xr = x + STEM, x + STEM + c
    return [Shape(flag(x, XH) + [
        n(x1, 160, D),                            # 左竖右边沿往下，转进碗的内沿
        n((x1 + xr) / 2 - 24, -OS + HAIR + 2, R),
        n(xr, 168, din=64, t="line"),             # 内沿上到右竖左边沿：夹角
    ] + flag(xr, XH) + foot(xr, ol=0) + [
        n(xr, 64, dout=232),                      # 右竖左边沿往上到这里，转进碗的外沿
        n((x + xr + STEM) / 2, -OS, L, t=0.6),
        n(x, 150, U, t="line"),
    ], name="u")], 0, 0


def g_o():
    W = 494
    return ring(0, W, -OS, XH + OS), 4, 4


def g_c():
    """c：一条轮廓。上端的内沿卷下来收成球，球的外侧顺着外沿；下端斜切。"""
    W = 460
    r = 52
    bx, by = W - 84, XH - 126
    return [Shape([
        n(0, XH / 2, U, t=0.58),                  # 外沿左
        n(236, XH + OS, R),                       # 外沿顶
        n(bx + r, by, D, t=0.6),                  # 球右（外沿落下来）
        n(bx, by - r, L, t=0.5523),               # 球底
        n(bx - r, by, U),                         # 球左，往上卷进内沿
        n(238, XH + OS - HAIR, L),                # 内沿顶
        n(STEM, XH / 2, D, t=0.56),               # 内沿左
        n(246, -OS + HAIR, R),                    # 内沿底
        n(W - 44, 136, din=48),                   # 下端内角
        n(W - 18, 66, dout=230),                  # 下端外角
        n(240, -OS, L, t=0.58),                   # 外沿底
    ], name="c")], 4, 0


def g_e():
    """e：外轮廓连横杠一条，上面的字怀一条。下端斜切。"""
    W = 476
    cx = 238
    bar = 300                                     # 横杠中线
    return [Shape([
        n(0, XH / 2, U, t=0.58),                  # 外沿左
        n(cx, XH + OS, R),                        # 外沿顶
        n(W, bar + 24, D, t=0.6, ),               # 外沿右，落到横杠下沿
        n(W, bar - HAIR / 2),                     # 外沿右下角
        n(STEM, bar - HAIR / 2, dout=270),        # 横杠下沿左端：转进下面的内沿
        n(cx + 10, -OS + HAIR, R, t=0.6),         # 内沿底
        n(W - 42, 144, din=46),                   # 下端内角
        n(W - 14, 76, dout=228),                  # 下端外角
        n(cx + 4, -OS, L, t=0.58),                # 外沿底
    ], name="e"), Shape([
        n(STEM, bar + HAIR / 2, dout=90),         # 字怀左下
        n(cx + 2, XH + OS - HAIR, R, t=0.6),
        n(W - STEM + 4, bar + 40, D),
        n(W - STEM + 4, bar + HAIR / 2, t="line"),
    ], hole=True, name="e 字怀")], 4, 0


def g_a():
    """a：一条外轮廓（弯头 → 右竖 → 脚 → 碗）加碗的字怀。弯头左端收成球。"""
    sx = 330                                      # 右竖左缘
    r = 52
    bx, by = 84, XH - 132
    cb = 196                                      # 碗外沿最左
    return [Shape([
        n(bx - r, by, U),                         # 球左，顺着外沿上去
        n(228, XH + OS, R, t=0.58),               # 弯头外沿顶
        n(sx + STEM, XH - 150, D, t="line"),      # 右竖右边沿
    ] + foot(sx, ol=0, orr=SO - 10) + [
        n(sx, 44, dout=214),                      # 碗底接竖：转进碗的外沿
        n(cb + 14, -OS, L, t=0.6),                # 碗外沿底
        n(52, 146, U, t=0.6),                     # 碗外沿左
        n(cb + 20, 304, R),                       # 碗外沿顶
        n(sx, 290, din=338, t="line"),            # 碗顶接竖
        n(sx, XH - 160, U),                       # 右竖左边沿往上，转进弯头内沿
        n(238, XH + OS - HAIR, L),                # 弯头内沿顶
        n(bx + r, by, D),                         # 球右
        n(bx, by - r, L, t=0.5523),               # 球底
    ], name="a"), counter(sx, -1, -OS, 304, 52, thick=STEM * .98, ct=226, cb=96, ang=32, name="a 字怀")], 0, 0


def g_d():
    sx = 360
    return [Shape(flag(sx, ASC) + foot(sx, ol=0) + [
        n(sx, 34, dout=220),                      # 碗底接竖
        n(250, -OS, L, t=0.6),
        n(40, XH / 2, U, t=0.58),
        n(250, XH + OS, R, t=0.6),
        n(sx, 506, din=318, t="line"),            # 碗顶接竖
    ], name="d"), counter(sx, -1, -OS, XH + OS, 40, ct=432, cb=106, name="d 字怀")], 0, 0


def g_p():
    x = SO
    x0 = x + STEM
    xr = x0 + 320
    return [Shape(flag(x, XH) + [
        n(x0, 506, dout=42),                      # 碗顶接竖
        n(x0 + 156, XH + OS, R, t=0.6),
        n(xr, XH / 2, D, t=0.58),
        n(x0 + 156, -OS, L, t=0.6),
        n(x0, 34, din=140, t="line"),             # 碗底接竖
    ] + foot(x, y=DESC), name="p"), counter(x0, 1, -OS, XH + OS, xr, ct=432, cb=106, name="p 字怀")], 0, 0


def g_r():
    """r：竖、带球的臂一条轮廓。臂从竖顶斜着分出，越往右越细，末端的球挂在臂下。"""
    x = SO
    x0 = x + STEM
    rb = 50
    bx, by = x0 + 150, XH - 74
    return [Shape(flag(x, XH) + [
        shoulder(x0),
        n(x0 + 110, XH + OS, R),                  # 臂外沿顶
        n(bx + rb, by, D, t=0.6),                 # 球右
        n(bx, by - rb, L, t=0.5523),              # 球底
        n(bx - rb, by, U),                        # 球左，往上卷进臂的内沿
        n(x0 + 56, XH + OS - HAIR + 2, L),        # 臂内沿最高处
        n(x0, XH - 96, D, t="line"),              # 臂的下沿顺着竖的右边沿长出来，不留夹角
    ] + foot(x, orr=SO + 22), name="r")], 0, 0


def g_s():
    """s：一条轮廓，上下两半绕中心转 180° 基本对称，下半略大。两端是斜切口，不加衬线。
    脊的上下两沿各一个节点，放在拐点上，走向 330°（往右下 30°），两沿相距约 104。"""
    W = 404
    cx, cy = W / 2, XH / 2
    upper = [
        n(32, 395, U, t=0.6),                     # 上碗外沿左
        n(200, XH + OS, R),                       # 外沿顶
        n(382, 490, din=305),                     # 上端外角
        n(346, 422, dout=125),                    # 上端内角
        n(204, XH + OS - HAIR, L, t=0.6),         # 内沿顶
        n(130, 425, D),                           # 上碗内沿左
        n(226, 318, 330, t=0.6),                  # 脊上沿
    ]
    # 下半：上半绕中心转 180°，再往外放一点
    rot = lambda q, grow: n(2 * cx - q.x + grow[0], 2 * cy - q.y + grow[1],
                            din=None if q.din is None else (q.din + 180) % 360,
                            dout=None if q.dout is None else (q.dout + 180) % 360, t=q.t)
    grow = [(6, 0), (2, 0), (-4, 0), (-2, 2), (2, 0), (6, 0), (0, 0)]
    lower = [rot(q, g) for q, g in zip(upper, grow)]
    return [Shape(upper + lower, name="s")], 0, 0


def g_t():
    """t：一条轮廓。顶端斜切成尖，横杠从竖里伸出来，底部弯钩斜切收尾。"""
    x = 60
    bl, br_ = x - 62, x + STEM + 128             # 横杠左右端
    return [Shape([
        n(x, XH + 30),                            # 斜切顶左端
        n(x + STEM, XH + 122, tip=True),          # 斜切顶的尖
        n(x + STEM, XH), n(br_, XH), n(br_, XH - HAIR), n(x + STEM, XH - HAIR, t="line"),
        n(x + STEM, 150, D),
        n(x + 136, -OS + HAIR + 2, R),            # 内沿底
        n(x + 190, 96, din=60),                   # 尾端内角
        n(x + 222, 72, dout=232),                 # 尾端外角
        n(x + 118, -OS, L, t=0.58),               # 外沿底
        n(x, 150, U, t="line"),
        n(x, XH - HAIR), n(bl, XH - HAIR), n(bl, XH), n(x, XH, t="line"),
    ], name="t")], 0, 0


# ───────── 斜笔 ─────────

def _x_at(e, y):
    (x0, y0), (x1, y1) = e
    return x0 + (y - y0) * (x1 - x0) / (y1 - y0)


def _ang(e, up):
    """沿边 e 往上（up=True）或往下走的方向角。"""
    (x0, y0), (x1, y1) = e
    a = math.degrees(math.atan2(y1 - y0, x1 - x0))
    return a % 360 if (y1 > y0) == up else (a + 180) % 360


def _isect(e1, e2):
    (x1, y1), (x2, y2) = e1
    (x3, y3), (x4, y4) = e2
    d = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    a = x1 * y2 - y1 * x2
    b = x3 * y4 - y3 * x4
    return ((a * (x3 - x4) - (x1 - x2) * b) / d, (a * (y3 - y4) - (y1 - y2) * b) / d)


def _shift(e, d):
    """把边 e 往它的左手方向平移 d（d 为负往右手）。"""
    (x0, y0), (x1, y1) = e
    dx, dy = x1 - x0, y1 - y0
    k = math.hypot(dx, dy)
    ox, oy = -dy / k * d, dx / k * d
    return ((x0 + ox, y0 + oy), (x1 + ox, y1 + oy))


def _edges(p0, p1, w):
    """直笔画的左右两条边（按 p0 那一头的 x 从左到右）。"""
    a, b = _shift((p0, p1), w / 2), _shift((p0, p1), -w / 2)
    return (a, b) if _x_at(a, p0[1]) < _x_at(b, p0[1]) else (b, a)


def top_serif(le, re, y, ol, orr):
    """斜笔顶上的衬线（顺时针：沿左边往上 → 衬线 → 沿右边往下）。托角顺着斜边收进笔画。"""
    yb, yk = y - TIP, y - TIP - BR
    xl, xr = _x_at(le, y), _x_at(re, y)
    return [n(_x_at(le, yk), yk, _ang(le, True)), n(xl - ol, yb, din=L), n(xl - ol, y), n(xr + orr, y),
            n(xr + orr, yb, dout=L), n(_x_at(re, yk), yk, _ang(re, False), t="line")]


def foot_serif(le, re, y, ol, orr, brl=BR, brr=BR):
    """斜笔底下的衬线（顺时针：沿右边往下 → 衬线 → 沿左边往上）。
    斜边和衬线夹成锐角的那一侧（字里面那一侧），托角要矮一些，不然看起来像个小钩。"""
    yb = y + TIP
    xl, xr = _x_at(le, y), _x_at(re, y)
    return [n(_x_at(re, yb + brr), yb + brr, _ang(re, False)), n(xr + orr, yb, din=R), n(xr + orr, y), n(xl - ol, y),
            n(xl - ol, yb, dout=R), n(_x_at(le, yb + brl), yb + brl, _ang(le, True), t="line")]


def g_v():
    W = 548
    xl, xr = 70 - STEM * .56, W - 70 + HAIR * .65
    thick, thin = STEM * 1.12, HAIR * 1.3
    vx = (xl + xr) / 2 + 22
    V = (vx, -8)
    kl, kr = ((xl, XH), V), ((xl + thick, XH), (vx + thick, -8))
    nl, nr = ((xr - thin, XH), (vx - thin, -8)), ((xr, XH), V)
    return [Shape(top_serif(kl, kr, XH, 20, 22) + [n(*_isect(kr, nl))] + top_serif(nl, nr, XH, 22, 18)
                  + [n(*V, tip=True)], name="v")], 0, 0


def g_w():
    W = 790
    m = W / 2
    thick, thin = STEM * 1.08, HAIR * 1.3
    xl1, xr1, v1 = 66 - STEM * .54, m + 10, 226
    xl2, xr2, v2 = m - 30, W - 66 + HAIR * .65, W - 196
    k1l, k1r = ((xl1, XH), (v1, -8)), ((xl1 + thick, XH), (v1 + thick, -8))
    n1l, n1r = ((xr1 - thin, XH), (v1 - thin, -8)), ((xr1, XH), (v1, -8))
    k2l, k2r = ((xl2, XH), (v2, -8)), ((xl2 + thick, XH), (v2 + thick, -8))
    n2l, n2r = ((xr2 - thin, XH), (v2 - thin, -8)), ((xr2, XH), (v2, -8))
    return [Shape(top_serif(k1l, k1r, XH, 18, 20) + [n(*_isect(k1r, n1l)), n(_x_at(n1l, XH), XH),
                                                     n(_x_at(k2r, XH), XH), n(*_isect(k2r, n2l))]
                  + top_serif(n2l, n2r, XH, 20, 16) + [n(v2, -8, tip=True), n(*_isect(k2l, n1r)), n(v1, -8, tip=True)],
                  name="w")], 0, 0


def g_y():
    """y：粗笔、细笔、尾巴一条轮廓。粗笔左边并进尾巴左边，尾端收成球。"""
    W = 540
    mid = W / 2
    al, ar = _edges((70, XH), (mid + 14, 10), STEM * .98)
    tl, tr = _edges((W - 70, XH), (mid - 26, -60), HAIR * 1.12)
    rb = 48
    bx, by = mid - 192, DESC + 50
    ts = top_serif(tl, tr, XH, 26, 20)
    return [Shape(top_serif(al, ar, XH, 22, 26) + [n(*_isect(ar, tl))] + ts + [
        n(_x_at(tr, -30), -30, _ang(tr, False)),  # 尾巴右边沿开始往左弯
        n(bx + 4, by - rb, L, t=0.6),             # 球底（顺着尾巴外沿）
        n(bx - rb, by, U, t=0.5523),              # 球左
        n(bx, by + rb, R),                        # 球顶，往右卷进尾巴上沿
        n(_x_at(tl, -6), -6, _ang(tl, True), t="line"),
        n(*_isect(al, tl)),                       # 粗笔左边并进尾巴左边
    ], name="y")], 0, 0


# ───────── 大写、数字、标点 ─────────

def g_I():
    x = SO + 4
    return [Shape(head(x, CAP) + foot(x, w=CSTEM, ol=SO + 4, orr=SO + 4), name="I")], 0, 0


def g_A():
    """A：两条腿、顶、横杠一条外轮廓，横杠上面的三角形是字怀。脚衬线顺着斜边。"""
    W = 700
    Y = CAP + 12
    apex = (W / 2 + 6, CAP + 56)                  # 两条外沿延长后的交点，在顶上方
    nl_o, kr_o = (apex, (54, 0)), (apex, (W - 52, 0))
    tw, kw = CHAIR * 1.15, CSTEM * 1.04
    nl_i = _shift(nl_o, tw) if _x_at(_shift(nl_o, tw), 0) > 54 else _shift(nl_o, -tw)
    kr_i = _shift(kr_o, kw) if _x_at(_shift(kr_o, kw), 0) < W - 52 else _shift(kr_o, -kw)
    b0, b1 = 210, 210 + CHAIR                     # 横杠上下沿
    hy = lambda e, y: n(_x_at(e, y), y)
    body = Shape([hy(nl_o, Y), hy(kr_o, Y)] + foot_serif(kr_i, kr_o, 0, 22, 40, brl=22)
                 + [hy(kr_i, b0), hy(nl_i, b0)] + foot_serif(nl_o, nl_i, 0, 34, 30, brr=22), name="A")
    tri = Shape([hy(nl_i, b1), n(*_isect(nl_i, kr_i), tip=True), hy(kr_i, b1)], hole=True, name="A 字怀")
    return [body, tri], 0, 0


def g_O():
    W = 726
    return ring(0, W, -OSC, CAP + OSC, thick=CSTEM, thin=CHAIR, name="O"), 4, 4


def g_C():
    """C：一条轮廓，两端是近乎竖直的切口。"""
    W = 668
    cx = 352
    return [Shape([
        n(0, CAP / 2, U, t=0.58),
        n(cx, CAP + OSC, R),
        n(W - 14, CAP - 120, din=-54),            # 上端外角
        n(W - 34, CAP - 186, dout=128),           # 上端内角
        n(cx + 4, CAP + OSC - CHAIR - 4, L, t=0.56),
        n(CSTEM + 4, CAP / 2, D, t=0.56),
        n(cx + 10, -OSC + CHAIR + 4, R),
        n(W - 32, 196, din=52),                   # 下端内角
        n(W - 10, 128, dout=232),                 # 下端外角
        n(cx + 4, -OSC, L, t=0.58),
    ], name="C")], 4, 0


def g_D():
    x = SO + 4
    xs = x + CSTEM
    return [Shape(head(x, CAP, orr=0)[:-1] + [
        n(330, CAP, R, t=0.6), n(668, CAP / 2, D, t=0.6), n(330, 0, L, t="line"),
    ] + foot(x, w=CSTEM, ol=SO + 4, orr=0)[1:], name="D"),
        Shape([n(xs, CAP - CHAIR), n(320, CAP - CHAIR, R, t=0.6), n(668 - CSTEM - 6, CAP / 2, D, t=0.6),
               n(320, CHAIR, L, t="line"), n(xs, CHAIR)], hole=True, name="D 字怀")], 0, 0


def g_5():
    """5：顶横、竖、碗一条轮廓，碗的左下端收成球。"""
    r = 52
    bx, by = 96, 102
    vw = HAIR * 1.2
    return [Shape([
        n(100, 700), n(452, 700), n(452, 700 - HAIR * 1.05), n(100 + vw, 700 - HAIR * 1.05, t="line"),
        n(100 + vw, 446, dout=28),                # 竖右边沿往下到这里，转进碗的外沿
        n(290, 474, R),                           # 碗外沿顶
        n(474, 236, D, t=0.6),                    # 碗外沿右
        n(254, -OSC, L),                          # 碗外沿底
        n(bx - r, by, U),                         # 球左
        n(bx, by + r, R, t=0.5523),               # 球顶
        n(bx + r, by, D),                         # 球右，往下卷进内沿
        n(254, -OSC + HAIR + 2, R),               # 内沿底
        n(474 - STEM, 236, U, t=0.6),             # 内沿右
        n(284, 474 - HAIR, L),                    # 内沿顶
        n(100, 384, din=206, t="line"),           # 内沿落到竖左下角
    ], name="5")], 0, 0


def g_period():
    return [circle(70, 62, 60, name="句点")], 6, 0


GLYPHS = {
    "a": g_a, "c": g_c, "d": g_d, "e": g_e, "h": g_h, "i": g_i, "l": g_l, "m": g_m, "n": g_n,
    "o": g_o, "p": g_p, "r": g_r, "s": g_s, "t": g_t, "u": g_u, "v": g_v, "w": g_w, "y": g_y,
    "A": g_A, "C": g_C, "D": g_D, "I": g_I, "O": g_O, "5": g_5, ".": g_period,
}
