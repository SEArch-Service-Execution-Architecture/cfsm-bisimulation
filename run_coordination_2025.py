from coordination_2025.case_studies.c_pop_1 import e_cfsm as e_cfsm_1
from coordination_2025.case_studies.c_pop_2 import e_cfsm as e_cfsm_2
import time

start = time.time()

relation, matches = e_cfsm_1.calculate_bisimulation_with(c_pop_2)

end = time.time()

duration = end - start
print(f"Execution time: {duration:.4f} seconds")
