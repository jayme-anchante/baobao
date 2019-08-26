import csv
from collections import OrderedDict
try:
    # for Python 2.x
    from StringIO import StringIO
except ImportError:
    # for Python 3.x
    from io import StringIO

class DataFrame: 
    def __init__(self):
        self.data = OrderedDict()
        pass
    def __repr__(self):
        string = ""
        for key in self.data:
            string += key+", "
        string += "\n"+"-" * len(string)
        for row in range(min(5, self.shape[0])):
            string += "\n"+", ".join([self.data[column][row] for column in self.columns])
        return string
    def __setitem__(self, key, value):
        """
        key (single position):
            When providing a single str and value in [None, 0, ""], create an empty column
        key (two positions):
            When providing an int and a str in columns, insert item into index
        """
        if type(key) == str and value in [None, 0, ""]:
            self.data[key] = []
        elif type(key[0]) == int and type(key[1]) == str and key[1] in self.columns:
            self.data[key[1]].insert(key[0], value)
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
            return (len(self.data[self.columns[0]]), len(self.data))
        return (0, 0)
    @property
    def columns(self):
        if self.data:
            return ([column for column in self.data.keys()])
        return (None)
    def append(self, other, ignore_index=False, verify_integrity=False, sort=None):
        if type(other) == dict:
            for key in other.keys():
                self.data[key].append(other[key])
        pass

def read(filepath_or_buffer, sep=","):
    with open(filepath_or_buffer) as f:
        header = f.readline()
        columns = header.replace("\n", "").split(sep)
        lines = f.readlines()
        length = len(lines)
        new_f = StringIO("".join(lines))
        reader = csv.reader(new_f)
        df = DataFrame()
        for column in columns:
            df[column] = None
        for row in reader:
            for column, value in zip(columns, row):
                df.append({column: value})
    return df
