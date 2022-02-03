from hashlib import new
from flask import render_template, url_for, flash, redirect, request, abort
from app import app, db, bcrypt
from app.forms import EditorForm, HostAddForm, UserAddForm, LoginForm, NewFolderForm
from app.dbase import *
from flask_login import login_user, current_user, logout_user, login_required
from app.worker import get_facts, run_playbook
import os, subprocess, shutil

allow_root_path=f"{os.getcwd()}/playbooks"


@app.route("/")
@app.route("/host_list")
def host_list():
    list=Hosts.query.all()
    return render_template('host_list.html', hosts=list)

@app.route("/useradd", methods=['GET', 'POST'])
@login_required
def useradd():
    if current_user.is_authenticated:
        return redirect(url_for('host_list'))
    form = UserAddForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, isadmin=True)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been created! You are now able to log in', 'success')
        return redirect(url_for('login'))
    return render_template('useradd.html', title='Add new user', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('host_list'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('host_list'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('login.html', title='Login', form=form)

@app.route("/settings")
@login_required
def settings():
    return render_template('settings.html', title='App settings')

@app.route("/hostadd", methods=['GET', 'POST'])
@login_required
def hostadd():
    form = HostAddForm()
    if form.validate_on_submit():
      flash(f'Host created with hostname {form.hostname.data} and ip {form.ip.data}!', 'success')
      new_host=Hosts(hostname=form.hostname.data, ip_address=form.ip.data, os=form.os.data)
      print(form.hostname.data)
      db.session.add(new_host)
      db.session.commit()
      return redirect(url_for('host_list'))
    return render_template('hostadd.html',title='Add Host', form=form, legend='New host')

@app.route("/host_info/<int:host_id>")
@login_required
def host_info(host_id):
    host = Hosts.query.get_or_404(host_id)
    print(host)
    return render_template('host_info.html', title='Host Info' , host=host)

@app.route("/host_info/<int:host_id>/facts")
@login_required
def view_facts(host_id):
    host = Hosts.query.filter_by(id=host_id).first()
    facts=get_facts(host.ip_address)
    return render_template('host_facts.html', title='Host facts' , host=host, facts=facts)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('host_list'))

@app.route("/host_info/<int:host_id>/update", methods=['GET', 'POST'])
@login_required
def update_host(host_id):
    host = Hosts.query.get_or_404(host_id)
    # if post.author != current_user:
    #     abort(403)
    form = HostAddForm()
    if form.validate_on_submit():
        host.hostname = form.hostname.data
        host.ip_address = form.ip.data
        host.os = form.os.data
        db.session.commit()
        flash('Your Host has been updated!', 'success')
        return redirect(url_for('host_info', host_id=host.id))
    elif request.method == 'GET':
        form.hostname.data = host.hostname
        form.ip.data = host.ip_address
        form.os.data = host.os
    return render_template('hostadd.html', title='Update host',
                           form=form, legend='Update host')
 
@app.route("/host_info/<int:host_id>/delete", methods=['POST'])
@login_required
def delete_host(host_id):
    host = Hosts.query.get_or_404(host_id)
    # if host.author != current_user:
    #     abort(403)
    db.session.delete(host)
    db.session.commit()
    flash('Your post has been deleted!', 'success')
    return redirect(url_for('host_list'))

@app.route("/host_info/<int:host_id>/task")
@login_required
def run_task(host_id):
    host = Hosts.query.filter_by(id=host_id).first()
    task=run_playbook(host.ip_address, "ping.yml")


    return render_template('task_info.html', title='Task run info' , host=host, task=task['stat'])

@app.route("/playbooks")
@login_required
def playbooks():
    form=NewFolderForm()
    target_path=request.args.get('path')

    if not target_path or allow_root_path not in target_path:
        current_working_directory=allow_root_path
    else:       
        current_working_directory=request.args.get('path')
        print(current_working_directory)
    file_list=subprocess.check_output(f'ls {current_working_directory}', shell=True).decode('utf-8').split('\n')
    return render_template('playbooks.html', legend='Playbooks list', allow_root_path=allow_root_path, current_working_directory=current_working_directory,file_list=file_list, form=form)

@app.route('/playbooks/cd')
@login_required
def cd():
    os.chdir(request.args.get('path'))
    print(request.args.get('path'))
    return redirect(url_for('playbooks', path=request.args.get('path')))


@app.route('/playbooks/new_dir', methods=['GET', 'POST'])
@login_required
def new_dir():
    file_dir=request.args.get('path')
    form = NewFolderForm()
    print(file_dir)
    print(form.dirname.data)
    if form.validate_on_submit():
        new_dirname=file_dir+form.dirname.data
        print(new_dirname)
        os.mkdir(new_dirname)
    return redirect(url_for('playbooks'))

@app.route('/playbooks/rm')
@login_required
def rm():
    shutil.rmtree(request.args.get('path'))
    return redirect('/playbooks')
    
@app.route('/playbooks/view')
@login_required
def view():
    filename=request.args.get('filename')
    filedir=request.args.get('path')
    filepath=filedir+filename
    with open(filepath, 'r') as f:
        file_content=f.read()
    return render_template('playbook_view.html', title='Editor', playbook=file_content, filename=filename, filedir=filedir)

@app.route('/playbooks/edit', methods=['GET', 'POST'])
@login_required
def playbook_edit():
    filename=request.args.get('filename')
    file_dir=request.args.get('file')
    full_path_to_file=request.args.get('file')+filename

    with open(full_path_to_file, 'r+') as f:
        file_content=f.read()
    form = EditorForm()
    if form.validate_on_submit():
        if file_content != form.content.data or filename != form.filename.data:
            if filename != form.filename.data and file_content == form.content.data:
                new_name=file_dir+form.filename.data
                os.rename(full_path_to_file,new_name)
            if file_content != form.content.data and filename == form.filename.data:
                with open(full_path_to_file, 'w') as f:
                    f.write(form.content.data)
            if file_content != form.content.data and filename != form.filename.data:
                new_name=file_dir+form.filename.data
                os.rename(full_path_to_file,new_name)
                with open(new_name, 'w') as f:
                    f.write(form.content.data)
        return redirect(url_for('playbooks'))
    elif request.method == 'GET':
        form.filename.data = filename
        form.content.data = file_content
    return render_template('editor.html', title='Editor', form=form, file_dir=file_dir, legend='Editor')
