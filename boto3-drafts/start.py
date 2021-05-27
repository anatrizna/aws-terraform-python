import boto3

ec2 = boto3.resource('ec2', 'eu-central-1')
asg = boto3.client('autoscaling')
s3 = boto3.resource('s3')

def lambda_handler(event, context):
    text_instance_ids = s3.Object('ec2-scheduler-asg-data', 'instances_ids.txt')
    get_instance_ids = text_instance_ids.get()['Body'].read()
    instance_ids = eval(get_instance_ids)

    #Start instances
    starting_instances = ec2.instances.filter(Filters=[{'Name': 'instance-id', 'Values': instance_ids}]).start()
    print("---------")
    print("Instances successfully started:", instance_ids)