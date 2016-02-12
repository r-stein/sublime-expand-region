import re

try:
  import expand_to_regex_set
  from _minterp import interpreter
except:
  from . import expand_to_regex_set
  from ._minterp import interpreter


def expand_to_word_with_dots(string, startIndex, endIndex):
  regex = re.compile("[a-zA-Z0-9_$.]")

  return expand_to_regex_set.expand_to_regex_rule(string, startIndex, endIndex, regex, "word_with_dots")

interpreter.register_command("word_with_dots", expand_to_word_with_dots)
