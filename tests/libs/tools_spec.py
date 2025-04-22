import unittest
from src.cfsm_bisimulation.libs.tools import collect_variables
from z3 import Int, Real, String, Bool, And, Or, Not, ForAll, Exists, Function, RealSort

class ToolsTestCase(unittest.TestCase):

    def test_expression_without_variables(self):
        expr = And(True, Not(False))  # No tiene variables
        self.assertEqual(collect_variables(expr), set())

    def test_literal_with_one_variable(self):
        x = Int('x')
        expr = x > 0
        self.assertEqual(collect_variables(expr), {x})

    def test_literal_with_multiple_variables(self):
        x, y = Int('x'), Int('y')
        expr = x + y > 10
        self.assertEqual(collect_variables(expr), {x, y})

    def test_quantifier_without_free_variables(self):
        x = Int('x')
        expr = ForAll(x, x > 0)  # x está ligado
        self.assertEqual(collect_variables(expr), set())

    def test_quantifier_with_free_variable(self):
        x, y = Int('x'), Int('y')
        expr = ForAll(x, x + y > 0)  # y es libre
        self.assertEqual(collect_variables(expr), {y})

    def test_combination_of_quantifiers_and_free_variables(self):
        x, y, z = Int('x'), Int('y'), Int('z')
        expr = And(ForAll(x, x + y > 0), z < 5)  # y y z son libres
        self.assertEqual(collect_variables(expr), {y, z})

    def test_nested_quantifiers_with_free_variable(self):
        x, y, z = Int('x'), Int('y'), Int('z')
        expr = ForAll(x, Exists(y, x + y > z))  # Solo z es libre
        self.assertEqual(collect_variables(expr), {z})

    def test_function_application_with_quantifiers(self):
        x, y = Real('x'), Real('y')
        f = Function('f', RealSort(), RealSort())
        expr = ForAll(x, f(x) > y)  # Solo y es libre
        self.assertEqual(collect_variables(expr), {y})

if __name__ == '__main__':
    unittest.main()
