from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def hello_world():
    return render_template('home.html')


@app.route('/foo',methods=['POST','GET'])
def foo():
	if request.method == 'POST':
		if request.form['submit'] == 'ISS':
			print "ISS"
		elif request.form['submit'] == 'Jupiter':
			print "Jupiter" # do something else
		else:
			print request.form['submit']
		return render_template('home.html')

if __name__=="__main__":
	app.run(debug=True)