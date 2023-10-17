from flask import Flask, jsonify
from minio import Minio
import os

# Initialize a Minio client object.
minio_client = Minio(
    endpoint="bucket:9000",
    access_key="z0JkVnGjKZUBEzMFfVpd",
    secret_key="jIVNFUyP6WfOoaOiNHz54Ip9Q9ljMFc27CUwTD5q",
    secure=False
)

app = Flask(__name__)

@app.route('/')
def index():
    try:
        # Fetch the list of buckets
        buckets = minio_client.list_buckets()
        # Convert the list of buckets to a list of bucket names
        bucket_names = [bucket.name for bucket in buckets]
        return jsonify({"buckets": bucket_names})
    except Exception as e:
        return str(e), 500  # Return the exception message as a string, with a 500 Internal Server Error status code

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
