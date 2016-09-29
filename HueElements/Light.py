import requests
from Helpers.HueElement import HueElement
from json import loads,dumps

class Light(HueElement):

    _on_json = dumps({"on": True})
    _off_json = dumps({"on":False})

    # Initialize the Light object with all of it's info elements
    def __init__(self,light_number):
        self.light_number = light_number
        self.light_url = self.api_url + "/lights/%d" %(self.light_number)

        light_info = self.get_light_info()
        state = light_info["state"]

        # State of the light
        self.on = state["on"]
        self.bri = state['bri']
        self.hue = state["hue"]
        self.sat = state["sat"]
        self.effect = state["effect"]
        self.xy = state["xy"]
        self.ct = state["ct"]
        self.alert = state["alert"]
        self.color_mode = state["colormode"]
        self.reachable = state["reachable"]

        # Light details
        self.type = light_info["type"]
        self.name = light_info["name"]
        self.model_id = light_info["modelid"]
        self.manufacturer_name = light_info["manufacturername"]
        self.unique_id = light_info["uniqueid"]
        self.sw_version = light_info["swversion"]

    # Get all the info for a light
    def get_light_info(self):
        light_call = requests.get(self.light_url)
        info = loads(light_call.text)
        return info

    # Turns on the light
    def turn_on(self):
        on_call = requests.put(self.light_url +"/state",self._on_json)
        self.update_state()
        return on_call

    # Turns off the light
    def turn_off(self):
        off_call = requests.put(self.light_url + "/state",self._off_json)
        self.update_state()
        return off_call

    def update_state(self):
        state_info = self.get_light_info()["state"]

        # State of the light
        self.on = state_info["on"]
        self.bri = state_info['bri']
        self.hue = state_info["hue"]
        self.sat = state_info["sat"]
        self.effect = state_info["effect"]
        self.xy = state_info["xy"]
        self.ct = state_info["ct"]
        self.alert = state_info["alert"]
        self.color_mode = state_info["colormode"]
        self.reachable = state_info["reachable"]