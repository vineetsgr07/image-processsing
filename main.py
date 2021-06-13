import flask
import pymongo
from imageToText import image_to_Text
from key import keyPath

app = flask.Flask(__name__)
app.config["DEBUG"] = True

client = pymongo.MongoClient(keyPath)
db = client.test

print("db", db)
@app.route('/', methods=['GET'])
def home():
    return '''<h1>Distant Reading Archive</h1>
<p>A prototype API for distant reading of science fiction novels.</p>'''


# A route to return all of the available entries in our catalog.
@app.route('/api/v1/transform-image', methods=['GET'])
def api_all():
    path = 'images/1.jpg'
    characterWithText, imageWithText, actualImage, croppedImage = image_to_Text(path)
    db.mapper.insert_one({'title': "todo title", 'body': "todo body"})
    return imageWithText

app.run()