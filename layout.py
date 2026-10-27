"""汉字的结构规范（说明见 docs/STRUCTURE.md）。数字都是 1/1000 em，字身是 x 0–1000、y −120–880。

除了检查用的范围，这里还有「按间距摆部件」的工具：左右、上下结构的字不再手写右边 / 下面部件的框边，
而是量两个部件真实轮廓之间最近的距离，把框边挪到正好留出规定的间距，所有字的部件间距就统一了。
"""
import numpy as np
from PIL import Image, ImageDraw

# ── 字面 ──
# 字在设计坐标里画（长横 56–944，字面大约 y −67–896，偏高）；出字体时 glyphs.collect 把整字纵向压到 HAN_SY，
# 设计坐标里的 HAN_CY 对到字身中心 EM_CY。横画在 han.drawing() 里先按 1/HAN_SY 加粗，压完正好是 60。
# 2026-10-21 定：压完典型字面 −67–827、高约 896，和常见中文字体（字面约占字身九成）一致，所有字都在字面框里。
HAN_SY = 0.93
HAN_CY = 415
EM_CY = 380
FACE = (30, -100, 975, 880)        # 字面框（出字体后）：墨不能出这个框（捺脚、撇尖算在内）


def han_y(y):
    """设计坐标的 y 出字体后在哪。"""
    return EM_CY + (y - HAN_CY) * HAN_SY


# ── 拼字（设计坐标）──
LR_GAP = 92                        # 左右结构：两个部件之间的距离
TB_GAP = 76                        # 上下结构：两个部件之间的距离（出字体后约 71）
LR_GAP_BY_LEFT = {"fu_left": 60, "xin_left": 76}   # 偏旁靠右的一侧是细弧、点，按轮廓量会显得松

# ── 检查（出字体后的坐标；纵向的数是原来设计坐标里的范围压过来的）──
LR_GAP_RANGE = (55, 125)           # 检查时允许的范围（个别字手调过框时用）
TB_GAP_RANGE = (46, 116)           # 设计坐标里 50–125
BAO_GAP_RANGE = (46, 140)          # 半包围（辶）：里面的部件和外框之间（斜着量，下限按纵向压过来算）
LR_CENTER_X = (390, 580)           # 左右结构的重心横坐标（宋体里 队、忙 这种左重的字也在 0.42 左右）
TB_CENTER_Y = (301, 441)           # 上下结构的重心纵坐标（设计坐标里 330–480）

# ── 减细档位：按整字的轮廓条数（docs/RULES.md「粗细」）──
WEIGHT_TIERS = ((5, 1.0), (6, 0.92), (9, 0.9))     # 轮廓条数不超过多少 → 档位；再多是 0.88
WEIGHT_MANY = 0.88
WEIGHT_COMPOSED = 0.92             # lr()、tb()、bao() 拼的字部件压进了窄格，最少也减到这一档
WEIGHT_EXCEPT = {}                 # 破例的字，写明理由


def weight_for(n, composed):
    """n 条轮廓的字该用的减细档位。"""
    k = next((k for most, k in WEIGHT_TIERS if n <= most), WEIGHT_MANY)
    return min(k, WEIGHT_COMPOSED) if composed else k

CENTER_EXCEPT = {                  # 量出来超标、但目测平衡的字，写明理由
    "队": "左边一整条竖加耳刀，右边只有一撇一捺，按面积算的重心一定偏左（宋体约 415，这里约 370）",
    "罗": "罒 是一个实心的扁框，夕 的墨又集中在上半（撇头、横撇的横），按面积算的重心一定偏高（约 490）；"
          "罒 再收小，框里的格子就成了几个小点",
}

# ── 量距离 ──
_PX = 4
_TOP = 880


def _raster(shapes):
    n = 1000 // _PX
    im = Image.new("L", (n, n), 0)
    d = ImageDraw.Draw(im)
    for hole in (False, True):
        for s in shapes:
            if s.hole == hole:
                d.polygon([(x / _PX, (_TOP - y) / _PX) for x, y in s.flatten(6)], fill=0 if hole else 255)
    return np.asarray(im) > 127


def _edge_points(ink, side):
    """墨朝向另一个部件的那一圈边：side 是 right / left / bottom / top。返回 [(x, y)]（像素）。"""
    pts = []
    if side in ("right", "left"):
        for r in range(ink.shape[0]):
            cols = np.nonzero(ink[r])[0]
            if len(cols):
                pts.append((cols.max() + 1 if side == "right" else cols.min(), r + 0.5))
    else:
        for c in range(ink.shape[1]):
            rows = np.nonzero(ink[:, c])[0]
            if len(rows):
                pts.append((c + 0.5, rows.max() + 1 if side == "bottom" else rows.min()))
    return np.array(pts, dtype=float)


def _outline_points(ink):
    """墨的一圈边上的像素。"""
    inner = ink.copy()
    inner[1:-1, 1:-1] = ink[1:-1, 1:-1] & ink[:-2, 1:-1] & ink[2:, 1:-1] & ink[1:-1, :-2] & ink[1:-1, 2:]
    r, c = np.nonzero(ink & ~inner)
    return np.stack([c + 0.5, r + 0.5], 1).astype(float)


def gap(a, b, side):
    """部件 a 和部件 b 之间最近的距离（单位）。side：b 在 a 的 right（右边）、bottom（下面），或 any（半包围）。"""
    ia, ib = _raster(a), _raster(b)
    if (ia & ib).any():
        return 0.0
    if side == "any":
        pa, pb = _outline_points(ia), _outline_points(ib)
        return min(float(np.sqrt(((pa[i:i + 400, None, :] - pb[None, :, :]) ** 2).sum(2)).min())
                   for i in range(0, len(pa), 400)) * _PX
    pa = _edge_points(ia, side)
    pb = _edge_points(ib, {"right": "left", "bottom": "top"}[side])
    d = np.sqrt(((pa[:, None, :] - pb[None, :, :]) ** 2).sum(2))
    return float(d.min()) * _PX


def fit(fixed, make, box, side, target):
    """挪动 box 靠近 fixed 的那条边（右边部件挪左边沿，下面部件挪上边沿），让两部件间距等于 target。
    make(box) 画出放进 box 的部件。返回 (部件, 用上的 box)。"""
    i = 0 if side == "right" else 3
    lo, hi = box[i] - 260, box[i] + 260
    best = None
    for _ in range(14):
        mid = (lo + hi) / 2
        b = list(box)
        b[i] = mid
        shapes = make(tuple(b))
        g = gap(fixed, shapes, side)
        best = (shapes, tuple(b))
        # 右边部件：左边沿往右挪，间距变大；下面部件：上边沿往下挪，间距变大
        grows = (g < target)
        if side == "right":
            lo, hi = (mid, hi) if grows else (lo, mid)
        else:
            lo, hi = (lo, mid) if grows else (mid, hi)
        if abs(g - target) < 2:
            break
    return best
