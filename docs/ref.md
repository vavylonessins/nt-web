# Short NTWeb Reference

Project is just a folder with structure like that:
- project
- src
...
- dst
\<empty>

To compile a project, type `ntwc.py path/to/project/folder` and it will compile all code and move it into `project/dst`.

If error occurs, you will see most recent call position _python-like exception_. You should pay attension for *autospaces*.
They are automatic in all tags except `code`. In this tag, all unescaped spaces will be deleted.

tagset:
- block / bl
- code / cd
- text / t
- input / inp
- htX / hX
- link / ln
- form / f       NEW
- table / tab    NEW
- tr             NEW
- td             NEW
- image / img    NEW

 escape characters:
-  \[nl\]
-  \[sp\]
-  \[\(\]
-  \[\[\]
-  \[\{\]

TODO:
- tagset update:
  - include / inc
- ntcss
- webfalco
