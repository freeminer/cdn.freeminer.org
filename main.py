from glob import glob
from binascii import a2b_hex
from time import sleep

from flask import Flask, request, abort

app = Flask(__name__)

known_hashes = set()


def init():
    for name in glob("data/*/*/*/*/*"):
        h = name.split("/")[-1]
        known_hashes.add(a2b_hex(h))

init()


@app.route("/index.mth", methods=["POST"])
def index_mth():
    data = request.data
    if not data.startswith("MTHS"):
        abort(400)
    result = set()
    count = (len(data) - 6) / 20
    for i in range(count):
        h = data[6 + i * 20:26 + i * 20]
        if h in known_hashes:
            result.add(h)

    response = "MTHS\x00\x01"
    response += "".join(result)

    print "Found {} files, not found {} files.".format(len(result), count - len(result))

    return response


@app.route("/")
def root():
    return "This server knows {} files.".format(len(known_hashes))

if __name__ == "__main__":
    app.run(debug=True)
