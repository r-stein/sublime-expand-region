try:
  # Block it from trying to import something which should not be on the python sys.path
  # https://github.com/hktonylee/SublimeNumberKing/issues/4
  import expand_region_handler
  import utils
  from _minterp import interpreter
except:
  from . import utils
  from ._minterp import interpreter


def expand_to_line(string, start, end):
  line = utils.get_line(string, start, end)
  indent = utils.get_indent(string, line)
  lstart = line["start"] + indent
  if start < lstart:
    lstart = line["start"]
  lend = max(end, line["end"])
  if lstart == start and lend == end:
    return
  return utils.create_return_obj(lstart, lend, string, "line")


def expand_to_full_line(string, start, end):
  line = utils.get_line(string, start, end)
  lstart = line["start"]
  lend = line["end"]
  return utils.create_return_obj(lstart, lend, string, "full_line")


interpreter.register_command("line", expand_to_line)
interpreter.register_command("full_line", expand_to_full_line)
