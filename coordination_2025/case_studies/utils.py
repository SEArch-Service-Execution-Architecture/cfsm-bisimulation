from z3 import Int, Real, String, And, Implies, Exists

t_cpu_time = Real('t')
c_monetary_cost = Real('c')
m_memory_usage = Real('m')

x = Real('x')

Vars = {
    'n': Int('n'),
    'i': Int('i'),
    's': Int('s'),
    's_p': Int('s_p'),
    'e': Int('e')
}

QoS = {
    # low computational cost
    'low': [
        t_cpu_time <= 0.01,
        c_monetary_cost <= 0.01,
        m_memory_usage <= 0.01
    ],
    # emails integrity check cost
    'chk': [
        t_cpu_time <= 5,
        c_monetary_cost == 0.5,
        m_memory_usage == 0
    ],
    # messages reception from server cost
    'mem': [
        And(1 <= t_cpu_time, t_cpu_time <= 6),
        c_monetary_cost == 0,
        m_memory_usage <= 64
    ],
    # operation execution cost
    'db': [
        Implies(t_cpu_time <= 3, Exists(x, And(0.5 <= x, x <= 1, c_monetary_cost == t_cpu_time * x))),
        Implies(t_cpu_time > 3, c_monetary_cost == 10),
        m_memory_usage <= 5
    ]
}



