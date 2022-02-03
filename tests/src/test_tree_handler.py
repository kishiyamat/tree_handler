# %%
from nltk.tree import ParentedTree

from src.tree_handler import TreeHandler

# TODO: morphのテスト
# #Numberは形態素ID
# \はアクセント記号
# invalid escape sequence になる
# ojt_out_0: str = """#0 s o n o #1 k o k u o \ o #2 n i #3 w a
#                     #4 f U t a r i \ # 5 n o #6 o \ o j i #7 g a #8 a r i
#                     #9 m a \ sh I #10 t a #11."""

th = TreeHandler()


def test_wrap_siblings():
    # 例0
    haruniwa2_out: str = """
    ( (IP-MAT (PP (NP (D #0その)
                    (N #1国王))
                (P-ROLE #2に)
                (P-OPTR #3は))
            (PP-SBJ (NP (PP (NP (N #4二人))
                            (P-ROLE #5の))
                        (N #6王子))
                    (P-ROLE #7が))
            (VB #8あり)
            (AX #9まし)
            (AXD #10た)
            (PU #11。))
    (ID 1_ex1640391709;JP))
    """
    haruniwa2_out_tgt: str = """
    ( (IP-MAT (PP (NP (D #0その)
                    (N #1国王))
                (P-ROLE #2に)
                (P-OPTR #3は))
            (PP-SBJ (NP (PP (NP (N #4二人))
                            (P-ROLE #5の))
                        (N #6王子))
                    (P-ROLE #7が))
            (VP (VB #8あり)
            (AX #9まし)
            (AXD #10た))
            (PU #11。))
    (ID 1_ex1640391709;JP))
    """
    src = ParentedTree.fromstring(haruniwa2_out)
    tgt = ParentedTree.fromstring(haruniwa2_out_tgt)
    res = th.wrap_siblings(src)
    tgt.pretty_print()
    res.pretty_print()
    assert res == tgt

    # 例0でPUなどが複数存在するケース
    haruniwa2_out: str = """
    ( (IP-MAT (PP (NP (D #0その)
                    (N #1国王))
                (P-ROLE #2に)
                (P-OPTR #3は))
            (PU #11...)
            (PP-SBJ (NP (PP (NP (N #4二人))
                            (P-ROLE #5の))
                        (N #6王子))
                    (P-ROLE #7が))
            (PU #11...)
            (PU #11、)
            (VB #8あり)
            (AX #9まし)
            (AXD #10た)
            (PU #11...)
            (PU #11。)
            )
    (ID 1_ex1640391709;JP))
    """
    haruniwa2_out_tgt: str = """
    ( (IP-MAT (PP (NP (D #0その)
                    (N #1国王))
                (P-ROLE #2に)
                (P-OPTR #3は))
            (PU #11...)
            (PP-SBJ (NP (PP (NP (N #4二人))
                            (P-ROLE #5の))
                        (N #6王子))
                    (P-ROLE #7が))
            (PU #11...)
            (PU #11、)
            (VP (VB #8あり)
            (AX #9まし)
            (AXD #10た))
            (PU #11...)
            (PU #11。)
            )
    (ID 1_ex1640391709;JP))
    """
    src = ParentedTree.fromstring(haruniwa2_out)
    tgt = ParentedTree.fromstring(haruniwa2_out_tgt)
    res = th.wrap_siblings(src)
    tgt.pretty_print()
    res.pretty_print()
    assert res == tgt

# %%
