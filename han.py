"""渡言的汉字：轮廓优先，宋体笔法。

字身框 1000 × 1000（y 从 -120 到 880），字面大约 x 60–960、y -60–915。
竖画 104、横画 60，和西文同一套粗细。
每一笔（连笔也算一笔）画成一条闭合轮廓，都按顺时针写（墨在走向的右边）：
横折、横撇、横钩、横折钩、「了」的横撇连弯钩，转角处的肩直接画在轮廓里；
不相连的笔画在笔画深处交叉，要藏起来的端点标 hid，有意的尖标 tip。
"""
import math

from outline import D, L, R, U, Shape, n

V, H = 104, 60
T = H / 2


# ───────── 几何小工具 ─────────

def _bz(seg, t):
    p0, p1, p2, p3 = seg
    u = 1 - t
    return (u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0],
            u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1])


def _unit(v):
    k = math.hypot(*v) or 1
    return (v[0] / k, v[1] / k)


def _ang(v):
    return math.degrees(math.atan2(v[1], v[0])) % 360


def _tan(seg, t):
    a, b = _bz(seg, max(0, t - 1e-4)), _bz(seg, min(1, t + 1e-4))
    return _unit((b[0] - a[0], b[1] - a[1]))


def _edge(seg, t, wf, side):
    """中心线 seg 在 t 处、走向左手（side=+1）或右手（side=-1）那条边上的点。"""
    p, d = _bz(seg, t), _tan(seg, t)
    w = wf(t) / 2 * side
    return (p[0] - d[1] * w, p[1] + d[0] * w)


def _edge_dir(seg, t, wf, side):
    a = _edge(seg, max(0, t - 1e-3), wf, side)
    b = _edge(seg, min(1, t + 1e-3), wf, side)
    return _ang((b[0] - a[0], b[1] - a[1]))


def _solve(f, lo, hi, target):
    """f 单调时，在 [lo, hi] 里找 f(t) = target。"""
    flo = f(lo) - target
    for _ in range(60):
        mid = (lo + hi) / 2
        fm = f(mid) - target
        if (fm > 0) == (flo > 0):
            lo, flo = mid, fm
        else:
            hi = mid
    return (lo + hi) / 2


def sym_end(a, a_dir, b):
    """从 a 以 a_dir 出发、匀称地弯到 b，到 b 时的走向（两端转角相等）。"""
    chord = _ang((b[0] - a[0], b[1] - a[1]))
    turn = ((chord - a_dir + 180) % 360) - 180
    return (chord + turn) % 360


def sym_start(a, b, b_dir):
    """匀称地弯进 b（到 b 时走向 b_dir），从 a 出发时的走向。"""
    chord = _ang((b[0] - a[0], b[1] - a[1]))
    turn = ((b_dir - chord + 180) % 360) - 180
    return (chord - turn) % 360


def pie_seg(p0, p1, bend=(0, 0)):
    c1 = (p0[0] + (p1[0] - p0[0]) * 0.15 + bend[0] * .3, p0[1] + (p1[1] - p0[1]) * 0.35 + bend[1] * .3)
    c2 = (p0[0] + (p1[0] - p0[0]) * 0.6 + bend[0], p0[1] + (p1[1] - p0[1]) * 0.85 + bend[1])
    return (p0, c1, c2, p1)


def on_pie(p0, p1, bend, y):
    """撇的中心线在高度 y 处的点：捺从这里起笔，起笔藏进撇身里。"""
    seg = pie_seg(p0, p1, bend)
    return _bz(seg, _solve(lambda t: _bz(seg, t)[1], 0, 1, y))


# ───────── 笔画的端头（按顺时针给节点）─────────

def heng_left(x0, y, entry=True):
    """横的左端：沿底边往左进来，往上，沿顶边往右出去。入笔略圆、微斜。"""
    if entry:
        return [n(x0 + 4, y - T, dout=112), n(x0 + 14, y + T, din=46, t="line")]
    return [n(x0, y - T, hid=entry is None), n(x0, y + T, hid=entry is None, t="line")]


def heng_right(x0, x1, y, beak=True, hid=False):
    """横的右端：沿顶边进来，经过喙，往下，沿底边往左出去。beak 可以是 0～1 的数，按比例压矮喙。"""
    if not beak:
        return [n(x1, y + T, hid=hid), n(x1, y - T, hid=hid, t="line")]
    span = x1 - x0
    bh, bw = min(48, 18 + span * 0.055), min(96, 34 + span * 0.1)
    if beak is not True:
        bh *= beak
    return [n(x1 - bw, y + T, R), n(x1 - bw * 0.24, y + T + bh, R, t=0.62),
            n(x1, y + T * 0.1, D), n(x1 - 20, y - T, L, t="line")]


def shoulder(x1, y, lift=16):
    """折的肩：横的顶边在转角前隆起，圆圆地落到竖的右边沿。x1 是竖的右边沿。"""
    return [n(x1 - V - 14, y + T, R), n(x1 - 26, y + T + lift, R, t=0.62), n(x1, y - 34, D, t="line")]


def shu_top(x, y0, kind="head", w=V):
    """竖的顶：沿左边沿往上进来，沿右边沿往下出去。head 是左高右低的斜切加圆肩。"""
    l, r = x - w / 2, x + w / 2
    if kind == "head":
        return [n(l, y0 + 16), n(r - 20, y0 - 2, -12), n(r, y0 - 38, D, t="line")]
    hid = kind == "hid"
    return [n(l, y0, hid=hid), n(r, y0, hid=hid, t="line")]


def shu_end(x, y1, kind="dew", w=V):
    """竖的底：沿右边沿往下进来，沿左边沿往上出去。dew 垂露，needle 悬针。"""
    l, r = x - w / 2, x + w / 2
    if kind == "dew":
        return [n(r, y1 + 34, D), n(x + 2, y1 - 10, L, t=0.6), n(l, y1 + 26, U, t="line")]
    if kind == "needle":
        return [n(r, y1 + 230, D, t=0.5), n(x + 2, y1, din=250, dout=110, tip=True, t=0.5), n(l, y1 + 230, U, t="line")]
    hid = kind == "hid"
    return [n(r, y1, hid=hid), n(l, y1, hid=hid, t="line")]


def gou_end(x, y, dx=-120, dy=86, w=V):
    """竖钩的底：右边沿圆转到底，向左上挑出尖，钩的上沿顺着弯回竖的左边沿。"""
    l, r = x - w / 2, x + w / 2
    tip = (x + dx, y + dy)
    bottom = (x + 4, y - 14)
    join = (l, y + 160)
    return [n(r, y + 80, D), n(*bottom, L, t=0.6),
            n(*tip, din=sym_end(bottom, 180, tip), dout=sym_start(tip, join, 90), tip=True),
            n(*join, U, t="line")]


# ───────── 单笔 ─────────

def heng(x0, x1, y, beak=True, entry=True, right_hid=False):
    """横。entry=None 表示左端藏起来（平头、hid）。"""
    return Shape(heng_left(x0, y, entry) + heng_right(x0, x1, y, beak, right_hid), name="横")


def shu(x, y0, y1, top="head", end="dew"):
    return Shape(shu_top(x, y0, top) + shu_end(x, y1, end), name="竖")


def _pie_width(w0, w1):
    return lambda t: w1 + (w0 - w1) * (1 - t ** 1.7)


def _side(seg, wf, ts, sd):
    """沿一条边在几个 t 处放光滑节点；sd=-1 那条边是倒着走的。"""
    out = []
    for t in (ts if sd > 0 else reversed(ts)):
        a = _edge_dir(seg, t, wf, sd)
        out.append(n(*_edge(seg, t, wf, sd), a if sd > 0 else (a + 180) % 360))
    return out


def _pie_body(seg, wf, mids=(0.36, 0.7)):
    """撇身：沿左手边（屏幕右下那条）往下到尖，再沿右手边（屏幕左上那条）回来。"""
    tip = _bz(seg, 1)
    td = _tan(seg, 1)
    tip = (tip[0] + td[0] * 3, tip[1] + td[1] * 3)
    return _side(seg, wf, mids, 1) + [
        n(*tip, din=_edge_dir(seg, 0.97, wf, 1), dout=(_edge_dir(seg, 0.97, wf, -1) + 180) % 360, tip=True),
    ] + _side(seg, wf, mids, -1)


def pie(p0, p1, bend=(0, 0), w0=V * 1.02, w1=10, head="cut"):
    """撇：粗起细收。head：cut（左高右低斜切、右角圆）、hid（藏进别的笔画）、round（圆头）。"""
    seg = pie_seg(p0, p1, bend)
    wf = _pie_width(w0, w1)
    d0 = _tan(seg, 0)
    a, b = _edge(seg, 0, wf, -1), _edge(seg, 0, wf, 1)     # 起笔的左上角、右下角
    body = _pie_body(seg, wf)
    up0 = (_edge_dir(seg, 0, wf, -1) + 180) % 360           # 沿左上那条边往上走到起笔的方向
    if head == "cut":
        hl = (a[0], a[1] + 10)
        cut = _unit((b[0] - hl[0], b[1] - hl[1]))
        e0 = _edge_dir(seg, 0.02, wf, 1)
        ed = (math.cos(math.radians(e0)), math.sin(math.radians(e0)))
        r = 14
        # 左上角也磨圆一点（半径 6），右下角圆一些（半径 14）
        ud = (math.cos(math.radians(up0)), math.sin(math.radians(up0)))
        start = [n(hl[0] - ud[0] * 6, hl[1] - ud[1] * 6, up0), n(hl[0] + cut[0] * 6, hl[1] + cut[1] * 6, _ang(cut)),
                 n(b[0] - cut[0] * r, b[1] - cut[1] * r, _ang(cut)), n(b[0] + ed[0] * r, b[1] + ed[1] * r, e0)]
    elif head == "round":
        rr = wf(0) / 2
        back = (p0[0] - d0[0] * rr, p0[1] - d0[1] * rr)
        start = [n(*a, (_ang(d0) + 180) % 360, t=0.5523), n(*back, (_ang(d0) + 90) % 360, t=0.5523),
                 n(*b, _ang(d0))]
        start = [start[1], start[2]]
        body = body + [n(*a, (_ang(d0) + 180) % 360, t=0.5523)]
    else:
        start = [n(*a, din=up0, hid=True), n(*b, dout=_edge_dir(seg, 0, wf, 1), hid=True)]
    return Shape(start + body, name="撇")


def na(p0, p1, bend=(30, -10), wmax=V * 1.18, w0=30, foot=0.62):
    """捺：起笔藏进别的笔画（平头、hid），越写越粗，末端平出捺脚：上沿凹下去接到尖，底边平。"""
    c1 = (p0[0] + (p1[0] - p0[0]) * 0.3 + bend[0], p0[1] + (p1[1] - p0[1]) * 0.3 + bend[1])
    c2 = (p0[0] + (p1[0] - p0[0]) * 0.72 + bend[0] * .5, p0[1] + (p1[1] - p0[1]) * 0.8 + bend[1] * .5)
    seg = (p0, c1, c2, p1)
    wf = lambda t: w0 + (wmax - w0) * t ** 1.25
    top_end = _edge(seg, 0.86, wf, 1)                 # 上沿开始凹下去的地方
    bot = _edge(seg, 1, wf, -1)
    up = _edge(seg, 1, wf, 1)
    tip = (max(up[0], bot[0]) + wmax * foot, bot[1] + 8)
    d_top = _edge_dir(seg, 0.86, wf, 1)
    s_l, s_r = _edge(seg, 0, wf, 1), _edge(seg, 0, wf, -1)
    return Shape([n(*s_l, _edge_dir(seg, 0, wf, 1), hid=True)] + _side(seg, wf, (0.3, 0.6), 1) + [
        n(*top_end, d_top),
        n(*tip, din=sym_end(top_end, d_top, tip), dout=180, tip=True),
        n(bot[0] + 6, bot[1], 180),
    ] + _side(seg, wf, (0.3, 0.64), -1) + [
        n(*s_r, (_edge_dir(seg, 0, wf, -1) + 180) % 360, hid=True, t="line"),
    ], name="捺")


def dian(p0, p1, w=V * 1.2):
    """点：尖头入笔，圆头收笔（对应西文的球形收笔）。"""
    d = _unit((p1[0] - p0[0], p1[1] - p0[1]))
    nl = (-d[1], d[0])
    r = w / 2
    a = (p1[0] + nl[0] * r, p1[1] + nl[1] * r)        # 走向左手那一侧
    b = (p1[0] + d[0] * r, p1[1] + d[1] * r)
    c = (p1[0] - nl[0] * r, p1[1] - nl[1] * r)
    da = _ang(d)
    return Shape([
        n(*p0, din=sym_end(c, (da + 180) % 360, p0), dout=sym_start(p0, a, da), tip=True),
        n(*a, da, t=0.5523), n(*b, (da - 90) % 360, t=0.5523), n(*c, (da + 180) % 360),
    ], name="点")


def ti(p0, p1, w0=V * 1.08):
    """提：圆头起笔，向右上挑出尖。"""
    d = _unit((p1[0] - p0[0], p1[1] - p0[1]))
    nl = (-d[1], d[0])
    r = w0 / 2
    a = (p0[0] - nl[0] * r, p0[1] - nl[1] * r)        # 右手边起点
    back = (p0[0] - d[0] * r, p0[1] - d[1] * r)
    c = (p0[0] + nl[0] * r, p0[1] + nl[1] * r)
    da = _ang(d)
    return Shape([
        n(*back, (da + 90) % 360, t=0.5523),
        n(*c, da),
        n(*p1, din=sym_end(c, da, p1), dout=sym_start(p1, a, (da + 180) % 360), tip=True),
        n(*a, (da + 180) % 360, t=0.5523),
    ], name="提")


# ───────── 连笔 ─────────

def hengzhe(x0, x1, y, y1, end="dew", entry=True):
    """横折：横、肩、竖一条轮廓。x1 是竖的右边沿。"""
    xv = x1 - V / 2
    return Shape(heng_left(x0, y, entry) + shoulder(x1, y) + shu_end(xv, y1, end) + [n(x1 - V, y - T)],
                 name="横折")


def hengzhegou(x0, x1, y, yb, dx=-120, dy=86):
    """横折钩：横、肩、竖、钩一条轮廓。"""
    xv = x1 - V / 2
    return Shape(heng_left(x0, y) + shoulder(x1, y) + gou_end(xv, yb, dx, dy) + [n(x1 - V, y - T)],
                 name="横折钩")


def _pie_part(x1, y, p1, bend, w0):
    """横撇里那一撇：从转角出发。返回中心线、粗细。"""
    p0 = (x1 - w0 * .5, y - 6)
    return pie_seg(p0, p1, bend), _pie_width(w0, 10)


def _inner_corner(seg, wf, y):
    """撇的右手边（屏幕左上那条）和横的底边 y 的交点。"""
    t = _solve(lambda t: _edge(seg, t, wf, -1)[1], 0, 0.9, y)
    return _edge(seg, t, wf, -1), (_edge_dir(seg, t, wf, -1) + 180) % 360


def hengpie(x0, x1, y, p1, bend=(0, 0), w0=V * .98, entry=True):
    """横撇：横、肩、撇一条轮廓。肩的右侧顺着撇的外沿下去，撇的内沿在横的底边形成夹角。"""
    seg, wf = _pie_part(x1, y, p1, bend, w0)
    ic, icd = _inner_corner(seg, wf, y - T)
    return Shape(heng_left(x0, y, entry) + [
        n(x1 - 104, y + T, R), n(x1 - 32, y + T + 14, R, t=0.62),
        n(*_edge(seg, 0.04, wf, 1), _edge_dir(seg, 0.04, wf, 1)),
    ] + _pie_body(seg, wf) + [n(*ic, din=icd)], name="横撇")


def hook_down(x0, x1, y, entry=True):
    """横钩（宀 的顶）：横、顿、向左下的钩一条轮廓。"""
    tip = (x1 - 44, y - 118)
    rs = (x1 + 14, y - 10)
    ic = (x1 - 70, y - T)
    return Shape(heng_left(x0, y, entry) + [
        n(x1 - 110, y + T, R), n(x1 - 34, y + T + 14, R, t=0.62),
        n(*rs, D),
        n(*tip, din=sym_end(rs, 270, tip), dout=sym_start(tip, ic, 112), tip=True),
        n(*ic, din=112),
    ], name="横钩")


def hengpie_wangou(x0, x1, y, p1, x, yb, w0=V * .9, bow=16, dx=-120, dy=86):
    """「了」：横、肩、撇、弯钩一条轮廓。撇往左下走到竖的位置，竖从那里接着往下，底部出钩。
    x 是竖（弯钩）的中心，yb 是钩的底。"""
    seg, wf = _pie_part(x1, y, p1, (0, 0), w0)
    ic, icd = _inner_corner(seg, wf, y - T)
    l, r = x - V / 2, x + V / 2
    # 撇的外沿（屏幕右下那条）碰到竖的右边沿：凹角；撇的内沿碰到竖的左边沿：转折的尖
    tr = _solve(lambda t: _edge(seg, t, wf, 1)[0], 0.05, 1, r + bow * .3)
    tl = _solve(lambda t: _edge(seg, t, wf, -1)[0], 0.05, 1, l + bow * .3)
    jr, jl = _edge(seg, tr, wf, 1), _edge(seg, tl, wf, -1)
    tip, bottom, join = (x + dx, yb + dy), (x + 4, yb - 14), (l, yb + 160)
    # 竖的两条边各是一整条弧：上端略往右、下端略往左，整支竖微微向右鼓
    return Shape(heng_left(x0, y) + [
        n(x1 - 104, y + T, R), n(x1 - 32, y + T + 14, R, t=0.62),
        n(*_edge(seg, 0.04, wf, 1), _edge_dir(seg, 0.04, wf, 1)),
        n(*_edge(seg, tr * .5, wf, 1), _edge_dir(seg, tr * .5, wf, 1)),
        n(*jr, din=_edge_dir(seg, tr, wf, 1), dout=274),                # 撇外沿接竖右边沿
        n(r, yb + 80, 266),
        n(*bottom, L, t=0.6),
        n(*tip, din=sym_end(bottom, 180, tip), dout=sym_start(tip, join, 86), tip=True),
        n(*join, 86),
        n(*jl, din=94, dout=(_edge_dir(seg, tl, wf, -1) + 180) % 360),  # 转折的尖
        n(*_edge(seg, tl * .5, wf, -1), (_edge_dir(seg, tl * .5, wf, -1) + 180) % 360),
        n(*ic, din=icd),
    ], name="了")


# ───────── 字 ─────────

def c_yi():                    # 一
    return [heng(100, 900, 380)]


def c_shi():                   # 十
    return [heng(90, 910, 440), shu(500, 812, -66, end="needle")]


def _kou(xl, xr, yt, yb, foot=44):
    """口：左竖、横折、底横。xl/xr 是左右竖的中心；底横两端藏进竖里。"""
    return [shu(xl, yt + 40, yb - foot), hengzhe(xl, xr + V / 2, yt, yb - foot),
            heng(xl, xr, yb, beak=False, entry=None, right_hid=True)]


def c_kou():                   # 口
    return _kou(230, 770, 660, 110)


def c_ri():                    # 日
    return _kou(280, 720, 760, 10) + [heng(280, 720, 390, beak=False, entry=None, right_hid=True)]


def c_zhong():                 # 中
    return _kou(170, 830, 610, 220) + [shu(500, 852, -80, end="needle")]


def _pie_na(pie_p0, pie_p1, bend, na_y, na_p1, na_bend=(30, -10), w0=V * 1.1, wmax=V * 1.18, head="cut"):
    """撇 + 从撇身中间起笔的捺（人、大、天、美的下半部）。"""
    start = on_pie(pie_p0, pie_p1, bend, na_y)
    return [pie(pie_p0, pie_p1, bend=bend, w0=w0, head=head), na(start, na_p1, bend=na_bend, wmax=wmax)]


def c_ren():                   # 人
    return _pie_na((525, 840), (70, -50), (-20, -20), 540, (850, -10))


def c_da():                    # 大
    return [heng(80, 920, 530)] + _pie_na((505, 860), (70, -50), (10, -90), 470, (850, -10))


def c_tian():                  # 天
    return [heng(190, 810, 720), heng(80, 920, 450)] + _pie_na((505, 722), (75, -50), (10, -70), 400, (850, -10),
                                                               w0=V * 1.08, head="hid")


def c_wen():                   # 文
    return [dian((460, 890), (540, 795)), heng(80, 920, 660),
            pie((715, 660), (70, -50), bend=(-70, 40), w0=V * 1.08, head="hid"),
            na((305, 655), (850, -10), bend=(70, 10))]


def c_yan():                   # 言
    return [dian((455, 905), (540, 835)), heng(80, 920, 705), heng(210, 790, 565, beak=0.7), heng(210, 790, 430, beak=0.7)] \
        + _kou(255, 745, 280, -20)


def c_yong():                  # 永
    return [dian((470, 910), (550, 825)),
            hengzhegou(300, 592, 650, 50, dx=-130, dy=86),
            hengpie(110, 404, 490, (70, 110), bend=(-20, 10), w0=V),
            pie((830, 640), (560, 420), w0=V * .98),
            na((555, 470), (860, 20), bend=(20, -10), wmax=V * 1.25)]


def c_zi():                    # 字
    return [dian((465, 905), (540, 835)),
            dian((150, 770), (170, 640), w=V * 1.05),
            hook_down(170, 870, 705, entry=None),
            hengpie_wangou(250, 744, 545, (430, 380), 505, 30),
            heng(80, 920, 290)]


def c_mei():                   # 美
    return [dian((290, 905), (345, 832)), pie((722, 905), (652, 805), w0=V * .95, head="round"),
            heng(220, 780, 695), heng(250, 750, 590, beak=0.3), shu(500, 695, 480, top="hid", end="hid"),
            heng(140, 860, 480, beak=0.3),
            heng(80, 920, 330)] + _pie_na((505, 482), (70, -55), (10, -50), 280, (850, -15), w0=V * 1.05, head="hid")


def c_du():                    # 渡
    return [dian((85, 790), (180, 705), w=V * 1.05), dian((65, 570), (155, 485), w=V * 1.05),
            ti((60, 70), (210, 325), w0=V),
            dian((590, 915), (650, 855), w=V * 1.05), heng(362, 920, 735, entry=None),
            pie((350, 770), (215, -60), bend=(-15, -10), w0=V),
            heng(410, 912, 560, beak=0.8), nian_u(530, 735, 638, 455),
            hengpie(440, 844, 345, (410, -50), bend=(-50, -10), w0=V * .95),
            na((500, 340), (860, -20), bend=(10, -10), wmax=V * 1.15)]


def capsule(p0, p1, w0, w1, w2, bend=(0, 0)):
    """两头圆的笔画：起笔粗 w0、中段 w1、收笔 w2。"""
    seg = pie_seg(p0, p1, bend)
    wf = lambda t: (w0 * (1 - t) ** 2 + 2 * w1 * t * (1 - t) + w2 * t * t)
    d0, d1 = _ang(_tan(seg, 0)), _ang(_tan(seg, 1))
    e = lambda t, sd: _edge(seg, t, wf, sd)
    far = (p1[0] + _tan(seg, 1)[0] * w2 / 2, p1[1] + _tan(seg, 1)[1] * w2 / 2)
    back = (p0[0] - _tan(seg, 0)[0] * w0 / 2, p0[1] - _tan(seg, 0)[1] * w0 / 2)
    return Shape([
        n(*e(0, 1), d0), n(*e(.5, 1), _edge_dir(seg, .5, wf, 1)), n(*e(1, 1), d1, t=0.5523),
        n(*far, (d1 - 90) % 360, t=0.5523), n(*e(1, -1), (d1 + 180) % 360),
        n(*e(.5, -1), (_edge_dir(seg, .5, wf, -1) + 180) % 360), n(*e(0, -1), (d0 + 180) % 360, t=0.5523),
        n(*back, (d0 + 90) % 360, t=0.5523),
    ], name="斜笔")


def nian_u(xl, xr, top, y):
    """「廿」下半：两竖和底横一条 U 形轮廓。xl、xr 是两竖中心，y 是底横中线。"""
    l1, r1, l2, r2 = xl - V / 2, xl + V / 2, xr - V / 2, xr + V / 2
    return Shape(shu_top(xl, top)[:-1] + [n(r1, top - 38, D, t="line"), n(r1, y + T), n(l2, y + T, t="line")]
                 + shu_top(xr, top) + [n(r2, y - T), n(l1, y - T, t="line")], name="廿")


def c_no():                    # の
    """の：一笔写成。斜笔往左下，在底端折回往上绕一圈，收在底部的细尾。
    折回处外侧是一个干净的尖，内侧是夹角。"""
    seg = pie_seg((505, 596), (330, 104), (-6, 0))
    wf = lambda t: 44 * (1 - t) ** 2 + 2 * 84 * t * (1 - t) + 60 * t * t
    d0 = _ang(_tan(seg, 0))
    back = (505 - _tan(seg, 0)[0] * 22, 596 - _tan(seg, 0)[1] * 22)
    key = [((236, 380), 90, 92), ((500, 670), 0, 46), ((812, 380), 270, 96), ((660, 80), 208, 58)]
    def side(p, a, w, sd):
        r = math.radians(a)
        return (p[0] - math.sin(r) * w / 2 * sd, p[1] + math.cos(r) * w / 2 * sd)
    outer = [n(*side(p, a, w, 1), a) for p, a, w in key]
    inner = [n(*side(p, a, w, -1), (a + 180) % 360) for p, a, w in reversed(key)]
    v = _edge(seg, 1, wf, 1)                       # 折回处外侧的尖
    crotch = _edge(seg, 0.86, wf, -1)              # 折回处内侧的夹角
    tail = (512, 44)
    up = (_edge_dir(seg, 0.86, wf, -1) + 180) % 360
    return [Shape([
        n(*back, (d0 + 90) % 360, t=0.5523),
        n(*_edge(seg, 0, wf, 1), d0),
        n(*_edge(seg, 0.5, wf, 1), _edge_dir(seg, 0.5, wf, 1)),
        n(*v, din=_edge_dir(seg, 0.96, wf, 1), dout=sym_start(v, outer[0].xy, 90), tip=True),
    ] + outer + [
        n(*tail, din=sym_end(outer[-1].xy, 208, tail), dout=sym_start(tail, inner[0].xy, 28), tip=True),
    ] + inner[:-1] + [
        n(*inner[-1].xy, 270),
        n(*crotch, din=sym_end(inner[-1].xy, 270, crotch), dout=up),
        n(*_edge(seg, 0.4, wf, -1), (_edge_dir(seg, 0.4, wf, -1) + 180) % 360),
        n(*_edge(seg, 0, wf, -1), (d0 + 180) % 360, t=0.5523),
    ], name="の")]


def p_comma():                 # ，
    """逗号：按「点」的画法，尖尾朝左下，圆头在上。"""
    return [dian((112, -118), (166, 104), w=100)]


def p_period():                # 。
    from outline import circle
    outer = circle(170, 60, 87, name="句号")
    hole = circle(170, 60, 57, name="句号怀")
    hole.hole = True
    return [outer, hole]


GLYPHS = {"一": c_yi, "十": c_shi, "口": c_kou, "日": c_ri, "中": c_zhong, "人": c_ren, "大": c_da, "天": c_tian,
          "文": c_wen, "言": c_yan, "永": c_yong, "字": c_zi, "美": c_mei, "渡": c_du, "の": c_no,
          "，": p_comma, "。": p_period}
