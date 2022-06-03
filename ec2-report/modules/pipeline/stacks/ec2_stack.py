from aws_cdk import (  
    Stack,
    aws_ec2 as ec2,
    

)
from constructs import Construct

class Ec2InstanceStack(Stack):

    def __init__(self, scope: Construct, id: str, **kwargs) -> None:
        super().__init__(scope, id, **kwargs)

        ##################################
        # Look up for vpc based on configs
        ##################################

        vpc = ec2.Vpc.from_lookup(
            self,
            "vpc",
            vpc_id=self.node.try_get_context('vpc-id'),
        )
        
        
        ##################################
        # Add Security group for http/https
        ##################################

        sec_group = ec2.SecurityGroup(
            self,
            "allow_All_http,https",
            vpc=vpc,
            allow_all_outbound=True,
        )

        sec_group.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            description="Allow all http connection", 
            connection=ec2.Port.tcp(80)
        )

        sec_group.add_ingress_rule(
            peer=ec2.Peer.any_ipv4(),
            description="Allow https connection", 
            connection=ec2.Port.tcp(443)
        )
       

        
        ##################################
        # Define new ec2 instance
        ##################################
        ec2_instance = ec2.Instance(
            self,
            "ec2-instance",
            instance_name="testinstance",
            instance_type=ec2.InstanceType("t2.micro"),
            machine_image=ec2.MachineImage().latest_amazon_linux(),
            vpc=vpc,
            security_group=sec_group,
        )
