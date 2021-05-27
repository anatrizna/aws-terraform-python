import boto3
import os

#client = boto3.client('ecs')

#target_cluster='infra-dev-sandbox'
os.environ['TARGET_CLUSTER'] = 'sandbox'
os.environ['TARGET_SERVICE'] = ''

target_cluster=os.environ.get('TARGET_CLUSTER')
target_service=os.environ.get('TARGET_SERVICE')

print(type(target_service))
print(len(target_service))