# SQL-Mocker
A simplified mocker of SQL engine.

## Structure
- db_utils: including the executor of the parsed result, and database/table data structures with operation methods.
- 1. executor.py: entry point of SQL interpretion.
- 2. functions.py: interpret the parsed result with recursive pattern.
- 3. database.py: database structure and table data structure. To improve the efficiency of selection and filtration, table can be transformed into row-based structure and column based structure. Table input would be structured as ```{"column1": [value1, value2], "column2": []}```. Row based would be ```[{"column1": value, "column2": value}, {"column1": value, "column2": value}]```. Column based would be ```{"column1": {value_a: [row1, row2], value_b: [row3, row4]}}```.

- parse_utils: including a predictive recursive parser. 
- 1. parser.py: entry point of parsing.
- 2. regular_expressions.py & tokenizer.py: implement the tokenizer specifically designed for getting tokens from SQL
- 3. parser_units.py: implement parser for each components of the SQL string.

## Testing
```pytest tests/test.py```

## Extension
The framework is flexible to be extended for interpreting more complicated SQL statements. 
1. Support DELETE, INSERT, and UPDATE operation with extension to patterns.
2. Support Window function with extension to Column parser definition.
3. Support Temporal table with extension to Table parser definition.
