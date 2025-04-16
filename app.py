from flask import Flask, render_template, request, redirect
import sqlite3
from datetime import datetime

app = Flask(__name__)

def init_db():
    conn = sqlite3.connect('orders.db')
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS orders (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        date TEXT,
        customer_name TEXT,
        phone TEXT,
        product_name TEXT,
        size TEXT,
        area TEXT,
        price REAL,
        notes TEXT
    )''')
    conn.commit()
    conn.close()

@app.route('/')
def index():
    conn = sqlite3.connect('orders.db')
    c = conn.cursor()
    c.execute("SELECT * FROM orders ORDER BY id DESC")
    orders = c.fetchall()
    conn.close()
    return render_template('index.html', orders=orders)

@app.route('/add', methods=['POST'])
def add():
    date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    customer_name = request.form['customer_name']
    phone = request.form['phone']
    product_name = request.form['product_name']
    size = request.form['size']
    area = request.form['area']
    price = request.form['price']
    notes = request.form.get('notes', '')

    conn = sqlite3.connect('orders.db')
    c = conn.cursor()
    c.execute("INSERT INTO orders (date, customer_name, phone, product_name, size, area, price, notes) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
              (date, customer_name, phone, product_name, size, area, price, notes))
    conn.commit()
    conn.close()
    return redirect('/')

if __name__ == '__main__':
    init_db()
    app.run(debug=True)
