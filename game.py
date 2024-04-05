from cellworld_game import *
from cellworld_loader import CellWorldLoader
import math

loader = CellWorldLoader(world_name="05_02")

model = Model(arena=loader.arena,
              occlusions=loader.occlusions,
              time_step=.5,
              real_time=True)

navigation = Navigation(locations=loader.locations,
                        paths=loader.paths)

print(navigation.get_path((.2, .8), (.6, .3)))

predator = Robot(start_locations=loader.open_locations,
                 navigation=navigation)

model.add_agent("predator", predator)


prey = Mouse(start_state=AgentState(location=(.05, .5),
                                    direction=0),
             goal_location=(1, .5),
             goal_threshold=.1,
             puff_threshold=.05,
             puff_cool_down_time=.5,
             navigation=navigation)
model.add_agent("prey", prey)


view = View(model=model)
model.reset()
post_observation = prey.get_observation()
while not prey.finished:
    pre_observation = post_observation
    view.draw()
    model.step()
    post_observation = prey.get_observation()
