import json
import boto3

def lambda_handler(event, context):
    __TableName__ = 'swiftie-customer'
    # Create DynamoDB 
    client = boto3.client('dynamodb').list_tables()
    
    dynamoDB = boto3.resource('dynamodb', region_name='us-east-1')
    #Table Object
    Table = dynamoDB.Table(__TableName__)
    
    # TODO implement
    print(event)
    serviceType = event['queryStringParameters']['service']
    accountType = None
    username = None


    if serviceType == 'account_type':
        accountType = event['queryStringParameters']['account_type']
        response = Table.scan(FilterExpression = boto3.dynamodb.conditions.Attr('account_type').eq(accountType))
        responseObject ={}
        if len(response['Items']) > 0:
            responseObject['statusCode'] = 200
            responseObject['headers'] = {}
            responseObject['headers']['Content-Type'] = 'application/json'
            responseObject['body'] = json.dumps({"customers":response['Items']})
            
            return responseObject
            
        return {
            'statusCode': 404,
            'body': json.dumps("Customer not found.")
            }
            
    elif serviceType == 'login':
        username = event['queryStringParameters']['username']
        response = Table.scan(FilterExpression = boto3.dynamodb.conditions.Attr('username').eq(username))
        responseObject ={}
        if len(response['Items']) > 0:
            responseObject['statusCode'] = 200
            responseObject['headers'] = {}
            responseObject['headers']['Content-Type'] = 'application/json'
            responseObject['body'] = json.dumps(json.dumps(response['Items'][0]))
            return responseObject
        return {
                'statusCode': 404,
                'body': json.dumps("Customer not found.")
            }

