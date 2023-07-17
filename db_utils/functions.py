from operator import itemgetter


class Union:
    def __call__(self, lists):
        res = set()
        for x in lists:
            for val in x:
                res.add(val)
        return list(res)


class Intersect:
    def __call__(self, lists):
        res = set.intersection(*[set(x) for x in lists])
        return list(res)


class Selector:
    def __init__(self, query, db):
        self.query = query
        self.db = db

    def semantic_checker(self):
        if not self.db.check_table_existence(self.query.table.table):
            raise ValueError("Table is not in the database")
        for col in self.query.columns.columns:
            if col not in self.db.retrieve_table(self.query.table.table).cols:
                raise ValueError("Column is not in the table")
        return True

    def select(self):
        if self.semantic_checker():
            data = self.db.retrieve_table(self.query.table.table)
            if self.query.predicates:
                idx = Filter(self.query.predicates, data).filter()
                res = {}
                for col in self.query.columns.columns:
                    if len(idx) > 1:
                        res[col] = list(itemgetter(*idx)(data.data[col]))
                    else:
                        res[col] = [data.data[col][idx[0]]]
            else:
                return data.data[self.query.columns.columns]
            return res


class Filter:
    def __init__(self, predicates, table):
        self.predicates = predicates
        self.table = table

    def filter(self):
        return self.visit_predicate(self.predicates)

    def visit_predicate(self, predicate):
        if predicate.logic == "or":
            lhs_val = self.visit_predicate(predicate.lhs)
            rhs_val = self.visit_predicate(predicate.rhs)
            return Union()([lhs_val, rhs_val])
        elif predicate.logic == "and":
            return Intersect()([self.visit_predicate(predicate.lhs), self.visit_predicate(predicate.rhs)])
        elif predicate.logic == "not_equal":
            return self.not_equal(predicate)
        elif predicate.logic == "equal":
            return self.equal(predicate)

    def equal(self, predicate):
        rhs = predicate.rhs
        lhs = predicate.lhs
        if rhs.type == "NUMBER" or rhs.type == "STRING":
            self.table.to_col_base()
            return self.table.col_based[lhs.value][rhs.value]
        elif rhs.type == "VARIABLE":
            self.table.to_row_base()
            result = []
            for row in range(self.table.rows):
                if self.table.row_based[row][lhs.value] == self.table.row_based[row][rhs.value]:
                    result.append(row)
            return result

    def not_equal(self, predicate):
        equal_idx = set(self.equal(predicate))
        result = []
        for i in range(self.table.rows):
            if i not in equal_idx:
                result.append(i)
        return result
