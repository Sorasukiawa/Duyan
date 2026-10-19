"""渡言的西文：用 pen.py 那支笔，从零构造每个字母。

参考 Anthropic Serif 的比例和气质（只量数字，不碰轮廓），按自己的取舍做：
字形略窄、衬线更短更利落，主干 100、细线 50。
"""
import math

from pen import _bez, _dbez, arc, contrast, curve, dot, line, poly, profile, ring, sweep

XH, OS = 540, 12            # x 高度、圆形字母的过冲
CAP, OSC = 720, 14
ASC, DESC = 760, -220
STEM, HAIR = 100, 50
CSTEM, CHAIR = 108, 52
SO, TIP, BR = 54, 12, 42    # 衬线：伸出长度、末端厚度、托角高度
PEN = contrast(STEM, HAIR, stress=0, power=1.35)
CPEN = contrast(CSTEM, CHAIR, stress=0, power=1.35)


# ───────── 部件 ─────────

def rect(x0, y0, x1, y1):
    return poly((x0, y0), (x1, y0), (x1, y1), (x0, y1))


def foot(xl, xr, y=0, ol=SO, or_=SO, tip=TIP, br=BR):
    """底部衬线，带弧形托角。"""
    return poly((xl - ol, y), (xr + or_, y), (xr + or_, y + tip), (xr, y + tip), (xr, y + tip + br),
                (xl, y + tip + br), (xl, y + tip), (xl - ol, y + tip), smooth={3, 6})


def head(xl, xr, y, ol=SO, or_=SO, tip=TIP, br=BR):
    """顶部衬线（大写字母用）。"""
    return poly((xl - ol, y), (xl - ol, y - tip), (xl, y - tip), (xl, y - tip - br), (xr, y - tip - br),
                (xr, y - tip), (xr + or_, y - tip), (xr + or_, y), smooth={2, 5})


def flag(xl, xr, top, out=SO + 4, drop=38, thick=12, br=58):
    """小写字母竖画顶端的楔形入笔衬线。"""
    return poly((xl - out, top - drop), (xr, top), (xr, top - 80), (xl, top - drop - br),
                (xl, top - drop - thick), (xl - out, top - drop - thick), smooth={4})


def ball(c, r=46):
    return dot(c, r, 10)


def ball_end(seg, t, w, r, toward):
    """贴着笔画外缘的球形收笔：球心从笔端往里挪 r - w/2，外缘和笔画外缘相切，接口不露角。
    seg 是笔画最后（或最前）一段，t 取 1（或 0），w 是笔端粗细，toward 是字怀那一侧的任意一点。"""
    E, T = _bez(seg, t), _dbez(seg, t)
    n = (-T[1], T[0])
    if (toward[0] - E[0]) * n[0] + (toward[1] - E[1]) * n[1] < 0:
        n = (-n[0], -n[1])
    return ball((E[0] + n[0] * (r - w / 2), E[1] + n[1] * (r - w / 2)), r)


def _x_at(edge, y):
    (x0, y0), (x1, y1) = edge
    return x0 + (y - y0) * (x1 - x0) / (y1 - y0)


def _edges(p0, p1, w):
    """直笔画的左右两条边（按顶部的 x 从左到右排）。"""
    d = (p1[0] - p0[0], p1[1] - p0[1])
    n = math.hypot(*d)
    o = (-d[1] / n * w / 2, d[0] / n * w / 2)
    a = ((p0[0] + o[0], p0[1] + o[1]), (p1[0] + o[0], p1[1] + o[1]))
    b = ((p0[0] - o[0], p0[1] - o[1]), (p1[0] - o[0], p1[1] - o[1]))
    return (a, b) if a[0][0] < b[0][0] else (b, a)


def dserif(left, right, y, ol, or_, tip=TIP, br=BR, top=True):
    """斜笔上的衬线：托角顺着两条斜边收进笔画里，所以接口处不会留小缺口。
    left、right 是笔画左右两条边，y 是衬线外沿（顶衬线的上沿、底衬线的下沿）。"""
    s = -1 if top else 1
    yb, yk = y + s * tip, y + s * (tip + br)
    xl0, xr0 = _x_at(left, y), _x_at(right, y)
    return poly((xl0 - ol, y), (xr0 + or_, y), (xr0 + or_, yb), (_x_at(right, yb), yb), (_x_at(right, yk), yk),
                (_x_at(left, yk), yk), (_x_at(left, yb), yb), (xl0 - ol, yb), smooth={3, 6})


def stemmed(xl, y0, y1, w=STEM):
    return rect(xl, y0, xl + w, y1)


# ───────── 小写 ─────────

def g_l():
    x = SO
    return [stemmed(x, 0, ASC - 60), flag(x, x + STEM, ASC), foot(x, x + STEM)], 0, 0


def g_i():
    x = SO
    return [stemmed(x, 0, XH - 60), flag(x, x + STEM, XH), foot(x, x + STEM),
            ball((x + STEM / 2 + 4, XH + 168), 56)], 0, 0


def _arch(x0, x1, top=XH, w=PEN):
    """n、m、h 的拱：从左竖右缘细细分出，拱顶细，落到右竖变粗。x0 左竖右缘，x1 右竖中心。"""
    yap = top + OS - HAIR / 2
    xap = (x0 + x1) / 2 + 14
    path = [curve((x0 - 30, top - 205), (x0 + 2, top - 78), (xap - 92, yap), (xap, yap)),
            curve((xap, yap), (xap + 84, yap), (x1, yap - 62), (x1, top - 205))]
    return sweep(path, profile(w, (0, .42), (.28, 1), (1, 1)))


def g_n():
    x, c = SO, 236
    r = x + STEM + c
    return [stemmed(x, 0, XH - 60), flag(x, x + STEM, XH), foot(x, x + STEM, or_=SO - 8),
            _arch(x + STEM, r + STEM / 2), stemmed(r, 0, XH - 200), foot(r, r + STEM, ol=SO - 8)], 0, 0


def g_h():
    x, c = SO, 236
    r = x + STEM + c
    return [stemmed(x, 0, ASC - 60), flag(x, x + STEM, ASC), foot(x, x + STEM, or_=SO - 8),
            _arch(x + STEM, r + STEM / 2), stemmed(r, 0, XH - 200), foot(r, r + STEM, ol=SO - 8)], 0, 0


def g_m():
    x, c = SO, 214
    r1 = x + STEM + c
    r2 = r1 + STEM + c
    return [stemmed(x, 0, XH - 60), flag(x, x + STEM, XH), foot(x, x + STEM, or_=SO - 10),
            _arch(x + STEM, r1 + STEM / 2), stemmed(r1, 0, XH - 200), foot(r1, r1 + STEM, ol=SO - 10, or_=SO - 10),
            _arch(r1 + STEM, r2 + STEM / 2), stemmed(r2, 0, XH - 200), foot(r2, r2 + STEM, ol=SO - 10)], 0, 0


def g_u():
    x, c = SO, 236
    r = x + STEM + c
    lc = x + STEM / 2
    yb = -OS + HAIR / 2
    xb = (lc + r) / 2 - 8
    bowl = sweep([line((lc, 250), (lc, 190)),
                  curve((lc, 190), (lc, 70), (xb - 100, yb), (xb, yb)),
                  curve((xb, yb), (xb + 92, yb), (r + 20, 70), (r + 30, 205))],
                 profile(PEN, (0, 1), (.72, 1), (1, .42)))
    return [stemmed(x, 230, XH - 60), flag(x, x + STEM, XH), bowl,
            stemmed(r, 0, XH - 60), flag(r, r + STEM, XH), foot(r, r + STEM, ol=0)], 0, 0


def _bowl(cx, cy, rx, ry, k=0.58, w=PEN):
    return ring(arc((cx, cy), rx, ry, 0, 360, k), w)


def g_o():
    W = 494
    rx, ry = (W - STEM) / 2, (XH + 2 * OS - HAIR) / 2
    return _bowl(W / 2, XH / 2, rx, ry), 4, 4


def g_c():
    W = 452
    rx, ry = (W - STEM) / 2 + 6, (XH + 2 * OS - HAIR) / 2
    cx, cy = rx + STEM / 2, XH / 2
    segs = arc((cx, cy), rx, ry, 40, 316, 0.58)
    width = profile(PEN, (0, .6), (.14, 1), (.9, 1), (1, .8))
    body = sweep(segs, width, cap1=("cut", 80))
    T = _dbez(segs[0], 0)
    return [body, ball_end(segs[0], 0, width(0, math.atan2(T[1], T[0])), 50, (cx, cy))], 4, 0


def g_e():
    W = 470
    rx, ry = (W - STEM) / 2 + 2, (XH + 2 * OS - HAIR) / 2
    cx, cy = rx + STEM / 2, XH / 2
    body = sweep(arc((cx, cy), rx, ry, 4, 322, 0.58), profile(PEN, (0, 1), (.9, 1), (1, .78)), cap1=("cut", 82))
    bar_y = 300
    bar = rect(STEM / 2 + 6, bar_y - HAIR * .5, cx + rx + STEM * .5 - 2, bar_y + HAIR * .5)
    return [body, bar], 4, 0


def g_a():
    sx = 330                              # 右竖左缘
    sc = sx + STEM / 2
    yap = XH + OS - HAIR / 2
    end = curve((sc - 150, yap), (sc - 230, yap), (sc - 286, XH - 40), (sc - 294, XH - 120))
    width = profile(PEN, (0, 1), (.8, 1), (1, .7))
    hood = sweep([curve((sc, XH - 150), (sc, XH - 30), (sc - 70, yap), (sc - 150, yap)), end], width)
    T = _dbez(end, 1)
    bowl = _bowl(sx - 92, 150, 132, 128, 0.6)
    return ([stemmed(sx, 0, XH - 150), hood, ball_end(end, 1, width(1, math.atan2(T[1], T[0])), 52, (sc, XH - 200))] + bowl
            + [foot(sx, sx + STEM, ol=0, or_=SO - 10)]), 0, 0


def g_d():
    sx = 360
    bowl = _bowl(sx - 110, XH / 2, 160, (XH + 2 * OS - HAIR) / 2, 0.58)
    return bowl + [stemmed(sx, 0, ASC - 60), flag(sx, sx + STEM, ASC), foot(sx, sx + STEM, ol=0)], 0, 0


def g_p():
    x = SO
    bowl = _bowl(x + STEM + 110, XH / 2, 160, (XH + 2 * OS - HAIR) / 2, 0.58)
    return [stemmed(x, DESC, XH - 60), flag(x, x + STEM, XH), foot(x, x + STEM, y=DESC)] + bowl, 0, 0


def g_r():
    x = SO
    yap = XH + OS - HAIR / 2
    seg = curve((x + STEM - 30, XH - 195), (x + STEM + 0, XH - 66), (x + STEM + 70, yap), (x + STEM + 152, yap))
    width = profile(PEN, (0, .42), (.4, 1), (1, 1.05))
    arm = sweep([seg], width)
    return [stemmed(x, 0, XH - 60), flag(x, x + STEM, XH), foot(x, x + STEM, or_=SO + 22), arm,
            ball_end(seg, 1, width(1, 0), 50, (x + STEM + 150, 0))], 0, 0


def g_s():
    W = 404
    yt, yb = XH + OS - HAIR / 2, -OS + HAIR / 2
    path = [line((W - 50, XH - 152), (W - 50, XH - 100)),
            curve((W - 50, XH - 100), (W - 52, yt - 6), (W - 150, yt), (W / 2 - 4, yt)),
            curve((W / 2 - 4, yt), (90, yt), (52, XH - 70), (56, XH - 150)),
            curve((56, XH - 150), (62, XH - 250), (W - 60, 300), (W - 52, 150)),
            curve((W - 52, 150), (W - 46, 50), (W - 120, yb), (W / 2 - 6, yb)),
            curve((W / 2 - 6, yb), (110, yb), (42, 30), (42, 100)),
            line((42, 100), (42, 150))]
    spine = profile(contrast(STEM * 1.04, HAIR, stress=-12, power=1.2), (0, .56), (.07, .9), (.13, 1), (.88, 1),
                    (.95, .9), (1, .56))
    return [sweep(path, spine)], 0, 0


def g_t():
    x = 60
    xc = x + STEM / 2
    yb = -OS + HAIR / 2
    main = sweep([line((xc, XH + 40), (xc, 120)),
                  curve((xc, 120), (xc, 30), (xc + 50, yb), (xc + 110, yb)),
                  curve((xc + 110, yb), (xc + 160, yb), (xc + 196, 30), (xc + 210, 74))],
                 profile(PEN, (0, 1), (.8, 1), (1, .85)))
    wedge = poly((x, XH + 30), (x + STEM, XH + 122), (x + STEM, XH + 30))
    bar = rect(xc - STEM / 2 - 62, XH - HAIR, xc + STEM / 2 + 128, XH)
    return [main, wedge, bar], 0, 0


def _diag(p0, p1, w, cut0=0, cut1=0):
    return sweep([line(p0, p1)], lambda s, phi: w, cap0=("cut", cut0), cap1=("cut", cut1))


def _isect(p1, p2, p3, p4):
    """两条直线 p1p2、p3p4 的交点。"""
    d = (p1[0] - p2[0]) * (p3[1] - p4[1]) - (p1[1] - p2[1]) * (p3[0] - p4[0])
    a = p1[0] * p2[1] - p1[1] * p2[0]
    b = p3[0] * p4[1] - p3[1] * p4[0]
    return ((a * (p3[0] - p4[0]) - (p1[0] - p2[0]) * b) / d, (a * (p3[1] - p4[1]) - (p1[1] - p2[1]) * b) / d)


def _vee(xl, xr, top=XH, bottom=-8, thick=STEM * 1.12, thin=HAIR * 1.3, vx=None):
    """v 形：左边粗笔下行，右边细笔上行。xl 粗笔左上角，xr 细笔右上角。
    返回轮廓和四条边（粗笔左、粗笔右、细笔左、细笔右），衬线按边来贴。"""
    vx = (xl + xr) / 2 + 22 if vx is None else vx
    V = (vx, bottom)
    TL, TR = (xl, top), (xl + thick, top)
    t1, t2 = (xr - thin, top), (xr, top)
    C = _isect(TR, (vx + thick, bottom), t1, (vx - thin, bottom))
    return poly(TL, TR, C, t1, t2, V), ((TL, V), (TR, (vx + thick, bottom)), (t1, (vx - thin, bottom)), (t2, V))


def g_v():
    W = 548
    body, (a, b, c, d) = _vee(70 - STEM * .56, W - 70 + HAIR * .65)
    return [body, dserif(a, b, XH, 20, 22), dserif(c, d, XH, 22, 18)], 0, 0


def g_w():
    W = 790
    m = W / 2
    left, (a, b, _, _) = _vee(66 - STEM * .54, m + 10, vx=226)
    right, (_, _, c, d) = _vee(m - 30, W - 66 + HAIR * .65, vx=W - 196)
    return [left, right, dserif(a, b, XH, 18, 20), dserif(c, d, XH, 20, 16)], 0, 0


def g_y():
    W = 540
    mid = W / 2
    q0, q1 = (W - 70, XH), (mid - 26, -60)
    end = curve(q1, (mid - 70, -170), (mid - 120, DESC + 24), (mid - 196, DESC + 24))
    width = profile(lambda s, phi: HAIR * 1.12, (0, 1), (.7, 1.1), (1, 1.2))
    tail = sweep([line(q0, q1), end], width, cap0=("cut", 0))
    tl, tr = _edges(q0, q1, HAIR * 1.12)
    al, ar = _edges((70, XH), (mid + 14, 10), STEM * .98)
    arm = poly((_x_at(al, XH), XH), (_x_at(ar, XH), XH), _isect(*ar, *tr), _isect(*al, *tl))
    return [arm, tail, ball_end(end, 1, width(1, 0), 48, (mid - 196, 0)),
            dserif(al, ar, XH, 22, 26), dserif(tl, tr, XH, 26, 20)], 0, 0


# ───────── 大写、数字、标点 ─────────

def g_I():
    x = SO + 4
    return [rect(x, 0, x + CSTEM, CAP), head(x, x + CSTEM, CAP, ol=SO + 4, or_=SO + 4),
            foot(x, x + CSTEM, ol=SO + 4, or_=SO + 4)], 0, 0


def g_A():
    W = 700
    Y = CAP + 12
    ax = W / 2 + 6
    nl, nr = _edges((ax - 24, Y), (88, 0), CHAIR * 1.15)       # 细笔
    kl, kr = _edges((ax - 40, Y), (W - 112, 0), CSTEM * 1.04)  # 粗笔
    body = poly((_x_at(nl, Y), Y), (_x_at(kr, Y), Y), (_x_at(kr, 0), 0), (_x_at(kl, 0), 0), _isect(*kl, *nr),
                (_x_at(nr, 0), 0), (_x_at(nl, 0), 0))
    return [body, rect(170, 210, W - 200, 210 + CHAIR),
            dserif(nl, nr, 0, 34, 40, top=False), dserif(kl, kr, 0, 26, 40, top=False)], 0, 0


def g_O():
    W = 726
    rx, ry = (W - CSTEM) / 2, (CAP + 2 * OSC - CHAIR) / 2
    return _bowl(W / 2, CAP / 2, rx, ry, 0.58, CPEN), 4, 4


def g_C():
    W = 664
    rx, ry = (W - CSTEM) / 2 + 10, (CAP + 2 * OSC - CHAIR) / 2
    cx, cy = rx + CSTEM / 2, CAP / 2
    body = sweep(arc((cx, cy), rx, ry, 36, 320, 0.58), profile(CPEN, (0, 1.2), (.1, 1), (.9, 1), (1, 1.1)))
    return [body], 4, 0


def g_D():
    x = SO + 4
    xc = x + CSTEM / 2
    yt, yb = CAP - CHAIR / 2, CHAIR / 2
    bowl = sweep([line((xc, yt), (300, yt)),
                  curve((300, yt), (560, yt), (640, 560), (640, CAP / 2)),
                  curve((640, CAP / 2), (640, 160), (560, yb), (300, yb)),
                  line((300, yb), (xc, yb))], CPEN)
    return [rect(x, 0, x + CSTEM, CAP), head(x, x + CSTEM, CAP, ol=SO + 4, or_=0),
            foot(x, x + CSTEM, ol=SO + 4, or_=0), bowl], 0, 0


def g_5():
    yap = 470
    end = curve((250, -OS + HAIR / 2), (150, -OS + HAIR / 2), (86, 30), (76, 96))
    width = profile(PEN, (0, .6), (.15, 1), (.86, 1), (1, .62))
    bowl = sweep([curve((112, 400), (170, 440), (230, yap), (290, yap)),
                  curve((290, yap), (420, yap), (470, 380), (470, 240)),
                  curve((470, 240), (470, 90), (380, -OS + HAIR / 2), (250, -OS + HAIR / 2)), end], width)
    T = _dbez(end, 1)
    return [bowl, ball_end(end, 1, width(1, math.atan2(T[1], T[0])), 52, (250, 240)), rect(100, 380, 100 + HAIR * 1.2, 700),
            rect(100, 700 - HAIR * 1.05, 452, 700)], 0, 0


def g_period():
    return [ball((70, 62), 60)], 6, 0


GLYPHS = {
    "a": g_a, "c": g_c, "d": g_d, "e": g_e, "h": g_h, "i": g_i, "l": g_l, "m": g_m, "n": g_n,
    "o": g_o, "p": g_p, "r": g_r, "s": g_s, "t": g_t, "u": g_u, "v": g_v, "w": g_w, "y": g_y,
    "A": g_A, "C": g_C, "D": g_D, "I": g_I, "O": g_O, "5": g_5, ".": g_period,
}
SIDE = 34      # 默认左右边距
