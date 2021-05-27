import boto3
import os

client = boto3.client('elasticache')

os.environ['TARGET_CLUSTER'] = 'cluster'
os.environ['TARGET_NODE'] = '' 

target_cluster=os.environ.get('TARGET_CLUSTER')
target_node=os.environ.get('TARGET_NODE')

if len(target_node)==0: 
    all_nodes = ['0', '001', '002', '003']
    for n in all_nodes:
      cluster = target_cluster + '-' + n
      shard_id = '0001'
      node_restart = client.reboot_cache_cluster(CacheClusterId=cluster, CacheNodeIdsToReboot=[shard_id])
    print("--------")
    print("All nodes in", target_cluster, "are restarting.")
    print("Note that restart can take up to 5 minutes.")
    print("--------")

else:
    cluster = target_cluster + '-' + target_node
    shard_id = '0001'
    node_restart = client.reboot_cache_cluster(CacheClusterId=cluster, CacheNodeIdsToReboot=[shard_id])
    print("--------")
    print("Node", target_node, "in", target_cluster, "is restarting.")
    print("Note that restart can take up to 5 minutes.")
    print("--------")