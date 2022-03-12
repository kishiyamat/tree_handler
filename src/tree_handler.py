# %%
from copy import deepcopy
from typing import Any

from nltk.tree import ParentedTree


class TreeHandler:
    def __init__(self):
        self.alinged_np_list = []
        self.morph_symbol = "#"
        self.morph_bind = "="
        self.type_given = "|"
        self.i_type = "{}"
        self.p_type = "[]"
        self.n_type = ""  # iやpとことなり()は""で表現
        self.phoneme_split = " "
        self.phoneme_bind = "_"
        self._symbol_list_half = ",.()[]?!"
        self._symbol_list_full = "、。（）「」？！"
        self.symbol_list = self._symbol_list_half + self._symbol_list_full

    def assign_morph(self, tree: ParentedTree) -> ParentedTree:
        # symbol_list は morph に含めない.
        # inf2の結果のmphで.や,を無視するため
        # cf. https://github.com/kishiyamat/tree_handler/pull/60
        tree = deepcopy(tree)
        morph_idx = 0
        for subtree_idx in tree.treepositions():  # tree を上から順番に走査
            subtree = tree[subtree_idx]
            if isinstance(subtree, str):  # leaveなら
                if subtree in self.not_morph_list:  # *等なら無視
                    continue
                if subtree in self.symbol_list:  # *等なら無視
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

    def create_vp_node(
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
                right_pos = tree[parent_idx+[key_pos_idx+1]].label()
                if right_pos[:2] != "P-":
                    # このケースはNP--P-ROLEではないので対象外
                    continue
                else:
                    return False
            except IndexError:
                # すでにNPの右隣は存在しない場合は続ける
                continue
        return True

    def align_np(self, tree: ParentedTree) -> ParentedTree:
        tree = deepcopy(tree)
        counter = 0
        while not self.all_align_np(tree):
            tree = self._align_np(tree)
            counter += 1
            if counter > 10000:  # inf loop 対策
                raise ValueError("reached max")
        return tree

    def _align_np(self, tree: ParentedTree) -> ParentedTree:
        for subtree_idx in tree.treepositions():
            if not self.is_key_pos(tree[subtree_idx], "NP"):  # leaf node
                continue
            key_pos_idx = subtree_idx[-1]  # NPの位置
            parent_idx = list(subtree_idx[:-1])
            try:
                # popしたparticleに0は必ず存在する. 例: (P-ROLE が)
                right_pos = tree[parent_idx+[key_pos_idx+1]].label()
                if right_pos[:2] != "P-":
                    continue
                else:  # NPの後ろにP-ROLEなどがある場合
                    particle_leaf = tree[parent_idx].pop(key_pos_idx+1)[0]
            except IndexError:
                # すでにNPの右隣は存在しない場合は続ける
                continue
            # NPの一番最後[-1]は葉っぱで、その上[:-1]がNのidx
            n_idx = tree[subtree_idx].treepositions()[-1][:-1]
            # Nの下に何この要素があるか(すでにくっついている場合がある)
            len_n = len(tree[list(subtree_idx) + [n_idx]])
            tree[list(subtree_idx) + [n_idx]].insert(len_n, particle_leaf)
            break
        return tree

    def _align_vp(self, tree: ParentedTree) -> ParentedTree:
        # 全てのVPがVBを含むことを保証
        # TODO: add test
        if not self.all_wrapped(tree, "VB", "VP"):
            raise ValueError("There's a VP that doesn't dominate VB.")
        for subtree_idx in tree.treepositions():
            if not self.is_key_pos(tree[subtree_idx], "VB"):  # leaf node
                continue
            key_pos_idx = subtree_idx[-1]  # sister内でのVB位置
            parent_idx = list(subtree_idx[:-1])
            try:
                # 右がPUなら continue
                right_pos = tree[parent_idx+[key_pos_idx+1]].label()
                if right_pos[:2] == "PU":
                    continue
                # 右がPOSじゃない(最初の子[0]がstrじゃない)ならcontinue
                if not isinstance(tree[parent_idx+[key_pos_idx+1]][0], str):
                    continue
                # 右が葉っぱじゃないならcontinue
                # 右隣のノードの葉っぱをpopして、さらにleafを取る
                leaf = tree[parent_idx].pop(key_pos_idx+1)[0]
                tree[subtree_idx].insert(len(tree[subtree_idx]), leaf)
            except IndexError:
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
                # 右がPUなら continue
                right_pos = tree[parent_idx+[key_pos_idx+1]].label()
                if right_pos[:2] == "PU":
                    continue
                # 右がPOSじゃない(最初の子[0]がstrじゃない)ならcontinue
                if not isinstance(tree[parent_idx+[key_pos_idx+1]][0], str):
                    continue
                # 右が葉っぱじゃないならcontinue
                # 親(VP)の隣を参照できるなら存在する
                _ = tree[[parent_idx] + [key_pos_idx+1]]
                return False
            except IndexError:
                # すでにNPの右隣は存在しない場合は続ける
                continue
        return True

    def align_vp(self, tree: ParentedTree) -> ParentedTree:
        tree = deepcopy(tree)
        counter = 0
        while not self.all_align_vp(tree):
            tree = self._align_vp(tree)
            counter += 1
            if counter > 10000:  # inf loop 対策
                raise ValueError("reached max")
        return tree

    def align_p_words(self, tree: ParentedTree) -> ParentedTree:
        tree = deepcopy(tree)
        return self.align_vp(self.align_np(tree))

    def integrate_morph_accent(self, tree: ParentedTree, idx_accent) -> ParentedTree:
        # PUならそのまま
        idx_accent = idx_accent.strip()
        idx_accent = list(filter(len, idx_accent.split(self.morph_symbol)))
        idx_accent_wo_pu = list(map(self.split_idx_accent, idx_accent))
        tree = deepcopy(tree)
        morph_idx = 0
        for subtree_idx in tree.treepositions():  # tree を上から順番に走査
            subtree = tree[subtree_idx]
            if isinstance(subtree, str):  # leaveなら
                if subtree in self.not_morph_list:  # *等なら無視
                    continue
                if subtree in self.symbol_list:
                    continue
                idx, accent = idx_accent_wo_pu[morph_idx]
                if morph_idx != idx:
                    raise IndexError("The morph idx is not compatible!")
                # ## 1. assign morpheme IDs  to terminal nodes
                # もしかしたら=と_でつないだほうが早いかも
                tree[subtree_idx] = self.phoneme_bind\
                    .join(accent.split(self.phoneme_split))
                morph_idx += 1
        # わかりづらいが、morph_idxをcountupしてtreeのインデックスをgetしている
        # FIXME: 一旦、ここは中断
        if morph_idx != len(idx_accent_wo_pu):
            raise IndexError(f"tree:morph={morph_idx}:{len(idx_accent_wo_pu)}")
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
            _type_: 編集されるべき木ならTrue
        """
        for subtree_idx in tree.treepositions():  # tree を上から順番に走査
            subtree = tree[subtree_idx]
            if isinstance(subtree, str):  # leaveは無視
                continue
            if len(subtree) == 0:
                continue
            if subtree[0] in self.not_morph_list:
                subtree.parent().pop(subtree_idx[-1])
                return True  # 編集されるべき条件
            if subtree.parent() == None:  # topは無視.
                # FIXME: トップはredundunt でないことを仮定している
                continue
            if subtree.label().split(self.type_given)[-1] == self.p_type:
                continue  # []: pは無視
            if len(subtree.parent()) == 1:  # 親が[]でなく、sisterが1なら冗長
                return True  # 編集されるべき条件
            # TODO: こどもがleafかつproなど -> return True
        return False

    def remove_redunduncy(self, tree: ParentedTree) -> ParentedTree:
        tree = deepcopy(tree)
        while self.is_redundunt(tree):
            for subtree_idx in tree.treepositions():  # tree を上から順番に走査
                subtree = tree[subtree_idx]
                if isinstance(subtree, str):
                    continue
                if len(subtree) == 0:
                    return tree
                if subtree[0] in self.not_morph_list:
                    subtree.parent().pop(subtree_idx[-1])
                    break  # 編集したら0から is_redunduntである限りやり直す
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
        # ここ 1:: となっていたが...
        return (int(str_split[0]), " ".join(str_split[1:]))

    @staticmethod
    def is_key_pos(tree, key_pos) -> bool:
        if isinstance(tree, str):  # leaf node
            return False
        if tree.label() == key_pos:
            return True
        return False

    def workflow(self, OpenJTalk: str, Haruniwa2: str):
        src, src_1 = ParentedTree.fromstring(Haruniwa2), OpenJTalk
        src = self.remove_outmost_id(src)
        src = self.create_vp_node(src)
        src = self.add_phrase_type(src)
        src = self.align_p_words(src)
        src = self.integrate_morph_accent(src, src_1)
        src = self.remove_redunduncy(src)
        src = self.apply_constraints(src)
        src = self.to_line(src)
        return src

    def assign_bar(self, tree):
        tree = deepcopy(tree)
        for subtree_idx in tree.treepositions():
            subtree = tree[subtree_idx]
            if isinstance(subtree, str):
                continue
            if "|" not in subtree.label():
                subtree.set_label(subtree.label()+"|")
        return tree

    def percolate(self, tree):
        tree = deepcopy(tree)
        # assign_bar -> parcolate にしないと pos の種類が合わない
        # ここ、なぜか0にleaveが来ているひっくり返ってる
        for subtree_idx in tree.treepositions():
            subtree = tree[subtree_idx]
            if isinstance(subtree, str):  # not pos
                continue
            if not isinstance(subtree[0], str):  # not pos
                continue
            if "\\" in "".join(subtree):
                subtree.set_label(subtree.label()+"\\")
        return tree

    def is_reduced_1(self, tree):
        tree = deepcopy(tree)
        pos_list = [t[1] for t in tree.pos()]
        for subtree_idx in tree.treepositions():
            subtree = tree[subtree_idx]
            if isinstance(subtree, str):
                continue
            if subtree.label() in pos_list:
                # posレベルまで下がると、下が葉っぱになってしまう。
                continue
            n_sisters = len(subtree)
            for i in range(n_sisters-1):
                # とりあえず pos のみを統合
                if not (isinstance(subtree[i][0], str) and isinstance(subtree[i+1][0], str)):
                    continue
                left = subtree[i].label().split("|")[1]
                right = subtree[i+1].label().split("|")[1]
                if left == "" and right == "":
                    return False
        return True

    def _reduce_1(self, tree):
        # reduce_1: (a)＊→(a＊)  # この時点で存在するすべての（）は一つになる
        tree = deepcopy(tree)
        pos_list = [t[1] for t in tree.pos()]
        for subtree_idx in tree.treepositions():
            subtree = tree[subtree_idx]
            if isinstance(subtree, str):
                continue
            if subtree.label() in pos_list:
                # posレベルまで下がると、下が葉っぱになってしまう。
                continue
            n_sisters = len(subtree)
            for i in range(n_sisters-1):
                if not (isinstance(subtree[i][0], str) and isinstance(subtree[i+1][0], str)):
                    continue
                left = subtree[i].label().split("|")[1]
                right = subtree[i+1].label().split("|")[1]
                if left == "" and right == "":
                    # leavesになってない
                    leaves = subtree.pop(i)
                    leaves.reverse()
                    # iをpopしたからiに挿入できる
                    _ = [subtree[i].insert(0, leaf) for leaf in leaves]
                    # _ = [subtree[i].insert(0, leaf) for leaf in leaves]
                    return tree

    def is_reduced_2(self, tree):
        tree = deepcopy(tree)
        pos_list = [t[1] for t in tree.pos()]
        for subtree_idx in tree.treepositions():
            subtree = tree[subtree_idx]
            if isinstance(subtree, str):
                continue
            if subtree.label() in pos_list:
                # posレベルまで下がると、下が葉っぱになってしまう。
                continue
            n_sisters = len(subtree)
            for i in range(n_sisters-1):
                if not (isinstance(subtree[i][0], str) and isinstance(subtree[i+1][0], str)):
                    continue
                left = subtree[i].label().split("|")[1]
                right = subtree[i+1].label().split("|")[1]
                if left == "" and right == "\\":
                    return False
        return True

    def _reduce_2(self, tree):
        # reduce_2: (a)(b\)->(a b\)
        tree = deepcopy(tree)
        pos_list = [t[1] for t in tree.pos()]
        for subtree_idx in tree.treepositions():
            subtree = tree[subtree_idx]
            if isinstance(subtree, str):
                continue
            if subtree.label() in pos_list:
                # posレベルまで下がると、下が葉っぱになってしまう。
                continue
            n_sisters = len(subtree)
            for i in range(n_sisters-1):
                # 対象は (POS leaf) 間の関係(両方、子がstr)
                if not (isinstance(subtree[i][0], str) and isinstance(subtree[i+1][0], str)):
                    continue
                left = subtree[i].label().split("|")[1]
                right = subtree[i+1].label().split("|")[1]
                if left == "" and right == "\\":
                    leaves = subtree.pop(i)
                    leaves.reverse()
                    # iをpopしたからiに挿入できる
                    for leaf in leaves:
                        subtree[i].insert(0, leaf)
                    return tree

    def reduce(self, tree: ParentedTree) -> ParentedTree:
        tree = deepcopy(tree)
        tree = self.percolate(self.assign_bar(tree))
        while not self.is_reduced_1(tree):
            tree = self._reduce_1(tree)
        while not self.is_reduced_2(tree):
            tree = self._reduce_2(tree)
        return tree

    def lapse(self, tree):
        tree = deepcopy(tree)
        for subtree_idx in tree.treepositions():
            subtree = tree[subtree_idx]
            if isinstance(subtree, str):
                continue
            if not("[]" in subtree.label() or "{}" in subtree.label()):
                subtree.set_label(subtree.label().replace("|", "|[]"))
        return tree

    def is_flat(self, tree):
        tree = deepcopy(tree)
        for subtree_idx in tree.treepositions():
            subtree = tree[subtree_idx]
            if isinstance(subtree, str):
                continue
            if subtree.parent() == None:
                # IP−MATではない
                continue
            # 葉っぱとは限らない
            subtree_par = subtree.label().replace("\\", "").split("|")[1]
            parent_par = subtree.parent().label().replace(
                "\\", "").split("|")[1]
            if subtree_par != parent_par:  # []や{}が違う
                continue
            # 兄弟がいない(葉っぱかどうかは関係ない)
            if len(subtree.parent()) == 1:
                return False
        return True

    def _flatten(self, tree):
        # 潰す条件
        # 1. 葉っぱではない
        # 1. IP−MATではない
        # 1. []や{}が同じ. ""なら潰す
        # 1. 兄弟がいない
        tree = deepcopy(tree)
        for subtree_idx in tree.treepositions():
            subtree = tree[subtree_idx]
            if isinstance(subtree, str):  # 葉っぱ
                continue
            if subtree.parent() == None:  # IP−MAT
                continue
            # 葉っぱとは限らない
            subtree_par = subtree.label().replace("\\", "").split("|")[1]
            parent_par = subtree.parent().label().replace(
                "\\", "").split("|")[1]
            if subtree_par != parent_par:  # []や{}が違う
                continue
            if len(subtree.parent()) == 1:  # 兄弟がいない
                if isinstance(subtree[0], str):  # 葉っぱ
                    subtree.parent().set_label(subtree.label())
                    leaves = [x for x in subtree]
                    leaves.reverse()
                    [subtree.parent().insert(0, x) for x in leaves]
                    subtree.parent().pop(-1)
                    return tree
                else:  # 葉っぱ以外
                    subtree.parent().set_label(subtree.label())
                    trees = [subtree.pop(0) for i in range(len(subtree))]
                    [subtree.parent().insert(-1, t_i)for t_i in trees]
                    subtree.parent().pop(-1)
                    return tree

    def flatten(self, tree):
        tree = deepcopy(tree)
        while not self.is_flat(tree):
            tree = self._flatten(tree)
        return tree

    def apply_constraints(self, tree):
        # 1. reduce_1: (a)＊→(a＊)  # この時点で存在するすべての（）は一つになる
        # 1. reduce_2: (a)(b\)→(a b\)  #
        # 2. lapse: (＊) -> [＊]
        # 3. flatten: [[＊]] -> [＊]
        tree = deepcopy(tree)
        tree = self.reduce(tree)
        tree = self.lapse(tree)
        tree = self.flatten(tree)
        return tree

    def to_line(self, tree, adhoc_list=[".", ",", "“"]):
        tree = deepcopy(tree)
        out = ""
        stack = []
        nest_prev = -1
        for subtree_idx in tree.treepositions():
            nest_level = len(subtree_idx)
            if nest_level < nest_prev:
                # 上に戻った場合、その分stackをpopさせる
                # FIXME: 本当はleavesも1下がって1登る、という一般化ができる
                n_back = range(nest_prev - nest_level)
                out += " " + " ".join([stack.pop()
                                      for _ in n_back])  # 直近をpopする
            subtree = tree[subtree_idx]
            if isinstance(subtree, str):
                continue
            symbol = subtree.label().replace("\\", "").split("|")[1]
            out += " " + symbol[0]  # 必ずノードには[]か{}がある
            stack.append(symbol[1])
            if isinstance(subtree[0], str):  # 前終端
                out += " " + " ".join(subtree)
                out += " " + stack.pop()  # 直近をpopする
            nest_prev = len(subtree_idx)
        out += " " + stack.pop()
        for adhoc in adhoc_list:
            out = out.replace(f"[ {adhoc} ]", adhoc)
        out = out.strip()
        # FIXME: 出力で"_"がたされる. おそらく前の方の処理で_を足している
        out = out.replace("_", " ")
        return out


# WONTFIX
# DONE
# WIP
tgt_id = ""  # reduce_1起因
# PATH
error_type = "error_*"  # エラータイプ
debug = 0

if debug:
    import sys
    sys.path.append('..')
    from prog.inf2model1 import InfParser

    tgt_inf_path = f"../tests/data/{error_type}/{tgt_id}.inf2"
    tgt_psd_path = f"../tests/data/{error_type}/{tgt_id}.psd"

    with open(tgt_inf_path, "r") as f:
        l_strip = [s.strip() for s in f.readlines()]  # readlines and remove \n
        tgt_inf_str = list(filter(len, l_strip))  # filter zero-length str: ""
        parser = InfParser(2)
        tgt_morph = parser.inf2txt(tgt_inf_str)

    th = TreeHandler()

    with open(tgt_psd_path, "r") as f:
        tree_str = f.read()
        # out = th.workflow(tgt_morph, tree_str)

    tree, src_1 = ParentedTree.fromstring(tree_str), tgt_morph
    tree = th.remove_outmost_id(tree)
    tree = th.create_vp_node(tree)
    tree = th.add_phrase_type(tree)
    print(tree)
    tree = th.align_p_words(tree)
    tree = th.integrate_morph_accent(tree, src_1)
    tree = th.remove_redunduncy(tree)
    tree = th.reduce(tree)
    print(tree)
    tree = th.apply_constraints(tree)
    tree = th.to_line(tree)
    print(tree)
# %%

# %%
