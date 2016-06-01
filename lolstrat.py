from flask import Flask, render_template, redirect, request, session
from flaskext.mysql import MySQL

app = Flask(__name__)
app.debug = True
app.config['MYSQL_DATABASE_USER'] = ''
app.config['MYSQL_DATABASE_PASSWORD'] = ''
app.config['MYSQL_DATABASE_DB'] = ''
app.config['MYSQL_DATABASE_HOST'] = ''
mysql = MySQL()
mysql.init_app(app)

#Route to index and show party
@app.route('/')
@app.route('/party/<partyid>')
def index(partyid=None):
	yo = None
	if session.get('nick'):
		cursor = mysql.connect().cursor()
		cursor.execute("select riotID from summoners where summonerName='" + session['nick'] + "'")
		sumID = cursor.fetchone()
		sumID = sumID[0]
		cursor.execute("select name from champions where id=17");
		sumImage = cursor.fetchone()
		sumImage = sumImage[0]
	else:
		sumImage = None
	return render_template("index.html", partyid=partyid, nick=session['nick'], sumImage=sumImage)

#Handle quick join form
@app.route('/party/', methods=['POST'])
def party():
	session['nick'] = request.form['nick']
	session['partyid'] = request.form['partyid']
	session['yo'] = ''
	#return render_template("index.html", partyid=partyid)
	return redirect("/party/%s" % request.form['partyid'], code=302)

#Catch all other paths, route to index
@app.route('/<path:path>')
def catch_all(path):
	return redirect("/", code=302)

if __name__ == '__main__':
	app.secret_key = 'A0Zr98j/3yX R~XHH!jmN]LWX/,?RT'
	app.run(host='0.0.0.0')