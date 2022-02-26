# -*- coding: utf-8 -*-
# ファイル syn.py
#
# %%
import sys
import re
from typing import List


class InfParser():
    def __init__(self, version=0):
        self.version = version
        self.keys = "p3", "f2", "a1", "L", "a2", "M"

    @property
    def value_1(self):
        if self.version == 0:
            return ["sil", 0, 100, 100, 100, ""]
        elif self.version == 1:
            raise NotImplementedError
        else:
            raise NotImplementedError

    @property
    def value_pau(self):
        if self.version == 0:
            return ["pau", 0, 100, 100, 100, ""]
        elif self.version == 1:
            raise NotImplementedError
        else:
            raise NotImplementedError

    @property
    def value_sil(self):
        if self.version == 0:
            return ["sil", 0, -100, 200, 100, ""]
        elif self.version == 1:
            raise NotImplementedError
        else:
            raise NotImplementedError

    def content2columns(self, content: str) -> dict:
        """_summary_

        Args:
            content (str): a1, a2, などとパースする対象のstr
                p3, f2, a1, L, a2, M などの列を取得
                本当はここで\とか/とか処理したい

        Returns:
            dict: "a1" や "a2" などを key に持つ dict
        """
        # p3 is between - and + (e.g. sh^i-pau+i=...)
        # self.versionが1の時はbcdを取得して morph id を追加する。
        # is_first みたいなのもあると#で挿入しやすい
        # LMN は inf がない. カラムは統一する。
        p3: str = content.split("-")[1].split("+")[0]
        f2 = re.findall(r"\/F:.*?_([0-9])", content)
        a1 = re.findall(r"\/A:([0-9\-]+)", content)
        L = re.findall(r"\/L:.*?_([0-9\-]+)*", content)
        a2 = re.findall(r"\/A:.*?\+([0-9]+)\+", content)
        M = re.findall(r"\/M:.*?_([0-9\-]+)*", content)
        if p3 == "pau":
            value_i = self.value_pau
        elif p3 == "sil":
            value_i = self.value_sil
        else:
            M_map = {0: "", 1: ", ", 2: ". ", 3: "? ", 4: "! "}
            M = M_map.get(int(M[0]), "_ ")
            value_i = [p3] + \
                list(map(lambda i: int(i[0]), [f2, a1, L, a2]))+[M]
        return {k: v for k, v in zip(self.keys, value_i)}

    def inf2lines(self, rlist: List[str]):
        """テキストを生成
        Args:
            rlist (List[str]): _description_
            version (int, optional): 
                0: 先行研究
                1: 本研究1
                2: 本研究2
        Returns:
            _type_: _description_
        """
        # r_list の要素iを split した 2 番目が必要な情報(pやaなど)
        # 0 3950000 xx^xx-sil+s=o/A:xx+xx+xx/B:xx-xx_xx/C:xx_xx+xx/D:07+xx_xx/E:xx_xx!xx_xx-xx/F:xx_xx#xx_xx@xx_xx|xx_xx/G:2_2%0_xx_xx/H:xx_xx/I:xx-xx@xx+xx&xx-xx|xx+xx/J:5_21/K:1+5-11/L:
        # cf. https://docs.google.com/document/d/1qTUQO-dfWQjJovI0_cvV9V60NG-wD4Ic4Ev3_xjeBfA/edit#heading=h.7xfwt25c9zms
        contents: List[str] = list(map(lambda s: s.split(" ")[2], rlist))
        first_line = [{k: v for k, v in zip(self.keys, self.value_1)}]
        return first_line + list(map(self.content2columns, contents))

    def lines2txt(self, lines):
        # やっぱ個々で分割だな
        # 取得したp3やa1など中身(int)から記号(,.?!/\)と依存関係の距離(#[0-9])を追加
        txt = ""
        for i, line_i in enumerate(lines):
            if line_i["p3"] in ["sil", "pau"]:
                txt += lines[i-1]["M"]  # 現在がsil等なら一つ前のMを参照(理由不明)
                continue

            txt += line_i["p3"] + " "

            # TODO: ここもMに格納するタイミングで処理したいが、次のラインのa1が必要だからだめか？
            if (line_i["a1"] == 0 and lines[i+1]["a1"] == 1):
                txt += "\ "
            elif (line_i["a2"] == 1 and lines[i+1]["a2"] == 2):
                txt += "/ "
            else:
                txt += ""

            # 依存距離
            if (line_i["a1"] > lines[i+1]["a1"] or line_i["f2"] != lines[i+1]["f2"]):
                if ((line_i["L"] > 1) and (line_i["L"] == lines[i+1]["L"])):
                    dependency_dist = "#1 "
                elif (line_i["L"] < 1):
                    dependency_dist = "#1 "
                elif (line_i["L"] > 6):
                    dependency_dist = "#6 "
                else:
                    dependency_dist = "#" + str(line_i["L"]) + " "
                if (lines[i+1]["L"] != 200):
                    txt += dependency_dist
        return txt

    def inf2txt(self, rlist):
        return self.lines2txt(self.inf2lines(rlist))


def main():
    """
        arg1: file name w/o suffix
        arg2: experiment version
    """
    if len(sys.argv) < 2:
        print("処理ファイル名を指定してください。\n")
        sys.exit()

    version = 0 if len(sys.argv) == 2 else int(sys.argv[2])
    if version == 0:
        suffix = ".inf2"
    elif version == 1:
        suffix = ".inf"
    else:
        raise NotImplementedError("version の指定 {0, 1}がおかしい")

    with open("yomi/" + sys.argv[1] + suffix, "r") as f:
        l_strip = [s.strip() for s in f.readlines()]  # readlines and remove \n
        inf2_str = list(filter(len, l_strip))  # filter zero-length str: ""
        parser = InfParser(version)
        txt = parser.inf2txt(inf2_str)

    print(sys.argv[1], txt)


if __name__ == "__main__":
    main()
