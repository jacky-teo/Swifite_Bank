import json
import boto3

def lambda_handler(event, context):
    __TableName__ = 'swiftie-wallet'
    # Create DynamoDB 
    client = boto3.client('dynamodb').list_tables()
    
    dynamoDB = boto3.resource('dynamodb', region_name='us-east-1')
    #Table Object
    Table = dynamoDB.Table(__TableName__)
    
    # TODO implement
    print(event)
    serviceType = event['queryStringParameters']['service']
    customer_id = None


    if serviceType == 'byCustomer':
        customer_id = event['queryStringParameters']['customerID']
        response = Table.scan(FilterExpression = boto3.dynamodb.conditions.Attr('customer_id').eq(customer_id))
        responseObject ={}
        if len(response['Items']) > 0:
            responseObject['statusCode'] = 200
            responseObject['headers'] = {}
            responseObject['headers']['Content-Type'] = 'application/json'
            responseObject['body'] = json.dumps(response['Items'])
            
            return responseObject
            
        return {
            'statusCode': 404,
            'body': json.dumps("Payment Information not found.")
            }
            
    elif serviceType == 'updateFunds':
        data = event['queryStringParameters']
        customer_id = event['queryStringParameters']['customerID']
        response = Table.scan(FilterExpression = boto3.dynamodb.conditions.Attr('customer_id').eq(customer_id))
        wallet_id = response['Items'][0]['wallet_id']
        wallet_balance = float(response['Items'][0]['wallet_balance'])
        wallet_balance += int(data['amount'])
        
        Table.update_item(
            Key={
                'wallet_id': wallet_id
            },
            UpdateExpression='SET wallet_balance = :val1',
            ExpressionAttributeValues={
                ':val1': str(wallet_balance)
            }
        )
        responseObject ={}
        responseObject['statusCode'] = 201
        responseObject['headers'] = {}
        responseObject['headers']['Content-Type'] = 'application/json'
        responseObject['body'] = json.dumps("Wallet Updated")
        return responseObject
