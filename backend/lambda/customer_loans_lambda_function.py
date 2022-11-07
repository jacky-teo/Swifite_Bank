import json
import boto3

def lambda_handler(event, context):
    __TableName__ = 'swiftie-customer-loans'
    # Create DynamoDB 
    client = boto3.client('dynamodb').list_tables()
    
    dynamoDB = boto3.resource('dynamodb', region_name='us-east-1')
    #Table Object
    Table = dynamoDB.Table(__TableName__)
    
    # TODO implement
    print(event)
    serviceType = event['queryStringParameters']['service']
    customer_id = None
    loan_id = None


    if serviceType == 'byCustomer':
        customer_id = event['queryStringParameters']['customerID']
        response = Table.scan(FilterExpression = boto3.dynamodb.conditions.Attr('customer_id').eq(customer_id))
        responseObject ={}
        if len(response['Items']) > 0:
            responseObject['statusCode'] = 200
            responseObject['headers'] = {}
            responseObject['headers']['Content-Type'] = 'application/json'
            responseObject['body'] = json.dumps({"customer_loans":response['Items']})
            
            return responseObject
            
        return {
            'statusCode': 404,
            'body': json.dumps("Customer Loans not found.")
            }
            
    elif serviceType == 'byLoan':
        loan_id = event['queryStringParameters']['loanID']
        response = Table.scan(FilterExpression = boto3.dynamodb.conditions.Attr('loan_id').eq(loan_id))
        responseObject ={}
        if len(response['Items']) > 0:
            responseObject['statusCode'] = 200
            responseObject['headers'] = {}
            responseObject['headers']['Content-Type'] = 'application/json'
            responseObject['body'] = json.dumps({"customer_loans": response['Items']})
            return responseObject
        return {
                'statusCode': 404,
                'body': json.dumps("Customer Loans not found.")
            }
