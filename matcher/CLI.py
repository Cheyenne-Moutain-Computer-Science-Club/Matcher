# =====================
# Package imports
# =====================
# =====================
# Module imports
# =====================
from matcher.data import Data
from matcher.core import Core
import json
import threading
from tkinter import filedialog
# =====================
# Script
# =====================
class CLI(Data):
    def __init__(self):
        super().__init__()
        self.run()
    
    def run(self):
        print('Matcher CLI instance created')
        if input('Do you wish to proceed? [Y/n]').lower() != 'y': return
        self.setup()

        self.Core = Core()
        x: None = threading.Thread(target=self.Core.run).start()

        Data.save_output_as = filedialog.asksaveasfilename(initialdir='C:', title="Save File", filetypes=(
            ('CSV file', "*.csv"), ('TSV file', "*.tsv"), ('TXT file', "*.txt"), ("all files", "*.*")))
        if Data.output_option == 'Comma Separated Values (*.csv)':
            Data.output.to_csv(f'{Data.save_output_as}.csv', index=False)
        elif Data.output_option == 'Tab Separated Values (*.tsv)':
            Data.output.to_csv(f'{Data.save_output_as}.tsv', index=False, sep="\t")
        elif Data.output_option == 'Text File (*.txt)':
            Data.output.to_csv(f'{Data.save_output_as}.txt', header=None, index=None, sep=' ', mode='a')

    def setup(self):
        with open(Data.config['settings']['conversions']) as f:
            Data.conversions = json.load(f)
        # Data.inputs = (Data.config['settings']['input'])
        Data.input_csv = r'C:\\Users\\micha\\OneDrive\Documents\\GitHub\\Matcher\\inputs\\DECA.csv'

