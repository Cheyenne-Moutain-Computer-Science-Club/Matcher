# =====================
# Package imports
# =====================
import pandas as pd
import random as rd
# =====================
# Module imports
# =====================
from matcher.data import Data
from visiulization.graph import Graph
# =====================
# Script
# =====================

class Core(Data):
    def __init__(self):
        super().__init__()
        self.apothem = 1
        self.outer_apothem = 200

    def run(self):
        self.convert()
        self.lint()
        self.create_profiles()
        self.create_coordinates()
        self.get_people()
        self.generate_output()
        if Data.use_filtered_list:
            self.filter_outputs()
        else:
            Data.status += 15

    @staticmethod
    def convert() -> None:
        # Determines if CSV of TSV file format is used and
        # creates the inputs dataframe
        if Data.use_tsv_inputs:
            Data.inputs = pd.DataFrame(pd.read_csv(Data.input_csv, sep='\t'))
        else:
            Data.inputs = pd.DataFrame(pd.read_csv(Data.input_csv))

        # Checks to see if a filtered list is used
        if Data.use_filtered_list:
            # Creates filtered dataframe based on either CSV or TSV file format
            if Data.use_tsv_inputs:
                Data.filtered = pd.DataFrame(pd.read_csv(Data.filter_csv, sep='\t'))
            else:
                Data.filtered = pd.DataFrame(pd.read_csv(Data.filter_csv))
            # If only include is selected, remove non-filtered inputs from
            # inputs dataframe
            if Data.only_include_filtered:
                drop_list = []
                for index, row in Data.inputs.iterrows():
                    if row['Email'] in pd.merge(Data.inputs, Data.filtered, indicator=True, how='outer').query(
                            '_merge=="left_only"').drop('_merge', axis=1).values:
                        drop_list.append(index)
                Data.inputs = Data.inputs.drop(drop_list)
        Data.status += 15

    @staticmethod
    def lint() -> None:
        # Converts string outputs from form into into numerical values based on convert.json
        heads = list(Data.inputs.columns)
        for col in heads:
            if col in Data.conversions:
                convert = []
                for index, row in Data.inputs.iterrows():
                    convert.append(Data.conversions[col][row[col]])
                Data.inputs[col] = convert
        # Print status for logging
        print('Convert from Lint')
        Data.status += 15

    @staticmethod
    def create_profiles():
        # Creates a basic profile for every row
        for index, row in Data.inputs.iterrows():
            Data.profiles[index] = {
                'id': index,
                'grade': Data.inputs.iloc[index]['What grade are you in?'],
                'coords': [],
                'matches': [],
                'antimatches': [],
                'gradematches' : [],
                'gradeantimatches': []
            }
            Data.grade_quantities[Data.inputs.iloc[index]['What grade are you in?']] += 1
        print('Profiles Created')
        print(Data.grade_quantities)
        Data.status += 15

    @staticmethod
    def create_coordinates():
        for index in list(Data.inputs.index.values):
            heads = list(Data.inputs.columns)
            total_x = 0
            total_y = 0
            for col in heads:
                if col in Data.conversions:
                    if Data.conversions[col]['axis'] == 'x':
                        total_x += Data.inputs.iloc[index][col]
                    elif Data.conversions[col]['axis'] == 'y':
                        total_y += Data.inputs.iloc[index][col]
                    else:
                        raise ValueError('Incorrect Axis Definition')
            Data.profiles[index]['coords'] = [total_x, total_y]

        print('Graphed')
        Data.status += 15

    def get_people(self) -> None:
        for key, prof in Data.profiles.items():
            # Gets inside matches
            self.apothem = 1
            people = self.inside_matches(key, False, 0)
            while len(people) < Data.config["outputs"]["matches"] + 3:
                self.apothem += 0.5
                people = self.inside_matches(key, False, 0)
            try: 
                Data.profiles[key]['matches'] = rd.sample(people, Data.config["outputs"]["matches"])
                print(f'{key} has {len(people)} for 1')
            except:
                Data.profiles[key]['matches'] = "Not enough data to sufficiently generate matches"

            # Gets outside matches
            self.outer_apothem = 200
            people = self.outside_matches(key, False, 0)
            while len(people) < Data.config["outputs"]["antimatches"] + 3:
                self.outer_apothem -= 0.5
                people = self.outside_matches(key, False, 0) 
            try: 
                Data.profiles[key]['antimatches'] = rd.sample(people, Data.config["outputs"]["antimatches"])
                print(f'{key} has {len(people)} for 2')
            except:
                Data.profiles[key]['antimatches'] = "Not enough data to sufficiently generate matches"

            # Gets grade level matches
            self.apothem = 1
            people = self.inside_matches(key, True, prof["grade"])
            while (len(people) < Data.config["outputs"]["gradematches"] + 3) and not (len(people) == (Data.grade_quantities[prof["grade"]] - 1)):
                self.apothem += 0.5
                people = self.inside_matches(key, True, prof["grade"])
            try: 
                Data.profiles[key]['gradematches'] = rd.sample(people, Data.config["outputs"]["gradematches"])
                print(f'{key} has {len(people)} for 3')
            except:
                Data.profiles[key]['gradematches'] = "Not enough data to sufficiently generate matches"
            
            # Gets grade level antimatches
            self.outer_apothem = 200
            people = self.outside_matches(key, True, prof["grade"])
            while (len(people) < Data.config["outputs"]["gradeantimatches"] + 3) and not (len(people) == (Data.grade_quantities[prof["grade"]] - 1)):
                self.apothem -= 0.5
                people = self.outside_matches(key, True, prof["grade"])
            try: 
                Data.profiles[key]['gradeantimatches'] = rd.sample(people, Data.config["outputs"]["gradeantimatches"])
                print(f'{key} has {len(people)} for 4')
            except:
                Data.profiles[key]['gradeantimatches'] = "Not enough data to sufficiently generate matches"

        if Data.config['debug']['plot']: 
            Graph().graph()
        print('Matches Made')
        Data.status += 15

    def inside_matches(self, di, use_grade, grade) -> list:
        people = []
        dist = []
        for key, prof in Data.profiles.items():
            if ((Data.profiles[di]['coords'][0] - self.apothem) < prof['coords'][0] < (
                    Data.profiles[di]['coords'][0] + self.apothem)) and (
                    (Data.profiles[di]['coords'][1] - self.apothem) < prof['coords'][1] < (
                    Data.profiles[di]['coords'][1] + self.apothem)):
                if use_grade: 
                    if (not key == di) and prof['grade'] == grade:
                        dist.append(((Data.profiles[di]['coords'][0] + Data.profiles[key]['coords'][0]) ** 2 + (
                                    Data.profiles[di]['coords'][1] + Data.profiles[key]['coords'][1]) ** 2) ** (1 / 2))
                        people.append(key)
                else:
                    if not key == di:
                        dist.append(((Data.profiles[di]['coords'][0] + Data.profiles[key]['coords'][0]) ** 2 + (
                                    Data.profiles[di]['coords'][1] + Data.profiles[key]['coords'][1]) ** 2) ** (1 / 2))
                        people.append(key)
        try:
            dist, people = zip(*sorted(zip(dist, people)))
        except:
            people = [0]

        return people
    
    def outside_matches(self, di, use_grade, grade) -> list:
        people = []
        dist = []
        for key, prof in Data.profiles.items():
            if ((Data.profiles[di]['coords'][0] - self.outer_apothem) > prof['coords'][0] or prof['coords'][0] < (
                    Data.profiles[di]['coords'][0] + self.outer_apothem)) and (
                    (Data.profiles[di]['coords'][1] - self.outer_apothem) > prof['coords'][1] or prof['coords'][1] < (
                    Data.profiles[di]['coords'][1] + self.outer_apothem)): 
                if use_grade: 
                    if (not key == di) and prof['grade'] == grade:
                        dist.append(((Data.profiles[di]['coords'][0] + Data.profiles[key]['coords'][0]) ** 2 + (
                                    Data.profiles[di]['coords'][1] + Data.profiles[key]['coords'][1]) ** 2) ** (1 / 2))
                        people.append(key)
                else:
                    if not key == di:
                        dist.append(((Data.profiles[di]['coords'][0] + Data.profiles[key]['coords'][0]) ** 2 + (
                                    Data.profiles[di]['coords'][1] + Data.profiles[key]['coords'][1]) ** 2) ** (1 / 2))
                        people.append(key)
        try:
            dist, people = zip(*sorted(zip(dist, people)))
        except:
            people = [0]

        return people[::-1]

    @staticmethod
    def generate_output() -> None:
        Data.output = pd.DataFrame(Data.config["output_cols"])
        for key, prof in Data.profiles.items():
            build_list = [Data.inputs.iloc[key]['First Name'] + ' ' + Data.inputs.iloc[key]['Last Name'], Data.inputs.iloc[key]['Username'],
                          [(Data.inputs.iloc[x]['First Name'] + ' ' + Data.inputs.iloc[x]['Last Name']) for x in prof['matches']],
                          [(Data.inputs.iloc[x]['First Name'] + ' ' + Data.inputs.iloc[x]['Last Name']) for x in prof['antimatches']],
                          [(Data.inputs.iloc[x]['First Name'] + ' ' + Data.inputs.iloc[x]['Last Name']) for x in prof['gradematches']],
                          [(Data.inputs.iloc[x]['First Name'] + ' ' + Data.inputs.iloc[x]['Last Name']) for x in prof['gradeantimatches']],
                          Data.profiles[key]['coords']
                          ]
            # Data.output.loc[len(Data.inputs.index)] = build_list
            Data.output.loc[key] = build_list

        print('Compiled')
        Data.status += 15

    @staticmethod
    def filter_outputs() -> None:
        drop_list = []
        for index, row in Data.output.iterrows():
            if row['Email'] in pd.merge(Data.output, Data.filtered, indicator=True, how='outer').query(
                    '_merge=="left_only"').drop('_merge', axis=1).values:
                drop_list.append(index)
        Data.output = Data.output.drop(drop_list)
        Data.status += 15
