"""渡言的常用字（第四批）：按使用频率挑的高频字，规矩和第一批一样：
笔画多的字整体减细（6 条轮廓 0.92，7～9 条 0.9，10 条以上 0.88，左右、上下拼的字由 lr()、tb() 减细），
钩用默认长度，口字框的脚 30～44。"""
import han
from chars import _w, bao, lr, tb, zhu_top
from chars2 import chi_left, dao_right, jian_see, xi_, xue_top, yong, zou_di
from chars3 import li_in, li_stand, pie_at_x, qing, si_temple, xin_di
from han import (dian, heng, hengxiegou, hengzhe, hengzhe_heng, hengzhegou, hengzhewangou, hook_down, na, pie, piedian,
                 piezhe, shu, shugou, shupie, shuti, shuzhe, shuzhezhegou, ti, tilted, wogou, xiegou, _kou)
from parts import (ID, D_, H_, HP_, HZG_, INNER_, KOU_, N_, P_, S_, SG_, SWG_, T_, gu, he_left, into, kou_left, mian,
                   da, fu_left, li, mu, mu_left, qu, ren_left, ren_top, shou, si_left, shui, tian_, tu, wang, yan_left,
                   you, you_left, yuan, yue, zou)

V = lambda k=1.0: han.V * k      # noqa: E731


# ───────── 第一组的部件 ─────────

def fu_right(m=ID):
    """阝（右耳刀：那、部、都）：左边一竖，右边一个「3」形的横撇弯钩，两头都接在竖上（同左耳刀）。"""
    return [S_(m, 200, 872, -70, top="head", end="dew"),
            HP_(m, 200, 720, 830, (240, 620), bend=(-10, 0), w0=V(0.8), entry=None),
            pie(m.p((220, 610)), m.p((360, 170)), w0=V(0.9), head="hid",
                seg=(m.p((220, 610)), m.p((1120, 590)), m.p((1080, 190)), m.p((360, 170))))]


def pu(m=ID, na_end=(760, -40)):
    """攵（反文：政、做、放、改、收 的右边）。压得很窄时（做）捺会变陡、捺脚往右冲，na_end 往里收。"""
    p0, p1 = (430, 880), (250, 540)
    x0 = han.on_pie(m.p(p0), m.p(p1), (0, 0), m.y(660))[0]
    return [P_(m, p0, p1, w0=V(0.95)), heng(x0, m.x(944), m.y(660), entry=None),
            P_(m, (760, 662), (100, -60), bend=(-30, -60), head="hid", w0=V(1.0)),
            N_(m, (360, 650), na_end, bend=(-70, -150))]


def jin_axe(m=ID):
    """斤（所、听、近、新 的右边）"""
    return [P_(m, (900, 870), (330, 760), bend=(0, -10), w0=V(0.9)),
            shupie(m.x(330), m.y(770), m.x(60), m.y(-60), head="cut", w0=V(0.95)),
            heng(m.x(330), m.x(944), m.y(470), entry=None),
            S_(m, 700, 470, -70, top="hid")]


def gen(m=ID):
    """艮（很、眼、根、退 的右边）：上面一个两格的框，左竖写成竖提，右下一撇一捺。"""
    return [shuti(m.x(260), m.y(820) + 40, m.y(-30), m.p((560, 110))),
            hengzhe(m.x(260), m.x(760) + han.V / 2, m.y(820), m.y(400) - 34),
            INNER_(m, 260, 760, 610), INNER_(m, 260, 760, 400),
            P_(m, (900, 330), (590, 110), w0=V(0.85)),
            N_(m, (380, 395), (800, -30), bend=(-20, -50))]


def bei(m=ID):
    """贝（员、则）：冂 里一撇出框，右下一个长点。"""
    return [han.shu(m.x(200), m.y(820) + 40, m.y(420)), HZ_(m, 200, 800, 820, 300),
            P_(m, (500, 795), (80, -60), bend=(-20, -40), w0=V(0.95)),
            D_(m, (560, 230), (860, -40), w=V(1.15))]


def bei_left(m=ID):
    """贝（则 的左边）"""
    return bei(into((40, -70, 470, 880)))


def zheng_left(m=ID):
    """正（政 的左边）：底横变成提。"""
    return [H_(m, 60, 430, 780, beak=0.5), S_(m, 250, 780, 165, top="hid", end="hid"),
            H_(m, 250, 430, 460, entry=None, beak=0.5), S_(m, 110, 560, 95, end="hid"),
            T_(m, (90, 80), (440, 220))]


def fang_left(m=ID):
    """方（放 的左边）"""
    return [D_(m, (230, 905), (285, 805)), H_(m, 50, 460, 680), HZG_(m, 170, 380, 500, -40),
            P_(m, (200, 680), (40, -50), bend=(-10, -20), head="hid")]


def ji_left(m=ID):
    """己（改 的左边）：竖弯钩变成竖提。"""
    return [han.hengzhe_heng(m.x(70), m.x(380) + han.V / 2, m.y(780), m.y(480), m.x(120) - han.V / 2 - 22),
            shuti(m.x(120), m.y(480), m.y(60), m.p((440, 230)), top="hid")]


def shou_left(m=ID):
    """丩（收 的左边）：短的竖提接到长竖上。"""
    return [shuti(m.x(110), m.y(700), m.y(170), m.p((320, 330)), w=V(0.9)), S_(m, 300, 880, -60)]


def hu_left(m=ID):
    """户（所 的左边）"""
    return [P_(m, (440, 880), (90, 790), bend=(0, -10), w0=V(0.85)),
            shupie(m.x(160), m.y(740), m.x(60), m.y(-60), head="cut", w0=V(0.9)),
            hengzhe(m.x(160), m.x(410) + han.V / 2, m.y(600), m.y(290)),
            INNER_(m, 160, 410, 380)]


def qin_left(m=ID):
    """亲（新 的左边）：立 + 木，木的捺写成点。"""
    return [D_(m, (220, 905), (280, 800)), H_(m, 60, 420, 740, beak=0.5),
            D_(m, (110, 725), (130, 660), w=V(0.75)), P_(m, (370, 725), (340, 660), w0=V(0.7)),
            H_(m, 40, 450, 560, beak=0.5), H_(m, 60, 440, 390, beak=0.5),
            han.shugou(m.x(250), m.y(560), m.y(-40), top="hid"),
            P_(m, (250, 350), (40, 60), w0=V(0.8), head="hid"), D_(m, (280, 340), (420, 160), w=V(0.9))]


def na_left(m=ID):
    """那 的左边：横折钩、两横、竖撇。"""
    return [HZG_(m, 90, 470, 790, -20), H_(m, 70, 470, 580, beak=False, right_hid=True),
            H_(m, 60, 470, 380, beak=False, right_hid=True),
            shupie(m.x(250), m.y(580), m.x(50), m.y(-40), head="hid")]


def bu_left(m=ID):
    """部 的左边：立 + 口"""
    return [D_(m, (270, 905), (330, 790)), H_(m, 70, 500, 730, beak=0.5),
            D_(m, (150, 715), (185, 620), w=V(0.85)), P_(m, (430, 715), (385, 620), w0=V(0.75)),
            H_(m, 40, 540, 500, beak=0.5)] + KOU_(m, 110, 450, 350, 30, foot=30)


def zhe(m=ID):
    """者（都 的左边，也可整字用）"""
    return [S_(m, 390, 880, 520, end="hid"), H_(m, 160, 600, 700), H_(m, 56, 944, 520),
            P_(m, (830, 770), (60, 160), bend=(-30, -30), w0=V(1.0))] + KOU_(m, 320, 720, 360, 0) + \
        [INNER_(m, 320, 720, 180)]


def mu_eye(m=ID):
    """目（眼 的左边）：窄长。"""
    return KOU_(m, 110, 310, 800, 60, foot=30) + [INNER_(m, 110, 310, 540), INNER_(m, 110, 310, 300)]


def ji_rice(m=ID):
    """即 的左边：白 一样的框，左竖写成竖提，右下一点。"""
    return [shuti(m.x(130), m.y(820) + 40, m.y(70), m.p((470, 220))),
            hengzhe(m.x(130), m.x(400) + han.V / 2, m.y(820), m.y(460) - 34),
            INNER_(m, 130, 400, 630), INNER_(m, 130, 400, 460),
            D_(m, (290, 360), (420, 160), w=V(1.0))]


def jie(m=ID):
    """卩（即、节 的一部分）：横折钩 + 长竖。竖头按绝对距离高出横 40（压扁的 节 里也不擦着横走）。"""
    return [HZG_(m, 300, 760, 790, 150), han.shu(m.x(300), m.y(790) + 40, m.y(-70))]


def zhi_only(m=ID, foot=30):
    """只（识、职 的右边）。压窄时口的脚 foot 留长一点。"""
    return KOU_(m, 260, 740, 830, 420, foot=foot) + [P_(m, (390, 290), (130, -50), w0=V(1.0)),
                                                    D_(m, (620, 290), (860, -10), w=V(1.2))]


def HZ_(m, x0, xc, y, y1, **kw):
    """横折：xc 是竖的中线。"""
    return hengzhe(m.x(x0), m.x(xc) + han.V / 2, m.y(y), m.y(y1), **kw)


# ───────── 第一组：新部件的字 ─────────

def c_na():                    # 那
    return lr(na_left, fu_right, (560, -70, 945, 880), 0.9)


def c_bu_part():               # 部
    return lr(bu_left, fu_right, (600, -70, 945, 880), 0.88)


def c_dou():                   # 都
    return lr(lambda m: zhe(into((70, -70, 570, 880))), fu_right, (600, -70, 945, 880), 0.88)


def c_yuan_member():           # 员
    return tb(lambda m: KOU_(m, 250, 750, 800, 590, foot=30), bei, (80, -70, 920, 530), 0.9)


def c_ze():                    # 则
    return lr(bei_left, dao_right, (600, -60, 945, 880))


def c_zheng_govern():          # 政
    return lr(zheng_left, pu, (450, -70, 945, 880), 0.9)


def c_zuo_do():                # 做
    return lr(ren_left, lambda m: gu(m.into((70, -70, 450, 880))) + pu(m.into((475, -70, 930, 880)), na_end=(620, -40)),
              (320, -70, 945, 880), 0.88)


def c_fang_put():              # 放
    return lr(fang_left, pu, (470, -70, 945, 880), 0.9)


def c_gai():                   # 改
    return lr(ji_left, pu, (470, -70, 945, 880))


def c_shou_receive():          # 收
    return lr(shou_left, pu, (420, -70, 945, 880))


def c_suo():                   # 所
    return lr(hu_left, jin_axe, (470, -70, 945, 880), 0.9)


def c_ting():                  # 听
    return lr(kou_left, jin_axe, (370, -70, 945, 880), 0.9)


def c_jin_near():              # 近
    return bao(zou, jin_axe, (330, 150, 930, 880), 0.9)


def c_xin_new():               # 新
    return lr(qin_left, jin_axe, (490, -70, 945, 880), 0.88)


def c_hen():                   # 很
    return lr(chi_left, gen, (380, -70, 945, 880), 0.9)


def c_yan_eye():               # 眼
    return lr(mu_eye, gen, (380, -70, 945, 880), 0.88)


def c_gen_root():              # 根
    return lr(mu_left, gen, (380, -70, 945, 880), 0.88)


def c_ji_at_once():            # 即
    return lr(ji_rice, jie, (520, -70, 945, 880), 0.9)


def c_tui():                   # 退
    return bao(zou, gen, (330, 200, 920, 890), 0.9)


def c_shi_know():              # 识
    return lr(yan_left, zhi_only, (360, -40, 945, 860), 0.9)


# ───────── 第二组的部件 ─────────

def niu_left(m=ID):
    """牛（特、物 的左边）：底横变成提。"""
    return [P_(m, (170, 860), (70, 570), w0=V(0.85)), H_(m, 60, 380, 620, beak=0.5),
            S_(m, 230, 880, -70), T_(m, (90, 260), (390, 430), w0=V(0.95))]


def wu_not(m=ID):
    """勿（物 的右边）"""
    p0, p1 = (420, 880), (220, 600)
    x0 = han.on_pie(m.p(p0), m.p(p1), (0, 0), m.y(650))[0]
    return [P_(m, p0, p1, w0=V(0.95)),
            hengzhegou(x0, m.x(860) + han.V / 2, m.y(650), m.y(-40)),
            P_(m, (520, 640), (180, 120), head="hid", w0=V(0.85)),
            P_(m, (720, 640), (330, -40), bend=(-20, -30), head="hid", w0=V(0.9))]


def de_right(m=ID):
    """㝵（得 的右边）：日、一、寸。"""
    return KOU_(m, 250, 750, 840, 600, foot=30) + [INNER_(m, 250, 750, 720), H_(m, 100, 900, 470),
                                                  H_(m, 56, 944, 270), SG_(m, 650, 470, -60, top="hid"),
                                                  D_(m, (300, 195), (390, 70))]


def shi_history(m=ID, yt=700, yb=400, na0=(300, 330)):
    """史：口，中间一竖从上面穿过口写成竖撇，捺从口的左下起笔。yt、yb 是口的上下横，na0 是捺的起点。"""
    return KOU_(m, 230, 760, yt, yb, foot=30) + [
        shupie(m.x(500), m.y(850), m.x(120), m.y(-60), head="cut", w0=V(0.95)),
        na(m.p(na0), m.p((800, -30)), m.v((10, -40)), wmax=V(1.15) * (0.8 + 0.2 * m.k), start="tip")]


def li_official(m=ID):
    """吏（使 的右边）：一 + 史（口扁一些）。"""
    return [H_(m, 120, 930, 720)] + shi_history(m, 540, 300, (300, 230))


def shi_is(m=ID, na_end=(780, -30), shu_end=70):
    """是（提、题 的左右边）。na_end 是捺的终点（𤴓 自己的坐标），题 里捺要伸到 页 下面；中竖的末端 shu_end 跟着藏进捺里。"""
    return KOU_(m, 250, 750, 860, 560, foot=30) + [INNER_(m, 250, 750, 710), H_(m, 56, 944, 420)] + \
        zou_di(m.into((70, -40, 930, 470)), heng_top=False, na_end=na_end, shu_end=shu_end)


def ji_lucky(m=ID):
    """吉（结 的右边）：士 + 口。"""
    return [S_(m, 500, 880, 470, end="hid"), H_(m, 80, 920, 690), H_(m, 220, 780, 470, beak=0.6)] + \
        KOU_(m, 220, 780, 300, -20, foot=30)


def qie(m=ID):
    """妾（接 的右边）：立 + 女。"""
    return [D_(m, (470, 905), (540, 810)), H_(m, 150, 850, 740),
            D_(m, (300, 725), (330, 665), w=V(0.85)), P_(m, (720, 725), (690, 670), w0=V(0.8)),
            H_(m, 56, 944, 560),
            piedian(m.p((420, 470)), m.p((250, 230)), m.p((800, -50)), w=V(0.8), wd=V(0.98)),
            P_(m, (690, 330), (110, -60), bend=(-40, -20), w0=V(0.95)), H_(m, 56, 944, 300)]


def qi_part(m=ID):
    """其"""
    return [H_(m, 80, 920, 700), S_(m, 330, 860, 250, end="hid"), S_(m, 670, 860, 250, end="hid"),
            INNER_(m, 330, 670, 545), INNER_(m, 330, 670, 395),
            H_(m, 56, 944, 250), P_(m, (360, 235), (80, -60), w0=V(0.95)), D_(m, (560, 240), (860, -40), w=V(1.15))]


def zhi_point(m=ID):
    """旨（指 的右边）：匕 + 日。"""
    return [P_(m, (850, 880), (360, 740), w0=V(0.85)), SWG_(m, 330, 880, 560, 900)] + \
        KOU_(m, 270, 730, 420, 20, foot=30) + [INNER_(m, 270, 730, 220)]


def wu_noon(m=ID):
    """午（许 的右边）"""
    p0, p1 = (420, 880), (90, 500)
    x0 = han.on_pie(m.p(p0), m.p(p1), (0, 0), m.y(650))[0]
    return [P_(m, p0, p1, w0=V(0.95)), heng(x0, m.x(900), m.y(650), entry=None), H_(m, 56, 944, 380),
            S_(m, 580, 650, -70, top="hid", end="needle")]


def dai_dull(m=ID):
    """呆（保 的右边）：口 + 木。"""
    return KOU_(m, 250, 750, 830, 560, foot=30) + [
        H_(m, 56, 944, 400), S_(m, 500, 560, -70, top="hid"),
        P_(m, (480, 390), (80, -10), bend=(-20, -10), head="hid"),
        N_(m, (520, 380), (800, 40), bend=(20, -10), wmax=V(1.1))]


def geng(m=ID):
    """更（便 的右边）：一、日，中间一竖从上横下来穿过日变成撇，捺从日的左下起笔。"""
    return [H_(m, 56, 944, 790)] + KOU_(m, 220, 780, 660, 330, foot=30) + [
        INNER_(m, 220, 780, 495),
        shupie(m.x(560), m.y(790), m.x(120), m.y(-60), head="hid", w0=V(0.95)),
        na(m.p((300, 280)), m.p((800, -30)), m.v((10, -40)), wmax=V(1.15) * (0.8 + 0.2 * m.k), start="tip")]


def zhu_master(m=ID):
    """主（住、往 的右边）"""
    return [D_(m, (450, 905), (540, 800))] + wang(m.into((70, -70, 930, 770)))


# ───────── 第二组的字 ─────────

def c_de():                    # 得
    return lr(chi_left, de_right, (380, -70, 945, 880), 0.88)


def c_shi_make():              # 使
    return lr(ren_left, li_official, (330, -70, 945, 880), 0.9)


def c_te():                    # 特
    return lr(niu_left, si_temple, (420, -70, 945, 880), 0.88)


def c_wu_thing():              # 物
    return lr(niu_left, wu_not, (420, -70, 945, 880), 0.9)


def c_ti_lift():               # 提
    return lr(shou, shi_is, (360, -70, 945, 880), 0.88)


def c_jie_tie():               # 结
    return lr(si_left, ji_lucky, (380, -70, 945, 880), 0.9)


def c_liang_amount():          # 量
    return _w(0.88, lambda: KOU_(ID, 250, 750, 850, 645, foot=30) + [INNER_(ID, 250, 750, 748), heng(56, 944, 530)]
              + li_in(into((70, -70, 930, 420))))


def c_jie_take():              # 接
    return lr(shou, qie, (360, -70, 945, 880), 0.88)


def c_qi_period():             # 期
    return lr(lambda m: qi_part(into((40, -70, 560, 880))), yue, (560, -70, 945, 880), 0.88)


def zhi_straight(m=ID, kou=(340, 740)):
    """直（值 的右边，也可整字用）。压窄时框里的目往右让（kou 是目的左右竖），别贴着左边的竖折。"""
    a, b = kou
    return [H_(m, 80, 920, 730), S_(m, 540, 880, 620, end="hid")] + KOU_(m, a, b, 620, 150) + [
        INNER_(m, a, b, 460), INNER_(m, a, b, 300), shuzhe(m.x(170), m.y(640), m.y(10), m.x(944), right="beak")]


def c_zhi_straight():          # 直
    return _w(0.9, zhi_straight)


def c_zhi_point():             # 指
    return lr(shou, zhi_point, (360, -70, 945, 880), 0.9)


def c_xu():                    # 许
    return lr(yan_left, wu_noon, (340, -70, 945, 880))


def c_bao_keep():              # 保
    return lr(ren_left, dai_dull, (330, -70, 945, 880), 0.9)


def c_bian():                  # 便
    return lr(ren_left, geng, (330, -70, 945, 880), 0.9)


def xue_cave(m=ID):
    """穴（空、究、容 的头）：宀 + 八。"""
    return mian(m) + [P_(m, (380, 680), (140, 460), w0=V(0.95)), D_(m, (600, 690), (780, 494), w=V(1.1))]


def c_kong():                  # 空
    return _w(0.9, lambda: xue_cave() + [heng(180, 780, 330), shu(500, 330, 20, top="hid", end="hid"), heng(56, 944, 20)])


def tai_platform(m=ID):
    """台（治、始 的右边，也可整字用）：厶 + 口。"""
    return [piezhe(m.p((470, 880)), m.p((220, 560)), m.p((830, 640)), w=V(0.9)),
            D_(m, (680, 800), (840, 650))] + KOU_(m, 230, 770, 380, 10, foot=30)


def c_zhi_govern():            # 治
    return lr(shui, tai_platform, (330, -70, 945, 880), 0.9)


def c_ji_base():               # 基
    return tb(qi_part, tu, (140, -60, 860, 320), 0.88, tbox=(70, 260, 930, 880))


def c_si_manage():             # 司
    return [hengzhegou(100, 880, 780, -40), heng(70, 640, 600, beak=0.6)] + _kou(230, 600, 440, 170, foot=30)


def c_zhu_live():              # 住
    return lr(ren_left, zhu_master, (330, -70, 945, 880), 0.9)


def c_wang_go():               # 往
    return lr(chi_left, zhu_master, (380, -70, 945, 880), 0.9)


# ───────── 第三组的部件 ─────────

def bing_left(m=ID):
    """冫（次、决、准 的左边）：上面一点，下面一提从左下挑向右上。"""
    return [D_(m, (100, 790), (200, 640), w=V(1.0)), T_(m, (110, 80), (320, 440), w0=V(1.0))]


def qian_owe(m=ID, hp_end=(720, 560), na_end=(800, -40)):
    """欠（次、欢 的右边）：撇、横撇、长撇、捺。压扁时（资 的头）横撇的撇太短会打结，hp_end 往下放；
    放进窄的右框时 na_end 往里收。"""
    p0, p1 = (440, 880), (170, 560)
    x0 = han.on_pie(m.p(p0), m.p(p1), (0, 0), m.y(690))[0]
    return [P_(m, p0, p1, w0=V(0.95)),
            han.hengpie(x0, m.x(880), m.y(690), m.p(hp_end), w0=V(0.8), entry=None),
            P_(m, (560, 690), (100, -60), bend=(-30, -60), head="hid", w0=V(1.0)),
            na(han.on_pie(m.p((560, 690)), m.p((100, -60)), m.v((-30, -60)), m.y(540)), m.p(na_end),
               m.v((20, -40)), wmax=V(1.18) * (0.8 + 0.2 * m.k))]


def jue(m=ID):
    """夬（决 的右边）"""
    return [HZ_(m, 280, 760, 720, 370, end="hid"), H_(m, 56, 944, 370),
            shupie(m.x(500), m.y(880), m.x(120), m.y(-60), head="cut", w0=V(0.95)),
            N_(m, (530, 360), (760, -40), bend=(20, -40))]


def zhui(m=ID):
    """隹（准、难、集）：撇、竖、点、四横、中间一竖。"""
    p0, p1 = (330, 880), (50, 420)
    return [P_(m, p0, p1, w0=V(0.95)), shu(m.x(230), m.y(720) + 40, m.y(-70)),
            D_(m, (560, 905), (620, 775), w=V(1.0)),
            H_(m, 230, 930, 720, entry=None), H_(m, 230, 800, 510, entry=None, beak=0.7),
            H_(m, 230, 800, 300, entry=None, beak=0.7), S_(m, 570, 720, 80, top="hid", end="hid"),
            H_(m, 230, 944, 80, entry=None)]


def yong_top(m=ID):
    """甬（通 的里面）：マ + 用。"""
    return [HP_(m, 200, 800, 870, (400, 660), bend=(-20, 0), w0=V(0.85)),
            D_(m, (480, 720), (550, 640), w=V(0.9)),
            shupie(m.x(180), m.y(500) + 40, m.x(50), m.y(-60), head="cut", w0=V(0.95)),
            HZG_(m, 180, 820, 500, -60), INNER_(m, 180, 820, 330), INNER_(m, 180, 820, 160),
            S_(m, 500, 500, -60, top="hid")]


def lun(m=ID):
    """仑（论 的右边）：人字头（捺收短，免得捺脚出框）+ 匕。"""
    p0, p1, bend = m.p((500, 880)), m.p((80, 520)), m.v((-20, -10))
    return [pie(p0, p1, bend, w0=V(1.04)),
            na(han.on_pie(p0, p1, bend, m.y(790)), m.p((800, 550)), m.v((40, -10)), wmax=V(1.1) * (0.8 + 0.2 * m.k)),
            P_(m, (830, 410), (400, 260), w0=V(0.85)), SWG_(m, 400, 480, -30, 880)]


def zhi_go(m=ID):
    """夂（处 的左边）：撇、横撇（撇扫得很长）、平捺托底。"""
    p0, p1 = (300, 880), (60, 430)
    x0 = han.on_pie(m.p(p0), m.p(p1), (0, 0), m.y(690))[0]
    return [P_(m, p0, p1, w0=V(0.95)),
            han.hengpie(x0, m.x(470), m.y(690), m.p((60, -60)), m.v((60, -40)), w0=V(0.95), entry=None)]


def ling_other(m=ID):
    """另（别 的左边，也可整字用）：口 + 力。"""
    return KOU_(m, 250, 760, 830, 570, foot=30) + [HZG_(m, 90, 850, 380, -50),
                                                  P_(m, (480, 400), (60, -60), bend=(-30, -30), w0=V(1.0))]


def ling_left(m=ID):
    """另（别 的左边）"""
    return ling_other(into((60, -70, 560, 880)))


def zhao_claw(m=ID):
    """爫 + 冖（受、爱 的头）"""
    return [P_(m, (860, 890), (150, 770), bend=(0, -10), w0=V(0.85)),
            D_(m, (260, 775), (320, 660), w=V(0.85)), D_(m, (500, 790), (540, 670), w=V(0.8)),
            P_(m, (800, 845), (700, 660), w0=V(0.8)),
            D_(m, (110, 620), (130, 490), w=V(1.0)), hook_down(m.x(130), m.x(900), m.y(540), entry=None)]


def chang_factory(m=ID):
    """厂（反 的外框）：平的撇作顶，左边竖撇。"""
    return [P_(m, (880, 880), (250, 780), bend=(0, -15), w0=V(0.9)),
            shupie(m.x(250), m.y(800), m.x(40), m.y(-60), head="cut", w0=V(0.95))]


def shi_left(m=ID, cloth=False):
    """礻（社、神、视 的左边）：点、横折撇、竖、点；竖从撇上起笔，不贴着横。
    cloth=True 时是 衤（被）：右边的点换成一个短撇、一个点。"""
    out = [D_(m, (200, 900), (260, 790), w=V(1.0)),
           han.hengpie(m.x(40), m.x(350), m.y(660), m.p((40, 280)), m.v((0, 0)), w0=V(0.85)),
           S_(m, 230, 540, -70)]
    if cloth:
        return out + [P_(m, (360, 540), (270, 470), w0=V(0.7)), D_(m, (262, 450), (390, 330), w=V(0.85))]
    return out + [D_(m, (270, 480), (370, 360), w=V(0.85))]


def shen(m=ID):
    """申（神 的右边）：日 + 中间一竖穿过。"""
    return KOU_(m, 200, 800, 700, 200, foot=30) + [INNER_(m, 200, 800, 450), S_(m, 500, 880, -70, end="needle")]


def dou_ladle(m=ID, h_y=300):
    """斗（科、料 的右边，也可整字用）：两点、斜横、长竖。整字的点大，斜横往下放一点（h_y）。"""
    return [D_(m, (190, 700), (300, 620), w=V(0.9)), D_(m, (190, 520), (300, 440), w=V(0.9)),
            tilted(H_(m, 56, 944, h_y), 8, m.x(56), m.y(h_y)), S_(m, 680, 880, -70, end="needle")]


def cheng_show(m=ID):
    """呈（程 的右边）：口 + 王。"""
    return KOU_(m, 230, 770, 840, 560, foot=30) + wang(m.into((70, -70, 930, 470)))


def ba_snake(m=ID):
    """巴（把、吧 的右边）：横折、中竖、横，左边一笔竖弯钩。"""
    return [hengzhe(m.x(240), m.x(760) + han.V / 2, m.y(800), m.y(440) - 34),
            S_(m, 500, 800, 440, top="hid", end="hid"), INNER_(m, 240, 760, 440), SWG_(m, 240, 860, -30, 920)]


# ───────── 第三组的字 ─────────

def c_ci_order():              # 次
    return lr(bing_left, qian_owe, (340, -70, 945, 880), gap=76)


def c_jue():                   # 决
    return lr(bing_left, jue, (340, -70, 900, 880), gap=60)


def c_zhun():                  # 准
    return lr(bing_left, zhui, (340, -70, 945, 880), 0.88, gap=76)


def c_nan():                   # 难
    return lr(you_left, zhui, (380, -70, 945, 880), 0.88)


def c_ji_gather():             # 集
    top = into((130, 380, 870, 880))
    return _w(0.88, lambda: zhui(top) + [heng(56, 944, 290), shu(500, top.y(80), -70, top="hid"),
                                        pie((500, 290), (80, -30), bend=(-20, -10), head="hid"),
                                        na((520, 285), (850, -20), (20, -10), wmax=V(1.1))])


def c_tong_through():          # 通
    return bao(zou, yong_top, (330, 200, 920, 880), 0.88)


def c_lun():                   # 论
    return lr(yan_left, lun, (340, -70, 945, 880))


def c_chu_place():             # 处
    return [*zhi_go(into((60, -70, 640, 880))), shu(650, 880, 230), dian((690, 600), (900, 400), w=V(1.1)),
            na((200, 330), (900, -20), (-150, -120), wmax=V(1.12), w0=34, foot=0.42, start="tip")]


def c_bie():                   # 别
    return lr(ling_left, dao_right, (600, -60, 945, 880), 0.9)


def c_ling():                  # 另
    return ling_other()


def c_zong():                  # 总
    return tb(lambda m: [D_(m, (260, 880), (330, 770)), P_(m, (760, 890), (650, 770), w0=V(0.9))]
              + KOU_(m, 230, 770, 690, 400, foot=30), xin_di, (70, -70, 930, 300), 0.9)


def c_wu_affair():             # 务
    return tb(lambda m: zhi_go_top(m), li, (70, -70, 930, 420), 0.92, tbox=(70, 420, 930, 880))


def zhi_go_top(m=ID, na_end=(880, 430)):
    """夂（务、格 的头）：撇、横撇、捺。压窄时 na_end 往里收。"""
    p0, p1 = (380, 880), (90, 440)
    x0 = han.on_pie(m.p(p0), m.p(p1), (0, 0), m.y(720))[0]
    return [P_(m, p0, p1, w0=V(1.0)),
            han.hengpie(x0, m.x(780), m.y(720), m.p((60, 220)), m.v((60, -40)), w0=V(0.95), entry=None),
            N_(m, (300, 700), na_end, bend=(-20, -80))]


def c_shou_receive2():         # 受
    return tb(zhao_claw, you, (90, -40, 910, 420), 0.9)


def c_fan():                   # 反
    return chang_factory() + you(into((300, -60, 930, 600)))


def c_she():                   # 社
    return lr(shi_left, tu, (380, -70, 945, 880), 0.9)


def c_shen():                  # 神
    return lr(shi_left, shen, (380, -70, 945, 880), 0.9)


def c_ke_subject():            # 科
    return lr(he_left, dou_ladle, (400, -70, 945, 880), 0.9)


def c_cheng_journey():         # 程
    return lr(he_left, cheng_show, (400, -70, 945, 880), 0.88)


def c_ba_hold():               # 把
    return lr(shou, ba_snake, (380, -70, 945, 880), 0.9)


def c_ba_ma():                 # 吧
    return lr(kou_left, ba_snake, (380, -70, 945, 880), 0.9)


# ───────── 第四组的部件 ─────────

def zhan_left(m=ID):
    """占（战 的左边）：卜 + 口。"""
    return [S_(m, 250, 880, 430, end="hid"), H_(m, 250, 450, 650, entry=None, beak=0.5)] + \
        KOU_(m, 90, 430, 430, 60, foot=30)


def ge_halberd(m=ID, xie_top=(300, 880), dot=((560, 840), (700, 710))):
    """戈（战、找 的右边）：斜横、斜钩、撇、点。放进比较宽的框时（找）斜钩起笔往右挪（xie_top），点跟着挪（dot），
    斜钩不会斜过头。"""
    return [tilted(H_(m, 56, 930, 560), 6, m.x(56), m.y(560)),
            xiegou(m.p(xie_top), m.p((790, -40)), end=302),
            P_(m, (860, 470), (420, -40), w0=V(0.9)), D_(m, *dot)]


def mi_rice(m=ID, top=((240, 890), (320, 790), (780, 890), (660, 780), 1.2), low=(400, (90, 380), (820, 420))):
    """米（类 的头，数 的左上，也可整字用）：两点、横、竖，撇和点从中间散开。
    top 是横上面那一点、一撇的起止和点的粗细；压扁时（数）点要收小、离横远一点。
    low 是竖的末端、下面一撇和一点的终点：整字的 米 竖写到底，撇点张开。"""
    d0, d1, p0, p1, dw = top
    ve, pe, de = low
    return [D_(m, d0, d1, w=V(dw)), P_(m, p0, p1, w0=V(0.85)),
            H_(m, 56, 944, 650), S_(m, 500, 880, ve, end="dew"),
            P_(m, (470, 640), pe, w0=V(0.85), head="hid"), D_(m, (540, 620), de, w=V(1.0))]


def jiao(m=ID, na_end=(840, -10)):
    """交（较、校 的右边，也可整字用）。放进窄的右框时 na_end 往里收。"""
    return [D_(m, (450, 910), (520, 825)), H_(m, 56, 944, 700),
            P_(m, (280, 680), (90, 420), w0=V(0.85)), D_(m, (620, 690), (800, 440), w=V(1.05)),
            P_(m, (650, 340), (60, -50), bend=(-30, -40), w0=V(1.0)),
            N_(m, (340, 490), na_end, bend=(20, -40), start="tip")]


def fu_man_left(m=ID):
    """夫（规 的左边）：捺写成点。"""
    return [H_(m, 60, 380, 650, beak=0.5), H_(m, 40, 410, 450, beak=0.5),
            P_(m, (230, 880), (60, -50), bend=(0, -70), w0=V(1.0)), D_(m, (270, 360), (370, 170), w=V(0.95))]


def er_ear(m=ID):
    """耳（取 的左边）：底横变成提。"""
    return [H_(m, 40, 560, 800, beak=0.5), S_(m, 160, 800, 150, top="hid", end="hid"),
            S_(m, 360, 800, -70, top="hid"), INNER_(m, 160, 360, 590), INNER_(m, 160, 360, 390),
            T_(m, (90, 150), (560, 330))]


def shi_teacher_left(m=ID):
    """师 的左边：短竖 + 竖撇。"""
    return [S_(m, 120, 700, 220), shupie(m.x(290), m.y(880), m.x(40), m.y(-60), head="cut", w0=V(0.95))]


def za(m=ID):
    """帀（师 的右边）：横 + 巾。"""
    return [H_(m, 56, 944, 790), S_(m, 200, 640, 130), HZG_(m, 200, 800, 600, 130),
            S_(m, 500, 790, -70, top="hid", end="needle")]


def qi_seven_left(m=ID):
    """七（切 的左边）：斜横 + 竖提。"""
    return [tilted(H_(m, 40, 440, 470, beak=0.4), 12, m.x(40), m.y(470)),
            shuti(m.x(220), m.y(880), m.y(90), m.p((470, 300)))]


def dao_knife(m=ID):
    """刀（切 的右边）：横折钩 + 撇。"""
    return [HZG_(m, 120, 840, 720, -50), P_(m, (520, 720), (60, -70), bend=(-20, -40), head="hid", w0=V(1.0))]


def si_snake(m=ID):
    """巳（导 的头）：横折、中横、竖弯钩。"""
    return [hengzhe(m.x(270), m.x(740) + han.V / 2, m.y(800), m.y(650) - 34), INNER_(m, 270, 740, 650),
            SWG_(m, 270, 840, 490, 880)]


def yun(m=ID):
    """云（运 的里面）"""
    return [H_(m, 220, 780, 780), H_(m, 56, 944, 560),
            piezhe(m.p((430, 550)), m.p((180, 120)), m.p((800, 240)), w=V(0.9)),
            D_(m, (620, 400), (800, 170), w=V(1.1))]


def yao_young(m=ID):
    """夭（笑 的下面）：平撇、横、撇、捺。"""
    p0, p1, bend = (480, 780), (60, -60), (10, -80)
    return [P_(m, (800, 890), (230, 790), bend=(0, -10), w0=V(0.85)), H_(m, 56, 944, 560),
            P_(m, p0, p1, bend=bend, w0=V(1.05)),
            na(han.on_pie(m.p(p0), m.p(p1), m.v(bend), m.y(480)), m.p((850, -20)), m.v((30, -10)),
               wmax=V(1.18) * (0.8 + 0.2 * m.k))]


def you_r(m=ID):
    """又（放在右边的窄写法：取）：捺收短，免得捺脚往右冲。"""
    return [HP_(m, 140, 820, 740, (100, -10), bend=(150, -70), w0=han.V),
            N_(m, (290, 734), (740, -40), bend=(-100, -85), foot=0.75)]


# ───────── 第四组的字 ─────────

def c_zhan():                  # 战
    return lr(zhan_left, ge_halberd, (450, -70, 945, 880), 0.9)


def shi_style(m=ID):
    """式（试 的右边，也可整字用）"""
    return [H_(m, 56, 944, 660), xiegou(m.p((560, 880)), m.p((850, -30)), end=300), D_(m, (690, 845), (800, 720)),
            H_(m, 100, 470, 470, beak=0.6), S_(m, 280, 470, 120, top="hid", end="hid"), T_(m, (100, 60), (580, 200))]


def c_shi_style():             # 式
    return _w(0.92, shi_style)


def c_nan_south():             # 南
    return _w(0.9, lambda: [heng(56, 944, 730), shu(505, 880, 590, end="hid"), shu(190, 630, -50),
                            hengzhegou(190, 897, 590, -50), dian((320, 505), (365, 455), w=V(0.9)),
                            pie((690, 490), (630, 430), w0=V(0.8)),
                            heng(190, 845, 340, beak=False, entry=None, right_hid=True),
                            heng(300, 720, 190, beak=0.6), shu(505, 340, -60, top="hid")])


def c_lei():                   # 类
    return tb(mi_rice, da, (60, -60, 940, 450), 0.9)


def c_jiao():                  # 交
    return _w(0.92, lambda: jiao())


def c_gui():                   # 规
    return lr(fu_man_left, jian_see, (430, -70, 945, 880), 0.9, lsx=0.75)


def c_qu_take():               # 取
    return lr(er_ear, you_r, (500, -60, 945, 760), 0.9)


def c_la():                    # 拉
    return lr(shou, li_stand, (360, -70, 945, 880), 0.9)


def c_ge_grid():               # 格
    return lr(mu_left, lambda m: zhi_go_top(m.into((70, 380, 930, 880)), na_end=(790, 430))
              + KOU_(m, 260, 740, 340, 0, foot=30),
              (370, -70, 945, 880), 0.88)


def c_jue_feel():              # 觉
    return tb(xue_top, jian_see, (80, -70, 920, 520), 0.9)


def shu_art(m=ID):
    """术（述 的里面，也可整字用）：木 + 右上一点。点离横按绝对距离留（压扁的 述 里也不贴横）。"""
    ye = m.y(620) + 126
    return mu(m) + [han.dian((m.x(690), ye + 114), (m.x(790), ye), w=V(1.05) * m.k)]


def c_shu_art():               # 术
    return shu_art()


def c_shi_teacher():           # 师
    return lr(shi_teacher_left, za, (400, -70, 945, 880))


def c_guan_view():             # 观
    return lr(you_left, jian_see, (390, -70, 945, 880), 0.92)


def c_qing_clear():            # 清
    return lr(shui, qing, (330, -70, 945, 880), 0.88)


def c_qie():                   # 切
    return lr(qi_seven_left, dao_knife, (480, -70, 945, 880))


def c_yuan_court():            # 院
    return lr(fu_left, lambda m: mian(m) + yuan(m.into((80, -70, 920, 560))),
              (400, -70, 945, 880), 0.88)


def c_dao_guide():             # 导
    return _w(0.92, lambda: si_snake() + [heng(56, 944, 300), han.shugou(650, 410, -60),
                                          dian((330, 230), (440, 90), w=V(1.1))])


def c_yun():                   # 运
    return bao(zou, yun, (330, 220, 920, 860), 0.9)


def c_xiao():                  # 笑
    return tb(zhu_top, yao_young, (70, -70, 930, 590), 0.88)


def c_qing_ask():              # 请
    return lr(yan_left, qing, (340, -70, 945, 880), 0.9)


# ───────── 第五组的部件 ─────────

def jing_capital_left(m=ID, ys=(910, 820, 700, 570, 400, 300, 60, 290, 120), gou=(-110, 80)):
    """京（就 的左边，影 的左下）：点、横、口、小（竖钩、左撇、右点）。
    ys 是各笔的高度：点的起止、横、口的上下横、左撇的起止、右点的起止。景（影）里要压扁，按笔画间距重新排，
    竖钩变短，钩也收短（gou）。"""
    d0, d1, h, kt, kb, p0, p1, q0, q1 = ys
    return [D_(m, (250, d0), (300, d1)), H_(m, 50, 540, h, beak=0.5)] + KOU_(m, 140, 440, kt, kb, foot=30) + [
        SG_(m, 290, kb, -60, dx=gou[0], dy=gou[1], top="hid"), P_(m, (170, p0), (60, p1), w0=V(0.8)),
        D_(m, (380, q0), (440, q1), w=V(0.9))]


def you_especially(m=ID):
    """尤（就 的右边）：横、穿过横的撇、竖弯钩、右上一点。"""
    return [H_(m, 230, 944, 600), P_(m, (420, 880), (200, -60), bend=(20, -60), w0=V(1.0)),
            SWG_(m, 680, 600, -30, 960, top="hid", r_in=40), D_(m, (730, 880), (810, 760), w=V(1.0))]


def xian_all(m=ID):
    """咸（感 的头）：横、竖撇、短横、口、斜钩、撇、点。"""
    return [H_(m, 170, 944, 620), shupie(m.x(180), m.y(810), m.x(40), m.y(-50), head="cut", w0=V(0.95)),
            H_(m, 330, 540, 450, beak=0.4)] + KOU_(m, 330, 540, 250, 0, foot=30) + [
            xiegou(m.p((580, 880)), m.p((840, -20)), end=305),
            P_(m, (880, 430), (640, 80), w0=V(0.85)), D_(m, (740, 890), (810, 800))]


def jiang_left(m=ID):
    """丬（将 的左边）：竖、点、提。"""
    return [S_(m, 250, 880, -70), D_(m, (90, 660), (170, 530), w=V(0.95)), T_(m, (80, 220), (300, 400), w0=V(0.95))]


def jie_meet(m=ID, na_end=(860, 400)):
    """介（界 的下面，价 的右边）：人字头 + 两竖。放进窄的右框时 na_end 往里收。"""
    p0, p1, bend = m.p((500, 880)), m.p((60, 380)), m.v((-20, -10))
    return [pie(p0, p1, bend, w0=V(1.0)),
            na(han.on_pie(p0, p1, bend, m.y(780)), m.p(na_end), m.v((40, -10)), wmax=V(1.1) * (0.8 + 0.2 * m.k)),
            shupie(m.x(370), m.y(560), m.x(90), m.y(-60), head="cut", w0=V(0.9)), S_(m, 660, 560, -60)]


def shu_weapon(m=ID):
    """殳（设 的右边）：几 + 又。"""
    return [shupie(m.x(330), m.y(900), m.x(110), m.y(560), head="cut", w0=V(0.9)),
            hengzhewangou(m.x(330), m.x(690) + han.V / 2, m.y(860), m.y(600), m.x(920), entry=None,
                          hook=40 * m.k, r_in=50 * m.k, r_out=70 * m.k)] + you_r(m.into((70, -70, 930, 500)))


def gong_bow(m=ID):
    """弓（张 的左边）：横折连一横（コ）、竖折折钩。"""
    return [hengzhe_heng(m.x(80), m.x(380) + han.V / 2, m.y(820), m.y(620), m.x(70)),
            shuzhezhegou(m.x(130), m.y(620), m.y(400), m.x(400) + han.V / 2, m.y(-50), top="hid")]


def chang_long_r(m=ID):
    """长（张 的右边）"""
    return [P_(m, (800, 800), (345, 515), bend=(-30, -20), w0=V(0.95)),
            shuti(m.x(310), m.y(860), m.y(-10), m.p((580, 170))), H_(m, 56, 944, 440),
            N_(m, (330, 420), (740, 70), bend=(-30, -40), wmax=V(1.15))]


def dao_top(m=ID):
    """⺈（色 的头）：撇 + 横撇，按整字坐标画在上面三成。"""
    p0, p1 = (430, 880), (140, 620)
    x0 = han.on_pie(m.p(p0), m.p(p1), (0, 0), m.y(790))[0]
    return [P_(m, p0, p1, w0=V(0.95)),
            han.hengpie(x0, m.x(720), m.y(790), m.p((460, 600)), w0=V(0.85), entry=None)]


# ───────── 第五组的字 ─────────

def c_zhe_wear():              # 着
    return _w(0.88, lambda: [dian((310, 890), (380, 790)), pie((700, 895), (600, 790), w0=V(0.85)),
                             heng(130, 870, 720), heng(170, 830, 600), heng(56, 944, 480),
                             pie((560, 715), (40, 120), bend=(-20, -40), head="hid")]
              + _kou(330, 730, 360, 0) + [heng(330, 730, 240, beak=False, entry=None, right_hid=True),
                                          heng(330, 730, 120, beak=False, entry=None, right_hid=True)])


def c_jiu_then():              # 就
    # 京 的横很长，按间距自动摆会把 尤 挤得太窄；宋体的 尤 从 京 的横下面伸过去，这里手摆右框
    return lr(jing_capital_left, you_especially, (470, -70, 945, 880), 0.88, gap=None)


def c_ran():                   # 然
    left = into((40, 330, 480, 880))
    return _w(0.88, lambda: [P_(left, (300, 880), (80, 420), w0=V(0.9)),
                             han.hengpie(han.on_pie(left.p((300, 880)), left.p((80, 420)), (0, 0), left.y(760))[0],
                                         left.x(560), left.y(760), left.p((60, 80)), left.v((40, -20)),
                                         w0=V(0.85), entry=None),
                             D_(left, (280, 640), (360, 520), w=V(0.8)), D_(left, (250, 470), (330, 360), w=V(0.8)),
                             heng(450, 930, 640), pie((640, 880), (300, 330), bend=(-20, -40), w0=V(0.95)),
                             na((660, 640), (860, 360), (20, -30), wmax=V(1.05)),
                             dian((790, 870), (850, 790), w=V(0.9)),
                             dian((150, 220), (90, 30), w=V(1.0)), dian((340, 220), (380, 40), w=V(1.0)),
                             dian((560, 220), (610, 40), w=V(1.0)), dian((780, 230), (880, 40), w=V(1.05))])


def c_shi_thing():             # 事
    return _w(0.9, lambda: [heng(56, 944, 770)] + _kou(240, 740, 680, 540, foot=30) + [
        hengzhe(130, 792, 410, 220 - 34), heng(56, 944, 315), heng(150, 740, 220, beak=False, right_hid=True),
        shugou(490, 880, -60)])


def c_zhong_heavy():           # 重
    return _w(0.9, lambda: [pie((800, 880), (150, 770), bend=(0, -10), w0=V(0.85)), heng(56, 944, 650)]
              + _kou(170, 810, 540, 280, foot=30)
              + [heng(170, 810, 410, beak=False, entry=None, right_hid=True), shu(490, 790, 20, end="hid"),
                 heng(140, 840, 150), heng(56, 944, 20)])


def c_zui():                   # 最
    return _w(0.88, lambda: KOU_(ID, 250, 750, 850, 640, foot=30) + [INNER_(ID, 250, 750, 745), heng(56, 944, 520)]
              + [shu(150, 520, 130, top="hid", end="hid"), shu(370, 520, -70, top="hid"),
                 heng(150, 370, 400, beak=False, entry=None, right_hid=True),
                 heng(150, 370, 270, beak=False, entry=None, right_hid=True),
                 ti((80, 110), (500, 260), w0=V(0.95))] + you_r(into((450, -60, 930, 450))))


def c_jiang():                 # 将
    return lr(jiang_left, lambda m: xi_(m.into((70, 420, 930, 890))) + [
        H_(m, 56, 944, 320), SG_(m, 680, 520, -60), D_(m, (330, 230), (440, 90), w=V(1.0))], (390, -70, 945, 880), 0.9)


def c_gan():                   # 感
    return tb(xian_all, xin_di, (70, -70, 930, 250), 0.88, tbox=(70, 280, 930, 890))


def bi_must(m=ID):
    """必（密 的中间，也可整字用）"""
    return [D_(m, (420, 895), (520, 700), w=V(1.1)), D_(m, (170, 480), (200, 230), w=V(1.0)),
            wogou(m.x(330), m.y(690), m.x(480), m.y(-40), m.x(820), m.y(0)),
            P_(m, (760, 860), (60, -50), bend=(-40, -60), w0=V(1.0)), D_(m, (790, 520), (910, 300), w=V(1.1))]


def c_bi_must():               # 必
    return bi_must()


def c_ming_life():             # 命
    p0, p1, bend = (500, 880), (50, 440), (-20, -10)
    return _w(0.9, lambda: [pie(p0, p1, bend=bend, w0=V(1.04)),
                            na(han.on_pie(p0, p1, bend, 790), (860, 520), (40, -10), wmax=V(1.1)),
                            heng(300, 700, 580, beak=0.6)] + _kou(180, 400, 350, 110, foot=30) + [
        shu(570, 420, -70), hengzhegou(570, 852, 380, 100)])


def qu_frame(m=ID):
    """匚（区、医 的框）：横、竖折（末端带喙）。"""
    return [H_(m, 150, 920, 770, entry=None), shuzhe(m.x(170), m.y(810), m.y(30), m.x(944), right="beak")]


def c_qu_area():               # 区
    return qu_frame() + [pie((760, 560), (200, 110), w0=V(0.95)), dian((280, 650), (760, 200), w=V(1.15))]


def c_fei():                   # 非
    return _w(0.9, lambda: [shu(330, 880, -60), shu(570, 880, -60), heng(70, 330, 640, beak=False, right_hid=True),
            heng(100, 330, 440, beak=False, right_hid=True), ti((90, 200), (330, 270), w0=V(0.95)),
            heng(570, 920, 660, entry=None), heng(570, 900, 450, entry=None), heng(570, 944, 220, entry=None)])


def c_que():                   # 却
    return lr(lambda m: qu(into((60, -70, 580, 880))), jie, (560, -70, 945, 880), 0.9)


def c_jie_world():             # 界
    return _w(0.9, lambda: tian_(into((170, 450, 830, 880))) + jie_meet(into((50, -70, 950, 470))))


def qie_and(m=ID, ti=False):
    """且（组 的右边；助 的左边 ti=True：底横写成提，两竖收在提的中线上）"""
    if ti:
        return [S_(m, 320, 840, 40, end="hid"), HZ_(m, 320, 730, 800, 105, end="hid"),
                INNER_(m, 320, 730, 540), INNER_(m, 320, 730, 290), T_(m, (160, 15), (950, 140), w0=V(1.15))]
    return [S_(m, 320, 840, 20, end="hid"), HZ_(m, 320, 730, 800, 20, end="hid"),
            INNER_(m, 320, 730, 540), INNER_(m, 320, 730, 280), H_(m, 56, 944, 20)]


def c_qie_and():               # 且
    return qie_and()


def c_quan():                  # 权
    return lr(mu_left, you_r, (370, -60, 945, 800))


def c_she_set():               # 设
    return lr(yan_left, shu_weapon, (340, -70, 945, 880), 0.92)


def c_zhang():                 # 张
    return lr(gong_bow, chang_long_r, (400, -70, 945, 880), 0.92)


def c_fei_fly():               # 飞
    return [hengxiegou(80, 560, 760, (870, -40), end=300),
            pie((830, 760), (570, 500), w0=V(0.9)), dian((580, 480), (800, 370), w=V(1.05))]


def se_color(m=ID):
    """色（绝 的右边，也可整字用）：⺈ + 巴。"""
    return dao_top(m) + ba_snake(m.into((120, -70, 900, 540)))


def c_se():                    # 色
    return _w(0.92, se_color)


GLYPHS = {
    "那": c_na, "部": c_bu_part, "都": c_dou, "员": c_yuan_member, "则": c_ze, "政": c_zheng_govern,
    "做": c_zuo_do, "放": c_fang_put, "改": c_gai, "收": c_shou_receive, "所": c_suo, "听": c_ting,
    "近": c_jin_near, "新": c_xin_new, "很": c_hen, "眼": c_yan_eye, "根": c_gen_root, "即": c_ji_at_once,
    "退": c_tui, "识": c_shi_know,
    "得": c_de, "使": c_shi_make, "特": c_te, "物": c_wu_thing, "提": c_ti_lift, "结": c_jie_tie, "量": c_liang_amount,
    "接": c_jie_take, "期": c_qi_period, "直": c_zhi_straight, "指": c_zhi_point, "许": c_xu, "保": c_bao_keep,
    "便": c_bian, "空": c_kong, "治": c_zhi_govern, "基": c_ji_base, "司": c_si_manage, "住": c_zhu_live,
    "往": c_wang_go,
    "次": c_ci_order, "决": c_jue, "准": c_zhun, "难": c_nan, "集": c_ji_gather, "通": c_tong_through, "论": c_lun,
    "处": c_chu_place, "别": c_bie, "另": c_ling, "总": c_zong, "务": c_wu_affair, "受": c_shou_receive2, "反": c_fan,
    "社": c_she, "神": c_shen, "科": c_ke_subject, "程": c_cheng_journey, "把": c_ba_hold, "吧": c_ba_ma,
    "战": c_zhan, "式": c_shi_style, "南": c_nan_south, "类": c_lei, "交": c_jiao, "规": c_gui, "取": c_qu_take,
    "拉": c_la, "格": c_ge_grid, "觉": c_jue_feel, "术": c_shu_art, "师": c_shi_teacher, "观": c_guan_view,
    "清": c_qing_clear, "切": c_qie, "院": c_yuan_court, "导": c_dao_guide, "运": c_yun, "笑": c_xiao, "请": c_qing_ask,
    "着": c_zhe_wear, "就": c_jiu_then, "然": c_ran, "事": c_shi_thing, "重": c_zhong_heavy, "最": c_zui, "将": c_jiang,
    "感": c_gan, "必": c_bi_must, "命": c_ming_life, "区": c_qu_area, "非": c_fei, "却": c_que, "界": c_jie_world,
    "且": c_qie_and, "权": c_quan, "设": c_she_set, "张": c_zhang, "飞": c_fei_fly, "色": c_se,
}
