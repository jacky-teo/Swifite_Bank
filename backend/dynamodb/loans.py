from urllib import response
import boto3
from flask import Flask, request, jsonify
from os import environ
from flask_cors import CORS  # enable CORS

app = Flask(__name__)

__TableName__ = 'swiftie-loan'

# columns = ['loan','business','loan_amount','loan_duration','loan_interest']


client = boto3.client('dynamodb').list_tables()

dynamoDB = boto3.resource('dynamodb')

Table = dynamoDB.Table(__TableName__)

#Query by business id
@app.route("/loans/business/<string:business>")
def find_by_business(business):
    response = Table.scan(
        FilterExpression = boto3.dynamodb.conditions.Attr('business').eq(business)
    )
    if len(response['Items']) > 0:
        return jsonify(response['Items'])
    return jsonify({"message": "Loan not found."}), 404

##Query all Loans
@app.route("/loans")
def find_all():
    response = Table.scan()
    if len(response['Items']) > 0:
        return jsonify(response['Items'])
    return jsonify({"message": "Loan not found."}), 404


##Query Loan by loan id
@app.route("/loans/<string:loan_id>")
def find_by_loan_id(loan_id):
    response = Table.scan(
        FilterExpression = boto3.dynamodb.conditions.Attr('loan').eq(loan_id)
    )
    if len(response['Items']) > 0:
        return jsonify(response['Items'])
    return jsonify({"message": "Loan not found."}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002, debug=True)