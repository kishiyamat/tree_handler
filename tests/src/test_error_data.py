import os
import sys
from copy import deepcopy
from typing import Any

import pytest
from nltk.tree import ParentedTree
from prog.inf2model1 import InfParser

from src.tree_handler import TreeHandler

sys.path.append('..')


def pathidx2mphpsd(path, idx):
    tgt_inf_path = f"./tests/data/{path}/{idx}.inf2"
    tgt_psd_path = f"./tests/data/{path}/{idx}.psd"

    with open(tgt_inf_path, "r") as f:
        l_strip = [s.strip() for s in f.readlines()]  # readlines and remove \n
        tgt_inf_str = list(filter(len, l_strip))  # filter zero-length str: ""
        parser = InfParser(2)
        tgt_morph = parser.inf2txt(tgt_inf_str)

    with open(tgt_psd_path, "r") as f:
        tree_str = f.read()

    return tgt_morph, tree_str


def test_data():
    # 報告のあったエラーが解消されていることを確認
    # IndexError はスコープ外
    th = TreeHandler()
    path = "error_subtree"  # エラータイプ

    tgt_idx_s = ["Arabian01_00070",
                 "Arabian01_00280", ]
    for tgt_id in tgt_idx_s:
        tgt_morph, tree_str = pathidx2mphpsd(path, tgt_id)
        th.workflow(tgt_morph, tree_str)

    tgt_idx_s_idxerror = [
        "Arabian01_00220",  # IndexError(LESS) # _reduce_2起因
        "Arabian01_00330",  # IndexError(LESS) # _reduce_2起因
        "Arabian01_00350",  # IndexError(LESS) # _reduce_2起因
        "Arabian01_00390",  # IndexError(LESS) # _reduce_2起因
        "Arabian01_00020",  # IndexError(LESS) # align_np起因
        "Arabian01_00110",  # IndexError(LESS) # align_np起因
        "Arabian01_00130",  # IndexError(OOR) # align_np起因
        "Arabian01_00490",  # IndexError(OOR) # align_np起因
    ]
    for tgt_id in tgt_idx_s_idxerror:
        with pytest.raises(IndexError):
            tgt_morph, tree_str = pathidx2mphpsd(path, tgt_id)
            th.workflow(tgt_morph, tree_str)

    path = "error_subtree2"  # エラータイプ

    tgt_idx_s_idxerror = [
        "Arabian01_01150",  # fix align_vp -> IndexError
        "Arabian02_00890",  # fix align_vp -> IndexError
        "Arabian02_05860",  # fix align_vp -> IndexError
        "Arabian01_03980",  # fix align_vp -> IndexError
    ]
    for tgt_id in tgt_idx_s_idxerror:
        with pytest.raises(IndexError):
            tgt_morph, tree_str = pathidx2mphpsd(path, tgt_id)
            th.workflow(tgt_morph, tree_str)

    tgt_idx_s = ["Arabian03_04540",  # reduce_1起因
                 "Arabian03_02230",  # reduce_1起因
                 "Arabian03_02100",  # reduce_1起因
                 "Arabian02_06640",  # reduce_1起因
                 "Arabian02_01350",  # reduce_1起因
                 "Arabian01_02930",  # reduce_1起因
                 "Arabian01_02920",  # reduce_1起因
                 "Arabian01_02460",  # reduce_1起因
                 "Arabian01_01420",  # reduce_1起因
                 "Arabian01_01420", ]  # reduce_1起因
    for tgt_id in tgt_idx_s:
        tgt_morph, tree_str = pathidx2mphpsd(path, tgt_id)
        th.workflow(tgt_morph, tree_str)
