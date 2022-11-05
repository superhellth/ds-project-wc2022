# Globals
VALID_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZÄÜÖß0123456789"
VALID_SPECIAL = "^|*+?"
VALID_BRACKETS = "()"
TEST_EXPR_TRUE = ['Hallo mein Name ist (^)', u'\x46', 'Is THi5 tru3?', 'alpha', 'ne(nu(un)e)n']
TEST_EXPR_FALSE = ['+-=005', u'\u2764', r'{}()[]', '<!=(`{mep', '(123(te)']


def split_string(string):
    string_array = []
    string_array.extend(string)
    return string_array


def to_upper(char):
    if char != "ß":
        return char.upper()
    else:
        return char


def upper_string(string):
    string_array = split_string(string)
    for i in range(len(string_array)):
        string_array[i] = to_upper(string_array[i])
    return string_array


def verify_regex(expr):
    stack = []
    valid = False
    # Handle potential unicode
    expr = expr.encode('ascii', errors='backslashreplace')
    expr = expr.decode('ascii')
    if expr is None:
        return valid
    elif expr == "":
        valid = True
        return valid
    else:
        expr = expr.replace(" ", "")
        regex_array = upper_string(expr)
        flag_special = False
        for char in regex_array:
            if char in VALID_CHARS:
                flag_special = False
            elif char in VALID_SPECIAL:
                if not flag_special:
                    flag_special = True
                else:
                    return valid
            elif char in VALID_BRACKETS:
                if char == "(":
                    stack.append("a")
                elif char == ")" and len(stack) > 0:
                    stack.pop()
                else:
                    return valid
            else:
                return valid
    if len(stack) == 0:
        valid = True
        return valid
    else:
        return valid


def test_regex_validator():
    for test_exp in TEST_EXPR_TRUE:
        assert (verify_regex(test_exp))
    for test_exp in TEST_EXPR_FALSE:
        assert (not verify_regex(test_exp))


if __name__ == "__main__":
    test_regex_validator()
