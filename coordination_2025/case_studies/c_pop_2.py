from z3 import And
from src.cfsm_bisimulation.models.communicating_system.cfsm import CommunicatingFiniteStateMachine
from coordination_2025.case_studies.utils import QoS, Vars

n, i, e, s, s_p = Vars['n'], Vars['i'], Vars['e'], Vars['s'], Vars['s_p']

e_cfsm = CommunicatingFiniteStateMachine(['C', 'S'])

e_cfsm.add_states(
    ('0', QoS['low']),
    ('1', QoS['low']),
    ('2', QoS['db']),
    ('3', QoS['low']),
    ('4', QoS['db']),
    ('4_p', QoS['db']),
    ('5', QoS['mem']),
    ('6', QoS['chk']),
    ('7', QoS['low']),
    ('8', QoS['low'])
)

e_cfsm.set_as_initial('0')
e_cfsm.set_as_finals('8')

e_cfsm.add_transition_between('0', '1', 'CS! hello()')
e_cfsm.add_transition_between('0', '7', 'CS! quit()')

e_cfsm.add_transition_between('1', '2', 'SC? num(int n)', n > 0)

e_cfsm.add_transition_between('2', '3', 'CS! read(int i)', And(0 < i, i <= n))
e_cfsm.add_transition_between('2', '7', 'CS! quit()')

e_cfsm.add_transition_between('3', '4', 'SC? size(int s)', And(s_p > 0, 0 <= s, s <= s_p))

e_cfsm.add_transition_between('3', '4_p', 'SC? size(int s)', And(s > s_p, s_p > 0))
e_cfsm.add_transition_between('4_p', '5', 'CS! retr()')
e_cfsm.add_transition_between('4_p', '7', 'CS! retr()')

e_cfsm.add_transition_between('4', '5', 'CS! retr()')
e_cfsm.add_transition_between('4', '7', 'CS! quit()')

e_cfsm.add_transition_between('5', '6', 'SC? msg(string e)', e != "")

e_cfsm.add_transition_between('6', '2', 'CS! ack()')

e_cfsm.add_transition_between('5', '6', 'SC? bye()')

