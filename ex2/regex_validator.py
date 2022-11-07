"""This is our A1 T2 Regex validitor"""

VALID_CHARS = "ABCDEFGHIJKLMNOPQRSTUVWXYZÄÜÖß0123456789"
VALID_SPECIAL = "^|*+?"
VALID_BRACKETS = "()"
stack = []


def split_string(string):
    """Splits string ???"""
    string_array = []
    string_array.extend(string)
    return string_array


def to_upper(char):
    """Does nothing???"""
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


def verify_regex(expression: str):
    """Our main verification method"""
    valid = False
    if expression is None:
        return valid
    elif expression == "":
        valid = True
        return valid
    else:
        expression = expression.replace(" ", "")
        regex_array = upper_string(expression)
        flag_special = False
        for char in regex_array:
            if char in VALID_CHARS:
                flag_special = False
            elif char in VALID_SPECIAL:
                if flag_special is False:
                    flag_special = True
                else:
                    return valid
            elif char in VALID_BRACKETS:
                if char == "(":
                    stack.append("a")
                elif (char == ")" and len(stack) > 0):
                    stack.pop()
                else:
                    return valid
            else:
                return valid
    if len(stack) == 0:
        valid = True
        return valid
    return valid


REGEX_TO_CHECK = "Hallo mein Name ist (^)"
print(verify_regex(REGEX_TO_CHECK))
