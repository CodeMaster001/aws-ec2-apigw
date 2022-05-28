import aws_cdk as core
import aws_cdk.assertions as assertions

from vpc_deployment.vpc_deployment_stack import VpcDeploymentStack

# example tests. To run these tests, uncomment this file along with the example
# resource in vpc_deployment/vpc_deployment_stack.py
def test_sqs_queue_created():
    app = core.App()
    stack = VpcDeploymentStack(app, "vpc-deployment")
    template = assertions.Template.from_stack(stack)

#     template.has_resource_properties("AWS::SQS::Queue", {
#         "VisibilityTimeout": 300
#     })
