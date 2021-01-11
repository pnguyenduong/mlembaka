from flask import Flask
from threading import Thread

app = Flask("")

@app.route('/')
def home():
  return "MlemBaka is up and running!"

def run():
  app.run(host="0.0.0.0", port=8000)

def uptime_monitor():
  t = Thread(target=run)
  t.start()