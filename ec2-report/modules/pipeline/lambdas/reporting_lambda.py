import boto3

def lambda_handler(event,context):
    '''
    Params:
    event: Event which is used as an input to lambda contains list of regions or list all regions if not present
    Returns:
    list that contains information about lambda.
    '''
    result = ""
    if event.get('req') is None:
        regions=['us-east-1','ap-south-1']
    else:
        regions = event.get('req')
    for region in regions:    
        result = result + get_info(region)
    
    return result

                
def get_info(region_name):

    result = ""
    ec2client = boto3.client('ec2',region_name=region_name)
    response = ec2client.describe_instances()
    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            instance_id = instance['InstanceId']
            state = instance['State']['Name']
            result = result + f"{instance_id},{state},{region_name}" + "\n"

    return result

