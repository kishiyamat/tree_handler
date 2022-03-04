import subprocess

from prog.inf2model1 import InfParser


def test_shell():
    # todo: w/o version
    subprocess.run(["bash", "oneliner.sh", "results_new.txt"])
    diff_res = subprocess.run(["diff", "results_original.txt", "results_new.txt"],
                              capture_output=True).stdout
    assert len(diff_res) == 0
    # todo: version 0
    subprocess.run(["bash", "oneliner.sh", "results_new.txt", "1"])
    diff_res = subprocess.run(["diff", "results_original.txt", "results_new.txt"],
                              capture_output=True).stdout
    assert len(diff_res) == 0
    # todo: version 1
    # todo: version 2
    # subprocess.run(["bash", "oneliner.sh", "results_new.txt", "1"])
    # diff_res = subprocess.run(["diff", "results_original.txt", "results_new.txt"],
    #                           capture_output=True).stdout
    # assert len(diff_res) == 0


def test_inf2txt():
    # TODO: inf2以外が来たら raise
    # inf2: version 0（ベースライン）
    # fname = "yomi/Arabian01_00050.inf2"
    # tgt = "s o / n o #1 k o / k u o \ o n i w a #3 f U / t a r i \ n o #1 o \ o j i g a #1 a / r i m a \ sh I t a . "
    FNAME = "yomi/Arabian01_00050.inf2"
    version = 0
    with open(FNAME, "r") as f:
        l_strip = [s.strip() for s in f.readlines()]  # readlines and remove \n
        inf2_str = list(filter(len, l_strip))  # filter zero-length str: ""
        parser = InfParser(version=version)
        res = parser.inf2txt(inf2_str)
        tgt = "s o n o k o k u o \ o n i w a f U t a r i \ n o o \ o j i g a a r i m a \ sh I t a . "
        assert res == tgt
    # inf2: version 1 (先行研究)
    version = 1
    tgt = "s o / n o #1 k o / k u o \ o n i w a #3 f U / t a r i \ n o #1 o \ o j i g a #1 a / r i m a \ sh I t a . "
    with open(FNAME, "r") as f:
        l_strip = [s.strip() for s in f.readlines()]  # readlines and remove \n
        inf2_str = list(filter(len, l_strip))  # filter zero-length str: ""
        parser = InfParser(version=version)
        res = parser.inf2txt(inf2_str)
        assert res == tgt
    # inf2: version 2 (提案手法)
    version = 2
    tgt = "#0 s o n o #1 k o k u o \ o #2 n i #3 w a #4 f U t a r i \ #5 n o #6 o \ o j i #7 g a #8 a r i #9 m a \ sh I #10 t a #11 . "
    with open(FNAME, "r") as f:
        l_strip = [s.strip() for s in f.readlines()]  # readlines and remove \n
        inf2_str = list(filter(len, l_strip))  # filter zero-length str: ""
        parser = InfParser(version=version)
        res = parser.inf2txt(inf2_str)
        assert res == tgt


def test_content2columns():
    # inf2: version 1
    version = 1
    parser = InfParser(version=version)
    inf2 = "3100000 4300000 xx^sil-s+o=n/A:-1+1+2/B:xx-xx_xx/C:07_xx+xx/D:02+xx_xx/E:xx_xx!xx_xx-xx/F:2_2#0_xx@1_5|1_21/G:6_3%0_xx_1/H:xx_xx/I:5-21@1+1&1-5|1+11/J:xx_xx/K:1+5-11/L:0_1/M:0_0/N:"
    inf2 = inf2.split(" ")[2]
    res = parser.content2columns(inf2)
    tgt = {"p3": "s", "f2": 2, "a1": -1, "L": 1, "a2": 1, "M": "",
           "B": "xx-xx_xx", "C": "07_xx+xx", "D": "02+xx_xx"}
    assert res == tgt
    inf2 = "5500000 6050000 o^n-o+k=o/A:0+2+1/B:xx-xx_xx/C:07_xx+xx/D:02+xx_xx/E:xx_xx!xx_xx-xx/F:2_2#0_xx@1_5|1_21/G:6_3%0_xx_1/H:xx_xx/I:5-21@1+1&1-5|1+11/J:xx_xx/K:1+5-11/L:0_1/M:0_0/N:"
    inf2 = inf2.split(" ")[2]
    res = parser.content2columns(inf2)
    tgt = {"p3": "o", "f2": 2, "a1": 0, "L": 1, "a2": 2, "M": "",
           "B": "xx-xx_xx", "C": "07_xx+xx", "D": "02+xx_xx"}
    assert res == tgt
    inf2 = "6050000 7100000 n^o-k+o=k/A:-2+1+6/B:07-xx_xx/C:02_xx+xx/D:13+xx_xx/E:2_2!0_xx-1/F:6_3#0_xx@2_4|3_19/G:4_3%0_xx_1/H:xx_xx/I:5-21@1+1&1-5|1+11/J:xx_xx/K:1+5-11/L:1_3/M:0_0/N:"
    inf2 = inf2.split(" ")[2]
    res = parser.content2columns(inf2)
    tgt = {"p3": "k", "f2": 3, "a1": -2, "L": 3, "a2": 1, "M": "",
           "B": "07-xx_xx", "C": "02_xx+xx", "D": "13+xx_xx"}
    assert res == tgt
    inf2 = "28350000 33650000 t^a-sil+xx=xx/A:xx+xx+xx/B:10-7_2/C:xx_xx+xx/D:xx+xx_xx/E:5_3!0_xx-xx/F:xx_xx#xx_xx@xx_xx|xx_xx/G:xx_xx%xx_xx_xx/H:5_21/I:xx-xx@xx+xx&xx-xx|xx+xx/J:xx_xx/K:1+5-11/L:1_0/M:0_2/N:"
    inf2 = inf2.split(" ")[2]
    res = parser.content2columns(inf2)
    tgt = {"p3": "sil", "f2": 0, "a1": -100, "L": 200,
           "a2": 100, "M": "", "B": 0, "C": 0, "D": 0}
    assert res == tgt
    # TODO: version0のテスト
    # TODO: version2のテスト
