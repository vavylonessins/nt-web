from ntml.ntml_parser import *
from ntml.tran import *
import sys


def compile(ntml: str|bytes) -> str:
    tree = ntml_parser.parse(ntml)
    tran = Tran(tree)
    tran.walk_tree()
    return tran.to_html()

def ntml_imports(ntml: str|bytes) -> str:
    tree = ntml_parser.parse(ntml)
    tran = Tran(tree)
    tran.walk_tree()
    return tran.imports


if __name__ == '__main__':
    with open(sys.argv[-2], "rt") as f:
        tree = ntml_parser.parse(f.read())

    tran = Tran(tree)

    tran.walk_tree()

    with open(sys.argv[-1], "wt") as out:
        print(tran.to_html(), file=out, flush=True)
