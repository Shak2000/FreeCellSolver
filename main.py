import random
import copy


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
        # Mapping for suits to home cell indices
        self.suit_to_home_idx = {'c': 0, 'd': 1, 'h': 2, 's': 3}

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
        # Initialize home cells with a "0" card of each suit for easier value comparison
        self.home[0].append("0c")  # Clubs
        self.home[1].append("0d")  # Diamonds
        self.home[2].append("0h")  # Hearts
        self.home[3].append("0s")  # Spades
        self.history = []
        self.expand_history()  # Save initial state

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
        # For the "0" cards in home cells
        if card[0] == '0':
            return 0
        return int(card[0])

    def move_column(self, src, dst):
        # Check if source column is empty
        if not self.table[src]:
            return False

        # If destination column is empty, any card can be moved
        if not self.table[dst]:
            self.expand_history()
            self.table[dst].append(self.table[src].pop())
            return True

        # Check for valid move: alternating colors and descending value
        if (self.red(self.table[src][-1]) == self.red(self.table[dst][-1])
                or self.value(self.table[src][-1]) + 1 != self.value(self.table[dst][-1])):
            return False
        self.expand_history()
        self.table[dst].append(self.table[src].pop())
        return True

    def move_to_free(self, src):
        # Check if source column is empty
        if not self.table[src]:
            return False

        if len(self.free) >= 4:
            return False
        self.expand_history()
        self.free.append(self.table[src].pop())
        return True

    def move_from_free(self, src, dst):
        # Check if free cell is empty
        if src >= len(self.free):
            return False

        # If destination column is empty, any card can be moved
        if not self.table[dst]:
            self.expand_history()
            self.table[dst].append(self.free.pop(src))
            return True

        # Check for valid move: alternating colors and descending value
        if (self.red(self.free[src]) == self.red(self.table[dst][-1])
                or self.value(self.free[src]) + 1 != self.value(self.table[dst][-1])):
            return False
        self.expand_history()
        self.table[dst].append(self.free.pop(src))
        return True

    def column_to_home(self, src):  # Removed dst parameter
        # Check if source column is empty
        if not self.table[src]:
            return False

        card_to_move = self.table[src][-1]
        suit = card_to_move[1]
        dst = self.suit_to_home_idx.get(suit)

        if dst is None:  # Should not happen with valid cards
            return False

        # Check for valid move: same suit and ascending value
        if (card_to_move[1] != self.home[dst][-1][1]
                or self.value(card_to_move) != self.value(self.home[dst][-1]) + 1):
            return False
        self.expand_history()
        self.home[dst].append(self.table[src].pop())
        return True

    def free_to_home(self, src):  # Removed dst parameter
        # Check if free cell is empty
        if src >= len(self.free):
            return False

        card_to_move = self.free[src]
        suit = card_to_move[1]
        dst = self.suit_to_home_idx.get(suit)

        if dst is None:  # Should not happen with valid cards
            return False

        # Check for valid move: same suit and ascending value
        if (card_to_move[1] != self.home[dst][-1][1]
                or self.value(card_to_move) != self.value(self.home[dst][-1]) + 1):
            return False
        self.expand_history()
        self.home[dst].append(self.free.pop(src))
        return True

    def expand_history(self):
        # Deep copy the current state to history
        self.history.append((
            copy.deepcopy(self.table),
            copy.deepcopy(self.free),
            copy.deepcopy(self.home)
        ))

    def undo(self):
        if len(self.history) > 1:  # Keep at least the initial state
            self.history.pop()
            # Restore the previous state
            self.table, self.free, self.home = copy.deepcopy(self.history[-1])
            return True
        return False

    def is_game_won(self):
        # Check if all home cells are full (King of each suit)
        return all(self.value(home[-1]) == 13 for home in self.home)

    def get_possible_moves(self):
        moves = []
        # 1. Column to Column
        for src in range(8):
            if self.table[src]:
                for dst in range(8):
                    if src != dst:
                        temp_game = copy.deepcopy(self)
                        if temp_game.move_column(src, dst):
                            moves.append(('column_to_column', src, dst))

        # 2. Column to FreeCell
        for src in range(8):
            if self.table[src]:
                temp_game = copy.deepcopy(self)
                if temp_game.move_to_free(src):
                    moves.append(('column_to_free', src))

        # 3. FreeCell to Column
        for src_idx in range(len(self.free)):
            for dst in range(8):
                temp_game = copy.deepcopy(self)
                if temp_game.move_from_free(src_idx, dst):
                    moves.append(('free_to_column', src_idx, dst))

        # 4. Column to HomeCell (No longer needs dst parameter)
        for src in range(8):
            if self.table[src]:
                temp_game = copy.deepcopy(self)
                if temp_game.column_to_home(src):  # Removed dst here
                    moves.append(('column_to_home', src))  # Changed move tuple

        # 5. FreeCell to HomeCell (No longer needs dst parameter)
        for src_idx in range(len(self.free)):
            temp_game = copy.deepcopy(self)
            if temp_game.free_to_home(src_idx):  # Removed dst here
                moves.append(('free_to_home', src_idx))  # Changed move tuple
        return moves

    def display_game(self):
        print("\n--- Current Game State ---")
        print("Free Cells:")
        if self.free:
            print("  " + " | ".join(self.free))
        else:
            print("  Empty")

        print("\nHome Cells:")
        # Display only the top card of home cells, excluding the "0" initializer
        home_display = []
        for h_cell in self.home:
            if len(h_cell) > 1:  # If there's a card on top of "0"
                home_display.append(h_cell[-1])
            else:
                home_display.append("Empty")
        print("  " + " | ".join(home_display))

        print("\nTable Columns:")
        # Determine the maximum height of any column for formatted printing
        max_height = max(len(col) for col in self.table) if self.table else 0

        # Print cards row by row
        for i in range(max_height):
            row_str = "  "
            for j in range(8):
                if i < len(self.table[j]):
                    row_str += f"{self.table[j][i]:<5}"  # Left-align card string
                else:
                    row_str += "     "  # Empty space for shorter columns
            print(row_str)
        print("--------------------------\n")

    @staticmethod
    def get_user_input(prompt):
        return input(prompt)

    def apply_move(self, game_instance, move):  # Helper for MCTS, can be static or part of Game
        move_type = move[0]
        if move_type == 'column_to_column':
            game_instance.move_column(move[1], move[2])
        elif move_type == 'column_to_free':
            game_instance.move_to_free(move[1])
        elif move_type == 'free_to_column':
            game_instance.move_from_free(move[1], move[2])
        elif move_type == 'column_to_home':
            game_instance.column_to_home(move[1])  # No dst parameter here
        elif move_type == 'free_to_home':
            game_instance.free_to_home(move[1])  # No dst parameter here

    def computer_play(self, simulations=100):
        root = MCTSNode(self)

        for _ in range(simulations):
            node = root
            # Selection
            while node.children and not node.unexplored_moves:
                node = node.select_child()

            # Expansion
            if node.unexplored_moves:
                node = node.expand()

            # Simulation
            result = node.simulate()

            # Backpropagation
            node.backpropagate(result)

        # Choose the best move from the root's children
        best_move = None
        best_win_rate = -1

        if not root.children:
            return None  # No possible moves from current state

        for child in root.children:
            if child.visits > 0:
                win_rate = child.wins / child.visits
                if win_rate > best_win_rate:
                    best_win_rate = win_rate
                    best_move = child.move

        return best_move


class MCTSNode:
    def __init__(self, game_state, parent=None, move=None):
        self.game_state = game_state
        self.parent = parent
        self.move = move
        self.children = []
        self.wins = 0
        self.visits = 0
        self.unexplored_moves = game_state.get_possible_moves()

    def ucb1(self, c_param=1.4):
        if self.visits == 0:
            return float('inf')
        return (self.wins / self.visits) + c_param * (self.parent.visits ** 0.5 / self.visits ** 0.5)

    def select_child(self):
        return max(self.children, key=lambda child: child.ucb1())

    def expand(self):
        move = self.unexplored_moves.pop()
        new_game_state = copy.deepcopy(self.game_state)
        Game().apply_move(new_game_state, move)
        child_node = MCTSNode(new_game_state, parent=self, move=move)
        self.children.append(child_node)
        return child_node

    def simulate(self):
        current_game = copy.deepcopy(self.game_state)
        max_moves = 20
        for _ in range(max_moves):
            if current_game.is_game_won():
                return True
            possible_moves = current_game.get_possible_moves()
            if not possible_moves:
                return False

            home_moves = [m for m in possible_moves if m[0] == 'column_to_home' or m[0] == 'free_to_home']
            if home_moves:
                move = random.choice(home_moves)
            else:
                move = random.choice(possible_moves)

            Game().apply_move(current_game, move)
        return False

    def backpropagate(self, result):
        self.visits += 1
        if result:
            self.wins += 1
        if self.parent:
            self.parent.backpropagate(result)


def main():
    print("Welcome to the FreeCell Solver!")
    game = Game()

    while True:
        choice_str = game.get_user_input("Enter (1) to start a new game or (2) to quit: ")
        try:
            choice = int(choice_str)
        except ValueError:
            print("Invalid input. Please enter a number.")
            continue

        if choice == 1:
            game.start()
            game.display_game()

            while True:
                if game.is_game_won():
                    print("Congratulations! You won the game!")
                    break

                print("What would you like to do?")
                print("(1) Move a card between columns")
                print("(2) Move a card from a column to a FreeCell")
                print("(3) Move a card from a FreeCell to a column")
                print("(4) Move a card from a column to its HomeCell")  # Updated description
                print("(5) Move a card from a FreeCell to its HomeCell")  # Updated description
                print("(6) Have the computer play a move")
                print("(7) Undo a move")
                print("(8) Start a new game")
                print("(9) Quit")

                game_choice_str = game.get_user_input("Enter your choice: ")
                try:
                    game_choice = int(game_choice_str)
                except ValueError:
                    print("Invalid input. Please enter a number.")
                    game.display_game()
                    continue

                if game_choice == 1:
                    src_str = game.get_user_input("Enter source column (0-7): ")
                    dst_str = game.get_user_input("Enter destination column (0-7): ")
                    try:
                        src = int(src_str)
                        dst = int(dst_str)
                        if 0 <= src <= 7 and 0 <= dst <= 7:
                            if game.move_column(src, dst):
                                print("Move successful!")
                            else:
                                print("Invalid move. Please try again.")
                        else:
                            print("Invalid column numbers (must be 0-7).")
                    except ValueError:
                        print("Invalid input. Please enter numbers for columns.")
                elif game_choice == 2:
                    src_str = game.get_user_input("Enter source column (0-7): ")
                    try:
                        src = int(src_str)
                        if 0 <= src <= 7:
                            if game.move_to_free(src):
                                print("Move successful!")
                            else:
                                print("Invalid move. FreeCells might be full or source column empty.")
                        else:
                            print("Invalid column number (must be 0-7).")
                    except ValueError:
                        print("Invalid input. Please enter a number for the column.")
                elif game_choice == 3:
                    src_str = game.get_user_input("Enter FreeCell index (0-3): ")
                    dst_str = game.get_user_input("Enter destination column (0-7): ")
                    try:
                        src = int(src_str)
                        dst = int(dst_str)
                        if 0 <= src <= 3 and 0 <= dst <= 7:
                            if game.move_from_free(src, dst):
                                print("Move successful!")
                            else:
                                print("Invalid move. Check FreeCell index or destination column.")
                        else:
                            print("Invalid FreeCell (0-3) or column number (0-7).")
                    except ValueError:
                        print("Invalid input. Please enter numbers for FreeCell and column.")
                elif game_choice == 4:  # No longer asks for dst
                    src_str = game.get_user_input("Enter source column (0-7): ")
                    try:
                        src = int(src_str)
                        if 0 <= src <= 7:
                            if game.column_to_home(src):  # Removed dst here
                                print("Move successful!")
                            else:
                                print("Invalid move. Card might not fit in its HomeCell or source column empty.")
                        else:
                            print("Invalid column number (must be 0-7).")
                    except ValueError:
                        print("Invalid input. Please enter a number for the column.")
                elif game_choice == 5:  # No longer asks for dst
                    src_str = game.get_user_input("Enter FreeCell index (0-3): ")
                    try:
                        src = int(src_str)
                        if 0 <= src <= 3:
                            if game.free_to_home(src):  # Removed dst here
                                print("Move successful!")
                            else:
                                print("Invalid move. Card might not fit in its HomeCell or FreeCell empty.")
                        else:
                            print("Invalid FreeCell number (must be 0-3).")
                    except ValueError:
                        print("Invalid input. Please enter a number for the FreeCell.")
                elif game_choice == 6:
                    print("Computer is thinking...")
                    best_move = game.computer_play(simulations=100)
                    if best_move:
                        print(f"Computer decided to make move: {best_move}")
                        game.apply_move(game, best_move)
                        print("Computer move executed!")
                    else:
                        print("Computer could not find a valid move or game is stuck.")
                elif game_choice == 7:
                    if game.undo():
                        print("Undo successful!")
                    else:
                        print("Cannot undo further.")
                elif game_choice == 8:
                    print("Starting a new game...")
                    game.start()
                elif game_choice == 9:
                    print("Quitting game. Goodbye!")
                    break
                else:
                    print("Invalid choice. Please enter a number between 1 and 9.")

                game.display_game()

        elif choice == 2:
            print("Quitting FreeCell Solver. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1 or 2.")


if __name__ == "__main__":
    main()
