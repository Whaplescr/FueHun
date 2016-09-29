from collections import deque
from HueElements.Light import Light
from Helpers.Colors import ColorHelper

lights = deque([Light(2),Light(4),Light(5)])

color_help = ColorHelper()

for _ in range(0,100):
    light = lights.popleft()
    lights.append(light)

    random_color = color_help.get_random_color()
    light.change_light_color_xy(random_color[1])


