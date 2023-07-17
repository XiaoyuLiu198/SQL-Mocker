from parse_utils.parser import Parser
from db_utils.executor import Executor
examples = []

def execute(sql_string: str, db_input: dict):
    database = db_input
    parsed_sql = Parser(sql_string).parse()
    res = Executor(parsed_sql, database).execute()
    return res


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    for sql_string, db_tables in examples:
        execute(sql_string, db_tables)

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
