import botocore
import ec2
import click
import route53
import s3

@click.group()
def cli():
    pass


@cli.command(name="create-ec2")
@click.option("--name" , required=True , help="instance name")
@click.option("ami",'--ami' ,type=click.Choice(["ubuntu","amazon"]) , required=True , help="instance provider choose between ubuntu and amazon")
@click.option("--key" , required= True , help="instance ssh key pair name")
@click.option("--type" , type=click.Choice(["t3.micro","t2.small"]) , required=True)
@click.option("--count", type=click.IntRange(1,2), default=1, show_default=True)
def create_instance_cmd(name,ami,key,type,count):
    try:
        ec2.create_instance(name,ami,key,type,count)
        print('instance created!')
    except botocore.exceptions.ClientError as e:
        code = e.response["Error"].get("Code", "")
        if code == "InvalidKeyPair.NotFound":
            print("Not a valid keypair use existing one")

@cli.command(name="list-ec2")
def list_instances_cmd():
    ec2.list_cli_instance()


@cli.command(name='stop-ec2')
@click.option("--instance-id","--id" , required=True , help="instance ID (e.g., i-0123456789abcdef0)")
def stop_ec2_cmd(instance_id):
        ec2.stop_instance(instance_id)

@cli.command(name="start-ec2")
@click.option("--instance-id", "--id", required=True , help="instance ID (e.g., i-0123456789abcdef0)")
def start_ec2_cmd(instance_id):
    ec2.start_instance(instance_id)

@cli.command(name="create-s3")
@click.option("--bucket-name","--name", required=True,help="s3 bucket name")
def create_s3_cmd(bucket_name):
    s3.create_bucket(bucket_name)

@cli.command(name="upload-s3")
@click.option("--path", required=True , help="file path")
@click.option("--bucket-name","--name" , required=True , help="bucket name")
@click.option("--file-name", required=True , help="upload file to s3 bucket")
def upload_s3_file_cmd(path , bucket_name , file_name):
     try:
      s3.upload_file(path , bucket_name , file_name)
     except botocore.exceptions.ClientError as e:
        code = e.response["Error"].get("Code", "")
        if code == "NoSuchBucket" or "AccessDenied":
            print(" The specified bucket does not exist in your account")
     except FileNotFoundError as e:
            print("Cant find the file path. ")



@cli.command(name="list-s3")
def list_s3_with_tags_cmd():
        s3.get_buckets_with_tags()

@cli.command(name="delete-s3")
@click.option("--bucket-name","--name" , required=True , help="bucket name")
def delete_s3(bucket_name):
    try:
        s3.delete_bucket(bucket_name)
    except botocore.exceptions.ClientError as e:
        code = e.response["Error"].get("Code", "")
        if code == "NoSuchBucket" or "AccessDenied":
            print(" The specified bucket does not exist in your account")

@cli.command(name="create-r53")
@click.option("--d-name","--name" , required=True , help="route53 domain name (e.g.,roy123.com) ")
def create_r53_cmd(d_name):
    route53.create_zone(d_name)

@cli.command(name="list-r53")
def list_r53_cmd():
    route53.list_hosted_zones_by_tag()

@cli.command(name="update-r53")
@click.option("--zone_id", "zid" , required=True , help="The zone ID (e.g.,Z034553925V2VMQ2O1PIA)")
@click.option("--action" ,type=click.Choice(["CREATE","DELETE","UPSERT"]) , help="CREATE,DELETE,UPSERT a record type to a domain")
@click.option("--name","domain_name", required=True , help="route53 domain name (e.g.,roy123.com) ")
@click.option("--type","record_type",type=click.Choice(["A", "AAAA" , "CAA" ,"CNAME","DS", "MX","NAPTR","NS","PTR","SOA","SPF","SRV"]), help="Insert record type options: (A | AAAA | CAA | CNAME | DS | MX | NAPTR | NS | PTR | SOA | SPF | SRV)")
@click.option("--value","record_value" , required=True , help="record value")
def update_records_cmd(zone_id, action, domain_name, record_type, record_value):
        route53.update_records(zone_id, action, domain_name, record_type, record_value)




if __name__ == "__main__":
    cli()