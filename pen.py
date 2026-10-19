"""一支笔：沿中心线扫出有粗细变化的笔画轮廓。中文、英文都用这支笔写。

坐标单位是 1/1000 em，y 轴向上，基线在 0。
"""
import math

from fontTools.cu2qu import curve_to_quadratic

FIT_TOL = 0.5      # 把密集采样点拟合成曲线时允许的误差（单位）
QUAD_TOL = 0.3     # 三次曲线转 TrueType 二次曲线时允许的误差

# ───────── 路径 ─────────


def lerp(a, b, t):
    return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)


def line(p0, p3):
    return (p0, lerp(p0, p3, 1 / 3), lerp(p0, p3, 2 / 3), p3)


def curve(p0, p1, p2, p3):
    return (p0, p1, p2, p3)


def arc(c, rx, ry, a0, a1, k=0.5523):
    """椭圆弧，角度单位度，a0→a1 可正可负；k 越大越方。"""
    segs = []
    n = max(1, math.ceil(abs(a1 - a0) / 90 - 1e-9))
    step = (a1 - a0) / n
    for i in range(n):
        t0, t1 = math.radians(a0 + step * i), math.radians(a0 + step * (i + 1))
        h = 4 / 3 * math.tan((t1 - t0) / 4) * (k / 0.5523)
        p0 = (c[0] + rx * math.cos(t0), c[1] + ry * math.sin(t0))
        p3 = (c[0] + rx * math.cos(t1), c[1] + ry * math.sin(t1))
        p1 = (p0[0] - h * rx * math.sin(t0), p0[1] + h * ry * math.cos(t0))
        p2 = (p3[0] + h * rx * math.sin(t1), p3[1] - h * ry * math.cos(t1))
        segs.append((p0, p1, p2, p3))
    return segs


def _bez(s, t):
    p0, p1, p2, p3 = s
    u = 1 - t
    return (u ** 3 * p0[0] + 3 * u * u * t * p1[0] + 3 * u * t * t * p2[0] + t ** 3 * p3[0],
            u ** 3 * p0[1] + 3 * u * u * t * p1[1] + 3 * u * t * t * p2[1] + t ** 3 * p3[1])


def _dbez(s, t):
    p0, p1, p2, p3 = s
    u = 1 - t
    d = (3 * u * u * (p1[0] - p0[0]) + 6 * u * t * (p2[0] - p1[0]) + 3 * t * t * (p3[0] - p2[0]),
         3 * u * u * (p1[1] - p0[1]) + 6 * u * t * (p2[1] - p1[1]) + 3 * t * t * (p3[1] - p2[1]))
    if abs(d[0]) + abs(d[1]) < 1e-9:      # 控制点重合时用弦方向
        d = (p3[0] - p0[0], p3[1] - p0[1])
    n = math.hypot(*d) or 1
    return (d[0] / n, d[1] / n)


def sample(segs, step=5):
    pts = []
    for si, s in enumerate(segs):
        length = sum(math.dist(_bez(s, i / 8), _bez(s, (i + 1) / 8)) for i in range(8))
        n = max(3, int(length / step))
        for i in range(n + 1):
            if i == 0 and si > 0:
                continue
            t = i / n
            pts.append((_bez(s, t), _dbez(s, t)))
    acc = [0.0]
    for i in range(1, len(pts)):
        acc.append(acc[-1] + math.dist(pts[i][0], pts[i - 1][0]))
    total = acc[-1] or 1
    return [(p, d, a / total) for (p, d), a in zip(pts, acc)]


# ───────── 拟合：密集的点 → 少量光滑曲线 ─────────
# 笔画边缘是按 4 单位一步采样出来的。如果把这些点直接写进字体，坐标取整的误差
# 会在大字号下显出一圈细小的锯齿；所以先拟合成几段三次曲线，再转成二次曲线。


def _unit(v):
    n = math.hypot(*v) or 1
    return (v[0] / n, v[1] / n)


def _end_tangent(pts, forward=True):
    """端点处的切线方向（指向曲线内部），跳过离端点太近的点，免得方向被取整噪声带偏。"""
    p0 = pts[0] if forward else pts[-1]
    seq = pts[1:] if forward else pts[-2::-1]
    for q in seq:
        if math.dist(p0, q) >= 3:
            return _unit((q[0] - p0[0], q[1] - p0[1]))
    q = seq[-1]
    return _unit((q[0] - p0[0], q[1] - p0[1]))


def _bern(u):
    v = 1 - u
    return v * v * v, 3 * v * v * u, 3 * v * u * u, u * u * u


def _fit_one(pts, u, t0, t1):
    """端点和端点切线固定，最小二乘求两个控制柄的长度（Schneider 的做法）。"""
    p0, p3 = pts[0], pts[-1]
    c00 = c01 = c11 = x0 = x1 = 0.0
    for p, ui in zip(pts, u):
        b0, b1, b2, b3 = _bern(ui)
        a0 = (t0[0] * b1, t0[1] * b1)
        a1 = (t1[0] * b2, t1[1] * b2)
        c00 += a0[0] * a0[0] + a0[1] * a0[1]
        c01 += a0[0] * a1[0] + a0[1] * a1[1]
        c11 += a1[0] * a1[0] + a1[1] * a1[1]
        tmp = (p[0] - p0[0] * (b0 + b1) - p3[0] * (b2 + b3), p[1] - p0[1] * (b0 + b1) - p3[1] * (b2 + b3))
        x0 += a0[0] * tmp[0] + a0[1] * tmp[1]
        x1 += a1[0] * tmp[0] + a1[1] * tmp[1]
    det = c00 * c11 - c01 * c01
    seg = math.dist(p0, p3)
    al = (x0 * c11 - x1 * c01) / det if abs(det) > 1e-9 else 0
    ar = (c00 * x1 - c01 * x0) / det if abs(det) > 1e-9 else 0
    if al < seg * 1e-3 or ar < seg * 1e-3:
        al = ar = seg / 3
    return (p0, (p0[0] + t0[0] * al, p0[1] + t0[1] * al), (p3[0] + t1[0] * ar, p3[1] + t1[1] * ar), p3)


def _newton(b, p, u):
    q = _bez(b, u)
    p0, p1, p2, p3 = b
    v = 1 - u
    d1 = (3 * (v * v * (p1[0] - p0[0]) + 2 * v * u * (p2[0] - p1[0]) + u * u * (p3[0] - p2[0])),
          3 * (v * v * (p1[1] - p0[1]) + 2 * v * u * (p2[1] - p1[1]) + u * u * (p3[1] - p2[1])))
    d2 = (6 * (v * (p2[0] - 2 * p1[0] + p0[0]) + u * (p3[0] - 2 * p2[0] + p1[0])),
          6 * (v * (p2[1] - 2 * p1[1] + p0[1]) + u * (p3[1] - 2 * p2[1] + p1[1])))
    num = (q[0] - p[0]) * d1[0] + (q[1] - p[1]) * d1[1]
    den = d1[0] ** 2 + d1[1] ** 2 + (q[0] - p[0]) * d2[0] + (q[1] - p[1]) * d2[1]
    return min(1.0, max(0.0, u - num / den)) if abs(den) > 1e-9 else u


def _fit(pts, t0, t1, depth=0):
    if len(pts) <= 3:
        d = math.dist(pts[0], pts[-1]) / 3
        return [(pts[0], (pts[0][0] + t0[0] * d, pts[0][1] + t0[1] * d),
                 (pts[-1][0] + t1[0] * d, pts[-1][1] + t1[1] * d), pts[-1])]
    acc = [0.0]
    for a, b in zip(pts, pts[1:]):
        acc.append(acc[-1] + math.dist(a, b))
    u = [a / (acc[-1] or 1) for a in acc]
    for _ in range(5):
        b = _fit_one(pts, u, t0, t1)
        errs = [math.dist(p, _bez(b, ui)) for p, ui in zip(pts, u)]
        worst = max(range(1, len(pts) - 1), key=lambda i: errs[i])
        if errs[worst] < FIT_TOL or depth > 12:
            return [b]
        u = [_newton(b, p, ui) for p, ui in zip(pts, u)]
    tc = _unit((pts[worst - 1][0] - pts[worst + 1][0], pts[worst - 1][1] - pts[worst + 1][1]))
    return (_fit(pts[:worst + 1], t0, tc, depth + 1) + _fit(pts[worst:], (-tc[0], -tc[1]), t1, depth + 1))


def _quads(cubics):
    """三次曲线串 → [(x, y, 是否在曲线上)]，含首尾两个端点。"""
    out = [(*cubics[0][0], True)]
    for c in cubics:
        q = curve_to_quadratic(c, QUAD_TOL)
        out += [(*pt, False) for pt in q[1:-1]] + [(*q[-1], True)]
    return out


def smooth_open(pts):
    """开放的点串（首尾是角点）→ 光滑曲线的轮廓点。"""
    if len(pts) < 3:
        return [(*p, True) for p in pts]
    t0, t1 = _end_tangent(pts, True), _end_tangent(pts, False)
    return _quads(_fit(pts, t0, t1))


def smooth_closed(pts):
    """闭合的点串（处处光滑）→ 分四段拟合，接点处切线连续。"""
    n = len(pts)
    cuts = [0, n // 4, n // 2, 3 * n // 4, n]
    tan = lambda i: _unit((pts[(i + 1) % n][0] - pts[i - 1][0], pts[(i + 1) % n][1] - pts[i - 1][1]))
    out = []
    for a, b in zip(cuts, cuts[1:]):
        piece = pts[a:b + 1] if b < n else pts[a:] + [pts[0]]
        ta, tb = tan(a), tan(b % n)
        out += _quads(_fit(piece, ta, (-tb[0], -tb[1])))[:-1]
    return out


# ───────── 粗细 ─────────


def contrast(thick, thin, stress=0.0, power=1.3):
    """竖粗横细：笔画方向越接近竖直越粗。stress 是轴心倾角（度）。"""
    st = math.radians(stress)

    def w(s, phi):
        return thin + (thick - thin) * abs(math.sin(phi - st)) ** power
    return w


def const(width):
    return lambda s, phi: width


def profile(base, *knots):
    """在 base 粗细上乘一条沿笔画的曲线，knots 是 (s, 倍数)。
    节点之间用缓入缓出插值（节点处斜率为 0），粗细变化处的轮廓不会出现小折角。"""
    def w(s, phi):
        k = knots[0][1]
        for (s0, k0), (s1, k1) in zip(knots, knots[1:]):
            if s0 <= s <= s1:
                t = (s - s0) / ((s1 - s0) or 1)
                k = k0 + (k1 - k0) * t * t * (3 - 2 * t)
                break
        else:
            k = knots[-1][1] if s > knots[-1][0] else knots[0][1]
        return base(s, phi) * k
    return w


# ───────── 轮廓 ─────────


class Contour:
    """points: [(x, y, 是否在曲线上)]；hole=True 表示字怀（挖空）。"""

    def __init__(self, points, hole=False):
        self.points = points
        self.hole = hole

    def area(self):
        p = self.points
        return 0.5 * sum(p[i][0] * p[(i + 1) % len(p)][1] - p[(i + 1) % len(p)][0] * p[i][1] for i in range(len(p)))

    def oriented(self):
        """TrueType：外轮廓顺时针，字怀逆时针。"""
        ccw = self.area() > 0
        if ccw != self.hole:
            return Contour(list(reversed(self.points)), self.hole)
        return self

    def moved(self, dx=0, dy=0):
        return Contour([(x + dx, y + dy, on) for x, y, on in self.points], self.hole)

    def mapped(self, fn):
        return Contour([(*fn((x, y)), on) for x, y, on in self.points], self.hole)


def poly(*pts, smooth=()):
    """多边形；smooth 里的下标是曲线控制点（不在曲线上）。"""
    return Contour([(p[0], p[1], i not in smooth) for i, p in enumerate(pts)])


def _cut(p, c, T, ang):
    """把端点 p 沿切线方向挪到穿过 c、方向为 ang 的直线上。"""
    u = (math.cos(math.radians(ang)), math.sin(math.radians(ang)))
    cross = lambda a, b: a[0] * b[1] - a[1] * b[0]
    den = cross(T, u)
    if abs(den) < 1e-6:
        return p
    s = cross((c[0] - p[0], c[1] - p[1]), u) / den
    if abs(s) > 2 * math.dist(p, c):      # 切口和笔画几乎平行时不挪，免得飞出去
        return p
    return (p[0] + s * T[0], p[1] + s * T[1])


def sweep(segs, width, cap0="flat", cap1="flat", step=4):
    """开放笔画。cap 可以是 'flat'（垂直切）、('cut', 角度)、'round'。"""
    sm = sample(segs, step)
    left, right = [], []
    for p, d, s in sm:
        w = width(s, math.atan2(d[1], d[0])) / 2
        n = (-d[1], d[0])
        left.append((p[0] + n[0] * w, p[1] + n[1] * w))
        right.append((p[0] - n[0] * w, p[1] - n[1] * w))
    for idx, cap in ((0, cap0), (-1, cap1)):
        if isinstance(cap, tuple) and cap[0] == "cut":
            c, T = sm[idx][0], sm[idx][1]
            u = (math.cos(math.radians(cap[1])), math.sin(math.radians(cap[1])))
            side_of = lambda q: u[0] * (q[1] - c[1]) - u[1] * (q[0] - c[0])
            inside = side_of(sm[len(sm) // 2][0])
            for side in (left, right):
                side[idx] = _cut(side[idx], c, T, cap[1])
                # 切口往笔画里收的那一侧，切线外面剩下的采样点要去掉，不然会折回来形成小缺口
                order = range(1, len(side) - 1) if idx == 0 else range(len(side) - 2, 0, -1)
                drop = []
                for i in order:
                    if side_of(side[i]) * inside > 0:
                        break
                    drop.append(i)
                for i in sorted(drop, reverse=True):
                    del side[i]
    pts = smooth_open(left)
    if cap1 == "round":
        pts += _round_cap(sm[-1][0], sm[-1][1], math.dist(left[-1], right[-1]) / 2, 1)
    pts += smooth_open(list(reversed(right)))
    if cap0 == "round":
        pts += _round_cap(sm[0][0], sm[0][1], math.dist(left[0], right[0]) / 2, -1)
    return Contour(pts)


def _round_cap(c, T, r, sign):
    """半圆收笔：四段二次曲线，控制点落在切线交点上，和笔画两边相切。"""
    base = math.atan2(T[1], T[0]) + (0 if sign > 0 else math.pi)
    k = r / math.cos(math.pi / 8)
    return [(c[0] + k * math.cos(a), c[1] + k * math.sin(a), False)
            for a in (base + math.pi / 2 - math.pi / 8 - math.pi / 4 * j for j in range(4))]


def ring(segs, width, step=4):
    """闭合笔画（比如 o 的一圈）：返回外轮廓和字怀两条。"""
    sm = sample(segs, step)[:-1]
    outer, inner = [], []
    for p, d, s in sm:
        w = width(s, math.atan2(d[1], d[0])) / 2
        n = (-d[1], d[0])
        outer.append((p[0] + n[0] * w, p[1] + n[1] * w))
        inner.append((p[0] - n[0] * w, p[1] - n[1] * w))
    a = Contour(smooth_closed(outer))
    b = Contour(smooth_closed(inner))
    if abs(a.area()) < abs(b.area()):
        a, b = b, a
    b.hole = True
    return [a, b]


def dot(c, r, n=8):
    """圆点（全部用控制点，TrueType 会画成光滑的圆）。"""
    k = r / math.cos(math.pi / n)
    return Contour([(c[0] + k * math.cos(2 * math.pi * i / n), c[1] + k * math.sin(2 * math.pi * i / n), False)
                    for i in range(n)])


def draw(contours, pen):
    for c in contours:
        c = c.oriented()
        pts = c.points
        idx = next((i for i, p in enumerate(pts) if p[2]), None)
        if idx is None:
            pen.qCurveTo(*[(x, y) for x, y, _ in pts], None)
            pen.closePath()
            continue
        pts = pts[idx:] + pts[:idx]
        pen.moveTo(pts[0][:2])
        offs = []
        for x, y, on in pts[1:]:
            if on:
                if offs:
                    pen.qCurveTo(*offs, (x, y))
                    offs = []
                else:
                    pen.lineTo((x, y))
            else:
                offs.append((x, y))
        if offs:
            pen.qCurveTo(*offs, pts[0][:2])
        pen.closePath()


def bounds(contours):
    xs = [p[0] for c in contours for p in c.points]
    ys = [p[1] for c in contours for p in c.points]
    return min(xs), min(ys), max(xs), max(ys)
