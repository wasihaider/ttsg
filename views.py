from flask import request, render_template
from ttsg import app
from scripts.scene import Scene


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

@app.route("/ttsg", methods = ['POST'])
@app.route("/ttsg/scene", methods = ["POST"])
def user_input():
	try:
		text = request.form['textInput']
		image = Scene()
		image.generate_scene(text)
		return render_template("scene.html", path = '/static/images/scene.png')
	except Exception as e:
		print("Exception in views.py (user_input method): ", str(e))


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
