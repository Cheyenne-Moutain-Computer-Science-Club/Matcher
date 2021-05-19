# =====================
# Package imports
# =====================
import matplotlib.pyplot as plt
# =====================
# Module imports
# =====================
from matcher.data import Data
# =====================
# Script
# =====================
class Graph(Data):
    def __init__(self):
        super().__init__()
    
    def graph(self) -> None:
        x, y = [], []
        for key, prof in Data.profiles.items():
            x.append(prof['coords'][0])
            y.append(prof['coords'][1])
        plt.scatter(x, y)
        plt.show()