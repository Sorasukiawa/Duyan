"""字距：几组常见的难排字对。数值单位是 1/1000 em，负数是拉近。

先按「形状组」写，再展开成字对；只收录字体里已经有的字。
"""

ROUND_LC = "aceodgq"          # 左边是圆的小写
DIAG_LC = "vwy"               # 斜笔小写
PERIODS = ".,"


def pairs():
    p = {}

    def add(lefts, rights, v):
        for a in lefts:
            for b in rights:
                p[(a, b)] = p.get((a, b), 0) + v

    # 大写斜笔、T 和 A、L 互相靠近
    add("A", "VW", -64); add("A", "Y", -58); add("A", "T", -46); add("A", "U", -20); add("A", "CGOQ", -18)
    add("VW", "A", -64); add("Y", "A", -58); add("T", "A", -46)
    add("L", "T", -78); add("L", "VW", -64); add("L", "Y", -70); add("L", "’”'\"", -90)
    add("FP", "A", -44); add("CGOQD", "A", -18); add("CGOQD", "VWY", -18); add("VWY", "CGOQ", -18)
    # 大写配小写
    add("T", ROUND_LC + "su", -66); add("T", "rwyv", -54); add("T", "i", -20)
    add("V", ROUND_LC, -52); add("W", ROUND_LC, -40); add("Y", ROUND_LC, -66)
    add("VWY", "u", -34); add("VWY", "rs", -34)
    add("P", ROUND_LC, -16); add("F", ROUND_LC, -24)
    # 句点、逗号
    add("TVWYPF", PERIODS, -82); add("r", PERIODS, -44); add(DIAG_LC, PERIODS, -44)
    add(PERIODS, "TVWY", -70); add(PERIODS, "’”", -70)
    # 小写之间
    add(DIAG_LC, "aceodgq", -14); add("aceobpq", DIAG_LC, -12); add("r", "aceodgq", -10)
    add("f", "’”'\"?!)", 46); add("f", "aceodgq", -10)
    # 引号
    add("‘“", "A", -54); add("A", "’”", -54); add("‘“", ROUND_LC, -24)
    return p
