from cellworld_game import Environment


def reward(observation):
    return 1-observation[6] - 100 * observation[7]


env = Environment("21_05", use_lppos=False, use_predator=True, max_step=200, reward_function=reward)

env.reset()

while not env.prey.finished:
    env.step(env.action_space.sample())
    env.render()
