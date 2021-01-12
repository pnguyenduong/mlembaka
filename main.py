import requests
import json
import random
import os
import discord
from discord.ext import commands
from replit import db
from server import uptime_monitor

import constants

client = discord.Client()
client = commands.Bot(command_prefix=constants.command_prefix)


def get_quote():
    response = requests.get(constants.random_quotes_url)
    json_data = json.loads(response.text)
    quote = json_data[0]['q'] + " -" + json_data[0]['a']
    return (quote)


def print_list(string_list):
    result = ""
    for i, val in enumerate(string_list):
        result = result + str(i) + ". " + val + ", "

    return result


def add_keyword(new_keyword):
    db[new_keyword] = []


# add reminder
def update_warnings(warning):
    if constants.k_warnings in db.keys():
        warning_list = db[constants.k_warnings]
        warning_list.append(warning)
        db[constants.k_warnings] = warning_list
    else:
        db[constants.k_warnings] = [warning]


# add bad word
def update_badword(bad_word):
    if constants.k_bad_words in db.keys():
        bad_word_list = db[constants.k_bad_words]
        bad_word_list.append(bad_word)
        db[constants.k_bad_words] = bad_word_list
    else:
        db[constants.k_bad_words] = [bad_word]


# delete reminder
def delete_warning(index):
    warning_list = db[constants.k_warnings]
    if index >= 0 and index < len(warning_list):
        del warning_list[index]
    db[constants.k_warnings] = warning_list


# delete bad word
def delete_badword(index):
    bad_word_list = db[constants.k_bad_words]
    if index >= 0 and index < len(bad_word_list):
        del bad_word_list[index]
    db[constants.k_bad_words] = bad_word_list


@client.event
async def on_ready():
    print(f"We have logged in as {client.user}.")


@client.event
async def on_message(message):
    if message.author.bot:
        return
    msg = message.content.lower()

    if msg in db.keys() and len(db[msg]) > 0:
        await message.channel.send(random.choice(db[msg]))

    prefix = client.command_prefix

    # list of available commands
    if msg.startswith(prefix + constants.k_help):
        await message.channel.send(constants.help_list)

    # send quote
    if msg.startswith(prefix + constants.k_inspire):
        quote = get_quote()
        await message.channel.send(quote)

    # bot running with responding value = true
    if db[constants.k_responding]:
        if len(db[constants.k_warnings]) < 1:
            db[constants.k_warnings] = [constants.k_default_warning]

        if any(word in msg.lower() for word in db[constants.k_bad_words]):
            await message.channel.send(random.choice(db[constants.k_warnings]))

    # create a new warning message
    if msg.startswith(prefix + constants.k_add_warning):
        warning = msg.split(constants.k_add_warning + " ", 1)[1]
        update_warnings(warning)
        await message.channel.send(constants.k_warning_reply)

    # create a new bad word
    if msg.startswith(prefix + constants.k_add_badword):
        badword = msg.split(constants.k_add_badword + " ", 1)[1]
        update_badword(badword)
        await message.channel.send(constants.k_badword_reply)

    # delete a reminder by index number
    if msg.startswith(prefix + constants.k_del_warning):
        index = int(msg.split(constants.k_del_warning)[1])
        delete_warning(index)
        warning_list = db[constants.k_warnings]
        await message.channel.send(warning_list)

    # delete a bad word by index number
    if msg.startswith(prefix + "del_badword"):
        if "bad_words" in db.keys():
            index = int(msg.split("del_badword")[1])
            delete_badword(index)
            bad_words = db["bad_words"]
        await message.channel.send(bad_words)

    # get a list of warnings
    if msg == constants.command_prefix + constants.k_warnings:
        warning_list = print_list(db[constants.k_warnings])
        await message.channel.send(warning_list)

    # get a list of bad words
    if msg == constants.command_prefix + constants.k_bad_words:
        badword_list = print_list(db[constants.k_bad_words])
        await message.channel.send(badword_list)

    # turn the bot on/off
    if msg.startswith(prefix + constants.k_responding):
        value = msg.split(constants.k_responding + " ", 1)[1]

        if value.lower() == "on":
            db[constants.k_responding] = True
            await message.channel.send("Responding is on.")
        elif value.lower() == "off":
            db[constants.k_responding] = False
            await message.channel.send("Responding is off.")


uptime_monitor()
client.run(os.getenv('TOKEN'))  # TOKEN is stored in .env
