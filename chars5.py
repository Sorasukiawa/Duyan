"""渡言的常用字（第五批）：按使用频率挑的高频字，规矩照 docs/RULES.md：
笔画多的字整体减细（6 条轮廓 0.92，7～9 条 0.9，10 条以上 0.88，左右、上下拼的字最少 0.92），
钩用默认长度，口字框的脚 30～44；部件压进窄框时用收短捺的参数，不改捺的画法。"""
import han
from outline import Shape, n
from chars import _w, bao, c_nv_m, lr, mi_cover, shao, tb, you_friend, zhu_top, zi_self
from chars2 import chi_left, dan, dao_right, huo_dots, jian_see, jing_r, kai, xi_, yong, zai_frame, zha, zheng
from chars3 import (pie_at_x, cai, chang_top, che, cheng, gao_tell, ge_each, guan, guang_, jiu, liang, niu, qing,
                    shou_head, si_temple, xin_di, ye_work, yi_by, yi_just, zou_walk)
from chars4 import (bei, bing_left, chang_factory, dao_knife, er_ear, ge_halberd, geng, gong_bow, jiang_left, jie_meet,
                    jing_capital_left, jin_axe, jue, mi_rice, pu, qian_owe, shi_is,
                    qie_and, qu_frame, shi_history, shi_left, shou_left, shu_weapon, si_snake, tai_platform, wu_not, xue_cave,
                    zhao_claw, zhi_go_top)
from han import (dian, heng, hengpie, hengpie_wangou, hengxiegou, tilted, xiegou, hengzhe, hengzhegou, hengzhezhepie, hengzhewangou, hook_down, na, pie,
                 piezhe, shu, shugou, shupie, shuti, shuzhe, shuzhezhegou, ti, _kou)
from parts import (FULL, ID, D_, H_, HP_, HZ_, HZG_, INNER_, KOU_, N_, P_, S_, SG_, SWG_, T_, bi, cao, da, er, fu_left, he_left, hua,
                   into, kou_left, li, mu, mu_left, nv_left, ren_left, ri, shou, shui, si_left, tian_, tu_left, wang,
                   mian, shi_, wang_lost, xin, xin_left, yan_left, you, yue, yue_left, zi_, zou)

V = lambda k=1.0: han.V * k      # noqa: E731


# ───────── 第一组的部件 ─────────

def xiong(m=ID):
    """兄（况 的右边）：口 + 儿。"""
    return KOU_(m, 230, 770, 830, 420, foot=30) + [
        shupie(m.x(400), m.y(420), m.x(80), m.y(-60), w0=V(0.95), head="hid"),
        SWG_(m, 610, 420, -30, 930, top="hid")]


def shi_show(m=ID):
    """示（际 的右边，也可整字用）：二 + 小（竖钩、左撇、右点）。"""
    return [H_(m, 200, 800, 800), H_(m, 56, 944, 570), SG_(m, 500, 570, -60, top="hid"),
            P_(m, (280, 410), (90, 120), w0=V(0.9)), D_(m, (680, 410), (870, 150), w=V(1.1))]


# ───────── 第一组的字 ─────────

def c_mei_not():               # 没
    return lr(shui, shu_weapon, (330, -70, 945, 880), 0.9)


def c_yin():                   # 因
    return _w(0.92, lambda: _kou(110, 890, 820, -40) + da(into((240, 70, 750, 740))))


def c_jun():                   # 军
    return tb(mi_cover, che, (100, -70, 900, 600))


def c_zao_make():              # 造
    return bao(zou, gao_tell, (360, 130, 920, 900), 0.88)


def c_lian_join():             # 联
    return lr(er_ear, lambda m: guan(m, na_end=(700, -10)), (500, -70, 945, 880), 0.88, lsx=0.95)


def c_chi_hold():              # 持
    return lr(shou, si_temple, (360, -70, 945, 880), 0.9)


def c_zu():                    # 组
    return lr(si_left, qie_and, (380, -60, 930, 860), 0.9)


def c_kuai():                  # 快
    return lr(xin_left, jue, (340, -70, 900, 880), 0.9)


def c_ban():                   # 办
    return li() + [dian((230, 450), (110, 270), w=V(1.1)), dian((520, 450), (650, 300), w=V(1.1))]


def c_yi_discuss():            # 议
    return lr(yan_left, lambda m: yi_just(m, na_end=(800, 0)), (340, -70, 945, 880))


def c_zheng_proof():           # 证
    return lr(yan_left, zheng, (340, -40, 945, 840), 0.9)


def c_zen():                   # 怎
    return tb(zha, xin, (56, -70, 944, 330), 0.9, tbox=(120, 360, 880, 900))


def c_jiao_call():             # 叫
    return lr(kou_left, lambda m: shou_left(m.into(FULL, (40, -70, 340, 880))), (380, -70, 945, 880))


def c_tai():                   # 台
    return tai_platform()


def c_lian_link():             # 连
    return bao(zou, che, (340, 180, 920, 880), 0.9)


def c_jia_price():             # 价
    return lr(ren_left, lambda m: jie_meet(m, na_end=(790, 410)), (330, -70, 945, 880))


def c_kuang():                 # 况
    return lr(bing_left, xiong, (340, -70, 945, 880), 0.9, gap=76)


def c_ji_border():             # 际
    return lr(fu_left, shi_show, (400, -70, 945, 880), 0.9)


def c_yue_about():             # 约
    return lr(si_left, shao, (380, -60, 945, 880))


def c_shi_show():              # 示
    return shi_show()


def c_xi_breath():             # 息
    return tb(zi_self, xin_di, (70, -70, 930, 260), 0.88, tbox=(210, 300, 790, 900))


def c_si_like():               # 似
    return lr(ren_left, yi_by, (330, -70, 945, 880))


def c_shi_look():              # 视
    return lr(shi_left, jian_see, (380, -70, 945, 880), 0.9, lsx=0.82)


def c_cheng_call():            # 称
    return lr(he_left, er, (380, -60, 945, 880), 0.88, lsx=0.9)



# ───────── 第二组的部件 ─────────

def gong_left(m=ID):
    """工（功 的左边）：底横变成提。"""
    return [H_(m, 60, 320, 720, beak=0.5), S_(m, 190, 720, 190, top="hid", end="hid"),
            T_(m, (80, 140), (350, 270), w0=V(0.9))]


def he_top(m=ID):
    """禾（委 的头）：竖不往下穿，捺写成点。"""
    return [P_(m, (680, 885), (300, 800), bend=(0, -10), w0=V(0.85)), H_(m, 80, 920, 710),
            S_(m, 500, 820, 420), P_(m, (480, 700), (90, 440), w0=V(0.95), head="hid"),
            D_(m, (540, 680), (870, 480), w=V(1.05))]


def mu_top(m=ID):
    """木（查 的头）：撇、捺往两边张开，竖不往下穿。"""
    return [H_(m, 56, 944, 720), S_(m, 500, 880, 440),
            P_(m, (480, 710), (80, 450), bend=(-10, -10), w0=V(0.95), head="hid"),
            N_(m, (520, 700), (840, 450), bend=(20, -10), wmax=V(1.1))]


def che_left(m=ID):
    """车（轻、转 的左边）：底横变成提。"""
    return [H_(m, 60, 330, 730, beak=0.5),
            piezhe(m.p((230, 880)), m.p((90, 480)), m.p((340, 480)), w=V(0.8), end="flat"),
            S_(m, 220, 650, -70), T_(m, (95, 170), (350, 300), w0=V(0.9))]


def zhi_arrive(m=ID):
    """至"""
    return [H_(m, 90, 910, 800), piezhe(m.p((450, 800)), m.p((260, 545)), m.p((780, 610)), w=V(0.9), head="hid"),
            D_(m, (640, 730), (820, 560), w=V(1.1)), H_(m, 190, 810, 300), S_(m, 500, 470, 30, end="hid"),
            H_(m, 56, 944, 30)]


def shi_stone(m=ID):
    """石"""
    return [H_(m, 56, 944, 770), P_(m, (420, 770), (60, -60), bend=(20, -70), head="hid", w0=V(1.05))] + \
        KOU_(m, 400, 800, 440, 30)


def shi_stone_left(m=ID):
    """石（研、确 的左边）"""
    return [H_(m, 40, 440, 780, beak=0.5), P_(m, (220, 780), (40, -20), bend=(20, -60), head="hid", w0=V(0.95))] + \
        KOU_(m, 230, 420, 450, 90, foot=30)


def huo_fire(m=ID):
    """火"""
    p0, p1, bend = (520, 880), (70, -60), (10, -90)
    return [D_(m, (150, 650), (240, 470), w=V(1.0)), P_(m, (820, 690), (660, 460), w0=V(0.9)),
            P_(m, p0, p1, bend=bend, w0=V(1.1)),
            na(han.on_pie(m.p(p0), m.p(p1), m.v(bend), m.y(420)), m.p((840, -40)), m.v((30, -10)),
               wmax=V(1.18) * (0.8 + 0.2 * m.k))]


def zhi_branch(m=ID):
    """支（技 的右边，也可整字用）：十 + 又。"""
    return [H_(m, 56, 944, 690), S_(m, 500, 880, 440, end="hid")] + you(m.into((150, -60, 870, 520)))


def qi_beg(m=ID):
    """乞（吃 的右边）：撇、短横、横折弯钩（乙）。"""
    p0, p1 = (420, 880), (140, 560)
    x0 = han.on_pie(m.p(p0), m.p(p1), (0, 0), m.y(720))[0]
    r_in = 90 * m.k
    # 乙 的折往左下斜得多：外沿的转弯放大到和竖的两条边平行（r_out = r_in + 34 + 0.8 横粗），不然左边沿接竖时会拐一下
    return [P_(m, p0, p1, w0=V(0.95)), heng(x0, m.x(860), m.y(720), entry=None, beak=0.6),
            hengzhewangou(m.x(200), m.x(700) + han.V / 2, m.y(500), m.y(-40), m.x(940), lean=280 * m.ax,
                          hook=74 * m.k, r_in=r_in, r_out=r_in + 34 + 0.8 * han.H)]


def ma(m=ID):
    """马（吗 的右边，也可整字用）：横折、竖折折钩、底横。"""
    # 横的起笔比竖的左边沿多出一点点，竖头藏在横里（压窄时也一样）
    return [hengzhe(m.x(240) - han.V / 2 - 16, m.x(660) + han.V / 2, m.y(790), m.y(470), end="hid"),
            shuzhezhegou(m.x(240), m.y(790), m.y(470), m.x(830) + han.V / 2, m.y(-40), top="hid"),
            H_(m, 56, 830, 190, beak=False, right_hid=True)]


# ───────── 第二组的字 ─────────

def c_gong_merit():            # 功
    return lr(gong_left, li, (370, -60, 945, 880))


def c_wei_entrust():           # 委
    return tb(he_top, c_nv_m, (110, -50, 890, 420), 0.9)


def c_cha():                   # 查
    return tb(mu_top, dan, (110, -70, 890, 470), 0.9)


def c_qing_light():            # 轻
    return lr(che_left, jing_r, (380, -70, 945, 880), 0.9)


def c_yi_easy():               # 易
    return tb(ri, wu_not, (80, -70, 920, 560), 0.9, tbox=(200, 520, 800, 880))


def c_zhao_find():             # 找
    return lr(shou, lambda m: ge_halberd(m, xie_top=(380, 880), dot=((610, 860), (720, 750))),
              (360, -70, 945, 880), 0.9)


def c_guang_wide():            # 广
    return guang_()


def c_xian_show():             # 显
    return tb(ri, ye_work, (60, -70, 940, 480), 0.9, tbox=(170, 520, 830, 880))


def c_yin_pull():              # 引
    return lr(gong_bow, lambda m: [S_(m, 500, 880, -70)], (480, -70, 945, 880))


def c_li_history():            # 历
    return chang_factory() + li(into((330, -60, 930, 640)))


def c_shou_head():             # 首
    return _w(0.9, shou_head)


def c_geng():                  # 更
    return _w(0.9, geng)


def c_zhi_arrive():            # 至
    return _w(0.92, zhi_arrive)


def c_tuan():                  # 团
    return _w(0.92, lambda: _kou(110, 890, 820, -40) + cai(into((230, 40, 790, 720))))


def c_shi_stone():             # 石
    return shi_stone()


def c_huo_fire():              # 火
    return huo_fire()


def c_zhi_branch():            # 支
    return zhi_branch()


def c_shi_begin():             # 始
    return lr(nv_left, tai_platform, (370, -70, 945, 880), 0.9)


def c_bei_prepare():           # 备
    return tb(zhi_go_top, tian_, (170, -60, 830, 420), 0.9, tbox=(70, 420, 930, 880))


def c_yan_grind():             # 研
    return lr(shi_stone_left, kai, (400, -70, 945, 880), 0.9)


def c_chi_eat():               # 吃
    return lr(kou_left, qi_beg, (380, -70, 945, 880))


def c_ma_horse():              # 马
    return ma()


def c_ma_q():                  # 吗
    return lr(kou_left, ma, (380, -70, 945, 880))


def c_cun_exist():             # 存
    return zai_frame() + zi_(into((400, -60, 930, 520)))


def c_bu_cloth():              # 布
    p0, p1, bend = (450, 880), (60, -40), (10, -70)
    return [H_(ID, 56, 944, 680), P_(ID, p0, p1, bend=bend, w0=V(1.05)), S_(ID, 400, 510, 40),
            han.hengzhegou(400, 830 + han.V / 2, 470, 60), S_(ID, 615, 580, -70, end="needle")]



# ───────── 第三组的部件 ─────────

def neng_left(m=ID):
    """能 的左边：厶 + 月。"""
    return [piezhe(m.p((240, 880)), m.p((140, 690)), m.p((390, 730)), w=V(0.8)),
            D_(m, (300, 820), (400, 700), w=V(0.9))] + yue_left(m.into((40, -70, 340, 600), (40, -70, 340, 880)))


def neng_r(m=ID):
    """能 的右边：上下两个 匕。"""
    return bi(m.into((70, 470, 930, 880))) + bi(m.into((70, -70, 930, 410)))


def di_lower(m=ID):
    """第 的下半：弓（张 左边那个弓放宽）、从顶上穿下来的一竖、左下一撇。"""
    return gong_bow(m.into(FULL, (70, -70, 460, 880))) + [
        S_(m, 500, 820, -70, top="hid", end="needle"),
        P_(m, (470, 400), (90, -50), bend=(-20, -30), w0=V(0.95), head="hid")]


def pi_skin(m=ID, na_end=(840, -40)):
    """皮（被 的右边）：横钩、竖撇、中间一竖、又（横撇从竖撇上起笔）。放进窄的右框时 na_end 往里收。"""
    return [shupie(m.x(200), m.y(820), m.x(60), m.y(-60), head="cut", w0=V(0.95)),
            hook_down(m.x(200), m.x(860), m.y(780), entry=None),
            S_(m, 530, 880, 480, end="hid"),
            HP_(m, 200, 800, 470, (300, -40), bend=(150, -70), w0=V(0.95), entry=None),
            N_(m, (360, 464), na_end, bend=(-100, -85), foot=0.75)]


def zhi_make_left(m=ID):
    """制 的左边：短撇、两横、巾（左竖、横折钩、中间长竖）。"""
    p0, p1 = (230, 880), (60, 680)
    x0 = han.on_pie(m.p(p0), m.p(p1), (0, 0), m.y(770))[0]
    return [P_(m, p0, p1, w0=V(0.95)), heng(x0, m.x(480), m.y(770), entry=None, beak=0.5),
            H_(m, 40, 540, 610, beak=0.5), S_(m, 130, 480, 100), HZG_(m, 130, 510, 440, 130, dx=-70, dy=56),
            S_(m, 320, 880, -70)]


def mei_every(m=ID):
    """每（海 的右边，也可整字用）：𠂉 + 母（竖折、横折钩、长横、两点）。"""
    p0, p1 = (390, 880), (120, 650)
    x0 = han.on_pie(m.p(p0), m.p(p1), (0, 0), m.y(740))[0]
    xl = m.x(250)
    # 横折钩的起笔比竖折的左边沿多出一点点，竖折的头藏在横里
    return [P_(m, p0, p1, w0=V(0.95)), heng(x0, m.x(880), m.y(740), entry=None, beak=0.6),
            shuzhe(xl, m.y(580), m.y(110), m.x(760), top="hid", right="hid"),
            hengzhegou(xl - han.V / 2 - 16, m.x(760) + han.V / 2, m.y(580), m.y(-50), -120 * m.k, 86 * m.k),
            H_(m, 56, 944, 345), D_(m, (480, 510), (540, 455), w=V(0.85)), D_(m, (480, 275), (540, 222), w=V(0.85))]


def xiao_left(m=ID):
    """孝（教 的左边）：土、长撇、子（子 的横撇从撇上起笔，末笔写成提）。"""
    P0, P1, B = m.p((450, 605)), m.p((90, 330)), m.v((-10, -20))
    x0 = han.on_pie(P0, P1, B, m.y(450))[0]
    return [S_(m, 250, 880, 600, end="hid"), H_(m, 90, 420, 750, beak=0.5), H_(m, 40, 520, 600, beak=0.5),
            pie(P0, P1, B, w0=V(0.85) * (0.8 + 0.2 * m.k), head="hid"),
            hengpie_wangou(x0, m.x(450), m.y(450), m.p((280, 330)), m.x(290), m.y(-50), w0=V(0.8),
                           dx=-80 * m.k, dy=64 * m.k, entry=None),
            T_(m, (85, 150), (510, 260), w0=V(0.9))]


def ji_reach(m=ID, na_end=(850, -40)):
    """及（级、极 的右边，也可整字用）：撇、横折折撇、从撇身起笔的捺。"""
    P0, P1, B = m.p((390, 870)), m.p((60, -50)), m.v((30, -80))
    x0 = han.on_pie(P0, P1, B, m.y(780))[0]
    k = 0.8 + 0.2 * m.k
    return [pie(P0, P1, B, w0=V(1.0) * k),
            hengzhezhepie(x0, m.x(760), m.y(780), m.p((560, 520)), m.x(830), m.p((230, -60)),
                          w0=V(0.8) * k, w2=V(0.95) * k, entry=None),
            na(han.on_pie(P0, P1, B, m.y(470)), m.p(na_end), m.v((-10, -40)), wmax=V(1.15) * k)]


def xi_system(m=ID):
    """系：平撇、幺（两个撇折、一点）、小。"""
    # 平撇写粗一点，幺 的第一个撇折起笔整个藏在里面
    return [P_(m, (780, 890), (250, 790), bend=(0, -10), w0=V(0.95)),
            piezhe(m.p((600, 835)), m.p((330, 640)), m.p((600, 690)), w=V(0.7), head="hid"),
            piezhe(m.p((610, 685)), m.p((230, 380)), m.p((780, 440)), w=V(0.85)),
            D_(m, (680, 580), (790, 440), w=V(1.0)),
            SG_(m, 500, 410, -60, top="hid"), P_(m, (330, 280), (110, 60), w0=V(0.9)),
            D_(m, (680, 290), (860, 80), w=V(1.1))]


def fu_serve_r(m=ID):
    """𠬝（报、服 的右边）：长竖、横折钩、又（横撇从竖上起笔）。"""
    return [S_(m, 200, 860, -70), HZG_(m, 200, 780, 790, 480, dx=-70, dy=56),
            HP_(m, 200, 800, 380, (290, -40), bend=(140, -60), w0=V(0.95), entry=None),
            N_(m, (360, 374), (800, -40), bend=(-90, -80), foot=0.75)]


def chang_r(m=ID):
    """场 的右边：横撇落进横折钩的起笔（横折折折钩），横下两撇。"""
    return [HP_(m, 150, 700, 790, (330, 600), bend=(-10, 0), w0=V(0.85)),
            hengzhegou(m.x(300), m.x(830) + han.V / 2, m.y(600), m.y(-50), -120 * m.k, 86 * m.k),
            P_(m, (560, 590), (250, 150), w0=V(0.85), head="hid"),
            P_(m, (770, 590), (400, -30), bend=(-20, -20), w0=V(0.95), head="hid")]


def ci_top(m=ID):
    """次（资 的头）：冫 + 欠，压扁。"""
    return bing_left(m.into((70, 400, 930, 890))) + qian_owe(m.into((330, 400, 930, 890)), hp_end=(690, 450))


def chong(m=ID):
    """充（统 的右边）：亠、厶、儿。"""
    return [D_(m, (470, 915), (530, 835)), H_(m, 56, 944, 720),
            piezhe(m.p((470, 720)), m.p((260, 470)), m.p((760, 520)), w=V(0.85), head="hid"),
            D_(m, (640, 640), (790, 500), w=V(1.0)),
            shupie(m.x(380), m.y(380), m.x(80), m.y(-60), head="cut", w0=V(0.9)), SWG_(m, 620, 380, -30, 930)]


def shan_hair(m=ID):
    """彡（形 的右边，须 的左边）：三撇。"""
    return [P_(m, (820, 870), (250, 620), w0=V(1.0)), P_(m, (850, 590), (200, 290), w0=V(1.05)),
            P_(m, (880, 300), (110, -50), bend=(-20, -20), w0=V(1.1))]


def zu_left(m=ID):
    """𧾷（路 的左边）：口、竖、右短横、左短竖、提。"""
    return KOU_(m, 110, 380, 820, 560, foot=30) + [
        S_(m, 245, 560, 152, top="hid", end="hid"), H_(m, 245, 420, 380, entry=None, beak=0.5),
        S_(m, 110, 370, 100, end="hid"), T_(m, (85, 75), (440, 230), w0=V(0.9))]


# ───────── 第三组的字 ─────────

def c_neng():                  # 能
    return lr(neng_left, neng_r, (420, -70, 945, 880), 0.9)


def er_and(m=ID):
    """而（需 的下面，也可整字用）"""
    return [H_(m, 56, 944, 790), P_(m, (520, 790), (450, 610), w0=V(0.85), head="hid"),
            shu(m.x(170), m.y(590) + 40, m.y(-60)), HZG_(m, 170, 830, 590, -50),
            S_(m, 390, 590, 20, top="hid"), S_(m, 610, 590, 20, top="hid")]


def c_er_and():                # 而
    return _w(0.92, er_and)


def c_mian_face():             # 面
    return _w(0.9, lambda: [heng(56, 944, 800), pie((540, 800), (470, 652), w0=V(0.8), head="hid")]
              + _kou(150, 850, 640, -40)
              + [shu(390, 640, -40, top="hid", end="hid"), shu(610, 640, -40, top="hid", end="hid"),
                 heng(390, 610, 410, beak=False, entry=None, right_hid=True),
                 heng(390, 610, 190, beak=False, entry=None, right_hid=True)])


def c_kan():                   # 看
    return _w(0.88, lambda: [pie((790, 895), (260, 805), bend=(0, -10), w0=V(0.85)), heng(200, 780, 722),
                             heng(140, 860, 620), heng(56, 944, 480),
                             pie((470, 735), (60, -60), bend=(-40, -40), w0=V(1.0), head="hid")]
              + _kou(410, 840, 370, -50, foot=34)
              + [heng(410, 840, 230, beak=False, entry=None, right_hid=True),
                 heng(410, 840, 90, beak=False, entry=None, right_hid=True)])


def c_qian_front():            # 前
    return _w(0.9, lambda: [dian((300, 905), (370, 795), w=V(1.0)), pie((730, 900), (620, 770), w0=V(0.9)),
                            heng(56, 944, 680)] + yue(into((90, -70, 560, 580)))
              + [shu(690, 520, 140), shugou(860, 580, -60)])


def c_di_order():              # 第
    return tb(zhu_top, di_lower, (90, -70, 910, 560), 0.88)


def c_bei_by():                # 被
    return lr(lambda m: shi_left(m, cloth=True), lambda m: pi_skin(m, na_end=(760, -40)), (400, -70, 945, 880), 0.88)


def c_zhi_make():              # 制
    return lr(zhi_make_left, dao_right, (600, -60, 945, 880), 0.9)


def c_shen_body():             # 身
    return _w(0.9, lambda: [pie((560, 900), (450, 765), w0=V(0.85)), shu(250, 800, 320, end="hid"),
                            hengzhegou(250, 760 + V() / 2, 760, -50),
                            heng(250, 760, 610, beak=False, entry=None, right_hid=True),
                            heng(250, 760, 470, beak=False, entry=None, right_hid=True),
                            ti((80, 290), (760, 380), w0=V(1.0)),
                            pie((880, 640), (180, -50), bend=(-40, -60), w0=V(1.0))])


def c_hai():                   # 海
    return lr(shui, mei_every, (330, -70, 945, 880), 0.88)


def c_mei_every():             # 每
    return _w(0.9, mei_every)


def c_jiao_teach():            # 教
    return lr(xiao_left, pu, (540, -70, 945, 880), 0.88)


def c_sheng_sound():           # 声
    # 士 的竖一直穿到下面框的底横（框被它分成左右两格）
    return _w(0.92, lambda: [heng(56, 944, 790), shu(500, 890, 330, end="hid"), heng(170, 830, 640, beak=0.7),
                             hengzhe(250, 800 + V() / 2, 500, 290, entry=None),
                             heng(250, 800, 330, beak=False, entry=None, right_hid=True),
                             shupie(250, 540, 50, -60, head="cut")])


def c_ji_reach():              # 及
    return ji_reach()


def c_xi_system():             # 系
    return _w(0.9, xi_system)


def c_bian_change():           # 变
    return _w(0.9, lambda: [dian((470, 920), (530, 850), w=V(1.0)), heng(56, 944, 730),
                            shu(390, 730, 480, top="hid"), shu(610, 730, 480, top="hid"),
                            dian((160, 650), (240, 520), w=V(0.95)), pie((810, 640), (700, 500), w0=V(0.9))]
              + you(into((130, -60, 870, 450))))


def c_bao_report():            # 报
    return lr(shou, fu_serve_r, (360, -70, 945, 880), 0.9)


def c_fu_serve():              # 服
    return lr(yue_left, fu_serve_r, (380, -70, 945, 880), 0.9)


def c_chang_field():           # 场
    return lr(tu_left, chang_r, (360, -70, 945, 880), 0.9)


def c_zi_capital():            # 资
    return tb(ci_top, bei, (120, -70, 880, 450), 0.88)


def c_tong_unite():            # 统
    return lr(si_left, chong, (380, -70, 945, 880), 0.9)


def c_xing_shape():            # 形
    return lr(lambda m: kai(into((40, -70, 560, 880))), shan_hair, (600, -70, 945, 880), 0.9)


def c_lu_road():               # 路
    return lr(zu_left, lambda m: ge_each(m, na_end=(790, 400)), (420, -70, 945, 880), 0.88)


def c_qiu():                   # 求
    return _w(0.9, lambda: [heng(56, 944, 720), shugou(500, 880, -60), dian((690, 870), (790, 770), w=V(1.0)),
                            dian((200, 620), (290, 520), w=V(0.95)), ti((110, 230), (470, 420), w0=V(1.0)),
                            pie((820, 620), (530, 470), w0=V(0.9)),
                            na((520, 480), (880, 60), bend=(-20, -40), wmax=V(1.15))])


def c_ji_level():              # 级
    return lr(si_left, lambda m: ji_reach(m, na_end=(760, -40)), (380, -70, 945, 880))


def c_ji_pole():               # 极
    return lr(mu_left, lambda m: ji_reach(m, na_end=(760, -40)), (380, -70, 945, 880), 0.9)



# ───────── 第四组的部件 ─────────

def shi_corpse(m=ID):
    """尸（居、局、尼 的外面）：横折、底横、竖撇。底横两端藏进竖撇和横折的竖里。"""
    return [hengzhe(m.x(220), m.x(820) + han.V / 2, m.y(800), m.y(620) - 40, entry=None),
            heng(m.x(220), m.x(820), m.y(620), beak=False, entry=None, right_hid=True),
            shupie(m.x(220), m.y(840), m.x(50), m.y(-60), head="cut", w0=V(0.95))]


def ju_reside(m=ID):
    """居（据 的右边）：尸 + 古。古 的竖从尸的底横下来，藏进口的顶横。"""
    return shi_corpse(m) + [H_(m, 330, 944, 450), S_(m, 620, 620, 250, top="hid", end="hid")] + \
        KOU_(m, 400, 840, 250, -40, foot=30)


def hai_pig(m=ID):
    """亥（该 的右边）：亠、撇折、两个长撇、长点。"""
    return [D_(m, (470, 920), (530, 845)), H_(m, 56, 944, 720),
            piezhe(m.p((450, 720)), m.p((250, 500)), m.p((680, 540)), w=V(0.85), head="hid"),
            P_(m, (800, 640), (150, 200), bend=(-20, -30), w0=V(0.95)),
            P_(m, (880, 450), (120, -60), bend=(-30, -40), w0=V(1.0)),
            D_(m, (560, 250), (820, -40), w=V(1.15))]


def ling_order(m=ID, na_end=(862, 470)):
    """令（领 的左边，也可整字用）：人字头、点、横撇、竖点。放进左边时捺收短（na_end）。"""
    P0, P1, B = m.p((500, 880)), m.p((80, 470)), m.v((-20, -10))
    return [pie(P0, P1, B, w0=V(1.04) * (0.8 + 0.2 * m.k)),
            na(han.on_pie(P0, P1, B, m.y(780)), m.p(na_end), m.v((40, -10)), wmax=V(1.1) * (0.8 + 0.2 * m.k)),
            D_(m, (440, 610), (490, 530), w=V(0.95)),
            HP_(m, 260, 740, 380, (650, 240), bend=(-10, -10), w0=V(0.9)),
            S_(m, 450, 380, -50, top="hid")]


def ye_page(m=ID):
    """页（领、须、题 的右边）：横、短撇、冂（左竖短、右竖长，同 贝）、出框的撇、长点。"""
    # 左竖的头按绝对距离高出横 40（压扁的 题 里也不擦着横走）
    return [H_(m, 90, 910, 800), P_(m, (520, 795), (430, 655), w0=V(0.8), head="hid"),
            han.shu(m.x(200), m.y(640) + 40, m.y(400)), HZ_(m, 200, 800, 640, 280),
            P_(m, (540, 625), (80, -60), bend=(-20, -40), w0=V(0.95)), D_(m, (580, 200), (860, -40), w=V(1.15))]


def zhuan(m=ID):
    """专（传、转 的右边）：两横、斜下来的一撇落进横撇的起笔（竖折撇）、点。"""
    return [H_(m, 180, 820, 760), H_(m, 56, 944, 570),
            P_(m, (480, 880), (330, 425), bend=(10, -20), w0=V(0.9)),
            hengpie(m.x(300), m.x(730), m.y(420), m.p((440, -50)), m.v((-20, -20)), w0=V(0.95)),
            D_(m, (540, 260), (740, 80), w=V(1.05))]


def wang_net(m=ID):
    """罒（罗 的头）：左竖、横折、两个中竖、底横。"""
    return KOU_(m, 170, 830, 840, 650, foot=36) + [S_(m, 390, 840, 650, top="hid", end="hid"),
                                                  S_(m, 610, 840, 650, top="hid", end="hid")]


def liu_r(m=ID):
    """㐬（流 的右边）：亠、厶、丿 丨 乚。"""
    return [D_(m, (470, 915), (530, 835)), H_(m, 56, 944, 720),
            piezhe(m.p((470, 720)), m.p((260, 470)), m.p((760, 520)), w=V(0.85), head="hid"),
            D_(m, (640, 640), (790, 500), w=V(1.0)),
            shupie(m.x(290), m.y(365), m.x(80), m.y(-60), head="cut", w0=V(0.9)), S_(m, 500, 365, 40),
            SWG_(m, 690, 365, -30, 940, r_in=50)]


def zhou(m=ID):
    """周（调 的右边）：竖撇、横折钩，里面 土 + 口。"""
    return [shupie(m.x(200), m.y(840), m.x(40), m.y(-60), head="cut", w0=V(0.95)), HZG_(m, 200, 820, 790, -50),
            S_(m, 510, 690, 440, end="hid"), H_(m, 380, 650, 590, beak=0.5), H_(m, 360, 670, 440, beak=0.5)] + \
        KOU_(m, 400, 630, 300, 100, foot=30)


# ───────── 第四组的字 ─────────

def c_ju_according():          # 据
    return lr(shou, ju_reside, (360, -70, 945, 880), 0.88)


def c_si_die():                # 死
    return _w(0.92, lambda: [heng(56, 944, 790)] + xi_(into((60, -60, 520, 760))) + bi(into((500, -60, 930, 700))))


def c_gai_should():            # 该
    return lr(yan_left, hai_pig, (340, -70, 945, 880), 0.9)


def c_wang_hope():             # 望
    def top(m):
        return wang_lost(m.into((60, 380, 470, 900))) + yue_left(m.into((520, 320, 930, 895), (40, -70, 420, 880)))
    return tb(top, wang, (100, -70, 900, 330), 0.88)


def c_ling_lead():             # 领
    return lr(lambda m: ling_order(into((40, -70, 480, 880)), na_end=(760, 520)), ye_page, (480, -70, 945, 880), 0.88)


def c_chuan():                 # 传
    return lr(ren_left, zhuan, (330, -70, 945, 880), 0.9)


def c_dai_belt():              # 带
    return _w(0.9, lambda: [heng(56, 944, 730), shu(280, 860, 600), shu(500, 880, 620), shu(720, 860, 600),
                            D_(ID, (112, 560), (132, 440), w=V(1.05)), hook_down(132, 890, 500, entry=None),
                            shu(250, 370, 0), hengzhegou(250, 750 + V() / 2, 330, 0),
                            shu(500, 500, -70, top="hid", end="needle")])


def c_zheng_contend():         # 争
    p0, p1 = (430, 880), (140, 640)
    x0 = han.on_pie(p0, p1, (0, 0), 790)[0]
    return _w(0.92, lambda: [pie(p0, p1, w0=V(0.95)), hengpie(x0, 720, 790, (520, 575), w0=V(0.85), entry=None),
                             hengzhe(200, 760 + V() / 2, 560, 250),
                             heng(56, 944, 410, beak=0.8),
                             heng(200, 760, 280, beak=False, right_hid=True),
                             shugou(500, 560, -60, top="hid")])


def c_feng():                  # 风
    return [shupie(290, 820, 50, -50, head="cut"), hengxiegou(290, 720, 760, (900, -40), end=300, entry=None),
            pie((580, 560), (300, 140), w0=V(0.95)), dian((330, 520), (650, 170), w=V(1.1))]


def c_bu_step():               # 步
    return _w(0.9, lambda: [shu(500, 880, 430, end="hid"), heng(500, 800, 690, entry=None, beak=0.6),
                            shu(260, 640, 430, end="hid"), heng(56, 944, 430),
                            pie((330, 320), (110, 110), w0=V(0.9)), shu(500, 340, _bu_y, end="hid"),
                            pie(_BU_P0, _BU_P1, bend=_BU_B, w0=V(1.05))])


_BU_P0, _BU_P1, _BU_B = (790, 310), (90, -60), (-60, -60)
_bu_y = pie_at_x(_BU_P0, _BU_P1, _BU_B, 500)[1]       # 步 下面那一竖藏进长撇的中线


def c_ji_aid():                # 济
    return lr(shui, qi_even, (330, -70, 945, 880), 0.9)


def qi_even(m=ID):
    """齐（济 的右边）：文（撇捺张开）、竖撇、竖。"""
    return [D_(m, (470, 920), (530, 845)), H_(m, 56, 944, 720),
            P_(m, (690, 715), (250, 430), bend=(-20, -20), w0=V(0.75), head="hid"),
            N_(m, (300, 715), (800, 440), bend=(20, -30)),
            shupie(m.x(330), m.y(370), m.x(100), m.y(-60), head="cut", w0=V(0.9)), S_(m, 670, 370, -70)]


def c_qin():                   # 亲
    # 立 的一点一撇落在下面那一横上（起笔不藏进上横：起笔落在别的轮廓里，系统渲染会把这一笔当成字怀）
    return _w(0.9, lambda: [dian((470, 910), (540, 815)), heng(150, 850, 740), dian((300, 665), (330, 600), w=V(0.8)),
                            pie((720, 645), (690, 580), w0=V(0.75)), heng(56, 944, 560), heng(130, 870, 380, beak=0.7),
                            shugou(500, 560, -50, top="hid"), pie((470, 360), (110, 80), w0=V(0.9), head="hid"),
                            dian((540, 350), (860, 100), w=V(1.05))])


def yang_center(m=ID):
    """央（英 的下面）：冂、长横、撇从框顶起笔穿下来、捺。"""
    P0, P1, B = m.p((500, 720)), m.p((80, -60)), m.v((10, -70))
    # 左竖的头按绝对距离高出横 40（压扁了也不擦着横走）
    return [shu(m.x(250), m.y(720) + 40, m.y(420), end="hid"), HZ_(m, 250, 750, 720, 420, end="hid"), H_(m, 56, 944, 420),
            pie(P0, P1, B, w0=V(1.05) * (0.8 + 0.2 * m.k), head="hid"),
            na(han.on_pie(P0, P1, B, m.y(380)), m.p((860, -40)), m.v((30, -10)), wmax=V(1.18) * (0.8 + 0.2 * m.k))]


def c_ying_hero():             # 英
    return tb(cao, yang_center, (70, -70, 930, 570), 0.9)


def c_zhuan_turn():            # 转
    return lr(che_left, zhuan, (380, -70, 945, 880), 0.9)


def c_ling_order():            # 令
    return ling_order()


def c_ne():                    # 呢
    return lr(kou_left, lambda m: shi_corpse(m) + bi(m.into((300, -60, 930, 560))), (380, -70, 945, 880), 0.9)


def c_dan_single():            # 单
    return _w(0.9, lambda: [dian((300, 905), (370, 795), w=V(1.0)), pie((720, 900), (620, 770), w0=V(0.9))]
              + _kou(200, 800, 680, 320, foot=30)
              + [heng(200, 800, 500, beak=False, entry=None, right_hid=True),
                 shu(500, 680, -70, top="hid", end="needle"), heng(56, 944, 150)])


def c_ju_tool():               # 具
    return _w(0.9, lambda: [shu(280, 860, 200, end="hid"), hengzhe(280, 720 + V() / 2, 820, 200, end="hid"),
                            heng(280, 720, 660, beak=False, entry=None, right_hid=True),
                            heng(280, 720, 500, beak=False, entry=None, right_hid=True),
                            heng(280, 720, 345, beak=False, entry=None, right_hid=True),
                            heng(56, 944, 200), pie((390, 80), (110, -60), w0=V(0.95)),
                            dian((600, 130), (860, -40), w=V(1.15))])


def c_luo():                   # 罗
    return tb(wang_net, xi_, (40, -180, 960, 620), 0.9)


def c_ai():                    # 爱
    return tb(zhao_claw, you_friend, (80, -50, 920, 470), 0.88)


def c_ji_strike():             # 击
    return [heng(200, 800, 760), heng(56, 944, 540), shu(500, 880, 40, end="hid"),
            shuzhe(200, 380, 40, 800, right="hid"), shu(800, 380, -30)]


def c_liu_flow():              # 流
    return lr(shui, liu_r, (330, -70, 945, 880), 0.88)


def c_bing_soldier():          # 兵
    return _w(0.9, lambda: [pie((760, 890), (300, 790), bend=(0, -10), w0=V(0.9)), shu(280, 800, 300, end="hid"),
                            heng(280, 820, 560, entry=None, beak=0.6), shu(600, 560, 300, top="hid", end="hid"),
                            heng(56, 944, 300), pie((380, 200), (110, -40), w0=V(0.95)),
                            dian((600, 200), (850, -40), w=V(1.15))])


def c_diao():                  # 调
    return lr(yan_left, zhou, (340, -70, 935, 880), 0.88, lsx=0.85)


def c_ju_bureau():             # 局
    return _w(0.9, lambda: shi_corpse() + [hengzhegou(220, 840 + V() / 2, 460, -50)] + KOU_(ID, 380, 680, 330, 110, foot=30))



# ───────── 第五组的部件 ─────────

def guan_official(m=ID):
    """㠯（官 的下面）：通到底的左竖，右边上小下大两个框。"""
    # 左竖的头、上框右竖的脚都按绝对距离留（压扁的 官 里也不擦着横、不互相藏端点）
    return [han.shu(m.x(230), m.y(820) + 40, m.y(-60)),
            hengzhe(m.x(230), m.x(740) + han.V / 2, m.y(820), m.y(600) - 30),
            heng(m.x(230), m.x(740), m.y(600), beak=False, entry=None, right_hid=True),
            hengzhe(m.x(230), m.x(790) + han.V / 2, m.y(470), m.y(40) - 30),
            heng(m.x(230), m.x(790), m.y(40), beak=False, entry=None, right_hid=True)]


def zhi_quality(m=ID):
    """质：平撇、竖撇、短横接竖（十）、贝。"""
    return [P_(m, (820, 890), (240, 790), bend=(0, -10), w0=V(0.9)),
            shupie(m.x(240), m.y(800), m.x(50), m.y(-60), head="cut", w0=V(0.95)),
            H_(m, 240, 800, 640, entry=None, beak=0.6), S_(m, 560, 740, 520, end="hid")] + \
        bei(m.into((280, -70, 940, 560)))


def yu_surplus(m=ID):
    """余（除 的右边）：人字头、两横、竖钩、撇、点。"""
    P0, P1, B = m.p((500, 880)), m.p((80, 560)), m.v((-20, -10))
    k = 0.8 + 0.2 * m.k
    return [pie(P0, P1, B, w0=V(1.04) * k),
            na(han.on_pie(P0, P1, B, m.y(780)), m.p((800, 560)), m.v((40, -10)), wmax=V(1.1) * k),
            H_(m, 250, 750, 560, beak=0.6), H_(m, 70, 930, 380), SG_(m, 500, 560, -60, top="hid"),
            P_(m, (330, 280), (110, 60), w0=V(0.9)), D_(m, (680, 290), (840, 80), w=V(1.05))]


def jian_small(m=ID):
    """戋（线 的右边）：两道斜横、斜钩、撇、点。"""
    return [tilted(H_(m, 160, 760, 650, beak=0.6), 6, m.x(160), m.y(650)),
            tilted(H_(m, 56, 900, 440), 6, m.x(56), m.y(440)),
            xiegou(m.p((380, 880)), m.p((820, -40)), end=302),
            P_(m, (820, 330), (380, -40), w0=V(0.9)), D_(m, (600, 860), (720, 740), w=V(1.0))]


def gu_valley(m=ID):
    """谷（容 的下面）：八、人、口。"""
    P0, P1, B = m.p((500, 720)), m.p((90, 430)), m.v((-20, -10))
    k = 0.8 + 0.2 * m.k
    return [P_(m, (360, 880), (160, 720), w0=V(0.9)), D_(m, (630, 880), (810, 720), w=V(1.05)),
            pie(P0, P1, B, w0=V(1.0) * k),
            na(han.on_pie(P0, P1, B, m.y(630)), m.p((870, 430)), m.v((40, -10)), wmax=V(1.1) * k)] + \
        KOU_(m, 290, 710, 220, -40)


def xiao_small(m=ID):
    """肖（消 的右边）：⺌ + 月。"""
    return [S_(m, 500, 880, 690), D_(m, (230, 860), (310, 740), w=V(1.0)), P_(m, (800, 870), (680, 740), w0=V(0.9))] + \
        yue(m.into((120, -70, 900, 640)))


def mi_left(m=ID):
    """米（精 的左边）：捺写成点。"""
    return [D_(m, (100, 840), (160, 730), w=V(0.9)), P_(m, (370, 850), (310, 730), w0=V(0.8)),
            H_(m, 40, 420, 640, beak=0.5), S_(m, 220, 880, -70),
            P_(m, (200, 620), (50, 300), w0=V(0.85), head="hid"), D_(m, (240, 560), (350, 420), w=V(0.9))]


def yu_rain_top(m=ID):
    """雨（需 的头）：横、点、横钩、中竖、四个点，压扁画。"""
    return [H_(m, 120, 880, 840), D_(m, (150, 760), (170, 640), w=V(1.0)),
            han.hook_down(m.x(170), m.x(860), m.y(700), entry=None), S_(m, 500, 840, 470, top="hid"),
            D_(m, (300, 628), (345, 595), w=V(0.75)), D_(m, (300, 518), (345, 483), w=V(0.75)),
            D_(m, (655, 628), (700, 595), w=V(0.75)), D_(m, (655, 518), (700, 483), w=V(0.75))]


def suan_lower(m=ID):
    """算 的下面：目、长横、廾。"""
    return KOU_(m, 270, 730, 830, 490, foot=30) + [INNER_(m, 270, 730, 717), INNER_(m, 270, 730, 603),
                                                 H_(m, 56, 944, 270),
                                                 shupie(m.x(360), m.y(340), m.x(80), m.y(-60), head="cut", w0=V(0.95)),
                                                 S_(m, 650, 340, -70)]


# ───────── 第五组的字 ─────────

def c_ji_skill():              # 技
    return lr(shou, zhi_branch, (360, -70, 945, 880), 0.9)


def c_cheng_city():            # 城
    return lr(tu_left, lambda m: cheng(m, xie_top=(620, 880), dot=((760, 880), (840, 790))), (360, -70, 945, 880), 0.9)


def c_hua_china():             # 华
    return tb(hua, shi_, (70, -70, 930, 450), tbox=(100, 380, 900, 900))


def c_dang_party():            # 党
    return tb(chang_top, xiong, (120, -70, 880, 560), 0.88)


def c_zhi_quality():           # 质
    return _w(0.9, zhi_quality)


def c_guan_official():         # 官
    return tb(mian, guan_official, (150, -70, 850, 580), 0.9)


def c_bao_wrap():              # 包
    p0, p1 = (360, 880), (110, 540)
    x0 = han.on_pie(p0, p1, (0, 0), 740)[0]
    return [pie(p0, p1, w0=V(0.95)), hengzhegou(x0, 850 + V() / 2, 740, -40),
            ] + si_snake(into((180, 60, 780, 640), (170, 440, 930, 880)))


def c_pian():                  # 片
    return [han.shupie(250, 820, 60, -60, head="cut"), shu(560, 880, 600, end="hid"),
            heng(250, 930, 600, entry=None), hengzhe(250, 600 + V() / 2, 400, -60, entry=None)]


def c_shi_history():           # 史
    return shi_history()


def c_hu_q():                  # 乎
    # 竖钩的头藏在平撇里：平撇在 x 450～550 处的上下沿量过，竖钩从 815 起笔
    return [pie((760, 890), (250, 790), bend=(0, -10), w0=V(0.95)), dian((280, 710), (345, 605), w=V(1.0)),
            pie((780, 700), (640, 560), w0=V(0.9)), heng(56, 944, 470), shugou(500, 815, -60, top="hid")]


def c_chu_remove():            # 除
    return lr(fu_left, yu_surplus, (400, -70, 945, 880), 0.88)


def c_nong():                  # 农
    p0, p1, bend = (560, 880), (60, 120), (-30, -40)
    return _w(0.92, lambda: [dian((110, 800), (130, 680), w=V(1.05)), hook_down(130, 880, 730, entry=None),
                             pie(p0, p1, bend=bend, w0=V(1.0)),
                             han.shuti(300, 470, 20, (560, 150)),
                             pie((840, 560), (650, 400), w0=V(0.85)),
                             na(han.on_pie(p0, p1, bend, 560), (840, -30), bend=(-40, -60), wmax=V(1.15))])


def c_tu_picture():            # 图
    return _w(0.9, lambda: _kou(110, 890, 820, -40) + zhi_go_top(into((210, 270, 790, 730)), na_end=(840, 430))
              + [dian((450, 360), (520, 300), w=V(0.9)), dian((450, 220), (530, 140), w=V(0.95))])


def c_yi_doctor():             # 医
    return _w(0.9, lambda: qu_frame() + shi_arrow_full(into((270, 120, 870, 750))))


def c_xian_line():             # 线
    return lr(si_left, jian_small, (380, -70, 945, 880), 0.9)


def c_jiu_research():          # 究
    return tb(xue_cave, jiu, (120, -70, 880, 450), 0.9)


def c_rong():                  # 容
    return tb(xue_cave, gu_valley, (90, -70, 910, 460), 0.88)


def c_xiao_vanish():           # 消
    return lr(shui, xiao_small, (330, -70, 945, 880), 0.9)


def c_xu_must():               # 须
    # 彡 靠右的一侧是三个撇头，按轮廓量的间距看上去偏松，收到 60（同 阝）
    return lr(lambda m: shan_hair(into((20, -70, 510, 880))), ye_page, (480, -70, 870, 880), 0.9, gap=60)


def c_bing_ill():              # 病
    return _w(0.88, lambda: guang_() + [dian((70, 600), (140, 500), w=V(0.9)), ti((80, 220), (190, 320), w0=V(0.9)),
                                       heng(320, 900, 550, beak=0.6), shu(380, 430, -40),
                                       hengzhegou(380, 860 + V() / 2, 390, -50),
                                       pie((600, 545), (460, 120), w0=V(0.85), head="hid"),
                                       dian((565, 330), (720, 130), w=V(0.95))])


def c_jing_fine():             # 精
    return lr(mi_left, qing, (400, -70, 945, 880), 0.88)


def c_man_full():              # 满
    return lr(shui, lambda m: cao(m.into((70, 600, 930, 880), (70, 580, 930, 880))) + liang(m.into((70, -70, 930, 560))),
              (330, -70, 945, 880), 0.88)


def c_xu_need():               # 需
    return tb(yu_rain_top, er_and, (90, -70, 910, 400), 0.88)


def c_suan():                  # 算
    return tb(zhu_top, suan_lower, (90, -70, 910, 580), 0.88)



# ───────── 第六组的部件 ─────────

def shi_arrow_full(m=ID, na_end=(880, -40)):
    """矢（医 的里面、候 的右下）：撇、短横、长横、从短横起笔的长撇、捺。放进窄框时捺收短。"""
    k = 0.8 + 0.2 * m.k
    p0, p1 = m.p((420, 880)), m.p((200, 620))
    x0 = han.on_pie(p0, p1, (0, 0), m.y(720))[0]
    P0, P1, B = m.p((540, 720)), m.p((120, -50)), m.v((-10, -40))
    return [pie(p0, p1, w0=V(0.9) * k), heng(x0, m.x(820), m.y(720), entry=None, beak=0.6), H_(m, 80, 920, 470),
            pie(P0, P1, B, w0=V(1.0) * k, head="hid"),
            na(han.on_pie(P0, P1, B, m.y(420)), m.p(na_end), m.v((20, -20)), wmax=V(1.1) * k)]


def shi_pig(m=ID, top=True, na_end=(880, 120), xg=450, tails=((120, 450), (80, 340), (60, 50))):
    """豕（家 的下面；top=False 时没有顶横，撇从上面别的横里起笔，象 的下半）：
    横、撇、从撇上起笔的弯钩、两个左撇、右边短撇、捺。
    压窄时（像）几笔左撇会和弯钩挤成一束：弯钩往左挪（xg）、左撇的尾巴往左摊开（tails）。"""
    k = 0.8 + 0.2 * m.k
    t1, t2, t3 = tails
    P0, P1, B = m.p((500, 820)), m.p(t1), m.v((-30, -30))
    xg = m.x(xg)
    # 弯钩的顶边两端都落在撇的中线上（顶边顺着撇斜），压窄、压扁了也藏得住
    yl, yr = pie_at_x(P0, P1, B, xg - han.V / 2)[1], pie_at_x(P0, P1, B, xg + han.V / 2)[1]
    out = [H_(m, 170, 830, 820)] if top else []
    hook = han.wangou(xg, yl, m.y(-50), dx=-110 * m.k, dy=80 * m.k, y0r=yr)
    # 弯钩是弧的，两个左撇的头按弯钩在那个高度的实际中线摆，压窄了也藏得住
    h1, h2 = ((_mid_x(hook, m.y(y)), m.y(y)) for y in (580, 420))
    return out + [pie(P0, P1, B, w0=V(0.7) * k, head="hid"), hook,
                  pie(h1, m.p(t2), w0=V(0.85) * k, head="hid"),
                  pie(h2, m.p(t3), m.v((-20, -30)), w0=V(0.95) * k, head="hid"),
                  P_(m, (820, 650), (480, 520), w0=V(0.85)),
                  na((_mid_x(hook, m.y(530)), m.y(530)), m.p(na_end), m.v((-20, -40)), wmax=V(1.15) * k)]


def _mid_x(shape, y):
    """一条轮廓在高度 y 处左右两边的中点。"""
    pts = shape.flatten(2)
    xs = []
    for (x0, y0), (x1, y1) in zip(pts, pts[1:] + pts[:1]):
        if (y0 - y) * (y1 - y) <= 0 and y0 != y1:
            xs.append(x0 + (x1 - x0) * (y - y0) / (y1 - y0))
    return (min(xs) + max(xs)) / 2


def xiang_elephant(m=ID, na_end=(880, 120), **pig):
    """象（像 的右边，也可整字用）：⺈、扁口、豕（没有顶横，撇从口的底横起笔）。放进窄的右框时捺收短。"""
    k = 0.8 + 0.2 * m.k
    p0, p1 = m.p((420, 880)), m.p((170, 720))
    x0 = han.on_pie(p0, p1, (0, 0), m.y(810))[0]
    return [pie(p0, p1, w0=V(0.9) * k), hengpie(x0, m.x(640), m.y(810), m.p((480, 670)), w0=V(0.8) * k, entry=None)] + \
        KOU_(m, 230, 740, 660, 520, foot=30) + shi_pig(m.into((70, -70, 930, 563)), top=False, na_end=na_end, **pig)


def jiao_horn(m=ID):
    """角（确 的右边；解 的左边压窄用）：⺈ + 用。"""
    k = 0.8 + 0.2 * m.k
    p0, p1 = m.p((430, 880)), m.p((170, 700))
    x0 = han.on_pie(p0, p1, (0, 0), m.y(800))[0]
    return [pie(p0, p1, w0=V(0.95) * k), hengpie(x0, m.x(700), m.y(800), m.p((500, 630)), w0=V(0.8) * k, entry=None)] + \
        yong(m.into((70, -70, 930, 660)))


def lou_left(m=ID):
    """娄（数 的左边）：米 + 女。"""
    return mi_rice(m.into((40, 300, 560, 860)), top=((250, 889), (300, 812), (760, 890), (670, 822), 0.85)) + \
        c_nv_m(m.into((40, -70, 560, 460)))


def yin_long(m=ID):
    """廴（建 的外面）：横折折撇、平捺。"""
    return [hengzhezhepie(m.x(70), m.x(300), m.y(780), m.p((80, 480)), m.x(300), m.p((60, 150)),
                          w0=V(0.8), w2=V(0.86), bend2=m.v((-10, 10))),
            na(m.p((92, 190)), m.p((920, -40)), m.v((-150, -110)), wmax=V(1.12), w0=34, foot=0.42, start="tip")]


def yu_pen(m=ID):
    """聿（建 的里面）：横折的小框、中间最长的横、框底、两横、穿下来的一竖。"""
    return [hengzhe(m.x(160), m.x(760) + han.V / 2, m.y(800), m.y(560) - 30),
            H_(m, 100, 900, 680), heng(m.x(160), m.x(760), m.y(560), beak=False, right_hid=True),
            H_(m, 180, 760, 430, beak=0.6), H_(m, 110, 880, 280), S_(m, 500, 880, -60)]


def guan_whole(m=ID):
    """官（管 的下面）：宀 + 㠯，按 官 的摆法。"""
    return mian(m) + guan_official(m.into((150, -70, 850, 470)))


def de_virtue_r(m=ID):
    """德 的右边：十、罒、一、心。"""
    return [S_(m, 500, 880, 700, end="hid"), H_(m, 160, 840, 790, beak=0.7)] + \
        wang_net(m.into((150, 540, 850, 710), (150, 620, 850, 872))) + [H_(m, 56, 900, 410)] + \
        xin_di(m.into((40, -70, 945, 320)))


def qiang_r(m=ID):
    """强 的右边：口 + 虫（口、穿过口的竖、提、点）。"""
    t0, t1 = (80, 30), (660, 175)
    return KOU_(m, 270, 730, 840, 630, foot=38) + KOU_(m, 230, 770, 470, 240, foot=38) + [
        _shu_to_line(m, 500, 530, t0, t1), T_(m, t0, t1, w0=V(1.1)), D_(m, (760, 150), (880, 10), w=V(1.1))]


def _shu_to_line(m, x, y0, p0, p1):
    """竖往下写到一条斜笔（提）的中线上收住：末端左右两角各自落在中线上，藏进那一笔里。p0、p1 是那一笔中线的两端。"""
    X = m.x(x)
    k = (p1[1] - p0[1]) / (p1[0] - p0[0])
    at = lambda xx: m.y(p0[1] + k * ((xx - m.bx) / m.ax - p0[0]))
    l, r = X - han.V / 2, X + han.V / 2
    return Shape(han.shu_top(X, m.y(y0)) + [n(r, at(r), hid=True), n(l, at(l), hid=True, t="line")], name="竖")


def hou_r(m=ID):
    """候 的右边：短竖、横折、矢。"""
    return [S_(m, 120, 640, 160), hengzhe(m.x(250), m.x(760) + han.V / 2, m.y(820), m.y(700))] + \
        shi_arrow_full(m.into((240, -70, 930, 650)), na_end=(780, -40))


def jing_view_left(m=ID):
    """景（影 的左边）：日 + 京。"""
    # 日 和 京 摞在一起，竖向很挤：京 按笔画间距重新排（点、横、口都往下挪，小 收短）
    return KOU_(m, 140, 460, 865, 680, foot=30) + [INNER_(m, 140, 460, 772)] + \
        jing_capital_left(m, ys=(600, 556, 430, 305, 205, 93, 40, 93, -30), gou=(-80, 64))


def shen_deep_r(m=ID):
    """罙（深 的右边）：冖、八、木。"""
    return [D_(m, (110, 830), (130, 710), w=V(1.05)), han.hook_down(m.x(130), m.x(890), m.y(760), entry=None),
            P_(m, (390, 660), (210, 540), w0=V(0.85)), D_(m, (600, 660), (770, 540), w=V(0.95))] + \
        mu(m.into((70, -70, 880, 500)))


def shu_bind(m=ID):
    """束（整 的左上）：一、口、穿过口的竖、撇、点。"""
    return [H_(m, 56, 944, 720), S_(m, 500, 880, -70)] + KOU_(m, 250, 750, 590, 330, foot=50) + [
        P_(m, (480, 320), (80, -20), w0=V(0.9), head="hid"), D_(m, (540, 300), (820, 60), w=V(1.05))]


def duan_left(m=ID):
    """断 的左边：米 + 竖折（𠃊）。"""
    return [shuzhe(m.x(90), m.y(860), m.y(80), m.x(520), right="beak"),
            D_(m, (180, 800), (230, 710), w=V(0.85)), P_(m, (450, 810), (400, 710), w0=V(0.75)),
            H_(m, 185, 480, 620, beak=0.5), S_(m, 310, 790, 200),
            P_(m, (295, 600), (180, 340), w0=V(0.8), head="hid"), D_(m, (330, 560), (450, 420), w=V(0.85))]


def zhao_top(m=ID):
    """昭（照 的上面）：日 + 召（刀 + 口）。"""
    return KOU_(m, 110, 300, 860, 380, foot=30) + [INNER_(m, 110, 300, 620)] + \
        dao_knife(m.into((430, 620, 930, 900))) + KOU_(m, 500, 860, 520, 380, foot=30)


def yue_axe(m=ID):
    """戉（越 的右边）：横、竖提、斜钩、撇、点。"""
    return [H_(m, 360, 944, 620), shuti(m.x(180), m.y(600), m.y(260), m.p((400, 340))),
            xiegou(m.p((520, 880)), m.p((850, 0)), end=302),
            P_(m, (880, 460), (500, 60), w0=V(0.9)), D_(m, (690, 860), (780, 760), w=V(1.0))]


def zeng(m=ID):
    """曾（增 的右边）：丷（右边的撇落到框顶）、中间有竖的框、框里一点一撇、日。"""
    return [D_(m, (250, 900), (318, 812), w=V(1.0)), P_(m, (760, 890), (520, 720), w0=V(0.9))] + \
        KOU_(m, 160, 840, 700, 440, foot=30) + [S_(m, 500, 700, 440, top="hid", end="hid"),
                                              D_(m, (190, 610), (300, 560), w=V(0.85)),
                                              P_(m, (840, 650), (560, 520), w0=V(0.8), head="hid")] + \
        KOU_(m, 240, 760, 300, -40, foot=30) + [INNER_(m, 240, 760, 130)]


def zhuang_top(m=ID):
    """壮（装 的上面）：丬 + 士。"""
    return jiang_left(m.into((70, 400, 844, 900))) + [H_(m, 420, 920, 740), S_(m, 670, 880, 530, end="hid"),
                                                      H_(m, 450, 870, 530, beak=0.6)]


def yi_cloth(m=ID):
    """衣（装 的下面）：点、长横、从横起笔的长撇、竖提、捺、右边短撇。"""
    k = 0.8 + 0.2 * m.k
    P0, P1, B = m.p((480, 700)), m.p((80, 150)), m.v((-20, -30))
    xs = m.x(330)
    ys = pie_at_x(P0, P1, B, xs - han.V / 2)[1]      # 竖提的头左角搭在长撇的中线上
    return [D_(m, (470, 905), (540, 815)), H_(m, 56, 944, 700), pie(P0, P1, B, w0=V(0.95) * k, head="hid"),
            shuti(xs, ys - 16, m.y(-40), m.p((600, 80))),
            na(m.p((500, 690)), m.p((850, -20)), m.v((-40, -60)), wmax=V(1.15) * k),
            P_(m, (840, 640), (680, 500), w0=V(0.85))]


# ───────── 第六组的字 ─────────

def c_jia_home():              # 家
    return tb(mian, shi_pig, (80, -70, 920, 600), 0.88)


def c_xiang_elephant():        # 象
    return _w(0.88, xiang_elephant)


def c_xiang_image():           # 像
    return lr(ren_left, lambda m: xiang_elephant(m, na_end=(800, 120), xg=420, tails=((40, 470), (-40, 360), (-60, 60))),
              (330, -70, 945, 880), 0.88)


def c_jie_solve():             # 解
    return lr(lambda m: jiao_horn(into((65, -70, 500, 880))),
              lambda m: dao_knife(m.into((70, 470, 930, 880))) + niu(m.into((70, -70, 930, 520))),
              (520, -70, 945, 880), 0.88)


def c_que_sure():              # 确
    return lr(shi_stone_left, jiao_horn, (400, -70, 945, 880), 0.88)


def c_ti_topic():              # 题
    # 是 在左边，𤴓 的捺一直伸到 页 下面：按 𤴓 自己的坐标反算捺的终点
    left = into((60, -70, 520, 880))
    f = left.into((70, -40, 930, 470))
    end = ((900 - f.bx) / f.ax, (-40 - f.by) / f.ay)
    return _w(0.88, lambda: shi_is(left, na_end=end, shu_end="na") + ye_page(into((520, 210, 935, 880))))


def c_shu_number():            # 数
    return lr(lou_left, lambda m: pu(m, na_end=(720, -40)), (540, -70, 945, 880), 0.88)


def c_jian_build():            # 建
    return bao(yin_long, yu_pen, (330, 180, 930, 890), 0.9)


def c_guan_manage():           # 管
    return tb(zhu_top, guan_whole, (70, -70, 930, 570), 0.88)


def c_de_virtue():             # 德
    return lr(chi_left, de_virtue_r, (380, -70, 945, 880), 0.88, lsx=0.85)


def c_zhan_unfold():           # 展
    return _w(0.88, lambda: shi_corpse() + [heng(330, 830, 520, beak=0.6), shu(470, 600, 360, end="hid"),
                                           shu(680, 600, 360, end="hid"), heng(280, 900, 360),
                                           han.shuti(360, 360, -30, (600, 90), top="hid"),
                                           na((520, 350), (860, -40), bend=(-40, -60), wmax=V(1.1)),
                                           pie((790, 355), (640, 200), w0=V(0.85), head="hid")])


def c_qiang():                 # 强
    return lr(gong_bow, qiang_r, (400, -70, 945, 880), 0.88)


def c_hou():                   # 候
    return lr(ren_left, hou_r, (330, -70, 945, 880), 0.9)


def c_ying_shadow():           # 影
    return lr(jing_view_left, shan_hair, (600, -70, 945, 880), 0.88, gap=60)


def c_shen_deep():             # 深
    return lr(shui, shen_deep_r, (330, -70, 945, 880), 0.88)


def c_shang_trade():           # 商
    return _w(0.88, lambda: [dian((470, 910), (540, 830)), heng(56, 944, 780), dian((300, 710), (370, 650), w=V(0.95)),
                             pie((720, 680), (620, 620), w0=V(0.85)), shu(170, 570, -60),
                             hengzhegou(170, 830 + V() / 2, 530, -50), pie((440, 425), (300, 325), w0=V(0.85)),
                             dian((570, 430), (690, 345), w=V(0.95))] + _kou(350, 620, 200, 40, foot=30))


def c_zheng_whole():           # 整
    def top(m):
        return shu_bind(m.into((60, 430, 540, 900))) + pu(m.into((570, 430, 940, 900)), na_end=(720, -40))
    return tb(top, zheng, (80, -70, 920, 380), 0.88)


def c_li_leave():              # 离
    return _w(0.88, lambda: [dian((470, 910), (540, 820)), heng(56, 944, 740),
                             shu(250, 650, 470), shu(750, 650, 470),
                             pie((640, 630), (330, 470), w0=V(0.85)), dian((370, 630), (620, 490), w=V(1.0)),
                             shu(170, 400, -60), hengzhegou(170, 830 + V() / 2, 360, -50),
                             piezhe((500, 260), (370, 70), (700, 180), w=V(0.7)),
                             dian((580, 235), (680, 130), w=V(0.9))])


def c_fu_again():              # 复
    p0, p1 = (380, 880), (140, 640)
    x0 = han.on_pie(p0, p1, (0, 0), 790)[0]
    return _w(0.9, lambda: [pie(p0, p1, w0=V(0.95)), heng(x0, 860, 790, entry=None)] + _kou(260, 740, 680, 490, foot=30)
              + [heng(260, 740, 585, beak=False, entry=None, right_hid=True)] + zhi_go_top(into((70, -70, 930, 380))))


def c_duan():                  # 断
    return lr(duan_left, jin_axe, (560, -70, 945, 880), 0.88)


def c_zhao_shine():            # 照
    return tb(zhao_top, lambda m: huo_dots(m.into(FULL, (60, -70, 940, 160))), (60, -70, 940, 250), 0.88)


def c_yue_exceed():            # 越
    # 走 的捺一直伸到 戉 下面：按 𤴓 自己的坐标反算捺的终点
    left = into((40, -70, 520, 880))
    f = left.into((70, -60, 930, 581))
    end = ((895 - f.bx) / f.ax, (-40 - f.by) / f.ay)
    return _w(0.88, lambda: zou_walk(left, na_end=end, shu_end="na")
              + yue_axe(into((490, 200, 940, 880))))


def c_zeng_add():              # 增
    return lr(tu_left, zeng, (360, -70, 945, 880), 0.88)


def c_zhuang():                # 装
    return tb(zhuang_top, yi_cloth, (60, -60, 940, 520), 0.88)


GLYPHS = {
    "没": c_mei_not, "因": c_yin, "军": c_jun, "造": c_zao_make, "联": c_lian_join, "持": c_chi_hold, "组": c_zu,
    "快": c_kuai, "办": c_ban, "议": c_yi_discuss, "证": c_zheng_proof, "怎": c_zen, "叫": c_jiao_call, "台": c_tai,
    "连": c_lian_link, "价": c_jia_price, "况": c_kuang, "际": c_ji_border, "约": c_yue_about, "示": c_shi_show,
    "息": c_xi_breath, "似": c_si_like, "视": c_shi_look, "称": c_cheng_call,
    "功": c_gong_merit, "委": c_wei_entrust, "查": c_cha, "轻": c_qing_light, "易": c_yi_easy, "找": c_zhao_find,
    "广": c_guang_wide, "显": c_xian_show, "引": c_yin_pull, "历": c_li_history, "首": c_shou_head, "更": c_geng,
    "至": c_zhi_arrive, "团": c_tuan, "石": c_shi_stone, "火": c_huo_fire, "支": c_zhi_branch, "始": c_shi_begin,
    "备": c_bei_prepare, "研": c_yan_grind, "吃": c_chi_eat, "马": c_ma_horse, "吗": c_ma_q, "存": c_cun_exist,
    "布": c_bu_cloth,
    "能": c_neng, "而": c_er_and, "面": c_mian_face, "看": c_kan, "前": c_qian_front, "第": c_di_order, "被": c_bei_by,
    "制": c_zhi_make, "身": c_shen_body, "海": c_hai, "每": c_mei_every, "教": c_jiao_teach, "声": c_sheng_sound,
    "及": c_ji_reach, "系": c_xi_system, "变": c_bian_change, "报": c_bao_report, "服": c_fu_serve, "场": c_chang_field,
    "资": c_zi_capital, "统": c_tong_unite, "形": c_xing_shape, "路": c_lu_road, "求": c_qiu, "级": c_ji_level,
    "极": c_ji_pole,
    "据": c_ju_according, "死": c_si_die, "该": c_gai_should, "望": c_wang_hope, "领": c_ling_lead, "传": c_chuan,
    "带": c_dai_belt, "争": c_zheng_contend, "风": c_feng, "步": c_bu_step, "济": c_ji_aid, "亲": c_qin,
    "英": c_ying_hero, "转": c_zhuan_turn, "令": c_ling_order, "呢": c_ne, "单": c_dan_single, "具": c_ju_tool,
    "罗": c_luo, "爱": c_ai, "击": c_ji_strike, "流": c_liu_flow, "兵": c_bing_soldier, "调": c_diao, "局": c_ju_bureau,
    "技": c_ji_skill, "城": c_cheng_city, "华": c_hua_china, "党": c_dang_party, "质": c_zhi_quality,
    "官": c_guan_official, "包": c_bao_wrap, "片": c_pian, "史": c_shi_history, "乎": c_hu_q, "除": c_chu_remove,
    "农": c_nong, "图": c_tu_picture, "医": c_yi_doctor, "线": c_xian_line, "究": c_jiu_research, "容": c_rong,
    "消": c_xiao_vanish, "须": c_xu_must, "病": c_bing_ill, "精": c_jing_fine, "满": c_man_full, "需": c_xu_need,
    "算": c_suan,
    "家": c_jia_home, "象": c_xiang_elephant, "像": c_xiang_image, "解": c_jie_solve, "确": c_que_sure, "题": c_ti_topic,
    "数": c_shu_number, "建": c_jian_build, "管": c_guan_manage, "德": c_de_virtue, "展": c_zhan_unfold, "强": c_qiang,
    "候": c_hou, "影": c_ying_shadow, "深": c_shen_deep, "商": c_shang_trade, "整": c_zheng_whole, "离": c_li_leave,
    "复": c_fu_again, "断": c_duan, "照": c_zhao_shine, "越": c_yue_exceed, "增": c_zeng_add, "装": c_zhuang,
}
