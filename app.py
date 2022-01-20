from operator import ne
import re
from flask import Flask, render_template, url_for, flash, redirect, request
from flask_sqlalchemy import SQLAlchemy
from forms import HostAddForm
from datetime import datetime
import os
import socket

app = Flask(__name__)
app.config['SECRET_KEY'] = '025da197e8c7e6b8d53c22c880cc74c2'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_ECHO'] = True
db=SQLAlchemy(app)


class User(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(20), unique=True, nullable=False)
    email=db.Column(db.String(20), unique=True, nullable=False)
    isadmin=db.Column(db.Boolean)

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.isadmin}')"

class Hostgroup(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    group_name=db.Column(db.String(20), unique=True, nullable=False)
    #members=db.relationship('Hosts', backref='hostgroup', lazy=True)

class Hosts(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    hostname=db.Column(db.String(200), unique=True, nullable=False)
    ip_address=db.Column(db.String(200), unique=True, nullable=False)
    last_sync_state=db.Column(db.String(10))
    last_sync=db.Column(db.DateTime)
    os=db.Column(db.String(100))
    #group_id=db.Column(db.Integer, db.ForeignKey('hostgroup.id'))
    def __repr__(self):
        return f"Hosts('{self.hostname}','{self.ip_address}','{self.os}')"

# hosts = [
#     {
#         'id': 0,
#         'hostname': 'server.domain.local',
#         'ip': '10.0.0.2',
#         'state': 'OK',
#         'last_sync': '15.12.2021',
#         'os': 'debian'
#     },
#     {
#         'id': 1,
#         'hostname': 'worstation.domain.local',
#         'ip': '10.0.0.3',
#         'state': 'UNKNOWN',
#         'last_sync': '15.11.2021',
#         'os': 'ubuntu'
#     }
# ]


@app.route("/")
@app.route("/host_list")
def host_list():
    #a=ping("192.168.0.11","192.168.0.102", "8.8.8.8", "1.1.1.1")
    list=Hosts.query.all()
    return render_template('host_list.html', hosts=list)

@app.route("/settings")
def settings():
    return render_template('settings.html', title='App settings')

@app.route("/hostadd", methods=['GET', 'POST'])
def hostadd():
    form = HostAddForm()
    if form.validate_on_submit():
      flash(f'Host created with hostname {form.hostname.data} and ip {form.ip.data}!', 'success')
      new_host=Hosts(hostname=form.hostname.data, ip_address=form.ip.data, os=form.os.data)
      print(form.hostname.data)
      db.session.add(new_host)
      db.session.commit()
      return redirect(url_for('host_list'))
    return render_template('hostadd.html',title='Add Host', form=form)

# @app.route("/host_info/<int:host_id>")
# def host_info(host_id):
#     host = hosts[host_id]
#     return render_template('host_info.html', title='Host Info' , host=host)

if __name__ == '__main__':
    app.run(debug=True)