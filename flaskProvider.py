from flask import Flask
from threading import Thread

#  Using Flask for HTTP monitor
app = Flask("")


#  Monitoring status
@app.route("/")
def home():
    return "Twitter Scraper is ON"


#  Running locally on port 8080
def run():
    app.run(host="0.0.0.0", port=8080)


#  Threading, keeping on monitoring in a single Thread action
def keep_alive():
    t = Thread(target=run)
    t.start()
