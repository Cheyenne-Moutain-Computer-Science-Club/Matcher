# =====================
# Package imports
# =====================
import pandas as pd
import random as rd
# =====================
# Module imports
# =====================
from data import Data
# =====================
# Script
# =====================

class Core(Data):
    def __init__(self):
        super().__init__()
        self.apothem = 15

    def run(self):
        self.convert()
        # self.Lint = Lint()
        # self.Graph = Graph()
        # self.Distance = Distance()
        # self.Compile = Compile()
        self.lint()
        self.create_profiles()
        self.create_coordinates()
        self.get_people()
        self.generate_output()
        if Data.use_filtered_list:
            self.filter_outputs()

    @staticmethod
    def convert():
        if Data.use_tsv_inputs:
            Data.inputs = pd.DataFrame(pd.read_csv(Data.input_csv, sep='\t'))
        else:
            Data.inputs = pd.DataFrame(pd.read_csv(Data.input_csv))

        if Data.use_filtered_list:
            if Data.use_tsv_inputs:
                Data.filtered = pd.DataFrame(pd.read_csv(Data.filter_csv, sep='\t'))
            else:
                Data.filtered = pd.DataFrame(pd.read_csv(Data.filter_csv))
            if Data.only_include_filtered:
                drop_list = []
                for index, row in Data.inputs.iterrows():
                    if row['Email Address'] in pd.merge(Data.inputs, Data.filtered, indicator=True, how='outer').query(
                            '_merge=="left_only"').drop('_merge', axis=1).values:
                        drop_list.append(index)
                Data.inputs = Data.inputs.drop(drop_list)

    @staticmethod
    def lint():
        heads = list(Data.inputs.columns)
        for col in heads:
            if col in Data.conversions:
                convert = []
                for index, row in Data.inputs.iterrows():
                    convert.append(Data.conversions[col][row[col]])
                Data.inputs[col] = convert
        print('Convert from Lint')

    @staticmethod
    def create_profiles():
        for index, row in Data.inputs.iterrows():
            Data.profiles[index] = {
                'id': index,
                'coords': [],
                'matches': []
            }
        print('Profiles Created')

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

    def get_people(self):
        for key, prof1 in Data.profiles.items():
            people = self.in_range(key)
            while len(people) < 13:
                self.apothem += 3
                people = self.in_range(key)
            Data.profiles[key]['matches'] = rd.sample(people, 10)
        print('Matches Made')

    def in_range(self, di):
        people = []
        dist = []
        for key, prof in Data.profiles.items():
            if ((Data.profiles[di]['coords'][0] - self.apothem) < prof['coords'][0] < (
                    Data.profiles[di]['coords'][0] + self.apothem)) and (
                    (Data.profiles[di]['coords'][1] - self.apothem) < prof['coords'][1] < (
                    Data.profiles[di]['coords'][1] + self.apothem)):
                if key == di:
                    pass
                else:
                    dist.append(((Data.profiles[di]['coords'][0] + Data.profiles[key]['coords'][0]) ** 2 + (
                                Data.profiles[di]['coords'][1] + Data.profiles[key]['coords'][1]) ** 2) ** (1 / 2))
                    people.append(key)
        dist, people = zip(*sorted(zip(dist, people)))
        return people

    @staticmethod
    def generate_output():
        Data.output = pd.DataFrame({"Name": [], "Email Address": [], "Matches": []})
        for key, prof in Data.profiles.items():
            build_list = [Data.inputs.iloc[key]['Name'], Data.inputs.iloc[key]['Email Address'],
                          [Data.inputs.iloc[x]['Name'] for x in prof['matches']]]
            # Data.output.loc[len(Data.inputs.index)] = build_list
            Data.output.loc[key] = build_list

        print('Compiled')

    @staticmethod
    def filter_outputs():
        drop_list = []
        for index, row in Data.output.iterrows():
            if row['Email Address'] in pd.merge(Data.output, Data.filtered, indicator=True, how='outer').query(
                    '_merge=="left_only"').drop('_merge', axis=1).values:
                drop_list.append(index)
        Data.output = Data.output.drop(drop_list)
