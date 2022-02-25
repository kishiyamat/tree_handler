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
    line = [["sil", 0, 100, 100, 100, 0]]
    # 以下の処理は必要なタグが変わるかもしれないので、できるかぎりネストせずに保つ
    for content in contents:
        p3 = content.split("-")[1].split("+")[0]
        f2 = re.findall(r"\/F:.*?_([0-9])", content)
        a1 = re.findall(r"\/A:([0-9\-]+)", content)
        L = re.findall(r"\/L:.*?_([0-9\-]+)*", content)
        a2 = re.findall(r"\/A:.*?\+([0-9]+)\+", content)
        M = re.findall(r"\/M:.*?_([0-9\-]+)*", content)
        # get content (pau) between - and + (e.g. sh^i-pau+i=...) as list
        if p3 == "pau":
            line_i = ["pau", 0, 100, 100, 100, 0]
        elif p3 == "sil":
            line_i = ["sil", 0, -100, 200, 100, 0]
        else:
            line_i = [p3]+list(map(lambda i: int(i[0]), [f2, a1, L, a2, M]))
        line += [line_i]

    # 取得したp3やa1などの情報から記号(,.?!/\)と依存関係の距離(#[0-9])を追加
    txt = ""
    M_map = {1: ", ", 2: ". ", 3: "? ", 4: "! "}
    for i, line_i in enumerate(line):
        M_prev = line[i-1][5]
        if line_i[0] == "sil":
            if M_prev in [2, 3, 4] and i != 0:
                # . ? !
                txt += M_map[M_prev]
            continue
        elif line_i[0] == "pau":
            if M_prev in [1, 2, 3, 4]:
                # , . ? !
                txt += M_map[M_prev]
            else:
                txt += "_ "
            continue

        line_next = line[i+1]
        p3_i, a1_i, a2_i = line_i[0], line_i[2], line_i[4]
        a1_next, a2_next = line_next[2], line_next[4]
        txt += p3_i + " "

        # ""を足す、と考えると一般化できる
        if (a1_i == 0 and a1_next == 1):
            txt += "\ "
        elif (a2_i == 1 and a2_next == 2):
            txt += "/ "
        # 依存距離
        if (a1_i > a1_next or line_i[1] != line_next[1]):
            if ((line_i[3] > 1) and (line_i[3] == line_next[3])):
                dependency_dist = "#1 "
            elif (line_i[3] < 1):
                dependency_dist = "#1 "
            elif (line_i[3] > 6):
                dependency_dist = "#6 "
            else:
                dependency_dist = "#" + str(line_i[3]) + " "
            if (line[i+1][3] != 200):
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
