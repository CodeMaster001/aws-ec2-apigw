# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import Stack
import aws_cdk
from constructs import Construct
from aws_cdk import (
    aws_lambda,
    Duration,
    aws_iam as iam,
    aws_apigateway as apigw,
    aws_ec2 as ec2,
    aws_ssm as ssm

)


class ApiLambdaStack(Stack):

    def __init__(self, scope: Construct, construct_id: str, vpc: ec2.Vpc = None, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)
        ###########################
       #
       # Lambda Configurationg(IAM)

       # ########################

        if vpc is None:
            vpc = ec2.Vpc.from_lookup(
                self, "vpc-lookup", vpc_id=self.node.try_get_context('vpc-id'))

        self.lambda_role = iam.Role(
            self, "Role", assumed_by=iam.ServicePrincipal("lambda.amazonaws.com"))

        self.lambda_role.add_to_policy(iam.PolicyStatement(
            effect=iam.Effect.ALLOW,
            resources=["*"],
            actions=["ec2:Describe*",
                     "ec2:DescribeNetworkInterfaces",
                     "ec2:CreateNetworkInterface",
                     "ec2:DeleteNetworkInterface",
                     "ec2:DescribeInstances",
                     "ec2:AttachNetworkInterface",
                     "logs:CreateLogGroup",
                     "logs:CreateLogStream",
                     "logs:PutLogEvents"
                     ]
        ))

        ##################################
        # Lambda Security Group
        ##################################
        self.lambda_sg = ec2.SecurityGroup(
            self,
            id="sg_elb",
            vpc=vpc,
            security_group_name="sg_elb"
        )

        # Extra safety for lambda

        self.lambda_sg.add_egress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(443)
        )
        self.lambda_sg.add_egress_rule(
            peer=ec2.Peer.any_ipv4(),
            connection=ec2.Port.tcp(80)
        )

        ##################################
        # Define Lambda Function
        ##################################
        report_lambda = aws_lambda.Function(self, "reporting_lambda", function_name="report_lambda",
                                            runtime=aws_lambda.Runtime.PYTHON_3_9,
                                            handler="reporting_lambda.lambda_handler",
                                            code=aws_lambda.Code.from_asset(
                                                "../ec2-report/modules/pipeline/lambdas"),
                                            memory_size=2048,
                                            timeout=Duration.seconds(60*3),
                                            role=self.lambda_role,
                                            security_groups=[self.lambda_sg]
                                            )

        ##################################
        # API Configuration,
        ##################################

        base_api = apigw.RestApi(
            self, 'ApiGW', rest_api_name='ec2_report', deploy=True)

        base_api.root.add_method("Any")
        fetch_api = base_api.root.add_resource('fetch_report')
        fetch_api.add_method('POST', integration=apigw.LambdaIntegration(
            handler=report_lambda, proxy=True), api_key_required=True)  # PI KEY

        ##################################
        # Create deployment and Stage
        ##################################

        deployment = apigw.Deployment(
            self, id="dep", api=base_api, retain_deployments=True)
        stage = apigw.Stage(
            self, "dev", deployment=deployment, stage_name="test")

        ##################################
        # Create Usage Plan amd add api key to it
        ##################################

        plan = base_api.add_usage_plan("usage", name="ec2_reports", throttle={
                                       "rate_limit": 10, "burst_limit": 20}, api_stages=[apigw.UsagePlanPerApiStage(api=base_api, stage=stage)])
        api_key = apigw.ApiKey(
            self, "apikey", api_key_name="prod", value=self.node.try_get_context('api-key'))
        plan.add_api_key(api_key)
        base_api.deployment_stage = stage

        aws_cdk.CfnOutput(self, 'apiURL', value=base_api.url +
                          fetch_api.path.replace('/', ''))
