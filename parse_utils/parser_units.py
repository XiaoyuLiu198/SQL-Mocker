class ColumnsObject:
    def __init__(self, columns: list):
        self.columns = columns


class ColumnsParser:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer

    def parse(self):
        columns = [self.tokenizer.lookahead.value]
        self.tokenizer.proceed("VARIABLE")
        while self.tokenizer.lookahead and self.tokenizer.lookahead.type == "COMMA":
            self.tokenizer.proceed("COMMA")
            columns.append(self.tokenizer.lookahead.value)
            self.tokenizer.proceed("VARIABLE")
        return ColumnsObject(columns=columns), self.tokenizer


class TableObject:
    def __init__(self, table):
        self.table = table


class TableParser:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer

    def parse(self):
        table = self.tokenizer.lookahead.value
        self.tokenizer.proceed("VARIABLE")
        return TableObject(table=table), self.tokenizer


class PredicateParser:

    def __init__(self, tokenizer):
        self.tokenizer = tokenizer

    def parse(self):
        if self.tokenizer.lookahead.type == "NOT":
            self.tokenizer.proceed("NOT")
            predicate = PredicateObject(logic="not_equal", lhs=None, rhs=None)
        else:
            predicate = PredicateObject(logic="equal", lhs=None, rhs=None)
        lhs = self.tokenizer.lookahead
        self.tokenizer.proceed("VARIABLE")
        self.tokenizer.proceed("EQUAL")
        rhs = self.tokenizer.lookahead
        self.tokenizer.proceed(rhs.type)
        predicate.lhs = lhs
        predicate.rhs = rhs
        return predicate, self.tokenizer


class AndParser:

    def __init__(self, tokenizer):
        self.tokenizer = tokenizer

    def parse(self):

        conditions = []
        value, tokenizer = PredicateParser(self.tokenizer).parse()
        conditions.append(value)
        self.tokenizer = tokenizer
        lhs = value
        while self.tokenizer.lookahead and self.tokenizer.lookahead.type == "AND":
            self.tokenizer.proceed("AND")
            value, tokenizer = PredicateParser(self.tokenizer).parse()
            self.tokenizer = tokenizer
            rhs = value
            lhs = PredicateObject(logic="and", lhs=lhs, rhs=rhs)
        return lhs, self.tokenizer


class PredicatesParser:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer

    def parse(self):
        conditions = []
        value, tokenizer = AndParser(self.tokenizer).parse()
        lhs = value
        conditions.append(value)
        self.tokenizer = tokenizer
        while self.tokenizer.lookahead and self.tokenizer.lookahead.type == "OR":
            self.tokenizer.proceed("OR")
            value, tokenizer = AndParser(self.tokenizer).parse()
            rhs = value
            lhs = PredicateObject(logic="or", lhs=lhs, rhs=rhs)
            self.tokenizer = tokenizer
        return lhs, self.tokenizer


class PredicateObject:
    def __init__(self, logic, lhs, rhs):
        self.logic = logic
        self.lhs = lhs
        self.rhs = rhs

# from parse_utils.tokenizer import Tokenizer
#
# sql_str = "not a1=8 or a2=6 or a3=7"
# tokenizer = Tokenizer(sql_str)
# res = PredicatesParser(tokenizer).parse()
# res