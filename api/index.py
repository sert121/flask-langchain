from flask import Flask,request
from flask_cors import CORS
from .helpers import lang_init

app = Flask(__name__)
CORS(app,resources={r"/*": {'origins': '*'}})

@app.route('/test_lang')
def home():
    result = lang_init(urls=['https://nike.com'])
    # use this result to add it to a chatgpt prompt before returning it
    
    return result
    # return 'Hello, World!'
@app.route('/', methods=['GET'])
def test():
    return 'Hello, World!'

@app.route('/woot', methods=['POST'])
def woot():
    data = request.get_json()
    print("logging the route... woot")
    return data

@app.route('/about')
def about():
    return 'About'