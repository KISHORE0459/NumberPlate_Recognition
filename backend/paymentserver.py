import razorpay
from flask import Flask, request, jsonify

app = Flask(__name__)

# Razorpay API Keys (Replace with your actual keys)
RAZORPAY_KEY_ID = "rzp_test_GL7rIL2x0NYu1z"
RAZORPAY_KEY_SECRET = "3fHjboaIwgTaGP8qGQAMMFfU"

# Initialize Razorpay client
client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))


@app.route('/create_order', methods=['POST'])
def create_order():
    data = request.json  # Get request data
    amount = data.get("amount")  # Amount in INR
    currency = "INR"

    order_data = {
        "amount": amount * 100,  # Convert to paise
        "currency": currency,
        "receipt": "order_rcptid_11",
        "payment_capture": 1  # Auto-capture payment
    }

    order = client.order.create(data=order_data)
    
    return jsonify(order)  # Return the order details to the frontend


@app.route('/capture_payment', methods=['POST'])
def capture_payment():
    data = request.json  # Get request data
    payment_id = data.get("payment_id")
    amount = data.get("amount") * 100  # Convert to paise

    try:
        captured_payment = client.payment.capture(payment_id, amount)
        return jsonify({"message": "Payment Captured Successfully", "data": captured_payment})
    except Exception as e:
        return jsonify({"error": str(e)})


@app.route('/verify_payment', methods=['POST'])
def verify_payment():
    data = request.json
    order_id = data.get("order_id")
    payment_id = data.get("payment_id")
    signature = data.get("signature")

    try:
        client.utility.verify_payment_signature({
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        })
        return jsonify({"message": "Payment Verified Successfully"})
    except razorpay.errors.SignatureVerificationError:
        return jsonify({"error": "Payment Verification Failed"}), 400
    
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=4001, debug=True)