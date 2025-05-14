from collections import defaultdict
import string
import itertools

class CFGtoCNFConverter:
    def __init__(self, productions, start_symbol):
        self.productions = defaultdict(list)
        self.start_symbol = start_symbol
        self.non_terminals = set()
        self.terminals = set()
        self.counter = 0
        for lhs, rhs_list in productions.items():
            self.non_terminals.add(lhs)
            for rhs in rhs_list:
                self.productions[lhs].append(rhs)
                for symbol in rhs:
                    if symbol.islower() or symbol in string.punctuation:
                        self.terminals.add(symbol)
                    elif symbol.isupper():
                        self.non_terminals.add(symbol)

    def get_new_non_terminal(self):
        while True:
            nt = f"X{self.counter}"
            self.counter += 1
            if nt not in self.non_terminals:
                self.non_terminals.add(nt)
                return nt

    def remove_epsilon_productions(self):
        nullable = set()
        for lhs in self.productions:
            for rhs in self.productions[lhs]:
                if rhs == ['ε']:
                    nullable.add(lhs)

        changed = True
        while changed:
            changed = False
            for lhs in self.productions:
                for rhs in self.productions[lhs]:
                    if all(symbol in nullable for symbol in rhs):
                        if lhs not in nullable:
                            nullable.add(lhs)
                            changed = True

        new_productions = defaultdict(list)
        for lhs in self.productions:
            for rhs in self.productions[lhs]:
                subsets = [i for i in range(len(rhs)) if rhs[i] in nullable]
                for bits in itertools.product((0, 1), repeat=len(subsets)):
                    new_rhs = list(rhs)
                    for index, bit in zip(subsets, bits):
                        if bit == 1:
                            new_rhs[index] = None
                    new_rhs = [x for x in new_rhs if x is not None]
                    if new_rhs != []:
                        if new_rhs not in new_productions[lhs]:
                            new_productions[lhs].append(new_rhs)

        self.productions = new_productions

    def remove_unit_productions(self):
        new_productions = defaultdict(list)
        for lhs in self.productions:
            for rhs in self.productions[lhs]:
                new_productions[lhs].append(rhs)

        changed = True
        while changed:
            changed = False
            for lhs in list(new_productions.keys()):
                to_add = []
                for rhs in new_productions[lhs]:
                    if len(rhs) == 1 and rhs[0] in self.non_terminals:
                        B = rhs[0]
                        for prod in new_productions[B]:
                            if prod not in new_productions[lhs]:
                                to_add.append(prod)
                                changed = True
                new_productions[lhs] += to_add

        self.productions = defaultdict(list)
        for lhs, rhs_list in new_productions.items():
            for rhs in rhs_list:
                if not (len(rhs) == 1 and rhs[0] in self.non_terminals and lhs != rhs[0]):
                    self.productions[lhs].append(rhs)

    def eliminate_terminals_in_long_rules(self):
        terminal_map = {}
        new_productions = defaultdict(list)

        for lhs in self.productions:
            for rhs in self.productions[lhs]:
                new_rhs = []
                for symbol in rhs:
                    if symbol in self.terminals and len(rhs) > 1:
                        if symbol not in terminal_map:
                            new_nt = self.get_new_non_terminal()
                            terminal_map[symbol] = new_nt
                            new_productions[new_nt].append([symbol])
                        new_rhs.append(terminal_map[symbol])
                    else:
                        new_rhs.append(symbol)
                new_productions[lhs].append(new_rhs)

        self.productions = new_productions

    def convert_to_binary_rules(self):
        new_productions = defaultdict(list)

        for lhs in self.productions:
            for rhs in self.productions[lhs]:
                while len(rhs) > 2:
                    new_nt = self.get_new_non_terminal()
                    new_productions[new_nt].append(rhs[1:])
                    rhs = [rhs[0], new_nt]
                new_productions[lhs].append(rhs)

        self.productions = new_productions

    def convert(self):
        self.remove_epsilon_productions()
        self.remove_unit_productions()
        self.eliminate_terminals_in_long_rules()
        self.convert_to_binary_rules()

    def print_cnf(self):
        print("CNF Productions:")
        for lhs in self.productions:
            for rhs in self.productions[lhs]:
                print(f"{lhs} -> {' '.join(rhs)}")

# --- Sample Usage ---
if __name__ == "__main__":
    # Sample grammar
    productions = {
        "S": [["A", "B"], ["B", "C"]],
        "A": [["B", "A"], ["a"]],
        "B": [["C", "C"], ["b"], ["ε"]],
        "C": [["A", "B"], ["a"]]
    }

    start_symbol = "S"
    converter = CFGtoCNFConverter(productions, start_symbol)
    converter.convert()
    converter.print_cnf()
