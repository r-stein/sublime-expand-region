try:
    import interpreter
except:
    from . import interpreter


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
