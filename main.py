from flask import Flask, render_template, url_for
import os
import socket
app = Flask(__name__)


def ping(*hostnames):
  hosts=[]
  for ip in  hostnames:
    response = os.system("ping -c 1 " + ip)
    if response == 0:
      hname=socket.gethostbyaddr(ip)
      h= {'hostname':hname[0], 'ip':ip, 'state':"Up!"}
    else:
      h= {'hostname':hname[0], 'ip':ip, 'state':"Down!"}
    hosts.append(h)
  return hosts
@app.route("/")
@app.route("/host_list")
def home():
    a=ping("192.168.0.1","192.168.0.106", "8.8.8.8", "1.1.1.1")
    return render_template('host_list.html', hosts=a)

@app.route("/about")
def about():
    return "<h1>About Page</h1>"


if __name__ == '__main__':
    app.run(debug=True)