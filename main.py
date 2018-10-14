from hardware.Control import Control
from tracking import parser, update_tle, NITK
from tracking.Tracker import Tracker
from flask import Flask, render_template, request

control = Control(freq=100, verbose=1)  # hardware control
tracker = Tracker(home=NITK, freq=1, verbose=1)  # find position of objects in space

print("Updating TLEs from the web...")
update_tle()


# call back function to point hardware every time tracking is updated
def set_position():
    az, alt = tracker.get_position()
    control.set_target(az, alt)


tracker.set_callback(set_position)

# Web App Flask UI
# ===========================================================================================

app = Flask(__name__, static_folder='flask_app/static', template_folder='flask_app/templates')


@app.route('/')
def home():
    return render_template('home.html')


@app.route('/foo', methods=['POST', 'GET'])
def foo():
    if request.method == 'POST':

        space_object = request.form['submit']
        parsed_object = parser(space_object)

        if parsed_object is None: print("Couldn't find object...")

        tracker.set_object(parsed_object)

    return render_template('home.html')


# ===========================================================================================

control.start()  # start thread
tracker.start()  # start thread

app.run('0.0.0.0', 5000)  # runs till keyboard interrupt

tracker.stop()  # stop threads
control.stop()
