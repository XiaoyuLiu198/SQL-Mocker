from parse_utils.tokenizer import Tokenizer
from parse_utils.pattern_parser import SelectWithPredicatePattern

SELECT_TYPE = "SELECT"
PATTERN2PARSER = {SELECT_TYPE: SelectWithPredicatePattern}


class Parser:
    def __init__(self, string: str):
        self._string = string
        self._tokenizer = Tokenizer(string)

    def parse(self):
        """
        Match sql operation type then parse into a tree
        :return: query object
        """
        matched = self._tokenizer.lookahead
        if matched:
            pattern_parser = PATTERN2PARSER[matched.type]
            return pattern_parser(self._tokenizer).parse()
