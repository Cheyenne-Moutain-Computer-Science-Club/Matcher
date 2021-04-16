# =====================
# Package imports
# =====================
import pandas as pd
import random as rd
# =====================
# Module imports
# =====================
from main import Main
# =====================
# Script
# =====================

class Lint(Main):
    def __init__(self, convertions):
        super().__init__()
        self.convertions = convertions

    def convert(self, key):
        convert = []

        for index, row in Main.inputs.iterrows():
            if self.convertions[key][0] == row[key]:
                convert.append(0)
            elif self.convertions[key][1] == row[key]:
                convert.append(1)
            elif self.convertions[key][2] == row[key]:
                convert.append(2)
            elif self.convertions[key][3] == row[key]:
                convert.append(3)
            else:
                raise TypeError

        Main.inputs[key] = convert

    def create_profiles(self):
        for index, row in Main.inputs.iterrows():
            Main.profiles[index] = {
                'id': index,
                'coords': [],
                'matches': []
            }