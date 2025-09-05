from flask import Flask, render_template, request, redirect, url_for
import os

app = Flask(__name__)

# Editable shop name (can set in Render env var SHOP_NAME)
SHOP_NAME = os.environ.get("SHOP_NAME", "MACS Coffee Shop")

menu = {
    "Espresso": 80,
    "Americano": 90,
    "Cappuccino": 100,
    "Latte": 110,
    "Mocha": 120,
    "Ube Cheese Pandesal": 130,
    "Pande Asado": 199,
    "Cheese Roll": 199,
    "Choco Banana Cupcakes": 150,
    "Classic Cheesy Ensaymada": 199,
    "Cinnamon Roll": 249,
}

orders = []

@app.route("/", methods=["GET"])
def home():
    return render_template("menu.html", menu=menu, shop_name=SHOP_NAME)

@app.route("/order", methods=["POST"])
def order():
    item = request.form.get("item")
    try:
        qty = int(request.form.get("quantity", 1))
    except Exception:
        qty = 1
    if item in menu and qty > 0:
        subtotal = menu[item] * qty
        orders.append({"item": item, "qty": qty, "subtotal": subtotal})
    return redirect(url_for("receipt"))

@app.route("/receipt", methods=["GET"])
def receipt():
    total = sum(order["subtotal"] for order in orders)
    return render_template("receipt.html", orders=orders, total=total, shop_name=SHOP_NAME)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
