from flask import render_template, request

from flask_app import app


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/foo', methods=['POST', 'GET'])
def foo():
    if request.method == 'POST':
        space_object = request.form['submit']

    return render_template('home.html')


try:
    app.run('0.0.0.0', 5000)
except KeyboardInterrupt:
    print("Interrupted...")

print("Ended...")
