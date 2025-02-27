from .case_studies.c_pop_1 import e_cfsm as e_cfsm_1
from .case_studies.c_pop_2 import e_cfsm as e_cfsm_2
from .case_studies.c_pop_3 import e_cfsm as e_cfsm_3

print("Case Studies: A variant of the POP protocol")
print("-----------------------------------------------------------\n")

print("Calculating bisimulation relation between C_pop and C'_pop:\n")

print(">>> C_pop.calculate_bisimulation_with(C'_pop)")
print("...")

relation, matches e_cfsm_1.calculate_bisimulation_with(e_cfsm_2)

if (len(relation) == 0):
    print("C_pop and C'_pop are not bisimilars")
else:
    print("C_pop and C'_pop are bisimilars. The relation is: \n")
    print(relation)


print("\n-----------------------------------------------------------\n")
print("Calculating bisimulation relation between C_pop and C''_popj, a variant of C'_pop where:")
print("    C''_pop = C'_pop and C''_pop.qos = C'_pop.qos[4' -> s' > 0 and 0 <= s <= s']\n")

print(">>> C_pop.calculate_bisimulation_with(C''_pop)")
print("...")

relation, matches e_cfsm_1.calculate_bisimulation_with(e_cfsm_3)
if (len(relation) == 0):
    print("C_pop and C''_pop are not bisimilars")
else:
    print("C_pop and C'_pop are bisimilars. The relation is: \n")
    print(relation)