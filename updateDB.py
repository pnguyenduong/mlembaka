
import json
from replit import db


def remove_duplicates(string_list):
  string_set = set(string_list)
  return list(string_set)

def lower_case(string_list):
    return [x.lower() for x in string_list]


if __name__=="__main__":  
  
  data = json.load(open("stories.json"))
  
  print(data.keys())
  for val in data.keys():
    if val not in db:
      db[val] = []
    phrase_list = db[val]
    print(val, " ", phrase_list)
    phrase_list.extend(lower_case(data[val]))
    phrase_list = remove_duplicates(phrase_list)
    db[val] = phrase_list
    print(val, " in db ", db[val])
