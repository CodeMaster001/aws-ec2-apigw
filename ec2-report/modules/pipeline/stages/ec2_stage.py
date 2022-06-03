
from aws_cdk import Stage
from constructs import Construct
from modules.pipeline.stacks.ec2_stack import Ec2InstanceStack
class EC2Stage(Stage):

    def __init__(self, scope: Construct, construct_id: str,env=None, **kwargs) -> None:
        super().__init__(scope, construct_id,**kwargs)
        Ec2InstanceStack(self,"EC2Stack",env=env)
