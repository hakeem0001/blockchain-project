from flask import Flask, render_template, request, redirect, session, url_for
from blockchain import Blockchain

# Create Flask app instance
app = Flask(__name__)
app.secret_key = 'super-secret-key'  # Needed for session management

# Create a blockchain instance to track blocks (orders/transactions)
blockchain = Blockchain()

# Home route: shows index.html (starting/home page)
@app.route('/')
def home():
    return render_template("index.html")

# Route to create a new order block
@app.route('/create', methods=['GET', 'POST'])
def create():
    if 'role' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        order = request.form['order']                      # Get order text from form
        blockchain.add_block(order)                        # Add new block to chain
        return redirect('/blocks')                         # Redirect to view updated blockchain
    return render_template("create_order.html")            # Show form to create new order

# Arabic login route
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "GET":
        return render_template("login.html")              # Show Arabic login page

    username = request.form.get("username")                # Get submitted username
    password = request.form.get("password")                # Get submitted password
    role = request.form.get("role")                        # Get selected role from dropdown

    # ✅ Dummy login validation — only checks that fields are filled
    if username and password and role:
        session['username'] = username
        session['role'] = role
        if role == "admin":
            return redirect(url_for('admin_dashboard'))
        elif role.startswith("supplier"):
            return redirect(url_for('supplier_dashboard'))
        elif role == "producer":
            return redirect(url_for('producer_dashboard'))
        elif role == "stock":
            return redirect(url_for('stock_dashboard'))
        else:
            return "دور غير معروف", 400                   # Unknown role error

    return "بيانات غير صحيحة", 401                          # Missing/invalid credentials

# Admin dashboard
@app.route('/admin')
def admin_dashboard():
    if session.get('role') != 'admin':
        return redirect(url_for('login'))
    return render_template("admin_dashboard.html")

# Supplier dashboard
@app.route('/supplier')
def supplier_dashboard():
    if not session.get('role', '').startswith('supplier'):
        return redirect(url_for('login'))
    return render_template("supplier_dashboard.html")

# Producer dashboard
@app.route('/producer')
def producer_dashboard():
    if session.get('role') != 'producer':
        return redirect(url_for('login'))
    return render_template("producer_dashboard.html")

# Stock dashboard
@app.route('/stock')
def stock_dashboard():
    if session.get('role') != 'stock':
        return redirect(url_for('login'))
    return render_template("stock_dashboard.html")

# Logout route
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# View the blockchain blocks
@app.route('/blocks')
def view_blocks():
    if 'role' not in session:
        return redirect(url_for('login'))
    chain = blockchain.get_chain()                          # Get full list of blocks
    return render_template("view_blocks.html", chain=chain) # Show in table/page

# Route to clear the blockchain
@app.route('/clear', methods=['POST'])
def clear_chain():
    if session.get('role') != 'producer':
        return redirect(url_for('login'))
    blockchain.chain = []
    blockchain.chain.append(blockchain.create_genesis_block())
    blockchain.save_chain()
    return redirect(url_for('view_blocks'))

# Invoice form route (create and view invoice)
@app.route('/invoice', methods=['GET', 'POST'])
def invoice():
    if 'role' not in session:
        return redirect(url_for('login'))
    if request.method == 'POST':
        parts = request.form['parts']                      # Get part name
        qty = request.form['qty']                          # Get quantity
        return render_template('invoice.html', message="تم تسجيل الطلب", parts=parts, qty=qty)
    return render_template('invoice.html', message=None)   # Show empty form first

# Educational route: Explain MRP + Blockchain to all users
@app.route('/mrp_guide')
def mrp_guide():
    if 'role' not in session:
        return redirect(url_for('login'))
    return render_template("mrp_guide.html")

# Start the app on all interfaces, port 5000, debug mode ON
if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)