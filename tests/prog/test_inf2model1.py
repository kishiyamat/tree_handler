import subprocess
from prog.inf2model1 import InfParser


def test_shell():
    # todo: w/o version
    subprocess.run(["bash", "inf2model1_col.sh", "results_new.txt"])
    diff_res = subprocess.run(["diff", "results_original.txt", "results_new.txt"],
                              capture_output=True).stdout
    assert len(diff_res) == 0
    # todo: version 0
    subprocess.run(["bash", "inf2model1_col.sh", "results_new.txt", "0"])
    diff_res = subprocess.run(["diff", "results_original.txt", "results_new.txt"],
                              capture_output=True).stdout
    assert len(diff_res) == 0
    # todo: version 1
    # subprocess.run(["bash", "inf2model1_col.sh", "results_new.txt", "1"])
    # diff_res = subprocess.run(["diff", "results_original.txt", "results_new.txt"],
    #                           capture_output=True).stdout
    # assert len(diff_res) == 0


def test_content2columns():
    parser = InfParser(version=0)
    inf2 = "3100000 4300000 xx^sil-s+o=n/A:-1+1+2/B:xx-xx_xx/C:07_xx+xx/D:02+xx_xx/E:xx_xx!xx_xx-xx/F:2_2#0_xx@1_5|1_21/G:6_3%0_xx_1/H:xx_xx/I:5-21@1+1&1-5|1+11/J:xx_xx/K:1+5-11/L:0_1/M:0_0/N:"
    inf2 = inf2.split(" ")[2]
    res = parser.content2columns(inf2)
    tgt = {"p3": "s", "f2": 2, "a1": -1, "L": 1, "a2": 1, "M": ""}
    assert res == tgt
    inf2 = "5500000 6050000 o^n-o+k=o/A:0+2+1/B:xx-xx_xx/C:07_xx+xx/D:02+xx_xx/E:xx_xx!xx_xx-xx/F:2_2#0_xx@1_5|1_21/G:6_3%0_xx_1/H:xx_xx/I:5-21@1+1&1-5|1+11/J:xx_xx/K:1+5-11/L:0_1/M:0_0/N:"
    inf2 = inf2.split(" ")[2]
    res = parser.content2columns(inf2)
    tgt = {"p3": "o", "f2": 2, "a1": 0, "L": 1, "a2": 2, "M": ""}
    assert res == tgt
    inf2 = "6050000 7100000 n^o-k+o=k/A:-2+1+6/B:07-xx_xx/C:02_xx+xx/D:13+xx_xx/E:2_2!0_xx-1/F:6_3#0_xx@2_4|3_19/G:4_3%0_xx_1/H:xx_xx/I:5-21@1+1&1-5|1+11/J:xx_xx/K:1+5-11/L:1_3/M:0_0/N:"
    inf2 = inf2.split(" ")[2]
    res = parser.content2columns(inf2)
    tgt = {"p3": "k", "f2": 3, "a1": -2, "L": 3, "a2": 1, "M": ""}
    assert res == tgt
    inf2 = "28350000 33650000 t^a-sil+xx=xx/A:xx+xx+xx/B:10-7_2/C:xx_xx+xx/D:xx+xx_xx/E:5_3!0_xx-xx/F:xx_xx#xx_xx@xx_xx|xx_xx/G:xx_xx%xx_xx_xx/H:5_21/I:xx-xx@xx+xx&xx-xx|xx+xx/J:xx_xx/K:1+5-11/L:1_0/M:0_2/N:"
    inf2 = inf2.split(" ")[2]
    res = parser.content2columns(inf2)
    tgt = {"p3": "sil", "f2": 0, "a1": -100, "L": 200, "a2": 100, "M": ""}
    assert res == tgt
