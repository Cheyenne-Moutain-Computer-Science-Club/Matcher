# =====================
# Package imports
# =====================
import pandas as pd
# =====================
# Module imports
# =====================
# from GUI import *
# from lint import *
# =====================
# Script
# =====================

class Main():
    profiles = {}
    output_csv = None

    def __init__(self, input_csv, pay_csv):
        self.inputs = pd.DataFrame(pd.read_csv(input_csv))


if __name__ == "__main__":
    GUI = GUI()
