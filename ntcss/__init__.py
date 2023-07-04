"""."""
try:
    # noinspection PyShadowingBuiltins
    from ntmlc import ntml_compile as compile
except ImportError:
    # noinspection PyShadowingBuiltins
    from ntml.ntmlc import ntml_compile as compile
