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


def get_p3(content: str) -> str:
    """_summary_

    Args:
        content (str): sh^i-pau+i=...

    Returns:
        str: symbol between - and +
            in this case, pau
    """
    return content.split("-")[1].split("+")[0]


def strip_and_split(inf2_str: str) -> List[str]:
    """入力のinfを行に分け、最後の行が""なら除外

    Args:
        inf2_str (str): _description_

    Returns:
        List[str]: _description_
    """
    rlist = inf2_str.split("\n")
    if (rlist[-1] == ""):
        rlist.pop()
    return rlist


def inf2model(inf2_str: str):
    rlist: List[str] = strip_and_split(inf2_str)

    line = [["sil", 0, 100, 100, 100, 0]]
    for w in rlist:
        # w is the follwoing string, which has the content (xx^xx...) in the second position given `split`
        # 0 3950000 xx^xx-sil+s=o/A:xx+xx+xx/B:xx-xx_xx/C:xx_xx+xx/D:07+xx_xx/E:xx_xx!xx_xx-xx/F:xx_xx#xx_xx@xx_xx|xx_xx/G:2_2%0_xx_xx/H:xx_xx/I:xx-xx@xx+xx&xx-xx|xx+xx/J:5_21/K:1+5-11/L:
        # https://docs.google.com/document/d/1qTUQO-dfWQjJovI0_cvV9V60NG-wD4Ic4Ev3_xjeBfA/edit#heading=h.7xfwt25c9zms
        content = w.split(" ")[2]
        p3 = get_p3(content)
        line_dict = {"pau": [["pau", 0, 100, 100, 100, 0]],
                     "sil": [["sil", 0, -100, 200, 100, 0]]}
        if p3 in ["pau", "sil"]:
            line += line_dict[p3]
        else:
            a1 = re.findall(r"\/A:([0-9\-]+)", content)[0]
            a2 = re.findall(r"\/A:.*?\+([0-9]+)\+", content)[0]
            f2 = re.findall(r"\/F:.*?_([0-9])", content)[0]
            # 以下の2つはinf2の特殊な事例
            L = re.findall(r"\/L:.*?_([0-9\-]+)*", content)[0]
            M = re.findall(r"\/M:.*?_([0-9\-]+)*", content)[0]
            line += [[p3, int(f2), int(a1), int(L), int(a2), int(M)]]

    txt = ""
    M_map = {1: ", ", 2: ". ", 3: "? ", 4: "! "}
    for i, line_i in enumerate(line, 0):
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

    obj = open("yomi/" + sys.argv[1] + ".inf2", "r")
    inf2_str = obj.read()
    obj.close()
    txt = inf2model(inf2_str)
    print(sys.argv[1], txt)


if __name__ == "__main__":
    main()
