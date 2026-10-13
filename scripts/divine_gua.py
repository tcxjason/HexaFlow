#!/usr/bin/env python3
"""由本卦与变爻位置推导之卦、变爻爻题与朱熹解卦引用范围。

仅依赖 Python 标准库，无网络与文件写入行为。

用法：
    python divine_gua.py --gua 噬嗑 --changing 六二
    python divine_gua.py --gua 艮 --changing 6
    python divine_gua.py --gua 谦 --changing 2,4
    python divine_gua.py --gua 52            # 无变爻（静卦）
"""
import argparse
import re
import sys

# 八卦爻画，自下而上（初、中、上）
TRI = {
    "乾": (1, 1, 1), "兑": (1, 1, 0), "离": (1, 0, 1), "震": (1, 0, 0),
    "巽": (0, 1, 1), "坎": (0, 1, 0), "艮": (0, 0, 1), "坤": (0, 0, 0),
}

# 卦象（自然物）-> 八卦
SYMBOL = {"乾": "天", "兑": "泽", "离": "火", "震": "雷",
          "巽": "风", "坎": "水", "艮": "山", "坤": "地"}

# (序号, 卦名, 上卦, 下卦)
GUA = [
    (1, "乾", "乾", "乾"), (2, "坤", "坤", "坤"), (3, "屯", "坎", "震"),
    (4, "蒙", "艮", "坎"), (5, "需", "坎", "乾"), (6, "讼", "乾", "坎"),
    (7, "师", "坤", "坎"), (8, "比", "坎", "坤"), (9, "小畜", "巽", "乾"),
    (10, "履", "乾", "兑"), (11, "泰", "坤", "乾"), (12, "否", "乾", "坤"),
    (13, "同人", "乾", "离"), (14, "大有", "离", "乾"), (15, "谦", "坤", "艮"),
    (16, "豫", "震", "坤"), (17, "随", "兑", "震"), (18, "蛊", "艮", "巽"),
    (19, "临", "坤", "兑"), (20, "观", "巽", "坤"), (21, "噬嗑", "离", "震"),
    (22, "贲", "艮", "离"), (23, "剥", "艮", "坤"), (24, "复", "坤", "震"),
    (25, "无妄", "乾", "震"), (26, "大畜", "艮", "乾"), (27, "颐", "艮", "震"),
    (28, "大过", "兑", "巽"), (29, "坎", "坎", "坎"), (30, "离", "离", "离"),
    (31, "咸", "兑", "艮"), (32, "恒", "震", "巽"), (33, "遁", "乾", "艮"),
    (34, "大壮", "震", "乾"), (35, "晋", "离", "坤"), (36, "明夷", "坤", "离"),
    (37, "家人", "巽", "离"), (38, "睽", "离", "兑"), (39, "蹇", "坎", "艮"),
    (40, "解", "震", "坎"), (41, "损", "艮", "兑"), (42, "益", "巽", "震"),
    (43, "夬", "兑", "乾"), (44, "姤", "乾", "巽"), (45, "萃", "兑", "坤"),
    (46, "升", "坤", "巽"), (47, "困", "兑", "坎"), (48, "井", "坎", "巽"),
    (49, "革", "兑", "离"), (50, "鼎", "离", "巽"), (51, "震", "震", "震"),
    (52, "艮", "艮", "艮"), (53, "渐", "巽", "艮"), (54, "归妹", "震", "兑"),
    (55, "丰", "震", "离"), (56, "旅", "离", "艮"), (57, "巽", "巽", "巽"),
    (58, "兑", "兑", "兑"), (59, "涣", "巽", "坎"), (60, "节", "坎", "兑"),
    (61, "中孚", "巽", "兑"), (62, "小过", "震", "艮"), (63, "既济", "坎", "离"),
    (64, "未济", "离", "坎"),
]

# 八纯卦（输出「X为Y」式全称）
PURE = {"乾", "坤", "坎", "离", "震", "艮", "巽", "兑"}

BY_NAME = {}
BY_PATTERN = {}
for _no, _name, _up, _down in GUA:
    _pat = TRI[_down] + TRI[_up]          # 六爻自下而上
    _rec = {"no": _no, "name": _name, "up": _up, "down": _down, "pattern": _pat}
    BY_NAME[_name] = _rec
    BY_PATTERN[_pat] = _rec

POS_NAME = {1: "初", 2: "二", 3: "三", 4: "四", 5: "五", 6: "上"}

RULES = {
    0: "六爻皆不变 → 占本卦卦辞（辅以本卦彖、象）",
    1: "一爻变 → 以本卦变爻爻辞为主，之卦卦辞为辅",
    2: "二爻变 → 占本卦二变爻爻辞，以上爻之辞为主",
    3: "三爻变 → 占本卦与之卦卦辞，以本卦为主",
    4: "四爻变 → 占之卦中二不变爻的爻辞",
    5: "五爻变 → 占之卦中不变爻的爻辞",
    6: "六爻皆变 → 乾变坤看乾卦用九；坤变乾看坤卦用六；其余各卦看之卦卦辞",
}


def resolve_gua(text):
    """把用户输入归一化为卦记录。支持卦名、卦序、上下卦组合、全称、X为Y。"""
    t = re.sub(r"[（）()\[\]【】\s]", "", text.strip()).replace("卦", "")
    if not t:
        return None
    # 「艮为山」「坎为水」
    m = re.fullmatch(r"(乾|兑|离|震|巽|坎|艮|坤)为(天|泽|火|雷|风|水|山|地)", t)
    if m:
        return BY_NAME[m.group(1)]
    if t == "习坎":
        return BY_NAME["坎"]
    # 「地山谦」「火雷噬嗑」
    m = re.fullmatch(r"(天|泽|火|雷|风|水|山|地)(天|泽|火|雷|风|水|山|地)(.+)", t)
    if m and m.group(3) in BY_NAME:
        return BY_NAME[m.group(3)]
    # 卦名
    if t in BY_NAME:
        return BY_NAME[t]
    # 卦序
    if t.isdigit() and 1 <= int(t) <= 64:
        return BY_NAME[GUA[int(t) - 1][1]]
    # 「艮上艮下」/「上艮下艮」
    m = re.fullmatch(r"上?(.)[上下/…\-](.)下?", t)
    if m:
        up, down = m.group(1), m.group(2)
        if up in TRI and down in TRI:
            return BY_PATTERN.get(TRI[down] + TRI[up])
    return None


def fmt_pattern(pattern):
    return "".join(str(x) for x in pattern)


def full_name(rec):
    """输出规范全称：八纯卦用「X为Y」，其余用「上象+下象+卦名」。"""
    if rec["name"] in PURE and rec["up"] == rec["down"]:
        return f"{rec['up']}为{SYMBOL[rec['up']]}"
    return f"{SYMBOL[rec['up']]}{SYMBOL[rec['down']]}{rec['name']}"


def parse_changing(text):
    """解析变爻位置，返回升序整数列表（1-6）。"""
    if not text or not text.strip():
        return []
    mapping = {"初": 1, "二": 2, "三": 3, "四": 4, "五": 5, "上": 6,
               "初爻": 1, "二爻": 2, "三爻": 3, "四爻": 4, "五爻": 5, "上爻": 6}
    out = []
    for item in re.split(r"[,，、/\s]+", text.strip()):
        if not item:
            continue
        key = item.replace("九", "").replace("六", "")
        if item in mapping:
            out.append(mapping[item])
        elif key in mapping:
            out.append(mapping[key])
        elif item.isdigit() and 1 <= int(item) <= 6:
            out.append(int(item))
        else:
            raise ValueError(f"无法识别的变爻位置：{item}")
    if len(set(out)) != len(out):
        raise ValueError("变爻位置重复")
    return sorted(out)


def yao_title(idx, pattern):
    """爻题：初位作「初九/初六」，上位作「上九/上六」，其余作「九二/六三」等。"""
    yy = "九" if pattern[idx - 1] == 1 else "六"
    if idx == 1:
        return f"初{yy}"
    if idx == 6:
        return f"上{yy}"
    return f"{yy}{POS_NAME[idx]}"


def main():
    ap = argparse.ArgumentParser(description="易经占卦：由本卦与变爻推导之卦与引用范围")
    ap.add_argument("--gua", required=True, help="本卦：卦名/卦序/上下卦组合/全称")
    ap.add_argument("--changing", default="", help="变爻位置，如 6 / 2,4 / 六二 / 初,三")
    args = ap.parse_args()

    rec = resolve_gua(args.gua)
    if rec is None:
        print(f"[错误] 无法识别本卦输入：{args.gua}", file=sys.stderr)
        print("请用卦名（噬嗑）、卦序（21）、上下卦组合（离上震下）或全称（火雷噬嗑）。", file=sys.stderr)
        return 1

    try:
        changing = parse_changing(args.changing)
    except ValueError as e:
        print(f"[错误] {e}", file=sys.stderr)
        return 1

    print("=" * 54)
    print(f"本卦：{rec['name']}（第 {rec['no']} 卦 · {full_name(rec)}，上{rec['up']}下{rec['down']}）")
    print(f"      六爻（自下而上）：{fmt_pattern(rec['pattern'])}")

    if not changing:
        print("变爻：无（静卦）")
        print(f"引用范围：{RULES[0]}")
        print("=" * 54)
        return 0

    titles = "、".join(yao_title(i, rec["pattern"]) for i in changing)
    print(f"变爻：{titles}（位置 {'、'.join(str(i) for i in changing)}）")

    new_pattern = list(rec["pattern"])
    for i in changing:
        new_pattern[i - 1] = 1 - new_pattern[i - 1]
    new_rec = BY_PATTERN[tuple(new_pattern)]

    if new_rec["name"] == rec["name"] and len(changing) != 6:
        print("之卦：与本卦相同（异常，请检查变爻位置）")
    else:
        print(f"之卦：{new_rec['name']}（第 {new_rec['no']} 卦 · {full_name(new_rec)}，"
              f"上{new_rec['up']}下{new_rec['down']}）")
    print(f"      六爻（自下而上）：{fmt_pattern(new_pattern)}")
    print(f"引用范围：{RULES[len(changing)]}")

    if len(changing) == 6:
        if rec["name"] == "乾":
            print("补充：乾六爻皆变（乾变坤）→ 取乾卦「用九」")
        elif rec["name"] == "坤":
            print("补充：坤六爻皆变（坤变乾）→ 取坤卦「用六」")
        else:
            print(f"补充：六爻皆变且非乾坤 → 取之卦「{new_rec['name']}」卦辞")

    print("=" * 54)
    return 0


if __name__ == "__main__":
    sys.exit(main())
