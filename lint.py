class Lint(Main):
    def __init__(self, convertions):
        Main.super()
        self.convertions = convertions

    def convert(self, key):
        convert = []

        for index, row in Main.inputs.iterrows():
            if convertions.key[0] == row[key]:
                convert.append(0)
            elif convertions.key[1] == row[key]:
                convert.append(1)
            elif convertions.key[2] == row[key]:
                convert.append(2)
            elif convertions.key[3] == row[key]:
                convert.append(3)
            else:
                raise TypeError

        inputs[key] = convert

    def create_profiles(self):
        for index, row in Main.inputs.iterrows():
            profiles[index] = {
                'id': index,
                'coords': [],
                'matchs': []
            }
