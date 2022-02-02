# %%
from nltk.tree import ParentedTree

input_0: str = "その国王には二人の王子がありました。"
# #Numberは形態素ID
# \はアクセント記号
ojt_out_0: str = "#0 s o n o #1 k o k u o \ o #2 n i #3 w a #4 f U t a r i \ # 5 n o #6 o \ o j i #7 g a #8 a r i #9 m a \ sh I #10 t a #11."
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
# TODO: こういうケースにもたいおうしないとならない
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
# %%
print("## 1. assign morpheme IDs  to terminal nodes")


class TreeHandler:
    def __init__(self):
        pass

    def assign_morph(self, tree: ParentedTree) -> ParentedTree:
        morph_idx = 0
        for subtree_idx in tree.treepositions():  # tree を上から順番に走査
            subtree = tree[subtree_idx]
            if isinstance(subtree, str):  # leaveなら
                # FIXME: not_morph_list の外部参照を修正
                if subtree in self.not_morph_list:  # *等なら無視
                    continue
                # ## 1. assign morpheme IDs  to terminal nodes
                tree[subtree_idx] = f"#{morph_idx}-" + tree[subtree_idx]
                morph_idx += 1
        return tree

    @property
    def not_morph_list(self):
        not_morph = """
    *
    *T*
    *exp*
    *arb*
    *pro*
    *hearer*
    *hearer+pro*
    *speaker*
    *speaker+hearer*
    *speaker+pro*
    *ICH*
    """
        return not_morph.split()


th = TreeHandler()
th.assign_morph(tree_0).pretty_print()
# %%
print("## 2. create VP nodes")
tree_i = ParentedTree.fromstring(haruniwa2_out_0_2)


def is_kwey_pos(tree, key_pos) -> bool:
    if isinstance(tree, str):  # leaf node
        return False
    if tree.label() == key_pos:
        return True
    return False


def wrap_siblings(tree: ParentedTree = None,
                  key_pos: str = "VB",
                  wrap_pos: str = "VP",
                  left_pos: str = "SBJ",
                  right_pos: str = "PU",
                  ignore: str = "PU",
                  ) -> ParentedTree:
    """
    tree から key_pos を見つけて wrap_pos でラップする
    その際、ingnore はラップの両端から除外する
    """
    for subtree_idx in tree.treepositions():
        if not is_kwey_pos(tree[subtree_idx], key_pos):  # leaf node
            continue
        print("VB")
        key_pos_idx = subtree_idx[-1]
        parent_idx = list(subtree_idx[:-1])
        if tree[parent_idx].label() == "VP":
            continue
        # set left and right idx
        left_idx, right_idx = 0, len(tree[parent_idx])
        for idx, t in enumerate(tree[parent_idx]):
            if idx < key_pos_idx and left_pos in t.label():
                left_idx = idx + 1
            if key_pos_idx < idx and right_pos in t.label():
                right_idx = idx
        new_node = ParentedTree.fromstring(f'({wrap_pos})')
        tree[parent_idx].insert(left_idx, new_node)
        for pop_idx in range(left_idx, right_idx):
            # TODO: ignore を無視
            hoge = tree[parent_idx].pop(left_idx+1)
            tree[parent_idx + [left_idx]].insert(pop_idx-left_idx, hoge)
        break
    return tree


# だめだ、whileで回した方が絶対にはやい
tree_i.pretty_print()
wrap_siblings(tree_i).pretty_print()
# %%

# %%
