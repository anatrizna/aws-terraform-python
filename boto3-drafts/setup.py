import boto3

asg = boto3.client('autoscaling')
s3_resource = boto3.resource('s3')
s3_client = boto3.client('s3')

def lambda_handler(event, context):
    text_instance_asg = s3_resource.Object('ec2-scheduler-asg-data', 'instances_asg.txt')
    text_asg_list = s3_resource.Object('ec2-scheduler-asg-data', 'asg_list.txt')

    get_instance_asg = text_instance_asg.get()['Body'].read()
    get_asg_list = text_asg_list.get()['Body'].read()

    instance_asg = eval(get_instance_asg)
    asg_list = eval(get_asg_list)

    #Connect instances to autoscaling groups
    for pair in instance_asg:
        attach_asg = asg.attach_instances(InstanceIds=[pair], AutoScalingGroupName=instance_asg[pair])
        print("---------")
        print("Instance", pair, "attatched to", instance_asg[pair], "autoscaling group")

    #Set min size back to 1
    for i in asg_list:
        set_min = asg.update_auto_scaling_group(AutoScalingGroupName=i, MinSize=1)

    #Delete files
    remove_instance_ids = s3_client.delete_object(Bucket='ec2-scheduler-asg-data', Key='instances_ids.txt',)
    remove_instance_asg = s3_client.delete_object(Bucket='ec2-scheduler-asg-data', Key='instances_asg.txt',)
    remove_asg_desiredcount = s3_client.delete_object(Bucket='ec2-scheduler-asg-data', Key='asg_list.txt',)
    print("---------")
    print("Files removed from S3")