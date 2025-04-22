from src.cfsm_bisimulation.models.assertable_finite_state_machines.afsm import AFSM
from src.cfsm_bisimulation.models.assertable_finite_state_machines.assertable_label import AssertableLabel
from z3 import Int

x = Int('x')

afsm_example_4_1 = AFSM()

afsm_example_4_1.add_states('p0', 'p1', 'p2', 'p3', 'p4', 'p5')
afsm_example_4_1.set_as_initial('p0')

afsm_example_4_1.add_transition_between(
    'p0',
    'p1',
    AssertableLabel('f(int x)', x),
    x != 0
)

afsm_example_4_1.add_transition_between(
    'p1',
    'p2',
    AssertableLabel('g'),
    x > 0
)
afsm_example_4_1.add_transition_between(
    'p1',
    'p3',
    AssertableLabel('g'),
    x < 0
)

afsm_example_4_1.add_transition_between('p2', 'p4', AssertableLabel('h'))
afsm_example_4_1.add_transition_between('p3', 'p5', AssertableLabel('h'))
