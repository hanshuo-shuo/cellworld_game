import typing

import pygame
from .agent import AgentState
from .navigation import Navigation
from .navigation_agent import NavigationAgent
from .resources import Resources
import shapely as sp
from .util import distance


class Mouse(NavigationAgent):
    def __init__(self,
                 start_state: AgentState,
                 actions: typing.List[typing.Tuple[float, float]],
                 goal_location: typing.Tuple[float, float],
                 goal_threshold: float,
                 puff_threshold: float,
                 puff_cool_down_time: float,
                 navigation: Navigation):
        NavigationAgent.__init__(self,
                                 navigation=navigation,
                                 max_forward_speed=0.05,
                                 max_turning_speed=2.0)
        self.start_state = start_state
        self.actions = actions
        self.goal_location = goal_location
        self.goal_threshold = goal_threshold
        self.puff_threshold = puff_threshold
        self.puff_cool_down = 0
        self.puff_cool_down_time = puff_cool_down_time
        self.observation = None
        self.finished = False

    def get_observation(self):
        return self.observation

    def parse_observation(self, observation: dict):
        goal_distance = distance(self.goal_location, observation["agent_states"]["prey"][0])
        self.finished = goal_distance <= self.goal_threshold
        if observation["agent_states"]["predator"][0]:
            predator_distance = distance(observation["agent_states"]["prey"][0],
                                         observation["agent_states"]["predator"][0])
            if self.puff_threshold <= 0:
                puff = predator_distance <= self.puff_threshold
                self.puff_cool_down = self.puff_cool_down_time
            else:
                puff = False
            parsed_observation = (observation["agent_states"]["prey"][0][0],
                                  observation["agent_states"]["prey"][0][1],
                                  observation["agent_states"]["prey"][1],
                                  observation["agent_states"]["predator"][0][0],
                                  observation["agent_states"]["predator"][0][1],
                                  observation["agent_states"]["predator"][1],
                                  goal_distance,
                                  self.finished,
                                  predator_distance,
                                  puff,
                                  observation["walls"][:3]
                                  )
        else:
            parsed_observation = (observation["agent_states"]["prey"][0][0],
                                  observation["agent_states"]["prey"][0][1],
                                  observation["agent_states"]["prey"][1],
                                  None,
                                  None,
                                  None,
                                  goal_distance,
                                  self.finished,
                                  None,
                                  None,
                                  observation["walls"][:3]
                                  )
        return parsed_observation

    def reset(self):
        self.finished = False
        self.puff_cool_down = 0
        self.observation = None
        self.state.location = self.start_state.location
        self.state.direction = self.start_state.direction
        NavigationAgent.reset(self)

    def start(self, observation: dict):
        self.observation = self.parse_observation(observation=observation)
        NavigationAgent.start(self,
                              observation=observation)

    def step(self, delta_t: float, observation: dict):
        self.observation = self.parse_observation(observation=observation)
        self.puff_cool_down -= delta_t
        self.navigate(delta_t=delta_t)

    @staticmethod
    def create_sprite() -> pygame.Surface:
        sprite = pygame.image.load(Resources.file("prey.png"))
        rotated_sprite = pygame.transform.rotate(sprite, 270)
        return rotated_sprite

    @staticmethod
    def create_polygon() -> sp.Polygon:
        return sp.Polygon([(.015, 0), (0, 0.005), (-.015, 0), (0, -0.005)])

    def set_action(self, action_number: int):
        self.set_destination(self.actions[action_number])

