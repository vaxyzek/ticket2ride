import random
from model import *

"""state is a dictionary that contains the followig items
state["roads"] - list of roads (67), where each road is a dictionart --6-tuple--
  <start, end, length, road_color, built, builder_color>
    start - start city name
    end   - end city name, you could assume that start < end alphabetically
    length - road length
    color - road color
    built - True/False
    builder_color - color of a builder (probably useless information)
state["hand"] - list of numbers of train cards for each color, for example
                [0, 3, 2, 0, 1, 0, 2] - means that there are 3 green, 2 red,
                1 white and 2 rainbow cards
state["tickets"] - list of two tickets, where ticket is a 2-tuple <start, end>
state["num_trains"] - number of trains left to build for the current agent

Returns tuple <action, road> where
  action - one of the action numbers
  road - 3-tuple <start, end, color> with cities names and road color in case of BUILD action
"""

def stupid_fifty(state):
  # 50% chance to DRAW card
  if random.random() < 0.5:
    return (DRAW, None)
  else:
    # 50% chance to build a random road
    road = random.sample(state["roads"], 1)[0]
    return (BUILD, (road["start"], road["finish"], road["color"],),)
