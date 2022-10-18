from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS  # enable CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/swiftiebank'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
cors =CORS(app)


#   `payment_id` int(11) NOT NULL AUTO_INCREMENT,
#   `business_id` int(11) NOT NULL,
#   `customer_id` int(11) NOT NULL,
#   `loan_id` int(11) NOT NULL,
#   `payment_amount` int(11) NOT NULL,
#   `payment_date` date NOT NULL,

class Payments(db.Model):
    __tablename__ = 'payments'

    payment_id = db.Column(db.Integer, primary_key=True)
    business_id = db.Column(db.Integer, nullable=False)
    customer_id = db.Column(db.Integer, nullable=False)
    loan_id = db.Column(db.Integer, nullable=False)
    payment_amount = db.Column(db.Float(precision=2), nullable=False)
    payment_date = db.Column(db.Date, nullable=False)

    def __init__(self, payment_id, business_id, customer_id, loan_id, payment_amount, payment_date):
        self.payment_id = payment_id
        self.business_id = business_id
        self.customer_id = customer_id
        self.loan_id = loan_id
        self.payment_amount = payment_amount
        self.payment_date = payment_date

    def json(self):
        return {"payment_id": self.payment_id, "business_id": self.business_id, "customer_id": self.customer_id, "loan_id": self.loan_id, "payment_amount": self.payment_amount, "payment_date": self.payment_date}

# get all payments
@app.route("/payments")
def get_all():
    return jsonify({"payments": [payment.json() for payment in Payments.query.all()]})

# get payment by payment_id
@app.route("/payments/<int:payment_id>")
def find_by_payment_id(payment_id):
    payment = Payments.query.filter_by(payment_id=payment_id)
    if payment:
        return jsonify({"payments": [payment.json() for payment in payment]})
    return jsonify({"message": "Payment not found."}), 404

# get payment by customer_id
@app.route("/payments/customer/<int:customer_id>")
def find_by_customer_id(customer_id):
    payment = Payments.query.filter_by(customer_id=customer_id)
    if payment:
        return jsonify([payment.json() for payment in payment])
    return jsonify({"message": "Payment not found."}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)