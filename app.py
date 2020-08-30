from routes.words import words_api
from routes.definitions import definitions_api
from settings import *

app.register_blueprint(words_api)
app.register_blueprint(definitions_api)

app.run(port=5000)
