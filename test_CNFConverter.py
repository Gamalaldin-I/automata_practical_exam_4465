import unittest
from collections import defaultdict
from CNFConverter import CFGtoCNFConverter  # Assuming your code is in cfg_to_cnf.py

class TestCFGtoCNFConverter(unittest.TestCase):
    def setUp(self):
        # Common setup if needed
        pass

    def test_simple_cnf_conversion(self):
        """Test conversion of a simple CFG to CNF"""
        productions = {
            "S": [["A", "B"], ["a"]],
            "A": [["a"]],
            "B": [["b"]]
        }
        start_symbol = "S"
        converter = CFGtoCNFConverter(productions, start_symbol)
        converter.convert()
        
        # Expected CNF productions
        expected = {
            "S": [["A", "B"], ["a"]],
            "A": [["a"]],
            "B": [["b"]]
        }
        
        self.assert_productions_equal(converter.productions, expected)

    def test_epsilon_removal(self):
        """Test removal of epsilon productions"""
        productions = {
            "S": [["A", "B"]],
            "A": [["a"], ["ε"]],
            "B": [["b"], ["ε"]]
        }
        start_symbol = "S"
        converter = CFGtoCNFConverter(productions, start_symbol)
        converter.remove_epsilon_productions()
        
        # Expected after epsilon removal
        expected = {
            "S": [["A", "B"], ["A"], ["B"]],
            "A": [["a"]],
            "B": [["b"]]
        }
        
        self.assert_productions_equal(converter.productions, expected)

    def test_unit_production_removal(self):
        """Test removal of unit productions"""
        productions = {
            "S": [["A"], ["a"]],
            "A": [["B"], ["b"]],
            "B": [["C"], ["c"]],
            "C": [["D"]],
            "D": [["d"]]
        }
        start_symbol = "S"
        converter = CFGtoCNFConverter(productions, start_symbol)
        converter.remove_unit_productions()
        
        # Expected after unit production removal
        expected = {
            "S": [["a"], ["b"], ["c"], ["d"]],
            "A": [["b"], ["c"], ["d"]],
            "B": [["c"], ["d"]],
            "C": [["d"]],
            "D": [["d"]]
        }
        
        self.assert_productions_equal(converter.productions, expected)

    def test_terminal_elimination_in_long_rules(self):
        """Test elimination of terminals in long rules"""
        productions = {
            "S": [["A", "b", "C"]],
            "A": [["a"]],
            "C": [["c"]]
        }
        start_symbol = "S"
        converter = CFGtoCNFConverter(productions, start_symbol)
        converter.eliminate_terminals_in_long_rules()
        
        # Should have new non-terminals for terminals in long rules
        self.assertEqual(len(converter.productions), 4)  # S, A, C, and new X for 'b'
        
        # Check that 'b' was replaced with a new non-terminal
        s_productions = converter.productions["S"]
        self.assertEqual(len(s_productions[0]), 3)
        self.assertTrue(s_productions[0][1].startswith("X"))  # The new NT for 'b'

    def test_binary_rule_conversion(self):
        """Test conversion to binary rules"""
        productions = {
            "S": [["A", "B", "C", "D"]],
            "A": [["a"]],
            "B": [["b"]],
            "C": [["c"]],
            "D": [["d"]]
        }
        start_symbol = "S"
        converter = CFGtoCNFConverter(productions, start_symbol)
        converter.convert_to_binary_rules()
        
        # Original rule should be broken down into binary rules
        s_productions = converter.productions["S"]
        self.assertEqual(len(s_productions[0]), 2)
        
        # Should have new non-terminals for the breakdown
        self.assertGreater(len(converter.productions), 5)  # Original 5 plus new ones

    def test_full_conversion(self):
        """Test full CNF conversion with the sample grammar"""
        productions = {
            "S": [["A", "B"], ["B", "C"]],
            "A": [["B", "A"], ["a"]],
            "B": [["C", "C"], ["b"], ["ε"]],
            "C": [["A", "B"], ["a"]]
        }
        start_symbol = "S"
        converter = CFGtoCNFConverter(productions, start_symbol)
        converter.convert()
        
        # Verify all productions are in CNF
        for lhs, rhs_list in converter.productions.items():
            for rhs in rhs_list:
                self.assertTrue(
                    len(rhs) == 1 and rhs[0] in converter.terminals or  # Terminal
                    len(rhs) == 2 and all(s in converter.non_terminals for s in rhs),  # Two non-terminals
                    f"Production {lhs} -> {' '.join(rhs)} is not in CNF"
                )

    def assert_productions_equal(self, actual, expected):
        """Helper method to compare productions, ignoring order"""
        actual_dict = defaultdict(list)
        for lhs, rhs_list in actual.items():
            for rhs in rhs_list:
                actual_dict[lhs].append(rhs)
        
        expected_dict = defaultdict(list)
        for lhs, rhs_list in expected.items():
            for rhs in rhs_list:
                expected_dict[lhs].append(rhs)
        
        self.assertEqual(actual_dict.keys(), expected_dict.keys())
        
        for lhs in actual_dict:
            # Compare lists of productions as sets (order doesn't matter)
            self.assertEqual(
                set(tuple(rhs) for rhs in actual_dict[lhs]),
                set(tuple(rhs) for rhs in expected_dict[lhs]),
                f"Productions for {lhs} don't match"
            )

if __name__ == "__main__":
    unittest.main()
