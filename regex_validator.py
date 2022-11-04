
valid_char = "ABCDEFGHIJKLMNOPQRSTUVWXYZÄÜÖß0123456789"
valid_special = "^|*+?"
valid_brackets = "()"
stack = []

def split_string(string):
        string_array = []
        string_array.extend(string)
        return string_array

def to_upper(char):
    if(char != "ß"):
        return char.upper()
    else: return char

def upper_string(string):
    string_array = split_string(string)
    for i in range(len(string_array)):
        string_array[i] = to_upper(string_array[i])
    return string_array

def verify_regex(regex):
    valid = False
    if(regex==None):
        return valid
    elif(regex==""):
        valid = True
        return valid
    else:
        regex = regex.replace(" ", "")
        regex_array = upper_string(regex)
        flag_special = False
        for char in regex_array:
            if(valid_char.__contains__(char)==True):
                flag_special = False
            elif(valid_special.__contains__(char)==True):
                if(flag_special == False):
                    flag_special = True
                else:
                    return valid
            elif(valid_brackets.__contains__(char)==True):
                if(char=="("):
                    stack.append("a")
                elif(char==")" and len(stack)>0):
                    stack.pop()
                else:
                    return valid
            else: return valid
    if(len(stack)==0):
        valid = True
        return valid
    else: return valid






regex = "Hallo mein Name ist (^)"
print(verify_regex(regex))




