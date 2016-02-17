import re
try:
    import utils
    import expand_to_symbols
    import expand_to_word
    from _minterp import interpreter
    _ST3 = False
except:
    from . import utils
    from . import expand_to_symbols
    from . import expand_to_word
    from ._minterp import interpreter
    _ST3 = True


_BEGIN_END_REG = re.compile(
    r"\\(?P<command>begin|end)"
    r"(?:\[.*\])?"
    r"\{(?P<name>[^\}]*)\}"
)
_EXCLUSIVE_BEGIN_END_REG = re.compile(
    r"^"
    r"\\(?P<command>begin|end)"
    r"(?:\[.*\])?"
    r"\{(?P<name>[^\}]*)\}"
    r"$"
)


def chart_at(string, index):
    """returns the chart at the position or the empty string,
    if the index is outside the string"""
    return string[index:index+1]


def _get_closest_env_border(string, start_pos, end_pos, reverse=False):
    open_command = "begin"
    close_command = "end"
    if _ST3:
        iterator = _BEGIN_END_REG.finditer(string, pos=start_pos,
                                           endpos=end_pos)
        offset = 0
    else:
        s = string[start_pos:end_pos]
        iterator = _BEGIN_END_REG.finditer(s)
        offset = start_pos
    if reverse:
        iterator = reversed(list(iterator))
        open_command, close_command = close_command, open_command
    count = 0
    for before in iterator:
        line = utils.get_line(string, before.start(), before.end())
        # ignore comment lines
        if string[line["start"]:line["end"]].strip()[0] == "%":
            continue
        command = before.group("command")
        if command == open_command:
            count += 1
        elif command == close_command and count > 0:
            count -= 1
        elif command == close_command:
            # found begin before
            return {
                "start": offset + before.start(),
                "end": offset + before.end(),
                "name": before.group("name")
            }


def expand_against_matching_env(string, start, end):
    m = _EXCLUSIVE_BEGIN_END_REG.match(string[start:end])
    if not m:
        return None
    if m.group("command") == "begin":
        reverse = False  # search downwards
        search_start = end
        search_end = len(string)
    else:  # == "end"
        reverse = True  # search upwards
        search_start = 0
        search_end = start
    env_border = _get_closest_env_border(string, search_start, search_end,
                                         reverse=reverse)
    if not env_border:
        return None
    if not env_border["name"] == m.group("name"):
        print("Environments not matching '{}' and '{}'"
              .format(env_border["name"], m.group("name")))
        return None
    if not reverse:  # search from begin
        start = start
        end = env_border["end"]
    else:  # search from end
        start = env_border["start"]
        end = end
    return utils.create_return_obj(start, end, string,
                                   "latex_environment_matching")


def expand_against_env(string, start, end):
    tex_begin = _get_closest_env_border(string, 0, start, reverse=True)
    tex_end = _get_closest_env_border(string, end, len(string), reverse=False)

    if tex_begin is None or tex_end is None:
        return None
    if tex_begin["name"] != tex_end["name"]:
        print("Environments not matching '{}' and '{}'"
              .format(tex_begin["name"], tex_end["name"]))
        return None
    inner_env_selected = start == tex_begin["end"] and end == tex_end["start"]
    if inner_env_selected:
        start = tex_begin["start"]
        end = tex_end["end"]
    else:
        start = tex_begin["end"]
        end = tex_end["start"]
    return utils.create_return_obj(start, end, string, "latex_environment")


def expand_agains_base_command(string, start, end):
    start -= 1
    if chart_at(string, start) == "\\":
        if chart_at(string, end) == "*":
            end += 1
        result = utils.create_return_obj(start, end, string,
                                         "latex_command_base")
        return result


class NoSemanticUnit(Exception):
    pass


def _stretch_over_previous_semantic_unit(string, start):
    start -= 1
    while chart_at(string, start) == " ":
        start -= 1
    if chart_at(string, start) in ["]", "}"]:
        r = expand_to_symbols.expand_to_symbols(string, start, start)
        if r is not None:
            return r["start"] - 1
    raise NoSemanticUnit()


def _stretch_over_next_semantic_unit(string, end):
    while chart_at(string, end) == " ":
        end += 1
    if chart_at(string, end) in ["[", "{"]:
        end += 1
        r = expand_to_symbols.expand_to_symbols(string, end, end)
        if r is not None:
            end = r["end"]
            # special case: '{}' (no content)
            if end == r["start"] + 2:
                return end
            return end + 1
    raise NoSemanticUnit()


def expand_against_command_args(string, start, end):
    if not chart_at(string, start) == "\\":
        return None
    if chart_at(string, end) not in ["{", "["]:
        return None
    original_end = end
    while True:
        try:
            end = _stretch_over_next_semantic_unit(string, end)
        except NoSemanticUnit:
            break
    # if the end did not change: do nothing
    if original_end == end:
        return None
    return utils.create_return_obj(start, end, string, "latex_command_arg")


def expand_against_surrounding_command(string, start, end):
    if chart_at(string, start) in ["{", "["] and\
            chart_at(string, end - 1) in ["}", "]"]:
        # span backwards over [..] and {..}
        while True:
            try:
                start = _stretch_over_previous_semantic_unit(string, start)
            except NoSemanticUnit:
                break
        # span forwards over [..]  and [..]
        while True:
            try:
                end = _stretch_over_next_semantic_unit(string, end)
            except NoSemanticUnit:
                break

        # span over the previous \command or \command*
        if chart_at(string, start - 1) == "*":
            start -= 1
        result = expand_to_word.expand_to_word(string, start, start)
        if result is None:
            return None
        start = result["start"] - 1
        if chart_at(string, start) == "\\":
            return utils.create_return_obj(start, end, string,
                                           "latex_command_surround")


interpreter.create_macro("latex", [
    "word",
    expand_agains_base_command,
    expand_against_command_args,
    expand_against_surrounding_command,
    expand_against_matching_env,
    [
        expand_against_env,
        "symbol"
    ]
])
