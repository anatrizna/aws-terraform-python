import boto3
import os
from datetime import datetime

ssm = boto3.client('ssm')
s3 = boto3.client('s3')

###Get RDS password from SSM
os.environ['TARGET_ENV'] = 'sandbox'
os.environ['S3_LIFECYCLE'] = '1'
target_env=os.environ.get('TARGET_ENV')
lifecycle=os.environ.get('S3_LIFECYCLE')

draft_path = '/infra-dev/postgres/password'
place = draft_path.find('postgres/password')
target_path = draft_path[:place] + target_env + "/" + draft_path[place:]

parameter = ssm.get_parameter(Name=target_path, WithDecryption=True)
key = parameter['Parameter']['Value']

###Get date, time that will be used to create S3 bucket
now = datetime.now()
date = now.strftime("%b%d%H%M")

###Create S3 with lifecycle policy
s3_name = 'backup-' + target_env + '-' + date
policy_id = target_env + date

create_s3 = s3.create_bucket(Bucket=s3_name.lower(), CreateBucketConfiguration={'LocationConstraint': 'eu-central-1'})
permissions_s3 = s3.put_public_access_block(Bucket=s3_name.lower(),PublicAccessBlockConfiguration={'BlockPublicAcls': True, 'IgnorePublicAcls': True,'BlockPublicPolicy': True, 'RestrictPublicBuckets': True}, ExpectedBucketOwner='280811547308')
encrypt_s3 = s3.put_bucket_encryption(Bucket=s3_name.lower(),ServerSideEncryptionConfiguration={'Rules': [{'ApplyServerSideEncryptionByDefault': {'SSEAlgorithm': 'AES256'},'BucketKeyEnabled': False}]},ExpectedBucketOwner='280811547308')
add_policy_s3 = s3.put_bucket_lifecycle_configuration(Bucket=s3_name.lower(), LifecycleConfiguration={'Rules': [{'Expiration': {'Days': int(lifecycle)},'ID': policy_id.lower(), 'Filter': {'Prefix': ''}, 'Status': 'Enabled'}]}, ExpectedBucketOwner='280811547308')

print('--------')
print('Bucket', s3_name.lower(), 'is created.')
print('Note that', s3_name.lower(), 'bucket will be deleted automatically after', lifecycle, 'day(s).')
print('You can change it by disabling a policy in AWS management console.')
print('--------')

##Output gathered key and created s3 name
os.environ['ENV_KEY'] = key
os.environ['S3_NAME'] = s3_name.lower()

#env_key=os.environ.get('ENV_KEY')
#s3_name=os.environ.get('S3_NAME')
