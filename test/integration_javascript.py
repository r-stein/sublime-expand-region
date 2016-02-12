import unittest

from expand_region_handler import *

class JavascriptIntegrationTest(unittest.TestCase):

  @classmethod
  def setUpClass(self):
    with open ("test/snippets/integration_01.txt", "r") as myfile:
      self.string1 = myfile.read()
    with open ("test/snippets/integration_02.txt", "r") as myfile:
      self.string2 = myfile.read()
    with open ("test/snippets/integration_03.txt", "r") as myfile:
      self.string3 = myfile.read()
    with open ("test/snippets/integration_04.txt", "r") as myfile:
      self.string4 = myfile.read()

  def test_subword (self):
    result = expand(self.string1, 7, 7, "javascript");
    self.assertEqual(result["start"], 6)
    self.assertEqual(result["end"], 9)
    self.assertEqual(result["string"], "bar")
    self.assertEqual(result["type"], "subword")

  def test_word (self):
    result = expand(self.string1, 6, 9, "javascript");
    self.assertEqual(result["start"], 2)
    self.assertEqual(result["end"], 9)
    self.assertEqual(result["string"], "foo_bar")
    self.assertEqual(result["type"], "word")

  def test_quotes_inner (self):
    result = expand(self.string1, 2, 9, "javascript");
    self.assertEqual(result["start"], 2)
    self.assertEqual(result["end"], 17)
    self.assertEqual(result["string"], "foo_bar foo bar")
    self.assertEqual(result["type"], "quotes")

  def test_quotes_outer (self):
    result = expand(self.string1, 2, 17, "javascript");
    self.assertEqual(result["start"], 1)
    self.assertEqual(result["end"], 18)
    self.assertEqual(result["string"], "\"foo_bar foo bar\"")
    self.assertEqual(result["type"], "quotes")

  def test_symbol_inner (self):
    result = expand(self.string1, 1, 10, "javascript");
    self.assertEqual(result["start"], 1)
    self.assertEqual(result["end"], 24)
    self.assertEqual(result["string"], "\"foo_bar foo bar\" + \"x\"")
    self.assertEqual(result["type"], "symbol")

  def test_dont_expand_to_dots (self):
    result = expand(self.string2, 2, 5, "javascript");
    self.assertEqual(result["start"], 1)
    self.assertEqual(result["end"], 10)
    self.assertEqual(result["string"], " foo.bar ")
    self.assertEqual(result["type"], "quotes")

  # def test_expand_to_line (self):
  #   result = expand(self.string3, 30, 35, "javascript");
  #   self.assertEqual(result["start"], 28)
  #   self.assertEqual(result["end"], 37)
  #   self.assertEqual(result["string"], "foo: true")
  #   self.assertEqual(result["type"], "line")

  def test_expand_to_symbol_from_line (self):
    result = expand(self.string3, 28, 37, "javascript");
    self.assertEqual(result["start"], 23)
    self.assertEqual(result["end"], 40)
    self.assertEqual(result["string"], "\n    foo: true\n  ")
    self.assertEqual(result["type"], "symbol")

  def test_skip_some_because_of_linebreak (self):
    result = expand(self.string3, 22, 41, "javascript");
    self.assertEqual(result["start"], 15)
    self.assertEqual(result["end"], 41)
    self.assertEqual(result["string"], "return {\n    foo: true\n  }")
    self.assertEqual(result["type"], "semantic_unit")

  def test_skip_some_because_of_linebreak_2 (self):
    result = expand(self.string3, 15, 41, "javascript");
    self.assertEqual(result["start"], 12)
    self.assertEqual(result["end"], 42)
    self.assertEqual(result["type"], "symbol")

  def test_symbols_in_string_01 (self):
    result = expand(self.string4, 35, 42, "javascript");
    self.assertEqual(result["start"], 30)
    self.assertEqual(result["end"], 42)
    self.assertEqual(result["type"], "symbol")

  def test_symbols_in_string_02 (self):
    result = expand(self.string4, 30, 42, "javascript");
    self.assertEqual(result["start"], 29)
    self.assertEqual(result["end"], 43)
    self.assertEqual(result["type"], "symbol")

  def test_symbols_in_string_03 (self):
    result = expand(self.string4, 29, 43, "javascript");
    self.assertEqual(result["start"], 29)
    self.assertEqual(result["end"], 46)
    self.assertEqual(result["type"], "symbol")

  def test_symbols_in_string_04 (self):
    result = expand(self.string4, 29, 46, "javascript");
    self.assertEqual(result["start"], 28)
    self.assertEqual(result["end"], 47)
    self.assertEqual(result["type"], "symbol")

  def test_symbols_in_string_05 (self):
    result = expand(self.string4, 28, 47, "javascript");
    self.assertEqual(result["start"], 23)
    self.assertEqual(result["end"], 55)
    self.assertEqual(result["type"], "quotes")

if __name__ == "__main__":
  unittest.main()
