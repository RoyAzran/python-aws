import boto3
import uuid

def create_tags(id):
    route53 = boto3.client('route53')
    route53.change_tags_for_resource(
    ResourceType='hostedzone',
    ResourceId=id,
    AddTags=[
        {
            'Key': 'cli',
            'Value': 'made'
        },
    ]
)
def create_zone(name):
        route53 = boto3.client('route53')
        response = route53.create_hosted_zone(
            Name = name ,
            CallerReference=str(uuid.uuid4())
        )
        zone_id = response['HostedZone']['Id'].split('/')[-1]
        create_tags(zone_id)
        print('Zone created!')


def update_records(z_id, action, domain_name, record_type, record_value):
    route53 = boto3.client('route53')
    tags = route53.list_tags_for_resource(
        ResourceType="hostedzone",
        ResourceId=z_id
    )["ResourceTagSet"].get("Tags", [])
    if any(tag["Key"] == "cli" and tag["Value"] == "made" for tag in tags):
        route53.change_resource_record_sets(
            HostedZoneId=z_id,
            ChangeBatch={
                'Changes': [
                    {
                        'Action': action,
                        'ResourceRecordSet': {
                            'Name': domain_name,
                            'Type': record_type,
                            'TTL': 3600,
                            'ResourceRecords': [
                                {'Value': record_value}
                            ]
                        }
                    }
                ]
            }
        )
    else:
        print(f" you dont have any zones.")


def list_hosted_zones_by_tag(tag_key='cli', tag_value='made'):
    route53 = boto3.client('route53')
    hosted_zones = route53.list_hosted_zones_by_name()['HostedZones']
    for z in hosted_zones:
        zid = z['Id'].split('/')[-1]
        tags = {t['Key']: t['Value'] for t in route53.list_tags_for_resource(
            ResourceType='hostedzone', ResourceId=zid)['ResourceTagSet']['Tags']}
        if tags.get(tag_key) == tag_value:
            print(f"Name: {z['Name']} | ID: {zid} | {'Private' if z['Config']['PrivateZone'] else 'Public'}")
            for r in route53.list_resource_record_sets(HostedZoneId=zid)['ResourceRecordSets']:
                print(f"Records: {r}")

