"""

ntwc.py

main NTWeb compiler file

"""


import os
import sys
import traceback as tb
import ntml
import shutil
import re
import parglare


path: str = sys.argv[-1].replace("\\s", " ")
compiled: list[str] = []
last_opened: str | os.PathLike = path


def restyle(data: str) -> str:
    """

    function restyle

    data (str): source string
    rvalue (str): re-styled string

    Makes parse error messages prettier

    """
    data = data.replace("Tcomment", "comment declaration")
    data = data.replace("Tdoctype", "keyword \"doctype\"")
    data = data.replace("Tntml", "keyword \"ntml\"")
    data = data.replace("Timport", "keyword \"import\"")
    data = data.replace("Ttitle", "keyword \"title\"")
    data = data.replace("Ttagname", "tag name")
    data = data.replace("Tverfloat", "version declaration")
    data = data.replace("Tescape", "escape sequence")
    data = data.replace("Tany", "any other content")
    data = data.replace("Tname", "symbol name")
    data = data.replace("Tname", "symbol name")
    data = data.replace("Tname", "symbol name")
    data = data.replace("Tname", "symbol name")
    data = data.replace("Tfloat", "float")
    data = data.replace("Tint", "integer")
    data = data.replace("Tstr", "string")
    data = data.replace("Sdoctype", "doctype declaration")
    data = data.replace("Sbody", "tag body")
    data = data.replace("Sexpr", "expression")
    data = data.replace("Sassign", "assignment")
    data = data.replace("Sprops", "tag properties")
    data = data.replace("Stag", "tag declaration")
    data = data.replace("Stitle", "title declaration")
    data = data.replace("Simport", "import declaration")
    data = data.split(" but found ", 1)[0]
    if " or " in data:
        rdata = data.split(" or ")
        data = ", ".join(rdata[:-1])
        data += " or "+rdata[-1]
    return data


# noinspection PyShadowingNames
def ntml_recursive_compile_all(srcdir: str | os.PathLike,
                               dstdir: str | os.PathLike,
                               level: int = 1) -> None:
    """

    function ntml_recursive_compile_all

    srcdir (str|os.PathLike): path to sources
    dstdir (str|os.PathLike): path to distribution

    rvalue (NoneType)

    """

    global last_opened

    if srcdir.endswith("/dir/"):
        print(srcdir)

    try:
        os.mkdir(dstdir)
    except FileExistsError:
        pass

    f: str
    for f in os.listdir(srcdir):
        if srcdir + f in compiled:
            continue
        if os.path.isdir(srcdir + f):
            print("    " * level + f + "/")
            try:
                os.mkdir(dstdir+f)
            except FileExistsError:
                pass
            ntml_recursive_compile_all(srcdir + f + "/", dstdir + f + "/", level+1)
        else:
            print("    " * level + f, end="")
            last_opened = srcdir + f
            if f.endswith("ntml"):
                print(" NTML")
                opath = (dstdir+f).replace(".ntml", ".html")
                with open(srcdir+f, "rt") as fp:
                    with open(opath, "wt") as op:
                        op.write(ntml.compile(fp.read(), srcdir + f))
            else:
                print()
                src = srcdir+f
                dst = dstdir+f
                shutil.copy(src, dst)
        compiled.append(f)


try:
    if "--one-file" in sys.argv:
        last_opened = path
        with open(path, "rt") as i:
            with open(path.replace(".ntml", ".html"), "wt") as o:
                o.write(ntml.compile(i.read()))
        sys.exit()
    print()
    print(path.removesuffix("/") + "/")
    ntml_recursive_compile_all(path + ("/src/" if "--index-file" not in sys.argv else "/"),
                               path + ("/dst/" if "--index-file" not in sys.argv else "/"))
except parglare.exceptions.ParseError as pe:
    print()
    exc_n = pe.__class__.__name__
    exc_d = str(pe)
    # exc = re.sub(r"", r"", exc)
    nl, ns, dt = exc_d.split(":", 2)
    nl = int(nl.split()[-1])
    ns = int(ns)
    print("Error while parsing file %s," % last_opened)
    print("At line %d, column %d:" % (nl, ns))
    with open(last_opened, "rt") as f:
        print("│   " + f.read().split("\n")[nl - 1].strip())
    print("│   " + " " * ns + "▲")
    print("└───" + "─" * ns + "┘")
    print(restyle(dt.split("=> ", 1)[1]))
    print()
except SystemExit:
    sys.exit()
except BaseException as be:
    tb.print_exception(be)
    # print(be.__class__.__name__+":", str(be))
