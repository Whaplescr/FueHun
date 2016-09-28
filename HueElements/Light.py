import requests
from Helpers.HueElement import HueElement
from json import loads

class Light(HueElement):

    def __init__(self,light_number):
        self.light_number = light_number
        light_info = self.populate_initial_values()
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
        self.colormode = state["colormode"]
        self.reachable = state["reachable"]

        # Light details
        self.type = light_info["type"]
        self.name = light_info["name"]
        self.modelid = light_info["modelid"]
        self.manufacturername = light_info["manufacturername"]
        self.uniqueid = light_info["uniqueid"]
        self.swversion = light_info["swversion"]


    def populate_initial_values(self):
        info_load = loads(self.get_light().text)

    def get_light(self):
        url = self.api_url + "/lights/%d" %self.light_number
        return requests.get(url)