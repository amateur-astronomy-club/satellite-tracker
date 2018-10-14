from flask import Flask, render_template, request

app = Flask(__name__, static_folder='../flask_app/static', template_folder='../flask_app/templates')


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