from db_utils.database import TableData, DataBase
from db_utils.executor import Executor
from parse_utils.parser_units import PredicateObject, ColumnsObject, TableObject
from parse_utils.pattern_parser import Query
from parse_utils.tokenizer import Token
from parse_utils.parser import Parser

test1 = {"col1": [1, 2, 3, 4.5, 5, 6], "col2": [2, 5, 3, 2, 4, 6], "col3": [2, 3, 4, 5, 7, 6]}
test2 = {"col1": ["val1", "val2", "val3"], "col2": ["val1", "v5", "v6"]}

table_1 = TableData(data=test1, name="dataset_1")
table_2 = TableData(data=test2, name="dataset_2")

db = DataBase({table_1.name: table_1, table_2.name: table_2})


def test_select_function():
    query = Query("select", ColumnsObject(columns=["col1"]), TableObject(table="dataset_1"),
                  PredicateObject(logic="or", lhs=
                  PredicateObject(logic="equal", lhs=Token(type="VARIABLE", value="col1"),
                                  rhs=Token(type="NUMBER", value=2)),
                                  rhs=PredicateObject(logic="equal", lhs=Token(type="VARIABLE", value="col1"),
                                                      rhs=Token(type="NUMBER", value=6))))
    res = Executor(query=query, db=db).execute()
    assert res == {'col1': [2, 6]}


def test_select_statement():
    query = "select col1 from dataset_1 where col1=2;"
    parsed_query = Parser(query).parse()
    res = Executor(query=parsed_query, db=db).execute()
    assert res == {'col1': [2]}

def test_select_statement_1():
    query = "select col1 from dataset_1 where not col1=2;"
    parsed_query = Parser(query).parse()
    res = Executor(query=parsed_query, db=db).execute()
    assert res == {'col1': [1,3,4.5,5,6]}

def test_select_statement_2():
    query = "select col1 from dataset_1 where col1=2 and col2=5;"
    parsed_query = Parser(query).parse()
    res = Executor(query=parsed_query, db=db).execute()
    assert res == {'col1': [2]}


def test_select_statement_3():
    query = "select col1, col2 from dataset_1 where col1=2 or col2=5;"
    parsed_query = Parser(query).parse()
    res = Executor(query=parsed_query, db=db).execute()
    assert res == {'col1': [2], 'col2': [5]}


def test_select_statement_4():
    query = "select col1, col2 from dataset_1 where col1=6 or col2=5 and col1=2;"
    parsed_query = Parser(query).parse()
    res = Executor(query=parsed_query, db=db).execute()
    assert res == {'col1': [2, 6], 'col2': [5, 6]}


def test_select_statement_5():
    query = 'select col1 from dataset_2 where col1="val1";'
    parsed_query = Parser(query).parse()
    res = Executor(query=parsed_query, db=db).execute()
    assert res == {'col1': ['val1']}


def test_select_statement_6():
    query = 'select col1 from dataset_2 where not col1="val1";'
    parsed_query = Parser(query).parse()
    res = Executor(query=parsed_query, db=db).execute()
    assert res == {'col1': ['val2', 'val3']}


def test_select_statement_7():
    query = 'select col1 from dataset_2 where not col1="val1" and col2="v5" or col2="val1";'
    parsed_query = Parser(query).parse()
    res = Executor(query=parsed_query, db=db).execute()
    assert res == {'col1': ['val1', 'val2']}
