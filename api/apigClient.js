/*
 * Copyright 2010-2016 Amazon.com, Inc. or its affiliates. All Rights Reserved.
 *
 * Licensed under the Apache License, Version 2.0 (the "License").
 * You may not use this file except in compliance with the License.
 * A copy of the License is located at
 *
 *  http://aws.amazon.com/apache2.0
 *
 * or in the "license" file accompanying this file. This file is distributed
 * on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either
 * express or implied. See the License for the specific language governing
 * permissions and limitations under the License.
 */

//global client variables
var apigClientFactory = {};
var cognitoLoginUrl = 'https://swiftie-app.auth.us-east-1.amazoncognito.com/login?client_id=3ek88ssut1aagrqe2o6980k930&response_type=token&scope=aws.cognito.signin.user.admin+email+openid+phone+profile&redirect_uri=http://localhost/Swifite_Bank/login.html';
var authToken;

//initiate login and redirect user to cognito login page
function toLogin() {
    window.location.href = cognitoLoginUrl;
}

//if token in redirect url after login, set session storage
if (window.location.href.includes('login.html')) {
    const urlParams = new URLSearchParams(window.location.href);
    const token = urlParams.get('access_token');
    sessionStorage.setItem('clientAuthToken', token);

    //if token not available, redirect to login
    if (token !== undefined && token !== '' && token !== null) {
        authToken = token;
    } else {
        toLogin();
    }

//if page is not login page, check if token is available in session storage
} else {
    authToken = sessionStorage.getItem("clientAuthToken");

    //if stored token value not valid, redirect to login
    if (authToken === undefined || authToken === '' || authToken === null || authToken === "null") {
        toLogin();
    }
}

apigClientFactory.newClient = function (config) {
    
    var apigClient = { };

    //check if client auth token is set
    if (!authToken) {
        toLogin();
    } else {
        if(config === undefined) {
            config = {
                accessKey: '',
                secretKey: '',
                sessionToken: '',
                region: 'us-east-1',
                apiKey: undefined,
                defaultContentType: 'application/json',
                defaultAcceptType: 'application/json'
            };
        }
        if(config.accessKey === undefined) {
            config.accessKey = '';
        }
        if(config.secretKey === undefined) {
            config.secretKey = '';
        }
        if(config.apiKey === undefined) {
            config.apiKey = '';
        }
        if(config.sessionToken === undefined) {
            config.sessionToken = '';
        }
        //If defaultContentType is not defined then default to application/json
        if(config.defaultContentType === undefined) {
            config.defaultContentType = 'application/json';
        }
        //If defaultAcceptType is not defined then default to application/json
        if(config.defaultAcceptType === undefined) {
            config.defaultAcceptType = 'application/json';
        }

        
        // extract endpoint and path from url
        var invokeUrl = 'https://k8dxd81114.execute-api.us-east-1.amazonaws.com/customer';
        var endpoint = /(^https?:\/\/[^\/]+)/g.exec(invokeUrl)[1];
        var pathComponent = invokeUrl.substring(endpoint.length);

        var sigV4ClientConfig = {
            accessKey: config.accessKey,
            secretKey: config.secretKey,
            sessionToken: config.sessionToken,
            serviceName: 'execute-api',
            region: config.region,
            endpoint: endpoint,
            defaultContentType: config.defaultContentType,
            defaultAcceptType: config.defaultAcceptType
        };

        var authType = 'NONE';
        if (sigV4ClientConfig.accessKey !== undefined && sigV4ClientConfig.accessKey !== '' && sigV4ClientConfig.secretKey !== undefined && sigV4ClientConfig.secretKey !== '') {
            authType = 'AWS_IAM';
        }

        var simpleHttpClientConfig = {
            endpoint: endpoint,
            defaultContentType: config.defaultContentType,
            defaultAcceptType: config.defaultAcceptType
        };

        var apiGatewayClient = apiGateway.core.apiGatewayClientFactory.newClient(simpleHttpClientConfig, sigV4ClientConfig);
        
        
        
        apigClient.rootGet = function (params, body, additionalParams) {
            if(additionalParams === undefined) { additionalParams = {}; }
            
            apiGateway.core.utils.assertParametersDefined(params, [], ['body']);
            
            var rootGetRequest = {
                verb: 'get'.toUpperCase(),
                path: pathComponent + uritemplate('/').expand(apiGateway.core.utils.parseParametersToObject(params, [])),
                headers: apiGateway.core.utils.parseParametersToObject(params, []),
                queryParams: apiGateway.core.utils.parseParametersToObject(params, []),
                body: body
            };
            
            
            return apiGatewayClient.makeRequest(rootGetRequest, authType, additionalParams, config.apiKey);
        };
        
        
        apigClient.customerGet = function (params, body, additionalParams) {
            if(additionalParams === undefined) { additionalParams = {}; }
            
            apiGateway.core.utils.assertParametersDefined(params, [], ['body']);
            
            var customerGetRequest = {
                verb: 'get'.toUpperCase(),
                path: pathComponent + uritemplate('/customer').expand(apiGateway.core.utils.parseParametersToObject(params, [])),
                headers: apiGateway.core.utils.parseParametersToObject(params, []),
                queryParams: apiGateway.core.utils.parseParametersToObject(params, []),
                body: body
            };
            
            
            return apiGatewayClient.makeRequest(customerGetRequest, authType, additionalParams, config.apiKey);
        };
        
        
        apigClient.customerOptions = function (params, body, additionalParams) {
            if(additionalParams === undefined) { additionalParams = {}; }
            
            apiGateway.core.utils.assertParametersDefined(params, [], ['body']);
            
            var customerOptionsRequest = {
                verb: 'options'.toUpperCase(),
                path: pathComponent + uritemplate('/customer').expand(apiGateway.core.utils.parseParametersToObject(params, [])),
                headers: apiGateway.core.utils.parseParametersToObject(params, []),
                queryParams: apiGateway.core.utils.parseParametersToObject(params, []),
                body: body
            };
            
            return apiGatewayClient.makeRequest(customerOptionsRequest, authType, additionalParams, config.apiKey);
        };
        
        
        apigClient.customerLoansGet = function (params, body, additionalParams) {
            if(additionalParams === undefined) { additionalParams = {}; }
            
            apiGateway.core.utils.assertParametersDefined(params, [], ['body']);
            
            var customerLoansGetRequest = {
                verb: 'get'.toUpperCase(),
                path: pathComponent + uritemplate('/customer-loans').expand(apiGateway.core.utils.parseParametersToObject(params, [])),
                headers: apiGateway.core.utils.parseParametersToObject(params, []),
                queryParams: apiGateway.core.utils.parseParametersToObject(params, []),
                body: body
            };
            
            
            return apiGatewayClient.makeRequest(customerLoansGetRequest, authType, additionalParams, config.apiKey);
        };
        
        
        apigClient.loansGet = function (params, body, additionalParams) {
            if(additionalParams === undefined) { additionalParams = {}; }
            
            apiGateway.core.utils.assertParametersDefined(params, [], ['body']);
            
            var loansGetRequest = {
                verb: 'get'.toUpperCase(),
                path: pathComponent + uritemplate('/loans').expand(apiGateway.core.utils.parseParametersToObject(params, [])),
                headers: apiGateway.core.utils.parseParametersToObject(params, []),
                queryParams: apiGateway.core.utils.parseParametersToObject(params, []),
                body: body
            };
            
            
            return apiGatewayClient.makeRequest(loansGetRequest, authType, additionalParams, config.apiKey);
        };
    }

    

    return apigClient;
};
