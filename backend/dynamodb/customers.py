from urllib import response
import boto3
from flask import Flask, request, jsonify
from os import environ
from flask_cors import CORS  # enable CORS

app = Flask(__name__)

__TableName__ = 'swiftie-customer'
# Primary_Column_Name = 'account_type-index'
# Primary_Key = 'business'
# columns = ['customer','account_type','password','username']


client = boto3.client('dynamodb').list_tables()

dynamoDB = boto3.resource('dynamodb', region_name='us-east-1')

Table = dynamoDB.Table(__TableName__)

#Query by account type
@app.route("/customers/<string:account_type>")
def find_by_account_type(account_type):
    response = Table.scan(
        FilterExpression = boto3.dynamodb.conditions.Attr('account_type').eq(account_type)
    )
    if len(response['Items']) > 0:
        return jsonify({"customers":response['Items'] })
    return jsonify({"message": "Customer not found."}), 404

##Query by username
@app.route("/customer/<string:username>")
def find_by_username(username):
    response = Table.scan(
        FilterExpression = boto3.dynamodb.conditions.Attr('username').eq(username)
    )
    if len(response['Items']) > 0:
        return jsonify(response['Items'][0])
    return jsonify({"message": "Customer not found."}), 404

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)