from flask import Flask, request, jsonify

# Flask webhook receiver — listens for incoming Plaid webhook events
app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    # Parse the JSON payload and extract key fields
    data = request.get_json()
    webhook_type = data["webhook_type"]
    item_id = data["item_id"]
    print(f"Webhook type: {webhook_type} / Item ID: {item_id}")
    return jsonify({"status": "ok"}), 200


if __name__ == '__main__':
    app.run(debug=True)