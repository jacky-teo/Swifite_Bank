import json
import boto3

def lambda_handler(event, context):
    __TableName__ = 'swiftie-payment'
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
            
    elif serviceType == 'addPayment':
        data = event['queryStringParameters']
        response = Table.put_item(
        Item = {
            'customer_id': data['customerID'],
            'payment_id': data['payment_id'],
            'loan_id': data['loan_id'],
            'business_id': data['business_id'],
            'payment_amount': data['amount'],
            'payment_date': data['date']
        })
        responseObject ={}
        responseObject['statusCode'] = 201
        responseObject['headers'] = {}
        responseObject['headers']['Content-Type'] = 'application/json'
        responseObject['body'] = json.dumps("Payment added.")
        return responseObject
