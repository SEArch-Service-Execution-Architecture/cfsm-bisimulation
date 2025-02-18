from src.cfsm_bisimulation.models.communicating_system.cfsm import CommunicatingFiniteStateMachine
from z3 import Int, Real, And

x = Int('x')
a = Int('a')
cpu_usage = Real('cpu_usage')

cfsm_1 = CommunicatingFiniteStateMachine(['Consumer', 'Producer'])

cfsm_1.add_states(
    'p0',
    ('p1', [And(0 < cpu_usage, cpu_usage < 25)]),
    'p2'
)
cfsm_1.set_as_initial('p0')
cfsm_1.set_as_finals('p1', 'p2')

cfsm_1.add_transition_between('p0', 'p1', 'ConsumerProducer! f(int x)', x > 0)
cfsm_1.add_transition_between('p1', 'p2', 'ProducerConsumer! g(int y)')

cfsm_2 = CommunicatingFiniteStateMachine(['Customer', 'Service'])

cfsm_2.add_states(
    'q0',
    ('q1', [And(0 < cpu_usage, cpu_usage < 25)]),
    'q2'
)
cfsm_2.set_as_initial('q0')
cfsm_2.set_as_finals('q2')

cfsm_2.add_transition_between('q0', 'q1', 'CustomerService! h1(int a)', a > 0)
cfsm_2.add_transition_between('q1', 'q2', 'ServiceCustomer! h2(int b)')
