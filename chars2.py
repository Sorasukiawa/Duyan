"""渡言的常用字（第二批）：按使用频率挑的高频字，能用部件拼的就拼（拼法见 chars.py 的 lr、tb、bao）。"""
import han
from chars import _w, bao, lr, tb
from han import dian, heng, hengpie, hook_down, na, piezhe, pie, shu, shupie
from outline import Shape, n
from parts import (ID, D_, H_, HZ_, HZG_, INNER_, KOU_, P_, S_, SG_, SWG_, T_, gong, into, kou, li, men, mian, qu, ke,
                   ren, ren_left, ren_top, si_left, tu, tu_left, wang_left, ye, yan_left, you, yue, zi_, zou)

V = lambda k=1.0: han.V * k      # noqa: E731


# ───────── 新部件 ─────────

def bu(m=ID):
    """不（还 里面那个）"""
    return [H_(m, 62, 938, 760), P_(m, (560, 760), (90, 250), bend=(-30, -10), head="hid"),
            S_(m, 530, 600, -70, top="head", end="dew"), D_(m, (660, 520), (860, 330))]


def he_close(m=ID):
    """合（给 的右边）"""
    return ren_top(m) + [H_(m, 340, 640, 455, beak=0.6)] + KOU_(m, 270, 730, 310, -30)


def dan(m=ID):
    """旦"""
    return KOU_(m, 290, 710, 820, 330) + [INNER_(m, 290, 710, 575), H_(m, 100, 900, 60)]


def ren_narrow(m=ID):
    """从 左边的人：捺写成长点。"""
    start = han.on_pie(m.p((330, 870)), m.p((50, -50)), m.v((-20, -30)), m.y(430))
    return [P_(m, (330, 870), (50, -50), bend=(-20, -30), w0=V(1.1)),
            dian(start, m.p((380, 170)), w=V(1.1))]


# ───────── 字 ─────────

def c_huan():                  # 还
    return bao(zou, bu, (336, 220, 906, 900), 0.9)


def c_di():                    # 地
    return lr(tu_left, ye, (360, -50, 945, 860))


def c_wen_ask():               # 问
    with han.weight(0.92):
        return men() + KOU_(ID, 380, 640, 520, 210, foot=34)


def c_jian():                  # 间
    with han.weight(0.9):
        return men() + KOU_(ID, 380, 640, 560, 150, foot=34) + [INNER_(ID, 380, 640, 355)]


def c_gei():                   # 给
    return lr(si_left, he_close, (380, -60, 900, 880), 0.9)


def c_cong():                  # 从
    return lr(ren_narrow, ren, (420, -60, 895, 880))


def c_hui_back():              # 回
    with han.weight(0.92):
        return han._kou(110, 890, 820, -40) + han._kou(350, 650, 560, 230, foot=34)


def c_guo():                   # 国
    with han.weight(0.9):
        return han._kou(110, 890, 820, -40) + [
            heng(280, 720, 620, beak=0.6), heng(300, 700, 410, beak=0.6),
            shu(500, 620, 180, top="hid", end="hid"), heng(250, 750, 180, beak=0.6),
            dian((585, 340), (670, 250), w=V(0.95))]


def c_dan_but():               # 但
    return lr(ren_left, dan, (330, -40, 945, 860), 0.9)


def c_li_inside():             # 里
    with han.weight(0.9):
        return han._kou(200, 800, 820, 400) + [
            heng(200, 800, 610, beak=False, entry=None, right_hid=True),
            shu(500, 820, 200, top="hid", end="hid"),
            heng(170, 830, 200, beak=0.7), heng(56, 944, -40)]


def c_hou():                   # 后
    with han.weight(0.9):
        return [pie((780, 884), (300, 786), w0=V(0.9)), heng(230, 920, 690),
                pie((290, 700), (60, -60), bend=(10, -60), head="hid", w0=V(1.0)),
                heng(380, 880, 500, beak=0.7)] + han._kou(400, 850, 330, -40)


def c_tong():                  # 同
    with han.weight(0.92):
        return [shu(130, 850, -70, top="head", end="dew"), han.hengzhegou(130, 888, 830, -60),
                heng(300, 700, 640, beak=0.6)] + han._kou(330, 670, 470, 200, foot=34)


def c_kai():                   # 开
    return [heng(140, 860, 760), heng(56, 944, 470),
            pie((370, 760), (80, -60), bend=(10, -80), head="hid"),
            shu(640, 760, -70, top="hid", end="dew")]


def c_wu():                    # 无
    return [heng(160, 840, 760), heng(56, 944, 470),
            pie((470, 760), (70, -50), bend=(20, -60), head="hid"),
            han.shuwangou(570, 470, -30, 940, top="hid")]


def c_yu():                    # 于
    return [heng(140, 860, 740), heng(56, 944, 440), han.shugou(500, 740, -50, top="hid")]


def c_shou_hand():             # 手
    return [pie((790, 884), (250, 790), w0=V(0.9)), heng(170, 830, 660), heng(210, 790, 460),
            heng(56, 944, 250), han.shugou(500, 800, -50, top="hid")]


def c_zheng():                 # 正
    return [heng(110, 890, 790), shu(500, 790, 40, top="hid", end="hid"),
            heng(500, 830, 430, entry=None), shu(240, 520, 40, top="head", end="hid"), heng(56, 944, 40)]


def c_tou():                   # 头
    return [dian((310, 850), (400, 745), w=V(1.0)), dian((250, 660), (340, 555), w=V(1.0)),
            heng(56, 944, 400), pie((600, 884), (90, -60), bend=(10, -90)),
            dian((620, 250), (770, 80), w=V(1.15))]


def c_nian():                  # 年
    with han.weight(0.92):
        return [pie((330, 884), (110, 600), w0=V(0.95)), heng(250, 860, 740),
                heng(230, 770, 500, beak=0.6), shu(310, 500, 270, top="hid", end="hid"),
                heng(56, 944, 270), shu(570, 740, -70, top="hid", end="needle")]


# ───────── 第二组的部件 ─────────

def si_(m=ID):
    """厶（么、公 的下半）：撇折 + 点。"""
    return [piezhe(m.p((500, 880)), m.p((170, 110)), m.p((800, 230)), w=V(0.9)),
            D_(m, (640, 520), (840, 220), w=V(1.1))]


def ba(m=ID):
    """八（公、分 的上半）：撇和一个尖头起笔的短捺。"""
    return [P_(m, (400, 880), (70, 300), bend=(-10, -30), w0=V(1.05)),
            na(m.p((600, 870)), m.p((820, 380)), m.v((10, -40)), wmax=V(1.15) * (0.8 + 0.2 * m.k), start="tip")]


def xi_(m=ID):
    """夕（名、多、外）：撇、横撇、点。"""
    x0 = han.on_pie(m.p((470, 880)), m.p((120, 470)), m.v((-10, -20)), m.y(740))[0]
    return [P_(m, (470, 880), (120, 470), bend=(-10, -20), w0=V(1.0)),
            hengpie(x0, m.x(780), m.y(740), m.p((150, 40)), m.v((70, -40)), w0=V(1.0), entry=None),
            D_(m, (380, 610), (540, 480), w=V(1.1))]


def zou_di(m=ID, heng_top=True, na_end=(870, -30), shu_end=100):
    """定、是 下面的「𤴓」：顶横（是 用自己的长横，不画）、中间一竖、右边短横、左边竖撇、长捺托底。
    压窄放进右边时（提）捺脚会往右冲，na_end 往里收；中间一竖的末端 shu_end 要跟着藏进捺里。"""
    return [H_(m, 170, 830, 760)] * heng_top + [
            S_(m, 500, 760, shu_end, top="hid", end="hid"), H_(m, 500, 800, 470, entry=None, beak=0.6),
            shupie(m.x(290), m.y(560), m.x(70), m.y(-40), w0=V(0.95), head="cut"),
            na(m.p((280, 250)), m.p(na_end), m.v((-40, -70)), wmax=V(1.18) * (0.8 + 0.2 * m.k))]


def yun_left(m=ID):
    """云（动 的左边）"""
    return [H_(m, 90, 330, 730, beak=0.5), H_(m, 40, 400, 530, beak=0.5),
            piezhe(m.p((220, 520)), m.p((100, 140)), m.p((380, 230)), w=V(0.8)),
            D_(m, (290, 350), (390, 200), w=V(0.9))]


def zha(m=ID):
    """乍（作 的右边）"""
    return [P_(m, (390, 880), (100, 520), w0=V(1.0)), H_(m, 280, 900, 700, entry=None),
            S_(m, 340, 700, -70, top="hid", end="dew"),
            H_(m, 340, 800, 440, entry=None, beak=0.6), H_(m, 340, 830, 180, entry=None, beak=0.6)]


def chi_left(m=ID):
    """彳"""
    x = han.on_pie(m.p((320, 660)), m.p((40, 360)), (0, 0), m.y(520))[0] + 50 * m.ax
    return [P_(m, (280, 880), (60, 650), w0=V(0.9)), P_(m, (320, 660), (40, 360), w0=V(0.96)),
            shu(x, m.y(520), m.y(-70), top="head", end="dew")]


def chu(m=ID):
    """亍（行 的右边）"""
    return [H_(m, 150, 850, 760), H_(m, 56, 944, 500), SG_(m, 620, 500, -60)]


def jing_r(m=ID):
    """圣 的写法（经 的右边）：又 + 工。"""
    return you(m.into((150, 450, 850, 880))) + gong(m.into((110, -60, 890, 360)))


def jing_well(m=ID):
    """井"""
    return [H_(m, 150, 850, 620), H_(m, 56, 944, 300),
            shupie(m.x(360), m.y(880), m.x(120), m.y(-60), w0=V(1.0), head="cut"),
            S_(m, 650, 880, -70, top="head", end="dew")]


def zhi_left(m=ID):
    """至（到 的左边）：底横收短。"""
    return [H_(m, 72, 560, 800, beak=0.5),
            piezhe(m.p((320, 800)), m.p((170, 570)), m.p((460, 620)), w=V(0.8), head="hid"),
            D_(m, (390, 700), (520, 560), w=V(0.9)), H_(m, 110, 500, 380, beak=0.5),
            S_(m, 300, 500, 40, top="head", end="hid"), H_(m, 64, 560, 40, beak=0.5)]


def dao_right(m=ID):
    """刂"""
    return [S_(m, 260, 700, 200, top="head", end="dew"), SG_(m, 760, 880, -60)]


def dui(m=ID):
    """兑（说 的右边）：丷、口、儿。"""
    return [D_(m, (300, 880), (380, 770), w=V(1.05)), P_(m, (740, 890), (620, 760), w0=V(0.9)),
            *KOU_(m, 240, 760, 640, 400, foot=30),
            shupie(m.x(400), m.y(400), m.x(80), m.y(-60), w0=V(0.95), head="hid"),
            SWG_(m, 620, 400, -30, 930, top="hid")]


def shi_arrow(m=ID):
    """矢（知 的左边）：捺变成点。"""
    x0 = han.on_pie(m.p((230, 880)), m.p((60, 600)), (0, 0), m.y(700))[0]
    return [P_(m, (230, 880), (60, 600), w0=V(0.9)), heng(x0, m.x(400), m.y(700), entry=None, beak=0.5),
            H_(m, 40, 440, 450, beak=0.5), P_(m, (260, 700), (40, -50), bend=(-10, -20), head="hid"),
            D_(m, (290, 360), (430, 90), w=V(0.95))]


def jian_see(m=ID):
    """见：冂 + 儿。"""
    return [S_(m, 190, 860, 330, top="head", end="dew"), HZ_(m, 190, 810, 820, 330),
            shupie(m.x(396), m.y(650), m.x(70), m.y(-60), w0=V(0.85), head="cut"),
            SWG_(m, 598, 650, -30, 930, top="head")]


def yong(m=ID):
    """用：外框和 月 一样画成一条轮廓；中间一竖把框里的空当左右分开，竖的下半截单独画。"""
    xm, ybar = m.x(500), (m.y(560), m.y(290))
    frame = han.shupie_hengzhegou(m.x(150), m.y(830), m.x(840) + han.V / 2, m.y(-50), m.x(40), m.y(-60),
                                  dx=-110 * m.k, dy=80 * m.k, bars=ybar)
    out = [frame[0]]
    for h in frame[1:]:                     # 每个空当按中间那一竖切成左右两块
        (a, b, c, d) = h.nodes
        l, r = xm - han.V / 2, xm + han.V / 2
        out.append(Shape([n(l, a.y), n(l, b.y), c, d], hole=True, name="字怀"))
        out.append(Shape([n(a.x, a.y), n(b.x, b.y), n(r, b.y), n(r, a.y)], hole=True, name="字怀"))
    return out + [S_(m, 500, 290, -40, top="hid", end="dew")]


# ───────── 第二组的字 ─────────

def c_me():                    # 么
    return [P_(ID, (440, 880), (130, 560), w0=V(1.0)), piezhe((530, 640), (170, 80), (800, 190), w=V(0.9)),
            dian((650, 420), (860, 130), w=V(1.1))]


def c_gong_public():           # 公
    return ba(into((70, 380, 930, 880))) + si_(into((90, -70, 910, 460)))


def c_fen():                   # 分
    return ba(into((50, 420, 950, 890))) + [HZG_(ID, 270, 760, 470, -50),
                                             P_(ID, (470, 470), (100, -60), bend=(-20, -30), head="hid")]


def c_zhi_of():                # 之
    return [dian((470, 910), (550, 800)),
            hengpie(200, 760, 640, (160, 140), bend=(40, -20)),
            na((196, 186), (900, -20), (-150, -110), wmax=V(1.15), w0=34, foot=0.45, start="tip")]


def xue_top(m=ID):
    """学 的上半：⺍ + 冖。"""
    return [D_(m, (250, 880), (330, 770), w=V(1.0)), D_(m, (470, 900), (530, 800), w=V(1.0)),
            P_(m, (790, 905), (650, 770), w0=V(0.9)),
            D_(m, (110, 700), (130, 580), w=V(1.05)), hook_down(m.x(130), m.x(890), m.y(646), entry=None)]


def c_xue():                   # 学
    return tb(xue_top, zi_, (80, -70, 920, 540), 0.9)


def c_ding():                  # 定
    return tb(mian, zou_di, (80, -60, 940, 560), 0.9)


def c_shi_is():                # 是
    return _w(0.9, lambda: KOU_(ID, 250, 750, 860, 560, foot=30) + [INNER_(ID, 250, 750, 710), heng(56, 944, 420)]
              + zou_di(into((70, -40, 930, 470)), heng_top=False))


def c_you_have():              # 有
    return [heng(56, 944, 650), pie((470, 880), (60, -60), bend=(10, -90), w0=V(1.05))] + \
        yue(into((320, -60, 890, 500)))


def c_zai():                   # 在
    with han.weight(0.92):
        x = han.on_pie((470, 880), (70, 160), (10, -50), 500)[0] + 50
        return [heng(56, 944, 650), pie((470, 880), (70, 160), bend=(10, -50), w0=V(1.05)),
                shu(x, 500, -70, top="head", end="dew")] + tu(into((400, -50, 930, 500)))


def c_zuo():                   # 作
    return lr(ren_left, zha, (330, -60, 945, 880), 0.9)


def c_dong():                  # 动
    return lr(yun_left, li, (460, -60, 945, 880))


def c_gao():                   # 高
    return _w(0.88, lambda: [dian((460, 910), (540, 830)), heng(56, 944, 760)] + KOU_(ID, 320, 680, 630, 470, foot=30)
              + [shu(140, 360, -70, top="head", end="dew"), HZG_(ID, 140, 860, 360, -60)]
              + KOU_(ID, 360, 640, 230, 50, foot=30))


def c_dian():                  # 点
    return _w(0.9, lambda: [shu(430, 880, 560, top="head", end="hid"), heng(430, 770, 720, entry=None, beak=0.6)]
              + KOU_(ID, 230, 770, 560, 260, foot=30)
              + [dian((180, 130), (110, -30), w=V(1.05)), dian((380, 130), (410, -30), w=V(1.05)),
                 dian((600, 130), (650, -30), w=V(1.05)), dian((810, 140), (900, -30), w=V(1.1))])


def c_xing():                  # 行
    return lr(chi_left, chu, (380, -60, 945, 880))


def c_jing():                  # 经
    return lr(si_left, jing_r, (380, -60, 945, 880), 0.9)


def c_dang():                  # 当
    with han.weight(0.92):
        return [dian((230, 830), (310, 700)), shu(500, 880, 560, top="head", end="hid"),
                pie((790, 860), (650, 690), w0=V(0.95)),
                han.hengzhe(160, 820 + han.V / 2, 560, 0, end="hid"),
                heng(200, 820, 290, beak=False, right_hid=True), heng(100, 900, 0)]


def c_jin_enter():             # 进
    return bao(zou, jing_well, (330, 220, 920, 900), 0.9)


def c_dao():                   # 到
    return lr(zhi_left, dao_right, (600, -60, 945, 880), 0.9)


def c_shuo():                  # 说
    return lr(yan_left, dui, (340, -60, 945, 880), 0.9)


def c_zhi_know():              # 知
    return lr(shi_arrow, kou, (450, 40, 930, 760), 0.9)


def c_jian_see():              # 见
    return jian_see()


def c_xian():                  # 现
    return lr(wang_left, jian_see, (360, -60, 945, 880), 0.9)


def c_yong():                  # 用
    with han.weight(0.92):
        return yong()


def c_ming():                  # 名
    with han.weight(0.92):
        return xi_(into((60, 280, 840, 890))) + KOU_(ID, 330, 790, 360, -40)


def c_duo():                   # 多
    return _w(0.92, lambda: xi_(into((130, 430, 740, 890))) + xi_(into((170, -70, 930, 470))))


def c_wai():                   # 外
    return lr(lambda m=ID: xi_(into((40, -70, 520, 880))), bu_right, (520, -60, 945, 880))


def bu_right(m=ID):
    """卜（外 的右边）"""
    return [S_(m, 400, 880, -70, top="head", end="dew"), D_(m, (520, 600), (700, 420), w=V(1.0))]


GLYPHS = {
    "去": lambda: qu(), "可": lambda: ke(), "还": c_huan, "地": c_di, "问": c_wen_ask, "间": c_jian,
    "给": c_gei, "从": c_cong, "回": c_hui_back, "国": c_guo, "但": c_dan_but, "里": c_li_inside,
    "后": c_hou, "同": c_tong, "开": c_kai, "无": c_wu, "于": c_yu, "手": c_shou_hand, "正": c_zheng,
    "头": c_tou, "年": c_nian,
    "么": c_me, "公": c_gong_public, "分": c_fen, "之": c_zhi_of, "学": c_xue, "定": c_ding, "是": c_shi_is,
    "有": c_you_have, "在": c_zai, "作": c_zuo, "动": c_dong, "高": c_gao, "点": c_dian, "行": c_xing,
    "经": c_jing, "当": c_dang, "进": c_jin_enter, "到": c_dao, "说": c_shuo, "知": c_zhi_know,
    "见": c_jian_see, "现": c_xian, "用": c_yong, "名": c_ming, "多": c_duo, "外": c_wai,
}
