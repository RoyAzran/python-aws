# AWS CLI Helper (Python + Click)

This project is a custom **command-line interface (CLI)** built in Python with [Click](https://click.palletsprojects.com/) for managing AWS resources using [boto3](https://boto3.amazonaws.com/).

It provides simple commands to create, list, update, and delete AWS resources such as **EC2 instances, S3 buckets, and Route 53 hosted zones**.

---

##  Features

### EC2 
- Create a new EC2 instance (`t3.micro` or `t2.small`, up to 2 instances max).
- List EC2 instances tagged.
- Start and stop EC2 instances safely (checks state before acting).

### S3 
- Create new S3 buckets with tagging .
- List all tagged buckets.
- Upload files to S3 with validation.
- Delete buckets (with cleanup of objects).

### Route 53 
- Create a new hosted zone.
- List hosted zones.
- Add, update, and delete DNS record sets.

### CLI Entrypoint (`main.py`)
- Central CLI interface using **Click**.
- Commands:  
  - `create-ec2`, `list-ec2`, `start-ec2`, `stop-ec2`  
  - `create-s3`, `list-s3`, `upload-s3`, `delete-s3`  
  - `create-r53`, `list-r53`, `update-r53`

---

## ️ Installation - 

0. yum install git -y

1. Clone this repo:
   ```bash
   git clone https://github.com/RoyAzran/python-aws.git
   cd python-aws
   ```
2.  Create a virtual environment:
   ```bash
   yum install pip -y
   python3 -m venv .venv
   source .venv/bin/activate   # Linux / macOS
   .venv\Scripts\activate      # Windows
   ```

3. Install dependencies:
   ```bash
     pip install -r requirements.txt
   ```

4. Configure your AWS CLI credentials:
   ```bash
   aws configure
   put aws accsess key , secret key and region
   ```
5. alias roycli="python3 /home/ec2-user/python-aws/main.py"


---

##  Usage

Run the CLI with Python:

```bash
roycli  --help
```

### EC2 examples
```bash
roycli create-ec2 --name testvm --ami ubuntu --key my-key --type t3.micro --count 1
roycli list-ec2
roycli stop-ec2 --id i-0123456789abcdef0
roycli start-ec2 --id i-0123456789abcdef0
```

### S3 examples
```bash
roycli create-s3 --name mybucket123
roycli list-s3
roycli upload-s3 --path ./file.txt --name mybucket123 --file-name file.txt
roycli delete-s3 --name mybucket123

### Route 53 examples
```bash
roycli create-r53 --name mydomain.com
roycli list-r53
roycli update-r53 --zone_id Z12345ABC --action CREATE --name mydomain.com --type A --value "1.2.3.4"
```

---



