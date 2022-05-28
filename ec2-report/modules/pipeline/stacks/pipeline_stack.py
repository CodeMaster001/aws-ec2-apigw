import os
from aws_cdk import Aws, pipelines
from aws_cdk import Stack
from aws_cdk import (
    pipelines,
)
from constructs import Construct
from modules.pipeline.stages.api_gw_stage import ApiLambdaStage
from modules.pipeline.stages.ec2_stage import EC2Stage

class PipelineStack(Stack):
    def __init__(self, scope: Construct, id: str,  **kwargs):
        super().__init__(scope, id, **kwargs)
        connection_obj = pipelines.CodePipelineSource.connection("CodeMaster001/aws-test", "main",connection_arn=self.node.try_get_context('codestar_connection'))
        pipeline = pipelines.CodePipeline(self, "Pipeline",
                                          synth=pipelines.ShellStep("Synth",
                                                                    # Use a connection created using the AWS console to authenticate to GitHub
                                                                    # Other sources are available.
                                                                    input=connection_obj,
                                                                    commands=["npm install -g aws-cdk@2.25.0","pwd","mkdir ec2-report/cdk.out",
                                                                              "pip install -r ec2-report/requirements.txt","cd ec2-report", "pytest -v .", "cdk synth"],
                                                                              primary_output_directory="ec2-report/cdk.out"

                                                                    )
           
                                          )
        #########################################################
        #Add API Stack and add a manual approval step before that
        #
        ########################################################
        ec2_stage = pipeline.add_stage(stage=EC2Stage(self, "DummyEC2", **kwargs))

        api_deployment_stage = pipeline.add_stage(stage=ApiLambdaStage(self, "APIPipleLine", **kwargs),pre=pipelines.ManualApprovalStep("Deploy API","Please use it carefully and with honor"))