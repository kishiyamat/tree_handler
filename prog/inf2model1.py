# -*- coding: utf-8 -*-
# ファイル syn.py
#
# %%
import sys
import re
from typing import List


class InfFile():
    def __init__(self, dep_info=True):
        self.dep_info = dep_info  # true: inf2 a
        pass


def inf2model(rlist: List[str]):
    # p3, f2, a1, L, a2, M を各行で取得
    # r_list の要素iを split した 2 番目が必要な情報(pやaなど)
    # 0 3950000 xx^xx-sil+s=o/A:xx+xx+xx/B:xx-xx_xx/C:xx_xx+xx/D:07+xx_xx/E:xx_xx!xx_xx-xx/F:xx_xx#xx_xx@xx_xx|xx_xx/G:2_2%0_xx_xx/H:xx_xx/I:xx-xx@xx+xx&xx-xx|xx+xx/J:5_21/K:1+5-11/L:
    # cf. https://docs.google.com/document/d/1qTUQO-dfWQjJovI0_cvV9V60NG-wD4Ic4Ev3_xjeBfA/edit#heading=h.7xfwt25c9zms
    contents = map(lambda s: s.split(" ")[2], rlist)
    # 最初の p3, f2, a1, L, a2, M を加えておく
    keys = "p3", "f2", "a1", "L", "a2", "M"
    value_1 = ["sil", 0, 100, 100, 100, 0]
    line = [{k: v for k, v in zip(keys, value_1)}]
    # 以下の処理は必要なタグが変わるかもしれないので、できるかぎりネストせずに保つ
    for content in contents:
        # p3 is between - and + (e.g. sh^i-pau+i=...)
        p3: str = content.split("-")[1].split("+")[0]
        f2 = re.findall(r"\/F:.*?_([0-9])", content)
        a1 = re.findall(r"\/A:([0-9\-]+)", content)
        L = re.findall(r"\/L:.*?_([0-9\-]+)*", content)
        a2 = re.findall(r"\/A:.*?\+([0-9]+)\+", content)
        M = re.findall(r"\/M:.*?_([0-9\-]+)*", content)
        # FIXME: remove if statement
        if p3 == "pau":
            value_i = ["pau", 0, 100, 100, 100, 0]
        elif p3 == "sil":
            value_i = ["sil", 0, -100, 200, 100, 0]
        else:
            value_i = [p3]+list(map(lambda i: int(i[0]), [f2, a1, L, a2, M]))
        line += [{k: v for k, v in zip(keys, value_i)}]

    # 取得したp3やa1など中身(int)から記号(,.?!/\)と依存関係の距離(#[0-9])を追加
    M_map = {1: ", ", 2: ". ", 3: "? ", 4: "! "}
    txt = ""
    for i, line_i in enumerate(line):  # ""を足す、と考えると一般化していく
        if line_i["p3"] == "sil":
            if i != 0 and line[i-1]["M"] in [2, 3, 4]:  # . ? !
                txt += M_map[line[i-1]["M"]]
            continue
        elif line_i["p3"] == "pau":
            if line[i-1]["M"] in [1, 2, 3, 4]:  # , . ? !
                txt += M_map[line[i-1]["M"]]
            else:
                txt += "_ "
            continue

        line_next = line[i+1]
        txt += line_i["p3"] + " "
        if (line_i["a1"] == 0 and line_next["a1"] == 1):
            txt += "\ "
        elif (line_i["a2"] == 1 and line_next["a2"] == 2):
            txt += "/ "
        else:
            txt += ""
        # 依存距離
        if (line_i["a1"] > line_next["a1"] or line_i["f2"] != line_next["f2"]):
            if ((line_i["L"] > 1) and (line_i["L"] == line_next["L"])):
                dependency_dist = "#1 "
            elif (line_i["L"] < 1):
                dependency_dist = "#1 "
            elif (line_i["L"] > 6):
                dependency_dist = "#6 "
            else:
                dependency_dist = "#" + str(line_i["L"]) + " "
            if (line_next["L"] != 200):
                txt += dependency_dist
    return txt


def main():
    if len(sys.argv) < 2:
        print("処理ファイル名を指定してください。\n")
        sys.exit()

    with open("yomi/" + sys.argv[1] + ".inf2", "r") as f:
        l_strip = [s.strip() for s in f.readlines()]  # readlines and remove \n
        inf2_str = list(filter(len, l_strip))  # filter zero-length str: ""
        txt = inf2model(inf2_str)

    print(sys.argv[1], txt)


if __name__ == "__main__":
    main()
