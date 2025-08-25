import boto3
import click

def create_instance(name,ami,sshkey, instance_type, count):
    if instance_type != "t3.micro" and instance_type != "t2.small":
        print("invalid instance_type , you can only choose between t3.micro or t2.small!!")
        quit()
    if ami == 'ubuntu':
        ami = 'ami-0360c520857e3138f'
    elif ami == 'amazon':
        ami = 'ami-00ca32bbc84273381'
    else:
        print('not valid instance provider , must choose between ubuntu or amazon')
        quit()
    ec2c = boto3.client('ec2')
    resp = ec2c.describe_instances(
        Filters=[
            {'Name': 'tag:tag', 'Values': ['cli']},
            {'Name': 'instance-state-name', 'Values': ['pending', 'running', 'stopping', 'stopped']}
        ]
    )
    existing = sum(len(r.get('Instances', [])) for r in resp.get('Reservations', ['running']))

    if count > 2 or existing + count > 2:
        print("you can only create up to 2 instances.")
        quit()
    else:
        ec2 = boto3.resource('ec2')
        ec2.create_instances(
            ImageId=ami ,
            InstanceType=instance_type,
            KeyName=sshkey,
            MinCount=1,
            MaxCount=count,
            TagSpecifications=[
                {
                    'ResourceType': 'instance',
                    'Tags': [
                        {'Key': 'Name', 'Value': name},
                        {'Key': 'tag',  'Value': 'cli'}
                    ]
                }
            ]
        )
def list_cli_instance():
    ec2 = boto3.client('ec2')
    output = ec2.describe_instances(
        Filters=[
            {
                'Name': 'tag:tag' ,
                'Values': ['cli']
            }])
    for fil in output['Reservations']:
        for instance in fil['Instances']:
            instance_id = instance['InstanceId']
            state = instance['State']['Name']
            instance_type = instance['InstanceType']
            public_ip = instance.get('PublicIpAddress')
            name = next((t['Value'] for t in instance.get('Tags', []) if t['Key'] == 'Name'), 'N/A')
            if state != 'terminated':
                print(f"Name: {name} | ID: {instance_id} | State: {state} | Type: {instance_type} | Public IP: {public_ip}")

def stop_instance(instance_id):
    ec2 = boto3.client('ec2')
    response = ec2.describe_instances(InstanceIds=[instance_id])
    state = response['Reservations'][0]['Instances'][0]['State']['Name']
    if state == 'stopped':
        print(f"Instance {instance_id} is already in 'stopped' state")
    elif state == 'stopping':
        print(f"Instance {instance_id} is already in process of stopping")
    else:
        ec2.stop_instances(InstanceIds=[instance_id])
        print(f"Stop requested for {instance_id})")

def start_instance(instance_id):
    ec2 = boto3.client('ec2')
    response = ec2.describe_instances(InstanceIds=[instance_id])
    state = response['Reservations'][0]['Instances'][0]['State']['Name']
    if state == 'stopping':
         print(f"Instance {instance_id} is in 'stopping' state , wait 10 seconds please :) ")
    if state == 'running':
        print(f"Instance {instance_id} is already in 'running' state")
    elif state == 'pending':
        print(f"Instance {instance_id} is already in process of starting")
    else:
        ec2.start_instances(InstanceIds=[instance_id])
        print(f"Start requested for {instance_id} ")


