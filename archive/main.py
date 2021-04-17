# =====================
# Package imports
# =====================
import pandas as pd
# =====================
# Module imports
# =====================
from lint import Lint
from graph import Graph
from distance import Distance
from compile import Compile
import convertions as cv
# =====================
# Script
# =====================

class Main():
    profiles = {}
    output = None
    input_csv = None
    pay_csv = None
    use_tsv_inputs = None
    use_tsv_paid = None
    use_paid_list = None
    only_include_paid = None
    output_option = None
    convertions = cv.convertions
    finished = False

    def __init__(self):
        pass

    def convert(self):
        if self.use_tsv_inputs:
            self.inputs = pd.DataFrame(pd.read_csv(self.input_csv, sep='\t'))
        else:
            self.inputs = pd.DataFrame(pd.read_csv(self.input_csv))

        if self.use_paid_list:
            if self.use_tsv_inputs:
                self.paid = pd.DataFrame(pd.read_csv(self.pay_csv, sep='\t'))
            else:
                self.paid = pd.DataFrame(pd.read_csv(self.pay_csv))
            if self.only_include_paid:
                drop_list = []
                for index, row in self.inputs.iterrows():
                    if row['Email Address'] in pd.merge(self.inputs, self.paid, indicator=True, how='outer').query('_merge=="left_only"').drop('_merge', axis=1).values:
                        drop_list.append(index)
                self.inputs = self.inputs.drop(drop_list)

        Lint = Lint()
        Graph = Graph()
        Distance = Distance()
        Compile = Compile()
        
        print('Convert')
    

