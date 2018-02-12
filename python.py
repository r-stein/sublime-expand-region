try:
    import expand_to_indent
    import utils
    import interpreter
except:
    from . import expand_to_indent
    from . import utils
    from . import interpreter


def expand_over_line_continuation(string, start, end):
    if not string[end-1:end] == "\\":
        return None
    line = utils.get_line(string, start, start)
    next_line = utils.get_line(string, end + 1, end + 1)
    start = line["start"]
    end = next_line["end"]
    next_result = expand_over_line_continuation(string, start, end)
    # recursive check if there is an other continuation
    if next_result:
        start = next_result["start"]
        end = next_result["end"]
    return utils.create_return_obj(start, end, string, "line_continuation")


def expand_python_block_from_start(string, start, end):
    if string[end-1:end] != ":":
        return None
    result = expand_to_indent.expand_to_indent(string, end + 1,
                                               end + 1)
    if result:
        # line = utils.get_line(string, start, start)
        line = utils.get_line(string, start, start)
        start = line["start"]
        end = result["end"]
        return utils.create_return_obj(start, end, string, "py_block_start")


interpreter.create_macro("python", [
    "subword",
    "word",
    {
        "scope": "quotes",
        "command": "symbol"
    },
    [
        "symbol",
        "quotes",
        "semantic_unit",
        "line"
    ],
    [
        expand_over_line_continuation,
        expand_python_block_from_start
    ],
    # "indent",
    "py_indent"
])
