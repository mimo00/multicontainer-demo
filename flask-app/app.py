import sys
import time

from elasticsearch import Elasticsearch, exceptions
from flask import Flask

app = Flask(__name__)
es = Elasticsearch(host='es')


def test_connection(retry=3):
    """ connect to ES with retry """
    if not retry:
        print("Out of retries. Bailing out...")
        sys.exit(1)
    try:
        status = es.indices.exists("test_index")
        return status
    except exceptions.ConnectionError as e:
        print("Unable to connect to ES. Retrying in 5 secs...")
        time.sleep(5)
        test_connection(retry - 1)


@app.route('/')
def hello_world():
    return 'Hello World'


if __name__ == '__main__':
    test_connection()
    app.run(host="0.0.0.0", port=5000, debug=True)
