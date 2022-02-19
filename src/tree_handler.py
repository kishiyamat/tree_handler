# %%
from copy import deepcopy
from typing import Any

from nltk.tree import ParentedTree

# %%


class TreeHandler:
    def __init__(self):
        self.alinged_np_list = []
        self.morph_symbol = "#"
        self.type_given = "|"
        self.i_type = "{}"
        self.p_type = "[]"

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

    def all_wrapped(self, tree: ParentedTree, key_pos: str, wrap_pos: str) -> bool:
        for subtree_idx in tree.treepositions():
            if not self.is_key_pos(tree[subtree_idx], key_pos):  # leaf node
                continue
            parent_idx = list(subtree_idx[:-1])
            if tree[parent_idx].label()[:2] != wrap_pos:
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

    def all_align_np(self, tree: ParentedTree) -> ParentedTree:
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

    def align_np(self, tree: ParentedTree) -> ParentedTree:
        tree = deepcopy(tree)
        while not self.all_align_np(tree):
            tree = self._align_np(tree)
        return tree

    def _align_np(self, tree: ParentedTree) -> ParentedTree:
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

    def _align_vp(self, tree: ParentedTree) -> ParentedTree:
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

    def all_align_vp(self, tree: ParentedTree) -> bool:
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

    def align_vp(self, tree: ParentedTree) -> ParentedTree:
        tree = deepcopy(tree)
        while not self.all_align_vp(tree):
            tree = self._align_vp(tree)
        return tree

    def align_p_words(self, tree: ParentedTree) -> ParentedTree:
        tree = deepcopy(tree)
        return self.align_vp(self.align_np(tree))

    def integrate_morph_accent(self, tree: ParentedTree, idx_accent) -> ParentedTree:
        idx_accent = filter(len, idx_accent.split(self.morph_symbol))
        idx_accent = list(map(self.split_idx_accent, idx_accent))
        # TODO: flattenを検討
        tree = deepcopy(tree)
        morph_idx = 0
        for subtree_idx in tree.treepositions():  # tree を上から順番に走査
            subtree = tree[subtree_idx]
            if isinstance(subtree, str):  # leaveなら
                if subtree in self.not_morph_list:  # *等なら無視
                    continue
                idx, accent = idx_accent[morph_idx]
                if morph_idx != idx:
                    raise IndexError("The morph idx is not compatible!")
                # ## 1. assign morpheme IDs  to terminal nodes
                tree[subtree_idx] = accent
                morph_idx += 1
        return tree

    def p_conditional_operation(self, subtree: ParentedTree) -> ParentedTree:
        if isinstance(subtree, str):  # leaf node
            return subtree
        if subtree.label() == "VP":
            subtree.set_label(subtree.label()+self.type_given+self.p_type)
            return subtree
        if "PP" not in subtree.label()[:2]:
            return subtree
        if not "P-" in subtree[-1].label():
            return subtree
        if "の" in subtree[-1][0]:
            return subtree
        subtree.set_label(subtree.label()+self.type_given+self.p_type)
        return subtree

    def i_conditional_operation(self, subtree: ParentedTree) -> ParentedTree:
        # 親がCP*でない、子にADJ*を持たないすべてのIPを{}にする
        if isinstance(subtree, str):  # leaf node
            return subtree
        if subtree.parent() != None:
            if "CP-" in subtree.parent().label():  # 親がCP
                return subtree
        if not "IP-" in subtree.label():  # そもそもIPじゃない
            return subtree
        if sum(["ADJ" in st_i.label() for st_i in subtree]):  # 子のラベルがADJが含む
            return subtree
        subtree.set_label(subtree.label()+self.type_given+self.i_type)
        return subtree

    def cp_conditional_operation(self, subtree: ParentedTree) -> ParentedTree:
        # 子がIPであるCPを{}にする
        # i_conditional_opereationより、cpとiが両方{}になることはない
        if isinstance(subtree, str):  # leaf node
            return subtree
        if not "CP-" in subtree.label():  # 自身がCPでない
            return subtree
        if not sum(["IP-" in st_i.label() for st_i in subtree]):  # 子のラベルがIPが含まない
            return subtree
        # 自身がCPであり、子にIPがある。
        subtree.set_label(subtree.label()+self.type_given+self.i_type)
        return subtree

    def add_phrase_type(self, tree: ParentedTree) -> ParentedTree:
        """_summary_
            See: https://github.com/kishiyamat/tree_handler/issues/4

        Args:
            tree (_type_): _description_

        Returns:
            _type_: _description_
        """
        tree = deepcopy(tree)
        for subtree_idx in tree.treepositions():
            subtree = tree[subtree_idx]
            # 一つのsubtreeに対して複数の操作
            subtree = self.p_conditional_operation(subtree)
            subtree = self.cp_conditional_operation(subtree)
            subtree = self.i_conditional_operation(subtree)
        return tree

    def remove_outmost_id(self, tree: ParentedTree) -> ParentedTree:
        """Treeの最上階は0に本体、1にIDがいる。そこで
            0を返せばIDを飛ばせる

        Args:
            tree (_type_): _description_

        Raises:
            ValueError: _description_

        Returns:
            _type_: _description_
        """
        if tree[-1].label() != "ID":
            # そもそもIDが存在しなくて長さが1の場合もある
            raise ValueError("The input doesn't have ID node.")
        return tree[0]

    def is_redundunt(self, tree: ParentedTree) -> bool:
        """_summary_
            以下のLHSは冗長
            [ ( ) ] →[     ]
            ( ( ) ) →(     )
            (空白) → 削除
            # 以下は非冗長
            [ [ ] ] →[ [ ] ]  # current が[]なら飛ばす
        Args:
            tree (_type_): _description_

        Returns:
            _type_: _description_
        """
        for subtree_idx in tree.treepositions():  # tree を上から順番に走査
            subtree = tree[subtree_idx]
            if isinstance(subtree, str):  # leaveは無視
                continue
            if subtree.parent() == None:  # topは無視.
                # FIXME: トップはredundunt でないことを仮定している
                continue
            if subtree.label().split(self.type_given)[-1] == self.p_type:
                continue  # []: pは無視
            if len(subtree.parent()) == 1:  # 親が[]でなく、sisterが1なら冗長
                return True
            # TODO: こどもがleafかつproなど -> return True
        return False

    def remove_redunduncy(self, tree: ParentedTree) -> ParentedTree:
        tree = deepcopy(tree)
        while self.is_redundunt(tree):
            for subtree_idx in tree.treepositions():  # tree を上から順番に走査
                if isinstance(tree[subtree_idx], str):
                    continue
                subtree = tree[subtree_idx]
                if subtree.parent() == None:
                    # FIXME: 親がいないケースを握りつぶしている
                    continue
                if subtree.label().split(self.type_given)[-1] == self.p_type:
                    continue
                if len(subtree.parent()) == 1:
                    for _ in range(len(subtree)):
                        subtree.parent().insert(0, subtree.pop())
                    subtree.parent().pop()
                    break  # 編集したら0から is_redunduntである限りやり直す
        return tree

    @staticmethod
    def split_idx_accent(str_row) -> tuple:
        str_split = str_row.split()
        return (int(str_split[0]), " ".join(str_split[1::]))

    @staticmethod
    def is_key_pos(tree, key_pos) -> bool:
        if isinstance(tree, str):  # leaf node
            return False
        if tree.label() == key_pos:
            return True
        return False


# %%
# workflow
# wrap_siblings で VP作成
# assign-phrase IPとPP、VPに情報をつける
th = TreeHandler()

# %%
src = """
    (IP-MAT
        (PP (NP (D #0その) (N #1国王)) (P-ROLE #2に) (P-OPTR #3は))
        (PP-SBJ (NP (PP (NP (N #4二人)) (P-ROLE #5の)) (N #6王子)) (P-ROLE #7が))
        (VP (VB #8あり) (AX #9まし) (AXD #10た))
        (PU #11。))
    """
src = ParentedTree.fromstring(src)
src.pretty_print()
src = th.add_phrase_type(src)
src.pretty_print()
src = th.align_p_words(src)
src_accent = """#0 s o n o #1 k o k u o \ o #2 n i #3 w a 
            #4 f U t a r i \ #5 n o #6 o \ o j i #7 g a
            #8 a r i #9 m a \ sh I #10 t a #11 ."""
src = th.integrate_morph_accent(src, src_accent)
src = th.remove_redunduncy(src)
src.pretty_print()
# %%
'hello'[-2:]
# %%
