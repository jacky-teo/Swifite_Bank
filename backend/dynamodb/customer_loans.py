from urllib import response
import boto3
from flask import Flask, request, jsonify
from os import environ
from flask_cors import CORS  # enable CORS

app = Flask(__name__)

__TableName__ = 'swiftie-customer-loans'

# columns = ['customer-loan','customer_id','loan_id','customer_loan_amount']


client = boto3.client('dynamodb').list_tables()

dynamoDB = boto3.resource('dynamodb')

Table = dynamoDB.Table(__TableName__)

##Query all Loans
@app.route("/customer_loans")
def find_all():
    response = Table.scan()
    if len(response['Items']) > 0:
        return jsonify({
            "customer_loans": response['Items']}
            )
    return jsonify({"message": "customer loan not found."}), 404

#Query customer loan by customer id
@app.route("/customer_loans/<string:customer_id>")
def find_by_customer(customer_id):
    response = Table.scan(
        FilterExpression = boto3.dynamodb.conditions.Attr('customer_id').eq(customer_id)
    )
    if len(response['Items']) > 0:
        return jsonify({"customer_loans": response['Items']})
    return jsonify({"message": "customer loan not found."}), 404


## Query customer loand by loan id
@app.route("/customer_loans/loan/<string:loan_id>")
def find_by_loan_id(loan_id):
    response = Table.scan(
        FilterExpression = boto3.dynamodb.conditions.Attr('loan_id').eq(loan_id)
    )
    if len(response['Items']) > 0:
        return jsonify(
            {"customer_loans": response['Items']}
            )
    return jsonify({"message": "customer loan not found."}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5005, debug=True)