from flask import Flask, jsonify, request, flash
from flask_cors import CORS, cross_origin
from generate_index import retrieval_cosine, create_index, create_tweets_index, create_complete_tweets_index
import json
import os

# configuration
UPLOAD_FOLDER = './uploads/'
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'

cors = CORS(app, resources={r"/*": {"origins": "http://localhost:8080"}})

@app.route('/')
def home():
    return '¡Bienvenido Profesor Heider!'

@app.route('/queryTweets', methods=['GET'])
@cross_origin()
def query_tweets():
    query = request.args.get("query")
    # k = request.args.get("k")
    print("query: " + query)

    # TODO: -1 por ahora, pero luego sacar el 'k' del request
    result = retrieval_cosine(query, -1)
    return json.dumps(result)
    

@app.route('/uploadFile', methods=['POST'])
@cross_origin()
def index_file():
    file = request.files['file']
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    create_index(file.filename)
    create_tweets_index(file.filename)
    create_complete_tweets_index(file.filename)
    print(file.filename)
    return "success"

if __name__ == '__main__':
    app.run()

