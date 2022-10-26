from urllib import response
import boto3
from flask import Flask, request, jsonify
from os import environ
from flask_cors import CORS  # enable CORS

app = Flask(__name__)

__TableName__ = 'swiftie-wallet'

# columns = ['wallet','customer_id','wallet_balance']


client = boto3.client('dynamodb').list_tables()

dynamoDB = boto3.resource('dynamodb')

Table = dynamoDB.Table(__TableName__)

#Query by customer id
@app.route("/wallet/customer/<string:customer_id>")
def find_by_customer(customer_id):
    response = Table.scan(
        FilterExpression = boto3.dynamodb.conditions.Attr('customer_id').eq(customer_id)
    )
    if len(response['Items']) > 0:
        return jsonify(response['Items'])
    return jsonify({"message": "customer not found."}), 404

#Query All wallet
@app.route("/wallets")
def find_all():
    response = Table.scan()
    if len(response['Items']) > 0:
        return jsonify({"wallets": response['Items']})
    return jsonify({"message": "customer not found."}), 404 

## Query wallet by customer id
@app.route("/wallets/<string:customer_id>")
def find_by_wallet(customer_id):
    response = Table.scan(
        FilterExpression = boto3.dynamodb.conditions.Attr('customer_id').eq(customer_id)
    )
    if len(response['Items']) > 0:
        return jsonify(response['Items'][0])
    return jsonify({"message": "customer not found."}), 404

## Update funds to wallet
@app.route("/wallets/transaction/<string:customer_id>", methods=['PUT'])
def update_wallet(customer_id):
    data = request.get_json()
    if data['add']:
        response = Table.scan(
        FilterExpression = boto3.dynamodb.conditions.Attr('customer_id').eq(customer_id)
        )
        wallet = response['Items'][0]['wallet']
        wallet_balance = float(response['Items'][0]['wallet_balance'])
        wallet_balance += data['amount']
        Table.update_item(
            Key={
                'wallet': wallet
            },
            UpdateExpression='SET wallet_balance = :val1',
            ExpressionAttributeValues={
                ':val1': str(wallet_balance)
            }
        )
        return jsonify({
            "message": "wallet updated.",
            "wallet_balance": str(wallet_balance)
        }), 200
    else:
        response = Table.scan(
        FilterExpression = boto3.dynamodb.conditions.Attr('customer_id').eq(customer_id)
        )
        wallet_balance = float(response['Items'][0]['wallet_balance'])
        wallet = response['Items'][0]['wallet']
        wallet_balance -= data['amount']
        Table.update_item(
            Key={
                'wallet': wallet
            },
            UpdateExpression='SET wallet_balance = :val1',
            ExpressionAttributeValues={
                ':val1': str(wallet_balance)
            }
        )
        return jsonify({
            "message": "wallet updated.",
            "wallet_balance": str(wallet_balance)
        }), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004, debug=True)