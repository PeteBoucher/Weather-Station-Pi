from sense import Sense

from flask import *
sensors = Sense()
app = Flask(__name__)

# Define app routes.
# Index route renders the main HTML page.
@app.route('/')
def index():
  conditions = sensors.current_conditions()
  return render_template('index.html', conditions=conditions)

@app.route('/log')
def log():
  readings = sensors.read_log()
  return render_template('log.html', readings=readings)

# Start the flask debug server listening on the pi port 5000 by default.
if __name__=='__main__':
  app.run(host='0.0.0.0', debug=True)