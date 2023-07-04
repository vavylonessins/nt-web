"""."""
try:
    # noinspection PyShadowingBuiltins
    from webfalcoc import webfalco_compile as compile
except ImportError:
    # noinspection PyShadowingBuiltins
    from webfalco.webfalcoc import webfalco_compile as compile
