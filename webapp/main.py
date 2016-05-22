from sense import Sense
import time

from flask import *
sensors = Sense()
app = Flask(__name__)

# Define app routes.
# Index route renders the main HTML page.
@app.route('/')
def index():
  conditions = sensors.current_conditions()
  record = sensors.record_conditions()
  return render_template('index.html', conditions=conditions, record=record)

@app.route('/log')
def log():
  readings = history()
  return render_template('log.html', readings=readings)

#@app.route('/temp')
#def temp():
#  def get_temperature():
#    while True:
#      conditions = sensors.current_conditions()
#      yield('data: {0}\n\n'.format(conditions))
#      time.sleep(600.0) # Wait 10 mins for new reading to be logged
#  return Response(get_temperature(), mimetype='text/event-stream')

def history():
  return sensors.read_log()

# Start the flask debug server listening on the pi port 5000 by default.
if __name__=='__main__':
  app.run(host='0.0.0.0', debug=True)
