from flask import Flask, jsonify
from minio import Minio
from gensim.models import KeyedVectors
import io
import tempfile
import gzip
from sklearn.preprocessing import MinMaxScaler

# Initialize a Minio client object.
minio_client = Minio(
    endpoint="bucket:9000",
    access_key="2M2WMeNkgMr3RUXwIgYy",
    secret_key="b7zL3NM37uosqdvhblwYj8UG9VHDEpmoFzhboC6i",
    secure=False
)

app = Flask(__name__)

file_data = minio_client.get_object("google-news-vectors", "GoogleNews-vectors-negative300-SLIM.bin.gz")
with tempfile.NamedTemporaryFile(delete=False) as temp_file:
    with gzip.GzipFile(fileobj=file_data) as gz:
        temp_file.write(gz.read())
word_vectors = KeyedVectors.load_word2vec_format(temp_file.name, binary=True)

@app.route('/')
def index():
    return jsonify({ "status": "OK" }), 200

@app.route('/api/vector/<word>')
def get_antonym(word):
    try:
        # Finding most similar vectors to the negative vector of the given word
        vector = word_vectors[word]
        scaler = MinMaxScaler(feature_range=(0, 100))
        normalized_data = scaler.fit_transform([vector])[0]
        return jsonify({word: normalized_data.tolist() }), 200
    except Exception as e:
        return str(e), 500