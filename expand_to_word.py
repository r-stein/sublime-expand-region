import re

try:
  import expand_to_regex_set
  from _minterp import interpreter
except:
  from ._minterp import interpreter
  from . import expand_to_regex_set


def expand_to_word(string, startIndex, endIndex):
  regex = re.compile(r"[\w$]", re.UNICODE)

  return expand_to_regex_set.expand_to_regex_rule(string, startIndex, endIndex, regex, "word")

interpreter.register_command("word", expand_to_word)
