"""渡言的大写字母（A C D I O 在 latin.py 里，这里是其余 21 个）。

和小写同一套零件：竖连衬线、斜笔衬线顺着斜边、碗在竖上放角点。大写主干 108、细线 52，衬线伸出 58。
臂的末端是竖直的楔形小喙（E、F、L、T、Z）。
"""
from latin import (CAP, CHAIR, CSTEM, OSC, SO, STEM, BR, TIP, _edges, _isect, _x_at, foot, foot_serif, head,
                   ring, top_serif)
from outline import D, L, R, U, Shape, n

CO = SO + 4                 # 大写衬线伸出
W0 = 58                     # 竖的左边沿


def _stem_cw(x, top=CAP, bottom=0, w=CSTEM, hl=CO, hr=CO, fl=CO, fr=CO):
    """一根带衬线的竖：返回（顶部节点, 底部节点），中间由调用的人接上右边沿和左边沿的内容。"""
    return head(x, top, w, hl, hr), foot(x, w, bottom, fl, fr)


# ───────── 直笔为主 ─────────

def g_H():
    x, xr = W0, W0 + CSTEM + 372
    return [Shape(head(x, CAP) + [n(x + CSTEM, 396), n(xr, 396, t="line")] + head(xr, CAP) + foot(xr, CSTEM)
                  + [n(xr, 344), n(x + CSTEM, 344, t="line")] + foot(x, CSTEM), name="H")], 0, 0


def _arm_end_down(x_end, y_top, hb=CHAIR, drop=118):
    """臂的右端往下的小喙（E、F、T 的顶臂）：顺时针，从臂的顶边进来，从臂的底边出去。"""
    return [n(x_end, y_top), n(x_end + 6, y_top - drop, tip=True), n(x_end - 44, y_top - hb, t="line")]


def _arm_end_up(x_end, y_bot, hb=CHAIR, rise=118):
    """臂的右端往上的小喙（E、L、Z 的底臂）：顺时针，从臂的顶边进来，从臂的底边出去。"""
    return [n(x_end - 44, y_bot + hb), n(x_end + 6, y_bot + rise, tip=True), n(x_end, y_bot)]


def _mid_arm(x0, x_end, yc, h=CHAIR - 4):
    """中间的臂：末端上下各有一点小衬线。顺时针：竖的右边沿往下 → 臂顶 → 末端 → 臂底 → 回到竖。"""
    t, b = yc + h / 2, yc - h / 2
    return [n(x0, t), n(x_end - 30, t), n(x_end, t + 38, tip=True), n(x_end + 4, b - 38, tip=True),
            n(x_end - 30, b), n(x0, b, t="line")]


def g_E():
    x = W0
    xs = x + CSTEM
    return [Shape(head(x, CAP, orr=0)[:-1] + _arm_end_down(560, CAP) + [n(xs, CAP - CHAIR, t="line")]
                  + _mid_arm(xs, 498, 368) + [n(xs, CHAIR + 4)] + _arm_end_up(590, 0, hb=CHAIR + 4)
                  + foot(x, CSTEM, 0, CO, 0)[1:], name="E")], 0, 0


def g_F():
    x = W0
    xs = x + CSTEM
    return [Shape(head(x, CAP, orr=0)[:-1] + _arm_end_down(548, CAP) + [n(xs, CAP - CHAIR, t="line")]
                  + _mid_arm(xs, 486, 360) + foot(x, CSTEM, 0, CO, CO), name="F")], 0, 0


def g_L():
    x = W0
    xs = x + CSTEM
    return [Shape(head(x, CAP) + [n(xs, CHAIR + 4)] + _arm_end_up(566, 0, hb=CHAIR + 4)
                  + foot(x, CSTEM, 0, CO, 0)[1:], name="L")], 0, 0


def g_T():
    xl, xr = 30, 630
    xs = (xl + xr) / 2 - CSTEM / 2
    return [Shape([n(xl, CAP), n(xr, CAP), n(xr + 6, CAP - 124, tip=True), n(xr - 44, CAP - CHAIR, t="line"),
                   n(xs + CSTEM, CAP - CHAIR, t="line")] + foot(xs, CSTEM, 0, CO, CO)
                  + [n(xs, CAP - CHAIR), n(xl + 44, CAP - CHAIR), n(xl - 6, CAP - 124, tip=True)], name="T")], 0, 0


def g_J():
    """J：竖（顶上两边有衬线）往下弯向左，收成球，略低于基线。"""
    x = 200
    r = 40
    bx, by = x - 112, 40
    return [Shape(head(x, CAP) + [
        n(x + CSTEM, 150, D),                     # 右边沿往下，开始往左弯
        n(x - 20, -OSC - 30, L, t=0.6),           # 底
        n(bx - r, by, U, t=0.58),                 # 球左
        n(bx, by + r, R, t=0.5523),               # 球顶，往右卷进内沿
        n(x, 140, U, t="line"),
    ], name="J")], 0, 0


# ───────── 带碗的 ─────────

def g_P():
    x = W0
    xs = x + CSTEM
    yb = 300                                       # 碗底外沿
    return [Shape(head(x, CAP, orr=0)[:-1] + [
        n(340, CAP, R, t=0.62), n(626, (CAP + yb) / 2 + 6, D, t=0.62), n(330, yb, L, t="line"),
        n(xs, yb, t="line"),
    ] + foot(x, CSTEM, 0, CO, CO), name="P"),
        Shape([n(xs, CAP - CHAIR), n(330, CAP - CHAIR, R, t=0.6), n(626 - CSTEM - 2, (CAP + yb) / 2 + 6, D, t=0.6),
               n(322, yb + CHAIR, L, t="line"), n(xs, yb + CHAIR)], hole=True, name="P 字怀")], 0, 0


def g_B():
    x = W0
    xs = x + CSTEM
    ym = 382                                       # 两个碗相接的腰
    return [Shape(head(x, CAP, orr=0)[:-1] + [
        n(330, CAP, R, t=0.62), n(580, 556, D, t=0.62),
        n(452, ym + 6, din=220, dout=-14),         # 上碗收回来、下碗出去的腰
        n(640, 196, D, t=0.62), n(340, 0, L, t="line"),
    ] + foot(x, CSTEM, 0, CO, 0)[1:], name="B"),
        Shape([n(xs, CAP - CHAIR), n(322, CAP - CHAIR, R, t=0.6), n(580 - CSTEM + 4, 560, D, t=0.6),
               n(318, ym + 26, L, t="line"), n(xs, ym + 26)], hole=True, name="B 上字怀"),
        Shape([n(xs, ym - 26), n(340, ym - 26, R, t=0.6), n(640 - CSTEM - 2, 192, D, t=0.6),
               n(334, CHAIR, L, t="line"), n(xs, CHAIR)], hole=True, name="B 下字怀")], 0, 0


def g_R():
    """R：P 加一条腿。腿从碗底往右下走到基线，带脚衬线。"""
    x = W0
    xs = x + CSTEM
    yb = 316
    ll, lr = _edges((380, yb + 20), (620, 0), CSTEM * 1.02)
    return [Shape(head(x, CAP, orr=0)[:-1] + [
        n(340, CAP, R, t=0.62), n(626, (CAP + yb) / 2 + 10, D, t=0.62),
        n(_x_at(lr, yb + 40), yb + 40, din=236),   # 碗的右下接腿的右边沿
    ] + foot_serif(ll, lr, 0, 24, 40, brl=24)[0:6] + [
        n(_x_at(ll, yb), yb),                       # 腿的左边沿碰到碗底：夹角
        n(xs, yb, t="line"),
    ] + foot(x, CSTEM, 0, CO, CO), name="R"),
        Shape([n(xs, CAP - CHAIR), n(330, CAP - CHAIR, R, t=0.6), n(626 - CSTEM - 2, (CAP + yb) / 2 + 10, D, t=0.6),
               n(322, yb + CHAIR, L, t="line"), n(xs, yb + CHAIR)], hole=True, name="R 字怀")], 0, 0


def g_U():
    """U：左竖粗、右竖细，底部连成一个碗。两竖顶上都有衬线。"""
    x, xr = W0, W0 + CSTEM + 380
    wr = CHAIR * 1.3
    return [Shape(head(x, CAP) + [
        n(x + CSTEM, 230, D),                      # 左竖右边沿往下，转进碗的内沿
        n((x + CSTEM + xr) / 2 + 6, -OSC + CHAIR, R, t=0.6),
        n(xr, 220, U, t="line"),                   # 右竖左边沿
    ] + head(xr, CAP, w=wr, ol=CO - 6, orr=CO - 6) + [
        n(xr + wr, 220, D),                        # 右竖右边沿往下，转进碗的外沿
        n((x + xr + wr) / 2, -OSC, L, t=0.6),
        n(x, 230, U, t="line"),
    ], name="U")], 0, 0


def g_G():
    """G：C 的下半改成一根竖着的短柱（带衬线），柱顶到中线附近。"""
    W = 690
    cx = 360
    sx = W - CSTEM                                 # 柱的左边沿
    top = 330
    return [Shape([
        n(0, CAP / 2, U, t=0.58),
        n(cx, CAP + OSC, R),
        n(W - 26, CAP - 120, din=-54),             # 上端外角
        n(W - 46, CAP - 186, dout=128),            # 上端内角
        n(cx + 4, CAP + OSC - CHAIR - 4, L, t=0.56),
        n(CSTEM + 4, CAP / 2, D, t=0.56),
        n(cx + 10, -OSC + CHAIR + 4, R, t=0.62),
        n(sx, 150, U, t="line"),                   # 内沿上到柱的左边沿
        n(sx, top - TIP - BR, U), n(sx - CO, top - TIP, din=L), n(sx - CO, top), n(W + 20, top),
        n(W + 20, top - TIP, dout=L), n(W, top - TIP - BR, D, t="line"),
        n(W, 110, D),                              # 柱的右边沿往下，转进外沿
        n(cx + 4, -OSC, L, t=0.6),
    ], name="G")], 4, 0


def g_Q():
    """Q：O 加一条尾巴，尾巴从底部中间偏右出来，往右下甩出去、收细。"""
    o = ring(0, 734, -OSC, CAP + OSC, thick=CSTEM, thin=CHAIR, name="Q")
    tail = Shape([
        n(342, 20, hid=True), n(452, -24, -28),
        n(716, -158, din=-22, dout=168, tip=True),
        n(520, -116, 160), n(392, -50, 150), n(316, 4, hid=True),
    ], name="Q 尾巴")
    return o + [tail], 4, 0


# ───────── 斜笔 ─────────

def g_V():
    W = 720
    xl, xr = 20, W - 20
    thick, thin = CSTEM * 1.1, CHAIR * 1.25
    vx = W / 2 + 10
    V = (vx, -10)
    kl, kr = ((xl + 30, CAP), V), ((xl + 30 + thick, CAP), (vx + thick, -10))
    nl, nr = ((xr - 30 - thin, CAP), (vx - thin, -10)), ((xr - 30, CAP), V)
    return [Shape(top_serif(kl, kr, CAP, 28, 30) + [n(*_isect(kr, nl))] + top_serif(nl, nr, CAP, 30, 26)
                  + [n(*V, tip=True)], name="V")], 0, 0


def g_W():
    W = 980
    thick, thin = CSTEM * 1.06, CHAIR * 1.2
    xl1, v1 = 40, 300
    xl2, v2 = 470, W - 270
    xr1 = 520
    xr2 = W - 40
    k1l, k1r = ((xl1, CAP), (v1, -10)), ((xl1 + thick, CAP), (v1 + thick, -10))
    n1l, n1r = ((xr1 - thin, CAP), (v1 - thin, -10)), ((xr1, CAP), (v1, -10))
    k2l, k2r = ((xl2, CAP), (v2, -10)), ((xl2 + thick, CAP), (v2 + thick, -10))
    n2l, n2r = ((xr2 - thin, CAP), (v2 - thin, -10)), ((xr2, CAP), (v2, -10))
    return [Shape(top_serif(k1l, k1r, CAP, 26, 26) + [n(*_isect(k1r, n1l)), n(_x_at(n1l, CAP), CAP),
                                                      n(_x_at(k2r, CAP), CAP), n(*_isect(k2r, n2l))]
                  + top_serif(n2l, n2r, CAP, 26, 24) + [n(v2, -10, tip=True), n(*_isect(k2l, n1r)), n(v1, -10, tip=True)],
                  name="W")], 0, 0


def g_X():
    W = 690
    kl, kr = _edges((90, CAP), (W - 90, 0), CSTEM * 1.06)
    nl, nr = _edges((W - 96, CAP), (96, 0), CHAIR * 1.2)
    return [Shape(top_serif(kl, kr, CAP, 30, 26) + [n(*_isect(kr, nl))] + top_serif(nl, nr, CAP, 28, 30)
                  + [n(*_isect(nr, kr))] + foot_serif(kl, kr, 0, 26, 34) + [n(*_isect(kl, nr))]
                  + foot_serif(nl, nr, 0, 34, 26) + [n(*_isect(nl, kl))], name="X")], 0, 0


def g_Y():
    """Y：粗的左臂、细的右臂在中间汇合，下面接一根竖。"""
    W = 680
    xc = W / 2
    xs = xc - CSTEM / 2
    ym = 330                                       # 两臂汇合处
    kl, kr = _edges((80, CAP), (xc + 4, ym), CSTEM * 1.04)
    nl, nr = _edges((W - 80, CAP), (xc - 4, ym), CHAIR * 1.25)
    return [Shape(top_serif(kl, kr, CAP, 28, 26) + [n(*_isect(kr, nl))] + top_serif(nl, nr, CAP, 26, 28)
                  + [n(xs + CSTEM, _y_at(nr, xs + CSTEM)), n(xs + CSTEM, 120, D, t="line")]
                  + foot(xs, CSTEM, 0, CO, CO) + [n(xs, _y_at(kl, xs))], name="Y")], 0, 0


def _y_at(e, x):
    (x0, y0), (x1, y1) = e
    return y0 + (x - x0) * (y1 - y0) / (x1 - x0)


def g_Z():
    ht, hb = CHAIR, CHAIR + 4
    k = (566 - 160) / (CAP - hb)                   # 斜笔每升高 1 往右 k
    right = lambda y: 566 - (CAP - y) * k
    left = lambda y: 566 - 150 - (CAP - y) * k
    return [Shape([
        n(50, CAP), n(right(CAP), CAP, t="line"),
        n(right(hb), hb), n(520, hb), n(588, hb + 110, tip=True), n(594, 0), n(left(0), 0, t="line"),
        n(left(CAP - ht), CAP - ht), n(110, CAP - ht), n(48, CAP - ht - 110, tip=True),
    ], name="Z")], 0, 0


def g_K():
    """K：竖、细臂、粗腿一条轮廓。臂从竖的右边沿伸到大写高度，腿从臂上分出往右下。"""
    x = W0
    x0 = x + CSTEM
    arm_l, arm_r = _edges((x0 - 40, 230), (x0 + 380, CAP), CHAIR * 1.3)
    leg_l, leg_r = _edges((x0 + 130, 420), (x0 + 440, 0), CSTEM * 1.04)
    yu = _y_at(arm_l, x0)
    yl = _y_at(arm_r, x0)
    return [Shape(head(x, CAP) + [n(x0, yu)] + top_serif(arm_l, arm_r, CAP, 28, 34) + [
        n(*_isect(arm_r, leg_r)),
    ] + foot_serif(leg_l, leg_r, 0, 24, 46, brl=24) + [
        n(*_isect(arm_r, leg_l)),
        n(x0, yl, t="line"),
    ] + foot(x, CSTEM, 0, CO, CO), name="K")], 0, 0


def g_N():
    """N：左竖细、斜笔粗、右竖细。斜笔是等宽的平行四边形：顶上和左竖合成一个平头（左边带衬线），
    底下在右竖处平切；斜笔上沿在右竖左边沿、下沿在左竖右边沿各形成一个夹角。"""
    x = W0
    wl = wr = CHAIR * 1.3
    xr = 600                                       # 右竖左边沿
    dw = 130                                       # 斜笔的水平宽度
    dl = ((x + wl - 40, CAP), (xr + wr - dw, -12))   # 斜笔下沿
    dr = ((x + wl - 40 + dw, CAP), (xr + wr, -12))   # 斜笔上沿
    return [Shape([
        n(x, CAP - TIP - BR, U), n(x - CO + 4, CAP - TIP, din=L), n(x - CO + 4, CAP), n(*dr[0]),
        n(*_isect(dr, ((xr, 0), (xr, CAP)))),     # 斜笔上沿碰到右竖左边沿
        n(xr, CAP - TIP - BR, U), n(xr - CO + 4, CAP - TIP, din=L), n(xr - CO + 4, CAP), n(xr + wr + CO - 4, CAP),
        n(xr + wr + CO - 4, CAP - TIP, dout=L), n(xr + wr, CAP - TIP - BR, D, t="line"),
        n(*dr[1]), n(*dl[1]),                      # 斜笔的平底
        n(*_isect(dl, ((x + wl, 0), (x + wl, CAP)))),  # 斜笔下沿碰到左竖右边沿
        n(x + wl, TIP + BR, D),
    ] + foot(x, wl, 0, CO - 4, CO - 4)[1:], name="N")], 0, 0


def _shift_up(e, w):
    """把斜边往右上方平移，使两条边相距 w（垂直距离）。"""
    import math
    (x0, y0), (x1, y1) = e
    dx, dy = x1 - x0, y1 - y0
    k = math.hypot(dx, dy)
    nx, ny = -dy / k, dx / k
    if ny < 0:
        nx, ny = -nx, -ny
    return ((x0 + nx * w, y0 + ny * w), (x1 + nx * w, y1 + ny * w))


def g_M():
    """M：左竖细、左斜粗、右斜细、右竖粗。先定中间底尖的位置，再从底尖推出两条斜笔的边；
    两个顶角是平头，中间顶上是夹角。"""
    x = W0
    W = 860
    wl = CHAIR * 1.3
    xr = W - 60 - CSTEM                            # 右竖左边沿
    V = ((x + W - 60) / 2 + 6, -12)                # 中间的底尖
    kl = ((x + wl, CAP - 200), V)                  # 左斜下沿：从左竖右边沿到底尖
    nr = ((xr, CAP - 160), V)                      # 右斜下沿：从右竖左边沿到底尖
    kr = _shift_up(kl, CSTEM * 1.04)               # 左斜上沿
    nl = _shift_up(nr, CHAIR * 1.2)                # 右斜上沿
    return [Shape([
        n(x, CAP - TIP - BR, U), n(x - CO + 4, CAP - TIP, din=L), n(x - CO + 4, CAP), n(_x_at(kr, CAP), CAP),
        n(*_isect(kr, nl)),                        # 中间顶上的夹角
        n(_x_at(nl, CAP), CAP), n(xr + CSTEM + CO, CAP), n(xr + CSTEM + CO, CAP - TIP, dout=L),
        n(xr + CSTEM, CAP - TIP - BR, D, t="line"),
    ] + foot(xr, CSTEM, 0, CO, CO) + [
        n(*nr[0]),                                 # 右斜下沿碰到右竖左边沿
        n(*V, tip=True),
        n(*kl[0]),                                 # 左斜下沿碰到左竖右边沿
        n(x + wl, TIP + BR, D),
    ] + foot(x, wl, 0, CO - 4, CO - 4)[1:], name="M")], 0, 0


def g_S():
    """S：和小写 s 同样的做法，按大写高度重新定节点。"""
    W = 520
    cx, cy = W / 2, CAP / 2
    upper = [
        n(40, 532, U, t=0.6),
        n(262, CAP + OSC, R),
        n(492, 634, din=302),
        n(450, 556, dout=124),
        n(266, CAP + OSC - CHAIR - 2, L, t=0.6),
        n(152, 560, D),
        n(292, 418, 328, t=0.6),
    ]
    rot = lambda q, grow: n(2 * cx - q.x + grow[0], 2 * cy - q.y + grow[1],
                            din=None if q.din is None else (q.din + 180) % 360,
                            dout=None if q.dout is None else (q.dout + 180) % 360, t=q.t)
    grow = [(8, 0), (2, 0), (-6, 0), (-2, 2), (2, 0), (8, 0), (0, 0)]
    return [Shape(upper + [rot(q, g) for q, g in zip(upper, grow)], name="S")], 0, 0


GLYPHS = {
    "B": g_B, "E": g_E, "F": g_F, "G": g_G, "H": g_H, "J": g_J, "K": g_K, "L": g_L, "M": g_M, "N": g_N,
    "P": g_P, "Q": g_Q, "R": g_R, "S": g_S, "T": g_T, "U": g_U, "V": g_V, "W": g_W, "X": g_X, "Y": g_Y, "Z": g_Z,
}
