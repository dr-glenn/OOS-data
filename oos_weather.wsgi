#!/home/jkhyrsmy/venv27/weather/bin/python
# Python virtualenv must be activated
# virtualenv must have dash and pandas
activate_this = '/home/jkhyrsmy/venv27/weather/bin/activate_this.py'

with open(activate_this) as f:
    code = compile(f.read(), activate_this, 'exec')
    exec(code, dict(__file__=activate_this))

import sys
# Add to Python search path so that the app itself can be found
sys.path.insert(0,'/home/jkhyrsmy/pyapps/OOS-data')

# standard way to run python wsgi program
from oos_wind_app import server as application
