from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
import json

# configuration
DEBUG = True

# instantiate the app
app = Flask(__name__)
app.config.from_object(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'

cors = CORS(app, resources={r"/*": {"origins": "http://localhost:8080"}})

tweets_db = {}

@app.route('/')
def home():
    return 'unu'

@app.route('/queryTweets', methods=['GET'])
@cross_origin()
def query_tweets():
    query = request.args.get("query")
    print("query: " + query)

    # TODO: hacer query con el índice
    return {
            "id": 1026814183042687000,
            "date": "Tue Aug 07 12:55:53 +0000 2018",
            "text": "RT @de_patty: Asuuuuuuu..  @Renzo_Reggiardo me da mala espina...su pasado fujimorísta qué miedo!!!y @luchocastanedap hijo de corrupto que s…",
            "user_id": 544008122,
            "user_name": "@CARLOSPUEMAPE1",
            "location": {},
            "retweeted": True,
            "RT_text": "Asuuuuuuu..  @Renzo_Reggiardo me da mala espina...su pasado fujimorísta qué miedo!!!y @luchocastanedap hijo de corrupto que secunda lo del padre NI HABLAR! Más comunicore Plop!lideran las preferencias para la alcaldía de Lima, según Ipsos | RPP Noticias https://t.co/w5TnU0Dmwq",
            "RT_user_id": 302995560,
            "RT_user_name": "@de_patty"
           }

@app.route('/uploadFile', methods=['POST'])
@cross_origin()
def index_file():    
    return "success"

if __name__ == '__main__':
    app.run()

