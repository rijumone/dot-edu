from loguru import logger
import numpy as np

GOAL = 20
DISCOUNT_FACTOR = 0.7
THETA = 0.35

# Step 1: Define the environment
class DiceGame:
    def __init__(self):
        self.goal = GOAL
        self.actions = ["roll", "stop"]

    def step(self, state, action):
        if action == "stop":
            return state, 0
        else:
            roll = np.random.randint(1, 7)
            # logger.warning(roll)
            if roll == 1:
                return 0, -1
            else:
                new_state = state + roll
                if new_state > self.goal:
                    return state, -1
                elif new_state == self.goal:
                    return self.goal, 1
                else:
                    return new_state, 0

    def is_terminal(self, state):
        return state == self.goal or state == 0


# Step 2: Policy Evaluation
def policy_evaluation(policy, env, discount_factor=1.0, theta=0.0001):
    """Evaluates a given policy for an environment, estimating the state-value function V(s) for each state s under that policy. This process involves iteratively updating the value estimates until they converge to within a specified threshold.

    Args:
        policy: A policy to be evaluated, represented as a 2D list or array where
            policy[state] gives the probabilities of taking each action in that state.
        env: Instance of class DiceGame(); the environment being evaluated
        discount_factor (optional): A factor used to discount future rewards.
            It defaults to 1.0, meaning no discounting.
        theta (optional): A small threshold value for determining when the value
            function has converged. The iteration stops when the change in the
            value function is less than theta. Defaults to 0.0001.

    Returns:
        Value function V
    """
    V = np.zeros(env.goal + 1)
    # Initializes the value function V(s) to zero for all states. Assuming env.goal is the highest possible state index, this creates an array of zeros with a length of env.goal + 1.
    while True:
        # import pdb;pdb.set_trace()
        delta = 0
        for state in range(env.goal + 1):
            if env.is_terminal(state):
                continue
            v = 0
            for action, action_prob in enumerate(policy[state]):
                # action_prob = Probability of taking the current action under the given policy.
                new_state, reward = env.step(state, env.actions[action])
                v += action_prob * (reward + discount_factor * V[new_state])
                # Update the temporary value v with the expected return of taking the current action, which includes the immediate reward and the discounted value of the new state.
                # logger.debug(v)
            delta = max(delta, np.abs(v - V[state]))
            V[state] = v
        logger.info(f'{delta}, {theta}')
        if delta < theta:
            break
    return V


# Step 3: Policy Improvement
def policy_improvement(V, env, discount_factor=1.0):
    policy = np.ones((env.goal + 1, len(env.actions))) / len(env.actions)
    for state in range(env.goal + 1):
        if env.is_terminal(state):
            continue
        q = np.zeros(len(env.actions))
        for action in range(len(env.actions)):
            new_state, reward = env.step(state, env.actions[action])
            q[action] = reward + discount_factor * V[new_state]
        best_action = np.argmax(q)
        policy[state] = np.eye(len(env.actions))[best_action]
    return policy


# Step 4: Policy Iteration
def policy_iteration(env, discount_factor=1.0):
    policy = np.ones((env.goal + 1, len(env.actions))) / len(env.actions)
    
    while True:
        # import pdb;pdb.set_trace()
        V = policy_evaluation(policy, env, discount_factor, theta=THETA)
        new_policy = policy_improvement(V, env, discount_factor)
        if (new_policy == policy).all():
            break
        policy = new_policy
    return policy, V


# Step 5: Epsilon-Greedy Policy
def epsilon_greedy_policy(policy, epsilon, nA):
    def policy_fn(state):
        A = np.ones(nA, dtype=float) * epsilon / nA
        best_action = np.argmax(policy[state])
        A[best_action] += (1.0 - epsilon)
        return A
    return policy_fn


# Step 6: Training and Evaluation
def main():
    env = DiceGame()
    discount_factor = DISCOUNT_FACTOR
    optimal_policy, V = policy_iteration(env, discount_factor)
    import pdb;pdb.set_trace()
    epsilon = 0.1
    nA = len(env.actions)
    policy = epsilon_greedy_policy(optimal_policy, epsilon, nA)
    
    success_count = 0
    episodes = 10000
    for _ in range(episodes):
        state = 0
        while not env.is_terminal(state):
            action_probs = policy(state)
            action = np.random.choice(np.arange(len(action_probs)), p=action_probs)
            state, reward = env.step(state, env.actions[action])
        if state == env.goal:
            success_count += 1
    
    print(f"Probability of reaching exactly {GOAL} points: {success_count / episodes}")

if __name__ == "__main__":
    main()
