import click
from botocore.exceptions import ClientError
import boto3

def get_bucket_name_from_arn(arn):
    return arn.split(":::")[-1]


def get_buckets_with_tags():
    tag_client = boto3.client("resourcegroupstaggingapi")
    s3 = boto3.resource('s3')
    response = tag_client.get_resources(
        ResourceTypeFilters=["s3"],
        TagFilters=[
            {"Key": "Roy", "Values": ["prod"]},
        ],
    )
    buckets = []
    for resource in response["ResourceTagMappingList"]:
        arn = resource["ResourceARN"]
        bucket_name = get_bucket_name_from_arn(arn)
        buckets.append(
            {
                "name": bucket_name,            }
        )
    if len(buckets) == 0:
        print('You dont have any buckets! ')
    else:
        print( buckets)

def create_bucket(bucket_name):
    s3 = boto3.client('s3')
    existing = [b['Name'] for b in s3.list_buckets()['Buckets']]
    if bucket_name in existing:
        print(f" The bucket '{bucket_name}' already exists in your account.")
        quit()
    tags = [{"Key" : "Roy" , "Value" : "prod"}]
    try:
        s3.create_bucket(Bucket=bucket_name)
        s3.put_bucket_tagging(Bucket=bucket_name , Tagging={
            "TagSet" : tags

        })

        privorpub = str(input("choose public or private: "))
        if privorpub == "public":
            sure = str(input("Are you sure you want this bucket to be public? y/n "))
            if sure == 'y':
                s3.put_public_access_block(Bucket=bucket_name , PublicAccessBlockConfiguration={
                        'BlockPublicAcls': False,
                        'IgnorePublicAcls': False,
                        'BlockPublicPolicy': False,
                        'RestrictPublicBuckets': False
                })
            else:
                s3.put_public_access_block(Bucket=bucket_name, PublicAccessBlockConfiguration={
                    'BlockPublicAcls': True,
                    'IgnorePublicAcls': True,
                    'BlockPublicPolicy': True,
                    'RestrictPublicBuckets': True
                })
        print("Bucket created!")
    except ClientError as e:
        if e.response['Error']['Code'] in ("BucketAlreadyExists"):
            print(f" The bucket '{bucket_name}' already exists.")

def upload_file(path , bucket_name , file_name):
    s3 = boto3.client('s3')
    tags = s3.get_bucket_tagging(Bucket=bucket_name)['TagSet']
    if any(t['Key'] == 'Roy' and t['Value'] == 'prod' for t in tags):
        s3.upload_file(path, bucket_name, file_name)
        print("File uploaded!")

def delete_bucket(bucket_name):
    s3 = boto3.resource('s3')
    bucket = s3.Bucket(bucket_name)
    bucket.objects.all().delete()
    bucket.delete()
    print('Bucket deleted!')
