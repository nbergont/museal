#-------------------------------------------------------------------------------
# Name:        MUSELA
# Author:      nbergont
# Created:     12/02/2015
# Copyright:   (c) nbergont 2015
# Licence:     GPL2
#-------------------------------------------------------------------------------

from flask import Flask, request, render_template, url_for, redirect, session, send_file
import json
import uuid
import hashlib
import os
import re

CONF_FILE = 'conf.json'
DEFAULT_CONF_FILE = 'default_conf.json'
HOSTAPD_FILE = '/etc/hostapd/hostapd.conf'
app = Flask('MUSEAL')
conf = {} #Global json configuration

#*********** GLOBAL FUNCTIONS **************
def load_conf():
	global conf
	if os.path.exists(CONF_FILE):
		conf = json.loads(open(CONF_FILE, 'r').read())
	else: #First loading : generate new file
		conf = json.loads(open(DEFAULT_CONF_FILE, 'r').read())
		app.secret_key = uuid.uuid4().hex #Generate app secret key
		conf['secret_key'] = app.secret_key
		conf['options']['admin_password'] = hash_password('admin') #Create default password
		save_conf()

def save_conf():
	global conf
	open(CONF_FILE, 'w').write(json.dumps(conf, indent=True))
	if hasattr(os, 'sync'): #Prevent filesystem error on RPI
		os.sync()

def change_hostapd_ssid(name):
	if os.path.exists(HOSTAPD_FILE):
		str_file = re.sub(r'ssid=.*', 'ssid='+name, open(HOSTAPD_FILE, 'r').read())
		open(HOSTAPD_FILE, 'w').write(str_file)

def get_title():
	global conf
	return conf["options"]["home_title"]

def getSection(id):
	global conf
	for sec in conf["sections"]:
		if sec['id'] == id:
			return sec
	return None

def getFile(id):
	global conf
	for sec in conf["sections"]:
		for file in sec["files"]:
			if file['id'] == id:
				return file
	return None

def getFileSection(id):
	global conf
	for sec in conf["sections"]:
		for file in sec["files"]:
			if file['id'] == id:
				return sec
	return None

def getNextFileId(tag):
	global conf
	for sec in conf["sections"]:
		for file in sec["files"]:
			if file['tag'] == tag+1:
				return file['id']
	return None

def getPreviousFileId(tag):
	global conf
	for sec in conf["sections"]:
		for file in sec["files"]:
			if file['tag'] == tag-1:
				return file['id']
	return None

def genSecId():
	global conf
	id = 0
	for sec in conf["sections"]:
		if id < sec['id']:
			id = sec['id']
	return id + 1

def genFileId():
	global conf
	id = 0
	for sec in conf["sections"]:
		for file in sec["files"]:
			if id < file['id']:
				id = file['id']
	return id + 1

def addSection(label):
	global conf
	id = genSecId()
	conf['sections'].append({'label':label, 'id':id, 'files':[]})
	return id

def addFile(section_id, label, tag, description, filename):
	sec = getSection(section_id)
	id = genFileId()
	sec['files'].append({'label':label,'tag':tag,'desc':description,'filename':filename, 'type': 'audio', 'id':id})
	return id

def remove_file(id):
	f = getFile(id)
	filename = os.path.join(app.config['UPLOAD_FOLDER'], f['filename'])
	if os.path.exists(filename):
		os.remove(filename)
	sec = getFileSection(id)
	sec["files"].remove(f)

def remove_section(id):
	sec = getFileSection(id)
	for file in sec["files"]:
		remove_file(file['id'])
	conf["sections"].remove(sec)

def hash_password(password):
	return hashlib.sha224(app.secret_key + password).hexdigest()

def isAdmin():
	return 'login' in session and session['login'] == conf["options"]["admin_login"]

def logout_admin():
	session.pop('login', None)

def allowed_ext(filename, ext):
	return filename.rsplit('.', 1)[1].lower() in ext

#*********** SERVEUR INIT **************

load_conf() #Load config file
app.secret_key = conf['secret_key']
app.config['UPLOAD_FOLDER'] = 'static/media'

#*********** SERVER FUNCTIONS **************
@app.route('/')
@app.route('/list')
def list_page():
	global conf
	if conf["sections"] :
		return render_template ('list.html', sections=conf["sections"], title=get_title())
	else:
		return render_template ('info.html', msg='Go to <a href="/admin">admin page</a> to add new audio media', title=get_title())


@app.route ('/play/<int:id>')
def play_page(id):
	f = getFile(id)
	if f :
		return render_template ('playjs.html', file=f, next_id=getNextFileId(f["tag"]), previous_id=getPreviousFileId(f["tag"]), title=get_title())
	return redirect('list')


@app.route('/admin')
def admin_page():
	global conf
	if isAdmin():
		return render_template ('admin.html', options=conf["options"], sections=conf["sections"], title=get_title())
	return redirect('login')

@app.route('/login', methods=['GET', 'POST'])
def login_page():
	global conf
	if request.method == 'POST':
		login = request.form['login']
		password = request.form['password']

		if login == conf["options"]['admin_login'] and hash_password(password) == conf["options"]['admin_password']:
			session['login'] = login
			return redirect('admin')
		else :
			return render_template ('error.html', msg='Wrong password or login', title=get_title())

	return render_template ('login.html', title=get_title())

@app.route('/logout')
def logout_action():
	logout_admin()
	return redirect('list')


@app.route('/set_options', methods=['POST'])
def set_options_post():
	global conf
	if isAdmin() and request.method == 'POST':
		conf["options"]['home_title'] = request.form['home_title']
		conf["options"]['hostspot_name'] = request.form['hostspot_name']
		change_hostapd_ssid(conf["options"]['hostspot_name'])
		save_conf()

	return redirect('admin')


@app.route('/set_login', methods=['POST'])
def set_login_post():
	global conf
	if isAdmin() and request.method == 'POST':
		login = request.form['login']
		password1 = request.form['password1']
		password2 = request.form['password2']

		if password1 == password2:
			conf["options"]['admin_login'] = login
			conf["options"]['admin_password'] = hash_password(password1)
			conf["options"]['first_launch'] = False
			save_conf()
			logout_admin()
		else:
			return render_template ('error.html', msg='Wrong passwords', title=get_title())

	return redirect('login')

@app.route ('/remove/<int:id>')
def remove_action(id):
	if isAdmin():
		remove_file(id)
		save_conf()
		return redirect('admin')
	return redirect('login')

@app.route ('/remove_section/<int:id>')
def remove_sec_action(id):
	if isAdmin():
		remove_section(id)
		save_conf()
		return redirect('admin')
	return redirect('login')

@app.route ('/move_up/<int:id>')
def move_up_action(id):
	global conf
	if isAdmin():
		for sec in conf["sections"]:
			files = sec["files"]
			for i, file in enumerate(files):
				if file['id'] == id and i > 0:
					files[i], files[i-1] = files[i-1], files[i] #Swap items
					save_conf()
					break
		return redirect('admin')
	return redirect('login')

@app.route ('/move_down/<int:id>')
def move_down_action(id):
	global conf
	if isAdmin():
		for sec in conf["sections"]:
			files = sec["files"]
			for i, file in enumerate(files):
				if file['id'] == id and i+1 < len(files):
					files[i+1], files[i] = files[i], files[i+1] #Swap items
					save_conf()
					break
		return redirect('admin')
	return redirect('login')

@app.route ('/edit/<int:id>', methods=['GET', 'POST'])
def edit_page(id):
	if isAdmin():
		f=getFile(id)
		if request.method == 'POST':
			f['tag'] = int(request.form['tag'])
			f['label'] = request.form['label']
			f['desc'] = request.form['description']
			save_conf()
			return redirect('admin')
		else:
			return render_template ('edit.html', file=f, title=get_title())
	return redirect('login')

@app.route('/upload')
def upload_page():
	global conf
	if isAdmin():
		return render_template ('upload.html', sections=conf["sections"], title=get_title())
	return redirect('login')

@app.route('/upload_file', methods=['POST'])
def upload_file_post():
	if isAdmin() and request.method == 'POST':
		section_id = int(request.form['section_id'])
		tag = int(request.form['tag'])
		label = request.form['label']
		description = request.form['description']
		file = request.files['file']

		if file and allowed_ext(file.filename, ['mp3']):
			filename = uuid.uuid4().hex + '.mp3' #Generate filename
			file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

			addFile(section_id, label, tag, description, filename)
			save_conf()
			return redirect('admin')

		return render_template ('error.html', msg='Wrong file type', title=get_title())

	return redirect('login')

@app.route('/add_section', methods=['POST'])
def add_section_post():
	if isAdmin() and request.method == 'POST':
		label = request.form['label']
		addSection(label)
		save_conf()
	return redirect('admin')

@app.route('/rename_section/<int:id>', methods=['GET', 'POST'])
def rename_section(id):
	if isAdmin():
		sec = getSection(id)
		if request.method == 'POST':
			sec['label'] = request.form['label']
			save_conf()
		else:
			return render_template ('rename_section.html', section=sec, title=get_title())
	return redirect('admin')

#QRCode generator
@app.route('/qrcode/<int:id>')
def get_qrcode(id):
	try:
		import qrcode
		import StringIO
	except ImportError:
		return render_template ('error.html', msg='No QRCode module', title=get_title())
	img = qrcode.make('www.museal.org/play/' + str(id))
	img_io = StringIO.StringIO()
	img.save(img_io, 'PNG')
	img_io.seek(0)
	return send_file(img_io, mimetype='image/png')

#Global redirection
@app.route('/<path:url>', methods=['GET', 'POST'])
def redirect_page(url):
	return redirect('list')


#*********** MAIN **************
if __name__ == '__main__':
	app.run(debug=True, port=80)
	#app.run(debug=True, host='0.0.0.0', port=80, threaded=True)

