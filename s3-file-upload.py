#!/usr/bin/python

import os
import sys
import boto3
import argparse
from pathlib import Path
import posixpath
import string
import secrets

KEY_LENGTH = 32

def main():
    parser = argparse.ArgumentParser(description='upload file to aws s3 bucket')
    parser.add_argument('--source', required=True, type=str, help="source file")
    parser.add_argument('--bucket', required=True, type=str, help="target s3 bucket name")
    parser.add_argument('--destination', required=True, type=str, help="destination directory")
    parser.add_argument('--awsRegion', required=True, type=str, help="target aws region")
    parser.add_argument('--awsAccessKeyID', required=True, type=str, help="AWS access key id, get it from IAM users")
    parser.add_argument('--awsSecretAccessKey', required=True, type=str, help="AWS secret access key, get it from IAM users")
    args = parser.parse_args()

    source = args.source
    bucket = args.bucket
    destination = args.destination
    aws_region = args.awsRegion
    aws_access_key_id = args.awsAccessKeyID
    aws_secret_access_key = args.awsSecretAccessKey

    print("initializing aws client")
    client = boto3.client('s3', region_name = aws_region, aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)

    if not Path(source).exists():
        print("source file not found", file=sys.stderr)
        sys.exit(1)
        return

    key = ''.join(secrets.choice(string.ascii_letters + string.digits) for _ in range(KEY_LENGTH))
    file_name = os.path.basename(source)
    s3_path = posixpath.join(destination, key, file_name)

    print(f"uploading {s3_path}...")
    client.upload_file(source, bucket, s3_path)

    url = f"https://{bucket}.s3.{aws_region}.amazonaws.com/{s3_path}";
    print(f"file url: {url}")

    print("done")
    sys.exit(0)
    return

if __name__ == '__main__':
    main()