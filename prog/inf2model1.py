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


def current_segment(content: str) -> str:
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

    lin = [["sil", 0, 100, 100, 100, 0]]
    for w in rlist:
        # w is the follwoing string, which has the content (xx^xx...) in the second position given `split`
        # 0 3950000 xx^xx-sil+s=o/A:xx+xx+xx/B:xx-xx_xx/C:xx_xx+xx/D:07+xx_xx/E:xx_xx!xx_xx-xx/F:xx_xx#xx_xx@xx_xx|xx_xx/G:2_2%0_xx_xx/H:xx_xx/I:xx-xx@xx+xx&xx-xx|xx+xx/J:5_21/K:1+5-11/L:
        content = w.split(" ")[2]
        if current_segment(content) == "pau":
            lin += [["pau", 0, 100, 100, 100, 0]]
            continue

        if current_segment(content) == "sil":
            lin += [["sil", 0, -100, 200, 100, 0]]
            continue

        # (content, A, F)
        p = re.findall(r"\-(.*?)\+.*?\/A:([0-9\-]+).*?\/F:.*?_([0-9])",
                       content)
        # if p != current_segment(content):
        #     print(p, current_segment(content))
        a2 = re.findall(r"\/A:.*?\+([0-9]+)\+", content)
        p2 = re.findall(r"\/L:.*?_([0-9\-]+)*", content)
        p3 = re.findall(r"\/M:.*?_([0-9\-]+)*", content)
        #    p2 = c[2][-14:]

        lin += [[p[0][0], int(p[0][2]), int(p[0][1]),
                 int(p2[0]), int(a2[0]), int(p3[0])]]

    # lin += [["sil", 0, -100, 200, 100, 0]]
    # print(lin)

    txt = ""
    for i, l in enumerate(lin, 0):
        if (l[0] == "sil"):
            if (i == 0):
                continue
            elif (lin[i-1][5] == 2):
                txt += ". "
            elif (lin[i-1][5] == 3):
                txt += "? "
            elif (lin[i-1][5] == 4):
                txt += "! "
            continue

        elif (l[0] == "pau"):
            if (lin[i-1][5] == 1):
                txt += ", "
            elif (lin[i-1][5] == 2):
                txt += ". "
            elif (lin[i-1][5] == 3):
                txt += "? "
            elif (lin[i-1][5] == 4):
                txt += "! "
            else:
                txt += "_ "
            continue

        txt += l[0] + " "

        if (l[2] == 0 and lin[i+1][2] == 1):
            txt += "\ "
        elif (l[4] == 1 and lin[i+1][4] == 2):
            txt += "/ "

        if (lin[i][2] > lin[i+1][2] or lin[i][1] != lin[i+1][1]):
            if ((l[3] > 1) and (lin[i][3] == lin[i+1][3])):
                dd = "#1 "
            elif (l[3] < 1):
                dd = "#1 "
            elif (l[3] > 6):
                dd = "#6 "
            else:
                dd = "#" + str(l[3]) + " "

            if (lin[i+1][3] != 200):
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
