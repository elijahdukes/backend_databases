import json
from flask import Flask, request
import db

DB = db.DatabaseDriver()

app = Flask(__name__)


@app.route("/")
def hello_world():
    return "Hello world!"


# your routes here
@app.route("/api/users/")
def get_users():
    """
    Gets all users
    """
    return json.dumps({"users":DB.get_all_users()}), 200

@app.route("/api/users/", methods = ["POST"])
def insert_user():
    """
    Creates a new user
    """
    body = json.loads(request.data)
    name = body.get("name")
    username = body.get("username")
    balance = body.get("balance", 0)
    if name is None:
        return json.dumps({"error": "Input name!"}), 400
    if username is None:
        return json.dumps({"error": "Input username!"}), 400

    user_id = DB.insert_user_table(name, username, balance)
    user = DB.get_user_by_id(user_id)
    if user is None:
        return json.dumps({"error": "something went wrong when creating the user"}), 400
    return json.dumps(user), 201

@app.route("/api/user/<int:user_id>/")
def get_user(user_id):
    """
    Gets a specific user by user id
    """
    user = DB.get_user_by_id(user_id)
    if user is None:
        return json.dumps({"error":"User not found."}), 404
    return json.dumps(user), 200

@app.route("/api/user/<int:user_id>/", methods = ["DELETE"])
def delete_user(user_id):
    """
    Deletes a specific user
    """
    user = DB.get_user_by_id(user_id)
    if user is None:
        return json.dumps({"error":"User not found."}), 404
    DB.delete_user_by_id(user_id)
    return json.dumps(user)

@app.route("/api/send/", methods=["POST"])
def send_money():
    """
    Sends money from one user to another
    """
    body = json.loads(request.data)
    sender_id = body.get("sender_id")
    receiver_id = body.get("receiver_id")
    amount = body.get("amount")
    if sender_id is None:
        return json.dumps({"error": "Input sender id!"}), 400
    if receiver_id is None:
        return json.dumps({"error": "Input receiver id!"}), 400
    if amount is None:
        return json.dumps({"error": "Input amount!"}), 400

    sender = DB.get_user_by_id(sender_id)
    receiver = DB.get_user_by_id(receiver_id)
    sender_balance = sender["balance"]
    receiver_balance = receiver["balance"]
    if amount > sender_balance:
        return json.dumps({"error":"Insufficient Funds!"}), 400

    new_sbalance = sender_balance - amount
    new_rbalance = receiver_balance +  amount

    DB.update_user_by_id(sender_id,new_sbalance)
    DB.update_user_by_id(receiver_id, new_rbalance)

    res = {
        "sender_id":sender_id,
        "receiver_id":receiver_id,
        "amount":amount
    }

    return json.dumps(res), 200




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000, debug=True)
