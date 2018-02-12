# the registered and used command
# core structure of the interpreter
if '_commands' not in globals():
    _commands = {}

if '_macros' not in globals():
    _macros = {}


def register_command(name, function):
    """Register a function and bind it to a name"""
    # print("register {0}, func: {1}".format(name, function))
    _commands[name] = function
    # print("_commands:", _commands)


def available_commands():
    return sorted(_commands.keys())


def macros():
    return _macros


def create_macro(macro_name, macro):
    """Register a macro and bind it to a name"""
    _macros[macro_name] = macro
    register_command(macro_name, compile_macro(macro))


def interp(macro, string, start, end):
    """interprets a macro to retrieve the resulting selection"""
    # ensure we use a list
    if type(macro) is not list:
        macro = [macro]
    for command in macro:
        # retrieve or generate the expand function
        if type(command) is dict:
            expand = _interp_dict(command)
        elif type(command) is list:
            expand = _interp_list(command)
        elif callable(command):
            expand = command
        else:
            if command not in _commands:
                print("Missing function for '{0}'".format(command))
                continue
            expand = _commands[command]
        # expand the selection
        result = expand(string, start, end)
        if result and not(result["start"] == start and result["end"] == end):
            # insert the expand stack if it does not exists
            return result


def compile_macro(names):
    """compiles an macro into an executable function"""
    def expand(string, start, end):
        return interp(names, string, start, end)
    return expand


def _interp_dict(name):
    """
    returns the result with considering the keywords in the list
    """
    def imp(string, start, end):
        if "scope" in name:
            scope_res = interp(name["scope"], string, start, end)
            print("scope_res:", scope_res)
            if not scope_res:
                return
            string = string[scope_res["start"]:scope_res["end"]]
            offset = scope_res["start"]
            start -= offset
            end -= offset
        else:
            offset = 0
        # print("string:", string)
        # print("start:", start)
        # print("end:", end)
        command = name["command"]
        if "args" in name:
            args = name["args"]
            if not callable(command):
                try:
                    command = _commands[command]
                except:
                    print("CANNOT CALL {0} with args".format(command))
                    return
            result = command(string, start, end, **args)
        else:
            result = interp(command, string, start, end)
        if result:
            # update the offset
            result["start"] += offset
            result["end"] += offset
            return result
    return imp


def _interp_list(commands):
    """
    returns the most inner result of the commands in the list
    """
    def imp(string, start, end):
        results = []
        for command in commands:
            result = interp(command, string, start, end)
            if result:
                results.append(result)
        if not results:
            return
        inner_result = results[0]
        for result in results:
            if (inner_result["start"] <= result["start"] and
                    result["end"] <= inner_result["end"]):
                inner_result = result
        # print("inner_result:", inner_result)
        return inner_result
    return imp
