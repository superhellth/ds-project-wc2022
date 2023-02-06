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

sorted_list = sorted(ne_dict.items(), key=lambda x: x[1], reverse=True)
print(sorted_list[0:20])
sorted_list = sorted(converted_dict.items(), key=lambda x: x[1], reverse=True)
print(sorted_list[0:20])
