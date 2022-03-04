from nltk.tree import ParentedTree
import sys
import pytest

from tree_handler import TreeHandler

th = TreeHandler()


def main():
    """
    $ python src/combine_morph_tree.py sample00
    # $ python src/combine_morph_tree.py data/sample00.mph data/sample00.psd
        arg1: morph file (.mph)
        arg2: parsed tree file (.psd)
    """
    with open("mph/"+ sys.argv[1]+".mph", "r") as f:
        morph_str = f.read()
    with open("psd/"+ sys.argv[1]+".psd", "r") as f:
        tree_str = f.read()
    print(f"{sys.argv[1]} " + th.workflow(morph_str, tree_str))


if __name__ == "__main__":
    main()
