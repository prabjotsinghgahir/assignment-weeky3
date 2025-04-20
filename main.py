import os
from deploy_scripts import stack_deploy

template_name = 'templates/glue-pipeline.yaml'
file_zip = 'copy_function.py'
lambda_function_name = "cf-lambda-copy-s3"
lambda_code_bucket = os.getenv("BUCKET")
stack_name = 'assignment1'
source_bucket_name = "cf-bucket-landing-psg"
destination_bucket_name = "cf-bucket-copy-psg"
region = 'ap-south-1'


parameter = [
        {
            'ParameterKey': 'SourceBucketName',
            'ParameterValue': source_bucket_name
        },
        {
            'ParameterKey': 'DestinationBucketName',
            'ParameterValue': destination_bucket_name
        },
        {
            'ParameterKey': 'CodeBucketName',
            'ParameterValue': lambda_code_bucket
        },
        {
            'ParameterKey': 'LambdaFunctionKey',
            'ParameterValue': file_zip.split('.')[0]+".zip"
        },
        {
            'ParameterKey': 'LambdaFunctionHandler',
            'ParameterValue': file_zip.split('.')[0]+".lambda_handler"
        },
        {
            'ParameterKey': 'LambdaFunctionName',
            'ParameterValue': lambda_function_name
        }
]

opening_temp = open(template_name)
reading = opening_temp.read()

call_create_stack = stack_deploy.StackCreation(stack_name, reading, parameter)

call_create_stack.create_stack()
call_create_stack.stack_status()