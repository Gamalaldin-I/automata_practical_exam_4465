from collections import defaultdict

class DFA:
    def __init__(self, states, alphabet, transition, start_state, accept_states):
        self.states = states
        self.alphabet = alphabet
        self.transition = transition  
        self.start_state = start_state
        self.accept_states = accept_states

    def minimize(self):
        P = [set(self.accept_states), set(self.states) - set(self.accept_states)]
        W = [set(self.accept_states)] 

        while W:
            A = W.pop()

            for c in self.alphabet:
                X = set()
                for (state, symbol), next_state in self.transition.items():
                    if symbol == c and next_state in A:
                        X.add(state)

                new_P = []
                for Y in P:
                    intersection = Y & X
                    difference = Y - X
                    if intersection and difference:
                        new_P.extend([intersection, difference])
                        if Y in W:
                            W.remove(Y)
                            W.extend([intersection, difference])
                        else:
                            W.append(intersection if len(intersection) <= len(difference) else difference)
                    else:
                        new_P.append(Y)
                P = new_P

        new_states = [frozenset(group) for group in P]
        state_map = {}
        for i, group in enumerate(new_states):
            for state in group:
                state_map[state] = i

        new_start_state = state_map[self.start_state]
        new_accept_states = {state_map[s] for s in self.accept_states}

        new_transition = {}
        for (state, symbol), next_state in self.transition.items():
            s1 = state_map[state]
            s2 = state_map[next_state]
            new_transition[(s1, symbol)] = s2

        return DFA(
            states=set(state_map.values()),
            alphabet=self.alphabet,
            transition=new_transition,
            start_state=new_start_state,
            accept_states=new_accept_states
        )

    def print_dfa(self):
        print("States:", self.states)
        print("Alphabet:", self.alphabet)
        print("Start state:", self.start_state)
        print("Accept states:", self.accept_states)
        print("Transitions:")
        for (state, symbol), dest in self.transition.items():
            print(f"  δ({state}, '{symbol}') → {dest}")

states = {'A', 'B', 'C', 'D', 'E', 'F'}
alphabet = {'0', '1'}
transition = {
    ('A', '0'): 'B', ('A', '1'): 'C',
    ('B', '0'): 'A', ('B', '1'): 'D',
    ('C', '0'): 'E', ('C', '1'): 'F',
    ('D', '0'): 'E', ('D', '1'): 'F',
    ('E', '0'): 'E', ('E', '1'): 'F',
    ('F', '0'): 'F', ('F', '1'): 'F'
}
start_state = 'A'
accept_states = {'E'}

dfa = DFA(states, alphabet, transition, start_state, accept_states)
print("Original DFA:")
dfa.print_dfa()

min_dfa = dfa.minimize()
print("\nMinimized DFA:")
min_dfa.print_dfa()
