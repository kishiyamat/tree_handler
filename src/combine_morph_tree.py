from nltk.tree import ParentedTree
import sys
import pytest

from tree_handler import TreeHandler

th = TreeHandler()


def main():
    """
    $ python src/combine_morph_tree.py data/sample00.mph data/sample00.psd
        arg1: morph file (.mph)
        arg2: parsed tree file (.psd)
    """
    with open(sys.argv[1], "r") as f:
        morph_str = f.read()
    with open(sys.argv[2], "r") as f:
        tree_str = f.read()

    print(th.workflow(morph_str, tree_str))


if __name__ == "__main__":
    main()
