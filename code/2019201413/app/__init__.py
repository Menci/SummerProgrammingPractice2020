from flask import Flask
app = Flask(__name__, static_folder="source")

auto = False

if auto == True:
    from . import route
else:
    from . import routes
