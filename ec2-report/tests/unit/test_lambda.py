from modules.pipeline.lambdas import reporting_lambda
from unittest import mock

@mock.patch('modules.pipeline.lambdas.reporting_lambda.get_info')
def test_lambda_handler_when_all_okay_status_is_200(return_func):
    return_func.return_value = "001,running,us-east-1"
    result = reporting_lambda.lambda_handler({},{})
    assert result == {'isBase64Encoded': True, 'statusCode': '200', 'body': '001,running,us-east-1001,running,us-east-1'}


@mock.patch('modules.pipeline.lambdas.reporting_lambda.get_info')
def test_lambda_handler_when_error_status_is_400(return_func):
    return_func.return_value = "001,running,us-east-1"
    result = reporting_lambda.lambda_handler(None,{})
    assert result['statusCode'] == '400'


