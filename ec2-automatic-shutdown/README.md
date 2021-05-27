
# Latest update (3/3/2021)

Lambda is currently configured to search for a tag `Shutdown = "runner"`.
Cloudwatch event schedules:
- Stop - 9 PM GMT
- Start - 6 AM GMT
- Setup - 6:15 AM GMT

# General description

This project intend is to implement automatic ec2 start/stop using Lambda function triggered by CloudWatch events. The trick here is that instances are connected to auto-scaling groups, so you can't stop them without triggering autoscaling to replace instances. 
This code will first detatch instances from ASG, and push this data in s3 (the s3 you should create and define yourself in the code). Here s3 is called 'ec2-scheduler-asg-data', and it is defined in python script.
Then, when starting instances, first start script will power on ec2s, and then connect back to ASGs (thus, asg_setup should be scheduled in about 15-30 minutes after start_instance script, to give instances a while to switch from stopped to running state).

#Files

## iam.tf
Creates IAM role that allows Lambda to start/stop ec2 instances.

## cloudwatch.tf
Creates two events with associations.
`start_instances_event_rule` - event that triggers Lambda to start instances during the morning hours. Currently set to run at 7AM (CET) during working days. Associated with Lambda function $ec2_start_lambda$.
`stop_instances_event_rule` - event that triggers Lambda to stop instances during the evening hours. Currently set to run at 9PM (CET) during working days. Associated with Lambda function $ec2_stop_lambda$.

## lambda.tf
Creates two functions.
$ec2_start_lambda$ - uses `start_instance.py` Python script.
$ec2_stop_lambda$ -  uses `stop_instance.py` Python script.
$ec2_setup_lambda$ -  uses `asg_setup.py` Python script

## stop.py
Finds running ec2 instances in eu-central-1 region that have tag `Shutdown = "true"`, retireve IDs, ASGs, detatch from ASGs and then stop instances. Saves all gathered data in `atrium-ec2-scheduler-asg-data` bucket.

## start.py
Gets gata from `atrium-ec2-scheduler-asg-data` S3, retireve instance IDs and then start instances. 

## setup.py
Gets gata from `atrium-ec2-scheduler-asg-data` S3, attaches instances back to ASGs, sets min size back to 1 and cleans S3. 