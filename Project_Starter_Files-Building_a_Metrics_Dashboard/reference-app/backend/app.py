from time import sleep
from flask import Flask, request, jsonify
from flask_pymongo import PyMongo
from prometheus_flask_exporter import PrometheusMetrics
import opentracing
from jaeger_client import Config
from flask_opentracing import FlaskTracer


app = Flask(__name__)

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
        span.set_tag("api", answer)
        span.set_tag("status", 200)
    return jsonify(repsonse=answer)


@app.route("/latency")
def slowness():
    parent_span = flask_tracer.get_span()
    with opentracing.tracer.start_span('backend-service-latency-test', child_of=parent_span) as span:
        sleep_time = 10
        answer = "very slow"
        span.set_tag("latency-test", answer)
        span.set_tag("status", 200)
        span.set_tag("processing-time", sleep_time)
        sleep(sleep_time)
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