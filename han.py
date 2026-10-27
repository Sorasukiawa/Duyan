"""渡言的汉字：轮廓优先，宋体笔法。

字身框 1000 × 1000（y 从 -120 到 880）。字在「设计坐标」里画，出字体时 glyphs.collect 把整字纵向压扁、
中心移到字身中心（layout.HAN_SY、HAN_CY），字面框见 layout.FACE，说明见 docs/STRUCTURE.md「字面」。
竖画 104、横画 60（出字体后的粗细），和西文同一套粗细。
每一笔（连笔也算一笔）画成一条闭合轮廓，都按顺时针写（墨在走向的右边）：
横折、横撇、横钩、横折钩、「了」的横撇连弯钩，转角处的肩直接画在轮廓里；
不相连的笔画在笔画深处交叉，要藏起来的端点标 hid，有意的尖标 tip。
"""
import math
from contextlib import contextmanager

from outline import D, L, R, U, Node, Shape, n

V0, H0 = 104, 60            # 标准粗细（出字体后）
V, H = V0, H0               # 当前粗细（笔画多的字用 weight() 临时调细）
T = H / 2
_SY = 1.0                   # 正在画的字出字体时纵向压扁的比例：横画先按 1/_SY 加粗，压完正好是标准粗细
_used = None                # 正在画的字用过哪些 weight()（drawing() 里记，结构检查核对减细档位）


@contextmanager
def weight(kv=1.0, kh=None):
    """临时调整竖画、横画的粗细：with weight(0.92): ... 里面画的笔画都按这个比例。"""
    global V, H, T
    old = V, H, T
    V, H = V0 * kv, H0 * (kv if kh is None else kh) / _SY
    T = H / 2
    if _used is not None:
        _used.append(kv)
    try:
        yield
    finally:
        V, H, T = old


@contextmanager
def drawing(sy=1.0):
    """画一个汉字：sy 是这个字出字体时纵向压扁的比例。with drawing(sy) as used: ... 之后，
    used 里是这个字用过的 weight() 档位。"""
    global V, H, T, _SY, _used
    old = V, H, T, _SY, _used
    _SY, _used = sy, []
    V, H = V0, H0 / sy
    T = H / 2
    try:
        yield _used
    finally:
        V, H, T, _SY, _used = old


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


def tilted(shape, deg, cx, cy):
    """把一条轮廓绕 (cx, cy) 转 deg 度：七、代 的横是斜着往上写的。"""
    a = math.radians(deg)
    c, s = math.cos(a), math.sin(a)
    r = lambda d: None if d is None else (d + deg) % 360
    return Shape([Node(cx + (q.x - cx) * c - (q.y - cy) * s, cy + (q.x - cx) * s + (q.y - cy) * c,
                       din=r(q.din), dout=r(q.dout), hid=q.hid, tip=q.tip, t=q.t, h=q.h) for q in shape.nodes],
                 shape.tension, shape.hole, shape.name)


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


def shu_top(x, y0, kind="head", w=None):
    """竖的顶：沿左边沿往上进来，沿右边沿往下出去。head 是左高右低的斜切加圆肩。"""
    w = V if w is None else w
    l, r = x - w / 2, x + w / 2
    if kind == "head":
        return [n(l, y0 + 16), n(r - 20, y0 - 2, -12), n(r, y0 - 38, D, t="line")]
    hid = kind == "hid"
    return [n(l, y0, hid=hid), n(r, y0, hid=hid, t="line")]


def shu_end(x, y1, kind="dew", w=None):
    """竖的底：沿右边沿往下进来，沿左边沿往上出去。dew 垂露，needle 悬针。"""
    w = V if w is None else w
    l, r = x - w / 2, x + w / 2
    if kind == "dew":
        return [n(r, y1 + 34, D), n(x + 2, y1 - 10, L, t=0.6), n(l, y1 + 26, U, t="line")]
    if kind == "needle":
        return [n(r, y1 + 230, D, t=0.5), n(x + 2, y1, din=250, dout=110, tip=True, t=0.5), n(l, y1 + 230, U, t="line")]
    hid = kind == "hid"
    return [n(r, y1, hid=hid), n(l, y1, hid=hid, t="line")]


def gou_end(x, y, dx=-120, dy=86, w=None):
    """竖钩的底：右边沿圆转到底，向左上挑出尖，钩的上沿顺着弯回竖的左边沿。"""
    w = V if w is None else w
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


def pie(p0, p1, bend=(0, 0), w0=None, w1=10, head="cut", seg=None):
    """撇：粗起细收。head：cut（左高右低斜切、右角圆）、hid（藏进别的笔画）、round（圆头）。
    seg 可以直接给中心线（竖撇这种先直后弯的用）。"""
    w0 = V * 1.02 if w0 is None else w0
    seg = pie_seg(p0, p1, bend) if seg is None else seg
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
    else:                                                   # hid：藏进别的笔画；flat：露在外面的平头
        hid = head != "flat"
        start = [n(*a, din=up0, hid=hid), n(*b, dout=_edge_dir(seg, 0, wf, 1), hid=hid)]
    return Shape(start + body, name="撇")


def na(p0, p1, bend=(30, -10), wmax=None, w0=30, foot=0.62, start="hid"):
    """捺：起笔藏进别的笔画（平头、hid），越写越粗，末端平出捺脚：上沿凹下去接到尖，底边平。"""
    wmax = V * 1.18 if wmax is None else wmax
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
    if start == "tip":                                    # 尖头起笔：两条边在起点收成一个尖
        d0 = _tan(seg, 0)
        tp = (p0[0] - d0[0] * 6, p0[1] - d0[1] * 6)
        head = [n(*tp, din=(_edge_dir(seg, 0.05, wf, -1) + 180) % 360, dout=_edge_dir(seg, 0.05, wf, 1), tip=True)]
        tail = []
    else:
        head = [n(*s_l, _edge_dir(seg, 0, wf, 1), hid=True)]
        tail = [n(*s_r, (_edge_dir(seg, 0, wf, -1) + 180) % 360, hid=True, t="line")]
    return Shape(head + _side(seg, wf, (0.3, 0.6), 1) + [
        n(*top_end, d_top),
        n(*tip, din=sym_end(top_end, d_top, tip), dout=180, tip=True),
        n(bot[0] + 6, bot[1], 180),
    ] + _side(seg, wf, (0.3, 0.64), -1) + tail, name="捺")


def dian(p0, p1, w=None):
    """点：尖头入笔，圆头收笔（对应西文的球形收笔）。"""
    w = V * 1.2 if w is None else w
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


def ti(p0, p1, w0=None):
    """提：圆头起笔，向右上挑出尖。"""
    w0 = V * 1.08 if w0 is None else w0
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


def hengpie(x0, x1, y, p1, bend=(0, 0), w0=None, entry=True):
    """横撇：横、肩、撇一条轮廓。肩的右侧顺着撇的外沿下去，撇的内沿在横的底边形成夹角。"""
    w0 = V * .98 if w0 is None else w0
    seg, wf = _pie_part(x1, y, p1, bend, w0)
    ic, icd = _inner_corner(seg, wf, y - T)
    return Shape(heng_left(x0, y, entry) + [
        n(x1 - 104, y + T, R), n(x1 - 32, y + T + 14, R, t=0.62),
        n(*_edge(seg, 0.04, wf, 1), _edge_dir(seg, 0.04, wf, 1)),
    ] + _pie_body(seg, wf) + [n(*ic, din=icd)], name="横撇")


def hengzhezhepie(x0, x1, y, p_mid, x2, p_end, w0=None, w2=None, bend1=(0, 0), bend2=(-20, 0), entry=True):
    """横折折撇（辶 中间那一笔，像个「3」的上半截接一撇）：横、肩、撇、短横、肩、撇一条轮廓。
    x1 是第一撇起笔处的右边沿，p_mid 是第一撇中心线的终点（要比短横底边再低一点），
    短横的中线高度取 p_mid 上方 T + 20，x2 是第二撇起笔处的右边沿，p_end 是第二撇的尖。"""
    w0 = V * .8 if w0 is None else w0
    w2 = V * .86 if w2 is None else w2
    seg1, wf1 = _pie_part(x1, y, p_mid, bend1, w0)
    wf1 = _pie_width(w0, H * .7)
    y2 = p_mid[1] + T + 20
    seg2, wf2 = _pie_part(x2, y2, p_end, bend2, w2)
    j0, j0d = _inner_corner(seg1, wf1, y - T)                         # 第一撇和上横底边的夹角
    tj = _solve(lambda t: _edge(seg1, t, wf1, 1)[1], 0, 1, y2 + T)  # 第一撇外沿碰到短横顶边：凹角
    tc = _solve(lambda t: _edge(seg1, t, wf1, -1)[1], 0, 1, y2 - T)  # 第一撇内沿碰到短横底边：左下的转角
    j1, c = _edge(seg1, tj, wf1, 1), _edge(seg1, tc, wf1, -1)
    j2, j2d = _inner_corner(seg2, wf2, y2 - T)
    # 短横露出来的一截很短：肩只留一个微微隆起的点，太短就不要
    bump = [n(x2 - 22, y2 + T + 4, R, t=0.6)] if x2 - 22 > j1[0] + 10 else []
    # 有肩时，凹角出去就是短横的顶边，往右走（不写的话这一小段会顺着弦斜着进肩，肩上留一个小拐）
    j1n = n(*j1, din=_edge_dir(seg1, tj, wf1, 1), dout=R if bump else None)
    return Shape(heng_left(x0, y, entry) + [
        n(x1 - 104, y + T, R), n(x1 - 32, y + T + 14, R, t=0.62),
        n(*_edge(seg1, 0.04, wf1, 1), _edge_dir(seg1, 0.04, wf1, 1)),
        n(*_edge(seg1, tj * .5, wf1, 1), _edge_dir(seg1, tj * .5, wf1, 1)),
        j1n,
    ] + bump + [
        n(*_edge(seg2, 0.04, wf2, 1), _edge_dir(seg2, 0.04, wf2, 1)),
    ] + _pie_body(seg2, wf2) + [
        n(*j2, din=j2d),
        n(*c, dout=(_edge_dir(seg1, tc, wf1, -1) + 180) % 360, tip=True),   # 左边转折的尖
        n(*_edge(seg1, tc * .5, wf1, -1), (_edge_dir(seg1, tc * .5, wf1, -1) + 180) % 360),
        n(*j0, din=j0d),
    ], name="横折折撇")


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


def hengpie_wangou(x0, x1, y, p1, x, yb, w0=None, bow=16, dx=-120, dy=86, entry=True):
    """「了」：横、肩、撇、弯钩一条轮廓。撇往左下走到竖的位置，竖从那里接着往下，底部出钩。
    x 是竖（弯钩）的中心，yb 是钩的底。"""
    w0 = V * .9 if w0 is None else w0
    seg, wf = _pie_part(x1, y, p1, (0, 0), w0)
    ic, icd = _inner_corner(seg, wf, y - T)
    l, r = x - V / 2, x + V / 2
    # 撇的外沿（屏幕右下那条）碰到竖的右边沿：凹角；撇的内沿碰到竖的左边沿：转折的尖
    tr = _solve(lambda t: _edge(seg, t, wf, 1)[0], 0.05, 1, r + bow * .3)
    tl = _solve(lambda t: _edge(seg, t, wf, -1)[0], 0.05, 1, l + bow * .3)
    jr, jl = _edge(seg, tr, wf, 1), _edge(seg, tl, wf, -1)
    tip, bottom, join = (x + dx, yb + dy), (x + 4, yb - 14), (l, yb + 160)
    # 竖的两条边各是一整条弧：上端略往右、下端略往左，整支竖微微向右鼓
    return Shape(heng_left(x0, y, entry) + [
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


# ───────── 扩字用的笔形 ─────────

def _lineint(a0, a1, b0, b1):
    """两条直线（各用两点给出）的交点。"""
    (x1, y1), (x2, y2), (x3, y3), (x4, y4) = a0, a1, b0, b1
    d = (x1 - x2) * (y3 - y4) - (y1 - y2) * (x3 - x4)
    a = x1 * y2 - y1 * x2
    b = x3 * y4 - y3 * x4
    return ((a * (x3 - x4) - (x1 - x2) * b) / d, (a * (y3 - y4) - (y1 - y2) * b) / d)


def _off(p, nrm, k):
    return (p[0] + nrm[0] * k, p[1] + nrm[1] * k)


def shugou(x, y0, yb, top="head", dx=-110, dy=80):
    """竖钩（亅、寸、小、可 里的那一笔）。"""
    return Shape(shu_top(x, y0, top) + gou_end(x, yb, dx, dy), name="竖钩")


def wangou(x, y0, yb, bow=8, dx=-110, dy=80, top="hid", y0r=None):
    """弯钩（豕、家、象 的那一笔）：竖往下、整支微微向右鼓（bow 是两端偏离竖直的角度），底部向左挑出钩。
    写法同「了」下半截的弯钩：两条边各是一整条弧，钩同竖钩。从斜笔上起笔时顶边跟着斜：y0、y0r 是顶边左右两端的高度。"""
    l, r = x - V / 2, x + V / 2
    tip, bottom, join = (x + dx, yb + dy), (x + 4, yb - 14), (l, yb + 160)
    hid = top == "hid"
    return Shape([n(l, y0, din=90 + bow, hid=hid), n(r, y0 if y0r is None else y0r, dout=270 + bow, hid=hid),
                  n(r, yb + 80, 270 - bow),
                  n(*bottom, L, t=0.6),
                  n(*tip, din=sym_end(bottom, 180, tip), dout=sym_start(tip, join, 90 - bow), tip=True),
                  n(*join, 90 - bow)], name="弯钩")


def shuzhe(x, y0, yb, x1, top="head", right="flat"):
    """竖折（山、出、世 的那一笔）：竖往下，在底部直角转向右成一横。yb 是那一横的中线，x1 是它的右端。
    right：flat 平收，hid 藏进别的笔画，beak 末端带喙（世）。"""
    l, r = x - V / 2, x + V / 2
    if right == "beak":
        end = heng_right(x, x1, yb)
    else:
        end = [n(x1, yb + T, hid=right == "hid"), n(x1, yb - T, hid=right == "hid", t="line")]
    return Shape(shu_top(x, y0, top) + [n(r, yb + T)] + end + [n(l + 10, yb - T), n(l, yb - T + 14, t="line")],
                 name="竖折")


def shuzhezhegou(x, y0, y1, x1, yb, dx=-110, dy=80, top="head"):
    """竖折折钩（与、写 里那一笔）：竖往下，转成一横往右，再折下来成竖钩。
    y1 是那一横的中线，x1 是竖钩的右边沿，yb 是钩的底。"""
    l, r = x - V / 2, x + V / 2
    return Shape(shu_top(x, y0, top) + [n(r, y1 + T)] + shoulder(x1, y1) + gou_end(x1 - V / 2, yb, dx, dy)
                 + [n(x1 - V, y1 - T), n(l + 10, y1 - T), n(l, y1 - T + 14, t="line")], name="竖折折钩")


def shuwangou(x, y0, yb, x1, top="head", hook=74, r_in=64, wb=None):
    """竖弯钩（也、乚、儿 的那一笔）：竖往下，圆转向右成一条底横，末端向上挑出钩。yb 是底横的底边。"""
    wb = H * 1.3 if wb is None else wb
    l, r = x - V / 2, x + V / 2
    ty = yb + wb
    tip = (x1 - 8, ty + hook)
    a = (x1 - 44, ty)
    b = (x1 + 6, yb + 12)
    return Shape(shu_top(x, y0, top) + [
        n(r, ty + r_in, D),                                    # 右边沿往下，开始转弯
        n(r + r_in, ty, R, t="line"),                          # 转成底横的上沿
        n(*a, R),
        n(*tip, din=74, dout=sym_start(tip, b, 270), tip=True),
        n(*b, D),
        n(x1 - 24, yb, L, t="line"),
        n(l + 84, yb, L),
        n(l, yb + 84, U, t="line"),
    ], name="竖弯钩")


def shuwan(x, y0, yb, x1, top="hid", r_in=50, r_out=70, wb=None, tick=28):
    """竖弯（四、西 里那一笔）：竖往下，圆转向右成一条底横，末端微微上翘，不出钩。yb 是底横的底边，x1 是右端。"""
    wb = H * 1.25 if wb is None else wb
    l, r = x - V / 2, x + V / 2
    ty = yb + wb
    a = (x1 - 50, ty)
    tip = (x1, ty + tick)
    b = (x1 + 6, yb + 14)
    return Shape(shu_top(x, y0, top) + [
        n(r, ty + r_in, D),
        n(r + r_in, ty, R, t="line"),
        n(*a, R),
        n(*tip, din=sym_end(a, 0, tip), dout=sym_start(tip, b, 270), tip=True),
        n(*b, D),
        n(x1 - 24, yb, L, t="line"),
        n(l + r_out, yb, L),
        n(l, yb + r_out, U, t="line"),
    ], name="竖弯")


def wogou(x0, y0, xb, yb, x1, y1, wb=None, lean=290):
    """卧钩（心 的那一笔）：左上细起，先往下、再兜到右边，底部最粗，右端向左上挑出钩。
    (x0, y0) 起笔尖；yb 是弧的外沿最低处，xb 是那一点的 x；(x1, y1) 是右端外沿。"""
    wb = V * 0.92 if wb is None else wb
    ym = (y0 + yb) / 2
    s0 = (x0, y0)
    lx = x0 + (xb - x0) * 0.32
    il = (lx + 34, ym, lean)                                   # 内沿左（往右下走）
    ib = (xb + 40, yb + wb)                                    # 内沿最低处
    root = (x1 - 66, y1 + 34)                                  # 钩根（内侧夹角）
    hk = (x1 - 92, y1 + 118)                                   # 钩尖
    o1 = (x1 + 6, y1 - 6)                                      # 右端外沿
    ob = (xb, yb)                                              # 外沿最低处
    ol = (lx - 30, ym - 30)                                    # 外沿左
    return Shape([
        n(*s0, din=sym_end(ol, (lean + 180) % 360, s0), dout=sym_start(s0, il[:2], il[2]), tip=True),
        n(*il[:2], il[2]),
        n(*ib, R),
        n(*root, din=sym_end(ib, 0, root), dout=118),
        n(*hk, din=118, dout=sym_start(hk, o1, 270), tip=True),
        n(*o1, D, t=0.6),
        n(*ob, L, t=0.6),
        n(*ol, (lean + 180) % 360),
    ], name="卧钩")


def piezhe(p0, p1, p2, w=None, head="cut", end="tip"):
    """撇折（厶、纟、云 的那一笔）：撇往左下到 p1，折回成提往右上，到 p2 收尖。
    end="flat" 时后半截是一横（东 的那一笔）：粗细按横画，末端平收；end="beak" 时这一横末端带喙（发 的第一笔）。"""
    w = V * 0.8 if w is None else w
    d1 = _unit((p1[0] - p0[0], p1[1] - p0[1]))
    n1 = (-d1[1], d1[0])                                       # 撇的左手边（屏幕右下）
    d2 = _unit((p2[0] - p1[0], p2[1] - p1[1]))
    n2 = (-d2[1], d2[0])                                       # 提的左手边（屏幕左上）
    a0, a1 = _off(p0, n1, w / 2), _off(p1, n1, w / 2)          # 撇右下沿
    b0, b1 = _off(p0, n1, -w / 2), _off(p1, n1, -w / 2)        # 撇左上沿
    c0 = _off(p1, n2, w / 2)                                   # 提上沿起点
    e0 = _off(p1, n2, -w / 2)                                  # 提下沿起点
    top = [n(b0[0], b0[1] + (8 if head == "cut" else 0), hid=head == "hid"), n(*a0, hid=head == "hid")]
    if end in ("flat", "beak"):
        c0, e0 = _off(p1, n2, T), _off(p1, n2, -T)
        ic = _lineint(a0, a1, c0, (c0[0] + d2[0], c0[1] + d2[1]))
        oc = _lineint(b0, b1, e0, (e0[0] + d2[0], e0[1] + d2[1]))
        if end == "beak":
            return Shape(top + [n(*ic)] + heng_right(ic[0], p2[0], p2[1]) + [n(*oc, tip=True)], name="撇折")
        return Shape(top + [n(*ic), n(*_off(p2, n2, T)), n(*_off(p2, n2, -T), t="line"), n(*oc, tip=True)], name="撇折")
    ic = _lineint(a0, a1, c0, p2)                              # 里面的夹角
    oc = _lineint(b0, b1, e0, p2)                              # 外面的尖角
    return Shape(top + [n(*ic), n(*p2, tip=True), n(*oc, tip=True)], name="撇折")


def piedian(p0, p1, p2, w=None, wd=None):
    """撇点（女 的第一笔）：撇往左下到 p1，折回成点往右下到 p2，点的末端是圆头。"""
    w = V * 0.82 if w is None else w
    wd = V * 1.08 if wd is None else wd
    d1 = _unit((p1[0] - p0[0], p1[1] - p0[1]))
    n1 = (-d1[1], d1[0])
    d2 = _unit((p2[0] - p1[0], p2[1] - p1[1]))
    n2 = (-d2[1], d2[0])                                       # 点的左手边（屏幕右上）
    a0, a1 = _off(p0, n1, w / 2), _off(p1, n1, w / 2)
    b0, b1 = _off(p0, n1, -w / 2), _off(p1, n1, -w / 2)
    cu0, cu1 = _off(p1, n2, w / 2), _off(p2, n2, wd / 2)       # 点的上沿
    cl0, cl1 = _off(p1, n2, -w / 2), _off(p2, n2, -wd / 2)     # 点的下沿
    ic = _lineint(a0, a1, cu0, cu1)
    oc = _lineint(b0, b1, cl0, cl1)
    da = _ang(d2)
    far = _off(p2, d2, wd / 2)
    return Shape([
        n(b0[0], b0[1] + 8), n(*a0), n(*ic),
        n(*cu1, da, t=0.5523), n(*far, (da - 90) % 360, t=0.5523), n(*cl1, (da + 180) % 360, t="line"),
        n(*oc, tip=True),
    ], name="撇点")


def hengzheti(x0, x1, y, yb, p2, entry=True):
    """横折提（讠 的第二笔）：短横、肩、竖往下，底部折成提往右上收尖。x1 是竖的右边沿，yb 是竖的底（提的起点）。"""
    l = x1 - V
    oc = (l, yb - V * 0.22)                                    # 竖的左下角，提的下沿从这里出发
    k = (p2[1] - oc[1]) / (p2[0] - oc[0])                      # 提下沿的斜率
    ic = (x1, oc[1] + V * k + V * 0.62)                        # 竖右边沿和提上沿的夹角：留出提根部的厚度
    return Shape(heng_left(x0, y, entry) + shoulder(x1, y) + [n(*ic), n(*p2, tip=True), n(*oc, tip=True), n(l, y - T)],
                 name="横折提")


def hengzhe_heng(x0, x1, y, y2, x2, entry=True):
    """横折再往左折成一横（己、已、巳 的上半，像一个开口朝左的「コ」）：一条轮廓。
    x1 是竖的右边沿，y2 是下面那一横的中线，x2 是它的左端。"""
    l = x1 - V
    return Shape(heng_left(x0, y, entry) + shoulder(x1, y) + [
        n(x1, y2 - T), n(x2, y2 - T), n(x2, y2 + T), n(l, y2 + T), n(l, y - T),
    ], name="横折横")


def shupie_hengzhegou(x, y, x1, yb, x_tail, y_tail, w0=None, dx=-110, dy=80, bars=()):
    """月、用 的外框：左边的竖撇和上面的横折钩画成一条轮廓。x 是竖撇顶部中线，y 是顶上那一横的中线，
    x1 是右边竖的右边沿，yb 是钩的底，(x_tail, y_tail) 是竖撇的尾尖。

    bars 是框里短横的中线高度（从上往下）。短横也并进这条轮廓，横与横之间的空当挖成字怀：
    系统渲染（CoreText）遇到一笔被另一条轮廓两头穿过时，会把重叠处画成镂空，所以框里的横不能叠着画。"""
    w0 = V if w0 is None else w0
    top = y + T
    seg = ((x, top), (x, top - (top - y_tail) * 0.55), (x - 6, y_tail + (top - y_tail) * 0.16), (x_tail, y_tail))
    wf = _pie_width(w0, 10)
    tip = _bz(seg, 1)
    td = _tan(seg, 1)
    tip = (tip[0] + td[0] * 3, tip[1] + td[1] * 3)
    xi = x1 - V                                   # 右边竖的内沿
    down = lambda t: _edge_dir(seg, t, wf, 1)     # 竖撇右边沿往下走的方向
    at = lambda yy: _solve(lambda t: _edge(seg, t, wf, 1)[1], 0, 0.95, yy)
    # 竖撇左边沿（往上走）、右边沿（往下走）；右边沿从最下面那一横的底边开始
    left = [n(*_edge(seg, t, wf, -1), (_edge_dir(seg, t, wf, -1) + 180) % 360) for t in (0.7, 0.36)]
    ylo = bars[-1] - H / 2 if bars else y - T
    t0 = at(ylo)
    right = [n(*_edge(seg, t, wf, 1), down(t)) for t in (0.36, 0.7) if t > t0 + 0.04]
    xv = x1 - V / 2
    outer = Shape([n(*tip, din=_edge_dir(seg, 0.97, wf, 1), dout=(_edge_dir(seg, 0.97, wf, -1) + 180) % 360, tip=True)]
                  + left + [n(x - w0 / 2, top, din=90)] + shoulder(x1, y) + gou_end(xv, yb, dx, dy)
                  + [n(xi, ylo), n(*_edge(seg, t0, wf, 1), dout=down(t0))] + right,
                  name="竖撇横折钩")
    holes = []
    uppers = [y - T] + [b - H / 2 for b in bars[:-1]]
    for ya, b in zip(uppers, bars):
        ta, tb = at(ya), at(b + H / 2)
        holes.append(Shape([n(xi, ya), n(xi, b + H / 2), n(*_edge(seg, tb, wf, 1), dout=(down(tb) + 180) % 360),
                            n(*_edge(seg, ta, wf, 1), din=(down(ta) + 180) % 360)], hole=True, name="字怀"))
    return [outer] + holes


def shupie(x, y0, x1, y1, w0=None, head="flat"):
    """竖撇（月、用、几 的左边那一笔）：先直着往下，再弯向左下收尖。"""
    seg = ((x, y0), (x, y0 - (y0 - y1) * 0.55), (x - 6, y1 + (y0 - y1) * 0.16), (x1, y1))
    return pie((x, y0), (x1, y1), w0=V if w0 is None else w0, head=head, seg=seg)


def shuti(x, y0, yb, p2, top="head", w=None):
    """竖提（以、长、民、比 的那一笔）：竖往下，底部折成提往右上收尖。yb 是竖的底（提的起点），p2 是提的尖。
    折法和 讠 的横折提一样：竖的左下角是外面的尖，竖的右边沿和提的上沿夹出里面的角。"""
    w = V if w is None else w
    l, r = x - w / 2, x + w / 2
    oc = (l, yb - w * 0.22)
    k = (p2[1] - oc[1]) / (p2[0] - oc[0])
    ic = (r, oc[1] + w * k + w * 0.62)
    return Shape(shu_top(x, y0, top, w) + [n(*ic), n(*p2, tip=True), n(*oc, tip=True)], name="竖提")


def xiegou(p0, p1, end=305, w0=None, w1=None, top="head", hook=(24, 130), tc=0.9, base=0.62, name="斜钩"):
    """斜钩（戈、我、成、民 的那一笔）：竖着起笔，越往下越向右斜（end 是收笔处的走向），底部向上挑出钩。
    p0 是起笔中心，p1 是笔画末端中心。钩从右上沿上的钩根（中心线 tc 处）往上挑，钩尖在钩根 + hook；
    base 是钩脚的宽（按笔宽算）。整笔一条轮廓：
    右上沿往下走到钩根，沿钩的里沿上到尖，沿外沿下来兜过底，再沿左下沿回到起笔。
    top 是 head（竖的头）、hid（藏进别的笔画），或者 (起笔节点, 收尾节点)：横斜钩用它接上横和肩。"""
    w0 = V * 0.86 if w0 is None else w0
    w1 = V * 0.96 if w1 is None else w1
    L = math.dist(p0, p1)
    e = math.radians(end)
    seg = (p0, (p0[0], p0[1] - L * 0.4), (p1[0] - math.cos(e) * L * 0.3, p1[1] - math.sin(e) * L * 0.3), p1)
    wf = lambda t: w0 + (w1 - w0) * t
    l, r = p0[0] - w0 / 2, p0[0] + w0 / 2
    if top == "head":
        head, tail = [n(l, p0[1] + 16, din=U), n(r - 20, p0[1] - 2, -12), n(r, p0[1] - 38, D)], []
    elif top == "hid":
        head, tail = [n(l, p0[1], din=U, hid=True), n(r, p0[1], dout=D, hid=True)], []
    else:
        head, tail = top
    root = _edge(seg, tc, wf, 1)                                   # 钩根：右上沿上的内侧夹角
    tip = (root[0] + hook[0], root[1] + hook[1])
    out = (root[0] + w1 * base, p1[1] + 6)                         # 钩的外沿往下到这里
    bot = (p1[0] + 6, p1[1] - wf(1) * 0.44)                        # 兜底最低处
    up = _ang(hook) + 10                                           # 钩的里沿微微内凹
    back = _side(seg, wf, (0.2, 0.55, 0.86), -1)                   # 左下沿，倒着往上走
    return Shape(head + _side(seg, wf, (0.3, 0.62), 1) + [
        n(*root, din=_edge_dir(seg, tc, wf, 1), dout=up),
        n(*tip, din=sym_end(root, up, tip), dout=sym_start(tip, out, 268), tip=True),
        n(*out, 268, t=0.6),
        n(*bot, sym_start(bot, back[0].xy, back[0].din)),
    ] + back + tail, name=name)


def hengxiegou(x0, x1, y, p1, end=305, w0=None, entry=True, **kw):
    """横斜钩（气、风、飞 的那一笔）：横、肩，再往下写成斜钩。x1 是往下那一笔顶上的右边沿，p1 是它的末端中心。"""
    w0 = V * 0.86 if w0 is None else w0
    head = heng_left(x0, y, entry) + [n(x1 - w0 - 14, y + T, R), n(x1 - 26, y + T + 16, R, t=0.62), n(x1, y - 34, D)]
    return xiegou((x1 - w0 / 2, y), p1, end=end, w0=w0, top=(head, [n(x1 - w0, y - T)]), name="横斜钩", **kw)


def hengzhewangou(x0, x1, y, yb, x2, lean=0, hook=74, r_in=64, r_out=84, wb=None, entry=True):
    """横折弯钩（几、九、机 的那一笔）：横、肩、竖往下（lean 是竖底往左偏多少），圆转向右成一条底横，末端向上挑出钩。
    x1 是竖顶的右边沿，yb 是底横的底边，x2 是钩的右端。转弯和钩的画法同竖弯钩。"""
    wb = H * 1.3 if wb is None else wb
    ty = yb + wb
    rb = x1 - lean                                                 # 竖底的右边沿
    dv = _ang((rb - x1, ty + r_in - (y - 34)))                     # 竖往下的走向
    lb = rb - V
    tip = (x2 - 8, ty + hook)
    a = (x2 - 44, ty)
    b = (x2 + 6, yb + 12)
    return Shape(heng_left(x0, y, entry) + [
        n(x1 - V - 14, y + T, R), n(x1 - 26, y + T + 16, R, t=0.62), n(x1, y - 34, dv, t="line"),
        n(rb, ty + r_in, dv),
        n(rb + r_in, ty, R, t="line"),
        n(*a, R),
        n(*tip, din=74, dout=sym_start(tip, b, 270), tip=True),
        n(*b, D),
        n(x2 - 24, yb, L, t="line"),
        n(lb + r_out, yb, L),
        n(lb, yb + r_out, (dv + 180) % 360, t="line"),
        n(x1 - V, y - T),
    ], name="横折弯钩")


# ───────── 字 ─────────

def c_yi():                    # 一
    return [heng(56, 944, 380)]


def c_shi():                   # 十
    return [heng(62, 938, 440), shu(500, 812, -66, end="needle")]


def _kou(xl, xr, yt, yb, foot=44):
    """口：左竖、横折、底横。xl/xr 是左右竖的中心；底横两端藏进竖里。"""
    return [shu(xl, yt + 40, yb - foot), hengzhe(xl, xr + V / 2, yt, yb - foot),
            heng(xl, xr, yb, beak=False, entry=None, right_hid=True)]


def c_kou():                   # 口
    return _kou(222, 778, 716, 22)


def c_ri():                    # 日
    return _kou(258, 742, 770, 0) + [heng(258, 742, 390, beak=False, entry=None, right_hid=True)]


def c_zhong():                 # 中
    return _kou(170, 830, 610, 220) + [shu(500, 852, -80, end="needle")]


def _pie_na(pie_p0, pie_p1, bend, na_y, na_p1, na_bend=(30, -10), w0=None, wmax=None, head="cut"):
    """撇 + 从撇身中间起笔的捺（人、大、天、美的下半部）。"""
    w0 = V * 1.1 if w0 is None else w0
    start = on_pie(pie_p0, pie_p1, bend, na_y)
    return [pie(pie_p0, pie_p1, bend=bend, w0=w0, head=head), na(start, na_p1, bend=na_bend, wmax=wmax)]


def c_ren():                   # 人
    return _pie_na((525, 840), (70, -50), (-20, -20), 540, (850, -10))


def c_da():                    # 大
    return [heng(56, 944, 530)] + _pie_na((505, 860), (70, -50), (10, -90), 470, (850, -10))


def c_tian():                  # 天
    return [heng(190, 810, 720), heng(56, 944, 450)] + _pie_na((505, 722), (75, -50), (10, -70), 400, (850, -10),
                                                               w0=V * 1.08, head="hid")


def c_wen():                   # 文
    return [dian((460, 890), (540, 795)), heng(56, 944, 660),
            pie((715, 660), (70, -50), bend=(-70, 40), w0=V * 1.08, head="hid"),
            na((305, 655), (842, -10), bend=(70, 10))]


def c_yan():                   # 言
    with weight(0.9):
        return [dian((455, 905), (540, 835)), heng(56, 944, 705), heng(210, 790, 565, beak=0.7), heng(210, 790, 430, beak=0.7)] \
            + _kou(255, 745, 280, -20)


def c_yong():                  # 永
    return [dian((470, 910), (550, 825)),
            hengzhegou(300, 592, 650, 50, dx=-130, dy=86),
            hengpie(110, 404, 490, (70, 110), bend=(-20, 10), w0=V),
            pie((830, 640), (560, 420), w0=V * .98),
            na((555, 470), (838, 20), bend=(20, -10), wmax=V * 1.25)]


def c_zi():                    # 字
    return [dian((465, 905), (540, 839)),
            dian((150, 770), (170, 640), w=V * 1.05),
            hook_down(170, 870, 705, entry=None),
            hengpie_wangou(250, 744, 545, (430, 380), 505, 30),
            heng(56, 944, 290)]


def c_mei():                   # 美
    with weight(0.9):
        return [dian((290, 905), (345, 832)), pie((722, 905), (652, 805), w0=V * .95, head="round"),
                heng(220, 780, 695), heng(250, 750, 590, beak=0.3), shu(500, 695, 480, top="hid", end="hid"),
                heng(140, 860, 480, beak=0.3),
                heng(56, 944, 330)] + _pie_na((505, 482), (70, -55), (10, -50), 280, (850, -15), w0=V * 1.05, head="hid")


def c_du():                    # 渡
    with weight(0.88):
        return [dian((85, 790), (180, 705), w=V * 1.05), dian((65, 570), (155, 485), w=V * 1.05),
                ti((88, 70), (214, 312), w0=V),
                dian((590, 915), (650, 855), w=V * 1.05), heng(362, 920, 735, entry=None),
                pie((350, 770), (215, -60), bend=(-15, -10), w0=V),
                heng(410, 912, 560, beak=0.8), nian_u(530, 735, 638, 455),
                # 又：撇先往下再向左下扫出去，捺先陡后平、尾巴拖长，两笔都带弧度，不是直直的一个叉
                hengpie(440, 844, 345, (345, -58), bend=(90, -40), w0=V * .95),
                na((500, 340), (850, -28), bend=(-60, -50), wmax=V * 1.2, foot=0.75)]


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
