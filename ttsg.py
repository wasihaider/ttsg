from flask import Flask, abort, request, render_template
from flask_cors import cross_origin, CORS
from scripts.process_admin_login import process_admin_login
from scripts.process_images import *

###########################################################

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
# from views import *

app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app, resources = {
	r"/": {"origin": "*"},
	## These are templates views ###
	r"/ttsg": {"origins": '*'},
	r"/ttsg/scene": {"origins": '*'},
	r"/ttsg/what": {"origins": '*'},
	r"/ttsg/how": {"origins": '*'},
	r"/ttsg/about": {"origins": '*'},
	r"/admin-ttsg": {"origins": '*'},
	r"/admin-panel": {"origins": '*'},
	## These are APIs
	r"/admin/login": {"origins": '*'},
	r"/get/images": {"origins": '*'},
	r"/delete/image": {"origins": '*'},
	r"/add/image": {"origins": '*'},
	r"/generate/scene": {"origins": '*'},
})


###########################################################

@app.route("/")
def hello():
	try:
		return "<h1 style='color:blue'>Hello There!</h1>"
	except Exception as e:
		print("Exception in views.py (hello method): ", str(e))


###########################################################

@app.route("/ttsg")
def index():
	try:
		return render_template("index.html")
	except Exception as e:
		print("Exception in views.py (index method): ", str(e))


###########################################################

@app.route("/ttsg/what")
def what():
	try:
		return render_template("what.html", title = "What is does")
	except Exception as e:
		print("Exception in views.py (what method): ", str(e))


###########################################################

@app.route("/ttsg/about")
def about():
	try:
		return render_template("about.html", title = "About us")
	except Exception as e:
		print("Exception in views.py (about method): ", str(e))


###########################################################

@app.route("/ttsg/how")
def how():
	try:
		return render_template("how.html", title = "How it works")
	except Exception as e:
		print("Exception in views.py (how method): ", str(e))


###########################################################

@app.route("/ttsg/scene")
def scene():
	try:
		return render_template("scene.html", title = "TTSG-Scene")
	except Exception as e:
		print("Exception in views.py (scene method): ", str(e))


#########################################################
@app.after_request
def add_header(response):
	# response.cache_control.no_store = True
	response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
	response.headers['Pragma'] = 'no-cache'
	response.headers['Expires'] = '-1'
	return response


###########################################################

@app.route("/admin-ttsg")
def admin_login():
	try:
		return render_template("admin_login.html")
	except Exception as e:
		print("Exception in views.py (index method): ", str(e))


###########################################################

@app.route("/admin-panel")
def admin_panel():
	try:
		return render_template("images.html")
	except Exception as e:
		print("Exception in views.py (index method): ", str(e))


###########################################################

@app.route('/admin/login', methods = ['POST'])
@cross_origin(origin = '*', headers = ["Content- Type", "application/json"])
def admin_ttsg_login():
	try:
		print("REQUEST: ", request.json)
		return process_admin_login(request.json)
	except Exception as e:
		print("Exception in ttsg.py (admin_ttsg_login method): ", str(e))
		abort(503)


###########################################################


@app.route('/get/images', methods = ['POST'])
@cross_origin(origin = '*', headers = ["Content- Type", "application/json"])
def get_images():
	try:

		return process_get_images(request.json)
	except Exception as e:
		print("Exception in ttsg.py (admin_ttsg_login method): ", str(e))
		abort(503)


###########################################################

@app.route('/delete/image', methods = ['POST'])
@cross_origin(origin = '*', headers = ["Content- Type", "application/json"])
def delete_image():
	try:

		return process_delete_image(request.json)
	except Exception as e:
		print("Exception in ttsg.py (admin_ttsg_login method): ", str(e))
		abort(503)


###########################################################

@app.route('/add/image', methods = ['POST'])
@cross_origin(origin = '*', headers = ["Content- Type", "application/json"])
def add_image():
	try:

		return process_add_image(request.json)
	except Exception as e:
		print("Exception in ttsg.py (admin_ttsg_login method): ", str(e))
		abort(503)


###########################################################

@app.route("/generate/scene", methods = ['POST'])
@cross_origin(origin = '*', headers = ["Content- Type", "application/json"])
def generate_scene():
	try:
		return process_generate_image(request.json)
	except Exception as e:
		print("Exception in views.py (user_input method): ", str(e))
		abort(503)


###########################################################

if __name__ == "__main__":
	import logging

	logging.basicConfig(filename = 'error.log', level = logging.DEBUG)
	app.run(host = '0.0.0.0')

###########################################################
