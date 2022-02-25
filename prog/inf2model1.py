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
        L_pau, L_sil, M = 100, 200, 0
        if p3 == "pau":
            line += [["pau", 0, 100, L_pau, 100, M]]
        elif p3 == "sil":
            line += [["sil", 0, -100, L_sil, 100, M]]
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
        if (line_i[0] == "sil"):
            if i in [0, 1]:
                continue
            M_i_prev = line[i-1][5]
            txt += M_map[M_i_prev]

        elif (line_i[0] == "pau"):
            if i in [0]:
                continue
            M_i_prev = line[i-1][5]
            txt += M_map[M_i_prev]

        txt += line_i[0] + " "

        # 正直、ここが一番大事
        if (line_i[2] == 0 and line[i+1][2] == 1):
            txt += "\ "
        elif (line_i[4] == 1 and line[i+1][4] == 2):
            txt += "/ "

        if (line[i][2] > line[i+1][2] or line[i][1] != line[i+1][1]):
            if ((line_i[3] > 1) and (line[i][3] == line[i+1][3])):
                dd = "#1 "
            elif (line_i[3] < 1):
                dd = "#1 "
            elif (line_i[3] > 6):
                dd = "#6 "
            else:
                dd = "#" + str(line_i[3]) + " "

            if (line[i+1][3] != 200):
                txt += dd
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
