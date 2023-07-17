class Query:
    def __init__(self, sql_type, columns, table, predicates):
        self.sql_type = sql_type
        self.columns = columns
        self.table = table
        self.predicates = predicates


class SelectWithPredicatePattern:
    def __init__(self, tokenizer):
        self.tokenizer = tokenizer

    def parse(self):
        from parse_utils.parser_units import ColumnsParser, TableParser, PredicatesParser

        self.tokenizer.proceed("SELECT")
        columns, self.tokenizer = ColumnsParser(self.tokenizer).parse()
        self.tokenizer.proceed("FROM")
        table, self.tokenizer = TableParser(self.tokenizer).parse()
        self.tokenizer.proceed("WHERE")
        predicates, self.tokenizer = PredicatesParser(self.tokenizer).parse()
        self.tokenizer.proceed("END")
        return Query("select", columns, table, predicates)
