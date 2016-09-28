import csv
import random

class ColorHelper:

    def get_color_dict(self):
        reader = csv.reader('HueColors.csv','r')
        color_dict = dict(reader)
        return color_dict

    def get_random_color(self):
        colors = self.get_color_dict()
        return random.choice(list(colors.items()))

