from flask import Blueprint, jsonify, request

api = Blueprint("accounts", __name__)

# In-memory storage for the starter project. Data resets when the app restarts.
_accounts = {}
_next_id = 1


@api.get("/health")
def health():
    return jsonify({"status": "ok"}), 200


@api.post("/accounts")
def create_account():
    global _next_id
    data = request.get_json(silent=True) or {}
    if not data.get("name"):
        return jsonify({"error": "name is required"}), 400

    account = {
        "id": _next_id,
        "name": data["name"],
        "email": data.get("email", ""),
    }
    _accounts[_next_id] = account
    _next_id += 1
    return jsonify(account), 201


@api.get("/accounts")
def list_accounts():
    return jsonify(list(_accounts.values())), 200


@api.get("/accounts/<int:account_id>")
def read_account(account_id):
    account = _accounts.get(account_id)
    if account is None:
        return jsonify({"error": "account not found"}), 404
    return jsonify(account), 200


@api.patch("/accounts/<int:account_id>")
def update_account(account_id):
    account = _accounts.get(account_id)
    if account is None:
        return jsonify({"error": "account not found"}), 404

    data = request.get_json(silent=True) or {}
    if "name" in data:
        account["name"] = data["name"]
    if "email" in data:
        account["email"] = data["email"]
    return jsonify(account), 200


@api.delete("/accounts/<int:account_id>")
def delete_account(account_id):
    if account_id not in _accounts:
        return jsonify({"error": "account not found"}), 404
    del _accounts[account_id]
    return "", 204
