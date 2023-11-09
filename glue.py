import boto3
import os
import sys
from io import BytesIO

def list_all_regions():
    client = boto3.client('ec2', region_name='us-east-1')
    region_list = set([region['RegionName'] for region in client.describe_regions()['Regions']])
    return region_list

def glue_functions_list(region=None):
    if not region:
        region_list = list_all_regions()
    else:
        if type(region) is list:
            region_list = region
        else:
            region_list = [region]
    resources = []

    for region in region_list:
        client = boto3.client('glue', region)
        response = client.get_jobs()['Jobs']

        for job in response:
            resources.append(job['Command']['ScriptLocation'])
        
    return resources

def separate_path(s3FullURI):
    s3_list = s3FullURI[5:].split('/')
    return s3_list.pop(0), s3_list.pop(-1), '/'.join(s3_list)

def download_glue_function(glue_list, dirPath):
    s3 = boto3.client('s3')
    for item in glue_list:
        print(f"Downloading {item}")
        bucket_name, suffix, prefix = separate_path(item)
        functionPath = os.path.join(dirPath, suffix.split('.')[0])
        if not os.path.exists(functionPath):
            os.mkdir(functionPath)
        s3.download_file(bucket_name, (prefix+'/'+suffix) if prefix else suffix, functionPath+'/{0}'.format(suffix))
    

if __name__ == "__main__":
    inp = sys.argv[1:]
    print("Destination folder {}".format(inp))

    if inp and os.path.exists(inp[0]):
        dest = os.path.abspath(inp[0])
        download_glue_function(glue_functions_list(), dest) 
    else:
        print("Destination folder doesn't exist")