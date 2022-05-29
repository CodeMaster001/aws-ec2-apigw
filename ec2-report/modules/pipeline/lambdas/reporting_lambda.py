import boto3
import traceback
import json
import logging

def lambda_handler(event, context):
    '''
    Params:
    event: Event which is used as an input to lambda contains list of regions or list all regions if not present
    Returns:
    (return):List of EC2 instances in the format which is accepted by API gateway.
    '''
    data = None

    try:
        result = ""
        logging.info('Even received:'+str(event))
        if event.get('body') is None:
            regions = ['us-east-1', 'ap-south-1']
        else:
            regions = json.loads(event.get('body'))['regions']

        for region in regions:
            result = result + get_info(region)

        data = result
    except Exception as ex:
        data = traceback.format_exc(chain=True)
    
    logging.info('Output generated:'+str(data))
    
    return {
        "isBase64Encoded": True,
        "statusCode": "200",
        "body": data
    }


def get_info(region_name):
    '''
    Params:
    region_name: Name of the region from which ec2 information needs to be fetched
    Returns:
    result(str):Returns a csv entry to be appended to the output
    '''

    result = ""
    ec2client = boto3.client('ec2', region_name=region_name)
    response = ec2client.describe_instances()

    for reservation in response["Reservations"]:
        for instance in reservation["Instances"]:
            instance_id = instance['InstanceId']
            state = instance['State']['Name']
            result = result + f"{instance_id},{state},{region_name}" + "\n"

    return result
