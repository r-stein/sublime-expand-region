try:
    import interpreter
except:
    from . import interpreter


interpreter.create_macro("html", [
    "subword",
    "word",
    "quotes",
    "xml_node"
])
