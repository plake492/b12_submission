import hmac
import hashlib
import os
from flask import Flask, request, jsonify
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
SIGNING_SECRET = os.getenv("SIGNING_SECRET", "").encode("utf-8")


@app.get("/")
def get_root():
    return jsonify({"message": "success"}), 200


@app.post("/echo")
def post_echo():
    raw_body = request.get_data()

    incoming_sig = request.headers.get("X-Signature-256", "")
    expected_sig = "sha256=" + hmac.new(
        key=SIGNING_SECRET,
        msg=raw_body,
        digestmod=hashlib.sha256,
    ).hexdigest()
    sig_valid = hmac.compare_digest(incoming_sig, expected_sig)

    body = request.get_json(silent=True) or {}
    headers = dict(request.headers)
    return jsonify({
        "message": "received",
        "status": "ok",
        "signature_valid": sig_valid,
        "body": body,
        "headers": headers,
    }), 200 if sig_valid else 401


if __name__ == "__main__":
    app.run(debug=True, port=5000)
