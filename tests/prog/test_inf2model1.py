import subprocess


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
