"""渡言的造字方式：轮廓优先。

每个笔画（或部件）直接画成一条闭合轮廓，和在造字软件里画字一样：
在曲线的极值点（最高、最低、最左、最右）和转角处放节点，写明经过这个点时的走向；
两个节点之间的弯度用「张力」控制——控制柄长度 = 张力 × 节点到两条切线交点的距离。
张力 0.55 左右是圆弧，越大越方，越小越尖。

方向用角度：0 向右、90 向上、180 向左、270 向下（也可以写 R、U、L、D）。
坐标单位是 1/1000 em，y 轴向上，基线在 0。
"""
import math

R, U, L, D = 0, 90, 180, 270
TENSION = 0.56


def _dir(a):
    r = math.radians(a)
    return (math.cos(r), math.sin(r))


def _unit(v):
    n = math.hypot(*v) or 1
    return (v[0] / n, v[1] / n)


class Node:
    """轮廓上的一个节点。

    d：光滑点经过时的走向（进出同向）；din、dout 分开给是带方向的角点；都不给就是直线角点。
    hid：这个点应该藏在别的笔画里面（检查时会核对它有没有露出来）。
    tip：这是有意做出的尖（撇尾、捺脚尖、喙尖……）。没标 tip 的锐角，检查时会报出来。
    t：从这个点出发那一段的张力；写 "line" 表示这一段是直线。
    h：(a, b) 直接指定从这个点出发那一段两个控制柄的长度。
    """
    __slots__ = ("x", "y", "din", "dout", "hid", "tip", "t", "h")

    def __init__(self, x, y, d=None, din=None, dout=None, hid=False, tip=False, t=None, h=None):
        self.x, self.y = float(x), float(y)
        self.din = d if din is None else din
        self.dout = d if dout is None else dout
        self.hid, self.tip, self.t, self.h = hid, tip, t, h

    @property
    def xy(self):
        return (self.x, self.y)

    @property
    def corner(self):
        return self.din is None or self.dout is None or abs(((self.din - self.dout) + 180) % 360 - 180) > 1e-6

    def moved(self, dx, dy):
        return Node(self.x + dx, self.y + dy, din=self.din, dout=self.dout, hid=self.hid, tip=self.tip, t=self.t, h=self.h)

    def mirrored(self, cx):
        """左右翻转（以 x = cx 为轴）。"""
        f = lambda a: None if a is None else (180 - a) % 360
        return Node(2 * cx - self.x, self.y, din=f(self.din), dout=f(self.dout), hid=self.hid, tip=self.tip, t=self.t, h=self.h)


def n(x, y, d=None, **kw):
    return Node(x, y, d, **kw)


class Shape:
    """一条闭合轮廓。hole=True 是字怀（挖空）。"""

    def __init__(self, nodes, tension=TENSION, hole=False, name=""):
        self.nodes = nodes
        self.tension = tension
        self.hole = hole
        self.name = name

    # ── 曲线 ──
    def segments(self):
        out = []
        k = len(self.nodes)
        for i in range(k):
            a, b = self.nodes[i], self.nodes[(i + 1) % k]
            out.append(_segment(a, b, self.tension))
        return out

    def flatten(self, step=2.0):
        pts = []
        for seg in self.segments():
            if seg[0] == "line":
                pts.append(seg[1])
            else:
                _, p0, h1, h2, p1 = seg
                length = math.dist(p0, h1) + math.dist(h1, h2) + math.dist(h2, p1)
                m = max(4, int(length / step))
                pts += [_bez((p0, h1, h2, p1), i / m) for i in range(m)]
        return pts

    def area(self):
        p = self.flatten(6)
        return 0.5 * sum(p[i][0] * p[(i + 1) % len(p)][1] - p[(i + 1) % len(p)][0] * p[i][1] for i in range(len(p)))

    # ── 变换 ──
    def moved(self, dx=0, dy=0):
        return Shape([q.moved(dx, dy) for q in self.nodes], self.tension, self.hole, self.name)

    def mirrored(self, cx):
        """左右翻转。节点顺序不变，轮廓方向在输出时统一。"""
        return Shape([q.mirrored(cx) for q in self.nodes], self.tension, self.hole, self.name)

    # ── 输出 ──
    def draw(self, pen, ccw=True):
        segs = self.segments()
        if (self.area() > 0) != (ccw != self.hole):
            segs = [_reverse(s) for s in reversed(segs)]
        pen.moveTo(segs[0][1])
        for s in segs:
            if s[0] == "line":
                pen.lineTo(s[2])
            else:
                pen.curveTo(s[2], s[3], s[4])
        pen.closePath()


def _segment(a, b, tension):
    if a.t == "line" or (a.dout is None and b.din is None):
        return ("line", a.xy, b.xy)
    chord = _unit((b.x - a.x, b.y - a.y))
    u = _dir(a.dout) if a.dout is not None else chord
    v = _dir(b.din) if b.din is not None else chord
    if a.h is not None:
        la, lb = a.h
        return ("curve", a.xy, (a.x + u[0] * la, a.y + u[1] * la), (b.x - v[0] * lb, b.y - v[1] * lb), b.xy)
    k = tension if a.t is None else a.t
    dx, dy = b.x - a.x, b.y - a.y
    s, t = handle_reach(a, b, u, v)
    if s is not None:
        return ("curve", a.xy, (a.x + u[0] * s * k, a.y + u[1] * s * k), (b.x - v[0] * t * k, b.y - v[1] * t * k), b.xy)
    # 切线平行（S 形）或交点在背后：柄长按弦长取（检查器会把这种段报成「走向不顺」）
    d = math.hypot(dx, dy) * k * 0.66
    return ("curve", a.xy, (a.x + u[0] * d, a.y + u[1] * d), (b.x - v[0] * d, b.y - v[1] * d), b.xy)


def handle_reach(a, b, u, v):
    """两条切线的交点 X：a + s·u = b − t·v。交点在两点前方（s、t 都为正）时返回 (s, t)，否则 (None, None)。"""
    dx, dy = b.x - a.x, b.y - a.y
    den = u[0] * v[1] - u[1] * v[0]
    if abs(den) < 1e-6:
        return None, None
    s = (dx * v[1] - dy * v[0]) / den
    t = (u[0] * dy - u[1] * dx) / den
    L = math.hypot(dx, dy)
    if 0 < s < 4 * L and 0 < t < 4 * L:
        return s, t
    return None, None


def tangents(shape):
    """每个节点处的（进入方向, 离开方向），用实际曲线算，不用标注的方向。"""
    segs = shape.segments()
    k = len(segs)
    def start_dir(sg):
        if sg[0] == "line":
            return _unit((sg[2][0] - sg[1][0], sg[2][1] - sg[1][1]))
        p0, h1, h2, p1 = sg[1:]
        q = h1 if math.dist(p0, h1) > 1e-6 else (h2 if math.dist(p0, h2) > 1e-6 else p1)
        return _unit((q[0] - p0[0], q[1] - p0[1]))
    def end_dir(sg):
        if sg[0] == "line":
            return _unit((sg[2][0] - sg[1][0], sg[2][1] - sg[1][1]))
        p0, h1, h2, p1 = sg[1:]
        q = h2 if math.dist(p1, h2) > 1e-6 else (h1 if math.dist(p1, h1) > 1e-6 else p0)
        return _unit((p1[0] - q[0], p1[1] - q[1]))
    return [(end_dir(segs[i - 1]), start_dir(segs[i])) for i in range(k)]


def _reverse(s):
    return ("line", s[2], s[1]) if s[0] == "line" else ("curve", s[4], s[3], s[2], s[1])


def _bez(s, t):
    p0, p1, p2, p3 = s
    u = 1 - t
    return (u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0],
            u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1])


def bounds(shapes):
    xs, ys = [], []
    for s in shapes:
        for p in s.flatten(4):
            xs.append(p[0])
            ys.append(p[1])
    return min(xs), min(ys), max(xs), max(ys)


# ───────── 常用形状 ─────────

def rect(x0, y0, x1, y1, hid=(), name=""):
    """矩形；hid 里写要藏起来的角：'bl' 'br' 'tr' 'tl'。"""
    return Shape([n(x0, y0, hid="bl" in hid), n(x1, y0, hid="br" in hid), n(x1, y1, hid="tr" in hid),
                  n(x0, y1, hid="tl" in hid)], name=name)


def ellipse(cx, cy, rx, ry, tension=0.5523, hole=False, name=""):
    return Shape([n(cx + rx, cy, U), n(cx, cy + ry, L), n(cx - rx, cy, D), n(cx, cy - ry, R)],
                 tension, hole, name)


def circle(cx, cy, r, name=""):
    return ellipse(cx, cy, r, r, name=name)
