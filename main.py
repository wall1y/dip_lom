from flask import Flask
import os
app = Flask(__name__)


def ping(hostname):
  response = os.system("ping -c 1 " + hostname)
  if response == 0:
    return f"{hostname} is up!"
  else:
    return "{hostname} is down!"
@app.route("/")
@app.route("/home")
def home():
    a=ping("192.168.0.1")
    return f"yay! {a}"
@app.route("/about")
def about():
    return "<h1>About Page</h1>"


if __name__ == '__main__':
    app.run(debug=True)