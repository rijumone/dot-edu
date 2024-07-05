import numpy as np
import matplotlib.pyplot as plt

class DiceGame:
    def __init__(self):
        self.goal = 100
        self.num_states = self.goal + 1
        self.actions = ['roll', 'stop']
        self.dice_outcomes = [1, 2, 3, 4, 5, 6]

    def roll_dice(self):
        return np.random.choice(self.dice_outcomes)

    def step(self, state, action):
        if action == 'stop':
            return state, 0, True
        
        roll = self.roll_dice()
        if roll == 1:
            return 0, 0, True
        
        new_state = min(state + roll, self.goal)
        reward = 1 if new_state == self.goal else 0
        done = new_state == self.goal
        
        return new_state, reward, done

class DiceAgent:
    def __init__(self, env, gamma=1.0, epsilon=0.1):
        self.env = env
        self.gamma = gamma
        self.epsilon = epsilon
        self.values = np.zeros(env.num_states)
        self.policy = np.full(env.num_states, 'roll')
        self.policy[env.goal] = 'stop'

    def value_iteration(self, theta=1e-6):
        while True:
            delta = 0
            for s in range(self.env.num_states):
                if s == self.env.goal:
                    continue
                v = self.values[s]
                self.values[s] = max(self._value_of_action(s, 'roll'), self._value_of_action(s, 'stop'))
                delta = max(delta, abs(v - self.values[s]))
            if delta < theta:
                break

    def _value_of_action(self, state, action):
        if action == 'stop':
            return state
        
        value = 0
        for roll in self.env.dice_outcomes:
            if roll == 1:
                value += 1/6 * self.gamma * self.values[0]
            else:
                next_state = min(state + roll, self.env.goal)
                value += 1/6 * (self.gamma * self.values[next_state] + (1 if next_state == self.env.goal else 0))
        return value

    def policy_improvement(self):
        policy_stable = True
        for s in range(self.env.num_states):
            if s == self.env.goal:
                continue
            old_action = self.policy[s]
            roll_value = self._value_of_action(s, 'roll')
            stop_value = self._value_of_action(s, 'stop')
            self.policy[s] = 'roll' if roll_value > stop_value else 'stop'
            if old_action != self.policy[s]:
                policy_stable = False
        return policy_stable

    def policy_iteration(self):
        while True:
            self.value_iteration()
            if self.policy_improvement():
                break

    def epsilon_greedy_action(self, state):
        if np.random.random() < self.epsilon:
            return np.random.choice(self.env.actions)
        return self.policy[state]

    def train(self, num_episodes=10000):
        for _ in range(num_episodes):
            state = 0
            done = False
            while not done:
                action = self.epsilon_greedy_action(state)
                next_state, reward, done = self.env.step(state, action)
                state = next_state

    def evaluate(self, num_episodes=10000):
        wins = 0
        for _ in range(num_episodes):
            state = 0
            done = False
            while not done:
                action = self.policy[state]
                next_state, reward, done = self.env.step(state, action)
                state = next_state
            if state == self.env.goal:
                wins += 1
        return wins / num_episodes

def plot_policy(agent):
    plt.figure(figsize=(12, 4))
    plt.plot(range(agent.env.num_states), [1 if p == 'roll' else 0 for p in agent.policy])
    plt.xlabel('Score')
    plt.ylabel('Action (1: Roll, 0: Stop)')
    plt.title('Optimal Policy')
    plt.grid(True)
    plt.show()

# Main execution
env = DiceGame()
agent = DiceAgent(env)

print("Running policy iteration...")
agent.policy_iteration()

print("Training agent with epsilon-greedy policy...")
agent.train()

win_probability = agent.evaluate()
print(f"Probability of winning: {win_probability:.4f}")

plot_policy(agent)

# Print the optimal policy
print("\nOptimal Policy:")
for state, action in enumerate(agent.policy):
    print(f"State {state}: {action}")