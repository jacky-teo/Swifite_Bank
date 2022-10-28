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
#   `business_id` int(11) NOT NULL,
#   `loan_amount` int(11) NOT NULL,
#   `loan_duration` int(11) NOT NULL,
#   `loan_start_date` date NOT NULL,
#   `loan_interest` int(11) NOT NULL,
class Loans(db.Model):
    __tablename__ = 'loans'
    loan_id = db.Column(db.String(255), primary_key=True)
    business_id = db.Column(db.String(255), nullable=False)
    loan_amount = db.Column(db.String(255), nullable=False)
    loan_duration = db.Column(db.String(255), nullable=False)
    loan_start_date = db.Column(db.String(255), nullable=False)
    loan_interest = db.Column(db.String(255), nullable=False)

    def __init__(self, loan_id, business_id, loan_amount, loan_duration, loan_start_date, loan_interest):
        self.loan_id = loan_id
        self.business_id = business_id
        self.loan_amount = loan_amount
        self.loan_duration = loan_duration
        self.loan_start_date = loan_start_date
        self.loan_interest = loan_interest
    
    def json(self):
        return {"loan_id": self.loan_id, "business_id": self.business_id, "loan_amount": self.loan_amount, "loan_duration": self.loan_duration, "loan_start_date": self.loan_start_date, "loan_interest": self.loan_interest}

# get all loans
@app.route("/loans")
def get_all():
    return jsonify([loan.json() for loan in Loans.query.all()])

# get loan by business_id
@app.route("/loans/business/<int:business_id>")
def find_by_business_id(business_id):
    loan = Loans.query.filter_by(business_id=business_id).first()
    if loan:
        return jsonify(loan.json())
    return jsonify({"message": "Loan not found."}), 404

# get loan by loan_id
@app.route("/loans/<int:loan_id>")
def find_by_loan_id(loan_id):
    loan = Loans.query.filter_by(loan_id=loan_id).first()
    if loan:
        return jsonify(loan.json())
    return jsonify({"message": "Loan not found."}), 404


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)

