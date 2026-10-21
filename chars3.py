"""渡言的常用字（第三批）：按使用频率挑的高频字。新笔画斜钩、竖提、横折弯钩、横斜钩、竖弯在 han.py 里，
能用部件拼的照样拼（拼法见 chars.py 的 lr、tb、bao）。"""
import han
from chars import _w, bao, dong, ji, lr, tb, zhu_top
from chars2 import dao_right, zou_di
from han import (dian, heng, hengpie, hengxiegou, hengzhegou, hengzhewangou, na, pie, piedian, piezhe, shu, shupie,
                 shuti, shuwan, shuwangou, ti, tilted, xiegou, _kou)
from parts import (FULL, ID, D_, H_, INNER_, KOU_, P_, S_, SG_, he_left, hua, into, ke, li, mian, mu_left, ren_left,
                   she, tian_, wang_left, xin_left, yan_left, yue, yuan, zao, zou)

V = lambda k=1.0: han.V * k      # noqa: E731


def pie_at_x(p0, p1, bend, x):
    """撇的中心线横坐标为 x 的那一点：竖、横接在撇上时用来定位。"""
    seg = han.pie_seg(p0, p1, bend)
    return han._bz(seg, han._solve(lambda t: han._bz(seg, t)[0], 0, 1, x))


# ───────── 部件 ─────────

def ji_few(m=ID):
    """几"""
    return [shupie(m.x(300), m.y(820), m.x(50), m.y(-50), head="cut"),
            hengzhewangou(m.x(300), m.x(640) + han.V / 2, m.y(760), m.y(-30), m.x(935), entry=None,
                          hook=74 * m.k, r_in=90 * m.k, r_out=120 * m.k)]


def li_stand(m=ID):
    """立"""
    return [D_(m, (370, 880), (450, 720), w=V(1.1)), H_(m, 100, 900, 590),
            D_(m, (250, 500), (360, 170), w=V(1.05)), P_(m, (760, 490), (550, 40), w0=V(0.9)), H_(m, 56, 944, 30)]


def zhong(m=ID):
    """中"""
    return KOU_(m, 170, 830, 610, 220) + [S_(m, 500, 852, -80, end="needle")]


def li_in(m=ID):
    """里"""
    return KOU_(m, 200, 800, 820, 400) + [INNER_(m, 200, 800, 610), S_(m, 500, 820, 200, top="hid", end="hid"),
                                         H_(m, 170, 830, 200, beak=0.7), H_(m, 56, 944, -40)]


def li_left(m=ID):
    """力（加 的左边）"""
    return li(into((50, -70, 500, 880)))


def kou_tall(m=ID):
    """加 右边的口：窄长、偏下"""
    return KOU_(m, 230, 770, 660, 110, foot=60)


def shou_head(m=ID):
    """首（道 里面那个）"""
    return [D_(m, (300, 900), (370, 820), w=V(1.0)), P_(m, (760, 910), (650, 820), w0=V(0.9)),
            H_(m, 56, 944, 660), P_(m, (520, 665), (455, 515), w0=V(0.8), head="hid"),
            *KOU_(m, 220, 780, 505, -40), INNER_(m, 220, 780, 330), INNER_(m, 220, 780, 145)]


def yang(m=ID):
    """羊"""
    return [D_(m, (290, 880), (390, 740), w=V(1.0)), P_(m, (770, 890), (650, 740), w0=V(0.9)),
            H_(m, 110, 890, 630), H_(m, 160, 840, 400, beak=0.7), H_(m, 56, 944, 170),
            S_(m, 500, 630, -70, top="hid", end="dew")]


def qing(m=ID):
    """青"""
    return [H_(m, 150, 850, 790), S_(m, 500, 880, 600, end="hid"), H_(m, 220, 780, 690, beak=0.6),
            H_(m, 56, 944, 600)] + yue(m.into((170, -70, 830, 510)))


def xin_di(m=ID):
    """扁的心字底（意 的下面）：在 (60, −70, 940, 260) 这样的扁框里设计，点不会被压成一团。"""
    d = m.into(FULL, (60, -70, 940, 260))
    return [D_(d, (100, 210), (160, 60), w=V(0.95)),
            han.wogou(d.x(260), d.y(240), d.x(470), d.y(-55), d.x(820), d.y(-5), wb=V(0.85)),
            D_(d, (440, 250), (500, 130), w=V(0.9)), D_(d, (800, 240), (900, 90), w=V(1.0))]


def niu(m=ID):
    """牛（件 的右边）"""
    p0, p1 = (420, 840), (130, 430)
    x0 = han.on_pie(m.p(p0), m.p(p1), (0, 0), m.y(620))[0]
    return [P_(m, p0, p1, w0=V(0.95)), heng(x0, m.x(900), m.y(620), entry=None),
            H_(m, 56, 944, 330), S_(m, 600, 880, -70)]


def ren9(m=ID):
    """壬（任 的右边）"""
    p0, p1 = (900, 860), (260, 700)
    y = han.on_pie(m.p(p0), m.p(p1), (0, -10), m.y(760))
    return [P_(m, p0, p1, bend=(0, -10), w0=V(0.9)), H_(m, 100, 900, 420),
            shu(m.x(560), m.y(780), m.y(20), end="hid"), H_(m, 56, 944, 20)]


def si_temple(m=ID):
    """寺（等 的下面）"""
    return [S_(m, 500, 880, 560, end="hid"), H_(m, 180, 820, 720), H_(m, 56, 944, 560),
            H_(m, 80, 920, 330), SG_(m, 640, 560, -60, top="hid"), D_(m, (300, 230), (410, 90))]


def guang_(m=ID):
    """广"""
    return [D_(m, (450, 890), (540, 740)), H_(m, 170, 930, 700, entry=None),
            shupie(m.x(170), m.y(740), m.x(40), m.y(-50), head="cut")]


# ───────── 第一组：新笔画的字 ─────────

def c_wo():                    # 我
    return [pie((470, 840), (70, 700), bend=(0, -10), w0=V(0.9)),
            heng(56, 944, 560),
            han.shugou(340, 760, -40, dx=-150, dy=90),
            ti((100, 260), (560, 450), w0=V(1.0)),
            xiegou((600, 870), (860, -20), end=308),
            pie((850, 440), (400, 50), bend=(-20, -20), w0=V(0.95)),
            dian((700, 820), (800, 690), w=V(1.05))]


def c_min():                   # 民
    return [shuti(215, 800, 40, (530, 190)),
            han.hengzhe(215, 800 + V() / 2, 760, 520),
            heng(215, 800, 590, beak=False, entry=None, right_hid=True),
            heng(215, 944, 390, entry=None),
            xiegou((500, 590), (850, 10), end=315, top="hid")]


def c_chang():                 # 长
    return [pie((800, 800), (345, 515), bend=(-30, -20), w0=V(0.95)),
            shuti(310, 860, -10, (580, 170)),
            heng(56, 944, 440),
            na((440, 440), (870, 70), bend=(-30, -40), wmax=V(1.15))]


def c_yi_by():                 # 以
    return [shuti(230, 810, 50, (560, 380)),
            dian((390, 790), (500, 580), w=V(1.1)),
            shupie(780, 870, 160, -60, head="cut"),
            dian((690, 250), (870, 10), w=V(1.15))]


def c_ji_few():                # 几
    return ji_few()


def c_jiu():                   # 九
    return [shupie(430, 870, 60, -60, w0=V(1.05), head="cut"),
            hengzhewangou(80, 680, 590, -30, 935, lean=20, r_in=90, r_out=120)]


def c_cheng():                 # 成
    return [heng(240, 944, 640, entry=None),
            shupie(240, 690, 40, -60, head="cut"),
            hengzhegou(240, 500, 450, 170, dx=-150, dy=80),
            xiegou((570, 880), (850, -20), end=305),
            pie((860, 520), (380, -40), bend=(-20, -30), w0=V(0.95)),
            dian((690, 870), (790, 770), w=V(1.0))]


def c_fa_send():               # 发
    return [piezhe((300, 800), (150, 560), (930, 560), w=V(0.86), end="beak"),
            pie((470, 770), (60, 0), bend=(-30, -60), w0=V(1.0)),
            dian((700, 830), (810, 690), w=V(1.0)),
            hengpie(330, 760, 450, (110, -40), bend=(40, -40), w0=V(0.95), entry=None),
            na((470, 452), (850, 30), bend=(-20, -40), wmax=V(1.15))]


def c_wei():                   # 为
    return [dian((250, 790), (370, 630), w=V(1.0)),
            pie((520, 880), (60, -50), bend=(-20, -60), w0=V(1.05)),
            hengzhegou(110, 912, 550, -30, dx=-160, dy=80),
            dian((560, 400), (660, 220), w=V(1.1))]


def c_lao():                   # 老
    p0, p1, bend = (860, 800), (40, 60), (-20, -40)
    y = pie_at_x(p0, p1, bend, 390)[1]
    return [heng(140, 640, 670), shu(330, 870, 480, end="hid"), heng(56, 944, 480),
            pie(p0, p1, bend=bend, w0=V(1.0)),
            pie((780, 330), (370, 200), w0=V(0.85)),
            shuwangou(390, y + 10, -30, 930)]


def c_ji_machine():            # 机
    return lr(mu_left, ji_few, (380, -60, 945, 880))


def c_bi_compare():            # 比
    return [shuti(170, 850, 10, (480, 180)), heng(170, 470, 510, entry=None, beak=0.5),
            pie((900, 640), (600, 400), w0=V(0.95)), shuwangou(620, 850, -20, 950)]


def c_ci():                    # 此
    return [shu(335, 860, 90, end="hid"), heng(335, 530, 455, entry=None, beak=0.5),
            shu(150, 650, 40, end="hid"), ti((100, 10), (530, 160), w0=V(1.0)),
            pie((890, 590), (640, 380), w0=V(0.95)), shuwangou(630, 860, -20, 950)]


def c_dai():                   # 代
    return lr(ren_left, lambda m: [tilted(H_(m, 56, 920, 470), 6, m.x(56), m.y(470)),
                                   xiegou(m.p((380, 880)), m.p((830, -40)), end=302),
                                   D_(m, (640, 830), (780, 690))], (300, -60, 945, 880))


def c_huo():                   # 或
    return [heng(56, 944, 650), *KOU_(ID, 140, 410, 520, 280, foot=30),
            ti((100, 30), (560, 170), w0=V(1.0)),
            xiegou((570, 880), (860, -30), end=305),
            pie((870, 500), (600, 80), w0=V(0.9)),
            dian((700, 830), (800, 700))]


def c_si_four():               # 四
    return _kou(150, 840, 770, 120, foot=130) + [
        shupie(400, 770, 200, 200, head="hid"),
        shuwan(580, 770, 270, 740)]


def c_xi_west():               # 西
    return [heng(56, 944, 790)] + _kou(170, 840, 600, 90, foot=100) + [
        shupie(400, 790, 220, 230, head="hid"),
        shuwan(590, 790, 270, 740, r_in=40)]


def c_qi_air():                # 气
    return [pie((300, 880), (60, 470), bend=(-10, -20), w0=V(0.95)),
            heng(han.on_pie((300, 880), (60, 470), (-10, -20), 740)[0], 900, 740, entry=None),
            heng(270, 780, 590, beak=0.6),
            hengxiegou(150, 740, 440, (870, -40), end=298)]


def c_xie_some():              # 些
    return _w(0.92, lambda: [
        shu(230, 740, 330, end="hid"), ti((100, 270), (510, 430), w0=V(0.95)),
        shu(330, 860, 370, end="hid"), heng(330, 520, 610, entry=None, beak=0.5),
        pie((860, 750), (620, 570), w0=V(0.85)), shuwangou(610, 860, 380, 910),
        heng(230, 800, 190, beak=0.7), heng(56, 944, 10)])


def c_bei():                   # 北
    return [shu(385, 850, -50), heng(90, 385, 560, beak=False, right_hid=True),
            ti((100, 130), (385, 250), w0=V(1.0)),
            pie((860, 680), (640, 470), w0=V(0.85)), shuwangou(610, 850, -30, 950)]


def c_dian_elec():             # 电
    return _kou(180, 780, 650, 270, foot=80) + [heng(180, 780, 460, beak=False, entry=None, right_hid=True),
                                                 shuwangou(470, 880, -30, 950)]


def c_qi_seven():              # 七
    return [tilted(heng(50, 940, 440), 10, 495, 440), shuwangou(450, 860, -30, 950)]


def c_guang():                 # 光
    return [shu(500, 870, 470, end="hid"), dian((200, 780), (320, 600), w=V(1.0)),
            pie((810, 730), (650, 540), w0=V(0.9)), heng(56, 944, 470),
            shupie(280, 470, 50, -50, head="hid"), shuwangou(610, 470, -30, 950, top="hid")]


def c_xian_first():            # 先
    return [pie((350, 830), (150, 470), w0=V(0.9)), heng(han.on_pie((350, 830), (150, 470), (0, 0), 650)[0], 860, 650, entry=None),
            shu(520, 880, 430, end="hid"), heng(56, 944, 430),
            shupie(350, 430, 60, -50, head="hid"), shuwangou(720, 430, -30, 950, top="hid")]


# ───────── 第二组：现成部件拼的字 ─────────

def c_ba():                    # 八
    return [pie((380, 780), (40, -40), bend=(60, -60), w0=V(1.05)),
            na((560, 840), (830, 30), bend=(-80, 0), wmax=V(1.18), start="tip")]


def c_er_child():              # 儿
    return [shupie(350, 830, 40, -40, head="cut"), shuwangou(600, 830, -20, 950)]


def c_ru():                    # 入
    p0, p1, bend = (330, 840), (850, -10), (-40, -60)
    return [na(p0, p1, bend=bend, wmax=V(1.2), w0=50, start="tip"),
            pie((480, 560), (50, -40), bend=(-20, -30), head="round", w0=V(0.85))]


def c_qian():                  # 千
    p0, p1 = (860, 860), (200, 690)
    y = pie_at_x(p0, p1, (0, -10), 500)[1]
    return [pie(p0, p1, bend=(0, -10), w0=V(0.9)), heng(56, 944, 470), shu(500, y + 10, -60)]


def c_bai_hundred():           # 百
    return [heng(56, 944, 780), pie((470, 775), (400, 600), w0=V(0.8), head="hid")] + \
        _kou(225, 775, 570, 90, foot=120) + [heng(225, 775, 330, beak=False, entry=None, right_hid=True)]


def c_bai():                   # 白
    return [pie((450, 880), (380, 640), w0=V(0.85))] + _kou(210, 800, 630, 80, foot=120) + \
        [heng(210, 800, 370, beak=False, entry=None, right_hid=True)]


def c_wei_pos():               # 位
    return lr(ren_left, li_stand, (330, -60, 945, 880))


def c_zhong_kind():            # 种
    return lr(he_left, zhong, (370, -70, 945, 880))


def c_li_profit():             # 利
    return lr(he_left, dao_right, (620, -60, 945, 880), lsx=1.5)


def c_li_reason():             # 理
    return lr(wang_left, li_in, (340, -60, 945, 880), 0.9)


def c_hua_talk():              # 话
    return lr(yan_left, she, (340, -60, 945, 880), 0.9)


def c_jia():                   # 加
    return lr(li_left, kou_tall, (600, -40, 940, 790))


def c_tai():                   # 太
    start = han.on_pie((510, 880), (50, -40), (10, -90), 480)
    return [heng(56, 944, 560), pie((510, 880), (50, -40), bend=(10, -90), w0=V(1.1)),
            na(start, (840, -10), bend=(30, -10)), dian((420, 260), (540, 90), w=V(1.05))]


def c_shao():                  # 少
    return [shu(515, 880, 280), pie((380, 650), (80, 280), w0=V(0.95)), dian((640, 700), (870, 520), w=V(1.1)),
            pie((800, 400), (40, -40), bend=(-60, -80), w0=V(1.05))]


def c_ping():                  # 平
    return [heng(100, 900, 760), dian((200, 690), (300, 500), w=V(1.0)), pie((830, 670), (620, 450), w0=V(0.9)),
            heng(56, 944, 380), shu(500, 760, -60, top="hid")]


def c_wu_five():               # 五
    return [heng(80, 900, 750), tilted(shu(390, 750, 60, top="hid", end="hid"), -5, 390, 750),
            han.hengzhe(140, 760, 480, 60, end="hid"), heng(56, 944, 60)]


def c_liu():                   # 六
    return [dian((420, 880), (530, 700), w=V(1.1)), heng(56, 944, 560),
            pie((390, 440), (60, -40), bend=(-10, -20), w0=V(1.0)), dian((560, 430), (850, 20), w=V(1.15))]


def c_wan_10k():               # 万
    return [heng(56, 944, 760), hengzhegou(440, 830, 520, 30, dx=-180, dy=90),
            shupie(440, 760, 50, -40, head="hid")]


def c_cai():                   # 才
    return [heng(56, 944, 600), han.shugou(610, 880, -60, dx=-170, dy=90),
            pie((590, 560), (60, 40), bend=(-40, -60), head="hid")]


# ───────── 第三组 ─────────

def c_yao():                   # 要
    return _w(0.92, lambda: [heng(56, 944, 790)] + _kou(210, 800, 650, 510, foot=30) + [
        shu(370, 790, 510, top="hid", end="hid"), shu(620, 790, 510, top="hid", end="hid"),
        piedian((380, 410), (230, 170), (800, -40)), pie((720, 415), (70, -50), bend=(-30, -30), w0=V(0.95)),
        heng(56, 944, 290)])


def c_dao_way():               # 道
    return bao(zou, shou_head, (345, 150, 930, 880))


def c_yang_kind():             # 样
    return lr(mu_left, yang, (380, -70, 945, 880))


def c_shi_real():              # 实
    return mian() + [dian((310, 590), (390, 510), w=V(0.95)), dian((240, 460), (320, 390), w=V(0.95)),
                     heng(56, 944, 270), pie((740, 600), (80, -50), bend=(10, -80), w0=V(1.0)),
                     dian((580, 160), (820, -30), w=V(1.15))]


def c_zhe_one():               # 者
    return [shu(390, 880, 520, end="hid"), heng(160, 600, 700), heng(56, 944, 520),
            pie((830, 770), (60, 160), bend=(-30, -30), w0=V(1.0))] + _kou(320, 720, 360, 40, foot=90) + \
        [heng(320, 720, 200, beak=False, entry=None, right_hid=True)]


def c_yi_idea():               # 意
    def top(m):
        return [dian((455, 915), (525, 850), w=V(1.0)), heng(110, 890, 740),
                dian((300, 725), (330, 690), w=V(0.75)), pie((700, 725), (670, 680), w0=V(0.7)),
                heng(56, 944, 595)] + KOU_(m, 250, 750, 475, 320, foot=34) + [INNER_(m, 250, 750, 397)]
    return tb(top, xin_di, (70, -70, 930, 260), 0.88)


def c_yu_give():               # 与
    return [han.shuzhezhegou(300, 880, 440, 820, -40, dx=-150, dy=90, top="head"),
            heng(300, 930, 680, entry=None), heng(56, 944, 230)]


def c_yi_already():            # 已
    return [han.hengzhe_heng(200, 748 + V() / 2, 760, 470, 192), shuwangou(222, 640, -30, 900)]


def c_qing():                  # 情
    return lr(xin_left, qing, (330, -70, 945, 880), 0.9)


def c_guan():                  # 关
    start = han.on_pie((500, 600), (50, -40), (10, -60), 400)
    return [dian((250, 870), (330, 720), w=V(1.0)), pie((790, 860), (660, 700), w0=V(0.9)),
            heng(150, 850, 600), heng(56, 944, 390),
            pie((500, 600), (50, -40), bend=(10, -60), head="hid", w0=V(1.05)),
            na(start, (850, -10), bend=(30, -20))]


def c_ye_work():               # 业
    return [shu(400, 860, 30, end="hid"), shu(600, 860, 30, end="hid"),
            dian((150, 620), (250, 240), w=V(1.0)), pie((880, 600), (640, 100), w0=V(0.95)),
            heng(56, 944, 20)]


def c_liang():                 # 两
    return [heng(56, 944, 780), shu(177, 640, -40), hengzhegou(177, 889, 600, -30, dx=-150, dy=80),
            shupie(340, 780, 210, 140, w0=V(0.85), head="hid"), dian((350, 410), (430, 230), w=V(0.95)),
            shupie(600, 780, 450, 110, w0=V(0.85), head="hid"), dian((610, 410), (690, 230), w=V(0.95))]


def c_you_from():              # 由
    return _kou(205, 825, 610, 60, foot=110) + [heng(205, 825, 335, beak=False, entry=None, right_hid=True),
                                                 shu(510, 870, 60, end="hid")]


def c_bing():                  # 并
    return [dian((280, 870), (390, 690), w=V(1.05)), pie((800, 860), (640, 700), w0=V(0.9)),
            heng(110, 890, 630), heng(56, 944, 360),
            shupie(320, 630, 40, -40, head="hid"), shu(650, 630, -50, top="hid")]


def c_ying():                  # 应
    return guang_() + [dian((300, 520), (390, 240), w=V(1.0)), dian((470, 610), (540, 370), w=V(1.0)),
                       pie((850, 540), (600, 40), w0=V(0.95)), heng(200, 944, 30)]


def c_xiang_to():              # 向
    return [pie((450, 880), (370, 650), w0=V(0.85)), shu(177, 700, -40),
            hengzhegou(177, 862, 660, -30, dx=-150, dy=80)] + _kou(370, 620, 480, 240, foot=30)


def c_guo_fruit():             # 果
    return _kou(230, 770, 790, 470, foot=30) + [heng(230, 770, 630, beak=False, entry=None, right_hid=True),
                                                 shu(500, 790, -60, top="hid"), heng(56, 944, 360),
                                                 pie((500, 350), (60, 10), bend=(-30, -30), head="hid"),
                                                 na((530, 320), (850, 100), bend=(20, -20), wmax=V(1.1))]


def c_qi_its():                # 其
    return [heng(80, 920, 700), shu(330, 860, 250, end="hid"), shu(670, 860, 250, end="hid"),
            heng(330, 670, 545, beak=False, entry=None, right_hid=True),
            heng(330, 670, 395, beak=False, entry=None, right_hid=True),
            heng(56, 944, 250), pie((360, 140), (80, -60), w0=V(0.95)), dian((560, 150), (860, -40), w=V(1.15))]


def c_nei():                   # 内
    p0, p1, bend = (450, 880), (210, 160), (-10, -20)
    return [shu(90, 700, -40), hengzhegou(90, 842, 660, -40, dx=-150, dy=80),
            pie(p0, p1, bend=bend, w0=V(1.0)), dian(han.on_pie(p0, p1, bend, 480), (640, 280), w=V(1.05))]


def c_jin_gold():              # 金
    p0, p1, bend = (500, 880), (60, 400), (-20, -10)
    return [pie(p0, p1, bend=bend, w0=V(1.04)), na(han.on_pie(p0, p1, bend, 790), (860, 450), bend=(40, -10)),
            heng(250, 750, 460, beak=0.6), heng(140, 850, 300), shu(500, 460, 20, top="hid", end="hid"),
            dian((215, 230), (320, 150), w=V(1.0)), pie((770, 230), (600, 40), w0=V(0.85)), heng(56, 944, 20)]


# ───────── 第四组 ─────────

def c_zou_walk():              # 走
    return [heng(180, 820, 700), shu(500, 880, 500, end="hid"), heng(56, 944, 500)] + \
        zou_di(into((70, -60, 930, 581)), heng_top=False)


def c_qi_rise():               # 起
    return _w(0.92, lambda: [
        heng(110, 500, 680), shu(315, 880, 490, end="hid"), heng(56, 510, 490, beak=0.6),
        shu(320, 490, 210, top="hid"), heng(320, 500, 330, entry=None, beak=0.5),
        shupie(180, 400, 40, -50, w0=V(0.9), head="cut"),
        na((190, 225), (870, 10), bend=(-80, -110), wmax=V(1.1))] + ji(into((560, 200, 960, 760))))


def c_che():                   # 车
    return [heng(56, 944, 690), piezhe((480, 870), (250, 400), (850, 400), w=V(0.86), end="beak"),
            shu(505, 620, -60), heng(56, 944, 190)]


def c_shu_book():              # 书
    return [han.hengzhe(140, 720, 640, 400, end="hid"), hengzhegou(56, 840, 400, -20, dx=-150, dy=80),
            shu(465, 880, -60), dian((760, 820), (880, 680), w=V(1.0))]


def c_shi_market():            # 市
    return [dian((470, 920), (530, 820)), heng(56, 944, 680), shu(230, 550, 70),
            hengzhegou(230, 790, 510, 90, dx=-120, dy=70), shu(510, 680, -60, top="hid")]


def c_jian_item():             # 件
    return lr(ren_left, niu, (330, -70, 945, 880))


def c_gong_share():            # 共
    return [shu(370, 860, 300, end="hid"), shu(640, 860, 300, end="hid"), heng(100, 900, 610),
            heng(56, 944, 300), pie((450, 180), (60, -60), w0=V(0.95)), dian((600, 180), (880, -40), w=V(1.15))]


def c_zai():                   # 再
    return [heng(100, 900, 780), shu(245, 660, -40), hengzhegou(245, 807, 620, -40, dx=-150, dy=80),
            shu(507, 780, 450, top="hid", end="hid"), heng(245, 755, 450, beak=False, entry=None, right_hid=True),
            heng(56, 944, 260)]


def c_shi_world():             # 世
    return [heng(56, 944, 530), han.shuzhe(245, 790, 20, 944, right="beak"), han.nian_u(470, 700, 840, 240)]


def c_ren_task():              # 任
    return lr(ren_left, ren9, (330, -70, 945, 880))


def c_du_degree():             # 度
    return [dian((470, 910), (540, 790)), heng(200, 930, 720, entry=None), shupie(200, 770, 40, -60, head="cut"),
            heng(300, 930, 560, beak=0.8), han.nian_u(440, 690, 630, 440),
            hengpie(280, 780, 300, (150, -60), bend=(90, -40), w0=V(0.95)),
            na((390, 290), (850, -30), bend=(-60, -50), wmax=V(1.2), foot=0.75)]


def c_deng():                  # 等
    return tb(zhu_top, si_temple, (70, -70, 930, 590), 0.9)


def c_chan():                  # 产
    return [dian((470, 910), (540, 780)), heng(120, 900, 720), dian((290, 700), (365, 575), w=V(1.0)),
            pie((740, 675), (620, 530), w0=V(0.85)), heng(190, 944, 450, entry=None),
            shupie(190, 500, 40, -60, head="cut")]


def c_biao():                  # 表
    return _w(0.92, lambda: [
        heng(140, 860, 720), shu(500, 880, 430, end="hid"), heng(190, 810, 580, beak=0.7), heng(56, 944, 430),
        pie((470, 418), (70, 60), bend=(-20, -30), w0=V(0.9)),
        shuti(300, 240, -60, (560, 110)), pie((820, 330), (620, 170), w0=V(0.85)),
        na((530, 425), (860, 20), bend=(-30, -40))])


def c_chang_often():           # 常
    return _w(0.92, lambda: [
        shu(500, 880, 650, end="hid"), dian((250, 880), (320, 780)), pie((790, 880), (660, 760), w0=V(0.85)),
        dian((110, 760), (130, 620), w=V(1.0)), han.hook_down(130, 890, 650, entry=None)]
        + _kou(300, 700, 530, 390, foot=30)
        + [shu(200, 260, -40), hengzhegou(200, 840, 260, -30, dx=-130, dy=70), shu(500, 390, -70, top="hid")])


def c_yuan_origin():           # 原
    return [heng(220, 944, 770, entry=None), shupie(220, 820, 40, -60, head="cut"),
            pie((600, 775), (530, 650), w0=V(0.8), head="hid")] + _kou(400, 780, 640, 310, foot=30) + [
            heng(400, 780, 475, beak=False, entry=None, right_hid=True),
            han.shugou(570, 310, -60, top="hid", dx=-120, dy=80),
            pie((440, 205), (180, -10), w0=V(0.95)), dian((680, 220), (880, 30), w=V(1.1))]


def c_zhen():                  # 真
    return [heng(100, 900, 740), shu(507, 880, 610, end="hid")] + _kou(300, 740, 610, 270, foot=100) + [
            heng(300, 740, 495, beak=False, entry=None, right_hid=True),
            heng(300, 740, 380, beak=False, entry=None, right_hid=True),
            heng(56, 944, 160), pie((430, 150), (60, -60), w0=V(0.9)),
            dian((570, 150), (840, -30), w=V(1.15))]


def c_yi_just():               # 义
    return [dian((360, 860), (540, 640), w=V(1.15)), pie((810, 800), (50, -50), bend=(-60, -60), w0=V(1.05)),
            na((240, 740), (840, 0), bend=(30, -40), start="tip", wmax=V(1.2))]


def c_ge_each():               # 各
    p0, p1, bend = (380, 870), (90, 440), (-10, -10)
    return [pie(p0, p1, bend=bend, w0=V(1.0)),
            hengpie(han.on_pie(p0, p1, bend, 700)[0], 760, 700, (60, 250), bend=(60, -40), w0=V(0.95), entry=None),
            na((330, 690), (860, 400), bend=(20, -40))] + _kou(290, 750, 270, 20, foot=60)


def c_tiao():                  # 条
    p0, p1, bend = (380, 870), (130, 520), (-10, -10)
    return [pie(p0, p1, bend=bend, w0=V(1.0)),
            hengpie(han.on_pie(p0, p1, bend, 750)[0], 780, 750, (60, 380), bend=(60, -40), w0=V(0.95), entry=None),
            na((380, 740), (860, 450), bend=(20, -40)),
            heng(80, 860, 300), han.shugou(500, 470, -60, dx=-130, dy=80),
            pie((470, 260), (60, -20), w0=V(0.95), head="hid"), dian((610, 230), (840, 60), w=V(1.1))]


# ───────── 第五组 ─────────

def c_shui():                  # 水
    return [han.shugou(500, 880, -60, dx=-170, dy=90),
            hengpie(80, 405, 560, (50, 30), bend=(-30, 10), w0=V(1.0)),
            pie((850, 660), (545, 420), w0=V(0.95)),
            na((530, 600), (840, 110), bend=(-20, -40), wmax=V(1.2))]


def c_pin():                   # 品
    return _w(0.92, lambda: KOU_(ID, 250, 750, 790, 540, foot=30) + KOU_(ID, 130, 400, 380, 80, foot=60)
              + KOU_(ID, 590, 860, 380, 80, foot=60))


def c_shi_scholar():           # 士
    return [shu(500, 870, 40, end="hid"), heng(56, 944, 500), heng(130, 870, 40)]


def c_fu():                    # 夫
    p0, p1, bend = (500, 880), (60, -50), (10, -90)
    return [heng(160, 840, 650), heng(56, 944, 420), pie(p0, p1, bend=bend, w0=V(1.1)),
            na(han.on_pie(p0, p1, bend, 380), (850, -10), bend=(30, -10))]


def c_wei_not():               # 未
    return [heng(140, 860, 660), heng(56, 944, 450), shu(500, 880, -70),
            pie((480, 440), (70, 40), bend=(-20, -20), head="hid"),
            na((520, 430), (860, 110), bend=(20, -10), wmax=V(1.1))]


def c_shi_lose():              # 失
    p0, p1 = (340, 820), (80, 400)
    return [pie(p0, p1, w0=V(0.9)), heng(han.on_pie(p0, p1, (0, 0), 620)[0], 900, 620, entry=None),
            heng(56, 944, 400), shupie(550, 880, 60, -60, head="cut"),
            na((540, 380), (840, 0), bend=(20, -20))]


def c_gao_tell():              # 告
    p0, p1 = (340, 840), (110, 480)
    return [pie(p0, p1, w0=V(0.95)), heng(han.on_pie(p0, p1, (0, 0), 650)[0], 840, 650, entry=None),
            shu(520, 880, 430, end="hid"), heng(56, 944, 430)] + _kou(275, 755, 280, 20, foot=60)


def c_he_what():               # 何
    return lr(ren_left, ke, (330, -60, 945, 880), 0.9)


GLYPHS = {
    "我": c_wo, "民": c_min, "长": c_chang, "以": c_yi_by, "几": c_ji_few, "九": c_jiu,
    "成": c_cheng, "发": c_fa_send, "为": c_wei, "老": c_lao, "机": c_ji_machine, "比": c_bi_compare,
    "此": c_ci, "代": c_dai, "或": c_huo, "四": c_si_four, "西": c_xi_west, "气": c_qi_air, "些": c_xie_some,
    "北": c_bei, "电": c_dian_elec, "七": c_qi_seven, "光": c_guang, "先": c_xian_first, "化": lambda: hua(),
    "元": lambda: yuan(), "东": lambda: dong(), "己": lambda: ji(), "早": lambda: zao(), "田": lambda: tian_(),
    "八": c_ba, "儿": c_er_child, "入": c_ru, "千": c_qian, "百": c_bai_hundred, "白": c_bai, "立": lambda: li_stand(),
    "位": c_wei_pos, "种": c_zhong_kind, "利": c_li_profit, "理": c_li_reason, "话": c_hua_talk, "加": c_jia,
    "太": c_tai, "少": c_shao, "平": c_ping, "五": c_wu_five, "六": c_liu, "万": c_wan_10k, "才": c_cai,
    "要": c_yao, "道": c_dao_way, "样": c_yang_kind, "实": c_shi_real, "者": c_zhe_one, "意": c_yi_idea,
    "与": c_yu_give, "已": c_yi_already, "情": c_qing, "关": c_guan, "业": c_ye_work, "两": c_liang,
    "由": c_you_from, "并": c_bing, "应": c_ying, "向": c_xiang_to, "果": c_guo_fruit, "其": c_qi_its,
    "内": c_nei, "金": c_jin_gold,
    "走": c_zou_walk, "起": c_qi_rise, "车": c_che, "书": c_shu_book, "市": c_shi_market, "件": c_jian_item,
    "共": c_gong_share, "再": c_zai, "世": c_shi_world, "任": c_ren_task, "度": c_du_degree, "等": c_deng,
    "产": c_chan, "表": c_biao, "常": c_chang_often, "原": c_yuan_origin, "真": c_zhen, "义": c_yi_just,
    "各": c_ge_each, "条": c_tiao,
    "水": c_shui, "品": c_pin, "士": c_shi_scholar, "夫": c_fu, "未": c_wei_not, "失": c_shi_lose, "告": c_gao_tell,
    "何": c_he_what,
}
