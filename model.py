import json

#Number of colors
NUM_COLORS = 7

#Colors
BLUE, GREEN, RED, YELLLOW, WHITE, BLACK, RAINBOW = range(NUM_COLORS)

COLORS_MAP = {
  "Bl" : BLUE,
  "Gr" : GREEN,
  "Rd" : RED,
  "Yl" : YELLLOW,
  "Wh" : WHITE,
  "Bk" : BLACK
}

#Actions
DRAW, BUILD, DISCARD = range(3)

MODEL = json.load(open("model.json"))

CITIES = MODEL["cities"]
ROADS = MODEL["roads"]
TICKETS = MODEL["tickets"]

#Map color names to color
for road in MODEL["roads"]:
  road["color"] = COLORS_MAP[road["colorName"]]

if __name__ == '__main__':
  print(MODEL)
