from z3 import Or, Not, Implies, Solver, unsat
from ....libs.tools import powerset
from ....models.assertable_finite_state_machines.assertion import Assertion


class SharedLanguageSimulationStrategy:

    def __init__(self, bisimulation, candidate_element_tuple):
        self.bisimulation = bisimulation
        (simulated_state, simulated_knowledge), (simulator_state, simulator_knowledge) = candidate_element_tuple
        self.simulated_state = simulated_state
        self.simulated_knowledge = simulated_knowledge
        self.simulator_state = simulator_state
        self.simulator_knowledge = simulator_knowledge

        self.simulated_transition = None

    def is_able_to_simulate(self):
        is_able = True
        simulated_transitions = self.simulated_state.get_transitions()
        i = 0

        # If it exits because is_able is False, then it's because there exists an action that "simulator_state" cannot simulate, 
        # or it can simulate it but does not fall into the relation.
        # If it exits because i < len(transitions), then it iterated through all actions and "simulator_state" was always able to simulate "simulated_state" 
        # and fall within the relation
        while is_able and i < len(simulated_transitions):
            self.simulated_transition = simulated_transitions[i]

            # Is necesary to verify whether there exists any subset of transitions from "simulator_state" that can simulate the transition from "simulated_state".
            # If it exists, it will be unique, because if there were more than one subset that achieves this, it would mean that there are at least two transitions
            # from "simulated_state" such that both paths are valid for a valid trace. 
            # This would give us a non-deterministic automaton, and we are always working with deterministic ones.

            is_able = self._exists_a_valid_transition_subset_that_simulates()

            i += 1

        return is_able

    def _exists_a_valid_transition_subset_that_simulates(self):
        cleaned_simulated_knowledge = self.simulated_knowledge.clean_by(self.simulated_transition.label)
        cleaned_simulator_knowledge = self.simulator_knowledge.clean_by(self.simulated_transition.label)
        simulator_transitions = self.simulator_state.get_transitions_with(self.simulated_transition.label)

        # I don’t consider the empty subset because it would not be valid. If there are no subsets other than the empty one,
        # the loop will never execute and the function will return False.
        simulator_transitions_subsets = list(powerset(simulator_transitions))
        simulator_transitions_subsets.remove(frozenset())

        valid_transitions_set_exists = False
        j = 0

        while (not valid_transitions_set_exists) and j < len(simulator_transitions_subsets):
            simulator_transitions_subset = list(simulator_transitions_subsets[j])
            valid_transitions_set_exists = self._is_a_valid_transition_subset_to_simulate(simulator_transitions_subset, cleaned_simulated_knowledge, cleaned_simulator_knowledge)

            j += 1

        return valid_transitions_set_exists

    def _is_a_valid_transition_subset_to_simulate(self, simulator_transitions_subset, cleaned_simulated_knowledge, cleaned_simulator_knowledge):
        # If I find a subset of transitions whose implication is satisfiable and also falls into the current_relation, then it is valid.
        return self._transitions_subset_fall_into_relation(simulator_transitions_subset, cleaned_simulated_knowledge, cleaned_simulator_knowledge) and \
               self._is_able_to_simulate_knowledge(simulator_transitions_subset, cleaned_simulated_knowledge, cleaned_simulator_knowledge)

    def _transitions_subset_fall_into_relation(self, simulator_transitions_subset, cleaned_simulated_knowledge, cleaned_simulator_knowledge):
        fall_into_current_relation = True
        k = 0

        # I check whether all transitions in the subset fall within the approximation passed as a parameter.
        while fall_into_current_relation and k < len(simulator_transitions_subset):
            simulator_transition = simulator_transitions_subset[k]

            simulated_element = (self.simulated_transition.target, cleaned_simulated_knowledge.add(self.simulated_transition.assertion))
            simulator_element = (simulator_transition.target, cleaned_simulator_knowledge.add(simulator_transition.assertion))

            fall_into_current_relation = self.bisimulation.includes((simulated_element, simulator_element))

            k += 1

        return fall_into_current_relation

    def _is_able_to_simulate_knowledge(self, simulator_transitions_subset, cleaned_simulated_knowledge, cleaned_simulator_knowledge):
        simulated_formula = self._simulated_formula_from(cleaned_simulated_knowledge)

        simulator_formula = Or({
            cleaned_simulator_knowledge.add(transition.assertion).build_conjunction()
            for transition in simulator_transitions_subset
        })

        implication = Implies(simulated_formula, simulator_formula)
        solver = Solver()

        return solver.check(Not(implication)) == unsat

    def _simulated_formula_from(self, cleaned_simulated_knowledge):
        return cleaned_simulated_knowledge.add(self.simulated_transition.assertion).build_conjunction()