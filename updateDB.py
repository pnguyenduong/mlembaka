
import json
from replit import db


def remove_duplicates(string_list):
  string_set = set(string_list)
  return list(string_set)


if __name__=="__main__":  
  chom = "chom"
  duong = "duong"
  badwords = "bad_words"
  warnings = "warnings"
  reminders = "reminders"
  
  data = json.load(open("stories.json"))
  
  # Get lists from DB
  reminders_list = db[reminders]
  chom_list = db[chom]
  duong_list = db[duong]
  print("DB duong list", duong_list)
  
  # Add words from json file to list
  # reminders_list.extend(data[reminders])
  chom_list.extend(data[chom])
  duong_list.extend(data[duong])

  print("before remove dups")
  print(reminders_list)
  print(chom_list)
  print(duong_list)

  reminders_list = remove_duplicates(reminders_list)
  chom_list = remove_duplicates(chom_list)
  duong_list = remove_duplicates(duong_list)
  
  print("after remove dups")
  print(reminders_list)
  print(chom_list)
  print(duong_list)

  db[reminders] = reminders_list
  db[chom] = chom_list
  db[duong] = duong_list
  
  print(reminders, db[reminders])
  print(chom, db[chom])
  print(duong, db[duong])
