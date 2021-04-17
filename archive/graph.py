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

class Graph(Main):
    def __init__(self):
        super().__init__()
        self.create_coordinates()

    def create_coordinates(self):
        for index in list(Main.inputs.index.values):
            heads = list(Main.inputs.columns)
            total_x = 0
            total_y = 0
            for col in heads:
                if col in Main.convertions:
                    if Main.convertions[col]['axis'] == 'x':
                        total_x += Main.inputs.iloc[index][col]
                    elif Main.convertions[col]['axis'] == 'y':
                        total_y += Main.inputs.iloc[index][col]
                    else:
                        raise ValueError('Incorrect Axis Definition')
            Main.profiles[index]['coords'] = [total_x, total_y]
        
        print('Graphed')