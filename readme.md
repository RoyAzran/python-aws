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

## ️ Installation

1. Clone this repo:
   ```bash
   git clone https://github.com/<your-username>/<repo-name>.git
   cd <repo-name>
   ```

2. (Optional) Create a virtual environment:
   ```bash
   python -m venv .venv
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
   ```

---

##  Usage

Run the CLI with Python:

```bash
python main.py --help
```

### EC2 examples
```bash
python main.py create-ec2 --name testvm --ami ubuntu --key my-key --type t3.micro --count 1
python main.py list-ec2
python main.py stop-ec2 --id i-0123456789abcdef0
python main.py start-ec2 --id i-0123456789abcdef0
```

### S3 examples
```bash
python main.py create-s3 --name mybucket123
python main.py list-s3
python main.py upload-s3 --path ./file.txt --name mybucket123 --file-name file.txt
python main.py delete-s3 --name mybucket123
```

### Route 53 examples
```bash
python main.py create-r53 --name mydomain.com
python main.py list-r53
python main.py update-r53 --zone_id Z12345ABC --action CREATE --name mydomain.com --type A --value "1.2.3.4"
```

---

##  Requirements

- Python 3.8+
- AWS CLI configured with credentials
- boto3 / botocore
- click

---
