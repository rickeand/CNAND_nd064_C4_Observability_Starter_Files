import os
import time
import requests

from flask import Flask, jsonify, render_template

import logging
from jaeger_client import Config
from flask_opentracing import FlaskTracing

app = Flask(__name__)


def init_tracer(service):
    logging.getLogger("").handlers = []
    logging.basicConfig(format="%(message)s", level=logging.DEBUG)

    config = Config(
        config={"sampler": {"type": "const", "param": 1,}, "logging": True,
        'reporter_batch_size': 1,},
        service_name=service,
    )

    # this call also sets opentracing.tracer
    return config.initialize_tracer()


jagertracer = init_tracer("test-service")
tracer = FlaskTracing(jagertracer,True, app)

@app.route("/")
def homepage():
    return render_template("main.html")

@app.route("/beta")
def beta():
    with tracer.tracer.start_span("beta") as span:
        span.set_tag('http.method',"GET")
        r = requests.get("https://www.google.com/search?q=python")
        dict = {}
        for key, value in r.headers.items():
            print(key, ":", value)
            dict.update({key: value})
        return jsonify(dict)


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=int(os.environ.get("PORT", 8083)))