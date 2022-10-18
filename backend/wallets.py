from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS  # enable CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/swiftiebank'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
cors =CORS(app)
#   `wallet_id` int(11) NOT NULL AUTO_INCREMENT,
#   `customer_id` int(11) NOT NULL,
#   `wallet_balance` int(11) NOT NULL,
class Wallets(db.Model):
    __tablename__ = 'wallets'

    wallet_id = db.Column(db.Integer, primary_key=True)
    customer_id = db.Column(db.Integer, nullable=False)
    wallet_balance = db.Column(db.float(precision=2), nullable=False)

    def __init__(self, wallet_id, customer_id, wallet_balance):
        self.wallet_id = wallet_id
        self.customer_id = customer_id
        self.wallet_balance = wallet_balance
    
    def json(self):
        return {"wallet_id": self.wallet_id, "customer_id": self.customer_id, "wallet_balance": self.wallet_balance}

# get all wallets
@app.route("/wallets")
def get_all():
    return jsonify({"wallets": [wallet.json() for wallet in Wallets.query.all()]})

# get wallet by customer_id
@app.route("/wallets/<int:customer_id>")
def find_by_customer_id(customer_id):
    wallet = Wallets.query.filter_by(customer_id=customer_id)
    if wallet:
        return jsonify({"wallets": [wallet.json() for wallet in wallet]})
    return jsonify({"message": "Wallet not found."}), 404

# update funds to wallet
@app.route("/wallets/<int:customer_id>", methods=['PUT'])
def update_funds(customer_id):
    wallet = Wallets.query.filter_by(customer_id=customer_id)
    if wallet:
        data = request.get_json()
        if data['add']:
            wallet.wallet_balance += data['amount']
        else:
            wallet.wallet_balance -= data['amount']
        try:
            db.session.commit()
        except:
            return jsonify({"message": "An error occurred updating the wallet."}), 500
        return jsonify(wallet.json())
    return jsonify({"message": "Wallet not found."}), 404

    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=True)