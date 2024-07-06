from time import time
import numpy as np
from loguru import logger

# discount factor
GAMMA = 1.0
GOAL = 100
THETA = 0.01

class DiceGame:
    def __init__(self, goal=100):
        self.goal = goal
        self.states = list(range(self.goal + 1))
        self.actions = ['roll', 'stop']
        self.gamma = GAMMA  # Discount factor (1.0 for undiscounted rewards)

    def transition_probability(self, state, action, next_state):
        if action == 'stop':
            return 1.0 if next_state == state else 0.0
        else:
            return 1 / 6
        if action == 'stop':
            # logger.info(f'{next_state}, {state}, {next_state == state}')
            return 1.0 if next_state == state else 0.0
        elif action == 'roll':
            if next_state == 0:
                return 1/6  # Probability of rolling a 1
            elif (next_state - state) > 6:
                # logger.info(f'{state}, {action}, {next_state}, 0.0')
                return 0.0 # next state can never be more than what's possible on a single dice roll
            elif state < next_state <= min(state + 6, self.goal):
                return 1/6  # Probability of rolling 2-6
            else:
                return 0.0

    def reward(self, state, action, next_state):
        random_roll = np.random.randint(1, 7)
        if action == 'roll':
            if random_roll == 1:
                return (-1 * state)
            else:
                return random_roll
        if action == 'stop':
            return 0

        '''
        if (next_state - state) > 6:
            return -1.0 # no reward for impossible states
        if (next_state == self.goal) and (state == (self.goal - 1)) and action == 'roll':
            # logger.debug(f'{next_state}, {self.goal}, {state}, {action}')
            return -1.0
        if (next_state == self.goal) and (state == (self.goal - 1)) and action == 'stop':
            return 1.0
        if next_state == self.goal:
            logger.info(f'{state}, {next_state}, {self.goal}')
            return 1.0
        else:
            return 0.0
        '''
            
        
    def _reward(self, state, action, next_state):
        if next_state == self.goal:
            return 1
        elif next_state == 0 or next_state == state:
            return -1
        else:
            return 0

    def value_iteration(self, theta=1e-6):
        V = np.zeros(self.goal + 1)
        _ctr = 0
        while True:
            _ctr += 1
            # import pdb;pdb.set_trace()
            delta = theta
            for s in self.states[:-6]:
                # if _ctr < 100:
                #     logger.info(V)
                v = V[s]
                V[s] = max(self.calculate_action_value(s, a, V)
                           for a in self.actions)
                delta = max(delta, abs(v - V[s]))
            logger.debug(delta)
            if delta < theta:
                break
        return V

    def calculate_action_value(self, state, action, V):
        # possible_states_from_current_state = [0]
        # for idx in range(self.goal - 6):
        #     possible_states_from_current_state
        action_value = sum(
            self.transition_probability(state, action, next_state) *
            (self.reward(state, action, next_state) +
             self.gamma * V[next_state])
            for next_state in [
                0,
                (state+1),
                (state+2),
                (state+3),
                (state+4),
                (state+5),
                (state+6),
            ] 
        )
        logger.info(f'{action_value}, {state}, {action}, ')
        return action_value

    def policy_improvement(self, V):
        # import pdb;pdb.set_trace()
        policy = {}
        for s in self.states:
            policy[s] = max(
                self.actions, key=lambda a: self.calculate_action_value(s, a, V))
        return policy

    def policy_evaluation(self, policy, theta=1e-6):
        V = np.zeros(self.goal + 1)
        while True:
            delta = 0
            for s in self.states:
                v = V[s]
                V[s] = self.calculate_action_value(s, policy[s], V)
                delta = max(delta, abs(v - V[s]))
            if delta < theta:
                break
        return V

    def find_optimal_policy(self):
        V = self.value_iteration(theta=THETA)
        policy = self.policy_improvement(V)
        return policy, V

    def evaluate_performance(self, policy, num_episodes=10000):
        wins = 0
        for _ in range(num_episodes):
            state = 0
            while state < self.goal:
                action = policy[state]
                if action == 'stop':
                    break
                roll = np.random.randint(1, 7)
                if roll == 1:
                    state = 0
                else:
                    state = min(state + roll, self.goal)
            if state == self.goal:
                wins += 1
        return wins / num_episodes

if __name__ == '__main__':
    start_ts = time()
    # Create the game and find the optimal policy
    game = DiceGame(goal=GOAL)
    optimal_policy, optimal_value = game.find_optimal_policy()
    import pdb;pdb.set_trace()
    # Evaluate the performance
    win_probability = game.evaluate_performance(optimal_policy)
    print(f"Probability of winning with optimal policy: {win_probability:.4f}")

    # Print the optimal policy
    print("\nOptimal Policy:")
    for state, action in optimal_policy.items():
        print(f"State {state}: {action}")

    # Betting scenarios


    def optimal_bet(current_score, goal):
        return 'roll' if optimal_policy[current_score] == 'roll' else 'stop'


    print("\nBetting Scenarios:")
    scenarios = [(0, 100), (50, 100), (90, 100), (95, 100), (99, 100)]
    for current_score, goal in scenarios:
        decision = optimal_bet(current_score, goal)
        print(f"Current score: {current_score}, Goal: {
            goal}, Optimal decision: {decision}")

    print(f'Time taken: {int(time() - start_ts)} second(s).')