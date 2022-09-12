from collections import defaultdict
from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

db = {}
client_db = {}
policies = defaultdict(list)
devices = []

test_policies = [
    {
        "id": "0",
        "name": "Temperature Sensor",
        "authorized_devices": ["CO2 Sensor", "Air Quality Sensor"],
        "authorized_users": ["ron@test.com", "banana@gmail.com"],
    },
    {
        "id": "1",
        "name": "Humidity Sensor",
        "authorized_devices": ["Air Quality Sensor"],
        "authorized_users": ["test@gmail.com"],
    },
]


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

    print(f"Client db: {client_db}")

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


@app.route("/devices", methods=["GET"])
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


@app.route("/devices", methods=["POST"])
def register_device():
    request_data = request.json
    print(f"Registering a new device with request data: {request_data}")

    devices.append(request_data)

    return jsonify()


@app.route("/policies", methods=["GET"])
@cross_origin(origin="*")
def get_policies():
    res = jsonify(
        {
            "policies": test_policies,
        }
    )
    res.headers.add("Access-Control-Allow-Origin", "*")
    return res


@app.route("/policies", methods=["POST"])
def create_policy():
    request_data = request.json
    print(f"Creating a new policy with request data: {request_data}")
    policies[request_data["device_id"]].append(request_data["accessing_device_id"])
    policies[request_data["device_id"]].append(request_data["accessing_user_id"])

    print(f"Policy db: {policies}")

    test_policies.append(
        {
            "id": "5",
            "name": "Test Addition",
            "authorized_devices": ["Test Sensor"],
            "authorized_users": ["test@test.com"],
        },
    )

    return jsonify()

@app.route("/ipfs-hash/<device_id>", methods=["PUT"])
def get_ipfs_hash(device_id):
    if device_id == "":
        return jsonify({"error": "No device id provided"}), 400

    print(f"Getting ipfs hash for device id: {device_id} with body {request.json}")

    return jsonify({"ipfsHash": "QmT5NvUtoM5nWFfrQdVrFtvGfKFmG7AHE8P34isapyhCxX"})


@app.route("/ipfs-hash", methods=["GET"])
def get_ipfs_hashs():
    return jsonify({"ipfsHash": "QmT5NvUtoM5nWFfrQdVrFtvGfKFmG7AHE8P34isapyhCxX"})


# Routes for IoT device
@app.route("/iot/ipfs-hash", methods=["PUT"])
def update_ipfs_hash():
    print(f"/iot/ipfs-hash called with body {request.json}")
    request_data = request.json
    if "device-id" not in request_data:
        return jsonify({"error": "No device id provided"}), 400

    if "ipfs-hash" not in request_data:
        return jsonify({"error": "No ipfs hash provided"}), 400

    if "device-key" not in request_data:
        return jsonify({"error": "No device key provided"}), 400

    return jsonify(), 200

@app.route("/iot/data-access", methods=["PUT"])
def data_access():
    print(f"/iot/data-access called with body {request.json}")
    request_data = request.json
    if "device-id" not in request_data:
        return jsonify({"error": "No device id provided"}), 400

    if "device-key" not in request_data:
        return jsonify({"error": "No device key provided"}), 400

    return jsonify({"ipfs-hash": "<IPFS HASH>"}), 200


if __name__ == "__main__":
    app.run(debug=True)
