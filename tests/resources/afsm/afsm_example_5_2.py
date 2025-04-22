from src.cfsm_bisimulation.models.assertable_finite_state_machines.afsm import AFSM
from src.cfsm_bisimulation.models.assertable_finite_state_machines.assertable_label import AssertableLabel
from src.cfsm_bisimulation.libs.tools import TrueFormula
from z3 import Int

afsm_example_5_2 = AFSM()

afsm_example_5_2.add_states('q0', 'q1')
afsm_example_5_2.set_as_initial('q0')

afsm_example_5_2.add_transition_between(
    'q0',
    'q1',
    AssertableLabel('f(int x)', Int('x')),
    Int('x') > 0
)
