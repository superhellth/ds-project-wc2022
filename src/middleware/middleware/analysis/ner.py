import ujson

converted_dict = dict()
with open("./src/data/nes.json", "r", encoding="utf_8") as f:
    ne_dict = ujson.loads(f.read())

for item in ne_dict.items():
    key_string = item[0]
    parts = key_string.split(",")
    ne = parts[0][2:len(parts[0]) - 1]
    type = parts[1][2:len(parts[1]) - 2]
    converted_dict[(ne, type)] = item[1]


def get_nes_of_type(type):
    return {entry[0]: entry[1] for entry in converted_dict.items() if type in entry[0]}


def get_top_k(dict, k):
    as_list = sorted(dict.items(), key=lambda x: x[1], reverse=True)
    return {entry[0]: entry[1] for entry in as_list[:k]}


print(get_top_k(get_nes_of_type("EVENT"), 20))
