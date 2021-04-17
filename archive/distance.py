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

class Distance(Main):
    def __init__(self):
        super().__init__()
        self.get_people()

    def get_people(self):
        for key, prof1 in Main.profiles.items():
            self.apothem = 15
            people = self.in_range(key)
            while len(people) < 13:
                self.apothem += 3
                people = self.in_range(key)
            Main.profiles[key]['matchs'] = rd.sample(people, 10)
        print('Matches Made')

    def in_range(self, di):
        people = []
        dist = []
        for key, prof in Main.profiles.items():
            if ((Main.profiles[di]['coords'][0] - self.apothem) < prof['coords'][0] < (Main.profiles[di]['coords'][0] + self.apothem)) and ((Main.profiles[di]['coords'][1] - self.apothem) < prof['coords'][1] < (Main.profiles[di]['coords'][1] + self.apothem)):
                if key == di:
                    pass
                else:
                    dist.append(((Main.profiles[di]['coords'][0] + Main.profiles[key]['coords'][0])**2 + (Main.profiles[di]['coords'][1] + Main.profiles[key]['coords'][1])**2) **(1/2))
                    people.append(key)
        dist, people = zip(*sorted(zip(dist, people)))
        return people