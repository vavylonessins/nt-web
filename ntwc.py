import os
import sys
import traceback as tb
from ntml import ntmlc
import shutil


path = sys.argv[-1].replace("\\s", " ")


def ntml_recursive_compile_all(srcdir: str|os.PathLike, dstdir: str|os.PathLike, level=1) -> None:
    if not dstdir:
        try: os.mkdir(dstdir)
        except: pass
    for f in os.listdir(srcdir):
        if os.path.isdir(srcdir+f):
            print("    "*(level)+f+"/")
            try:
                os.mkdir(dstdir+f)
            except FileExistsError:
                pass
            ntml_recursive_compile_all(srcdir+f+"/", dstdir+f+"/", level+1)
        else:
            print("    "*(level)+f, end="")
            if f.endswith("ntml"):
                print(" NTML")
                opath = (dstdir+f).replace(".ntml", ".html")
                with open(srcdir+f, "rt") as fp:
                    with open(opath, "wt") as op:
                        op.write(ntmlc.compile(fp.read()))
            else:
                print()
                src = srcdir+f
                dst = dstdir+f
                shutil.copy(src, dst)


try:
    print(path+"/")
    ntml_recursive_compile_all(path+"/src/", path+"/dst/")
except BaseException as be:
    tb.print_exception(be)
    #print(be.__class__.__name__+":", str(be))
