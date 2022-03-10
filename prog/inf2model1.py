# -*- coding: utf-8 -*-
# ファイル syn.py
#
# %%
import sys
import re
from typing import List
import logging

logging.basicConfig(filename='error_inf.log', filemode='a', level=logging.DEBUG)


class InfParser():
    def __init__(self, version=0):
        self.version = version
        self.keys = "p3", "f2", "a1", "L", "a2", "M", "B", "C", "D"
        self.value_1 = ["sil", 0, 100, 100, 100, "", 0, 0, 0]
        self.value_pau = ["pau", 0, 100, 100, 100, "", 0, 0, 0]
        self.value_sil = ["sil", 0, -100, 200, 100, "", 0, 0, 0]

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
        a1 = re.findall(r"\/A:([0-9\-]+)", content)
        a2 = re.findall(r"\/A:.*?\+([0-9]+)\+", content)
        f2 = re.findall(r"\/F:.*?_([0-9])", content)
        B = re.findall(r"\/B:(.*)\/C", content)[0]
        C = re.findall(r"\/C:(.*)\/D", content)[0]
        D = re.findall(r"\/D:(.*)\/E", content)[0]
        L = re.findall(r"\/L:.*?_([0-9\-]+)*", content)
        M = re.findall(r"\/M:.*?_([0-9\-]+)*", content)

        if p3 == "pau":
            value_i = self.value_pau
        elif p3 == "sil":
            value_i = self.value_sil
        else:
            M_map = {0: "", 1: ", ", 2: ". ", 3: "? ", 4: "! "}
            M = M_map.get(int(M[0]), "_ ")
            value_i = [p3] + \
                list(map(lambda i: int(i[0]), [f2, a1, L, a2])) + \
                [M, B, C, D]
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
        # 取得したp3やa1など中身(int)から記号(,.?!/\)と依存関係の距離(#[0-9])を追加
        txt = ""
        morph_idx = 0
        if self.version == 2:
            txt += f"#{morph_idx} "
            morph_idx += 1
        for i, line_i in enumerate(lines):
            if line_i["p3"] in ["sil", "pau"]:
                txt += lines[i-1]["M"]  # 現在がsil等なら一つ前のMを参照(理由不明)
                continue

            txt += line_i["p3"] + " "
            # TODO: ここもMに格納するタイミングで処理したいが、次のラインのa1が必要だからだめか？
            if self.version == 1:
                if (line_i["a1"] == 0 and lines[i+1]["a1"] == 1):
                    txt += "\ "
                elif (line_i["a2"] == 1 and lines[i+1]["a2"] == 2):
                    txt += "/ "
                else:
                    txt += ""
            elif self.version in [0, 2]:
                if (line_i["a1"] == 0 and lines[i+1]["a1"] == 1):
                    txt += "\ "
                elif (line_i["a2"] == 1 and lines[i+1]["a2"] == 2):
                    # FIXME: /が必要ならこの条件分岐は不要になる
                    txt += ""
                else:
                    txt += ""
            else:
                raise ValueError

            # txt += line_i["p3"] + " "
            # 依存距離 OR Morph id
            if self.version == 1:
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
            elif self.version == 2:
                is_not_switched = line_i["B"] == lines[i+1]["B"] and line_i["C"] == lines[i +
                                                                                          1]["C"] and line_i["D"] == lines[i+1]["D"]
                is_switched = not is_not_switched
                if is_switched:
                    txt += f"#{morph_idx} "
                    morph_idx += 1
            else:
                continue
        return txt

    def inf2txt(self, rlist):
        return self.lines2txt(self.inf2lines(rlist))


def main():
    """
        arg1: file name w/o suffix
        arg2: experiment version
            0: 先行研究
    """
    SUFFIX = ".inf2"

    if len(sys.argv) < 2:
        print("処理ファイル名を指定してください。\n")
        sys.exit()

    if len(sys.argv) == 2:
        # test
        # - directory は yomi 配下
        # - versionはなしだが、theirs の動作確認のため1を指定
        file_dir = "yomi/"
        version = 1
    else:
        file_dir = "inf/"
        version = int(sys.argv[2])

    filename = file_dir + sys.argv[1] + SUFFIX
    with open(filename, "r") as f:
        l_strip = [s.strip() for s in f.readlines()]  # readlines and remove \n
        inf2_str = list(filter(len, l_strip))  # filter zero-length str: ""
        parser = InfParser(version)
        try:
            txt = parser.inf2txt(inf2_str)
        except IndexError:
            logging.debug('value')
        except ValueError:
            logging.debug('index')
        

    if version == 2:
        # > で file ごとに作成していく
        # version2は mph を生成し、mphは 冒頭にファイル名を入れない
        print(txt)
    else:
        # >> で一つのファイルに書き足していく
        print(sys.argv[1], txt)


if __name__ == "__main__":
    main()
