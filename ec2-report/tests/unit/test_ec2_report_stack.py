import aws_cdk
import aws_cdk.assertions as assertions
from tests.unit.dummy_vpc import DummyVPC
from modules.pipeline.stacks.api_lambda_stack import ApiLambdaStack

#Some tests to show cdk can be tested with, we could add more tests but intrest of time ,I am adding only few tests.


def test_aws_iam_role_created():
    app = aws_cdk.App()
    vpc_stack = DummyVPC(app,"vpc")
    stack = ApiLambdaStack(app, "ec2-report",vpc=vpc_stack.vpc)
    template = assertions.Template.from_stack(stack)

    template.has_resource("AWS::IAM::Role",{})
 

def test_lambda_is_created():
    app = aws_cdk.App()
    vpc_stack = DummyVPC(app,"vpc")
    stack = ApiLambdaStack(app, "ec2-report",vpc=vpc_stack.vpc)
    template = assertions.Template.from_stack(stack)

    template.has_resource("AWS::Lambda::Function",{})


def test_api_gateway_created():
    app = aws_cdk.App()
    vpc_stack = DummyVPC(app,"vpc")
    stack = ApiLambdaStack(app, "ec2-report",vpc=vpc_stack.vpc)
    template = assertions.Template.from_stack(stack)

    template.has_resource("AWS::ApiGateway::RestApi",{})


def test_api_fetch_report_created():
    app = aws_cdk.App()
    vpc_stack = DummyVPC(app,"vpc")
    stack = ApiLambdaStack(app, "ec2-report",vpc=vpc_stack.vpc)
    template = assertions.Template.from_stack(stack)

    template.has_resource_properties("AWS::ApiGateway::Resource",{"PathPart":"fetch_report"})

