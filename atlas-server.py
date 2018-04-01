import os
import sys

from flask import Flask, send_from_directory, abort, send_file
import delegator

app = Flask(__name__)

HOSTDIR = sys.argv[1]


@app.route("/", defaults={"path": "/"})
@app.route("/<path:path>")
def route_all(path):

    if path.endswith("/") or os.path.isdir(os.path.join(HOSTDIR, path)):

        original_path = path

        if not original_path.endswith("/"):
            original_path += "/"

        path = os.path.join(HOSTDIR, path.rstrip("/"))

        if os.path.isfile(os.path.join(path, "index.html")):
            return send_from_directory(path, "index.html")

        elif os.path.isfile(os.path.join(path, "index.py")):
            process = delegator.run("python " + os.path.join(path, "index.py"))
            return process.out

        else:
            resp = ""
            for file in os.listdir(path):
                resp += '<a href="{0}{1}">{1}</a><br>'.format(original_path, file)
            return resp

    elif path.endswith(".py"):

        path = os.path.join(HOSTDIR, path)

        if not os.path.isfile(path):
            abort(404)

        process = delegator.run("python " + path)
        return process.out

    else:
        path = os.path.join(HOSTDIR, path)

        if not os.path.isfile(path):
            abort(404)

        return send_file(path)


app.run("0.0.0.0", 8080)
