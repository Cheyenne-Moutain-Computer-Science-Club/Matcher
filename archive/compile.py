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

class Compile(Main):
    def __init__(self):
        super().__init__()
        self.generate_output()

    def generate_output(self):
        Main.output = pd.DataFrame({"Name": [], "Email Address": [], "Matches": []})
        for key, prof in Main.profiles.items():
            build_list = [Main.inputs.iloc[key]['Name'], Main.inputs.iloc[key]['Email Address'], [Main.inputs.iloc[x]['Name'] for x in prof['matches']]]
        Main.output.loc[len(Main.inputs.index)] = build_list
        Main.finshed = True
    
        print('Compiled')