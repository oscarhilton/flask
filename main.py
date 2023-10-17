from flask import Flask, send_file
from minio import Minio
import os

# Initialize a Minio client object.
minio_client = Minio(
    endpoint="bucket:9000",
    access_key="2M2WMeNkgMr3RUXwIgYy",
    secret_key="b7zL3NM37uosqdvhblwYj8UG9VHDEpmoFzhboC6i",
    secure=False
)

app = Flask(__name__)

@app.route('/')
def index():
    try:
        # Fetch a specific file from MY_BUCKET
        file_data = minio_client.get_object("google-news-vectors", "GoogleNews-vectors-negative300-SLIM.bin.gz")
        byte_stream = io.BytesIO(file_data.read())
        return send_file(byte_stream, attachment_filename='GoogleNews-vectors-negative300-SLIM.bin.gz', as_attachment=True)
    except Exception as e:
        return str(e), 500  # Return the exception message as a string, with a 500 Internal Server Error status code

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))