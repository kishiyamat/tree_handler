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
    parser = InfParser(version=1)
    inf2 = "3100000 4300000 xx^sil-s+o=n/A:-1+1+2/B:xx-xx_xx/C:07_xx+xx/D:02+xx_xx/E:xx_xx!xx_xx-xx/F:2_2#0_xx@1_5|1_21/G:6_3%0_xx_1/H:xx_xx/I:5-21@1+1&1-5|1+11/J:xx_xx/K:1+5-11/L:0_1/M:0_0/N:"
    inf2 = inf2.split(" ")[2]
    res = parser.content2columns(inf2)
    tgt = {"p3": "s",
           "f2": 2,
           "a1": -1,
           "L": 1,
           "a2": 1,
           "M": "",
           }
    assert res == tgt
