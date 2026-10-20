"""渡言的常用字（第一批）：用 parts.py 的部件按框架摆放拼成。

左右结构：左偏旁按它画好的位置放，右边的部件从整字框压进右边的框；上下结构同理。
笔画越多的字整体越细一点（weight），压窄的部件才不会显得太黑。
"""
import han
import layout
from han import dian, heng, hengpie, hengpie_wangou, hengzhegou, pie, shu, weight
from parts import (ID, H_, HP_, HZG_, N_, INNER_, KOU_, P_, S_, SG_, SWG_, D_, HZ_, into, ben, bi, cao, cun, da, er, fu_left,
                   gan, gong, gu, he_left, hua, ke, kou, li, men, mian, mu, mu_box, mu_left, nv_left, piezhe, qu,
                   ren, ren_left, ren_top, ri, ri_left, she, shou, shui, shi_, si_left, sheng, tian_, tu, wang,
                   wang_lost, wen, xin, xin_left, yan, yan_left, ye, you, you_left, yuan, yue, yue_left, zao, zi_,
                   zou)


def _w(k, fn):
    """在 weight(k) 里画：fn 是不带参数的函数。"""
    with weight(k):
        return fn()


# ───────── 小部件（只在这里用到）─────────

def shang(m=ID):
    """上"""
    return [S_(m, 430, 830, 90, top="head", end="hid"), H_(m, 430, 760, 470, entry=None, beak=0.7), H_(m, 56, 944, 90)]


def ding(m=ID):
    """丁"""
    return [H_(m, 56, 944, 740), SG_(m, 600, 740, -50)]


def ji(m=ID):
    """己：横折的竖落到中间那一横的底边；中间一横的右端藏进那一竖，左端露出来，竖弯钩从它下面出发。"""
    return [han.hengzhe_heng(m.x(200), m.x(748) + han.V / 2, m.y(760), m.y(470), m.x(222) - han.V / 2 - 22),
            SWG_(m, 222, 470, -30, 900, top="hid")]


def jin_top(m=ID):
    """今（也做念的上半）"""
    return ren_top(m) + [D_(m, (480, 620), (540, 528), w=han.V * 1.0),
                         HP_(m, 270, 720, 360, (470, -60), bend=(-10, -10))]


# ───────── 单字 ─────────

def c_er():                    # 二
    return [heng(220, 780, 650), heng(56, 944, 110)]


def c_san():                   # 三
    return [heng(180, 820, 740), heng(232, 768, 430, beak=0.8), heng(56, 944, 80)]


def c_shang():                 # 上
    return shang()


def c_xia():                   # 下
    return [heng(56, 944, 760), shu(470, 760, -70, top="hid", end="dew"), dian((500, 590), (650, 410))]


def c_bu():                    # 不
    return [heng(62, 938, 760), pie((560, 760), (90, 250), bend=(-30, -10), head="hid"),
            shu(530, 600, -70, top="head", end="dew"), dian((620, 520), (830, 330))]


def c_xiao():                  # 小
    return [han.shugou(500, 880, -40, dx=-130, dy=90), pie((338, 600), (104, 250), w0=han.V * .96, bend=(-10, 0)),
            dian((650, 600), (880, 336))]


def c_shan():                  # 山
    return [shu(500, 860, 110, end="hid"), han.shuzhe(170, 610, 110, 830, right="hid"), shu(830, 640, 40, end="dew")]


def c_le():                    # 了
    return [hengpie_wangou(124, 850, 770, (450, 560), 520, -50)]


def c_fang():                  # 方
    return [dian((470, 912), (546, 806)), heng(56, 944, 660), hengzhegou(330, 812, 450, -40),
            pie((390, 666), (80, -60), bend=(-20, -10), head="hid")]


def c_chu():                   # 出
    return [han.shuzhe(220, 760, 440, 780, right="hid"), shu(780, 780, 410, end="dew"),
            shu(500, 880, 40, top="head", end="hid"),
            han.shuzhe(160, 380, 40, 840, right="hid"), shu(840, 400, -40, end="dew")]


def c_zi_self():               # 自
    return [pie((546, 900), (436, 770), w0=han.V * 0.84)] + KOU_(ID, 270, 730, 770, -40) + \
        [INNER_(ID, 270, 730, 520), INNER_(ID, 270, 730, 260)]


def c_zhu():                   # 主
    return [dian((450, 900), (540, 800))] + wang(into((70, -70, 930, 770)))


def c_nv():                    # 女
    return [han.piedian((450, 880), (240, 420), (800, -30)), pie((700, 610), (120, -50), bend=(-40, -20), w0=han.V * 1.02),
            heng(56, 944, 500)]


def c_jin():                   # 今
    return jin_top()


def c_ge():                    # 个
    return ren_top() + [shu(500, 620, -70, top="head", end="dew")]


def c_he_close():              # 合
    return ren_top() + [heng(316, 668, 470, beak=0.6)] + KOU_(ID, 270, 730, 310, -30)


def c_quan():                  # 全
    return ren_top() + wang(into((150, -70, 850, 566)))


def c_hui():                   # 会
    return _w(0.94, lambda: ren_top(into((70, 300, 930, 900))) + [heng(290, 710, 500, beak=0.5), heng(56, 944, 320),
                                         piezhe((440, 296), (226, -22), (660, 44)), dian((646, 200), (836, -20))])


def c_you_friend():            # 友
    return _w(0.95, lambda: [heng(56, 944, 640), pie((440, 870), (70, -60), bend=(-30, -30))]
              + you(into((300, -60, 930, 560))))


def c_zhi():                   # 只
    return KOU_(ID, 260, 740, 830, 420, foot=30) + [pie((390, 290), (130, -50), w0=han.V * 1.0),
                                                     dian((620, 290), (860, -10), w=han.V * 1.2)]


# ───────── 左右结构 ─────────

def _tag(shapes, part):
    for s in shapes:
        s.part = part              # 结构检查用：哪一笔属于哪个部件
    return shapes


_DEFAULT = object()


def lr(left, right, rbox, k=0.92, gap=_DEFAULT, lsx=1.0):
    """左右结构：右边部件放进 rbox。gap 不是 None 时，rbox 的左边沿按两部件间距自动摆（见 layout.py）。
    lsx < 1 时左偏旁以左边沿为准横向收窄（左边太重的字用）。"""
    if gap is _DEFAULT:
        gap = layout.LR_GAP_BY_LEFT.get(left.__name__, layout.LR_GAP)
    with weight(k):
        L = _tag(left(ID if lsx == 1 else into((40, -70, 40 + 300 * lsx, 880), (40, -70, 340, 880))), "左")
        R = right(into(rbox)) if gap is None else layout.fit(L, lambda b: right(into(b)), rbox, "right", gap)[0]
        return L + _tag(R, "右")


def c_ta():                    # 他
    return lr(ren_left, ye, (330, -40, 945, 820))


def c_men():                   # 们
    return lr(ren_left, men, (330, -60, 945, 880))


def c_ni():                    # 你
    return lr(ren_left, er, (320, -60, 945, 880), 0.9)


def c_xin_trust():             # 信
    return lr(ren_left, yan, (310, -50, 945, 890), 0.88)


def c_shen_what():             # 什
    return lr(ren_left, shi_, (330, -70, 945, 870))


def c_ti():                    # 体
    return lr(ren_left, ben, (310, -70, 905, 880), 0.9)


def c_jiang():                 # 江
    return lr(shui, gong, (340, 20, 930, 800))


def c_han():                   # 汉
    return lr(shui, you, (320, -40, 945, 800))


def c_he_river():              # 河
    return lr(shui, ke, (310, -50, 945, 820), 0.9)


def c_fa():                    # 法
    return lr(shui, qu, (310, -50, 945, 870), 0.9)


def c_huo():                   # 活
    return lr(shui, she, (310, -50, 945, 880), 0.9)


def c_he_and():                # 和
    with weight(0.92):
        return he_left(ID) + KOU_(ID, 560, 860, 600, 150, foot=30)


def c_hao():                   # 好
    return lr(nv_left, zi_, (370, -60, 945, 840))


def c_ta_she():                # 她
    return lr(nv_left, ye, (370, -40, 945, 820))


def c_ru():                    # 如
    with weight(0.92):
        return nv_left(ID) + KOU_(ID, 520, 860, 610, 160, foot=30)


def c_ming():                  # 明
    return lr(ri_left, yue, (370, -60, 940, 860))


def c_shi_time():              # 时
    return lr(ri_left, cun, (370, -60, 945, 880))


def c_lin():                   # 林
    return lr(mu_left, mu, (370, -70, 905, 880), 0.9)


def c_cun():                   # 村
    return lr(mu_left, cun, (370, -60, 945, 880))


def c_xiang():                 # 相
    return lr(mu_left, mu_box, (420, -50, 940, 860), 0.9)


def c_peng():                  # 朋
    return lr(yue_left, yue, (390, -60, 940, 860), 0.9)


def c_hong():                  # 红
    return lr(si_left, gong, (370, 20, 930, 790))


def c_yang():                  # 阳
    return lr(fu_left, ri, (400, 20, 930, 820))


def c_dui_team():              # 队
    return lr(fu_left, ren, (380, -70, 935, 860))


def c_da_hit():                # 打
    return lr(shou, ding, (360, -50, 945, 860))


def c_ren_know():              # 认
    return lr(yan_left, ren, (340, -60, 928, 840))


def c_rang():                  # 让
    return lr(yan_left, shang, (360, -40, 940, 860))


def c_ji_count():              # 计
    return lr(yan_left, shi_, (340, -70, 945, 870))


def c_ji_record():             # 记
    return lr(yan_left, ji, (370, -40, 930, 800))


def c_mang():                  # 忙
    return lr(xin_left, wang_lost, (340, -60, 945, 880))


def c_xing():                  # 性
    return lr(xin_left, sheng, (330, -70, 945, 880), 0.9)


def c_dui():                   # 对
    return lr(you_left, cun, (370, -60, 945, 880))


def c_shuang():                # 双
    return lr(you_left, you, (390, -60, 926, 800))


# ───────── 上下、半包围 ─────────

def bao(outer, inner, box, k=0.92):
    """半包围（辶）：里面的部件放进 box，位置手摆。"""
    with weight(k):
        return _tag(outer(ID), "外") + _tag(inner(into(box)), "内")


def tb(top, bottom, bbox, k=0.92, tbox=None, gap=layout.TB_GAP):
    """上下结构：下面部件放进 bbox。gap 不是 None 时，bbox 的上边沿按两部件间距自动摆。"""
    with weight(k):
        T = _tag(top(ID if tbox is None else into(tbox)), "上")
        B = bottom(into(bbox)) if gap is None else layout.fit(T, lambda b: bottom(into(b)), bbox, "bottom", gap)[0]
        return T + _tag(B, "下")


def c_an():                    # 安
    return tb(mian, lambda m: c_nv_m(m), (100, -60, 900, 560))


def c_nv_m(m):
    return [han.piedian(m.p((450, 880)), m.p((240, 420)), m.p((800, -30))),
            P_(m, (700, 610), (120, -50), bend=(-40, -20), w0=han.V * 1.02), H_(m, 56, 944, 500)]


def c_wan():                   # 完
    return tb(mian, yuan, (120, -60, 900, 560))


def c_ta_it():                 # 它
    return tb(mian, bi, (150, -50, 900, 580))


def c_shou_keep():             # 守
    return tb(mian, cun, (110, -60, 900, 580))


def c_hua():                   # 花
    return tb(cao, hua, (110, -70, 900, 580), 0.9)


def c_cao():                   # 草
    return tb(cao, zao, (130, -70, 870, 600), 0.9)


def c_ku():                    # 苦
    return tb(cao, gu, (150, -50, 850, 600), 0.92)


def c_si():                    # 思
    return tb(tian_, xin, (56, -70, 944, 360), 0.9, tbox=(160, 400, 840, 880))


def c_xiang_think():           # 想
    def top(m):
        return mu_left(into((90, 400, 420, 880), (40, -70, 340, 872))) + mu_box(into((460, 420, 900, 870)))
    return tb(top, xin, (56, -70, 944, 350), 0.86)


def c_nian():                  # 念
    return tb(jin_top, xin, (80, -70, 920, 310), 0.9, tbox=(80, 330, 920, 905))


def c_wang_forget():           # 忘
    return tb(wang_lost, xin, (80, -70, 920, 330), 0.9, tbox=(90, 380, 910, 900))


def c_zhe():                   # 这
    return bao(zou, wen, (348, 210, 906, 930))


def c_guo():                   # 过
    return bao(zou, cun, (340, 150, 920, 880))


def c_da_reach():              # 达
    return bao(zou, da, (320, 220, 918, 890))


def c_bian():                  # 边
    return bao(zou, li, (340, 210, 920, 890))


def c_yuan_far():              # 远
    return bao(zou, yuan, (320, 210, 930, 870))


def c_ke():                    # 克：十、口、儿
    return [heng(64, 936, 772), shu(500, 880, 620, top="head", end="hid")] + han._kou(250, 750, 620, 420) + [
        han.shupie(424, 420, 100, -60, head="hid"),
        han.shuwangou(628, 420, 14, 936, top="hid")]


def c_xie():                   # 写：冖 + 与
    return [dian((112, 812), (134, 690), w=han.V * 1.05), han.hook_down(134, 884, 760, entry=None),
            heng(258, 724, 556, beak=0.7),
            han.shuzhezhegou(322, 556, 380, 774, -50, top="hid"),
            heng(62, 938, 206)]


def bai_left(m=ID):
    """白（左偏旁，的）"""
    return [P_(m, (230, 886), (166, 784), w0=han.V * 0.86)] + KOU_(m, 110, 320, 700, 40) + [INNER_(m, 110, 320, 372)]


def shao(m=ID):
    """勺（的 的右边）"""
    return [P_(m, (360, 880), (110, 540), w0=han.V * 1.0),
            HZG_(m, 230, 800, 712, -50),
            D_(m, (360, 470), (500, 320), w=han.V * 1.1)]


def c_de():                    # 的
    return lr(bai_left, shao, (400, -60, 940, 880))


def c_lai():                   # 来
    return [heng(170, 830, 782), D_(ID, (304, 704), (346, 614), w=han.V * 1.0), P_(ID, (708, 688), (648, 604), w0=han.V * 0.9),
            heng(56, 944, 470), shu(500, 880, -70, top="head", end="dew"),
            P_(ID, (480, 470), (80, 30), bend=(-20, -10), head="hid"),
            N_(ID, (520, 460), (850, 30), bend=(20, -10), wmax=han.V * 1.1)]


def zhu_top(m=ID):
    """⺮（竹字头）：左右两组，每组一撇、一横、一点。"""
    out = []
    for dx in (0, 440):
        out += [P_(m, (250 + dx, 884), (96 + dx, 700), w0=han.V * 0.9),
                H_(m, 196 + dx, 462 + dx, 792, entry=None, beak=0.6),
                D_(m, (272 + dx, 730), (318 + dx, 636), w=han.V * 0.9)]
    return out


def mao(m=ID):
    """毛"""
    return [P_(m, (800, 870), (230, 760), w0=han.V * 0.9),
            H_(m, 200, 800, 600, beak=0.6), H_(m, 110, 890, 360),
            SWG_(m, 500, 812, -40, 930, top="hid")]


def c_bi():                    # 笔
    return tb(zhu_top, mao, (70, -70, 930, 590), 0.9)


def dong(m=ID):
    """东"""
    return [H_(m, 110, 890, 760),
            han.piezhe(m.p((470, 862)), m.p((196, 500)), m.p((850, 500)), w=han.V * 0.86, end="flat"),
            SG_(m, 530, 880, -50),
            P_(m, (400, 350), (150, 110), w0=han.V * 0.9),
            D_(m, (690, 330), (846, 150), w=han.V * 1.0)]


def c_lian():                  # 练
    return lr(si_left, dong, (380, -60, 945, 880))


GLYPHS = {
    "二": c_er, "三": c_san, "上": c_shang, "下": c_xia, "不": c_bu, "小": c_xiao, "山": c_shan, "了": c_le,
    "力": lambda: li(), "也": lambda: ye(), "子": lambda: zi_(), "心": lambda: xin(), "月": lambda: yue(),
    "目": lambda: mu_box(), "王": lambda: wang(), "工": lambda: gong(), "土": lambda: tu(), "门": lambda: men(),
    "又": lambda: you(), "寸": lambda: cun(), "生": lambda: sheng(), "干": lambda: gan(), "本": lambda: ben(),
    "古": lambda: gu(), "木": lambda: mu(), "女": c_nv, "方": c_fang, "出": c_chu, "自": c_zi_self, "主": c_zhu,
    "今": c_jin, "个": c_ge, "合": c_he_close, "全": c_quan, "会": c_hui, "友": c_you_friend, "只": c_zhi,
    "他": c_ta, "们": c_men, "你": c_ni, "信": c_xin_trust, "什": c_shen_what, "体": c_ti,
    "江": c_jiang, "汉": c_han, "河": c_he_river, "法": c_fa, "活": c_huo, "和": c_he_and,
    "好": c_hao, "她": c_ta_she, "如": c_ru, "明": c_ming, "时": c_shi_time, "林": c_lin, "村": c_cun,
    "相": c_xiang, "朋": c_peng, "红": c_hong, "阳": c_yang, "队": c_dui_team, "打": c_da_hit,
    "认": c_ren_know, "让": c_rang, "计": c_ji_count, "记": c_ji_record, "忙": c_mang, "性": c_xing,
    "对": c_dui, "双": c_shuang,
    "安": c_an, "完": c_wan, "它": c_ta_it, "守": c_shou_keep, "花": c_hua, "草": c_cao, "苦": c_ku,
    "思": c_si, "想": c_xiang_think, "念": c_nian, "忘": c_wang_forget,
    "这": c_zhe, "过": c_guo, "达": c_da_reach, "边": c_bian, "远": c_yuan_far,
    "克": c_ke, "写": c_xie, "的": c_de, "来": c_lai, "笔": c_bi, "练": c_lian,
}
