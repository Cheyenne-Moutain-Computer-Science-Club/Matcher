# =====================
# Package imports
# =====================
# =====================
# Module imports
# =====================
from matcher.GUI import GUI
from matcher.CLI import CLI
from matcher.data import Data
import json
# =====================
# Script
# =====================

if __name__ == "__main__":
    with open(r'config.json') as f:
        Data.config = json.load(f)
    if Data.config['settings']['use_CLI']: CLI = CLI()
    else: GUI = GUI()