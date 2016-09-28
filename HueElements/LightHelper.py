from json import dumps
import requests


class LightHelper:

    on_json = dumps({"on": True})
    off = dumps({"on":False})

    def turn_on(self,api_url,light):
        url = api_url+"/lights/%d/state"%(light)
        return requests.put(url,self.off)

    def turn_off(self,api_url,light):
        url = api_url + "/lights/%d/state" % (light)
        return requests.put(url, self.on)

    def change_brightness(self,api_url,light,brightness):
        url = api_url + "lights/%/state"%(light)
        bri = dumps({"bri":brightness})
        return requests.put(url,bri)

    def change_light_hue(self,api_url,light,hue):
        url = api_url + "lights/%/state" % (light)
        assert hue in range(0,65535),"Hue value not in range of 0-65535"
        abs_hue = dumps({"hue": hue})
        return requests.put(url,  abs_hue)

    def change_light_sat(self,api_url,light,sat):
        url = api_url + "lights/%/state" % (light)
        saturation = dumps({"sat": sat})
        return requests.put(url, saturation)

    def change_light_color_temperature(self,api_url,light,color_temp):
        url = api_url + "lights/%/state" % (light)
        ct = dumps({"ct": color_temp})
        return requests.put(url, ct)

    def change_light_color_xy(self,api_url,light,x_color=-1,y_color=-1,xy_list=[]):
        url = api_url + "lights/%/state" % (light)
        if x_color != -1 and y_color != -1:
            if x_color > 1 or y_color >1:
                raise("Color x and y values must be between 0 and 1 {ex. [0.41, 0.51721] }")
            else:
                xy_vals = [x_color,y_color]
                xy = dumps({"xy": xy_vals})
                return requests.put(url,xy)

        elif x_color == -1 or y_color == -1 or xy_list != None:
            xy = dumps({"xy":xy_list})
            return requests.put(url,xy)

    #TODO more methods later, just trying to hash out the basics
