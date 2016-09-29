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
        if on_call.status_code == 200:
            self.on = True
        return on_call

    # Turns off the light
    def turn_off(self):
        off_call = requests.put(self.light_url + "/state",self._off_json)
        if off_call.status_code == 200:
            self.on == False
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

    # TODO: Need to update the logic that confirms whether or not calls were made successfully
    # TODO: Status code of 200 isnt sufficient
    def change_brightness(self,brightness):
        bri = dumps({"bri":brightness})
        bri_request = requests.put(self.light_url + "/state",bri)
        if bri_request.status_code == 200:
            self.bri == brightness
            return True
        else:
            return False

    def change_light_hue(self,hue):
        new_hue = dumps({"hue": hue})
        hue_request = requests.put(self.light_url + "/state",  new_hue)

        if hue_request.status_code == 200:
            self.hue = hue
            return True
        else:
            return False

    def change_light_sat(self,sat):
        saturation = dumps({"sat": sat})
        saturation_request = requests.put(self.light_url + "/state", saturation)

        if saturation_request.status_code == 200:
            self.sat = sat
            return True
        else:
            return False

    def change_light_color_temperature(self,color_temp):
        ct = dumps({"ct": color_temp})
        ct_request = requests.put(self.light_url + "/state", ct)

        if ct_request.status_code == 200:
            self.ct == ct
            return True
        else:
            return False

    def change_light_color_xy(self,xy_list):
        xy = dumps({"xy":xy_list})
        xy_request = requests.put(self.light_url + "/state",xy)

        if xy_request.status_code == 200:
            self.xy = xy_list
            return True
        else:
            return False