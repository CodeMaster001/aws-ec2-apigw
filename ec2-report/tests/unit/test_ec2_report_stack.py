import aws_cdk as core
import aws_cdk.assertions as assertions

from modules.pipeline.stages.api_gw_stage import ApiLambdaStage

#Some tests to show cdk can be tested with, we could add more tests but intrest of time ,I am adding only few tests.

def test_aws_iam_role_created():
    app = core.App()
    stack = ApiLambdaStage(app, "ec2-report",vpc=None)
    template = assertions.Template.from_stack(stack)

    template.has_resource("AWS::IAM::Role",{})
 

def test_lambda_is_created():
    app = core.App()
    stack = ApiLambdaStage(app, "ec2-report",vpc=None)
    template = assertions.Template.from_stack(stack)

    template.has_resource("AWS::Lambda::Function",{})


def test_api_gateway_created():
    app = core.App()
    stack = ApiLambdaStage(app, "ec2-report",vpc=None)
    template = assertions.Template.from_stack(stack)

    template.has_resource("AWS::ApiGateway::RestApi",{})


def test_api_fetch_report_created():
    app = core.App()
    stack = ApiLambdaStage(app, "ec2-report",vpc=None)
    template = assertions.Template.from_stack(stack)

    template.has_resource_properties("AWS::ApiGateway::Resource",{"PathPart":"fetch_report"})

