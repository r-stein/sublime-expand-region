try:
    from _minterp import interpreter
except:
    from ._minterp import interpreter


interpreter.create_macro("javascript", [
    "subword",
    "word",
    {
        "scope": "quotes",
        "command": "symbol"
    },
    [
        "line",
        "quotes",
        "semantic_unit",
        "symbol"
    ]
])

# interpreter.create_macro("javascript", [
#     "subword",
#     "word",
#     {
#         "scope": "line",
#         "command": [
#             [
#                 "symbol",
#                 "quotes",
#                 "semantic_unit"
#             ]
#         ]
#     },
#     [
#         "line",
#         "semantic_unit"
#     ],
#     "symbol"
# ])
