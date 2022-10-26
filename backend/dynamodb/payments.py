from urllib import response
import boto3
from flask import Flask, request, jsonify
from os import environ
from flask_cors import CORS  # enable CORS

app = Flask(__name__)

__TableName__ = 'swiftie-payment'

# columns = ['payment','business_id','customer_id','loan_id','payment_amount','payment_date']


client = boto3.client('dynamodb').list_tables()

dynamoDB = boto3.resource('dynamodb')

Table = dynamoDB.Table(__TableName__)

#Query all payments
@app.route("/payments")
def find_all():
    response = Table.scan()
    if len(response['Items']) > 0:
        return jsonify({"payments":response['Items']})
    return jsonify({"message": "Payment not found."}), 404

#Query Payment by customer_id
@app.route("/payments/customer/<string:customer_id>")
def find_by_customer(customer_id):
    response = Table.scan(
        FilterExpression = boto3.dynamodb.conditions.Attr('customer_id').eq(customer_id)
    )
    if len(response['Items']) > 0:
        return jsonify(response['Items'])
    return jsonify({"message": "Payment not found."}), 404

## Add Payments
@app.route("/payments", methods=['POST'])
def add_payment():
    data = request.get_json()
    response = Table.put_item(
        Item = {
            'customer_id': data['customer_id'],
            'payment_id': data['payment_id'],
            'loan_id': data['loan_id'],
            'amount': data['amount'],
            'date': data['date']
        }
    )
    return jsonify({"message": "Payment added successfully."}), 200
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5003, debug=True)