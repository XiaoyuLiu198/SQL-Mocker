class Token:
    def __init__(self, type, value, start=None):
        self.type = type
        self.value = value
        self.start = start


def generate_tokens(pattern, text):
    scanner = pattern.scanner(text)
    for m in iter(scanner.match, None):
        token = Token(type=m.lastgroup, value=m.group(), start=m.lastindex)

        if token.type != 'INDENT':
            if token.type == "NUMBER":
                token.value = float(token.value)
            elif token.type == "STRING":
                token.value = token.value.strip('"')
            yield token


class Tokenizer:
    def __init__(self, string: str):
        from parse_utils.regular_expressions import REGEX_PATTERNS

        self._string = string
        self._cursor = 0
        self._lookahead = None
        self._tokens = generate_tokens(REGEX_PATTERNS, self._string)
        self.take_next()

    @property
    def string(self):
        return self._string

    @string.setter
    def string(self, string):
        self._string = string

    @property
    def cursor(self):
        return self._cursor

    @cursor.setter
    def cursor(self, cursor):
        self._cursor = cursor

    @property
    def lookahead(self):
        return self._lookahead

    @lookahead.setter
    def lookahead(self, val):
        self._lookahead = val

    def has_more_token(self):
        return len(self.string) > self.cursor

    def take_next(self):
        """
        Generate next token in the string with iterator
        """
        try:
            res = next(self._tokens)
            self.lookahead = res
        except:
            print("Reached end of string")


    def proceed(self, expected: str):
        """
        Check whether following string is matched with an expected token type, move pointer ahead with take_next

        param expected: expected input from the pre-defined pattern
        """
        token = self.lookahead
        if not token:
            raise SyntaxError("Already reached end of string")
        if token.type != expected:
            raise SyntaxError("Wrong type")
        else:
            if self.has_more_token():
                self.take_next()
