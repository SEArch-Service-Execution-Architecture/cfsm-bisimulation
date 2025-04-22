import unittest
from tests.resources.afsm.afsm_example_1 import afsm_example_1
from tests.resources.afsm.afsm_example_2_1 import afsm_example_2_1
from tests.resources.afsm.afsm_example_2_2 import afsm_example_2_2
from tests.resources.afsm.afsm_example_3_1 import afsm_example_3_1
from tests.resources.afsm.afsm_example_3_2 import afsm_example_3_2
from tests.resources.afsm.afsm_example_4_1 import afsm_example_4_1
from tests.resources.afsm.afsm_example_4_2 import afsm_example_4_2
from tests.resources.afsm.afsm_example_5_1 import afsm_example_5_1
from tests.resources.afsm.afsm_example_5_2 import afsm_example_5_2
from src.cfsm_bisimulation.models.assertable_finite_state_machines.assertion import Assertion
from src.cfsm_bisimulation.models.stratified_bisimulation_strategies.knowledge import Knowledge
from z3 import Int, BoolVal

true = BoolVal(True)
x = Int('x')
y = Int('y')

x_grater_than_zero = Assertion(Int('x') > 0)
x_lower_than_zero = Assertion(Int('x') < 0)
x_neq_zero = Assertion(Int('x') != 0)
y_grater_than_x = Assertion(Int('y') > Int('x'))


def _(state, *expressions):
    assertions = list(map(Assertion, expressions))
    return state, Knowledge(frozenset(assertions))


class AFSMCase(unittest.TestCase):

    def assertIsSubset(self, expected_relation, relation):
        self.assertTrue(expected_relation.issubset(relation))

    def test_must_be_bisimilar_with_itself(self):
        p0 = afsm_example_1.states['p0']
        p1 = afsm_example_1.states['p1']

        expected_relation = {
            (_(p0), _(p0)),
            (_(p1, x > 0), _(p1, x > 0)),
            (_(p0, x > 0, y > x), _(p0, x > 0, y > x))
        }
        relation = afsm_example_1.calculate_bisimulation_with(afsm_example_1)
        self.assertIsSubset(expected_relation, relation)

    def test_must_be_bisimilars_example_2(self):
        p0 = afsm_example_2_1.states['p0']
        p1 = afsm_example_2_1.states['p1']
        q0 = afsm_example_2_2.states['q0']
        q1 = afsm_example_2_2.states['q1']

        expected_relation = {
            (_(p0), _(q0)),
            (_(p1, x != 0), _(q1, x > 0)),
            (_(p1, x != 0), _(q1, x < 0))
        }
        relation = afsm_example_2_1.calculate_bisimulation_with(afsm_example_2_2)
        self.assertIsSubset(expected_relation, relation)

    def test_must_be_bisimilars_example_3(self):
        p0 = afsm_example_3_1.states['p0']
        p1 = afsm_example_3_1.states['p1']
        p2 = afsm_example_3_1.states['p2']
        q0 = afsm_example_3_2.states['q0']
        q1 = afsm_example_3_2.states['q1']
        q2 = afsm_example_3_2.states['q2']

        expected_relation = {
            (_(p0), _(q0)),
            (_(p1, x != 0), _(q1, x != 0)),
            (_(p2, x != 0,), _(q2, x > 0, x != 0)),
            (_(p2, x != 0), _(q2, x < 0, x != 0))
        }

        relation = afsm_example_3_1.calculate_bisimulation_with(afsm_example_3_2, True)
        self.assertIsSubset(expected_relation, relation)

    # this case breaks the algorithm when machines are not minimals.
    def test_must_be_not_bisimilars_example_4(self):
        relation = afsm_example_4_1.calculate_bisimulation_with(afsm_example_4_2)
        self.assertEqual(set(), relation)

    def test_must_be_not_bisimilars_example_5(self):
        relation = afsm_example_5_1.calculate_bisimulation_with(afsm_example_5_2)
        self.assertEqual(set(), relation)


if __name__ == '__main__':
    unittest.main()
