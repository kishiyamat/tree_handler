# %%
from copy import deepcopy
from typing import Any

from nltk.tree import ParentedTree

# %%


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

    @staticmethod
    def is_key_pos(tree, key_pos) -> bool:
        if isinstance(tree, str):  # leaf node
            return False
        if tree.label() == key_pos:
            return True
        return False


th = TreeHandler()
