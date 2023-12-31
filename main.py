from flask import Flask, jsonify
from minio import Minio
from gensim.models import KeyedVectors
import os
import tempfile
import gzip
from textblob import TextBlob
from flask_cors import CORS

# Initialize a Minio client object.
minio_client = Minio(
    endpoint="bucket:9000",
    access_key="2M2WMeNkgMr3RUXwIgYy",
    secret_key="b7zL3NM37uosqdvhblwYj8UG9VHDEpmoFzhboC6i",
    secure=False
)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "https://similar.objobj.xyz" }})



def get_vectors():
    file_data = minio_client.get_object("google-news-vectors", "GoogleNews-vectors-negative300-SLIM.bin.gz")
    with tempfile.NamedTemporaryFile(delete=False) as temp_file:
        with gzip.GzipFile(fileobj=file_data) as gz:
            temp_file.write(gz.read())
    word_vectors = KeyedVectors.load_word2vec_format(temp_file.name, binary=True)
    os.unlink(temp_file.name)  # Delete temporary file
    return word_vectors

word_vectors = get_vectors()

@app.route('/')
def index():
    return jsonify({ "status": "OK" }), 200

@app.route('/api/similar/<word>')
def get_similar(word):
    try:
        antonyms = word_vectors.most_similar(positive=[word])
        antonym_words = [item[0] for item in antonyms]
        return jsonify({"similar": antonym_words, "word": word }), 200
    except Exception as e:
        return str(e), 500


@app.route('/api/sentiment/<text>')
def get_sentiment(text):
    blob = TextBlob(text)
    sentiment = blob.sentiment.polarity
    return jsonify({"sentiment": sentiment, "text": text }), 200

@app.route('/api/vector/<word>')
def get_vector(word):
    try:
        # Finding most similar vectors to the negative vector of the given word
        vector = word_vectors[word]
        return jsonify({"vector": vector.tolist(), "word": word }), 200
    except Exception as e:
        return str(e), 500