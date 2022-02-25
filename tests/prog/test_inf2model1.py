import subprocess


def test_shell():
    subprocess.run(["bash", "inf2model1_col.sh", "results_new.txt"])
    diff_res = subprocess.run(
        ["diff", "results_original.txt", "results_new.txt"]).stdout
    assert diff_res == None
