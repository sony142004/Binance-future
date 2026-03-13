from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import os
from dotenv import load_dotenv
from bot.client import BinanceFuturesClient
from bot.orders import OrderManager
from bot.validators import (
    validate_symbol, validate_side, validate_order_type, 
    validate_quantity, validate_price
)

app = Flask(__name__)
CORS(app)
load_dotenv()

def get_client():
    api_key = os.getenv("BINANCE_API_KEY")
    api_secret = os.getenv("BINANCE_API_SECRET")
    if not api_key or not api_secret:
        return None
    return BinanceFuturesClient(api_key, api_secret)

@app.route('/')
def login():
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    return render_template('index.html')

@app.route('/api/order', methods=['POST'])
def place_order():
    data = request.json
    try:
        # Extract and Validate
        symbol = validate_symbol(data.get('symbol', ''))
        side = validate_side(data.get('side', ''))
        order_type = validate_order_type(data.get('type', ''))
        quantity = validate_quantity(data.get('quantity', ''))
        price = validate_price(data.get('price'), order_type)

        client = get_client()
        if not client:
            return jsonify({"error": "API Credentials not configured"}), 500
        
        order_manager = OrderManager(client)
        response = order_manager.place_order(symbol, side, order_type, quantity, price)
        
        return jsonify({
            "success": True,
            "orderId": response.get('orderId'),
            "status": response.get('status'),
            "executedQty": response.get('executedQty'),
            "avgPrice": response.get('avgPrice')
        })
    except Exception as e:
        return jsonify({"success": False, "error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True, port=5000)
