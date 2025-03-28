import requests

BASE_URL = "http://127.0.0.1:4001"  # Change this if running on a different server

def create_order(amount):
    """Calls the /create_order API to generate an order ID."""
    url = f"{BASE_URL}/create_order"
    data = {"amount": amount}
    response = requests.post(url, json=data)
    return response.json()

def capture_payment(payment_id, amount):
    """Calls the /capture_payment API to charge a user."""
    url = f"{BASE_URL}/capture_payment"
    data = {"payment_id": payment_id, "amount": amount}
    response = requests.post(url, json=data)
    return response.json()

def verify_payment(order_id, payment_id, signature):
    """Calls the /verify_payment API to ensure a transaction is valid."""
    url = f"{BASE_URL}/verify_payment"
    data = {
        "order_id": order_id,
        "payment_id": payment_id,
        "signature": signature
    }
    response = requests.post(url, json=data)
    return response.json()


print("Creating order...")
order = create_order(10)  # ₹500
print(order)

#Assuming we got a payment ID and signature after payment (Mock Data)
fake_payment_id = "pay_HQxp1234"
fake_signature = "sig_123abc"
order_id = order.get("id")

# Step 2: Capture Payment (Normally done after Razorpay redirects the user)
print("\nCapturing payment...")
payment_response = capture_payment(fake_payment_id, 500)
print(payment_response)

# Step 3: Verify Payment Signature (Optional Security Step)
print("\nVerifying payment signature...")
verification_response = verify_payment(order_id, fake_payment_id, fake_signature)
print(verification_response)

