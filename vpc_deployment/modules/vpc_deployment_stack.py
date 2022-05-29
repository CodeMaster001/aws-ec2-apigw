# For consistency with other languages, `cdk` is the preferred import name for
# the CDK's core module.  The following line also imports it as `core` for use
# with examples from the CDK Developer's Guide, which are in the process of
# being updated to use `cdk`.  You may delete this import if you don't need it.
from aws_cdk import Stack
from constructs import Construct
from aws_cdk import (
    aws_ec2 as ec2,
    aws_ssm as ssm,
    CfnOutput



)


class VPCDeploymentStack(Stack):

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
                           enable_dns_support=True,
                           subnet_configuration=[
                               ec2.SubnetConfiguration(
                                   name='Public-Subent',
                                   subnet_type=ec2.SubnetType.PUBLIC,
                                   cidr_mask=26
                               ),
                               ec2.SubnetConfiguration(
                                   name='Private-Subnet',
                                   subnet_type=ec2.SubnetType.PRIVATE_WITH_NAT,
                                   cidr_mask=26
                               )
                           ],default_instance_tenancy=ec2.DefaultInstanceTenancy
                           nat_gateways=1

                           )   
        CfnOutput(self, 'vpc-id', value=self.vpc.vpc_id)
