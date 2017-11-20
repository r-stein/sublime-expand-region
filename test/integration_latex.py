import unittest

from expand_region_handler import *


class LatexIntegrationTest(unittest.TestCase):

    @classmethod
    def setUpClass(self):
        with open("test/snippets/latex_01.txt", "r") as myfile:
            self.string1 = myfile.read()
        with open("test/snippets/latex_02.txt", "r") as myfile:
            self.string2 = myfile.read()

    def test_expand_to_word1(self):
        result = expand("\\section*{My Section}", 3, 3, "latex")
        self.assertEqual(result["start"], 1)
        self.assertEqual(result["end"], 8)

    def test_expand_to_word2(self):
        result = expand(self.string1, 243, 246, "latex")
        self.assertEqual(result["start"], 242)
        self.assertEqual(result["end"], 248)

    def test_expand_to_command_base1(self):
        result = expand("\\textbf{My Text}", 1, 7, "latex")
        self.assertEqual(result["start"], 0)
        self.assertEqual(result["end"], 7)

    def test_expand_to_command_base2(self):
        result = expand("\\section*{My Section}", 1, 8, "latex")
        self.assertEqual(result["start"], 0)
        self.assertEqual(result["end"], 9)

    def test_expand_to_command_base3(self):
        result = expand(self.string1, 242, 248, "latex")
        self.assertEqual(result["start"], 241)
        self.assertEqual(result["end"], 248)

    def test_expand_to_command_args1(self):
        result = expand(self.string1, 241, 248, "latex")
        self.assertEqual(result["start"], 241)
        self.assertEqual(result["end"], 254)

    def test_expand_to_command_args2(self):
        result = expand(self.string1, 213, 223, "latex")
        self.assertEqual(result["start"], 213)
        self.assertEqual(result["end"], 255)

    def test_expand_to_semantic_unit1(self):
        result = expand(self.string1, 249, 253, "latex")
        self.assertEqual(result["start"], 248)
        self.assertEqual(result["end"], 254)

    def test_expand_to_semantic_unit2(self):
        result = expand(self.string1, 229, 254, "latex")
        self.assertEqual(result["start"], 228)
        self.assertEqual(result["end"], 255)

    def test_expand_to_surrounding_command1(self):
        result = expand(self.string1, 248, 254, "latex")
        self.assertEqual(result["start"], 241)
        self.assertEqual(result["end"], 254)

    def test_expand_to_surrounding_command2(self):
        result = expand(self.string1, 228, 255, "latex")
        self.assertEqual(result["start"], 213)
        self.assertEqual(result["end"], 255)

    def test_expand_to_matching_env1(self):
        result = expand(self.string1, 114, 129, "latex")
        self.assertEqual(result["start"], 114)
        self.assertEqual(result["end"], 294)

    def test_expand_to_matching_env2(self):
        result = expand(self.string1, 281, 294, "latex")
        self.assertEqual(result["start"], 114)
        self.assertEqual(result["end"], 294)

    def test_expand_to_env1(self):
        result = expand(self.string1, 176, 176, "latex")
        self.assertEqual(result["start"], 174)
        self.assertEqual(result["end"], 193)

    def test_expand_to_env2(self):
        result = expand(self.string1, 174, 193, "latex")
        self.assertEqual(result["start"], 159)
        self.assertEqual(result["end"], 206)

    def test_expand_to_env3(self):
        result = expand(self.string1, 213, 255, "latex")
        self.assertEqual(result["start"], 129)
        self.assertEqual(result["end"], 281)

    def test_expand_to_env4(self):
        result = expand(self.string1, 129, 281, "latex")
        self.assertEqual(result["start"], 114)
        self.assertEqual(result["end"], 294)

    def test_expand_to_env5(self):
        result = expand(self.string1, 114, 294, "latex")
        self.assertEqual(result["start"], 89)
        self.assertEqual(result["end"], 297)

    def test_expand_to_env6(self):
        result = expand(self.string1, 89, 297, "latex")
        self.assertEqual(result["start"], 73)
        self.assertEqual(result["end"], 311)

    def test_expand_to_inline_math1(self):
        result = expand(self.string2, 137, 137, "latex")
        self.assertEqual(result["start"], 136)
        self.assertEqual(result["end"], 139)

    def test_expand_to_inline_math2(self):
        result = expand(self.string2, 136, 139, "latex")
        self.assertEqual(result["start"], 135)
        self.assertEqual(result["end"], 139)

    def test_expand_to_inline_math3(self):
        result = expand(self.string2, 135, 139, "latex")
        self.assertEqual(result["start"], 130)
        self.assertEqual(result["end"], 145)

    def test_expand_to_inline_math4(self):
        result = expand(self.string2, 130, 145, "latex")
        self.assertEqual(result["start"], 129)
        self.assertEqual(result["end"], 146)

    def test_expand_to_tex_word1(self):
        result = expand(self.string2, 165, 165, "latex")
        self.assertEqual(result["start"], 165)
        self.assertEqual(result["end"], 168)

    def test_expand_to_tex_word2(self):
        result = expand(self.string2, 165, 168, "latex")
        self.assertEqual(result["start"], 164)
        self.assertEqual(result["end"], 168)

    def test_expand_to_tex_word3(self):
        result = expand(self.string2, 164, 168, "latex")
        self.assertEqual(result["start"], 164)
        self.assertEqual(result["end"], 170)

    def test_expand_to_tex_word4(self):
        result = expand(self.string2, 173, 173, "latex")
        self.assertEqual(result["start"], 173)
        self.assertEqual(result["end"], 174)

    def test_expand_to_tex_word5(self):
        result = expand(self.string2, 173, 174, "latex")
        self.assertEqual(result["start"], 173)
        self.assertEqual(result["end"], 176)

    def test_expand_to_inline_math5(self):
        result = expand(self.string2, 173, 176, "latex")
        self.assertEqual(result["start"], 164)
        self.assertEqual(result["end"], 176)

    def test_expand_to_inline_math6(self):
        result = expand(self.string2, 164, 170, "latex")
        self.assertEqual(result["start"], 164)
        self.assertEqual(result["end"], 176)

    def test_expand_to_inline_math7(self):
        result = expand(self.string2, 164, 176, "latex")
        self.assertEqual(result["start"], 163)
        self.assertEqual(result["end"], 177)

if __name__ == "__main__":
    unittest.main()
