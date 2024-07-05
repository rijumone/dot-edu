import random


class DiceGame:
  def __init__(self):
    self.states = list(range(101))  # All possible scores (0-100)
    self.actions = ["roll", "stop"]
    self.goal_score = 100
    self.discount_factor = 0.9  # Adjust as needed

  def get_reward(self, state, action):
    if state == self.goal_score:
      return 100
    elif state == 0:
      return -1
    else:
      return 0

  def get_next_state(self, state, action):
    if action == "roll":
      roll = random.randint(2, 6)
      next_state = min(state + roll, self.goal_score)  # Limit to goal score
    else:
      next_state = state
    return next_state

  def get_transition_probability(self, state, action, next_state):
    if action == "roll":
      if next_state == state:
        return 0  # Can't roll and stay in the same state (stop action)
      elif next_state == 0:
        return 1/6  # Probability of rolling a 1
      else:
        # Probability of rolling a specific value (2-6) leading to next_state
        return 1/6
    else:
      return 1.0  # Deterministic transition for "stop" action

  def value_iteration(self, epsilon=0.1):
    V = {s: 0 for s in self.states}  # Initialize value function
    for _ in range(100):  # Adjust iterations for better convergence
      V_temp = V.copy()
      for state in self.states:
        if state == self.goal_score or state == 0:
          continue  # Fixed rewards for terminal states
        Q = [0 for _ in self.actions]
        for i, action in enumerate(self.actions):
          for next_state in self.states:
            prob = self.get_transition_probability(state, action, next_state)
            reward = self.get_reward(state, action)
            Q[i] += prob * (reward + self.discount_factor * V_temp[next_state])
        if random.random() < epsilon:
          best_action = random.choice(self.actions)  # Explore
        else:
          best_action = self.actions[Q.index(max(Q))]  # Exploit
        V[state] = max(Q)
      V = V_temp  # Update value function

    policy = {s: self.actions[Q.index(max(Q))] for s, Q in V.items()}
    return V, policy

  def play_game(self, policy, start_state=0):
    state = start_state
    while state != self.goal_score and state != 0:
      action = policy[state]
      if action == "roll":
        roll = random.randint(2, 6)
        state = min(state + roll, self.goal_score)
      else:
        break
    return state == self.goal_score

  def evaluate_policy(self, policy, num_games=1000):
    wins = 0
    for _ in range(num_games):
      wins += self.play_game(policy)
    return wins / num_games


if __name__ == "__main__":
  game = DiceGame()
  V, policy = game.value_iteration()
  win_rate = game.evaluate_policy(policy)
  print(f"Optimal Policy: {policy}")
  print(f"Win Rate: {win_rate:.2f}")

  # Use the learned policy for different scenarios (modify win condition)
  game.goal_score = 95  # Change goal score
  win_rate = game.evaluate_policy(policy)
  print(f"Win Rate (Goal 95): {win_rate:.2f}")
