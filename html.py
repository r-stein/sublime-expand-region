try:
    from _minterp import interpreter
except:
    from ._minterp import interpreter


interpreter.create_macro("html", [
    "subword",
    "word",
    "quotes",
    "xml_node"
])
