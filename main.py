# from final import *
# from graph import *
# from lint import *
# from compile import *
# from GUI import *
# =====================
import pandas as pd
# import random


def Main():
    profile = {}
    output_csv = None

    def __init__(self, input_csv, pay_csv):
        self.inputs = pd.DataFrame(pd.read_csv(input_csv))


class Lint(Main):
    def __init__(self, convertions):
        Main.super()
        self.convertions = convertions

    def convert(self, key):
        convert = []

        for index, row in Main.inputs.iterrows():
            if convertions.key[0] == row[key]:
                convert.append(0)
            elif convertions.key[1] == row[key]:
                convert.append(1)
            elif convertions.key[2] == row[key]:
                convert.append(2)
            elif convertions.key[3] == row[key]:
                convert.append(3)
            else:
                raise TypeError

        inputs[key] = convert

    def create_profiles(self):
        pass


class Graph(Main):
    def __init__(self):
        Main.super()

    def create_coordinates(self, id):
        pass


class Distance(Main):
    def __init__(self):
        Main.super()
        self.in_range = []
        self.range = [0,0]
        self.apothem = 0

    def calc_distance(self, id):
        pass

    def get_people(self, id):
        # Get coords from id
        # Go through dict and if in range, add to self.in_range
        # If self.in_range.length() < 5, do over again with larger apothem
        # Else, grab five random people from that range and order by distance
        # Append this array to profile from id
        pass

class Compile(Main):
    def __init__(self):
        pass


class MailMerge(Main):
    def __init__(self):
        pass


class GUI():
    def __init__():
        pass
