import random
import ast

class ColorHelper:

    def get_color_dict(self):
        color_dictionary  = {}
        import os
        dir_path = os.path.dirname(os.path.realpath(__file__))
        f = open(dir_path+'\HueColors.csv')
        for line in f:
            tmp_line = line.replace('\n','').replace('"','').replace('[','').replace(']','').split(',')

            color_dictionary[tmp_line[0]] = [float(tmp_line[1]),float(tmp_line[2])]

        return color_dictionary

    def get_random_color(self):
        colors = self.get_color_dict()
        return random.choice(list(colors.items()))
