from time import sleep
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from prometheus_flask_exporter import PrometheusMetrics
import opentracing
from jaeger_client import Config
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.instrumentation.requests import RequestsInstrumentor
from flask_opentracing import FlaskTracer


app = Flask(__name__)
FlaskInstrumentor().instrument_app(app)
RequestsInstrumentor().instrument()

PrometheusMetrics(app)

app.config["MONGO_DBNAME"] = "example-mongodb"
app.config[
    "MONGO_URI"
] = "mongodb://example-mongodb-svc.default.svc.cluster.local:27017/example-mongodb"

mongo = PyMongo(app)

# defaults to reporting via UDP, port 6831, to localhost
def initialize_tracer():
    config = Config(
        config={
            'sampler': {
                'type': 'const',
                'param': 1
            },
            'logging': True
        },
        service_name='backend-service'
    )
    # also sets opentracing.tracer
    return config.initialize_tracer()

flask_tracer = FlaskTracer(initialize_tracer, True, app, ["url_rule"])


@app.route("/")
def homepage():
    return "Hello World"


@app.route("/api")
def my_api():
    parent_span = flask_tracer.get_span()
    with opentracing.tracer.start_span('backend-service-api', child_of=parent_span) as span:
        answer = "something"
        span.set_tag("get-api", answer)
    return jsonify(repsonse=answer)


@app.route("/slowness")
def slowness():
    parent_span = flask_tracer.get_span()
    with opentracing.tracer.start_span('backend-service-slowness', child_of=parent_span) as span:
        answer = "something with latency"
        span.set_tag("get-slowness", answer)
        sleep(5)
    return jsonify(repsonse=answer)


@app.route("/star", methods=["POST"])
def add_star():
    parent_span = flask_tracer.get_span()
    with opentracing.tracer.start_span('backend-service-star', child_of=parent_span) as span:
        star = mongo.db.stars
        name = request.json["name"]
        distance = request.json["distance"]
        star_id = star.insert({"name": name, "distance": distance})
        new_star = star.find_one({"_id": star_id})
        output = {"name": new_star["name"], "distance": new_star["distance"]}
        span.set_tag("post-star", output)
    return jsonify({"result": output})


@app.route("/error")
def error():
    return ":(", 500


if __name__ == "__main__":
    app.run()