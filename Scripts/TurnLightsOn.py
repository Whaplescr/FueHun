from HueElements.Light import Light

lights = [2,4,5]
for light in lights:
    new_light = Light(light)
    new_light.turn_on()