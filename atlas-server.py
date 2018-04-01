import os
import sys

from flask import Flask
import delegator

app = Flask(__name__)

HOSTDIR = sys.argv[1]


@app.route("/", defaults={"path": "/"})
@app.route("/<path:path>")
def route_all(path):
    if path.endswith("/"):
        path = path.rstrip("/")
        if os.path.isfile(os.path.join(HOSTDIR, path, "index.html")):
            with open(os.path.join(HOSTDIR, path, "index.html")) as f:
                return f.read()
        elif os.path.isfile(os.path.join(HOSTDIR, path, "index.py")):
            process = delegator.run("python " + os.path.join(HOSTDIR, path, "index.py"))
            return process.out
    return os.path.join(HOSTDIR, path)


app.run("0.0.0.0", 8080)
