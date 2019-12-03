from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session
from tempfile import mkdtemp

app = Flask(__name__)

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

@app.route("/")
def index():
	
	if "board" not in session:
		session["board"] = [[None, None, None], [None, None, None], [None, None, None]]
		session["turn"] = "x"

	return render_template("index.html", game=session["board"], turn=session["turn"])

@app.route("/reset")
def reset():

	session.clear()
	return redirect(url_for("index"))

@app.route("/play/<int:row>/<int:col>")
def play(row, col):

	session["board"][row][col] = session["turn"]

	#Find the winner
	for i in range(3):
		if (session["board"][i][0] == session["board"][i][1] == session["board"][i][2]) and (session["board"][i][0]):
			return render_template("winner.html", winner=session["board"][i][0])
	for j in range(3):
		if (session["board"][0][j] == session["board"][1][j] == session["board"][2][j]) and (session["board"][0][j]):
			return render_template("winner.html", winner=session["board"][0][j])
	if (session["board"][0][0] == session["board"][1][1] == session["board"][2][2]) and (session["board"][1][1]):
		return render_template("winner.html", winner=session["board"][1][1])
	if (session["board"][0][2] == session["board"][1][1] == session["board"][2][0]) and (session["board"][1][1]):
		return render_template("winner.html", winner=session["board"][1][1])

	#Draw
	draw = True
	for i in range(3):
		for j in range(3):
			if session["board"][i][j] == None:
				draw = False
	if draw:
		return render_template("draw.html")

	#Game continue
	if session["turn"] == "x":
		session["turn"] = "o"
	else:
		session["turn"] = "x"
	return redirect(url_for("index"))

if __name__=='__main__':
	app.run(debug=True)