s = '{"id":2,"name":"111 продукт1"}'
s = s.replace("{", "").replace("}", "").split(",")

dictionary = {}

for i in s:
    dictionary[i.split(":")[0].strip('\'').replace("\"", "")] = i.split(":")[1].strip('"\'')

print(dictionary)

import json
h = '{"id":2,"name":"111 продукт1"}'
d = json.loads(h)
print(d)

type(d)
