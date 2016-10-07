from HueElements.Light import Light
from time import sleep

lights = [2,4,5]
sleep(10)
for light in lights:
    new_light = Light(light)
    new_light.turn_off()