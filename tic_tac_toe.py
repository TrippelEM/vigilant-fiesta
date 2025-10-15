import math
import time
from copy import deepcopy
from halving_game import minimax_search
State = tuple[int, list[list[int | None]]]  # Tuple of player (whose turn it is),
                                            # and board
Action = tuple[int, int]  # Where to place the player's piece

class Game:
    def initial_state(self) -> State:
        return (0, [[None, None, None], [None, None, None], [None, None, None]])

    def to_move(self, state: State) -> int:
        player_index, _ = state
        return player_index

    def actions(self, state: State) -> list[Action]:
        _, board = state
        actions = []
        for row in range(3):
            for col in range(3):
                if board[row][col] is None:
                    actions.append((row, col))
        return actions

    def result(self, state: State, action: Action) -> State:
        _, board = state
        row, col = action
        next_board = deepcopy(board)
        next_board[row][col] = self.to_move(state)
        return (self.to_move(state) + 1) % 2, next_board

    def is_winner(self, state: State, player: int) -> bool:
        _, board = state
        for row in range(3):
            if all(board[row][col] == player for col in range(3)):
                return True
        for col in range(3):
            if all(board[row][col] == player for row in range(3)):
                return True
        if all(board[i][i] == player for i in range(3)):
            return True
        return all(board[i][2 - i] == player for i in range(3))

    def is_terminal(self, state: State) -> bool:
        _, board = state
        if self.is_winner(state, (self.to_move(state) + 1) % 2):
            return True
        return all(board[row][col] is not None for row in range(3) for col in range(3))

    def utility(self, state, player):
        assert self.is_terminal(state)
        if self.is_winner(state, player):
            return 1
        if self.is_winner(state, (player + 1) % 2):
            return -1
        return 0

    def print(self, state: State):
        _, board = state
        print()
        for row in range(3):
            cells = [
                ' ' if board[row][col] is None else 'x' if board[row][col] == 0 else 'o'
                for col in range(3)
            ]
            print(f' {cells[0]} | {cells[1]} | {cells[2]}')
            if row < 2:
                print('---+---+---')
        print()
        if self.is_terminal(state):
            if self.utility(state, 0) > 0:
                print(f'P1 won')
            elif self.utility(state, 1) > 0:
                print(f'P2 won')
            else:
                print('The game is a draw')
        else:
            print(f'It is P{self.to_move(state)+1}\'s turn to move')

def alpha_beta_search(game:Game, state: State) -> Action:
    player = game.to_move(state)
    value, move = max_value(game,state,-math.inf,math.inf,player)
    return move

def max_value(game:Game, state:State,alpha:float, beta:float, player:int) -> tuple[int, Action | None]:
    if game.is_terminal(state): return game.utility(state, player), None
    v, move = -math.inf, None
    for a in game.actions(state):
        v2, a2 = min_value(game, game.result(state, a), alpha, beta, player)
        if v2 > v:
            v, move = v2, a
            alpha = max(alpha, v)
        if v >= beta: return v, move
    return v, move

def min_value(game:Game, state:State,alpha:float, beta:float, player:int) -> tuple[int, Action | None]:
    if game.is_terminal(state): return game.utility(state, player), None
    v, move = math.inf, None
    for a in game.actions(state):
        v2, a2 = max_value(game, game.result(state, a), alpha, beta, player)
        if v2 < v:
            v, move = v2, a
            beta = min(beta, v)
        if v <= alpha: return v, move
    return v, move

def main():
    game = Game()
    state = game.initial_state()
    game.print(state)
    start_time = time.perf_counter()
    while not game.is_terminal(state):
        cur_player = game.to_move(state)
        action = alpha_beta_search(game, state) # The player whose turn it is
                                                # is the MAX player
        print(f'P{cur_player+1}\'s action: {action}')
        assert action is not None
        state = game.result(state, action)
        game.print(state)
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(f"alpha-beta pruning execution time: {elapsed_time:.4f} seconds")

    game = Game()
    state = game.initial_state()
    game.print(state)
    start_time = time.perf_counter()
    while not game.is_terminal(state):
        cur_player = game.to_move(state)
        action = minimax_search(game, state) # The player whose turn it is
                                                # is the MAX player
        print(f'P{cur_player+1}\'s action: {action}')
        assert action is not None
        state = game.result(state, action)
        game.print(state)
    end_time = time.perf_counter()
    elapsed_time = end_time - start_time
    print(f"minimax execution time: {elapsed_time:.4f} seconds")


if __name__ == "__main__":
    main()
