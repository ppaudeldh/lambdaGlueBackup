import boto3
import os
import sys
from urllib.request import urlopen
import zipfile
from io import BytesIO

def list_all_regions():
    client = boto3.client('ec2', region_name='us-east-1')
    region_list = set([region['RegionName'] for region in client.describe_regions()['Regions']])
    return region_list

def lambda_functions_dict(region=None):
    if not region:
        region_list = list_all_regions()
    else:
        if type(region) is list:
            region_list = region
        else:
            region_list = [region]
    resources = {}

    for region in region_list:
        client = boto3.client('lambda', region)
        response = client.list_functions()

        if response['Functions']:
            resources[region] = [item['FunctionName'] for item in response['Functions']]

        while response.get('NextMarker'):
            response = client.list_functions(
                Marker=response['NextMarker']
            )
            if response['Functions']:
                resources[region] += [item['FunctionName'] for item in response['Functions']]
    return resources


def download_lambda_function_code(fn_name, fn_code_link, dir_path):
    function_path = os.path.join(dir_path, fn_name)
    if not os.path.exists(function_path):
        os.mkdir(function_path)

    with urlopen(fn_code_link) as lambda_extract:
        with zipfile.ZipFile(BytesIO(lambda_extract.read())) as zfile:
            zfile.extractall(function_path)

if __name__ == "__main__":
    inp = sys.argv[1:]
    print("Destination folder {}".format(inp))

    if inp and os.path.exists(inp[0]):
        dest = os.path.abspath(inp[0])
        lambdaDict = lambda_functions_dict()
        for region in lambdaDict:
            client = boto3.client('lambda', region)
            for function in lambdaDict[region]:
                responseCode = client.get_function(FunctionName=function)['Code']
            
                print(f"Downloading Lambda function {function} from {region}")
                try:
                    download_lambda_function_code(function, responseCode['Location'], dest)
                except:
                    print("ECR image type. No source code to download")
    else:
        print("Destination folder doesn't exist")
