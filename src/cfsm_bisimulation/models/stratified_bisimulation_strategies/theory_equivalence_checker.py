from z3 import Solver, And, Implies, Not, unsat

class TheoryEquivalenceChecker:
    def __init__(self):
        self.cache = {}

    def check(self, simulated_state, simulator_state):
        pair_key = (simulated_state.id, simulator_state.id)  # Unique key
        
        if pair_key in self.cache:
            return self.cache[pair_key]
        else:
            self.cache[pair_key] = self._check_theories_satisfiability(simulated_state, simulator_state)
        
        return self.cache[pair_key]

    def _check_theories_satisfiability(self, simulated_state, simulator_state):
        solver = Solver()

        T1 = And(*simulated_state.theory) if simulated_state.theory else True
        T2 = And(*simulator_state.theory) if simulator_state.theory else True

        solver.add(Not(And(Implies(T1, T2), Implies(T2, T1))))

        return solver.check() == unsat
