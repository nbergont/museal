#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      nbergont
#
# Created:     12/02/2015
# Copyright:   (c) nbergont 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from flask import Flask, request, render_template, url_for, redirect, session
import json
import hashlib

CONF_FILE = 'conf.json'

app = Flask("audiobox")
app.secret_key = '7b237c9e4e47de2b27a247a3c1a7d7bc'

#*********** GLOBAL FUNCTIONS **************
conf = {}
def load_conf():
    global conf
    conf = json.loads(open(CONF_FILE, 'r').read())

def save_conf():
    global conf
    open(CONF_FILE, 'w').write(json.dumps(conf, indent=True))

def get_title():
    global conf
    return conf["audiobox"]["home_title"]

def getFile(id):
    global conf
    for sec in conf["sections"]:
        for file in sec["files"]:
            if file['id'] == id:
                return file
    return None

def lastFileId():
    global conf
    id = 0
    for sec in conf["sections"]:
        for file in sec["files"]:
            if id < file['id']:
                id = file['id']
    return id

def genFileId():
    return lastFileId() + 1

#*********** SERVER FUNCTIONS **************
@app.route('/')
@app.route('/list')
def list_page():
    global conf
    return render_template ('list.html', sections=conf["sections"], title=get_title())


@app.route ('/play/<int:id>')
def play_page(id):
    global conf
    f = getFile(id)
    if f :
        return render_template ('play.html', file=f, title=get_title())
    return redirect('list')


@app.route('/admin')
def admin_page():
    global conf
    if 'username' in session:
        return render_template ('admin.html', audiobox=conf["audiobox"], sections=conf["sections"], title=get_title())
    return redirect('login')

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    global conf
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        password_hash = hashlib.sha224(app.secret_key + password).hexdigest()
        app.logger.info(password_hash)

        if username == conf["audiobox"]['admin_login'] and password_hash == conf["audiobox"]['admin_password']:
            session['username'] = username
            return redirect('admin')
        else :
            return render_template ('error.html', msg='Wrong password or username', title=get_title())

    return render_template ('login.html', title=get_title())

@app.route('/logout')
def logout_page():
    session.pop('username', None)
    return redirect('list')

#*********** MAIN **************
if __name__ == '__main__':
    load_conf()
    app.run(debug=True, host='0.0.0.0', port=80, threaded=True)

