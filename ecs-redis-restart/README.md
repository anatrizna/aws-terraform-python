# General description

This project intend is to implement automatic restart for ECS services and Redis.

Redis restart and ECS restarts are independed, meaning you can run one of them or both.

# Pipeline

## job: restart-ecs
Job takes 'TARGET_CLUSTER' and 'TARGET_SERVICE' as input variables and runs ecs_restart.py script.

­`TARGET_CLUSTER` - **REQUIRED** - specifies the name of the cluster that needs to be restarted.

`TARGET_SERVICE` - **REQUIRED** - if left empty, all services in the specified cluster will be restarted. If one service is specified, only this service will be restarted. For example: '' to restart all services, 'backend-statistics-service' to restart only this service.

## job: restart-redis
Job takes 'TARGET_CLUSTER' and 'TARGET_NODE' as input variables and runs redis_restart.py script.

­`TARGET_CLUSTER` - **REQUIRED** - specifies the name of the cluster that needs to be restarted.

`TARGET_NODE` - **REQUIRED** - if left empty, all nodes in the specified cluster will be restarted. 
If only one node should be restarted, the value must be one of the allowed values: '0', '001', '002', '003'. It represents the last digits of target node name in AWS ElastiCache dashboard.  


