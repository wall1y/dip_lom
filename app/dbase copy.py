from app import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(20), unique=True, nullable=False)
    email=db.Column(db.String(20), unique=True, nullable=False)
    password=db.Column(db.String(60), nullable=False)
    isadmin=db.Column(db.Boolean)

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.isadmin}')"

class Hostgroup(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    group_name=db.Column(db.String(20), unique=True, nullable=False)
    members=db.relationship('Hosts', backref='hostgroup', lazy=True)
    pb_id=db.Column(db.Integer, db.ForeignKey('playbooks.id'))

    def __repr__(self):
        return f"Hostgroup('{self.group_name}', '{self.members}')"

class Playbooks(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    pb_name=db.Column(db.String(20), unique=True, nullable=False)
    group_members=db.relationship('Hosts', backref='playbooks', lazy=True)
    host_members=db.relationship('Hostgroup', backref='playbooks', lazy=True)

    def __repr__(self):
        return f"Hostgroup('{self.pb_name}', '{self.group_members}', {self.host_members})"

class Hosts(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    hostname=db.Column(db.String(200), unique=True, nullable=False)
    ip_address=db.Column(db.String(200), unique=True, nullable=False)
    last_sync_state=db.Column(db.String(10))
    last_sync=db.Column(db.DateTime)
    os=db.Column(db.String(100))
    group_id=db.Column(db.Integer, db.ForeignKey('hostgroup.id'), nullable=False)
    pb_id=db.Column(db.Integer, db.ForeignKey('playbooks.id'))
    
    def __repr__(self):
        return f"Hosts('{self.hostname}','{self.ip_address}','{self.os}', {self.group_id})"
