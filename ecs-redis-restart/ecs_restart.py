import boto3
import os

client = boto3.client('ecs')

target_cluster=os.environ.get('TARGET_CLUSTER')
target_service=os.environ.get('TARGET_SERVICE')

#if no service defined - all services will be restarted
if len(target_service)==0:
    print("--------")
    print("All services in", target_cluster, "will be restarted")
    print("--------")

    #getting arns for all services
    services = client.list_services(cluster=target_cluster, maxResults=30)
    services_arns = services.get('serviceArns')

    #go through all services and find running tasks
    for s in services_arns:
        running_tasks = client.list_tasks(cluster=target_cluster,serviceName=s,desiredStatus='RUNNING')
        get_task=running_tasks.get('taskArns')
        if len(get_task) != 0: #if there are tasks running
            for t in get_task:
                client.stop_task(cluster=target_cluster, task=t, reason='Forced restart') #stop old tasks
            describe = client.describe_services(cluster='infra-dev-sandbox',services=[s])
            get_services = describe.get('services')
            get_parameters = get_services[0]
            desiredCount = get_parameters.get('desiredCount') #retireve desiredCount of tasks
            runningCount = get_parameters.get('runningCount') #verify that previous are stopped
            if runningCount == 0: #start new tasks
                client.update_service(cluster=target_cluster, service=s, desiredCount=desiredCount)
            print("Restarted service:", s)
            print("Number of tasks:", desiredCount)
            print("--------")
        else:
            print("This service currently is not running any task.")

#if target_services was defined, then only these services will be restarted
else: 
    service_list = eval(target_service)
    print("--------")
    print("Only", service_list, "in", target_cluster, "will be restarted")
    print("--------")    
    for s in service_list:
        running_tasks = client.list_tasks(cluster=target_cluster,serviceName=s,desiredStatus='RUNNING')
        get_task=running_tasks.get('taskArns')

        if len(get_task) != 0: #if there are tasks running
            for t in get_task:
                client.stop_task(cluster=target_cluster, task=t, reason='Forced restart') #stop old tasks
            describe = client.describe_services(cluster=target_cluster,services=[s])
            get_services = describe.get('services')
            get_parameters = get_services[0]
            desiredCount = get_parameters.get('desiredCount') #retireve desiredCount of tasks
            runningCount = get_parameters.get('runningCount') #verify that previous are stopped
            if runningCount == 0: #start new tasks
                client.update_service(cluster=target_cluster, service=s, desiredCount=desiredCount)
            print("Service restarted:", s)
            print("Number of tasks:", desiredCount)
            print("--------")
        else:
            print("This service currently is not running any task.")