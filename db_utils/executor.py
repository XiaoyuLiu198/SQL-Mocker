from db_utils.functions import Selector


class Executor:
    def __init__(self, query, db):
        self.query = query
        self.db = db

    def execute(self):
        if self.query.sql_type == "select":
            return Selector(self.query, self.db).select()



