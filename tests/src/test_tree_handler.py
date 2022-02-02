# %%
from nltk.tree import ParentedTree
from src.tree_handler import TreeHandler


def test_test():
    assert True
# %%
input_0: str = "その国王には二人の王子がありました。"

# #Numberは形態素ID
# \はアクセント記号
# invalid escape sequence になる
# ojt_out_0: str = "#0 s o n o #1 k o k u o \ o #2 n i #3 w a #4 f U t a r i \ # 5 n o #6 o \ o j i #7 g a #8 a r i #9 m a \ sh I #10 t a #11."
haruniwa2_out_0: str = """
( (IP-MAT (PP (NP (D その)
                  (N 国王))
              (P-ROLE に)
              (P-OPTR は))
          (PP-SBJ (NP (PP (NP (N 二人))
                          (P-ROLE の))
                      (N 王子))
                  (P-ROLE が))
          (VB あり)
          (AX まし)
          (AXD た)
          (PU 。))
  (ID 1_ex1640391709;JP))
"""

haruniwa2_out_0_2: str = """
( (IP-MAT (PP-SBJ-2 (NP (PP (NP (N 二人))
                          (P-ROLE の))
                      (N 王子))
                  (P-ROLE が))
          (PP (NP (D その)
                  (N 国王))
              (P-ROLE に)
              (P-OPTR は))
          (VB あり)
          (AX まし)
          (AXD た)
          (PU 。))
  (ID 1_ex1640391709;JP))
"""
haruniwa2_tree_0 = ParentedTree.fromstring(haruniwa2_out_0)
haruniwa2_tree_0.pretty_print()

tree_0 = ParentedTree.fromstring(haruniwa2_out_0)
tree_0.pretty_print()
assert 1 == 1

# %%
print("## 2. create VP nodes")
tree_i = ParentedTree.fromstring(haruniwa2_out_0_2)


tree_i.pretty_print()
# wrap_siblings(tree_i).pretty_print()

th = TreeHandler()
th.assign_morph(tree_0).pretty_print()
