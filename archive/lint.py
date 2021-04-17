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
    def __init__(self):
        super().__init__()
        self.convert()
        self.create_profiles()

    def convert(self):
        heads = list(Main.inputs.columns)
        for col in heads:
            if col in Main.convertions:
                convert = []
                for index, row in Main.inputs.iterrows():
                    convert.append(Main.convertions[col][row[col]])
                Main.inputs[col] = convert
        print('Convert from Lint')
    

    def create_profiles(self):
        for index, row in Main.inputs.iterrows():
            Main.profiles[index] = {
                'id': index,
                'coords': [],
                'matches': []
            }
        print('Profiles Created')