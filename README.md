# Projects: DFA Minimization and CFG to CNF Converter

## ✅ Task 1: DFA Minimization

### Overview
This project implements a **Deterministic Finite Automaton (DFA) Minimization** algorithm based on **Hopcroft's Algorithm**. The goal is to minimize the number of states in a DFA without altering the language it accepts.

### Features
- Define DFA with states, alphabet, transitions, start state, and accept states
- Apply Hopcroft's minimization algorithm
- Display original and minimized DFA

### Example 1: DFA Minimization
```python
# Define a DFA
dfa = DFA(
    states={'A', 'B', 'C', 'D', 'E', 'F'},
    alphabet={'0', '1'},
    transition={
        'A': {'0': 'B', '1': 'C'},
        'B': {'0': 'A', '1': 'D'},
        # ... other transitions
    },
    start_state='A',
    accept_states={'C', 'D'}
)

# Minimize the DFA
min_dfa = dfa.minimize()
Output Sample
Original DFA:
States: {'A', 'B', 'C', 'D', 'E', 'F'}
Alphabet: {'0', '1'}
Start State: A
Accept States: {'C', 'D'}
Transitions:
A -0-> B, A -1-> C
B -0-> A, B -1-> D
...

Minimized DFA:
States: {0, 1, 2}
Alphabet: {'0', '1'}
Start State: 0
Accept States: {1}
Transitions:
0 -0-> 1, 0 -1-> 2
...
```
ك
Project Structure
DFA Class: Represents the DFA=
minimize(): Implements Hopcroft's algorithm
print_dfa(): Displays DFA structure



✅ Task 2: CFG to CNF Converter
Overview
Converts Context-Free Grammar (CFG) to Chomsky Normal Form (CNF), required for parsing algorithms like CYK.

Features
Remove ε-productions, unit productions, and useless symbols

Convert productions to CNF form (A → BC or A → a)

Example 2: CFG to CNF Conversion
```python
# Define a CFG
grammar = {
    'S': ['AB', 'BC'],
    'A': ['BA', 'a'],
    'B': ['CC', 'b'],
    'C': ['AB', 'a']
}

# Convert to CNF
cnf_converter = CFG(grammar)
cnf_grammar = cnf_converter.to_cnf()
Output Sample
Original Grammar:
S → AB | BC
A → BA | a
B → CC | b
C → AB | a

CNF Grammar:
S → A1 B | B1 C
A → B2 A | a
B → C1 C | b
C → A2 B | a
A1 → A B
B1 → B C
...
```
Project Structure
CFG Class: Represents the grammar

remove_null_productions(): Eliminates ε-productions

remove_unit_productions(): Removes unit productions

remove_useless_symbols(): Cleans up grammar

to_cnf(): Performs full conversion to CNF
