from sense import Sense

from flask import *
sensors = Sense()
app = Flask(__name__)

# Define app routes.
# Index route renders the main HTML page.
@app.route('/')
def index():
  conditions = sensors.current_conditions()
  readings = history()
  record = {'temp':{'max':100,'min':0},'press':{},'humid':{}}
  return render_template('index.html', conditions=conditions, record=record)

@app.route('/log')
def log():
  readings = history()
  return render_template('log.html', readings=readings)

def history():
  return sensors.read_log()

# Start the flask debug server listening on the pi port 5000 by default.
if __name__=='__main__':
  app.run(host='0.0.0.0', debug=True)
