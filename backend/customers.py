from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS  # enable CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/swiftiebank'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
cors =CORS(app)

#   `customer_id` int(11) NOT NULL AUTO_INCREMENT,
#   `username` varchar(255) NOT NULL,
#   `password` varchar(255) NOT NULL,
#   `account_type` varchar(255) NOT NULL,
class Customer(db.Model):
    __tablename__ = 'customers'

    customer_id = db.Column(db.String(255), primary_key=True)
    username = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    account_type = db.Column(db.String(255), nullable=False)

    def __init__(self, customer_id, username, password, account_type):
        self.customer_id = customer_id
        self.username = username
        self.password = password
        self.account_type = account_type
    
    def json(self):
        return {"customer_id": self.customer_id, "username": self.username, "password": self.password, "account_type": self.account_type}

# get all customers
@app.route("/customer")
def get_all():
    return jsonify({"customers": [customer.json() for customer in Customer.query.all()]})

# get customer by username
@app.route("/customer/<string:username>")
def find_by_username(username):
    customer = Customer.query.filter_by(username=username).first()
    if customer:
        return jsonify(customer.json())
    return jsonify({"message": "Customer not found."}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)