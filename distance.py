class Distance(Main):
    def __init__(self):
        Main.super()
        self.in_range = []
        self.range = [0,0]
        self.apothem = 0

    def calc_distance(self, id1, id2):
        return ((Main.profiles[id1]['coords'][0] + Main.profiles[id2]['coords'][0])**2 + (Main.profiles[id1]['coords'][1] + Main.profiles[id2]['coords'][1])**2) **(1/2)

    def get_people(self, id):
        # Get coords from id
        # Go through dict and if in range, add to self.in_range
        # If self.in_range.length() < 5, do over again with larger apothem
        # Else, grab five random people from that range and order by distance
        # Append this array to profile from id
        pass
