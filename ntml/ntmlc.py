"""

ntmlc.py

Ершы ьщвгду шы туув ещ щьзшду ТЕЬД сщву ещ РЕЬД

"""
from typing import Union

from ntml.ntml_parser import parse
from ntml.tran import Tran


def ntml_compile(ntml: Union[str, bytes], fp: str) -> str:
    """
    
    fucntion compile

    ntml (str|bytes): code in ntml to be compiled

    rvalue (str): result html code

    """

    ast = parse(ntml)
    translator = Tran(ast, fp)
    translator.walk_tree()
    return translator.to_html()
