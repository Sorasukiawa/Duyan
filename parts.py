"""汉字部件。每个部件按它「最常见的样子」在整字的 1000 × 1000 框里画一次；
放进别的字时，用 Map 把坐标从原来的框线性移到新的框：位置和长短跟着缩放，笔画粗细不变
（所以压窄的部件会显得重一些，笔画多的字整体用 weight() 调细）。

每个部件都是一个函数 f(m=ID)，m 是坐标映射。左偏旁（亻、氵、扌……）就画在左边的位置上。
"""
import han
from han import (dian, heng, hengpie, hengpie_wangou, hengzhe, hengzhegou, hengzheti, hengzhezhepie, hook_down, na, on_pie, pie,
                 piedian, piezhe, shu, shugou, shupie, shupie_hengzhegou, shuwangou, shuzhe, ti, wogou, _kou)

FULL = (70, -70, 930, 880)          # 整字部件的设计框


class Map:
    """从设计框 src 线性映射到目标框 dst。"""

    def __init__(self, src=FULL, dst=None):
        dst = src if dst is None else dst
        self.ax = (dst[2] - dst[0]) / (src[2] - src[0])
        self.ay = (dst[3] - dst[1]) / (src[3] - src[1])
        self.bx = dst[0] - src[0] * self.ax
        self.by = dst[1] - src[1] * self.ay

    def x(self, v):
        return self.ax * v + self.bx

    def y(self, v):
        return self.ay * v + self.by

    def p(self, pt):
        return (self.x(pt[0]), self.y(pt[1]))

    def v(self, vec):
        return (vec[0] * self.ax, vec[1] * self.ay)

    def into(self, dst, src=FULL):
        """先从 src 放进 dst，再按自己映射：部件里套部件（化 里的 亻）时用。"""
        inner = Map(src, dst)
        m = Map()
        m.ax, m.ay = self.ax * inner.ax, self.ay * inner.ay
        m.bx, m.by = self.ax * inner.bx + self.bx, self.ay * inner.by + self.by
        return m

    @property
    def k(self):
        """点、钩这类「有大小」的东西跟着缩放的比例：缩得少一点。"""
        return min(1.0, (self.ax * self.ay) ** 0.5) ** 0.6


ID = Map()


def into(dst, src=FULL):
    return Map(src, dst)


# ───────── 映射过的笔画（参数都是设计坐标）─────────

def H_(m, x0, x1, y, **kw):
    return heng(m.x(x0), m.x(x1), m.y(y), **kw)


def S_(m, x, y0, y1, **kw):
    return shu(m.x(x), m.y(y0), m.y(y1), **kw)


def P_(m, p0, p1, bend=(0, 0), **kw):
    if "w0" in kw and kw["w0"] is not None:
        kw["w0"] = kw["w0"] * (0.8 + 0.2 * m.k)
    return pie(m.p(p0), m.p(p1), m.v(bend), **kw)


def N_(m, p0, p1, bend=(30, -10), **kw):
    wmax = kw.pop("wmax", None)
    wmax = (han.V * 1.18 if wmax is None else wmax) * (0.8 + 0.2 * m.k)
    return na(m.p(p0), m.p(p1), m.v(bend), wmax=wmax, **kw)


def D_(m, p0, p1, w=None):
    return dian(m.p(p0), m.p(p1), w=(han.V * 1.2 if w is None else w) * m.k)


def T_(m, p0, p1, w0=None):
    return ti(m.p(p0), m.p(p1), w0=(han.V * 1.08 if w0 is None else w0) * (0.85 + 0.15 * m.k))


def HZ_(m, x0, xc, y, y1, **kw):
    """横折：xc 是竖的中线。"""
    return hengzhe(m.x(x0), m.x(xc) + han.V / 2, m.y(y), m.y(y1), **kw)


def HZG_(m, x0, xc, y, yb, dx=-120, dy=86):
    return hengzhegou(m.x(x0), m.x(xc) + han.V / 2, m.y(y), m.y(yb), dx * m.k, dy * m.k)


def HP_(m, x0, x1, y, p1, bend=(0, 0), **kw):
    return hengpie(m.x(x0), m.x(x1), m.y(y), m.p(p1), m.v(bend), **kw)


def SG_(m, x, y0, yb, dx=-110, dy=80, **kw):
    return shugou(m.x(x), m.y(y0), m.y(yb), dx=dx * m.k, dy=dy * m.k, **kw)


def SZ_(m, x, y0, yb, x1, **kw):
    return shuzhe(m.x(x), m.y(y0), m.y(yb), m.x(x1), **kw)


def SWG_(m, x, y0, yb, x1, **kw):
    return shuwangou(m.x(x), m.y(y0), m.y(yb), m.x(x1), hook=74 * m.k, **kw)


def KOU_(m, xl, xr, yt, yb, foot=44):
    """口：xl、xr 是左右竖的中线，yt、yb 是上下横的中线。"""
    return _kou(m.x(xl), m.x(xr), m.y(yt), m.y(yb), foot * m.k)


def INNER_(m, xl, xr, y):
    """框里的横：两端藏进左右竖。"""
    return heng(m.x(xl), m.x(xr), m.y(y), beak=False, entry=None, right_hid=True)


# ───────── 左偏旁 ─────────

def ren_left(m=ID, vt=640):
    """亻：vt 是竖的起笔高度。"""
    return [P_(m, (250, 872), (54, 430), bend=(-8, 0), w0=han.V * 0.98),
            S_(m, 200, vt, -66, top="head", end="dew")]


def shui(m=ID):
    """氵"""
    return [D_(m, (85, 790), (180, 705), w=han.V * 1.05), D_(m, (65, 570), (155, 485), w=han.V * 1.05),
            T_(m, (88, 70), (226, 325), w0=han.V)]


def shou(m=ID):
    """扌"""
    return [H_(m, 40, 300, 590, beak=0.5), SG_(m, 170, 862, -40, dx=-86, dy=70),
            T_(m, (86, 200), (316, 400), w0=han.V * 0.92)]


def yan_left(m=ID):
    """讠"""
    return [D_(m, (110, 852), (190, 742), w=han.V * 1.1),
            hengzheti(m.x(46), m.x(196) + han.V / 2, m.y(570), m.y(84), m.p((332, 252)))]


def xin_left(m=ID):
    """忄"""
    return [D_(m, (54, 600), (96, 426), w=han.V * 0.86), D_(m, (200, 664), (288, 580), w=han.V * 0.76),
            S_(m, 168, 880, -70, top="head", end="dew")]


def si_left(m=ID):
    """纟"""
    return [piezhe(m.p((236, 880)), m.p((128, 700)), m.p((292, 734)), w=han.V * 0.74),   # 提的尖藏进第二笔的头里
            piezhe(m.p((304, 728)), m.p((124, 420)), m.p((342, 468)), w=han.V * 0.78),
            T_(m, (110, 150), (348, 236), w0=han.V * 0.9)]


def fu_left(m=ID):
    """阝（左耳刀）：左边一竖，右上一个「3」形的横撇弯钩。"""
    return [S_(m, 104, 872, -70, top="flat", end="dew"),
            HP_(m, 104, 280, 820, (150, 620), bend=(-10, 0), w0=han.V * 0.74, entry=None),
            pie(m.p((116, 630)), m.p((126, 290)), w0=han.V * 0.8, head="hid",
                seg=(m.p((116, 630)), m.p((350, 580)), m.p((330, 360)), m.p((126, 290))))]


def nv_left(m=ID):
    """女（左偏旁）：最后一横变成提。"""
    return [piedian(m.p((236, 880)), m.p((96, 470)), m.p((316, 120)), w=han.V * 0.8, wd=han.V * 0.98),
            P_(m, (296, 640), (60, -40), bend=(-20, -10), w0=han.V * 0.96),
            T_(m, (96, 446), (350, 548), w0=han.V * 0.8)]      # 提的圆头压在撇点的转角上，不往左鼓出去


def mu_left(m=ID):
    """木（左偏旁）：捺变成点。"""
    return [H_(m, 40, 310, 620, beak=0.4), S_(m, 190, 872, -70, top="head", end="dew"),
            P_(m, (176, 600), (44, 214), bend=(-6, 0), w0=han.V * 0.92, head="hid"),
            D_(m, (214, 520), (322, 384), w=han.V * 0.92)]


def wang_left(m=ID):
    """王（左偏旁）：底横变成提。"""
    return [H_(m, 50, 310, 720, beak=0.5), H_(m, 60, 290, 430, beak=0.4),
            S_(m, 176, 720, 156, top="hid", end="hid"), T_(m, (86, 102), (330, 226), w0=han.V * 0.9)]


def tu_left(m=ID):
    """土（左偏旁）：底横变成提。"""
    return [S_(m, 176, 820, 166, top="head", end="hid"), H_(m, 50, 310, 520, beak=0.5),
            T_(m, (86, 112), (330, 236), w0=han.V * 0.9)]


def ri_left(m=ID):
    """日（左偏旁）：窄长。"""
    return KOU_(m, 110, 300, 740, 140, foot=30) + [INNER_(m, 110, 300, 440)]


def kou_left(m=ID):
    """口（左偏旁）：小一些，偏上。"""
    return KOU_(m, 100, 300, 600, 250, foot=30)


def yue_left(m=ID):
    """月（左偏旁）：窄。"""
    return shupie_hengzhegou(m.x(110), m.y(800), m.x(312) + han.V / 2, m.y(-40), m.x(46), m.y(-60),
                             w0=han.V * 0.96, dx=-70 * m.k, dy=60 * m.k, bars=(m.y(540), m.y(300)))


def he_left(m=ID):
    """禾（左偏旁）。"""
    return [P_(m, (310, 872), (100, 786), w0=han.V * 0.8), H_(m, 40, 360, 620, beak=0.5),
            S_(m, 206, 822, -70, top="head", end="dew"),
            P_(m, (192, 600), (40, 230), w0=han.V * 0.9, head="hid"), D_(m, (226, 520), (350, 380), w=han.V * 0.9)]


def you_left(m=ID):
    """又（左边窄的那个，双、对、欢）：捺变成点。"""
    return [HP_(m, 60, 330, 740, (80, 80), bend=(-40, 0), w0=han.V * 0.9),
            D_(m, (150, 600), (330, 120), w=han.V * 1.1)]


# ───────── 整字部件（也常常压窄放进右边或下面）─────────

def shi_(m=ID):
    """十"""
    return [H_(m, 62, 938, 440), S_(m, 500, 812, -66, end="needle")]


def gong(m=ID):
    """工"""
    return [H_(m, 170, 830, 740), S_(m, 500, 740, 90, top="hid", end="hid"), H_(m, 56, 944, 90)]


def tu(m=ID):
    """土"""
    return [S_(m, 500, 840, 90, top="head", end="hid"), H_(m, 170, 830, 500), H_(m, 56, 944, 90)]


def wang(m=ID):
    """王"""
    return [H_(m, 160, 840, 760), H_(m, 220, 780, 430, beak=0.6), S_(m, 500, 760, 80, top="hid", end="hid"),
            H_(m, 56, 944, 80)]


def gan(m=ID):
    """干"""
    return [H_(m, 180, 820, 740), H_(m, 56, 944, 430), S_(m, 500, 740, -70, top="hid", end="needle")]


def you(m=ID):
    """又"""
    # 撇先往下再向左下扫出去，捺先陡后平、尾巴拖长；捺脚收在字身里，不挤下一个字
    return [HP_(m, 140, 820, 740, (100, -10), bend=(150, -70), w0=han.V),
            N_(m, (290, 734), (815, -40), bend=(-100, -85), foot=0.75)]


def cun(m=ID):
    """寸"""
    return [H_(m, 62, 938, 620), SG_(m, 640, 860, -40), D_(m, (300, 430), (400, 300))]


def zi_(m=ID):
    """子"""
    return [hengpie_wangou(m.x(220), m.x(784), m.y(780), m.p((450, 600)), m.x(510), m.y(-40)),
            H_(m, 70, 930, 360)]


def li(m=ID):
    """力"""
    return [HZG_(m, 100, 836, 630, -50), P_(m, (470, 880), (56, -66), bend=(-30, -20), w0=han.V * 1.04)]


def ye(m=ID):
    """也"""
    return [HZG_(m, 120, 816, 600, 300, dx=-84, dy=72), S_(m, 500, 790, 300, end="dew"),
            SWG_(m, 160, 700, -40, 950)]


def men(m=ID):
    """门"""
    return [D_(m, (230, 890), (310, 780)), S_(m, 196, 640, -60, top="head", end="dew"),
            HZG_(m, 340, 808, 770, -40)]


def er(m=ID):
    """尔"""
    return [P_(m, (330, 880), (110, 560), w0=han.V * 0.98),
            hook_down(m.x(240), m.x(820), m.y(700), entry=None),
            SG_(m, 520, 700, -40), P_(m, (330, 450), (150, 200), w0=han.V * 0.9),
            D_(m, (700, 460), (830, 250))]


def ben(m=ID):
    """本"""
    return mu(m) + [H_(m, 300, 700, 150, beak=0.6)]


def mu(m=ID):
    """木"""
    return [H_(m, 56, 944, 620), S_(m, 500, 872, -70, top="head", end="dew"),
            P_(m, (480, 610), (90, 180), bend=(-20, -10), head="hid"),
            N_(m, (520, 600), (860, 180), bend=(20, -10), wmax=han.V * 1.1)]


def ke(m=ID):
    """可"""
    return [H_(m, 56, 944, 760), *KOU_(m, 200, 520, 560, 290, foot=30), SG_(m, 730, 760, -50)]


def qu(m=ID):
    """去"""
    return [S_(m, 500, 860, 420, end="hid"), H_(m, 200, 800, 640), H_(m, 56, 944, 420),
            piezhe(m.p((430, 400)), m.p((200, 70)), m.p((720, 150)), w=han.V * 0.86),
            D_(m, (620, 340), (800, 130))]


def she(m=ID):
    """舌"""
    return [P_(m, (720, 880), (300, 780), w0=han.V * 0.8), H_(m, 62, 938, 650),
            S_(m, 500, 820, 400, top="head", end="hid"), *KOU_(m, 270, 730, 400, -30)]


def yuan(m=ID):
    """元"""
    return [H_(m, 230, 770, 760), H_(m, 56, 944, 500),
            shupie(m.x(380), m.y(500), m.x(90), m.y(-60), w0=han.V * 0.98),
            SWG_(m, 620, 500, -30, 920, top="hid")]


def bi(m=ID):
    """匕（它、化 的右下）"""
    return [P_(m, (720, 680), (170, 340), w0=han.V * 0.9), SWG_(m, 270, 800, -30, 900)]


def gu(m=ID):
    """古"""
    return [H_(m, 62, 938, 640), S_(m, 500, 870, 400, end="hid"), *KOU_(m, 260, 740, 400, -30)]


def zao(m=ID):
    """早"""
    return [*KOU_(m, 260, 740, 820, 470, foot=40), INNER_(m, 260, 740, 650), H_(m, 56, 944, 300),
            S_(m, 500, 450, -70, top="hid", end="needle")]


def tian_(m=ID):
    """田"""
    return KOU_(m, 200, 800, 820, 60) + [INNER_(m, 200, 800, 440), S_(m, 500, 820, 60, top="hid", end="hid")]


def ri(m=ID):
    """日"""
    return KOU_(m, 280, 720, 760, 10) + [INNER_(m, 280, 720, 390)]


def mu_box(m=ID):
    """目"""
    return KOU_(m, 280, 720, 820, -30) + [INNER_(m, 280, 720, 560), INNER_(m, 280, 720, 270)]


def yue(m=ID):
    """月"""
    return shupie_hengzhegou(m.x(240), m.y(800), m.x(788) + han.V / 2, m.y(-40), m.x(60), m.y(-60),
                             dx=-110 * m.k, dy=80 * m.k, bars=(m.y(540), m.y(300)))


def kou(m=ID):
    """口"""
    return KOU_(m, 230, 770, 660, 110)


def ren(m=ID):
    """人"""
    start = on_pie(m.p((540, 860)), m.p((40, -60)), m.v((-30, -50)), m.y(520))
    return [P_(m, (540, 860), (40, -60), bend=(-30, -50), w0=han.V * 1.2),
            na(start, m.p((790, -20)), m.v((20, -20)), wmax=han.V * 1.35 * (0.8 + 0.2 * m.k), foot=0.7)]


def da(m=ID):
    """大"""
    start = on_pie(m.p((505, 860)), m.p((70, -50)), m.v((10, -90)), m.y(470))
    return [H_(m, 56, 944, 530), P_(m, (505, 860), (70, -50), bend=(10, -90), w0=han.V * 1.1),
            na(start, m.p((850, -10)), m.v((30, -10)), wmax=han.V * 1.18 * (0.8 + 0.2 * m.k))]


def wen(m=ID):
    """文"""
    return [D_(m, (466, 900), (540, 812)), H_(m, 56, 944, 660),
            P_(m, (715, 660), (70, -50), bend=(-70, 40), w0=han.V * 1.08, head="hid"),
            N_(m, (305, 655), (850, -10), bend=(70, 10))]


def yan(m=ID):
    """言"""
    return [D_(m, (455, 905), (540, 835)), H_(m, 56, 944, 705), H_(m, 210, 790, 565, beak=0.7),
            H_(m, 210, 790, 430, beak=0.7)] + KOU_(m, 255, 745, 280, -20)


def xin(m=ID):
    """心"""
    return [D_(m, (100, 360), (170, 220), w=han.V * 1.05),
            wogou(m.x(240), m.y(600), m.x(470), m.y(-36), m.x(860), m.y(40)),
            D_(m, (450, 770), (530, 650)), D_(m, (710, 650), (850, 470), w=han.V * 1.1)]


def wang_lost(m=ID):
    """亡"""
    return [D_(m, (476, 930), (540, 848)), H_(m, 56, 944, 646), SZ_(m, 230, 646, 80, 900, top="hid")]


def sheng(m=ID):
    """生"""
    return [P_(m, (300, 870), (100, 520), w0=han.V * 0.96), H_(m, 196, 800, 650, entry=None),
            H_(m, 170, 830, 380), S_(m, 500, 860, 80, top="head", end="hid"), H_(m, 56, 944, 80)]


def hua(m=ID):
    """化：亻 + 匕"""
    return ren_left(m.into((60, -70, 330, 880), (40, -70, 300, 880)), vt=600) + \
        [P_(m, (820, 690), (380, 360), w0=han.V * 0.9), SWG_(m, 470, 860, -30, 920)]


# ───────── 头和底 ─────────

def mian(m=ID):
    """宀"""
    return [D_(m, (465, 905), (540, 835)), D_(m, (112, 772), (132, 642), w=han.V * 1.05),
            hook_down(m.x(132), m.x(912), m.y(705), entry=None)]


def cao(m=ID):
    """艹"""
    return [H_(m, 70, 930, 730), S_(m, 320, 880, 590, top="head", end="dew"),
            S_(m, 680, 880, 590, top="head", end="dew")]


def ren_top(m=ID):
    """人字头（今、会、合、全）：撇和捺张得很开。"""
    start = on_pie(m.p((500, 880)), m.p((80, 470)), m.v((-20, -10)), m.y(780))
    return [P_(m, (500, 880), (80, 470), bend=(-20, -10), w0=han.V * 1.04),
            na(start, m.p((862, 470)), m.v((40, -10)), wmax=han.V * 1.1 * (0.8 + 0.2 * m.k))]


def zou(m=ID):
    """辶：点、横折折撇（这里画成一个短横撇）、平捺（先往下，再贴着底往右扫出去）。
    里面的部件放在 (310, 150, 930, 880) 这样的框里。"""
    return [D_(m, (150, 836), (226, 740), w=han.V * 1.0),
            hengzhezhepie(m.x(56), m.x(250), m.y(590), m.p((70, 420)), m.x(244), m.p((62, 176)),
                          w0=han.V * 0.8, w2=han.V * 0.86, bend2=m.v((-10, 10))),
            na(m.p((88, 212)), m.p((918, -40)), m.v((-150, -110)), wmax=han.V * 1.12, w0=34, foot=0.42, start="tip")]
