from typing import *
from parglare import Grammar, Parser
from pprint import pformat
from ntml.const import *


ml_grm = r"""

Sroot: Sdoctype ( Simport | Stitle | Stag | Tcomment )*;

    Sdoctype: Tdoctype Tntml Tverfloat?;

    Simport: Timport "(" Tname "," Tstr ")" Tstr;

    Stitle: Ttitle Tstr;

    Stag: Ttagname Sprops? Sbody?;

        Sprops: "(" ( Sassign ( "," Sassign )* ) ")";

            Sassign: Tname "=" Sexpr;

                Sexpr: "(" Sexpr ")"
                     | Sexpr "**" Sexpr
                     | Sexpr "*" Sexpr
                     | Sexpr "/" Sexpr
                     | Sexpr "+" Sexpr
                     | Sexpr "-" Sexpr
                     | "-" Sexpr
                     | Tstr
                     | Tfloat
                     | Tint;

        Sbody: "{" ( Stag | Tcomment | Tname | Tescape | Tany )* "}";

terminals

Tstr: /"[^"\\]*(?:\\.[^"\\]*)*"/;
Tcomment: /\/\*.*\*\//;
Tdoctype: "doctype";
Tntml: /ntml/;
Timport: "import";
Ttitle: "title";
Ttagname: /[A-Za-zА-Яа-яЁё_]\w*\b\s*(?=(\(|\{))/;
Tname: /\b[A-Za-zА-Яа-яЁё_]\w*\b(?!(\(|\{))/;
Tint: /0[xX](?:_?[0-9a-fA-F])+|0[bB](?:_?[01])+|0[oO](?:_?[0-7])+|(?:0(?:_?0)*|[1-9](?:_?\d)*)/;
Tverfloat: /\d\.\d+(\.\d+)?/;
Tfloat: /\d(?:_?\d)*\.(?:\d(?:_?\d)*)?/;
Tescape: /\[.{1,4}\]/;
Tany: /(\+|\;|\/|\/|\*|\`|\’|\:|\d|\?|\&|\~|\'|\"SUPPRESS_NEWLINW
|\!|\-|\,|\.|\)|\]|<|>||\"|\=|\!|\@|\#|\||\$|\%|\^|\&|\*|\:|\/(?!\*)|\d|\b|\w(?!(\(|\{)))+/;

""".replace("SUPPRESS_NEWLINE\n", "")


class Node:
    kind: str
    data: dict
    pos: Any
    end_pos: Any

    def __init__(self, typ: str, data: dict = None, pos: int = None, end_pos: int = None):
        self.kind: str = str(typ)
        self.data: dict = data or {}
        self.pos = pos
        self.end_pos = end_pos

    def __str__(self):
        return """Node <%s at %s:%s>
    %s""" % (self.kind, self.pos, self.end_pos, pformat(self.data))
    
    __repr__ = __str__


def flat(a: list, tp: type = list):
    i: list | Any
    r: list

    r = []
    for i in a:
        if type(i) in (list, set, tuple):
            r += flat(i)
        else:
            r.append(i)
    return tp(r.copy())


def props_to_dict(n: Optional[list[str | dict]]):
    if not n:
        return {}

    n = flat(n[1:][:-1])
    ret = {}
    ptr = 0

    while ptr < len(n):
        ret[n[ptr]] = n[ptr+2]
        ptr += 4
    
    return ret


def unescape(raw):
    data = raw[1:][:-1]

    if raw == "[[]":
        return "["

    if data == "nl":
        return "<br/>"
    
    elif data == "sp":
        return "&nbsp;"
    
    elif data in ("c", "cp", "copy"):
        return "&copy;"
    
    elif data in list("()[]{}\\/"):
        return data
    
    else:
        return f"[{data}]"


def gnp(start_pos):
    ntml = code
    ls = ntml[:start_pos].split("\n")
    nl = len(ls)
    ns = len(ls[-1])
    return nl, ns


actions = {
    "Sdoctype": lambda _, n: Node("doctype", {"version": eval(n[2]) if n[2] else VERSION}, gnp(_.start_position), gnp(_.end_position)),
    "Simport": lambda _, n: Node("import", {"semantic": n[2], "type": eval(n[4]),
                                            "path": eval(n[6])}, gnp(_.start_position), gnp(_.end_position)),
    "Stitle": lambda _, n: Node("title", {"text": n[1]}, gnp(_.start_position), gnp(_.end_position)),
    "Stag": lambda _, n: Node("tag", {"type": n[0], "props": n[1], "body": n[2]}, gnp(_.start_position), gnp(_.end_position)),
    "Sprops": lambda _, n: props_to_dict(n),
    "Sbody": lambda _, n: n[1],
    "Tint": lambda _, n: '"' + n + '"',
    "Tverfloat": lambda _, n: '"' + n + '"',
    "Tfloat": lambda _, n: '"' + n + '"',
    "Tescape": lambda _, n: Node("html", {"value": unescape(n)}, gnp(_.start_position), gnp(_.end_position)),
    "Tcomment": lambda _, n: Node("comment", {"text": n[2:][:-2]}, gnp(_.start_position), gnp(_.end_position))
}


ntml_parser = Parser(grammar=Grammar.from_string(ml_grm), actions=actions)

def parse(ntml: str) -> Node:
    global code
    code = ntml
    return ntml_parser.parse(ntml)
