import random


class Game:
    deck = ["2c", "2d", "2h", "2s", "3c", "3d", "3h", "3s", "4c", "4d", "4h", "4s", "5c", "5d", "5h", "5s",
            "6c", "6d", "6h", "6s", "7c", "7d", "7h", "7s", "8c", "8d", "8h", "8s", "9c", "9d", "9h", "9s",
            "Tc", "Td", "Th", "Ts", "Jc", "Jd", "Jh", "Js", "Qc", "Qd", "Qh", "Qs", "Kc", "Kd", "Kh", "Ks",
            "Ac", "Ad", "Ah", "As"]

    def __init__(self):
        self.table = []
        self.free = []
        self.home = []
        self.history = []

    def start(self):
        random.shuffle(Game.deck)
        self.table = [[] for i in range(8)]
        for i in range(6):
            for j in range(8):
                self.table[j].append(Game.deck[8 * i + j])
        for i in range(4):
            self.table[i].append(Game.deck[i + 48])
        self.free = []
        self.home = [[] for i in range(4)]
        self.history = []

    def red(self, card):
        return card[1] == 'd' or card[1] == 'h'

    def value(self, card):
        if card[0] == 'T':
            return 10
        if card[0] == 'J':
            return 11
        if card[0] == 'Q':
            return 12
        if card[0] == 'K':
            return 13
        if card[0] == 'A':
            return 1
        return ord(card[0]) - 48

    def move_column(self, src, dst):
        if (self.red(self.table[src][-1]) == self.red(self.table[dst][-1])
                or self.value(self.table[src][-1]) + 1 != self.value(self.table[dst][-1])):
            return False
        self.table[dst].append(self.table[src].pop())
        self.expand_history()
        return True

    def move_to_free(self, src):
        if len(self.free) >= 4:
            return False
        self.free.append(self.table[src].pop())
        self.expand_history()
        return True

    def move_from_free(self, src, dst):
        if (self.red(self.free[src]) == self.red(self.table[dst][-1])
                or self.value(self.free[src]) + 1 != self.value(self.table[dst][-1])):
            return False
        self.table[dst].append(self.free.pop(src))
        self.expand_history()
        return True

    def column_to_home(self, src, dst):
        if (self.table[src][-1][1] != self.home[dst][-1][1]
                or self.value(self.table[src][-1]) != self.value(self.home[dst][-1]) + 1):
            return False
        self.home[dst].append(self.table[src].pop())
        self.expand_history()
        return True

    def free_to_home(self, src, dst):
        if (self.free[src][1] != self.home[dst][-1][1]
                or self.value(self.free[src]) != self.value(self.home[dst][-1]) + 1):
            return False
        self.home[dst].append(self.free.pop(src))
        self.expand_history()
        return True

    def expand_history(self):
        self.history.append((
            [[self.table[i][j] for j in range(len(self.table[i]))] for i in range(len(self.table))],
            [self.free[i] for i in range(len(self.free))],
            [self.home[i] for i in range(len(self.home))]
        ))


def main():
    print("Welcome to the FreeCell Solver!")


if __name__ == "__main__":
    main()
