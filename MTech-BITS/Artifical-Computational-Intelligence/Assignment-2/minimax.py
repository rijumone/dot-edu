from dataclasses import dataclass


@dataclass
class GameState:
    remaining_numbers: list
    player1_sum: int
    player2_sum: int
    current_player: int


def initialize_game_state(n):
    remaining_numbers = list(range(1, n + 1))
    player1_sum = 0
    player2_sum = 0
    current_player = 0
    return GameState(remaining_numbers, player1_sum, player2_sum, current_player)


def minimax(state, depth, maximizing_player):
    if depth == 0 or not state.remaining_numbers:
        # Return the evaluation of the state based on the current player
        return evaluate_state(state, maximizing_player)

    if maximizing_player:
        max_value = float('-inf')
        for move in state.remaining_numbers:
            new_remaining_numbers = state.remaining_numbers[:]
            new_remaining_numbers.remove(move)
            new_player1_sum = state.player1_sum + move
            new_player2_sum = state.player2_sum
            new_state = GameState(
                new_remaining_numbers, new_player1_sum, new_player2_sum, 1 - state.current_player)
            value = minimax(new_state, depth - 1, False)
            max_value = max(max_value, value)
        return max_value
    else:
        min_value = float('inf')
        for move in state.remaining_numbers:
            new_remaining_numbers = state.remaining_numbers[:]
            new_remaining_numbers.remove(move)
            new_player1_sum = state.player1_sum
            new_player2_sum = state.player2_sum + move
            new_state = GameState(
                new_remaining_numbers, new_player1_sum, new_player2_sum, 1 - state.current_player)
            value = minimax(new_state, depth - 1, True)
            min_value = min(min_value, value)
        return min_value


def alpha_beta(state, depth, alpha, beta, maximizing_player):
    if depth == 0 or not state.remaining_numbers:
        return evaluate_state(state, maximizing_player)

    if maximizing_player:
        max_value = float('-inf')
        for move in state.remaining_numbers:
            new_remaining_numbers = state.remaining_numbers[:]
            new_remaining_numbers.remove(move)
            new_player1_sum = state.player1_sum + move
            new_player2_sum = state.player2_sum
            new_state = GameState(
                new_remaining_numbers, new_player1_sum, new_player2_sum, 1 - state.current_player)
            value = alpha_beta(new_state, depth - 1, alpha, beta, False)
            max_value = max(max_value, value)
            alpha = max(alpha, value)
            if beta <= alpha:
                break
        return max_value
    else:
        min_value = float('inf')
        for move in state.remaining_numbers:
            new_remaining_numbers = state.remaining_numbers[:]
            new_remaining_numbers.remove(move)
            new_player1_sum = state.player1_sum
            new_player2_sum = state.player2_sum + move
            new_state = GameState(
                new_remaining_numbers, new_player1_sum, new_player2_sum, 1 - state.current_player)
            value = alpha_beta(new_state, depth - 1, alpha, beta, True)
            min_value = min(min_value, value)
            beta = min(beta, value)
            if beta <= alpha:
                break
        return min_value


def evaluate_state(state, maximizing_player):
    # Return the difference between player sums if maximizing player is Player 1,
    # otherwise return the difference multiplied by -1 for Player 2
    if maximizing_player:
        return state.player1_sum - state.player2_sum
    else:
        return state.player2_sum - state.player1_sum


def player_move1(player, state, human_players):
    print('===================================')
    print("Player", player + 1, "'s turn.")
    print("Current sum for Player 1:", state.player1_sum)
    print("Current sum for Player 2:", state.player2_sum)
    print("Remaining numbers:", state.remaining_numbers)

    if human_players and player == 0:
        while True:
            move = int(input("Enter your move: "))
            if move in state.remaining_numbers:
                state.remaining_numbers.remove(move)
                state.player1_sum += move
                return state
            else:
                print("Invalid move. Please choose from the remaining numbers.")
    else:
        best_move = None
        best_value = float('-inf') if player == 0 else float('inf')
        for move in state.remaining_numbers:
            new_remaining_numbers = state.remaining_numbers[:]
            new_remaining_numbers.remove(move)
            new_player1_sum = state.player1_sum + move if player == 0 else state.player1_sum
            new_player2_sum = state.player2_sum + move if player == 1 else state.player2_sum
            new_state = GameState(
                new_remaining_numbers, new_player1_sum, new_player2_sum, 1 - state.current_player)
            value = minimax(new_state, len(
                new_state.remaining_numbers), player == 0)
            if (player == 0 and value > best_value) or (player == 1 and value < best_value):
                best_move = move
                best_value = value

        state.remaining_numbers.remove(best_move)
        state.player1_sum += best_move if player == 0 else 0
        state.player2_sum += best_move if player == 1 else 0
        print("AI Player", player + 1, "chooses:", best_move)
        print('+++++++++++++++++++++++++++++++++++')
        return state


def player_move(player, state, human_players, depth):
    print('\n\t================================================')
    print("Player", player + 1, "'s turn.")
    print("Current sum for Player 1:", state.player1_sum)
    print("Current sum for Player 2:", state.player2_sum)
    print("Remaining numbers:", state.remaining_numbers)
    
    if human_players and player == 0:
        while True:
            move = input("Enter your move (comma-separated numbers, e.g., '1,2,3'): ")
            moves = [int(x) for x in move.split(',')]
            if all(num in state.remaining_numbers for num in moves):
                if sum(moves) > state.player2_sum:
                    for num in moves:
                        state.player1_sum += num
                        state.remaining_numbers.remove(num)
                    return state
                else:
                    print("Sum of your choices must exceed your opponent's previous sum.")
            else:
                print("Invalid move. Please choose from the remaining numbers.")
    else:
        best_move = None
        best_value = float('-inf') if player == 0 else float('inf')
        for move in state.remaining_numbers:
            new_remaining_numbers = state.remaining_numbers[:]
            new_remaining_numbers.remove(move)
            new_player1_sum = state.player1_sum + move if player == 0 else state.player1_sum
            new_player2_sum = state.player2_sum + move if player == 1 else state.player2_sum
            if (player == 0 and new_player1_sum > state.player2_sum) or (player == 1 and new_player2_sum > state.player1_sum):
                new_state = GameState(new_remaining_numbers, new_player1_sum, new_player2_sum, 1 - state.current_player)
                value = alpha_beta(new_state, depth - 1, float('-inf'), float('inf'), player == 0)
                if (player == 0 and value > best_value) or (player == 1 and value < best_value):
                    best_move = move
                    best_value = value
        
        if best_move is None:
            best_move = min(state.remaining_numbers)
        
        state.player1_sum += best_move if player == 0 else 0
        state.player2_sum += best_move if player == 1 else 0
        print("AI Player", player + 1, "chooses:", best_move)
        state.remaining_numbers.remove(best_move)
        return state


def play_catch_up(n, human_players):
    state = initialize_game_state(n)
    depth = 3  # Set the depth for AI search

    while state.remaining_numbers:
        state = player_move(state.current_player, state, human_players, depth)
        state.current_player = 1 - state.current_player

    print("Game Over!")
    print("Final sum for Player 1:", state.player1_sum)
    print("Final sum for Player 2:", state.player2_sum)

    if state.player1_sum > state.player2_sum:
        print("Player 1 wins!")
    elif state.player1_sum < state.player2_sum:
        print("Player 2 wins!")
    else:
        print("It's a tie!")


if __name__ == "__main__":
    n = int(input("Enter the value of n (the highest natural number): "))
    # human_players = input(
    #     "Enter 'both' if both players are human, 'one' if one player is human, 'none' if both players are AI: ")
    human_players = None
    if human_players == 'both':
        play_catch_up(n, True)
    elif human_players == 'one':
        human_player = int(
            input("Enter 1 if you want to be Player 1, 2 if you want to be Player 2: ")) - 1
        if human_player == 0:
            print("You are Player 1.")
        else:
            print("You are Player 2.")
        play_catch_up(n, True)
    else:
        play_catch_up(n, False)
