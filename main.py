import requests
import json
import random
import os
import discord
from discord.ext import commands
from replit import db
from server import uptime_monitor

client = discord.Client()
client = commands.Bot(command_prefix="mlem!")

def get_quote():
  response = requests.get("https://zenquotes.io/api/random")
  json_data = json.loads(response.text)
  quote = json_data[0]['q'] + " -" + json_data[0]['a']
  return(quote)
  
# add reminder
def update_reminder(reminder_message):
  if "reminders" in db.keys():
    print("db keys: ", db.keys())
    print("reminders: ", db["reminders"])
    reminders = db["reminders"]
    reminders.append(reminder_message)
    db["reminders"] = reminders
  else:
    db["reminders"] = [reminder_message]

# add bad word
def update_badword(bad_word):
  if "bad_words" in db.keys():
    bad_words = db["bad_words"]
    bad_words.append(bad_word)
    db["bad_words"] = bad_words
  else:
    db["bad_words"] = [bad_word]

# delete reminder
def delete_reminder(index):
  reminders = db["reminders"]
  if len(reminders) > index:
    del reminders[index]
  db["reminders"] = reminders
  
# delete bad word
def delete_badword(index):
  bad_words = db["bad_words"]
  if len(bad_words) > index:
    del bad_words[index]
  db["bad_words"] = bad_words

@client.event
async def on_ready():
  print(f"We have logged in as {client.user}.")

@client.event
async def on_message(message):
  msg = message.content

  if msg.lower() in db.keys() and len(db[msg]) > 0:
    await message.channel.send(random.choice(db[msg]))
    
  print(msg)
  prefix = client.command_prefix
  print('prefix: ', prefix)
  
  # list of available commands 
  if msg.startswith(prefix + "help"):
    help_list = ["add_reminder","add_badword", "del_reminder", "del_badword", "reminders", "badwords", "responding"]
    await message.channel.send(help_list)

  # send quote
  if msg.startswith(prefix + "inspire"):
    quote = get_quote()
    await message.channel.send(quote)
  if msg.lower().startswith("chom") or msg.lower().startswith("chôm"):
    # await message.channel.send(story["chom"])
    await message.channel.send(random.choice(db["chom"]))
  _reminders_name = "reminders"

  # bot running with responding value = true 
  print("reminders: ", db[_reminders_name])
  if db["responding"]:
    reminders = []
    if "reminders" in db.keys():
      reminders = db[_reminders_name]
    
    if not db["reminders"]:
      print('hello im in here')
      reminders.append("shut da fuck up")
      db[_reminders_name] = reminders
      
    print(db["reminders"])
    if any(word in msg.lower() for word in db["bad_words"]):
      await message.channel.send(random.choice(reminders))

  # create a new reminder message
  if msg.startswith(prefix + "add_reminder"):
    reminder_message = msg.split("add_reminder ", 1)[1]
    update_reminder(reminder_message)
    await message.channel.send("You added a new reminder message!")

  # create a new bad_word message
  if msg.startswith(prefix + "add_badword"):
    badword = msg.split("add_badword ", 1)[1]
    update_badword(badword)
    await message.channel.send("You added a new bad word message!")

  # delete a reminder by index number
  if msg.startswith(prefix + "del_reminder"):
    if "reminders" in db.keys():
      index = int(msg.split("del_reminder")[1])
      delete_reminder(index)
      reminders = db["reminders"]
    await message.channel.send(reminders)

  # delete a bad word by index number
  if msg.startswith(prefix + "del_badword"):
    if "bad_words" in db.keys():
      index = int(msg.split("del_badword")[1])
      delete_badword(index)
      bad_words = db["bad_words"]
    await message.channel.send(bad_words)

  # get a list of reminders
  if msg.startswith(prefix + "reminders"):
    if "reminders" in db.keys():
      reminders = db["reminders"]
    await message.channel.send(reminders)

  # get a list of bad words
  if msg.startswith(prefix + "badwords"):
    if "bad_words" in db.keys():
      bad_words = db["bad_words"]
    await message.channel.send(bad_words)

  # turn the reminder feature on/off 
  if msg.startswith(prefix + "responding"):
    value = msg.split("responding ", 1)[1]

    if value.lower() == "on":
      db["responding"] = True
      await message.channel.send("Responding is on.")
    elif value.lower() == "off":
      db["responding"] = False
      await message.channel.send("Responding is off.")

uptime_monitor()
client.run(os.getenv('TOKEN')) # TOKEN is stored in .env