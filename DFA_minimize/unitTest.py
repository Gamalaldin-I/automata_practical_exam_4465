import unittest
from DFAminimizer import DFA  

class TestDFAMinimization(unittest.TestCase):
    def setUp(self):
        self.states = {'A', 'B', 'C', 'D', 'E', 'F'}
        self.alphabet = {'0', '1'}
        self.transition = {
            ('A', '0'): 'B', ('A', '1'): 'C',
            ('B', '0'): 'A', ('B', '1'): 'D',
            ('C', '0'): 'E', ('C', '1'): 'F',
            ('D', '0'): 'E', ('D', '1'): 'F',
            ('E', '0'): 'E', ('E', '1'): 'F',
            ('F', '0'): 'F', ('F', '1'): 'F'
        }
        self.start_state = 'A'
        self.accept_states = {'E'}
        self.dfa = DFA(self.states, self.alphabet, self.transition, self.start_state, self.accept_states)

    def test_minimized_dfa_states_count(self):
        min_dfa = self.dfa.minimize()
        self.assertEqual(len(min_dfa.states), 4)

    def test_minimized_dfa_accept_states(self):
        min_dfa = self.dfa.minimize()
        self.assertEqual(len(min_dfa.accept_states), 1)

    def test_minimized_dfa_start_state_valid(self):
        min_dfa = self.dfa.minimize()
        self.assertIn(min_dfa.start_state, min_dfa.states)

    def test_transitions_maintain_validity(self):
        min_dfa = self.dfa.minimize()
        for (state, symbol), next_state in min_dfa.transition.items():
            self.assertIn(symbol, self.alphabet)
            self.assertIn(state, min_dfa.states)
            self.assertIn(next_state, min_dfa.states)

if __name__ == '__main__':
    unittest.main()
