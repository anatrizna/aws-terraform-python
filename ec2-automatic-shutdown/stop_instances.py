import boto3

ec2 = boto3.resource('ec2', 'eu-central-1')
asg = boto3.client('autoscaling')
s3 = boto3.resource('s3')

def lambda_handler(event, context):
    filter = [
        {'Name': 'tag:Shutdown',
        'Values': ['runner']},
        {'Name': 'instance-state-name',
        'Values': ['running']}]

    asg_names={}
    asg_list=[]
    
    instances = ec2.instances.filter(Filters=filter)
    instance_ids = [instance.id for instance in instances]

    describe_asg_instances = asg.describe_auto_scaling_instances(InstanceIds=instance_ids)
    get_instances = describe_asg_instances.get('AutoScalingInstances')

    #Determine which ec2 are in autoscaling groups
    for record in get_instances:
        get_instance= record.get('InstanceId')
        get_asg = record.get('AutoScalingGroupName')
        asg_names[get_instance] = get_asg
        asg_list.append(get_asg)

    describe_asg = asg.describe_auto_scaling_groups(AutoScalingGroupNames=asg_list)
    get_group = describe_asg.get('AutoScalingGroups')

    #Save gathered data in S3 called atrium-ec2-scheduler-asg-data
    convert_instance_ids=str(instance_ids)
    convert_asg_names=str(asg_names)
    convert_asg_list=str(asg_list)

    s3.Object('ec2-scheduler-asg-data', 'instances_ids.txt').put(Body=convert_instance_ids)
    s3.Object('ec2-scheduler-asg-data', 'instances_asg.txt').put(Body=convert_asg_names)
    s3.Object('ec2-scheduler-asg-data', 'asg_list.txt').put(Body=convert_asg_list)

    #Set autoscaling group min size to 0
    for name in asg_list:
        set_min = asg.update_auto_scaling_group(AutoScalingGroupName=name, MinSize=0)
        print(name, "minimal size now set to 0")
    print("-------")

    #Detatch ec2 from autoscaling groups and decrease desired count to 0, so no auto-scaling launched
    for pair in asg_names:
        detatch_asg = asg.detach_instances(InstanceIds=[pair], AutoScalingGroupName=asg_names[pair], ShouldDecrementDesiredCapacity=True)
        print("Instance", pair, "detatched from", asg_names[pair], "autoscaling group")

    #Stop all instances with tag
    stopping_instances = ec2.instances.filter(Filters=[{'Name': 'instance-id', 'Values': instance_ids}]).stop()
    print("---------")
    print("Instances successfully stopped:", instance_ids)