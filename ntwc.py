"""

ntwc.py

main NTWeb compiler file

"""


import os
import sys
import traceback as tb
from errors import print_parse_error
import ntml
import shutil
import re
import parglare


path: str = sys.argv[-1].replace("\\s", " ")
compiled: list[str] = []
last_opened: str | os.PathLike = path


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

if "--real-errors" in sys.argv:
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
else:
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
        nl, ns, dt = str(pe).split(":", 2)
        nl = int(nl.split()[-1])
        ns = int(ns)
        print_parse_error((nl, ns), last_opened, dt)
    except SystemExit:
        sys.exit()
    except BaseException as be:
        print(be)
