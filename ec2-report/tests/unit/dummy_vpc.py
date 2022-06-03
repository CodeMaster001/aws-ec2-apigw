from constructs import Construct
from aws_cdk import (
    aws_ec2 as ec2,
    Stack

)


class DummyVPC(Stack):

    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        #################################
        # SET UP VPC FOR NOW USE DEFAULT VPC
        #
        ##################################
        self.vpc = ec2.Vpc(self, 'reportvpc',
                           cidr='192.168.50.0/24',
                           max_azs=2,
                           enable_dns_hostnames=True,
                           enable_dns_support=True
                           )   
       