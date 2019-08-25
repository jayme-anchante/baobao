import csv
from collections import OrderedDict

class DataFrame: 
    def __init__(self, columns, length):
        self.columns = columns
        self.length = length
        self.data = OrderedDict({column: [] for column in self.columns})
        self.shape = (self.length, len(self.columns))
        self.dtypes = {}
        pass
    def __repr__(self):
        string = ""
        for key in self.data:
            string += key+", "
        string += "\n"+"-" * len(string)
        for row in range(min(5, self.length)):
            string += "\n"+", ".join([self.data[column][row] for column in self.columns])
        return string
    def __setitem__(self, key, value):
        self.data[key].append(value)
        pass
    def _setitem(self, row, column, value):
        pass
    def __getitem__(self, key):
        """
        key (int or str):
            When providing a single int, return a single row.
            When providing a single str, return a single column
        """
        try:
            column = key
            return self.data[column]
        except (KeyError) as e:
            pass
        try:
            row = int(key)
            return tuple([self.data[column][row] for column in self.data])
        except (ValueError, TypeError) as e:
            return e
    @property
    def shape(self):
        if self.data:
            return (len(self.data[0]), len(self.data))
        return (0, 0)

def read(filepath):
    with open(filepath) as f:
        length = sum(1 for line in f) - 1
    with open(filepath) as f:
        reader = csv.reader(f)
        headers = next(reader, None)
        df = DataFrame(headers, length)
        for row in reader:
            for c, r in zip(headers, row):
                df[c] = r
    return df
