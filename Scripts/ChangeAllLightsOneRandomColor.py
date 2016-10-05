from HueElements.Light import Light
from Helpers.Colors import ColorHelper
from time import sleep

lights = [Light(2),Light(4),Light(5)]

color_help = ColorHelper()
color = color_help.get_random_color()

lights[0].change_light_color_xy(color)
lights[1].change_light_color_xy(color)
lights[2].change_light_color_xy(color)

