import os
from clang.cindex import Config
if 'CLANG_LIBRARY_PATH' in os.environ:
    Config.set_library_path(os.environ['CLANG_LIBRARY_PATH'])

from clang.cindex import TranslationUnit, EvalResultKind
from tests.cindex.util import get_cursor, get_tu

import unittest


class TestEvaluate(unittest.TestCase):
    def test_evaluate(self):
        source = """constexpr static int calc_val() { return 1 + 2; }
                    constexpr auto value1 = calc_val() + sizeof(char);
                    constexpr auto value2 = -1 * 5;"""
        tu = get_tu(source, lang="cpp", flags=['-std=c++14'])

        def evaluate_variable(name):
            var = get_cursor(tu, name)
            self.assertIsNotNone(var, "Could not find {}.".format(name))

            res = var.evaluate()
            self.assertIsNotNone(res, "Could not evaluate {}.".format(name))

            return res


        value1 = evaluate_variable("value1")
        self.assertEqual(value1.kind, EvalResultKind.INT)
        self.assertTrue(value1.is_unsigned_int())
        self.assertEqual(value1.get_as_unsigned_int(), 4)

        value2 = evaluate_variable("value2")
        self.assertEqual(value2.kind, EvalResultKind.INT)
        self.assertFalse(value2.is_unsigned_int())
        self.assertEqual(value2.get_as_long_long(), -5)
