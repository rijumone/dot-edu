import numpy as np
import random


class SimpleGridEnv:
    def __init__(self):
        self.states = [0, 1, 2, 3, 4]
        self.terminal_states = [0, 4]
        self.current_state = 2
        self.rewards = {0: -1, 4: 1} # only extremes are rewarded or penalised
        self.actions = ["left", "right"]

    def step(self, action):
        if self.current_state in self.terminal_states:
            return self.current_state, 0

        if action == "left":
            # either the agent has reached the max left of the board
            next_state = max(0, self.current_state - 1)
        else:  # action == "right"
            # or the agent has reached the max right of the board
            next_state = min(4, self.current_state + 1)

        reward = self.rewards.get(next_state, 0)
        self.current_state = next_state
        return next_state, reward

    def reset(self):
        self.current_state = 2
        return self.current_state


def td_zero(env, num_episodes, alpha, gamma):
    V = np.zeros(len(env.states))
    # V is an array representing the value function for the states in the environment
    # The value function V(s) gives an estimate of the expected return (cumulative
    # future rewards) starting from state s and following a specific policy.
    

    for _ in range(num_episodes):
        print(V)
        state = env.reset()

        while state not in env.terminal_states:
            action = random.choice(env.actions)
            next_state, reward = env.step(action)
            V[state] = V[state] + alpha * \
                (reward + gamma * V[next_state] - V[state])
            state = next_state

    return V


# Parameters
num_episodes = 10
alpha = 0.1
gamma = 0.9

# Environment
env = SimpleGridEnv()

# Run TD(0)
value_function = td_zero(env, num_episodes, alpha, gamma)

print("Estimated Value Function:")
for state, value in enumerate(value_function):
    print(f"State {state}: {value:.2f}")
