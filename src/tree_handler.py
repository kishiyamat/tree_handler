# %%
from ast import Index
from copy import deepcopy
from typing import Any

from nltk.tree import ParentedTree

# %%


class TreeHandler:
    def __init__(self):
        self.alinged_np_list = []
        self.morph_symbol = "#"

    def assign_morph(self, tree: ParentedTree) -> ParentedTree:
        tree = deepcopy(tree)
        morph_idx = 0
        for subtree_idx in tree.treepositions():  # tree を上から順番に走査
            subtree = tree[subtree_idx]
            if isinstance(subtree, str):  # leaveなら
                if subtree in self.not_morph_list:  # *等なら無視
                    continue
                # ## 1. assign morpheme IDs  to terminal nodes
                tree[subtree_idx] = f"{self.morph_symbol}{morph_idx}-{tree[subtree_idx]}"
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

    def all_wrapped(self, tree, key_pos, wrap_pos):
        for subtree_idx in tree.treepositions():
            if not self.is_key_pos(tree[subtree_idx], key_pos):  # leaf node
                continue
            parent_idx = list(subtree_idx[:-1])
            if tree[parent_idx].label() != wrap_pos:
                return False
        return True

    def wrap_siblings(
        self,
        tree: ParentedTree = None,
        key_pos: str = "VB",
        wrap_pos: str = "VP",
        **kwags: Any,
    ) -> ParentedTree:
        tree = deepcopy(tree)
        while not self.all_wrapped(tree, key_pos, wrap_pos):
            tree = self._wrap_siblings(tree, key_pos, wrap_pos, **kwags)
        return tree

    def _wrap_siblings(
        self,
        tree: ParentedTree = None,
        key_pos: str = "VB",
        wrap_pos: str = "VP",
        left_pos: str = "SBJ",
        right_pos: str = "NONE",
        ignore: str = "PU",
    ) -> ParentedTree:
        """
        whileで回した方が実装が楽
        tree から key_pos を見つけて wrap_pos でラップする
        その際、ingnore はラップの両端から除外する
        """
        for subtree_idx in tree.treepositions():
            if not self.is_key_pos(tree[subtree_idx], key_pos):  # leaf node
                continue
            key_pos_idx = subtree_idx[-1]
            parent_idx = list(subtree_idx[:-1])
            if tree[parent_idx].label() == wrap_pos:
                continue
            # set left and right idx
            left_idx, right_idx = 0, len(tree[parent_idx])
            for idx, t in enumerate(tree[parent_idx]):
                if idx < key_pos_idx and left_pos in t.label():
                    left_idx = idx + 1
                if idx < key_pos_idx and ignore in t.label():
                    # 後ろに key_pos がくれば上書きされる
                    left_idx += 1
                if key_pos_idx < idx and right_pos in t.label():
                    right_idx = idx
                if key_pos_idx < idx and ignore in t.label():
                    # key_pos が後ろにくれば上書きされる
                    right_idx -= 1
            new_node = ParentedTree.fromstring(f'({wrap_pos})')
            tree[parent_idx].insert(left_idx, new_node)
            for pop_idx in range(left_idx, right_idx):
                # TODO: ignore を無視
                hoge = tree[parent_idx].pop(left_idx+1)
                tree[parent_idx + [left_idx]].insert(pop_idx-left_idx, hoge)
            break
        return tree

    def all_align_np(self, tree):
        for subtree_idx in tree.treepositions():
            if not self.is_key_pos(tree[subtree_idx], "NP"):  # leaf node
                continue
            key_pos_idx = subtree_idx[-1]
            parent_idx = list(subtree_idx[:-1])
            try:
                # 参照できるなら存在する
                _ = tree[[parent_idx] + [key_pos_idx+1]]
                return False
            except IndexError:
                # すでにNPの右隣は存在しない場合は続ける
                continue
        return True

    def align_np(self, tree):
        tree = deepcopy(tree)
        while not self.all_align_np(tree):
            tree = self._align_np(tree)
        return tree

    def _align_np(self, tree):
        for subtree_idx in tree.treepositions():
            if not self.is_key_pos(tree[subtree_idx], "NP"):  # leaf node
                continue
            key_pos_idx = subtree_idx[-1]  # NPの位置
            parent_idx = list(subtree_idx[:-1])
            try:
                # TODO: tryの幅を狭める
                # popしたparticleに0は必ず存在する. 例: (P-ROLE が)
                particle_leaf = tree[parent_idx].pop(key_pos_idx+1)[0]
                # NPの下のNのインデックス
                n_idx = len(tree[subtree_idx])-1
                # Nの下に何この要素があるか(すでにくっついている場合がある)
                len_n = len(tree[list(subtree_idx) + [n_idx]])
                tree[list(subtree_idx) + [n_idx]].insert(len_n, particle_leaf)
            except IndexError:
                # すでにNPの右隣は存在しない場合は続ける
                continue
            break
        return tree

    def _align_vp(self, tree):
        # 全てのVPがVBを含むことを保証
        # TODO: add test
        if not self.all_wrapped(tree, "VB", "VP"):
            tree.pretty_print()
            raise ValueError("There's a VP that doesn't dominate VB.")
        for subtree_idx in tree.treepositions():
            if not self.is_key_pos(tree[subtree_idx], "VB"):  # leaf node
                continue
            key_pos_idx = subtree_idx[-1]  # VBの位置
            parent_idx = list(subtree_idx[:-1])
            try:
                leaf = tree[parent_idx].pop(key_pos_idx+1)[0]
                # NPの下のNのインデックス
                n_idx = len(tree[subtree_idx])-1
                # Nの下に何この要素があるか(すでにくっついている場合がある)
                len_n = len(tree[list(subtree_idx) + [n_idx]])
                tree[subtree_idx].insert(len_n, leaf)
            except IndexError:
                # すでにVPの右隣は存在しない場合は続ける
                continue
            break
        return tree

    def all_align_vp(self, tree):
        for subtree_idx in tree.treepositions():
            if not self.is_key_pos(tree[subtree_idx], "VB"):  # leaf node
                continue
            key_pos_idx = subtree_idx[-1]
            parent_idx = list(subtree_idx[:-1])
            try:
                # 親(VP)の隣を参照できるなら存在する
                _ = tree[[parent_idx] + [key_pos_idx+1]]
                return False
            except IndexError:
                # すでにNPの右隣は存在しない場合は続ける
                continue
        return True

    def align_vp(self, tree):
        tree = deepcopy(tree)
        while not self.all_align_vp(tree):
            tree = self._align_vp(tree)
        return tree

    def align_p_words(self, tree):
        tree = deepcopy(tree)
        return self.align_vp(self.align_np(tree))

    @staticmethod
    def is_key_pos(tree, key_pos) -> bool:
        if isinstance(tree, str):  # leaf node
            return False
        if tree.label() == key_pos:
            return True
        return False


# %%
th = TreeHandler()
src_1 = "#0 k a \ n o #1 n e k o \  #2 w a #3 k i i r o i #4 m i ch i #5 o #6 a r u \ k u #7 i n u \  #8 o #9 y u k k u \ r i #10 m i \ #11 t a #12 y o \ o #13 da t  #14 t a  #15 r a sh i i #16 ."
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
      (PP-SBJ (NP (D k a \ n o) (N n e k o \ w a)))
      (VP
        (PP-OB1
          (NP
            (IP-REL
              (NP-SBJ *T*)
              (VP
                (PP-OB1
                  (NP
                    (IP-REL (NP-SBJ *T*) (ADJI k i i r o i))
                    (N m i ch i o)))
                (VB a r u \ k u)))
            (N i n u \ o)))
        (ADVP (ADV y u k k u \ r i))
        (VB m i \ t a y o \ o da t t a r a sh i i))
      (PU .))
    """
morph_symbol = "#"
idx_accent_gen = filter(len, src_1.split(morph_symbol))
src, tgt = ParentedTree.fromstring(src_2), ParentedTree.fromstring(tgt)


def split_idx_accent(str_row) -> tuple:
    str_split = str_row.split()
    return (int(str_split[0]), " ".join(str_split[1::]))


def integrate_morph_accent(tree, idx_accent):
    pass


idx_accent = list(map(split_idx_accent, idx_accent_gen))
[print(pitch) for _, pitch in idx_accent]

# %%
src.pretty_print()
# %%

def integrate_morph_accent(tree: ParentedTree, idx_accent) -> ParentedTree:
    tree = deepcopy(tree)
    morph_idx = 0
    for subtree_idx in tree.treepositions():  # tree を上から順番に走査
        subtree = tree[subtree_idx]
        if isinstance(subtree, str):  # leaveなら
            if subtree in th.not_morph_list:  # *等なら無視
                continue
            idx, accent = idx_accent[morph_idx]
            if morph_idx != idx:
                raise IndexError("The morph idx is not compatible!")
            # ## 1. assign morpheme IDs  to terminal nodes
            tree[subtree_idx] = accent
            morph_idx += 1
    return tree

# %%
tgt.pretty_print()
print(tgt.__str__())
# %%
res = integrate_morph_accent(src, idx_accent)
print(res.__str__())
# %%
tgt.__str__() == res.__str__()
# %%
