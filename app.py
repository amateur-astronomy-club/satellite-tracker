import threading

from flask import Flask, render_template, request


class object_setter:
    def __init__(self):
        app = Flask(__name__)

        self.current_object = None

        @app.route('/')
        def hello_world():
            return render_template('home.html')

        @app.route('/foo', methods=['POST', 'GET'])
        def foo():
            if request.method == 'POST':
                print request.form['submit']
                self.current_object = request.form['submit']
            return render_template('home.html')

        print "Starting App..."
        thread = threading.Thread(target=app.run)
        thread.setDaemon(False)  # don't keep thread running in the back ground
        thread.start()
        print "App started..."
