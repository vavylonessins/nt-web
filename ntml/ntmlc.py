"""

ntmlc.py

Ершы ьщвгду шы туув ещ щьзшду ТЕЬД сщву ещ РЕЬД

"""

import sys
from ntml.ntml_parser import ntml_parser
from ntml.tran import Tran


def ntml_compile(ntml: str | bytes) -> str:
    """
    
    fucntion compile

    ntml (str|bytes): code in ntml to be compiled

    rvalue (str): result html code

    """

    ast = ntml_parser.parse(ntml)
    translator = Tran(ast)
    translator.walk_tree()
    return translator.to_html()


if __name__ == '__main__':
    with open(sys.argv[-2], "rt", encoding="utf-8") as f:
        tree = ntml_parser.parse(f.read())

    tran = Tran(tree)

    tran.walk_tree()

    with open(sys.argv[-1], "wt", encoding="utf-8") as out:
        print(tran.to_html(), file=out, flush=True)
