"""按设计意图检查一个字的轮廓。不猜「这个尖是不是故意的」，而是核对标注：

- 露头：标了 hid（应该藏进别的笔画）的点，没被别的笔画盖住，或者离边不到 3 单位。
- 打结：一条轮廓自己和自己相交（偏移曲线打结、控制柄拉过头都会这样）。
- 尖角：露在外面的角，内角小于 40°，却没有标 tip（有意的尖）。
- 擦边：两笔的边缘以小于 15° 的夹角相交，交点露在外面——会出现细长的小缺口或小毛刺。
- 贴边：两笔的边缘几乎平行、相距不到 4 单位地并行一段——会出现台阶或发丝缝。
- 窄缝：不相连的两块墨，最近处不到 34 单位。
- 走向不顺：一段曲线两端标的走向对不上（切线交点在背后），曲线会扭成 S 形或打卷。
- 小折角：轮廓上的点进出方向差 3°～25°，看起来像没画顺的小拐。
- 被吞：一笔的节点全落在另一条轮廓里面。系统渲染（CoreText）会把这样的轮廓当成字怀、反过来画，
  重叠处变成镂空（「月」框里的短横两头都藏进同一条外框时就是这样）。
"""
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from outline import _dir, _unit, handle_reach, tangents  # noqa: E402

STEP = 1.5


def _poly(shape, ccw):
    p = np.array(shape.flatten(STEP))
    a = 0.5 * np.sum(p[:, 0] * np.roll(p[:, 1], -1) - np.roll(p[:, 0], -1) * p[:, 1])
    want_pos = ccw != shape.hole
    if (a > 0) != want_pos:
        p = p[::-1]
    return p


def winding(pts, poly):
    """每个点相对一条闭合折线的环绕数。"""
    x, y = pts[:, 0:1], pts[:, 1:2]
    x0, y0 = poly[:, 0], poly[:, 1]
    x1, y1 = np.roll(x0, -1), np.roll(y0, -1)
    cross = (x1 - x0) * (y - y0) - (x - x0) * (y1 - y0)
    up = (y0 <= y) & (y1 > y) & (cross > 0)
    down = (y0 > y) & (y1 <= y) & (cross < 0)
    return up.sum(1) - down.sum(1)


def fill(pts, polys):
    w = np.zeros(len(pts), int)
    for p in polys:
        w += winding(pts, p)
    return w != 0


def covered(pts, polys, margin):
    """点在这些轮廓的墨里面，而且往 8 个方向挪 margin 也还在里面。"""
    ok = fill(pts, polys)
    for a in range(0, 360, 45):
        d = np.array([math.cos(math.radians(a)), math.sin(math.radians(a))]) * margin
        ok &= fill(pts + d, polys)
    return ok


def _segs(p):
    return p, np.roll(p, -1, axis=0)


def intersections(pa, pb, same=False):
    """两条折线的交点：返回 [(x, y, 夹角°, i, j)]。"""
    a0, a1 = _segs(pa)
    b0, b1 = _segs(pb)
    out = []
    da = a1 - a0
    db = b1 - b0
    for i in range(len(a0)):
        p, r = a0[i], da[i]
        den = r[0] * db[:, 1] - r[1] * db[:, 0]
        q = b0 - p
        with np.errstate(divide="ignore", invalid="ignore"):
            t = (q[:, 0] * db[:, 1] - q[:, 1] * db[:, 0]) / den
            u = (q[:, 0] * r[1] - q[:, 1] * r[0]) / den
        scale = np.hypot(*r) * np.hypot(db[:, 0], db[:, 1]) + 1e-12
        hit = (np.abs(den) > 1e-6 * scale) & (t >= 0) & (t < 1) & (u >= 0) & (u < 1)   # 平行、共线的不算相交
        for j in np.nonzero(hit)[0]:
            if same and (abs(i - j) <= 1 or abs(i - j) >= len(a0) - 1):
                continue
            ang = math.degrees(math.acos(min(1, abs(r @ db[j]) / (np.hypot(*r) * np.hypot(*db[j]) + 1e-12))))
            x, y = p + t[j] * r
            out.append((x, y, ang, i, j))
    return out


def seg_distance(pts, poly):
    """每个点到折线的最近距离，以及最近那一段的方向。"""
    a0, a1 = _segs(poly)
    d = a1 - a0
    L2 = (d ** 2).sum(1) + 1e-12
    best = np.full(len(pts), np.inf)
    bdir = np.zeros((len(pts), 2))
    for k in range(0, len(a0), 256):
        s0, sd, sl = a0[k:k + 256], d[k:k + 256], L2[k:k + 256]
        rel = pts[:, None, :] - s0[None, :, :]
        t = np.clip((rel * sd[None]).sum(2) / sl[None], 0, 1)
        proj = s0[None] + t[..., None] * sd[None]
        dist = np.hypot(*(pts[:, None, :] - proj).transpose(2, 0, 1))
        j = dist.argmin(1)
        dj = dist[np.arange(len(pts)), j]
        better = dj < best
        best[better] = dj[better]
        bdir[better] = sd[j[better]] / np.sqrt(sl[j[better]])[:, None]
    return best, bdir


def check(shapes, gap=34):
    """返回 [(类别, x, y, 说明)]。"""
    polys = [_poly(s, True) for s in shapes]
    issues = []

    # 露头 / 尖角
    for si, s in enumerate(shapes):
        others = [p for j, p in enumerate(polys) if j != si]
        tans = tangents(s)
        area_sign = 1 if (s.area() > 0) != s.hole else -1   # 1：墨在走向左边
        for q, (tin, tout) in zip(s.nodes, tans):
            pt = np.array([[q.x, q.y]])
            if q.hid:
                if not others or not covered(pt, others, 3.0)[0]:
                    issues.append(("露头", q.x, q.y, f"{s.name or '笔画'} 的端点应该藏进别的笔画"))
                continue
            if others and covered(pt, others, 1.0)[0]:
                continue                       # 被别的笔画盖住了，看不见
            turn = math.degrees(math.atan2(tin[0] * tout[1] - tin[1] * tout[0], tin[0] * tout[0] + tin[1] * tout[1]))
            interior = 180 - turn * area_sign
            if interior < 40 and not q.tip:
                issues.append(("尖角", q.x, q.y, f"内角 {interior:.0f}°，没有标成有意的尖"))

    # 被吞
    holes = [p for s, p in zip(shapes, polys) if s.hole]
    for si, s in enumerate(shapes):
        if s.hole:
            continue
        pts = np.array([q.xy for q in s.nodes])
        if holes and fill(pts, holes).all():
            continue                           # 放在字怀里的笔画，嵌套关系是对的
        for sj, t in enumerate(shapes):
            if sj != si and not t.hole and fill(pts, [polys[sj]]).all():
                x, y = pts.mean(0)
                issues.append(("被吞", x, y, f"{s.name or '笔画'} 整笔落在 {t.name or '另一笔'} 里面，系统渲染会把它当成字怀"))
                break

    # 走向不顺、小折角
    for s in shapes:
        k = len(s.nodes)
        for i, a in enumerate(s.nodes):
            b = s.nodes[(i + 1) % k]
            if a.t == "line" or a.h is not None or (a.dout is None and b.din is None):
                continue
            chord = _unit((b.x - a.x, b.y - a.y))
            u = _dir(a.dout) if a.dout is not None else chord
            v = _dir(b.din) if b.din is not None else chord
            if a.dout is None or b.din is None:
                continue
            if handle_reach(a, b, u, v)[0] is None and abs(u[0] * v[1] - u[1] * v[0]) > 1e-3:
                # 两端往弦的两侧偏是正常的 S 形（拐点在中间）；往同一侧偏、交点却在背后才会打卷
                c1 = u[0] * chord[1] - u[1] * chord[0]
                c2 = chord[0] * v[1] - chord[1] * v[0]
                if c1 * c2 > 0:
                    issues.append(("走向不顺", (a.x + b.x) / 2, (a.y + b.y) / 2, f"{s.name or '笔画'} 这一段两端的走向对不上"))
        for q, (tin, tout) in zip(s.nodes, tangents(s)):
            turn = abs(math.degrees(math.atan2(tin[0] * tout[1] - tin[1] * tout[0], tin[0] * tout[0] + tin[1] * tout[1])))
            if 3 < turn < 25 and not q.hid and not q.tip:
                issues.append(("小折角", q.x, q.y, f"进出方向差 {turn:.0f}°"))

    # 打结
    for si, p in enumerate(polys):
        for x, y, ang, i, j in intersections(p, p, same=True)[:1]:
            issues.append(("打结", x, y, f"{shapes[si].name or '笔画'} 的轮廓自己相交"))

    # 擦边、贴边
    for a in range(len(polys)):
        for b in range(a + 1, len(polys)):
            rest = [p for k, p in enumerate(polys) if k not in (a, b)]
            for x, y, ang, i, j in intersections(polys[a], polys[b]):
                if ang < 15 and not (rest and covered(np.array([[x, y]]), rest, 1.5)[0]):
                    issues.append(("擦边", x, y, f"两笔边缘夹角只有 {ang:.0f}°"))
    for a in range(len(polys)):
        pa = polys[a]
        others = [p for k, p in enumerate(polys) if k != a]
        if not others:
            continue
        vis = ~fill(pa, others)
        da = np.roll(pa, -1, axis=0) - pa
        da = da / (np.hypot(da[:, 0], da[:, 1])[:, None] + 1e-12)
        for b, pb in enumerate(polys):
            if b == a:
                continue
            dist, bdir = seg_distance(pa, pb)
            par = np.abs((da * bdir).sum(1)) > math.cos(math.radians(12))
            bad = vis & par & (dist > 0.3) & (dist < 4)
            idx = np.nonzero(bad)[0]
            if len(idx) == 0:
                continue
            runs, start = [], idx[0]
            for u, v in zip(idx, list(idx[1:]) + [None]):
                if v is None or v != u + 1:
                    runs.append((start, u))
                    start = v
            for r0, r1 in runs:
                length = (r1 - r0 + 1) * STEP
                if length >= 6:
                    m = (r0 + r1) // 2
                    issues.append(("贴边", pa[m, 0], pa[m, 1], f"和另一笔相距 {dist[m]:.1f} 单位并行 {length:.0f} 单位"))

    # 窄缝：先按是否相连分组
    k = len(shapes)
    parent = list(range(k))
    def find(i):
        while parent[i] != i:
            parent[i] = parent[parent[i]]
            i = parent[i]
        return i
    for a in range(k):
        for b in range(a + 1, k):
            if shapes[a].hole or shapes[b].hole:
                continue
            touch = fill(polys[a][::4], [polys[b]]).any() or fill(polys[b][::4], [polys[a]]).any()
            if touch:
                parent[find(a)] = find(b)
    groups = {}
    for i in range(k):
        if not shapes[i].hole:
            groups.setdefault(find(i), []).append(i)
    keys = list(groups)
    for x in range(len(keys)):
        for y in range(x + 1, len(keys)):
            pa = np.vstack([polys[i] for i in groups[keys[x]]])
            pb_list = [polys[i] for i in groups[keys[y]]]
            best = (np.inf, None)
            for pb in pb_list:
                dist, _ = seg_distance(pa[::2], pb)
                m = dist.argmin()
                if dist[m] < best[0]:
                    best = (dist[m], pa[::2][m])
            if best[0] < gap:
                issues.append(("窄缝", best[1][0], best[1][1], f"两块墨最近处只有 {best[0]:.0f} 单位"))
    return issues
