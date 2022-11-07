"""This is our regex validitor"""

# Globals
VALID_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZÄÜÖß0123456789 "
VALID_SPECIAL = "^|*+?"
VALID_BRACKETS = "()"
TEST_EXPR_TRUE = [
    'Hallo mein Name ist (^)', '\x46', 'Is THi5 tru3?', 'alpha', 'ne(nu(un)e)n', '', ""]
TEST_EXPR_FALSE = ['+-=005', '\u2764',
                   r'{}()[]', '<!=(`{mep', '(123(te)', None]


def split_string(string):
    """Splits string into char array"""
    string_array = []
    string_array.extend(string)
    return string_array


def to_upper(char):
    """Returns the uppercased letter"""
    if char != "ß":
        return char.upper()
    else:
        return char


def upper_string(string):
    """Converts string to array of upper case letters"""
    string_array = split_string(string)
    for i, char in enumerate(string_array):
        string_array[i] = to_upper(char)
    return string_array


def verify_regex(expr):
    """Our main verification method"""
    # To keep track of brackets
    stack = []

    # Check if string is None
    if expr is None:
        return False

    # Handle potential unicode
    expr = expr.encode('ascii', errors='backslashreplace')
    expr = expr.decode('ascii')

    # Pre-proccessing: Transform string to uppercased char array
    regex_array = upper_string(expr)

    # This flag is to make sure special characters don't appear immediately after each other
    flag_special = False

    # Iterate Char Array
    for char in regex_array:
        if char in VALID_CHARS:
            flag_special = False
        elif char in VALID_SPECIAL:
            if not flag_special:
                flag_special = True
            else:
                return False
        elif char in VALID_BRACKETS:
            if char == "(":
                stack.append("a")
            elif char == ")" and len(stack) > 0:
                stack.pop()
            else:
                return False
        else:
            return False
    if len(stack) == 0:
        return True
    return False


def test_regex_validator():
    """Test the regex expressins"""
    for test_exp in TEST_EXPR_TRUE:
        assert verify_regex(test_exp)
    for test_exp in TEST_EXPR_FALSE:
        assert not verify_regex(test_exp)


if __name__ == "__main__":
    test_regex_validator()
