from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

db = {}
client_db = {}


# @app.after_request
# def add_headers(response):
#     response.headers.add('Content-Type', 'application/json')
#     response.headers.add('Access-Control-Allow-Origin', '*')
#     response.headers.add('Access-Control-Allow-Methods', 'PUT, GET, POST, DELETE, OPTIONS, PATCH')
#     response.headers.add('Access-Control-Allow-Headers', 'Origin, X-Requested-With, Content-Type, Accept, Authorization')
#     response.headers.add('Access-Control-Expose-Headers', 'Content-Type,Content-Length,Authorization,X-Pagination')
#     return response


def option_todo(id):
    return "", 204


app.add_url_rule(
    "/", view_func=option_todo, provide_automatic_options=False, methods=["OPTIONS"]
)
app.add_url_rule(
    r"/<path:path>",
    view_func=option_todo,
    provide_automatic_options=False,
    methods=["OPTIONS"],
)


@app.after_request
def after_request(response):
    response.headers["Access-Control-Allow-Methods"] = "*"
    response.headers["Access-Control-Allow-Origin"] = "*"
    response.headers["Vary"] = "Origin"
    return response


@app.route("/users", methods=["POST"])
def create_user():
    request_data = request.json
    print(f"Creating a new user with requst data: {request_data}")

    db[request_data["email"]] = request_data["password"]

    return jsonify({"token": "fake-token"})


@app.route("/clients", methods=["POST"])
def create_client():
    request_data = request.json
    print(f"Creating a new client with requst data: {request_data}")

    client_db[request_data["email"]] = request_data["password"]

    return jsonify({"token": "fake-token-for-client"})


@app.route("/users/signin", methods=["PUT"])
def signin_user():
    request_data = request.json
    print(f"Signing in user with request data: {request_data}")

    if (
        request_data["email"] in db
        and db[request_data["email"]] == request_data["password"]
    ):
        return jsonify({"token": "fake-token"})
    else:
        return jsonify({"error": "Invalid credentials"}), 401


@app.route("/devices")
@cross_origin(origin="*")
def get_devices():
    res = jsonify(
        {
            "devices": [
                {
                    "name": "CO2 Sensor",
                    "region": "US West",
                    "ipfs": "lkasdjf9325kadjsfkj",
                    "updated_at": "2020-01-01",
                },
                {
                    "name": "Air Quality Sensor",
                    "region": "US East",
                    "ipfs": "dsafadsf4tadsfads42",
                    "updated_at": "2020-04-19",
                },
                {
                    "name": "Temperature Sensor",
                    "region": "US Central",
                    "ipfs": "kadsjfki45889tioeqw",
                    "updated_at": "2020-05-09",
                },
            ]
        }
    )
    res.headers.add("Access-Control-Allow-Origin", "*")
    return res


@app.route("/policies")
@cross_origin(origin="*")
def get_policies():
    res = jsonify(
        {
            "policies": [
                {
                    "id": "0",
                    "name": "Temperature Sensor",
                    "authorized_devices": ["CO2 Sensor", "Air Quality Sensor"],
                },
                {
                    "id": "1",
                    "name": "Humidity Sensor",
                    "authorized_devices": ["Air Quality Sensor"],
                },
            ]
        }
    )
    res.headers.add("Access-Control-Allow-Origin", "*")
    return res


if __name__ == "__main__":
    app.run(debug=True)
