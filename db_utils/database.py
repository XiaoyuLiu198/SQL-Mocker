from collections import defaultdict

class TableData:
    def __init__(self, data: dict, name: str):
        # Data as passed in formats {column1: [value1, value2], column2: []}
        self.data = data
        self.name = name

    @property
    def cols(self):
        return set(self.data.keys())

    @property
    def rows(self):
        # Assuming all columns are of the same size
        return len(self.data[list(self.data.keys())[0]])

    def to_row_base(self):
        """
        Transform data into a row based form.
        [{"column1": value, "column2": value}, {"column1": value, "column2": value}]
        """
        self.row_based = []
        for i, column in enumerate(list(self.data.keys())):
            if len(self.row_based) < i:
                self.row_based.append({})
            for j in range(self.data[column]):
                self.row_based[i][column] = self.data[column][j]
        return self.row_based

    def to_col_base(self):
        """
        Transform data into a column based form.
        {column1: {value_a: [row1, row2], value_b: [row3, row4]}}
        """
        self.col_based = {}
        for i, column in enumerate(list(self.data.keys())):
            if column not in self.col_based:
                self.col_based[column] = defaultdict(lambda: [])
            for j, val in enumerate(self.data[column]):
                self.col_based[column][val].append(j)
        return self.col_based


class DataBase:
    def __init__(self, tables: dict):
        self.tables = tables

    def list_table_names(self):
        names = list(self.tables.keys())
        return set(names)

    def check_table_existence(self, name):
        if name in self.tables.keys():
            return True
        return False

    def retrieve_table(self, name):
        return self.tables[name]



