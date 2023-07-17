import re

# define all the expressions to match here
SELECT = r'(?P<SELECT>select)'
FROM = r'(?P<FROM>from)'
WHERE = r'(?P<WHERE>where)'
STRING = r'(?P<STRING>\"(.+?)\")'
COMMA = r'(?P<COMMA>,)'
OPERATOR = r'(?P<EQUAL>=)'
LOGIC_OR = r'(?P<OR>or)'
LOGIC_AND = r'(?P<AND>and)'
LOGIC_NOT = r'(?P<NOT>not)'
NUMBER = r'(?P<NUMBER>\b\d+(\.\d+)?\b)'
VARIABLE = r'(?P<VARIABLE>\b[^,^=^;\s]+\b)'
END = r'(?P<END>;)'
INDENT = r'(?P<INDENT>\s+)'

REGEX_PATTERNS = re.compile('|'.join((SELECT, FROM, WHERE, STRING, COMMA, OPERATOR, LOGIC_OR, LOGIC_AND, LOGIC_NOT,
                                      NUMBER, VARIABLE, INDENT, END)))
