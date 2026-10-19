"""渡言的汉字：用和西文同一支笔，按宋体的笔法从零构造。

字身框 1000 × 1000（y 从 -120 到 880），字面大约 x 70–930、y -60–860。
竖画 104、横画 60：和西文同一支笔；汉字比西文略重约一成，读起来两边一样深（苹方也是这样配的）。

接缝规则（避免毛刺和小缺口）：
- 笔画相接时，一笔的端头要整个藏进另一笔里，不能刚好碰边；
- 不相接的笔画之间至少留 35 单位的空，不能留一条细缝。
"""
import math

from pen import Contour, _bez, _dbez, arc, curve, line, poly, ring, sweep

V, H = 104, 60         # 竖画、横画粗细
GAP = 36               # 不相接的笔画之间最少留的空


# ───────── 笔画零件 ─────────

def heng(x0, x1, y, w=H, beak=True, entry=True):
    """横：入笔圆润微斜，末端是圆润的三角「喙」（对应西文的楔形衬线）。"""
    t = w / 2
    L = x1 - x0
    bh = min(48, 18 + L * 0.055)          # 喙高
    bw = min(96, 34 + L * 0.1)            # 喙宽
    if entry:
        left = [(x0 + 4, y - t, True), (x0 - 4, y - t * .1, False), (x0 + 12, y + t, True)]
    else:
        left = [(x0, y - t, True), (x0, y + t, True)]
    if beak:
        right = [(x1 - bw, y + t, True), (x1 - bw * .55, y + t + bh * .18, False), (x1 - bw * .2, y + t + bh * 1.05, False),
                 (x1 + 8, y + t * .3, True), (x1 + 6, y - t + 2, False), (x1 - 18, y - t, True)]
    else:
        right = [(x1, y + t, True), (x1, y - t, True)]
    return Contour(left + right)


def shu(x, y0, y1, w=V, top="head", end="dew"):
    """竖：起笔左高右低的斜切；底部垂露（dew）、悬针（needle）或平（flat）。"""
    l, r = x - w / 2, x + w / 2
    if top == "head":
        pts = [(l, y0 + 16, True), (r - 14, y0 - 6, True), (r + 2, y0 - 12, False), (r, y0 - 34, True)]
    else:
        pts = [(l, y0, True), (r, y0, True)]
    if end == "needle":
        pts += [(r, y1 + 200, True), (r - 8, y1 + 60, False), (x + 2, y1, True), (l + 8, y1 + 60, False), (l, y1 + 200, True)]
    elif end == "dew":
        pts += [(r, y1 + 26, True), (r - 2, y1 - 6, False), (x, y1 - 10, True), (l + 4, y1 - 4, False), (l, y1 + 18, True)]
    else:
        pts += [(r, y1, True), (l, y1, True)]
    return Contour(pts)


def _pie_ctrl(p0, p1, bend):
    c1 = (p0[0] + (p1[0] - p0[0]) * 0.15 + bend[0] * .3, p0[1] + (p1[1] - p0[1]) * 0.35 + bend[1] * .3)
    c2 = (p0[0] + (p1[0] - p0[0]) * 0.6 + bend[0], p0[1] + (p1[1] - p0[1]) * 0.85 + bend[1])
    return (p0, c1, c2, p1)


def pie(p0, p1, bend=(0, 0), w0=V * 1.02, w1=12, head=True):
    """撇：粗起细收。起笔斜切（左高右低）；从别的笔画里出来的撇用 head=False；
    短撇（比如「丷」右边那笔）用 head="round"，像倒过来的点。"""
    width = lambda s, phi: w1 + (w0 - w1) * (1 - s ** 1.7)
    cap = "round" if head == "round" else ("cut", -18) if head else "flat"
    return sweep([_pie_ctrl(p0, p1, bend)], width, cap0=cap)


def on_pie(p0, p1, bend, y):
    """撇的中心线在高度 y 处的点：让捺从撇的正中间起笔，端头不会露出来。"""
    seg = _pie_ctrl(p0, p1, bend)
    lo, hi = 0.0, 1.0
    for _ in range(40):
        mid = (lo + hi) / 2
        if _bez(seg, mid)[1] > y:
            lo = mid
        else:
            hi = mid
    return _bez(seg, (lo + hi) / 2)


def na(p0, p1, bend=(0, 0), wmax=V * 1.18, start="hidden"):
    """捺：细起，越写越粗，末端平出三角形捺脚。start='free' 时起笔是独立的细头。"""
    c1 = (p0[0] + (p1[0] - p0[0]) * 0.3 + bend[0], p0[1] + (p1[1] - p0[1]) * 0.3 + bend[1])
    c2 = (p0[0] + (p1[0] - p0[0]) * 0.72 + bend[0] * .5, p0[1] + (p1[1] - p0[1]) * 0.8 + bend[1] * .5)
    w0 = 26 if start == "free" else 34
    width = lambda s, phi: w0 + (wmax - w0) * s ** 1.25
    body = sweep([curve(p0, c1, c2, p1)], width, cap0=("cut", -18) if start == "free" else "flat")
    d = (p1[0] - c2[0], p1[1] - c2[1])
    n = math.hypot(*d)
    T = (d[0] / n, d[1] / n)
    N = (-T[1], T[0])
    top = (p1[0] + N[0] * wmax / 2, p1[1] + N[1] * wmax / 2)
    bot = (p1[0] - N[0] * wmax / 2, p1[1] - N[1] * wmax / 2)
    tip = (max(top[0], bot[0]) + wmax * .62, min(top[1], bot[1]) + 6)
    foot = poly(top, (top[0] + (tip[0] - top[0]) * .55, top[1] - (top[1] - tip[1]) * .25), tip, bot, smooth={1})
    return [body, foot]


def dian(p0, p1, w=V * 1.2):
    """点：尖头入笔，迅速变粗，圆头收笔（对应西文的球形收笔）。"""
    mid = ((p0[0] + p1[0]) / 2 + (p1[1] - p0[1]) * .08, (p0[1] + p1[1]) / 2 - (p1[0] - p0[0]) * .08)
    width = lambda s, phi: w * (0.2 + 0.8 * math.sin(min(1, s / 0.8) * math.pi / 2))
    return sweep([curve(p0, mid, mid, p1)], width, cap1="round")


def ti(p0, p1, w0=V * 1.08):
    """提：粗起细收，向右上挑出。"""
    width = lambda s, phi: 6 + (w0 - 6) * (1 - s) ** 1.2
    return sweep([line(p0, p1)], width, cap0="round")


def shoulder(x1, y, w=H):
    """横折的「肩」：转角右上方圆润隆起，顺滑地落回竖画右缘，不留台阶。x1 是竖画右缘。"""
    t = w / 2
    return poly((x1 - V - 10, y + t), (x1 - V * .4, y + t + 30), (x1 + 4, y + t + 10), (x1 + 3, y - 30),
                (x1, y - 100), (x1 - V, y - 100), (x1 - V, y - t + 2), smooth={1, 3})


def hengpie(x0, x1, y, p1, bend=(0, 0), w0=V * .98, entry=True):
    """横撇：横 + 肩 + 撇。肩的下沿正好贴着撇的起笔切口，转角处不露台阶。x1 是转角右缘。"""
    t = H / 2
    p0 = (x1 - w0 * .5, y - 6)
    seg = _pie_ctrl(p0, p1, bend)
    T = _dbez(seg, 0)
    n = (-T[1], T[0])
    a = (p0[0] + n[0] * w0 / 2, p0[1] + n[1] * w0 / 2)
    b = (p0[0] - n[0] * w0 / 2, p0[1] - n[1] * w0 / 2)
    lo, hi = sorted((a, b))                     # hi 是切口右下角
    sh = poly((x1 - 100, y + t), (x1 - 40, y + t + 26), (x1 + 6, y + t + 4),
              (hi[0] - T[0] * 35, hi[1] - T[1] * 35), hi, lo, (x1 - 100, y - t), smooth={1, 3})
    return [heng(x0, x1 - 60, y, beak=False, entry=entry), sh, pie(p0, p1, bend, w0=w0, head=False)]


def gou(x, y, dx=-120, dy=80, w=V):
    """竖画的收尾连同钩一起画成一块：右缘圆转到底，向左上挑出尖。x 竖画中心，y 底部。"""
    l, r = x - w / 2, x + w / 2
    return poly((r, y + 70), (r - 1, y + 18), (x + w * .18, y - 14), (x - w * .32, y - 10), (x + dx, y + dy),
                (l - 6, y + dy * .5 + 40), (l, y + 120), smooth={1, 2, 3, 5})


def hook_down(x1, y, w=H):
    """横钩：横画右端顿一下，再向左下出钩，画成一块。x1 是横画右端。"""
    t = w / 2
    return poly((x1 - 90, y + t), (x1 - 34, y + t + 26), (x1 + 16, y + t + 4), (x1 + 18, y - t - 10),
                (x1 - 8, y - 70), (x1 - 52, y - 118), (x1 - 40, y - 60), (x1 - 90, y - t), smooth={1, 3, 6})


def hengzhe(x0, x1, y, y1, end="dew"):
    """横折：横 + 肩 + 竖。x1 是竖画右缘。"""
    return [heng(x0, x1 - V / 2, y, beak=False), shoulder(x1, y), shu(x1 - V / 2, y - 10, y1, top="flat", end=end)]


def wangou(top, bottom, x, bow=18, cap0="flat"):
    """弯钩：微微向右弯的竖，末端向左钩。"""
    body = sweep([curve((x, top), (x + bow, top - (top - bottom) * .35), (x - 4, bottom + (top - bottom) * .35),
                        (x - 4, bottom + 60))], lambda s, phi: V, cap0=cap0)
    return [body, gou(x - 4, bottom)]


# ───────── 字 ─────────

def c_yi():                    # 一
    return [heng(100, 900, 380)]


def c_shi():                   # 十
    return [heng(90, 910, 440), shu(500, 812, -66, end="needle")]


def _kou(xl, xr, yt, yb, foot=24):
    """口：左竖、横折、底横。xl/xr 是左右竖的中心；底横两端藏进竖画里。"""
    return [shu(xl, yt + 40, yb - foot), *hengzhe(xl, xr + V / 2, yt, yb - foot),
            heng(xl, xr, yb, beak=False, entry=False)]


def c_kou():                   # 口
    return _kou(230, 770, 660, 110)


def c_ri():                    # 日
    return _kou(280, 720, 760, 10, foot=30) + [heng(280, 720, 390, beak=False, entry=False)]


def c_zhong():                 # 中
    return _kou(170, 830, 610, 220, foot=34) + [shu(500, 852, -80, end="needle")]


def _pie_na(pie_p0, pie_p1, bend, na_y, na_p1, na_bend=(30, -10), w0=V * 1.1, wmax=V * 1.18, head=True):
    """撇 + 从撇身中间起笔的捺（人、大、天、美的下半部）。"""
    start = on_pie(pie_p0, pie_p1, bend, na_y)
    return [pie(pie_p0, pie_p1, bend=bend, w0=w0, head=head), *na(start, na_p1, bend=na_bend, wmax=wmax)]


def c_ren():                   # 人
    return _pie_na((525, 840), (70, -50), (-20, -20), 540, (850, -10))


def c_da():                    # 大
    return [heng(80, 920, 530), *_pie_na((505, 860), (70, -50), (10, -90), 470, (850, -10))]


def c_tian():                  # 天
    return [heng(190, 810, 720), heng(80, 920, 450),
            *_pie_na((505, 722), (75, -50), (10, -70), 400, (850, -10), w0=V * 1.08, head=False)]


def c_wen():                   # 文
    return [dian((460, 890), (540, 795)), heng(80, 920, 660),
            pie((715, 660), (70, -50), bend=(-70, 40), w0=V * 1.08, head=False),
            *na((305, 655), (850, -10), bend=(70, 10))]


def c_yan():                   # 言
    return [dian((455, 905), (540, 835)), heng(80, 920, 705), heng(210, 790, 565), heng(210, 790, 430),
            *_kou(255, 745, 280, -20, foot=34)]


def c_yong():                  # 永
    return [dian((470, 910), (550, 825)),
            heng(300, 540, 650, beak=False), shoulder(592, 650), shu(540, 640, 110, top="flat", end="flat"),
            gou(540, 50, dx=-130, dy=86),
            *hengpie(110, 404, 490, (70, 110), bend=(-20, 10), w0=V),
            pie((830, 640), (560, 420), w0=V * .98), *na((555, 470), (860, 20), bend=(20, -10), wmax=V * 1.25)]


def c_zi():                    # 字
    return [dian((465, 905), (540, 835)),
            dian((150, 770), (170, 640), w=V * 1.05),
            heng(170, 860, 705, beak=False), hook_down(870, 705),
            *hengpie(250, 744, 545, (450, 390), w0=V * .9), *_zi_gou(744, 545, (450, 390)), heng(80, 920, 290)]


def _zi_gou(x1, y, tail, x=505):
    """「了」的弯钩：顶端顺着上面那一撇的方向斜切，藏进撇身里，转角只留一个利落的尖。"""
    p0 = (x1 - V * .9 * .5, y - 6)
    k = (p0[1] - tail[1]) / (p0[0] - tail[0])
    top = tail[1] + (x - tail[0]) * k
    return wangou(top, 30, x, cap0=("cut", math.degrees(math.atan(k))))


def c_mei():                   # 美
    return [dian((290, 905), (345, 832)), pie((722, 905), (652, 805), w0=V * .95, head="round"),
            heng(220, 780, 695), heng(250, 750, 590), shu(500, 695, 480, top="flat", end="flat"), heng(140, 860, 480),
            heng(80, 920, 330), *_pie_na((505, 482), (70, -55), (10, -50), 280, (850, -15), w0=V * 1.05, head=False)]


def c_du():                    # 渡
    return [dian((85, 790), (180, 705), w=V * 1.05), dian((65, 570), (155, 485), w=V * 1.05),
            ti((60, 70), (210, 325), w0=V),
            dian((590, 915), (650, 855), w=V * 1.05), heng(355, 920, 735, entry=False),
            pie((350, 770), (215, -60), bend=(-15, -10), w0=V),
            heng(410, 895, 560), shu(530, 638, 455, end="flat"), shu(735, 638, 455, end="flat"),
            heng(530 - V / 2, 735 + V / 2, 455, beak=False, entry=False),
            *hengpie(440, 844, 345, (410, -50), bend=(-50, -10), w0=V * .95),
            *na((500, 340), (860, -20), bend=(10, -10), wmax=V * 1.15)]


def c_no():                    # の
    diag = sweep([curve((505, 590), (465, 440), (410, 250), (335, 118))],
                 lambda s, phi: 40 + 50 * math.sin(math.pi * s) ** .8, cap0="round", cap1="round")
    loop = sweep([curve((335, 118), (240, 200), (230, 420), (320, 560)),
                  curve((320, 560), (400, 690), (620, 710), (740, 600)),
                  curve((740, 600), (850, 500), (840, 260), (720, 140)),
                  curve((720, 140), (660, 80), (590, 50), (520, 40))],
                 lambda s, phi: (42 + 54 * abs(math.sin(phi)) ** 1.3) * (0.62 + 0.38 * min(1, s * 6)) * (1 - max(0, s - .85) * 3),
                 cap0="round")
    return [diag, loop]


def p_comma():                 # ，
    return [sweep([curve((165, 105), (205, 55), (198, -30), (120, -115))],
                  lambda s, phi: 8 + 92 * (1 - max(0, (s - .1) / .9)) ** 1.3, cap0="round")]


def p_period():                # 。
    return ring(arc((170, 60), 72, 72, 0, 360), lambda s, phi: 30)


GLYPHS = {"一": c_yi, "十": c_shi, "口": c_kou, "日": c_ri, "中": c_zhong, "人": c_ren, "大": c_da, "天": c_tian,
          "文": c_wen, "言": c_yan, "永": c_yong, "字": c_zi, "美": c_mei, "渡": c_du, "の": c_no,
          "，": p_comma, "。": p_period}
