from app import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


group_playbooks = db.Table(
    "group_playbooks",
    db.Column("playbook_id", db.Integer, db.ForeignKey("playbooks.id")),
    db.Column("group_id", db.Integer, db.ForeignKey("hostgroup.id")),
)

host_playbooks = db.Table(
    "host_playbooks",
    db.Column("playbook_id", db.Integer, db.ForeignKey("playbooks.id")),
    db.Column("host_id", db.Integer, db.ForeignKey("hosts.id")),
)

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
    playbooks=db.relationship('Playbooks', secondary=group_playbooks, backref='hostgroups')
    
    def __repr__(self):
        return f"Hostgroup('{self.group_name}', '{self.members}')"

class Playbooks(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    pb_name=db.Column(db.String(20), unique=True, nullable=False)
    hosts=db.relationship('Hosts', secondary=host_playbooks, back_populates='playbooks')
    hotsgroups=db.relationship('Hostgroup', secondary=group_playbooks, back_populates='playbooks')

    def __repr__(self):
        return f"Hostgroup('{self.pb_name}')"

class Hosts(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    hostname=db.Column(db.String(200), unique=True, nullable=False)
    ip_address=db.Column(db.String(200), unique=True, nullable=False)
    last_sync_state=db.Column(db.String(10))
    last_sync=db.Column(db.DateTime)
    os=db.Column(db.String(100))
    group_id=db.Column(db.Integer, db.ForeignKey('hostgroup.id'), nullable=False)
    playbooks=db.relationship('Playbooks', secondary=host_playbooks, back_populates='hosts')
    
    def __repr__(self):
        return f"Hosts('{self.hostname}','{self.ip_address}','{self.os}', {self.group_id})"
