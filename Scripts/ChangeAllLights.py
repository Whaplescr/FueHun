from HueElements.Light import Light
from Helpers.Colors import ColorHelper
from time import sleep

lights = [Light(2),Light(4),Light(5)]

color_help = ColorHelper()
color_dict = color_help.get_color_dict()

for color in color_dict.values():
    lights[0].change_light_color_xy(color)
    lights[1].change_light_color_xy(color)
    lights[2].change_light_color_xy(color)
    sleep(2)
