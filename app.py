from flask import Flask, request, jsonify

app = Flask(__name__)

db = {}

@app.route('/users', methods=['POST'])
def create_user():
    request_data = request.json
    print(f"Creating a new user with requst data: {request_data}")

    db[request_data["email"]] = request_data["password"]

    return jsonify({"token": "fake-token"})

@app.route('/users/signin', methods=['PUT'])
def signin_user():
    request_data = request.json
    print(f"Signing in user with request data: {request_data}")

    if request_data["email"] in db and db[request_data["email"]] == request_data["password"]:
        return jsonify({"token": "fake-token"})
    else:
        return jsonify({"error": "Invalid credentials"}), 401

if __name__ == "__main__":
    app.run(debug=True)
