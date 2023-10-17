from flask import Flask, jsonify
from minio import Minio
from gensim.models import KeyedVectors
import io

# Initialize a Minio client object.
minio_client = Minio(
    endpoint="bucket:9000",
    access_key="2M2WMeNkgMr3RUXwIgYy",
    secret_key="b7zL3NM37uosqdvhblwYj8UG9VHDEpmoFzhboC6i",
    secure=False
)

app = Flask(__name__)

file_data = minio_client.get_object("google-news-vectors", "GoogleNews-vectors-negative300-SLIM.bin.gz")
word_vectors = KeyedVectors.load_word2vec_format(io.BytesIO(file_data.read()), binary=True)

@app.route('/')
def index():
    return "Hello World!"

@app.route('/api/antonym/<word>')
def get_antonym(word):
    try:
        # Finding most similar vectors to the negative vector of the given word
        antonyms = word_vectors.most_similar(negative=[word])
        antonym_words = [item[0] for item in antonyms]
        return jsonify({"antonyms": antonym_words}), 200
    except Exception as e:
        return str(e), 500