from flask import Flask, request, jsonify
from flask_cors import cross_origin

app = Flask(__name__)

db = {}


@app.route("/users", methods=["POST"])
def create_user():
    request_data = request.json
    print(f"Creating a new user with requst data: {request_data}")

    db[request_data["email"]] = request_data["password"]

    return jsonify({"token": "fake-token"})


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
    return jsonify(
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


if __name__ == "__main__":
    app.run(debug=True)
