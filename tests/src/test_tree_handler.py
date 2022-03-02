# %%
from nltk.tree import ParentedTree
import pytest

from src.tree_handler import TreeHandler

th = TreeHandler()


def test_create_vp_node():
    # 2. create VP nodes
    # 例0
    src: str = """
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
    tgt: str = """
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
    src = ParentedTree.fromstring(src)
    tgt = ParentedTree.fromstring(tgt)
    res = th.create_vp_node(src)
    assert res == tgt

    # 例0でPUなどが複数存在するケース
    src: str = """
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
    tgt: str = """
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
    src = ParentedTree.fromstring(src)
    tgt = ParentedTree.fromstring(tgt)
    res = th.create_vp_node(src)
    assert res == tgt

    # 例1
    src = """
    ( (IP-MAT (PP-SBJ (NP (D #0-かの)
                          (N #1-猫))
                      (P-OPTR #2-は))
              (PP-OB1 (NP (IP-REL (NP-SBJ *T*)
                                  (PP-OB1 (NP (IP-REL (NP-SBJ *T*)
                                                      (ADJI #3-黄色い))
                                              (N #4-道))
                                          (P-ROLE #5-を))
                                  (VB #6-歩く))
                          (N #7-犬))
                      (P-ROLE #8-を))
              (ADVP (ADV #9-ゆっくり))
              (VB #10-見)
              (AXD #11-た)
              (MD #12-よう)
              (AX #13-だっ)
              (AXD #14-た)
              (AX #15-らしい)
              (PU #16-。))
      (ID 1_ex1642489342;JP))
    """
    tgt = """
    ( (IP-MAT (PP-SBJ (NP (D #0-かの)
                          (N #1-猫))
                      (P-OPTR #2-は))
              (VP  (PP-OB1 (NP (IP-REL (NP-SBJ *T*)
                                  (VP (PP-OB1 (NP (IP-REL (NP-SBJ *T*)
                                                       (ADJI #3-黄色い))
                                              (N #4-道))
                                          (P-ROLE #5-を))
                                  (VB #6-歩く)))
                          (N #7-犬))
                      (P-ROLE #8-を))
              (ADVP (ADV #9-ゆっくり))
              (VB #10-見)
              (AXD #11-た)
              (MD #12-よう)
              (AX #13-だっ)
              (AXD #14-た)
              (AX #15-らしい))
              (PU #16-。))
      (ID 1_ex1642489342;JP))
    """
    src = ParentedTree.fromstring(src)
    tgt = ParentedTree.fromstring(tgt)
    res = th.create_vp_node(src)
    assert res == tgt

    # 例2
    src = """
        ( (CP-QUE (IP-SUB (NP-SBJ *pro*)
                        (PP-OB1 (NP (WPRO #0-何))
                                (P-ROLE #1-を))
                        (VB #2-買っ)
                        (P-CONN #3-て)
                        (VB2 #4-あげ)
                        (MD #5-よう))
                (P-FINAL #6-か)
                (PU #7-？))
        (ID 1_ex1643115998;JP))
    """
    tgt = """
        ( (CP-QUE (IP-SUB (NP-SBJ *pro*)
                        (VP (PP-OB1 (NP (WPRO #0-何))
                                (P-ROLE #1-を))
                        (VB #2-買っ)
                        (P-CONN #3-て)
                        (VB2 #4-あげ)
                        (MD #5-よう)) )
                (P-FINAL #6-か)
                (PU #7-？))
        (ID 1_ex1643115998;JP))
    """
    src = ParentedTree.fromstring(src)
    tgt = ParentedTree.fromstring(tgt)
    res = th.create_vp_node(src)
    assert res == tgt

    # 例3
    src = """
        ( (IP-MAT (PP-SBJ (NP (NPR #0-太郎))
                        (P-OPTR #1-は))
                (PU #2-、)
                (CP-THT (CP-FINAL (PUL #3-「)
                                (IP-SUB (PP-OB1 (NP (NPR #4-二郎))
                                                (P-ROLE #5-を))
                                        (PP-SBJ (NP (NPR #6-花子))
                                                (P-ROLE #7-が))
                                        (VB #8-殴っ)
                                        (AXD #9-た))
                                (P-FINAL #10-よ)
                                (PUR #11-」))
                        (P-COMP #12-と))
                (PP (NP (NPR #13-花子))
                (P-ROLE #14-に))
                (VB #15-言っ)
                (AXD #16-た)
                (PU #17-。))
        (ID 1_ex1643432427;JP))
    """
    tgt = """
        ( (IP-MAT (PP-SBJ (NP (NPR #0-太郎))
                        (P-OPTR #1-は))
                (PU #2-、)
        (VP    (CP-THT (CP-FINAL (PUL #3-「)
                                (IP-SUB (PP-OB1 (NP (NPR #4-二郎))
                                                (P-ROLE #5-を))
                                        (PP-SBJ (NP (NPR #6-花子))
                                                (P-ROLE #7-が))
                                        (VP   (VB #8-殴っ)
                                        (AXD #9-た)))
                                (P-FINAL #10-よ)
                                (PUR #11-」))
                        (P-COMP #12-と))
                (PP (NP (NPR #13-花子))
                (P-ROLE #14-に))
                (VB #15-言っ)
                (AXD #16-た))
                (PU #17-。))
        (ID 1_ex1643432427;JP))
    """
    src = ParentedTree.fromstring(src)
    tgt = ParentedTree.fromstring(tgt)
    res = th.create_vp_node(src)
    assert res == tgt


def test_add_phrase_type():
    # 3. convert ( ) of IPs and ( ) of PP to { } and [ ] respectively
    # 例0
    src: str = """
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
    tgt: str = """
    ( (IP-MAT|{} (PP|[] (NP (D #0その)
                    (N #1国王))
                (P-ROLE #2に)
                (P-OPTR #3は))
            (PP-SBJ|[] (NP (PP (NP (N #4二人))
                            (P-ROLE #5の))
                        (N #6王子))
                    (P-ROLE #7が))
            (VP|[] (VB #8あり)
            (AX #9まし)
            (AXD #10た))
            (PU #11。))
    (ID 1_ex1640391709;JP))
    """
    src, tgt = ParentedTree.fromstring(src), ParentedTree.fromstring(tgt)
    res = th.add_phrase_type(src)
    src.pretty_print()
    tgt.pretty_print()
    res.pretty_print()
    assert res == tgt

    # 例1
    src = """
    ( (IP-MAT (PP-SBJ (NP (D #0-かの)
                          (N #1-猫))
                      (P-OPTR #2-は))
              (VP  (PP-OB1 (NP (IP-REL (NP-SBJ *T*)
                                  (VP (PP-OB1 (NP (IP-REL (NP-SBJ *T*)
                                                       (ADJI #3-黄色い))
                                              (N #4-道))
                                          (P-ROLE #5-を))
                                  (VB #6-歩く)))
                          (N #7-犬))
                      (P-ROLE #8-を))
              (ADVP (ADV #9-ゆっくり))
              (VB #10-見)
              (AXD #11-た)
              (MD #12-よう)
              (AX #13-だっ)
              (AXD #14-た)
              (AX #15-らしい))
              (PU #16-。))
      (ID 1_ex1642489342;JP))
    """
    tgt = """
    ( (IP-MAT|{} (PP-SBJ|[] (NP (D #0-かの)
                          (N #1-猫))
                      (P-OPTR #2-は))
              (VP|[]  (PP-OB1|[] (NP (IP-REL|{} (NP-SBJ *T*)
                                  (VP|[] (PP-OB1|[] (NP (IP-REL (NP-SBJ *T*)
                                                       (ADJI #3-黄色い))
                                              (N #4-道))
                                          (P-ROLE #5-を))
                                  (VB #6-歩く)))
                          (N #7-犬))
                      (P-ROLE #8-を))
              (ADVP (ADV #9-ゆっくり))
              (VB #10-見)
              (AXD #11-た)
              (MD #12-よう)
              (AX #13-だっ)
              (AXD #14-た)
              (AX #15-らしい))
              (PU #16-。))
      (ID 1_ex1642489342;JP))
    """
    src, tgt = ParentedTree.fromstring(src), ParentedTree.fromstring(tgt)
    res = th.add_phrase_type(src)
    src.pretty_print()
    tgt.pretty_print()
    res.pretty_print()
    assert res == tgt

    # 例2
    src = """
        ( (CP-QUE (IP-SUB (NP-SBJ *pro*)
                        (VP (PP-OB1 (NP (WPRO #0-何))
                                (P-ROLE #1-を))
                        (VB #2-買っ)
                        (P-CONN #3-て)
                        (VB2 #4-あげ)
                        (MD #5-よう)) )
                (P-FINAL #6-か)
                (PU #7-？))
        (ID 1_ex1643115998;JP))
    """
    tgt = """
        ( (CP-QUE|{} (IP-SUB (NP-SBJ *pro*)
                        (VP|[] (PP-OB1|[] (NP (WPRO #0-何))
                                (P-ROLE #1-を))
                        (VB #2-買っ)
                        (P-CONN #3-て)
                        (VB2 #4-あげ)
                        (MD #5-よう)) )
                (P-FINAL #6-か)
                (PU #7-？))
        (ID 1_ex1643115998;JP))
    """
    src, tgt = ParentedTree.fromstring(src), ParentedTree.fromstring(tgt)
    res = th.add_phrase_type(src)
    src.pretty_print()
    tgt.pretty_print()
    res.pretty_print()
    assert res == tgt

    # 例3
    src = """
    ( (IP-MAT (PP-SBJ (NP (NPR #0-太郎))
                    (P-OPTR #1-は))
              (PU #2-、)
              (VP (CP-THT (CP-FINAL (PUL #3-「)
                                      (IP-SUB (PP-OB1 (NP (NPR #4-二郎))
                                                      (P-ROLE #5-を))
                                              (PP-SBJ (NP (NPR #6-花子))
                                                      (P-ROLE #7-が))
                                              (VP   (VB #8-殴っ)
                                              (AXD #9-た)))
                                      (P-FINAL #10-よ)
                                      (PUR #11-」))
                              (P-COMP #12-と))
                      (PP (NP (NPR #13-花子))
                      (P-ROLE #14-に))
                      (VB #15-言っ)
                      (AXD #16-た))
                      (PU #17-。))
    (ID 1_ex1643432427;JP))
    """
    tgt = """
        ( (IP-MAT|{} (PP-SBJ|[] (NP (NPR #0-太郎))
                        (P-OPTR #1-は))
                     (PU #2-、)
                     (VP|[] (CP-THT (CP-FINAL|{} (PUL #3-「)
                                             (IP-SUB (PP-OB1|[] (NP (NPR #4-二郎))
                                                             (P-ROLE #5-を))
                                                     (PP-SBJ|[] (NP (NPR #6-花子))
                                                             (P-ROLE #7-が))
                                                     (VP|[]   (VB #8-殴っ)
                                                     (AXD #9-た)))
                                             (P-FINAL #10-よ)
                                             (PUR #11-」))
                                     (P-COMP #12-と))
                             (PP|[] (NP (NPR #13-花子))
                             (P-ROLE #14-に))
                             (VB #15-言っ)
                             (AXD #16-た))
                             (PU #17-。))
        (ID 1_ex1643432427;JP))
    """
    src, tgt = ParentedTree.fromstring(src), ParentedTree.fromstring(tgt)
    res = th.add_phrase_type(src)
    src.pretty_print()
    tgt.pretty_print()
    res.pretty_print()
    assert res == tgt


def test_all_wrapped():
    # 4. align () to each edge of PWords の validation
    # 例0
    src_false = """
        (IP-MAT (PP-SBJ (NP (D #0-かの)
                        (N #1-猫))
                        (P-OPTR #2-は))
                (VP (PP-OB1 (NP (IP-REL (NP-SBJ *T*)
                                        (VP (PP-OB1 (NP (IP-REL (NP-SBJ *T*)
                                                        (VP (ADJI #3-黄色い)))
                                                (N #4-道))
                                                (P-ROLE #5-を))
                                        (VB #6-歩く)))
                                (N #7-犬))
                        (P-ROLE #8-を))
                (ADVP (ADV #9-ゆっくり))
                (VB #10-見)
                (AXD #11-た)
                (MD #12-よう)
                (AX #13-だっ)
                (AXD #14-た)
                (AX #15-らしい))
                (PU #16-。))
        """
    src_true = """
        (IP-MAT (PP-SBJ (NP (D #0-かの)
                        (N #1-猫 P-OPTR #2-は)))
                (VP (PP-OB1 (NP (IP-REL (NP-SBJ *T*)
                                        (VP (PP-OB1 (NP (IP-REL (NP-SBJ *T*)
                                                                (VP (ADJI #3-黄色い)))
                                                        (N #4-道 P-ROLE #5-を)))
                                        (VB #6-歩く)))
                                (N #7-犬 P-ROLE #8-を)))
                (ADVP (ADV #9-ゆっくり))
                (VB #10-見 AXD #11-た MD #12-よう AX #13-だっ AXD #14-た AX #15-らしい))
                (PU #16-。))
        """
    src_false = ParentedTree.fromstring(src_false)
    src_true = ParentedTree.fromstring(src_true)
    assert not th.all_align_np(src_false)
    assert th.all_align_np(src_true)


def test_align_np():
    # 4. align () to each edge of PWords | NP
    # 例0
    src = """
        (IP-MAT
          (PP (NP (D #0その) (N #1国王)) (P-ROLE #2に) (P-OPTR #3は))
          (PP-SBJ (NP (PP (NP (N #4二人)) (P-ROLE #5の)) (N #6王子)) (P-ROLE #7が))
          (VP (VB #8あり) (AX #9まし) (AXD #10た))
          (PU #11。))
        """
    tgt = """
        (IP-MAT
          (PP (NP (D #0その) (N #1国王 #2に #3は)))
          (PP-SBJ (NP (PP (NP (N #4二人 #5の))) (N #6王子 #7が)))
          (VP (VB #8あり) (AX #9まし) (AXD #10た))
          (PU #11。))
        """
    src, tgt = ParentedTree.fromstring(src), ParentedTree.fromstring(tgt)
    src.pretty_print()
    tgt.pretty_print()
    assert th.align_np(src) == tgt

    # 例1
    src = """
    (IP-MAT
      (PP-SBJ (NP (D #0-かの) (N #1-猫)) (P-OPTR #2-は))
      (VP
        (PP-OB1
          (NP
            (IP-REL
              (NP-SBJ *T*)
              (VP
                (PP-OB1
                  (NP (IP-REL (NP-SBJ *T*) (ADJI #3-黄色い)) (N #4-道))
                  (P-ROLE #5-を))
                (VB #6-歩く)))
            (N #7-犬))
          (P-ROLE #8-を))
        (ADVP (ADV #9-ゆっくり))
        (VB #10-見)
        (AXD #11-た)
        (MD #12-よう)
        (AX #13-だっ)
        (AXD #14-た)
        (AX #15-らしい))
      (PU #16-。))
    """
    tgt = """
    (IP-MAT
      (PP-SBJ (NP (D #0-かの) (N #1-猫 #2-は)))
      (VP
        (PP-OB1
          (NP
            (IP-REL
              (NP-SBJ *T*)
              (VP
                (PP-OB1
                  (NP
                    (IP-REL (NP-SBJ *T*) (ADJI #3-黄色い))
                    (N #4-道 #5-を)))
                (VB #6-歩く)))
            (N #7-犬 #8-を)))
        (ADVP (ADV #9-ゆっくり))
        (VB #10-見)
        (AXD #11-た)
        (MD #12-よう)
        (AX #13-だっ)
        (AXD #14-た)
        (AX #15-らしい))
      (PU #16-。))
    """
    src, tgt = ParentedTree.fromstring(src), ParentedTree.fromstring(tgt)
    src.pretty_print()
    tgt.pretty_print()
    assert th.align_np(src) == tgt

    # 例2
    src = """
    (CP-QUE
      (IP-SUB
        (NP-SBJ *pro*)
        (VP
          (PP-OB1 (NP (WPRO #0-何)) (P-ROLE #1-を))
          (VB #2-買っ)
          (P-CONN #3-て)
          (VB2 #4-あげ)
          (MD #5-よう)))
      (P-FINAL #6-か)
      (PU #7-？))
    """
    tgt = """
    (CP-QUE
      (IP-SUB
        (NP-SBJ *pro*)
        (VP
          (PP-OB1 (NP (WPRO #0-何 #1-を)))
          (VB #2-買っ)
          (P-CONN #3-て)
          (VB2 #4-あげ)
          (MD #5-よう)))
      (P-FINAL #6-か)
      (PU #7-？))
    """
    src, tgt = ParentedTree.fromstring(src), ParentedTree.fromstring(tgt)
    src.pretty_print()
    tgt.pretty_print()
    assert th.align_np(src) == tgt

    # 例3
    src = """
    (IP-MAT
      (PP-SBJ (NP (NPR #0-太郎)) (P-OPTR #1-は))
      (PU #2-、)
      (VP
        (CP-THT
          (CP-FINAL
            (PUL #3-「)
            (IP-SUB
              (PP-OB1 (NP (NPR #4-二郎)) (P-ROLE #5-を))
              (PP-SBJ (NP (NPR #6-花子)) (P-ROLE #7-が))
              (VP (VB #8-殴っ) (AXD #9-た)))
            (P-FINAL #10-よ)
            (PUR #11-」))
          (P-COMP #12-と))
        (PP (NP (NPR #13-花子)) (P-ROLE #14-に))
        (VB #15-言っ)
        (AXD #16-た))
      (PU #17-。))
    """
    tgt = """
    (IP-MAT
      (PP-SBJ (NP (NPR #0-太郎 #1-は)))
      (PU #2-、)
      (VP
        (CP-THT
          (CP-FINAL
            (PUL #3-「)
            (IP-SUB
              (PP-OB1 (NP (NPR #4-二郎 #5-を)))
              (PP-SBJ (NP (NPR #6-花子 #7-が)))
              (VP (VB #8-殴っ) (AXD #9-た)))
            (P-FINAL #10-よ)
            (PUR #11-」))
          (P-COMP #12-と))
        (PP (NP (NPR #13-花子 #14-に)))
        (VB #15-言っ)
        (AXD #16-た))
      (PU #17-。))
    """
    src, tgt = ParentedTree.fromstring(src), ParentedTree.fromstring(tgt)
    src.pretty_print()
    tgt.pretty_print()
    assert th.align_np(src) == tgt


def test_align_vp():
    # 4. align () to each edge of PWords | VP
    # 例0
    src = """
        (IP-MAT
          (PP (NP (D #0その) (N #1国王 #2に #3は)))
          (PP-SBJ (NP (PP (NP (N #4二人 #5の))) (N #6王子 #7が)))
          (VP (VB #8あり) (AX #9まし) (AXD #10た))
          (PU #11。))
        """
    tgt = """
        (IP-MAT
          (PP (NP (D #0その) (N #1国王 #2に #3は)))
          (PP-SBJ (NP (PP (NP (N #4二人 #5の))) (N #6王子 #7が)))
          (VP (VB #8あり #9まし #10た))
          (PU #11。))
        """
    src, tgt = ParentedTree.fromstring(src), ParentedTree.fromstring(tgt)
    src.pretty_print()
    tgt.pretty_print()
    assert th.align_vp(src) == tgt

    # 例1
    src = """
    (IP-MAT
      (PP-SBJ (NP (D #0-かの) (N #1-猫 #2-は)))
      (VP
        (PP-OB1
          (NP
            (IP-REL
              (NP-SBJ *T*)
              (VP
                (PP-OB1
                  (NP
                    (IP-REL (NP-SBJ *T*) (ADJI #3-黄色い))
                    (N #4-道 #5-を)))
                (VB #6-歩く)))
            (N #7-犬 #8-を)))
        (ADVP (ADV #9-ゆっくり))
        (VB #10-見)
        (AXD #11-た)
        (MD #12-よう)
        (AX #13-だっ)
        (AXD #14-た)
        (AX #15-らしい))
      (PU #16-。))
    """
    tgt = """
    (IP-MAT
      (PP-SBJ (NP (D #0-かの) (N #1-猫 #2-は)))
      (VP
        (PP-OB1
          (NP
            (IP-REL
              (NP-SBJ *T*)
              (VP
                (PP-OB1
                  (NP
                    (IP-REL (NP-SBJ *T*) (ADJI #3-黄色い))
                    (N #4-道 #5-を)))
                (VB #6-歩く)))
            (N #7-犬 #8-を)))
        (ADVP (ADV #9-ゆっくり))
        (VB #10-見 #11-た #12-よう #13-だっ #14-た #15-らしい))
      (PU #16-。))
    """
    src, tgt = ParentedTree.fromstring(src), ParentedTree.fromstring(tgt)
    src.pretty_print()
    tgt.pretty_print()
    assert th.align_vp(src) == tgt

    # 例2
    src = """
    (CP-QUE
      (IP-SUB
        (NP-SBJ *pro*)
        (VP
          (PP-OB1 (NP (WPRO #0-何 #1-を)))
          (VB #2-買っ)
          (P-CONN #3-て)
          (VB2 #4-あげ)
          (MD #5-よう)))
      (P-FINAL #6-か)
      (PU #7-？))
    """
    tgt = """
    (CP-QUE
      (IP-SUB
        (NP-SBJ *pro*)
        (VP
          (PP-OB1 (NP (WPRO #0-何 #1-を)))
          (VB #2-買っ #3-て #4-あげ #5-よう)))
      (P-FINAL #6-か)
      (PU #7-？))
    """
    src, tgt = ParentedTree.fromstring(src), ParentedTree.fromstring(tgt)
    src.pretty_print()
    tgt.pretty_print()
    assert th.align_vp(src) == tgt

    # 例3
    src = """
    (IP-MAT
      (PP-SBJ (NP (NPR #0-太郎 #1-は)))
      (PU #2-、)
      (VP
        (CP-THT
          (CP-FINAL
            (PUL #3-「)
            (IP-SUB
              (PP-OB1 (NP (NPR #4-二郎 #5-を)))
              (PP-SBJ (NP (NPR #6-花子 #7-が)))
              (VP (VB #8-殴っ) (AXD #9-た)))
            (P-FINAL #10-よ)
            (PUR #11-」))
          (P-COMP #12-と))
        (PP (NP (NPR #13-花子 #14-に)))
        (VB #15-言っ)
        (AXD #16-た))
      (PU #17-。))
    """
    tgt = """
    (IP-MAT
      (PP-SBJ (NP (NPR #0-太郎 #1-は)))
      (PU #2-、)
      (VP
        (CP-THT
          (CP-FINAL
            (PUL #3-「)
            (IP-SUB
              (PP-OB1 (NP (NPR #4-二郎 #5-を)))
              (PP-SBJ (NP (NPR #6-花子 #7-が)))
              (VP (VB #8-殴っ #9-た)))
            (P-FINAL #10-よ)
            (PUR #11-」))
          (P-COMP #12-と))
        (PP (NP (NPR #13-花子 #14-に)))
        (VB #15-言っ #16-た))
      (PU #17-。))
    """
    src, tgt = ParentedTree.fromstring(src), ParentedTree.fromstring(tgt)
    src.pretty_print()
    tgt.pretty_print()
    assert th.align_vp(src) == tgt


def test_align_p_words():
    # 4. align () to each edge of PWords
    # 例0
    src = """
        (IP-MAT
          (PP (NP (D #0その) (N #1国王)) (P-ROLE #2に) (P-OPTR #3は))
          (PP-SBJ (NP (PP (NP (N #4二人)) (P-ROLE #5の)) (N #6王子)) (P-ROLE #7が))
          (VP (VB #8あり) (AX #9まし) (AXD #10た))
          (PU #11。))
        """
    tgt = """
        (IP-MAT
          (PP (NP (D #0その) (N #1国王 #2に #3は)))
          (PP-SBJ (NP (PP (NP (N #4二人 #5の))) (N #6王子 #7が)))
          (VP (VB #8あり #9まし #10た))
          (PU #11。))
        """
    src, tgt = ParentedTree.fromstring(src), ParentedTree.fromstring(tgt)
    src.pretty_print()
    tgt.pretty_print()
    assert th.align_p_words(src) == tgt

    # 例1
    src = """
    (IP-MAT
      (PP-SBJ (NP (D #0-かの) (N #1-猫)) (P-OPTR #2-は))
      (VP
        (PP-OB1
          (NP
            (IP-REL
              (NP-SBJ *T*)
              (VP
                (PP-OB1
                  (NP (IP-REL (NP-SBJ *T*) (ADJI #3-黄色い)) (N #4-道))
                  (P-ROLE #5-を))
                (VB #6-歩く)))
            (N #7-犬))
          (P-ROLE #8-を))
        (ADVP (ADV #9-ゆっくり))
        (VB #10-見)
        (AXD #11-た)
        (MD #12-よう)
        (AX #13-だっ)
        (AXD #14-た)
        (AX #15-らしい))
      (PU #16-。))
    """
    tgt = """
    (IP-MAT
      (PP-SBJ (NP (D #0-かの) (N #1-猫 #2-は)))
      (VP
        (PP-OB1
          (NP
            (IP-REL
              (NP-SBJ *T*)
              (VP
                (PP-OB1
                  (NP
                    (IP-REL (NP-SBJ *T*) (ADJI #3-黄色い))
                    (N #4-道 #5-を)))
                (VB #6-歩く)))
            (N #7-犬 #8-を)))
        (ADVP (ADV #9-ゆっくり))
        (VB #10-見 #11-た #12-よう #13-だっ #14-た #15-らしい))
      (PU #16-。))
    """
    src, tgt = ParentedTree.fromstring(src), ParentedTree.fromstring(tgt)
    src.pretty_print()
    tgt.pretty_print()
    assert th.align_p_words(src) == tgt

    # 例2
    src = """
    (CP-QUE
      (IP-SUB
        (NP-SBJ *pro*)
        (VP
          (PP-OB1 (NP (WPRO #0-何)) (P-ROLE #1-を))
          (VB #2-買っ)
          (P-CONN #3-て)
          (VB2 #4-あげ)
          (MD #5-よう)))
      (P-FINAL #6-か)
      (PU #7-？))
    """
    tgt = """
    (CP-QUE
      (IP-SUB
        (NP-SBJ *pro*)
        (VP
          (PP-OB1 (NP (WPRO #0-何 #1-を)))
          (VB #2-買っ #3-て #4-あげ #5-よう)))
      (P-FINAL #6-か)
      (PU #7-？))
    """
    src, tgt = ParentedTree.fromstring(src), ParentedTree.fromstring(tgt)
    src.pretty_print()
    tgt.pretty_print()
    assert th.align_p_words(src) == tgt

    # 例3
    src = """
    (IP-MAT
      (PP-SBJ (NP (NPR #0-太郎)) (P-OPTR #1-は))
      (PU #2-、)
      (VP
        (CP-THT
          (CP-FINAL
            (PUL #3-「)
            (IP-SUB
              (PP-OB1 (NP (NPR #4-二郎)) (P-ROLE #5-を))
              (PP-SBJ (NP (NPR #6-花子)) (P-ROLE #7-が))
              (VP (VB #8-殴っ) (AXD #9-た)))
            (P-FINAL #10-よ)
            (PUR #11-」))
          (P-COMP #12-と))
        (PP (NP (NPR #13-花子)) (P-ROLE #14-に))
        (VB #15-言っ)
        (AXD #16-た))
      (PU #17-。))
    """
    tgt = """
    (IP-MAT
      (PP-SBJ (NP (NPR #0-太郎 #1-は)))
      (PU #2-、)
      (VP
        (CP-THT
          (CP-FINAL
            (PUL #3-「)
            (IP-SUB
              (PP-OB1 (NP (NPR #4-二郎 #5-を)))
              (PP-SBJ (NP (NPR #6-花子 #7-が)))
              (VP (VB #8-殴っ #9-た)))
            (P-FINAL #10-よ)
            (PUR #11-」))
          (P-COMP #12-と))
        (PP (NP (NPR #13-花子 #14-に)))
        (VB #15-言っ #16-た))
      (PU #17-。))
    """
    src, tgt = ParentedTree.fromstring(src), ParentedTree.fromstring(tgt)
    src.pretty_print()
    tgt.pretty_print()
    assert th.align_p_words(src) == tgt


def test_integrate_morph_accent():
    # 6. convert Japanese characters to phonemes & accents
    # 例0
    src_1 = """#0 s o n o #1 k o k u o \ o #2 n i #3 w a 
               #4 f U t a r i \ #5 n o #6 o \ o j i #7 g a
               #8 a r i #9 m a \ sh I #10 t a #11 ."""
    src_2 = """
        (IP-MAT
          (PP (NP (D #0-その) (N #1-国王 #2-に #3-は)))
          (PP-SBJ (NP (PP (NP (N #4-二人 #5-の))) (N #6-王子 #7-が)))
          (VP (VB #8-あり #9-まし #10-た))
          (PU #11-。))
        """
    tgt = """
        (IP-MAT
          (PP (NP (D s_o_n_o) (N k_o_k_u_o_\_o n_i w_a)))
          (PP-SBJ (NP (PP (NP (N f_U_t_a_r_i_\ n_o))) (N o_\_o_j_i g_a)))
          (VP (VB a_r_i m_a_\_sh_I t_a))
          (PU .))
        """
    src_2, tgt = ParentedTree.fromstring(src_2), ParentedTree.fromstring(tgt)
    res = th.integrate_morph_accent(src_2, src_1)
    assert tgt == res  # tree自体は異なる. tgtはスペース区切りがすべて独立したPOSになっている

    # 例1
    src_1 = """#0 k a \ n o #1 n e k o \ #2 w a
               #3 k i i r o i #4 m i ch i #5 o #6 a r u \ k u #7 i n u \  #8 o
               #9 y u k k u \ r i #10 m i \ #11 t a #12 y o \ o #13 da t  #14 t a 
               #15 r a sh i i #16 ."""
    src_2 = """
        (IP-MAT
          (PP-SBJ (NP (D #0-かの) (N #1-猫 #2-は)))
          (VP
            (PP-OB1
              (NP
                (IP-REL
                  (NP-SBJ *T*)
                  (VP
                    (PP-OB1
                      (NP
                        (IP-REL (NP-SBJ *T*) (ADJI #3-黄色い))
                        (N #4-道 #5-を)))
                    (VB #6-歩く)))
                (N #7-犬 #8-を)))
            (ADVP (ADV #9-ゆっくり))
            (VB #10-見 #11-た #12-よう #13-だっ #14-た #15-らしい))
          (PU #16-。))
        """
    tgt = """
        (IP-MAT
          (PP-SBJ (NP (D k_a_\_n_o) (N n_e_k_o_\ w_a)))
          (VP
            (PP-OB1
              (NP
                (IP-REL
                  (NP-SBJ *T*)
                  (VP
                    (PP-OB1
                      (NP
                        (IP-REL (NP-SBJ *T*) (ADJI k_i_i_r_o_i))
                        (N m_i_ch_i o)))
                    (VB a_r_u_\_k_u)))
                (N i_n_u_\ o)))
            (ADVP (ADV y_u_k_k_u_\_r_i))
            (VB m_i_\ t_a y_o_\_o da_t t_a r_a_sh_i_i))
          (PU .))
        """
    src_2, tgt = ParentedTree.fromstring(src_2), ParentedTree.fromstring(tgt)
    res = th.integrate_morph_accent(src_2, src_1)
    assert tgt == res

    # 例2
    src_1 = "#0 n a \ n i #1 o #2 k a t #3 t e #4 a g e #5 y o \ o #6 k a #7 ?"
    src_2 = """
    (CP-QUE
      (IP-SUB
        (NP-SBJ *pro*)
        (VP
          (PP-OB1 (NP (WPRO #0-何 #1-を)))
          (VB #2-買っ #3-て #4-あげ #5-よう)))
      (P-FINAL #6-か)
      (PU #7-？))
    """
    tgt = """
    (CP-QUE
      (IP-SUB
        (NP-SBJ *pro*)
        (VP
          (PP-OB1 (NP (WPRO n_a_\_n_i o)))
          (VB k_a_t t_e a_g_e y_o_\_o)))
      (P-FINAL k_a)
      (PU ?))
    """
    src_2, tgt = ParentedTree.fromstring(src_2), ParentedTree.fromstring(tgt)
    res = th.integrate_morph_accent(src_2, src_1)
    assert tgt == res

    # 例3
    src_1 = """
    #0 t a r o \ o #1 w a #2 , #3 “ #4 j i r o \ o #5 o #6 h a \ n a k o
    #7 g a #8 n a g u \ t  #9 t a #10 y o #11 “ #12 t o #13 h a \ n a k o
    #14 n i #15 i t #16 t a #17 .
    """
    src_2 = """
    (IP-MAT
      (PP-SBJ (NP (NPR #0-太郎 #1-は)))
      (PU #2-、)
      (VP
        (CP-THT
          (CP-FINAL
            (PUL #3-「)
            (IP-SUB
              (PP-OB1 (NP (NPR #4-二郎 #5-を)))
              (PP-SBJ (NP (NPR #6-花子 #7-が)))
              (VP (VB #8-殴っ #9-た)))
            (P-FINAL #10-よ)
            (PUR #11-」))
          (P-COMP #12-と))
        (PP (NP (NPR #13-花子 #14-に)))
        (VB #15-言っ #16-た))
      (PU #17-。))
    """
    tgt = """
    (IP-MAT
      (PP-SBJ (NP (NPR t_a_r_o_\_o w_a)))
      (PU ,)
      (VP
        (CP-THT
          (CP-FINAL
            (PUL “)
            (IP-SUB
              (PP-OB1 (NP (NPR j_i_r_o_\_o o)))
              (PP-SBJ (NP (NPR h_a_\_n_a_k_o g_a)))
              (VP (VB n_a_g_u_\_t t_a)))
            (P-FINAL y_o)
            (PUR “))
          (P-COMP t_o))
        (PP (NP (NPR h_a_\_n_a_k_o n_i)))
        (VB i_t t_a))
      (PU .))
    """
    src_2, tgt = ParentedTree.fromstring(src_2), ParentedTree.fromstring(tgt)
    res = th.integrate_morph_accent(src_2, src_1)
    # TODO: _が入力にないことを保証
    assert tgt == res


def test_remove_id():
    # もしidがなければValueError
    ill_formed_src: str = """
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
    (id 1_ex1640391709;JP))
    """
    with pytest.raises(ValueError):
        th.remove_outmost_id(ParentedTree.fromstring(ill_formed_src))
    # 例0
    src: str = """
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
    tgt: str = """
    (IP-MAT (PP (NP (D #0その)
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
    """
    src = ParentedTree.fromstring(src)
    tgt = ParentedTree.fromstring(tgt)
    res = th.remove_outmost_id(src)
    src.pretty_print()
    tgt.pretty_print()
    res.pretty_print()
    assert res == tgt

    # 例1
    src = """
    ( (IP-MAT (PP-SBJ (NP (D #0-かの)
                          (N #1-猫))
                      (P-OPTR #2-は))
              (PP-OB1 (NP (IP-REL (NP-SBJ *T*)
                                  (PP-OB1 (NP (IP-REL (NP-SBJ *T*)
                                                      (ADJI #3-黄色い))
                                              (N #4-道))
                                          (P-ROLE #5-を))
                                  (VB #6-歩く))
                          (N #7-犬))
                      (P-ROLE #8-を))
              (ADVP (ADV #9-ゆっくり))
              (VB #10-見)
              (AXD #11-た)
              (MD #12-よう)
              (AX #13-だっ)
              (AXD #14-た)
              (AX #15-らしい)
              (PU #16-。))
      (ID 1_ex1642489342;JP))
    """
    tgt = """
    (IP-MAT (PP-SBJ (NP (D #0-かの)
                          (N #1-猫))
                      (P-OPTR #2-は))
              (PP-OB1 (NP (IP-REL (NP-SBJ *T*)
                                  (PP-OB1 (NP (IP-REL (NP-SBJ *T*)
                                                      (ADJI #3-黄色い))
                                              (N #4-道))
                                          (P-ROLE #5-を))
                                  (VB #6-歩く))
                          (N #7-犬))
                      (P-ROLE #8-を))
              (ADVP (ADV #9-ゆっくり))
              (VB #10-見)
              (AXD #11-た)
              (MD #12-よう)
              (AX #13-だっ)
              (AXD #14-た)
              (AX #15-らしい)
              (PU #16-。))
    """
    src = ParentedTree.fromstring(src)
    tgt = ParentedTree.fromstring(tgt)
    res = th.remove_outmost_id(src)
    src.pretty_print()
    tgt.pretty_print()
    res.pretty_print()
    assert res == tgt

    # 例2
    src = """
    ( (CP-QUE (IP-SUB (NP-SBJ *pro*)
                      (PP-OB1 (NP (WPRO #0-何))
                              (P-ROLE #1-を))
                      (VB #2-買っ)
                      (P-CONN #3-て)
                      (VB2 #4-あげ)
                      (MD #5-よう))
            (P-FINAL #6-か)
            (PU #7-？))
    (ID 1_ex1643115998;JP))
    """
    tgt = """
    (CP-QUE (IP-SUB (NP-SBJ *pro*)
                      (PP-OB1 (NP (WPRO #0-何))
                              (P-ROLE #1-を))
                      (VB #2-買っ)
                      (P-CONN #3-て)
                      (VB2 #4-あげ)
                      (MD #5-よう))
            (P-FINAL #6-か)
            (PU #7-？))
    """
    src = ParentedTree.fromstring(src)
    tgt = ParentedTree.fromstring(tgt)
    res = th.remove_outmost_id(src)
    src.pretty_print()
    tgt.pretty_print()
    res.pretty_print()
    assert res == tgt

    # 例3
    src = """
    ( (IP-MAT (PP-SBJ (NP (NPR #0-太郎))
                          (P-OPTR #1-は))
            (PU #2-、)
            (CP-THT (CP-FINAL (PUL #3-「)
                            (IP-SUB (PP-OB1 (NP (NPR #4-二郎))
                                            (P-ROLE #5-を))
                                    (PP-SBJ (NP (NPR #6-花子))
                                            (P-ROLE #7-が))
                                    (VB #8-殴っ)
                                    (AXD #9-た))
                            (P-FINAL #10-よ)
                            (PUR #11-」))
                    (P-COMP #12-と))
            (PP (NP (NPR #13-花子))
            (P-ROLE #14-に))
            (VB #15-言っ)
            (AXD #16-た)
            (PU #17-。))
    (ID 1_ex1643432427;JP))
    """
    tgt = """
    (IP-MAT (PP-SBJ (NP (NPR #0-太郎))
                          (P-OPTR #1-は))
            (PU #2-、)
            (CP-THT (CP-FINAL (PUL #3-「)
                            (IP-SUB (PP-OB1 (NP (NPR #4-二郎))
                                            (P-ROLE #5-を))
                                    (PP-SBJ (NP (NPR #6-花子))
                                            (P-ROLE #7-が))
                                    (VB #8-殴っ)
                                    (AXD #9-た))
                            (P-FINAL #10-よ)
                            (PUR #11-」))
                    (P-COMP #12-と))
            (PP (NP (NPR #13-花子))
            (P-ROLE #14-に))
            (VB #15-言っ)
            (AXD #16-た)
            (PU #17-。))
    """
    src = ParentedTree.fromstring(src)
    tgt = ParentedTree.fromstring(tgt)
    res = th.remove_outmost_id(src)
    src.pretty_print()
    tgt.pretty_print()
    res.pretty_print()
    assert res == tgt


def test_remove_redunduncy():
    # 例0
    src: str = """
    (IP-MAT|{}
      (PP|[] (NP (D s o n o) (N k o k u o \ o n i w a)))
      (PP-SBJ|[] (NP (PP (NP (N f U t a r i \ n o))) (N o \ o j i g a)))
      (VP|[] (VB a r i m a \ sh I t a))
      (PU .))
    """
    tgt = """
    (IP-MAT|{}
      (PP|[] (D s o n o) (N k o k u o \ o n i w a))
      (PP-SBJ|[] (PP f U t a r i \ n o) (N o \ o j i g a))
      (VP|[] a r i m a \ sh I t a)
      (PU .))
    """
    src = ParentedTree.fromstring(src)
    tgt = ParentedTree.fromstring(tgt).__str__()
    res = th.remove_redunduncy(src).__str__()
    assert tgt == res

    # 例1
    src = """
    (IP-MAT|{}
      (PP-SBJ|[] (NP (D k a \ n o) (N n e k o \ w a)))
      (VP|[]
        (PP-OB1|[]
          (NP
            (IP-REL|{}
              (NP-SBJ *T*)
              (VP|[]
                (PP-OB1|[]
                  (NP
                    (IP-REL (NP-SBJ *T*) (ADJI k i i r o i))
                    (N m i ch i o)))
                (VB a r u \ k u)))
            (N i n u \ o)))
        (ADVP (ADV y u k k u \ r i))
        (VB m i \ t a y o \ o da t t a r a sh i i))
      (PU .))
    """
    tgt = """
    (IP-MAT|{}
      (PP-SBJ|[] (D k a \ n o) (N n e k o \ w a))
      (VP|[]
        (PP-OB1|[]
          (IP-REL|{}
            (VP|[]
              (PP-OB1|[] (IP-REL k i i r o i) (N m i ch i o))
              (VB a r u \ k u)))
          (N i n u \ o))
        (ADVP y u k k u \ r i)
        (VB m i \ t a y o \ o da t t a r a sh i i))
      (PU .))
    """
    src = ParentedTree.fromstring(src)
    tgt = ParentedTree.fromstring(tgt).__str__()
    res = th.remove_redunduncy(src).__str__()
    assert tgt == res

    # 例2
    src = """
    (CP-QUE|{}
      (IP-SUB
        (NP-SBJ *pro*)
        (VP|[]
          (PP-OB1|[] (NP (WPRO n a \ n i o)))
          (VB k a t t e a g e y o \ o)))
      (P-FINAL k a)
      (PU ?))
    """
    tgt = """
    (CP-QUE|{}
      (IP-SUB
        (VP|[] (PP-OB1|[] n a \ n i o) (VB k a t t e a g e y o \ o)))
      (P-FINAL k a)
      (PU ?))
    """
    src = ParentedTree.fromstring(src)
    tgt = ParentedTree.fromstring(tgt).__str__()
    res = th.remove_redunduncy(src).__str__()
    assert tgt == res

    # 例3
    src = """
    (IP-MAT|{}
      (PP-SBJ|[] (NP (NPR t a r o \ o w a)))
      (PU ,)
      (VP|[]
        (CP-THT
          (CP-FINAL|{}
            (PUL “)
            (IP-SUB
              (PP-OB1|[] (NP (NPR j i r o \ o o)))
              (PP-SBJ|[] (NP (NPR h a \ n a k o g a)))
              (VP|[] (VB n a g u \ t t a)))
            (P-FINAL y o)
            (PUR “))
          (P-COMP t o))
        (PP|[] (NP (NPR h a \ n a k o n i)))
        (VB i t t a))
      (PU .))
    """
    tgt = """
    (IP-MAT|{}
      (PP-SBJ|[] t a r o \ o w a)
      (PU ,)
      (VP|[]
        (CP-THT
          (CP-FINAL|{}
            (PUL “)
            (IP-SUB
              (PP-OB1|[] j i r o \ o o)
              (PP-SBJ|[] h a \ n a k o g a)
              (VP|[] n a g u \ t t a))
            (P-FINAL y o)
            (PUR “))
          (P-COMP t o))
        (PP|[] h a \ n a k o n i)
        (VB i t t a))
      (PU .))
    """
    src = ParentedTree.fromstring(src)
    tgt = ParentedTree.fromstring(tgt).__str__()
    res = th.remove_redunduncy(src).__str__()
    assert tgt == res


def test_reduce():
    src = "(X|[] (A| a) (B| b) (C| c\) (D| d))"
    tgt = "(X|[] (C|\ a b c\) (D| d))"
    src = ParentedTree.fromstring(src)
    tgt = ParentedTree.fromstring(tgt)
    res = th.reduce(src)
    assert tgt == res

    src = "(X|[] (A| a) (B| b) (C| c) (D| d))"
    tgt = "(X|[] (D| a b c d))"
    src = ParentedTree.fromstring(src)
    tgt = ParentedTree.fromstring(tgt)
    res = th.reduce(src)
    assert tgt == res

    src = "(X|[] (A| a) (B| b\) (C| c) (D| d))"
    src = ParentedTree.fromstring(src)
    tgt = "(X|[] (B|\ a b\) (D| c d))"
    tgt = ParentedTree.fromstring(tgt)
    res = th.reduce(src)
    assert tgt == res

def test_lapse():
    src = "(X|[] (C|\ a b c\) (D| d))"
    tgt = "(X|[] (C|[]\ a b c\) (D|[] d))"
    src = ParentedTree.fromstring(src)
    tgt = ParentedTree.fromstring(tgt)
    res = th.lapse(src)
    assert tgt == res
    #
    src = "(X|[] (D| a b c d))"
    tgt = "(X|[] (D|[] a b c d))"
    src = ParentedTree.fromstring(src)
    tgt = ParentedTree.fromstring(tgt)
    res = th.lapse(src)
    assert tgt == res
    #
    src = "(X|[] (B|\ a b\) (D| c d))"
    tgt = "(X|[] (B|[]\ a b\) (D|[] c d))"
    src = ParentedTree.fromstring(src)
    tgt = ParentedTree.fromstring(tgt)
    res = th.lapse(src)
    assert tgt == res

def test_flatten():
    src = "(X|[] (C|[]\ a b c\) (D|[] d))"
    tgt = "(X|[] (C|[]\ a b c\) (D|[] d))"
    src = ParentedTree.fromstring(src)
    tgt = ParentedTree.fromstring(tgt)
    res = th.flatten(src)
    assert tgt == res
    #
    src = "(X|[] (D|[] a b c d))"
    tgt = "(D|[] a b c d)"
    src = ParentedTree.fromstring(src)
    tgt = ParentedTree.fromstring(tgt)
    res = th.flatten(src)
    assert tgt == res
    #
    src = "(X|[] (B|[]\ a b\) (D|[] c d))"
    tgt = "(X|[] (B|[]\ a b\) (D|[] c d))"
    src = ParentedTree.fromstring(src)
    tgt = ParentedTree.fromstring(tgt)
    res = th.flatten(src)
    assert tgt == res


# def test_apply_constraints():
#     src = """
#     (IP-MAT|{}
#         (PP|[] (D s o n o) (N k o k u o \ o n i w a))
#         (PP-SBJ|[] (PP f U t a r i \ n o) (N o \ o j i g a))
#         (VP|[] a r i m a \ sh I t a)
#         (PU .))
#     """
#     tgt = """
#     (IP-MAT|{}
#         (PP|[] s o n o k o k u o \ o n i w a)
#         (PP-SBJ|[] (PP|[] f U t a r i \ n o) (N|[] o \ o j i g a))
#         (VP|[] a r i m a \ sh I t a)
#         (PU .))
#     """
#     src = ParentedTree.fromstring(src)
#     tgt = ParentedTree.fromstring(tgt).__str__()
#     res = th.apply_constraints(src).__str__()
#     assert tgt == res
#
