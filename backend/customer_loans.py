from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from os import environ
from flask_cors import CORS  # enable CORS

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root@localhost:3306/swiftiebank'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
cors =CORS(app)

#   `loan_id` int(11) NOT NULL AUTO_INCREMENT,
#   `customer_id` int(11) NOT NULL,

class CustomerLoans(db.Model):
    __tablename__ = 'customer_loans'

    loan_id = db.Column(db.String(255), primary_key=True)
    customer_id = db.Column(db.String(255), nullable=False)
    customer_loans = db.Column(db.String(255), nullable=False)

    def __init__(self, loan_id, customer_id, loan_amount):
        self.loan_id = loan_id
        self.customer_id = customer_id
        self.loan_amount = loan_amount

    def json(self):
        return {"loan_id": self.loan_id, "customer_id": self.customer_id, "customer_loans": self.customer_loans}
    
# get all customer loans
@app.route("/customer_loans")
def get_all():
    return jsonify({"customer_loans": [customer_loan.json() for customer_loan in CustomerLoans.query.all()]})

# get customer loan by customer_id
@app.route("/customer_loans/<int:customer_id>")
def find_by_customer_id(customer_id):
    customer_loan = CustomerLoans.query.filter_by(customer_id=customer_id)
    if customer_loan:
        return jsonify({"customer_loans": [customer_loan.json() for customer_loan in customer_loan]})
    return jsonify({"message": "Customer loan not found."}), 404

# get customer loan by loan_id
@app.route("/customer_loans/<int:loan_id>")
def find_by_loan_id(loan_id):
    customer_loan = CustomerLoans.query.filter_by(loan_id=loan_id)
    if customer_loan:
        return jsonify({"customer_loans": [customer_loan.json() for customer_loan in customer_loan]})
    return jsonify({"message": "Customer loan not found."}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)