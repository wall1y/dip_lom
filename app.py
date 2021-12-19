import re
from flask import Flask, render_template, url_for, flash, redirect, request
from forms import HostAddForm
import os
import socket
app = Flask(__name__)


hosts = [
    {
        'id': 0,
        'hostname': 'server.domain.local',
        'ip': '10.0.0.2',
        'state': 'OK',
        'last_sync': '15.12.2021',
        'os': 'debian'
    },
    {
        'id': 1,
        'hostname': 'worstation.domain.local',
        'ip': '10.0.0.3',
        'state': 'UNKNOWN',
        'last_sync': '15.11.2021',
        'os': 'ubuntu'
    }
]



app.config['SECRET_KEY'] = '025da197e8c7e6b8d53c22c880cc74c2'

# def ping(*hostnames):
#   hosts=[]
#   for ip in  hostnames:
#     response = os.system("ping -c 3 " + ip)
#     if response == 0:
#       try:
#         hname=socket.gethostbyaddr(ip)
#       except OSError:
#         h= {'hostname':"N/A", 'ip':ip, 'state':"Up!"}
#       else:
#         h= {'hostname':hname[0], 'ip':ip, 'state':"Up!"}
#     else:
#       h= {'hostname':ip, 'state':"Down!"}
#     hosts.append(h)
#   return hosts
@app.route("/")
@app.route("/host_list")
def host_list():
    #a=ping("192.168.0.11","192.168.0.102", "8.8.8.8", "1.1.1.1")
    return render_template('host_list.html', hosts=hosts)

@app.route("/settings")
def settings():
    return render_template('settings.html', title='App settings')

@app.route("/hostadd", methods=['GET', 'POST'])
def hostadd():
    form = HostAddForm()
    if form.validate_on_submit():
      flash(f'Host created with hostname {form.hostname.data} and ip {form.ip.data}!', 'success')
      return redirect(url_for('host_list'))
    return render_template('hostadd.html',title='Add Host', form=form)

@app.route("/host_info/<int:host_id>")
def host_info(host_id):
    host = hosts[host_id]
    return render_template('host_info.html', title='Host Info' , host=host)

if __name__ == '__main__':
    app.run(debug=True)