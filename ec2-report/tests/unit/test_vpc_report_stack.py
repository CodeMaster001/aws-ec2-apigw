import aws_cdk as core
import aws_cdk.assertions as assertions


from modules.pipeline.stacks.vpc_stack import VPCStack

# Some tests to show cdk can be tested with, we could add more tests but intrest of time ,I am adding only few tests.


def test_aws_vpc_created():
    app = core.App()
    stack = VPCStack(app, "vpc-stack")
    template = assertions.Template.from_stack(stack)
    print(template.to_json())

    template.has_resource("AWS::EC2::VPC", {})


def test_aws_vpc_created_with_enabled_dns_support():
    app = core.App()
    stack = VPCStack(app, "vpc-stack")
    template = assertions.Template.from_stack(stack)


    template.has_resource_properties(
        "AWS::EC2::VPC", {"EnableDnsSupport": True})

def test_aws_vpc_created_with_cidr_block():
    app = core.App()
    stack = VPCStack(app, "vpc-stack")
    template = assertions.Template.from_stack(stack)


    template.has_resource_properties(
        "AWS::EC2::VPC", {"CidrBlock": "192.168.50.0/24"})