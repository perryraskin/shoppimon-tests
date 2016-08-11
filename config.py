"""Configuration handling
"""

import yaml
import boto3

__config = None

def get_config(path):
    global __config

    if path.startswith("s3"):
        # Use Amazon S3
        s3 = boto3.resource('s3')

        bucket_name = path.split("/")[2]
        key_name = path.split(bucket_name[-1])

        # Download object at bucket-name with key-name to tmp.txt
        s3.download_file(bucket_name, key_name, "tmp.yaml")

        if __config is None:
            with open("tmp.yaml", 'r') as stream:
                __config = yaml.load(stream)
        
    else:
        if __config is None:
            with open(path, 'r') as stream:
                __config = yaml.load(stream)

    return __config
