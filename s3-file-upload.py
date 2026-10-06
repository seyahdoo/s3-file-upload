#!/usr/bin/python

import os
import sys
import boto3
import argparse
from sys import exit
from os.path import normpath
from pathlib import PureWindowsPath
from pathlib import Path

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
        os.exit(1)
        return 
    
    file_name = os.path.basename(source)
    s3_path = os.path.join(destination, file_name)
    
    print(f"uploading {s3_path}...")
    client.upload_file(source, bucket, s3_path)
    
    print("done")
    os.exit(0)

if __name__ == '__main__':
    main()