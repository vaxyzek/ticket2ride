import copy
from operator import length_hint
from random import shuffle
from model import *
from agents import *

def init_deck():
  deck = []

  for color in range(NUM_COLORS - 1):
    deck += [color] * 10
  deck += [RAINBOW] * 12
  shuffle(deck)
  return deck

def init_hand(deck):
  hand = [0] * NUM_COLORS
  draw_n_cards(hand, deck, 4)
  return hand

def draw_card(hand, deck):
  if deck:
    hand[deck.pop()] += 1

def draw_n_cards(hand, deck, n):
  for i in range(n):
    draw_card(hand, deck)

def find_road(roads, start, finish, color):
  for road in roads:
    if road["start"] == start and road["finish"] == finish and road["color"] == color:
      return road
  return None

# Update player hand to build a road with given length and color
# Return list of played train cards (colors)
def play_hand(hand, length, color):
  exact_color = min(length, hand[color])
  rainbow = length - exact_color
  hand[color] -= exact_color
  hand[RAINBOW] -= rainbow
  return [color] * exact_color + [RAINBOW] * rainbow

# Check if hand has enough colored cards (exact + rainbow) to build the road
def can_build(road, hand):
  color = road["color"]
  length = road["length"]
  return hand[color] + hand[RAINBOW] >= length

# Draw ticket from the deck. Reshuffle discard pile if necessary
def draw_ticket(tickets, discard_tickets):
  if not tickets:
    tickets += discard_tickets
    shuffle(tickets)
    discard_tickets.clear()

    if not tickets:
      print("Impossible. Tickets deck is empty")

  return tickets.pop()

def ticket_completed(roads, ticket, player_color):
  # TODO
  # TODO
  # TODO
  return False

def play(agents):
  """Plays a game with agents and returns a list of number of "developed" cards
  at the end of the game. E.g. [3, 2, 5, 6]
  """
  #################
  # Setup up board
  ################

  #Initialize roads
  roads = copy.deepcopy(ROADS)
  for road in roads:
    road["built"] = False

  #Initialize tickets
  tickets = copy.copy(TICKETS)
  shuffle(tickets)
  discard_tickets = []

  #Initialize train cards deck
  deck = init_deck()
  discard_deck = []

  #Initialize agent states
  states = []
  for a in agents:
    states.append({
      "hand" : init_hand(deck),
      "tickets" : [tickets.pop(), tickets.pop()],
      "num_trains" : 20,
      "completed_tickets" : 0
    })
  print("Initial states : ", states)

  ########
  # Play
  ########
  stopgame = False
  turn = 0
  while not stopgame:
    turn += 1
    built_roads = [road["length"] for road in roads if road["built"]]
    print("---")
    print("Turn#", turn, "# of built roads", len(built_roads), "of total length", sum(built_roads))

    for ix, agent in enumerate(agents):
      # Trick
      agent_color = ix
      agent_state = states[ix]
      #Call agent to receive next action
      game_state = {
        "roads" : roads,
        "hand" : states[ix]["hand"],
        "tickets" : states[ix]["tickets"],
        "num_trains" : states[ix]["num_trains"]
      }
      action = agent(game_state)
      print("Agent #", ix, "action", action, "Hand:", states[ix]["hand"], "Trains:", states[ix]["num_trains"])

      #Modify state according to agents action
      if action[0] == DRAW:
        draw_n_cards(states[ix]["hand"], deck, 2)

        if len(deck) == 0:
          if len(discard_deck) == 0:
            print("No more cards in the deck. Something wrong. Stop game.")
            stopgame = True
            break
          else:
            deck = discard_deck
            shuffle(deck)
            discard_deck = []
      elif action[0] == BUILD:
        # Check if road can be build and build it. Move train cards to discard pile
        start, finish, color = action[1]
        road = find_road(roads, start, finish, color)
        if road and not road["built"] and road["length"] <= states[ix]["num_trains"]:
          # Check if agent has enough cards to built the road
          if can_build(road, agent_state["hand"]):
            road["built"] = True
            road["builder_color"] = agent_color
            discard_deck += play_hand(agent_state["hand"], road["length"], road["color"])
            agent_state["num_trains"] -= road["length"]
            print("Build road. Hand:", agent_state["hand"])
          else:
            print("Requested road cannot be built, not enough train cards")

          if agent_state["num_trains"] == 0:
            print("Last train played. Stop game.")
            stopgame = True
        else:
          print("Agent requested to build a road that doesn't exist or already have been built")

        # Check if any tickets was completed
        # TODO: Handle east-west tickets
        updated_tickets = []
        for ticket in agent_state["tickets"]:
          if ticket_completed(roads, ticket, agent_color):
            agent_state["completed_tickets"] += 1
            discard_tickets.append(ticket)
          else:
            updated_tickets.append(ticket)

        #Draw new tickets
        for i in range(2 - len(updated_tickets)):
          updated_tickets.append(draw_ticket(tickets, discard_tickets))
        agent_state["tickets"] = updated_tickets

        pass
      elif action[0] == DISCARD:
        #Discard tickets and take 2 new
        discard_tickets += states[ix]["tickets"]
        agent_state["tickets"] = [draw_ticket(tickets, discard_tickets), draw_ticket(tickets, discard_tickets)]

      if stopgame:
        break

  #Return list of completed tickets for each agent
  return [agent_state["completed_tickets"] for agent_state in states]


if __name__ == '__main__':
  print("Loaded", len(CITIES), "cities")
  print("Loaded", len(ROADS), "roads")

  print("Playing game between 2 '50% agents'")
  result = play([stupid_fifty, stupid_fifty])
  print("Result", result)
