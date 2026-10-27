"""渡言的常用字（第六批）：按使用频率挑的高频字，规矩照 docs/RULES.md：
笔画多的字整体减细（6 条轮廓 0.92，7～9 条 0.9，10 条以上 0.88，左右、上下拼的字最少 0.92），
钩用默认长度，口字框的脚 30～44；部件压进窄框时用收短捺的参数，不改捺的画法。
窄框、扁框里的小距离（口字框左竖的头、点和横之间）按绝对距离留；出字体后纵向 ×0.93，窄缝按设计坐标 37 留。"""
import han
from chars import _w, bao, c_nv_m, dong, fang, ji, lr, mao, mi_cover, tb, zhu_top
from chars2 import (bu, chi_left, dao_right, he_close, huo_dots, jing_well, kai, ren_narrow, si_,
                    you_frame, zhi_left, zou_di)
from chars3 import (bai, bi_compare, cai, ge_each, gong_share, guan, guang_, jiu, li_top, pie_at_x, qing,
                    shi_scholar, si_temple, tai_big, wu_five, xian_first, xiang_to, xin_di, yang, ye_work,
                    zhong)
from chars4 import (ba_snake, bei, bei_left, bing_left, dao_knife, dao_top, dou_ladle, er_ear,
                    fu_right, ge_halberd, gen, gong_bow, jiang_left, jiao, jie, jin_axe, jing_capital_left, mi_rice,
                    na_left, pu, qi_part, qian_owe, qie_and, se_color, shi_left, shi_style, shu_art, shu_weapon,
                    xue_cave, you_r, yun, zhan_left, zhi_only, zhi_straight, zhu_master, zhui)
from chars5 import (_mid_x, ban, bu_cloth, che_left, chong, chong_insect, dan_single, dong_winter, gong_left, hai_pig,
                    huo_fire, ji_strike, ju_reside, ling_order, mi_left, mu_mother, mu_top, ni_nun, pi_skin, qiu,
                    shen_body, shi_corpse, shi_show, shi_stone_left, shu_bind, ye_page, yi_cloth, yu_pen,
                    zeng, zhi_stop, zhou, zhuan, zu_left)
from han import (_kou, dian, hengpie, hengpie_wangou, hengzhe, hengzhegou, hook_down, na, pie, piezhe, shu, shupie, shuti,
                 shuzhezhegou, ti, wangou, xiegou)
from parts import (D_, FULL, H_, HP_, HZG_, ID, INNER_, KOU_, P_, S_, SG_, SWG_, T_, cao, cun, da, er, fu_left, gu,
                   into, ke, kou, kou_left, li, mian, mu, mu_box, mu_left, ren, ren_left, ren_top, ri, she, sheng,
                   shou, shui, si_left, tian_, tu, tu_left, wang_left, xin_left, yan_left, you_left, yue_left, zi_,
                   zou)

V = lambda k=1.0: han.V * k      # noqa: E731


# ───────── 第一组的部件 ─────────

def hu_door(m=ID):
    """户（房 的外面，护 的右边）：点 + 尸（横折、底横、竖撇），尸 往下放，给点留地方。"""
    return [D_(m, (470, 915), (540, 832))] + shi_corpse(m.into((70, -70, 930, 760)))


# ───────── 第一组的字 ─────────

def c_si_this():               # 斯
    return lr(lambda m: qi_part(into((40, -70, 560, 880))), jin_axe, (560, -70, 945, 880), 0.88)


def c_er_you():                # 尔
    return er()


def c_ya():                    # 亚
    return _w(0.92, lambda: [H_(ID, 140, 860, 790)] + ye_work(into((70, -70, 930, 810)), vtop="hid"))


def c_qi_enterprise():         # 企
    return tb(ren_top, zhi_stop, (100, -70, 900, 520))


def c_a():                     # 阿
    return lr(fu_left, ke, (400, -70, 945, 880), 0.9)


def c_li_plum():               # 李
    return tb(mu_top, zi_, (100, -70, 900, 470), tbox=(70, 200, 930, 900))


def c_biao_mark():             # 标
    return lr(mu_left, shi_show, (380, -70, 945, 880), 0.9)


def c_zhuan_special():         # 专
    return zhuan()


def c_zhou_week():             # 周
    return _w(0.9, zhou)


def c_jiao_compare():          # 较
    return lr(che_left, lambda m: jiao(m, na_end=(760, -10)), (380, -70, 945, 880), 0.88)


def c_zhu_pour():              # 注
    return lr(shui, zhu_master, (330, -70, 945, 880), 0.9)


def c_jin_only():              # 仅
    return lr(ren_left, you_r, (330, -60, 945, 800))


def c_qing_blue():             # 青
    return _w(0.9, qing)


def c_xuan_choose():           # 选
    return bao(zou, xian_first, (330, 200, 930, 880), 0.9)


def c_xiang_sound():           # 响
    return lr(kou_left, lambda m: xiang_to(m, kou=(330, 560)), (380, -70, 945, 880), 0.9)


def c_tui_push():              # 推
    return lr(shou, zhui, (360, -70, 945, 880), 0.88)


def c_fang_house():            # 房
    return _w(0.9, lambda: hu_door() + fang(into((320, -70, 930, 310)), dot=(130, 90)))


def c_jie_section():           # 节
    return tb(cao, jie, (120, -90, 880, 560))


def c_tou_throw():             # 投
    return lr(shou, shu_weapon, (360, -70, 945, 880), 0.9)


def c_an_case():               # 案
    return tb(lambda m: mian(m) + c_nv_m(m.into((110, 300, 890, 540))), lambda m: mu(m, pie_w=V(0.7)),
              (70, -80, 930, 260), 0.88)


def c_wei_tie():               # 维
    return lr(si_left, zhui, (380, -70, 945, 880), 0.88)


def c_hua_draw():              # 划
    return lr(lambda m: ge_halberd(into((45, -70, 560, 880)), xie_top=(380, 880), dot=((610, 860), (720, 750))),
              dao_right, (600, -60, 925, 880))


def c_chen():                  # 陈
    return lr(fu_left, lambda m: dong(m, low=((330, 350), (110, 110), (730, 330), (870, 150))), (400, -70, 945, 880), 0.9)


def c_lv_law():                # 律
    return lr(chi_left, yu_pen, (380, -70, 945, 880), 0.9)


def c_hu_protect():            # 护
    return lr(shou, hu_door, (360, -70, 945, 880), 0.9)



# ───────── 第二组的部件 ─────────

def zi_left(m=ID):
    """子（孩 的左边）：了 + 提。"""
    return [hengpie_wangou(m.x(80), m.x(390), m.y(800), m.p((210, 620)), m.x(240), m.y(-50), w0=V(0.8),
                           dx=-80 * m.k, dy=64 * m.k),
            T_(m, (85, 320), (420, 450), w0=V(0.9))]


def li_left_stand(m=ID):
    """立（站 的左边）：底横变成提。"""
    return [D_(m, (240, 900), (300, 780), w=V(1.0)), H_(m, 60, 440, 650, beak=0.5),
            D_(m, (140, 560), (200, 330), w=V(0.9)), P_(m, (400, 560), (330, 330), w0=V(0.8)),
            T_(m, (85, 150), (470, 280), w0=V(0.9))]


def dai_left(m=ID):
    """歹（列 的左边）：一、从横里起笔的撇、横撇、框里一点。"""
    p0, p1 = m.p((300, 800)), m.p((80, 420))
    x0 = han.on_pie(p0, p1, (0, 0), m.y(620))[0]
    return [H_(m, 60, 520, 810, beak=0.5), pie(p0, p1, w0=V(0.9) * (0.8 + 0.2 * m.k), head="hid"),
            hengpie(x0, m.x(470), m.y(620), m.p((90, 40)), m.v((60, -40)), w0=V(0.9), entry=None),
            D_(m, (360, 520), (470, 400), w=V(0.95))]


# ───────── 第二组的字 ─────────

def c_tai_attitude():          # 态
    return tb(tai_big, xin_di, (70, -70, 930, 260), 0.9, tbox=(70, 330, 930, 900))


def c_hai_child():             # 孩
    return lr(zi_left, hai_pig, (380, -70, 945, 880), 0.9, lsx=0.9)


def c_xing_star():             # 星
    return tb(ri, lambda m: sheng(m, on_pie_x=True), (80, -70, 920, 560), 0.9, tbox=(220, 540, 780, 890))


def c_zhi_will():              # 志
    return tb(shi_scholar, xin_di, (70, -70, 930, 260), 0.9, tbox=(70, 330, 930, 900))


def c_zhan_stand():            # 站
    return lr(li_left_stand, lambda m: zhan_left(m.into(FULL, (40, -70, 500, 880))), (420, -70, 945, 880), 0.88)


def c_ba_hope():               # 巴
    return ba_snake()


def c_li_example():            # 例
    return lr(ren_left, lambda m: dai_left(m.into((70, -70, 560, 880))) + dao_right(m.into((560, -60, 935, 880))),
              (320, -70, 945, 880), 0.9)


def c_fang_defend():           # 防
    return lr(fu_left, fang, (400, -70, 945, 880), 0.9)


def c_gong_provide():          # 供
    return lr(ren_left, gong_share, (330, -70, 945, 880), 0.9)


def c_xiao_effect():           # 效
    return lr(lambda m: jiao(into((40, -70, 540, 880)), na_end=(780, -10)), lambda m: pu(m, na_end=(660, -40)),
              (540, -70, 945, 880), 0.88)


def c_jiang_speak():           # 讲
    return lr(yan_left, jing_well, (340, -70, 945, 880))


def c_liao():                  # 料
    return lr(mi_left, dou_ladle, (400, -70, 945, 880), 0.88)


def c_zhong_end():             # 终
    return lr(si_left, lambda m: dong_winter(m.into(FULL, (160, -10, 840, 790)), na_end=(800, 430)),
              (380, -70, 945, 880), 0.9)


def c_da_answer():             # 答
    return tb(zhu_top, he_close, (90, -70, 910, 580), 0.88)


def c_jue_cut():               # 绝
    return lr(si_left, se_color, (380, -70, 945, 880), 0.9)


def c_qi_strange():            # 奇
    return tb(da, lambda m: ke(m, kou=(200, 520, 495, 170, 44)), (80, -70, 920, 520), 0.9, tbox=(70, 520, 930, 900))


def c_yi_rely():               # 依
    return lr(ren_left, lambda m: yi_cloth(m, na_end=(770, -20)), (330, -70, 945, 880), 0.9)


def c_pi_criticize():          # 批
    return lr(shou, bi_compare, (360, -70, 945, 880), 0.9)


def c_xiang_item():            # 项
    return lr(gong_left, ye_page, (380, -70, 945, 880), 0.9)


def c_gu_reason():             # 故
    return lr(lambda m: gu(into((40, -70, 540, 880))), pu, (540, -70, 945, 880), 0.9)


def c_an_press():              # 按
    return lr(shou, lambda m: mian(m) + c_nv_m(m.into((100, -60, 900, 520))), (360, -70, 945, 880), 0.9)


def c_mi_rice():               # 米
    return _w(0.92, lambda: mi_rice(top=((240, 890), (320, 790), (780, 890), (660, 780), 1.2),
                                    low=(-70, (80, 120), (870, 170))))


def c_ke_guest():              # 客
    return tb(mian, ge_each, (120, -70, 880, 580), 0.9)


def c_ji_record():             # 纪
    return lr(si_left, ji, (380, -60, 930, 820))


def c_gong_attack():           # 攻
    return lr(gong_left, pu, (400, -70, 945, 880), 0.9)



# ───────── 第三组的字 ─────────

def c_xi_thin():               # 细
    return lr(si_left, tian_, (380, -40, 930, 820), 0.9)


def c_zhi_value():             # 值
    return lr(ren_left, lambda m: zhi_straight(m, kou=(410, 760)), (330, -70, 945, 880), 0.88)


def c_nan_male():              # 男
    return tb(tian_, li, (70, -70, 930, 480), 0.9, tbox=(220, 530, 780, 880))


def c_po_break():              # 破
    return lr(shi_stone_left, lambda m: pi_skin(m, na_end=(720, -40)), (400, -70, 945, 880), 0.88)


def c_zhu_help():              # 助
    return lr(lambda m: qie_and(into((40, -70, 560, 880)), ti=True), li, (560, -70, 945, 880), 0.9)


def c_dao_fall():              # 倒
    return lr(ren_left, lambda m: zhi_left(m.into((70, -70, 540, 880), (40, -70, 600, 880)), v_top=465) +
              dao_right(m.into((590, -60, 935, 880))), (320, -70, 945, 880), 0.88)


def c_xian_limit():            # 限
    return lr(fu_left, gen, (400, -70, 945, 880), 0.9)


def c_zhi_job():               # 职
    return lr(er_ear, lambda m: zhi_only(m, foot=44), (500, -70, 945, 880), 0.88)


def c_su_fast():               # 速
    return bao(zou, shu_bind, (330, 150, 930, 900), 0.88)


def c_ke_carve():              # 刻
    return lr(lambda m: hai_pig(into((40, -70, 600, 880))), dao_right, (600, -60, 945, 880), 0.9)


def c_fou():                   # 否
    return tb(lambda m: bu(m, v_end=330), kou, (150, -70, 850, 400), 0.9)


def c_mao_hair():              # 毛
    return mao(top_on_pie=True)


def c_qiu_ball():              # 球
    return lr(wang_left, lambda m: qiu(m, na_end=(800, 60)), (360, -70, 945, 880), 0.88)


def c_pa_fear():               # 怕
    return lr(xin_left, bai, (340, -70, 945, 880), 0.9)


def c_dan_bullet():            # 弹
    return lr(gong_bow, dan_single, (400, -70, 945, 880), 0.88)


def c_xiao_school():           # 校
    return lr(mu_left, lambda m: jiao(m, na_end=(760, -10)), (380, -70, 945, 880), 0.88)


def c_shi_try():               # 试
    return lr(yan_left, shi_style, (340, -70, 945, 880), 0.9)


def c_gu_stock():              # 股
    return lr(yue_left, shu_weapon, (380, -70, 945, 880), 0.9)


def c_shui_who():              # 谁
    return lr(yan_left, zhui, (340, -70, 945, 880), 0.88)


def c_na_which():              # 哪
    return lr(kou_left, lambda m: na_left(m.into((70, -70, 470, 880), (40, -70, 530, 880))) +
              fu_right(m.into((560, -70, 935, 880))), (330, -70, 945, 880), 0.88, lsx=0.8)


def c_ni_nun():                # 尼
    return ni_nun()


def c_song_send():             # 送
    return bao(zou, guan, (330, 180, 930, 860), 0.9)


def c_shi_fit():               # 适
    return bao(zou, she, (330, 150, 930, 900), 0.9)


def c_bo_wave():               # 波
    return lr(shui, lambda m: pi_skin(m, na_end=(800, -40)), (330, -70, 945, 880), 0.9)


def c_chu_begin():             # 初
    return lr(lambda m: shi_left(m, cloth=True), dao_knife, (420, -70, 945, 880), 0.9)



# ───────── 第四组的部件 ─────────

def gan_sweet(m=ID):
    """甘（某 的头）：长横、两竖、中横、底横（两竖往下多伸一点，底横两端藏进竖里）。"""
    return [H_(m, 70, 930, 700), S_(m, 300, 870, 330), S_(m, 700, 870, 330),
            INNER_(m, 300, 700, 540), INNER_(m, 300, 700, 370)]


def you_right(m=ID):
    """右（若 的下面）：𠂇 + 口。"""
    return you_frame(m) + KOU_(m, 380, 840, 420, 30)


# ───────── 第四组的字 ─────────

def c_dai_wait():              # 待
    return lr(chi_left, si_temple, (380, -70, 945, 880), 0.9)


def c_yun_cloud():             # 云
    return yun()


def c_leng():                  # 冷
    return lr(bing_left, lambda m: ling_order(m, na_end=(790, 490)), (340, -70, 945, 880), 0.9, gap=76)


def c_chong_rush():            # 冲
    return lr(bing_left, zhong, (340, -70, 945, 880), gap=76)


def c_dou():                   # 斗
    return dou_ladle(h_y=260)


def c_jing_capital():          # 京
    return _w(0.9, lambda: jing_capital_left(into(FULL, (40, -70, 560, 920)), ys=(925, 840, 700, 570, 400, 300, 60, 290, 120)))


def c_mu_mother():             # 母
    return mu_mother(into(FULL, (70, -70, 930, 650)))


def c_zhi_stop():              # 止
    return zhi_stop(into(FULL, (70, 400, 930, 900)))


def c_zu_foot():               # 足
    return _w(0.9, lambda: KOU_(ID, 250, 750, 860, 600, foot=30) + zou_di(into((70, -60, 930, 695)), heng_top=False))


def c_ban_half():              # 半
    return [dian((245, 865), (325, 748), w=V(1.0)), pie((720, 880), (620, 750), w0=V(0.9)), H_(ID, 200, 800, 620),
            H_(ID, 56, 944, 380), S_(ID, 500, 880, -70, end="needle")]


def c_fu_father():             # 父
    return [pie((400, 880), (170, 680), w0=V(0.95)), dian((610, 890), (790, 720), w=V(1.1)),
            pie((720, 620), (90, -50), bend=(-20, -40), w0=V(1.05)),
            na((290, 640), (840, -40), bend=(20, -40), wmax=V(1.18), start="tip")]


def c_ceng():                  # 曾
    return _w(0.88, lambda: zeng(pie_end=(590, 712)))


def c_ju_reside():             # 居
    return _w(0.9, ju_reside)


def c_chong_fill():            # 充
    return _w(0.92, chong)


def c_cai_wealth():            # 财
    return lr(bei_left, lambda m: cai(m, head=(610, 590)), (520, -70, 945, 880), 0.9)


def c_huan_joy():              # 欢
    return lr(you_left, lambda m: qian_owe(m, na_end=(730, -40)), (390, -70, 945, 880))


def c_fu_bear():               # 负
    return tb(dao_top, bei, (80, -70, 920, 560))


def c_shu_narrate():           # 述
    return bao(zou, shu_art, (330, 170, 900, 890), 0.9)


def c_lao_labor():             # 劳
    # 冖 只往下平移、不压扁（压扁了左点变细，盖不住横钩的起笔）
    return tb(lambda m: cao(m) + mi_cover(m.into((70, -332, 930, 618))), li, (90, -70, 910, 360), 0.9)


def c_ceng_layer():            # 层
    return _w(0.9, lambda: shi_corpse() + yun(into((300, -60, 930, 520))))


def c_she_shoot():             # 射
    return lr(lambda m: shen_body(into((75, -70, 560, 880))), cun, (570, -70, 945, 880), 0.88)


def c_ruo():                   # 若
    return tb(cao, you_right, (80, -70, 920, 580), 0.9)


def c_sui_although():          # 虽
    return tb(lambda m: KOU_(m, 270, 730, 860, 620, foot=30), lambda m: chong_insect(m.into(FULL, (70, -70, 930, 560))),
              (80, -70, 920, 560), 0.9)


def c_mou():                   # 某
    return tb(gan_sweet, lambda m: mu(m, pie_w=V(0.75)), (70, -70, 930, 330), 0.9)


def c_di_enemy():              # 敌
    return lr(lambda m: she(into((40, -70, 560, 880))), pu, (560, -70, 945, 880), 0.88)



# ───────── 第五组的部件 ─────────

def yan_flame(m=ID):
    """炎（谈 的右边）：上下两个火，上面的火压扁、捺收短。"""
    d = ((110, 660), (170, 500))
    return huo_fire(m.into((100, 450, 900, 890)), na_end=(780, 60), dot=d) + \
        huo_fire(m.into((70, -70, 930, 410)), na_end=(780, -40), dot=d)


def quan_dog(m=ID, na_end=(850, -10)):
    """犬（突 的下面、状 的右边）：大 + 右上一点。点离横按绝对距离留（压扁的 突 里也不贴横）。"""
    ye = m.y(530) + 140
    return da(m, na_end=na_end) + [dian((m.x(690), ye + 100), (m.x(780), ye), w=V(1.0) * m.k)]


def kao_breath(m=ID):
    """丂（号 的下面）：横 + 从横里起笔的竖折折钩。"""
    return [H_(m, 56, 944, 760), shuzhezhegou(m.x(260), m.y(760), m.y(400), m.x(780) + han.V / 2, m.y(-50), top="hid")]


def gou_hook(m=ID):
    """勾（构 的右边）：撇、从撇上起笔的横折钩，里面一个厶。"""
    k = 0.8 + 0.2 * m.k
    p0, p1 = m.p((380, 880)), m.p((130, 560))
    x0 = han.on_pie(p0, p1, (0, 0), m.y(740))[0]
    return [pie(p0, p1, w0=V(0.95) * k), hengzhegou(x0, m.x(840) + han.V / 2, m.y(740), m.y(-40), -120 * m.k, 86 * m.k)] + \
        si_(m.into((250, 60, 700, 620)))


def ze_top(m=ID):
    """龶（责 的头）：三横（最下一横最长）+ 中竖。"""
    return [H_(m, 160, 840, 820), S_(m, 500, 890, 560, end="hid"), H_(m, 200, 800, 690), H_(m, 56, 944, 560)]


def di_base(m=ID):
    """氐（底、低 的一部分）：平撇、竖提、横、斜钩、底下一点。"""
    p0, p1 = m.p((760, 880)), m.p((250, 790))
    seg = han.pie_seg(p0, p1)
    X = m.x(520)
    yx = han._bz(seg, han._solve(lambda t: han._bz(seg, t)[0], 0, 1, X))[1]
    return [pie(p0, p1, w0=V(0.9) * (0.8 + 0.2 * m.k)), shuti(m.x(250), m.y(800), m.y(160), m.p((560, 300))),
            H_(m, 250, 930, 520, entry=None), xiegou((X, yx), m.p((860, 0)), end=310, top="hid"),
            D_(m, (440, 130), (530, 30), w=V(1.0))]


def jun_lord(m=ID):
    """君（群 的左边）：尹（横折、短横、长横、穿下来的撇）+ 口。"""
    return [hengzhe(m.x(130), m.x(440) + han.V / 2, m.y(810), m.y(570), end="hid"),
            han.heng(m.x(130), m.x(440), m.y(690), beak=False, right_hid=True), H_(m, 40, 530, 570, beak=0.5),
            P_(m, (320, 880), (60, 170), bend=(-20, -30), w0=V(0.95))] + KOU_(m, 210, 470, 420, 120, foot=30)


def jing_finally(m=ID):
    """竟（境 的右边）：立 + 日 + 儿。"""
    return li_top(m) + KOU_(m, 240, 760, 458, 285, foot=30) + [
        INNER_(m, 240, 760, 372), shupie(m.x(390), m.y(290), m.x(80), m.y(-60), head="hid", w0=V(0.9)),
        SWG_(m, 610, 290, -30, 930, top="hid")]


# ───────── 第五组的字 ─────────

def c_tan_talk():              # 谈
    return lr(yan_left, yan_flame, (340, -70, 945, 880), 0.88)


def c_tu_sudden():             # 突
    return tb(xue_cave, quan_dog, (80, -70, 920, 500), 0.9)


def c_hao_number():            # 号
    return tb(lambda m: KOU_(m, 300, 700, 790, 620, foot=30), kao_breath, (60, -70, 940, 600))


def c_kao_test():              # 考
    p0, p1, bend = (860, 860), (120, 250), (-20, -40)
    x0 = han.on_pie(p0, p1, bend, 360)[0]
    return _w(0.92, lambda: [H_(ID, 160, 620, 700), S_(ID, 380, 880, 520, end="hid"), H_(ID, 56, 944, 520),
                             pie(p0, p1, bend=bend, w0=V(1.0)), han.heng(x0 - 70, 800, 360, beak=0.6),
                             shuzhezhegou(420, 360, 190, 760 + V() / 2, -50, top="hid")])


def c_jin_exhaust():           # 尽
    return _w(0.92, lambda: shi_corpse() + [na((225, 560), (850, 330), (-40, -60), wmax=V(1.1)),
                                           dian((380, 300), (460, 210), w=V(1.0)), dian((410, 125), (500, 30), w=V(1.0))])


def c_yu_language():           # 语
    return lr(yan_left, lambda m: wu_five(m.into((140, 440, 860, 880))) + KOU_(m, 230, 770, 330, 0, foot=30),
              (340, -70, 945, 880), 0.9)


def c_lie():                   # 列
    return lr(dai_left, dao_right, (560, -60, 945, 880))


def c_shi_power():             # 势
    def top(m):
        jm = m.into((380, 440, 930, 900))
        return shou(m.into((70, 420, 930, 900))) + jiu(jm) + [D_(jm, (420, 420), (520, 270), w=V(0.9))]
    return tb(top, li, (90, -70, 910, 380), 0.9)


def c_can_join():              # 参
    p0, p1, bend = (480, 600), (60, 140), (0, -40)
    return _w(0.9, lambda: si_(into((240, 650, 760, 905))) + [
        H_(ID, 56, 944, 560), pie(p0, p1, bend=bend, w0=V(1.0)),
        na(han.on_pie(p0, p1, bend, 480), (760, 380), (20, -30), wmax=V(1.1)),
        pie((700, 330), (450, 190), w0=V(0.85)), pie((780, 220), (400, 50), w0=V(0.9)),
        pie((870, 80), (260, -65), bend=(-20, -20), w0=V(1.0))])


def c_xi_hope():               # 希
    return _w(0.9, lambda: [pie((700, 895), (320, 730), w0=V(0.9)), dian((340, 885), (680, 740), w=V(1.0))]
              + bu_cloth(into((70, -70, 930, 640))))


def c_zhong_crowd():           # 众
    return _w(0.92, lambda: ren(into((190, 430, 810, 890))) + ren_narrow(into((60, -70, 500, 430)))
              + ren(into((440, -70, 915, 430))))


def c_gou_build():             # 构
    return lr(mu_left, gou_hook, (380, -70, 945, 880), 0.9)


def c_zhi_cause():             # 致
    return lr(zhi_left, lambda m: pu(m, na_end=(680, -40)), (560, -70, 945, 880), 0.88)


def c_xing_rise():             # 兴
    return _w(0.92, lambda: [dian((230, 840), (300, 720), w=V(1.0)), dian((470, 880), (520, 770), w=V(1.0)),
                             pie((790, 880), (650, 730), w0=V(0.9)), H_(ID, 56, 944, 560),
                             pie((380, 420), (90, 20), bend=(-20, -20), w0=V(1.0)), dian((620, 420), (870, 60), w=V(1.15))])


def c_ze_duty():               # 责
    return tb(ze_top, bei, (100, -70, 900, 520), 0.9)


def c_zhang_chapter():         # 章
    return _w(0.88, lambda: li_top() + KOU_(ID, 250, 750, 458, 260, foot=30)
              + [INNER_(ID, 250, 750, 359), H_(ID, 56, 944, 140), S_(ID, 500, 260, -70, top="hid", end="needle")])


def c_yin_sound():             # 音
    return tb(li_top, lambda m: KOU_(m, 250, 750, 470, 60, foot=36) + [INNER_(m, 250, 750, 265)], (70, -70, 930, 500), 0.9)


def c_gen_follow():            # 跟
    return lr(zu_left, gen, (420, -70, 945, 880), 0.88)


def c_di_bottom():             # 底
    return _w(0.9, lambda: guang_() + di_base(into((300, -70, 930, 650))))


def c_xing_model():            # 型
    return tb(lambda m: kai(m.into((70, 450, 620, 900))) + dao_right(m.into((650, 440, 930, 900))), tu,
              (100, -70, 900, 380), 0.9)


def c_qun():                   # 群
    return lr(jun_lord, yang, (500, -70, 945, 880), 0.88)


def c_wei_surround():          # 围
    return _w(0.9, lambda: _kou(110, 890, 820, -40) + [
        H_(ID, 300, 700, 680), H_(ID, 260, 740, 560), hengzhegou(260, 740 + V() / 2, 420, 170),
        S_(ID, 500, 730, 70)])


def c_jing_border():           # 境
    return lr(tu_left, jing_finally, (370, -70, 945, 880), 0.88)


def c_hai_harm():              # 害
    def low(m):
        return [H_(m, 160, 840, 780), H_(m, 210, 790, 650), H_(m, 56, 944, 520), S_(m, 500, 880, 390, end="hid")] + \
            KOU_(m, 250, 750, 360, 40, foot=30)
    return tb(mian, low, (90, -70, 910, 580), 0.88)


def c_su():                    # 苏
    return tb(cao, ban, (100, -70, 900, 560), 0.9)



# ───────── 第六组的部件 ─────────

def chi_reject(m=ID):
    """斥（诉 的右边）：斤 + 一点。"""
    return jin_axe(m) + [D_(m, (520, 380), (610, 250), w=V(0.95))]


def nai(m=ID):
    """乃（仍 的右边）：竖撇、横撇落进横折钩的起笔（横折折折钩）。"""
    return [shupie(m.x(250), m.y(840), m.x(50), m.y(-60), head="cut", w0=V(0.95)),
            HP_(m, 250, 700, 790, (420, 600), bend=(-10, 0), w0=V(0.85), entry=None),
            hengzhegou(m.x(390), m.x(830) + han.V / 2, m.y(600), m.y(-50), -120 * m.k, 86 * m.k)]


def gang(m=ID):
    """冈（刚 的左边）：冂 + 㐅。"""
    return [han.shu(m.x(150), m.y(760) + 40, m.y(-60)), HZG_(m, 150, 850, 760, -50),
            P_(m, (650, 640), (310, 170), w0=V(0.9)), D_(m, (330, 620), (635, 245), w=V(1.0))]


def quan_left(m=ID):
    """犭（独 的左边）：短撇、从撇上起笔的弯钩、左边一撇。"""
    k = 0.8 + 0.2 * m.k
    P0, P1 = m.p((360, 880)), m.p((110, 730))
    xg = m.x(250)
    yl, yr = pie_at_x(P0, P1, (0, 0), xg - han.V / 2)[1], pie_at_x(P0, P1, (0, 0), xg + han.V / 2)[1]
    hook = wangou(xg, yl, m.y(-50), bow=6, dx=-80 * m.k, dy=64 * m.k, y0r=yr)
    return [pie(P0, P1, w0=V(0.9) * k), hook,
            pie((_mid_x(hook, m.y(470)), m.y(470)), m.p((60, 150)), w0=V(0.85) * k, head="hid")]


def cang(m=ID):
    """仓（创 的左边）：人字头 + 横折 + 竖弯钩。"""
    k = 0.8 + 0.2 * m.k
    P0, P1, B = m.p((500, 880)), m.p((80, 520)), m.v((-20, -10))
    return [pie(P0, P1, B, w0=V(1.04) * k),
            na(han.on_pie(P0, P1, B, m.y(780)), m.p((860, 580)), m.v((40, -10)), wmax=V(1.1) * k),
            hengzhe(m.x(270) - han.V / 2 - 16, m.x(720) + han.V / 2, m.y(450), m.y(280)),
            SWG_(m, 270, 450, -30, 900, top="hid")]


def yin_left(m=ID):
    """印 的左边：短撇、竖提、中横。"""
    return [P_(m, (360, 885), (130, 790), w0=V(0.85)), shuti(m.x(150), m.y(800), m.y(100), m.p((460, 240))),
            H_(m, 150, 430, 470, entry=None, beak=0.5)]


def zhi_hold_top(m=ID):
    """执（势、热 的头）：扌 + 丸（九 + 一点）。"""
    jm = m.into((380, 440, 930, 900))
    return shou(m.into((70, 420, 930, 900))) + jiu(jm) + [D_(jm, (420, 420), (520, 270), w=V(0.9))]


def qian_all(m=ID, na_end=(870, 480)):
    """佥（险 的右边）：人字头、短横、一点一撇、长横。放进窄的右框时 na_end 往里收。"""
    k = 0.8 + 0.2 * m.k
    P0, P1, B = m.p((500, 880)), m.p((70, 470)), m.v((-20, -10))
    return [pie(P0, P1, B, w0=V(1.04) * k),
            na(han.on_pie(P0, P1, B, m.y(780)), m.p(na_end), m.v((40, -10)), wmax=V(1.1) * k),
            H_(m, 300, 700, 520, beak=0.6), D_(m, (320, 420), (380, 290), w=V(0.9)), P_(m, (700, 420), (620, 290), w0=V(0.85)),
            H_(m, 56, 944, 140)]


def ting_pavilion(m=ID):
    """亭（停 的右边）：亠、口、冖、丁。"""
    return [D_(m, (480, 945), (540, 878)), H_(m, 56, 944, 760)] + KOU_(m, 300, 700, 620, 510, foot=30) + [
        D_(m, (110, 440), (130, 340), w=V(1.0)), hook_down(m.x(130), m.x(890), m.y(390), entry=None),
        H_(m, 230, 770, 230, beak=0.6), SG_(m, 520, 230, -60, top="hid")]


# ───────── 第六组的字 ─────────

def c_mi_secret():             # 密
    # 必、山 直接按扁的位置画：整体压扁时点和卧钩挤成一团，山 的竖折也藏不住
    return _w(0.88, lambda: mian() + [
        dian((450, 630), (525, 570), w=V(1.0)), dian((178, 480), (200, 365), w=V(1.0)),
        han.wogou(300, 530, 470, 265, 770, 300), pie((740, 600), (150, 245), (-40, -60), w0=V(1.0)),
        dian((780, 500), (880, 380), w=V(1.1)),
        shu(500, 210, -40, end="hid"), han.shuzhe(220, 140, -40, 780, right="hid"), shu(780, 150, -65, end="dew")])


def c_di_low():                # 低
    return lr(ren_left, di_base, (330, -70, 945, 880), 0.9)


def c_su_tell():               # 诉
    return lr(yan_left, chi_reject, (340, -70, 945, 880), 0.9)


def c_yuan_wish():             # 愿
    # 原 按扁的位置重新排：整体压扁时 白 顶到横上，小 的钩撞上撇
    return _w(0.88, lambda: [H_(ID, 220, 944, 815, entry=None), shupie(220, 860, 40, 340, head="cut"),
                             pie((600, 815), (540, 715), w0=V(0.8), head="hid")] + KOU_(ID, 400, 780, 720, 520, foot=30) + [
                             INNER_(ID, 400, 780, 620), SG_(ID, 570, 520, 345, top="hid"),
                             pie((440, 470), (210, 350), w0=V(0.95)), dian((700, 450), (865, 350), w=V(1.1))] +
              xin_di(into((60, -70, 940, 260))))


def c_reng():                  # 仍
    return lr(ren_left, nai, (330, -70, 945, 880))


def c_wang_net():              # 网
    return _w(0.92, lambda: [shu(150, 800, -60), hengzhegou(150, 850 + V() / 2, 760, -50),
                             pie((450, 620), (255, 220), w0=V(0.85)), dian((260, 600), (450, 270), w=V(0.9)),
                             pie((725, 620), (535, 220), w0=V(0.85)), dian((545, 600), (695, 285), w=V(0.9))])


def c_re_hot():                # 热
    return tb(zhi_hold_top, lambda m: huo_dots(m.into(FULL, (60, -70, 940, 160))), (60, -70, 940, 250), 0.88)


def c_zuo_sit():               # 坐
    return _w(0.9, lambda: [shu(500, 880, 40, end="hid"),
                            pie((380, 830), (90, 430), w0=V(0.95)), dian((230, 640), (420, 470), w=V(1.0)),
                            pie((780, 830), (610, 450), w0=V(0.95)), dian((670, 640), (880, 470), w=V(1.0)),
                            H_(ID, 150, 850, 320), H_(ID, 56, 944, 40)])


def c_di_emperor():            # 帝
    return _w(0.9, lambda: [dian((460, 910), (540, 830)), H_(ID, 56, 944, 760),
                            dian((295, 668), (340, 590), w=V(0.9)), pie((705, 670), (650, 590), w0=V(0.85)),
                            dian((112, 526), (132, 404), w=V(1.05)), hook_down(132, 890, 470, entry=None),
                            shu(250, 380, 20), hengzhegou(250, 750 + V() / 2, 340, 20),
                            shu(500, 470, -70, top="hid", end="needle")])


def c_gang():                  # 刚
    return lr(lambda m: gang(into((40, -70, 580, 880))), dao_right, (600, -60, 945, 880))


def c_zhuang_shape():          # 状
    return lr(jiang_left, lambda m: quan_dog(m, na_end=(760, -10)), (390, -70, 945, 880), 0.9)


def c_du_alone():              # 独
    return lr(quan_left, lambda m: chong_insect(m.into(FULL, (70, -40, 930, 600))), (390, -70, 945, 880), 0.9)


def c_chuang():                # 创
    return lr(lambda m: cang(into((40, -70, 580, 880))), dao_right, (580, -60, 945, 880))


def c_jiu_long():              # 久
    p0, p1 = (420, 880), (120, 560)
    x0 = han.on_pie(p0, p1, (0, 0), 720)[0]
    P0, P1, B = (760, 720), (100, -50), (60, -40)
    return [pie(p0, p1, w0=V(0.95)), hengpie(x0, 760, 720, (100, -50), (60, -40), w0=V(0.95), entry=None),
            na((555, 415), (850, -40), (-20, -40), wmax=V(1.18), start="tip")]


def c_yin_print():             # 印
    return lr(yin_left, jie, (520, -70, 945, 880))


def c_lan():                   # 兰
    return [dian((300, 890), (375, 778), w=V(1.0)), pie((720, 890), (620, 760), w0=V(0.9)), H_(ID, 160, 840, 640),
            H_(ID, 220, 780, 400, beak=0.7), H_(ID, 56, 944, 130)]


def c_na_take():               # 拿
    # 合、手 都按扁框重新排（整体缩放会把横和口挤到一起）
    P0, P1, B = (500, 890), (70, 615), (-20, -10)
    return _w(0.88, lambda: [pie(P0, P1, B, w0=V(1.04)), na(han.on_pie(P0, P1, B, 805), (880, 610), (40, -10), wmax=V(1.1)),
                             H_(ID, 350, 650, 700, beak=0.6)] + KOU_(ID, 275, 725, 610, 470, foot=30) + [
                             pie((770, 340), (250, 300), w0=V(0.9)), H_(ID, 180, 820, 230), H_(ID, 220, 780, 135),
                             H_(ID, 56, 944, 40), SG_(ID, 500, 322, -60, top="hid")])


def c_ji_urgent():             # 急
    def top(m):
        return dao_top(m.into((70, 600, 930, 900), (70, 560, 930, 900))) + [
            hengzhe(m.x(220), m.x(760) + han.V / 2, m.y(560), m.y(300), end="hid"),
            han.heng(m.x(240), m.x(760), m.y(430), beak=False, right_hid=True), H_(m, 180, 820, 300)]
    return tb(top, lambda m: xin_di(m, mid=((440, 260), (490, 150))), (70, -70, 930, 260), 0.9)


def c_shang_wound():           # 伤
    def r(m):
        p0, p1 = m.p((380, 880)), m.p((140, 620))
        x0 = han.on_pie(p0, p1, (0, 0), m.y(760))[0]
        return [pie(p0, p1, w0=V(0.95) * (0.8 + 0.2 * m.k)), han.heng(x0, m.x(860), m.y(760), entry=None, beak=0.6)] + \
            li(m.into((80, -70, 930, 640)))
    return lr(ren_left, r, (330, -70, 945, 880))


def c_su_plain():              # 素
    # 糸 直接按扁的位置画：整体压扁会让撇折的夹角变尖，外角拖出长刺
    return _w(0.88, lambda: [H_(ID, 160, 840, 830), S_(ID, 500, 890, 585, end="hid"), H_(ID, 200, 800, 710),
                             H_(ID, 56, 944, 585),
                             piezhe((555, 585), (375, 405), (575, 442), w=V(0.75), head="hid"),
                             piezhe((595, 440), (340, 215), (770, 270), w=V(0.85)),
                             dian((680, 385), (772, 278), w=V(1.0)),
                             SG_(ID, 500, 238, -60, top="hid"), pie((310, 85), (105, -60), w0=V(0.9)),
                             dian((690, 105), (860, -50), w=V(1.1))])


def c_ye_night():              # 夜
    p0, p1 = (620, 625), (430, 420)
    x0 = han.on_pie(p0, p1, (0, 0), 525)[0]
    return _w(0.9, lambda: [dian((475, 935), (540, 855)), H_(ID, 56, 944, 720),
                            pie((360, 690), (90, 300), w0=V(0.95)), shu(250, 480, -70),
                            pie(p0, p1, w0=V(0.9)), hengpie(x0, 820, 525, (360, 40), (60, -40), w0=V(0.9), entry=None),
                            dian((560, 410), (640, 320), w=V(0.9)),
                            na((540, 320), (880, -40), (-30, -40), wmax=V(1.1), start="tip")])


def c_sheng_save():            # 省
    # 少 按扁的位置重新排，长撇从 目 的左上方扫过去
    return _w(0.9, lambda: [shu(515, 890, 600), pie((380, 790), (110, 600), w0=V(0.95)),
                            dian((620, 840), (820, 725), w=V(1.1)), pie((840, 580), (60, 420), (-60, -80), w0=V(1.05))] +
              mu_box(into((250, -70, 750, 380))))


def c_wei_guard():             # 卫
    return [shu(230, 800, 160, end="hid"), hengzhegou(230, 780 + V() / 2, 760, 300, -80, 64), H_(ID, 56, 944, 140)]


def c_xian_danger():           # 险
    return lr(fu_left, lambda m: qian_all(m, na_end=(790, 500)), (400, -70, 945, 880), 0.9)


def c_lu_land():               # 陆
    return lr(fu_left, ji_strike, (400, -70, 945, 880), 0.9)


def c_xi_practice():           # 习
    return [hengzhegou(120, 820 + V() / 2, 760, -50), dian((260, 560), (400, 450), w=V(1.0)),
            ti((180, 160), (700, 420), w0=V(1.0))]


def c_huan_ring():             # 环
    return lr(wang_left, bu, (360, -70, 945, 880), 0.9, lsx=0.9)


def c_ting_stop():             # 停
    return lr(ren_left, ting_pavilion, (330, -70, 945, 880), 0.88)


def c_fan():                   # 范
    def low(m):
        return shui(m.into((70, -70, 930, 880), (40, -70, 900, 880))) + [
            hengzhe(m.x(420) - han.V / 2 - 16, m.x(820) + han.V / 2, m.y(760), m.y(520)),
            SWG_(m, 420, 760, -30, 930, top="hid")]
    return tb(cao, low, (90, -70, 910, 560), 0.9)


GLYPHS = {
    "斯": c_si_this, "尔": c_er_you, "亚": c_ya, "企": c_qi_enterprise, "阿": c_a, "李": c_li_plum, "标": c_biao_mark,
    "专": c_zhuan_special, "周": c_zhou_week, "较": c_jiao_compare, "注": c_zhu_pour, "仅": c_jin_only,
    "青": c_qing_blue, "选": c_xuan_choose, "响": c_xiang_sound, "推": c_tui_push, "房": c_fang_house,
    "节": c_jie_section, "投": c_tou_throw, "案": c_an_case, "维": c_wei_tie, "划": c_hua_draw, "陈": c_chen,
    "律": c_lv_law, "护": c_hu_protect,
    "态": c_tai_attitude, "孩": c_hai_child, "星": c_xing_star, "志": c_zhi_will, "站": c_zhan_stand, "巴": c_ba_hope,
    "例": c_li_example, "防": c_fang_defend, "供": c_gong_provide, "效": c_xiao_effect, "讲": c_jiang_speak,
    "料": c_liao, "终": c_zhong_end, "答": c_da_answer, "绝": c_jue_cut, "奇": c_qi_strange, "依": c_yi_rely,
    "批": c_pi_criticize, "项": c_xiang_item, "故": c_gu_reason, "按": c_an_press, "米": c_mi_rice, "客": c_ke_guest,
    "纪": c_ji_record, "攻": c_gong_attack,
    "细": c_xi_thin, "值": c_zhi_value, "男": c_nan_male, "破": c_po_break, "助": c_zhu_help, "倒": c_dao_fall,
    "限": c_xian_limit, "职": c_zhi_job, "速": c_su_fast, "刻": c_ke_carve, "否": c_fou, "毛": c_mao_hair,
    "球": c_qiu_ball, "怕": c_pa_fear, "弹": c_dan_bullet, "校": c_xiao_school, "试": c_shi_try, "股": c_gu_stock,
    "谁": c_shui_who, "哪": c_na_which, "尼": c_ni_nun, "送": c_song_send, "适": c_shi_fit, "波": c_bo_wave,
    "初": c_chu_begin,
    "待": c_dai_wait, "云": c_yun_cloud, "冷": c_leng, "冲": c_chong_rush, "斗": c_dou, "京": c_jing_capital,
    "母": c_mu_mother, "止": c_zhi_stop, "足": c_zu_foot, "半": c_ban_half, "父": c_fu_father, "曾": c_ceng,
    "居": c_ju_reside, "充": c_chong_fill, "财": c_cai_wealth, "欢": c_huan_joy, "负": c_fu_bear, "述": c_shu_narrate,
    "劳": c_lao_labor, "层": c_ceng_layer, "射": c_she_shoot, "若": c_ruo, "虽": c_sui_although, "某": c_mou,
    "敌": c_di_enemy,
    "谈": c_tan_talk, "突": c_tu_sudden, "号": c_hao_number, "考": c_kao_test, "尽": c_jin_exhaust, "语": c_yu_language,
    "列": c_lie, "势": c_shi_power, "参": c_can_join, "希": c_xi_hope, "众": c_zhong_crowd, "构": c_gou_build,
    "致": c_zhi_cause, "兴": c_xing_rise, "责": c_ze_duty, "章": c_zhang_chapter, "音": c_yin_sound, "跟": c_gen_follow,
    "底": c_di_bottom, "型": c_xing_model, "群": c_qun, "围": c_wei_surround, "境": c_jing_border, "害": c_hai_harm,
    "苏": c_su,
    "密": c_mi_secret, "低": c_di_low, "诉": c_su_tell, "愿": c_yuan_wish, "仍": c_reng, "网": c_wang_net, "热": c_re_hot,
    "坐": c_zuo_sit, "帝": c_di_emperor, "刚": c_gang, "状": c_zhuang_shape, "独": c_du_alone, "创": c_chuang,
    "久": c_jiu_long, "印": c_yin_print, "兰": c_lan, "拿": c_na_take, "急": c_ji_urgent, "伤": c_shang_wound,
    "素": c_su_plain, "夜": c_ye_night, "省": c_sheng_save, "卫": c_wei_guard, "险": c_xian_danger, "陆": c_lu_land,
    "习": c_xi_practice, "环": c_huan_ring, "停": c_ting_stop, "范": c_fan,
}
