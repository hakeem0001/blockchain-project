from flask import Flask, render_template, request, redirect
from blockchain import Blockchain

app = Flask(__name__)
blockchain = Blockchain()

@app.route('/')
def home():
    return render_template("index.html")

@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        order = request.form['order']
        blockchain.add_block(order)
        return redirect('/blocks')
    return render_template("create_order.html")

@app.route('/blocks')
def view_blocks():
    chain = blockchain.get_chain()
    return render_template("view_blocks.html", chain=chain)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
    
@app.route('/invoice', methods=['GET', 'POST'])
def invoice():
    if request.method == 'POST':
        # Just mock the display for now
        parts = request.form['parts']
        qty = request.form['qty']
        return render_template('invoice.html', message="تم تسجيل الطلب", parts=parts, qty=qty)
    return render_template('invoice.html', message=None)