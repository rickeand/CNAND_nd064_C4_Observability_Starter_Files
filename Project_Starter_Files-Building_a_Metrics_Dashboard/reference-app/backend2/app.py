import logging

from jaeger_client import Config
from flask import Flask, request, jsonify
from flask_opentracing import FlaskTracing
from flask_pymongo import PyMongo

from prometheus_flask_exporter.multiprocess import GunicornInternalPrometheusMetrics

app = Flask(__name__)

app.config["MONGO_DBNAME"] = "example-mongodb"
app.config[
    "MONGO_URI"
] = "mongodb://example-mongodb-svc.default.svc.cluster.local:27017/example-mongodb"

mongo = PyMongo(app)

JAEGER_HOST = 'simplest-agent.observability.svc.cluster.local'
metrics = GunicornInternalPrometheusMetrics(app)
metrics.info('app_info', 'Backend Service', version='1.0')

def init_tracer(service):
    logging.getLogger('').handlers = []
    logging.basicConfig(format='%(message)s', level=logging.INFO)
    config = Config(
        config={
            'sampler': {
                'type': 'const',
                'param': 1,
            },
            'logging': True,
            'local_agent': {
                'reporting_host': JAEGER_HOST
            }
        },
        service_name=service,
    )
    return config.initialize_tracer()
tracer = init_tracer('backend')
tracing = FlaskTracing(tracer, True, app)

@app.route("/")
def homepage():
    return "Hello World"


@app.route("/api")
def my_api():
    answer = "something"
    return jsonify(repsonse=answer)


@app.route("/star", methods=["POST"])
def add_star():
    star = mongo.db.stars
    name = request.json["name"]
    distance = request.json["distance"]
    star_id = star.insert({"name": name, "distance": distance})
    new_star = star.find_one({"_id": star_id})
    output = {"name": new_star["name"], "distance": new_star["distance"]}
    return jsonify({"result": output})


if __name__ == "__main__":
    app.run()