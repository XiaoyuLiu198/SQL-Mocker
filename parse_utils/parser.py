# from parse_utils.keywords import PATTERN2PARSER
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
        :return: dictionary
        """
        matched = self._tokenizer.lookahead
        if matched:
            pattern_parser = PATTERN2PARSER[matched.type]
            return pattern_parser(self._tokenizer).parse()
#
# re = Parser("select c1 from t1 where a1=9 or a2=7 and s3=10;").parse()
# re