import os
from deploy_scripts import stack_deploy

template_name = 'templates/glue-pipeline.yaml'
lambda_glue_file = "lambda-glue.zip"
lambda_glue_crawler = "lambda-crawler.zip"
lambda_function_name = "cf-lambda-copy-s3"
lambda_code_bucket = os.getenv("BUCKET")
stack_name = 'assignment3'
source_bucket_name = "cf-a3-input-bucket-landing-psg"
crawler_bucket_name = "cf-a3-crawler-bucket-psg"
destination_bucket_name = "cf-a3-athena-output-bucket-psg"
crawler_name = "cf-a3-crawler-psg"
glue_job_csv = "glue-job-csv.py"
glue_job_json = "glue-job-json.py"
dynamodb_table_name = "glueTable"
glue_csv_name = "glue-job-csv"
glue_json_name = "glue-job-json"
region = 'ap-south-1'


parameter = [
    {
        'ParameterKey': 'S3InputBucketName',
        'ParameterValue': source_bucket_name
    },
    {
        'ParameterKey': 'S3CrawlerBucketName',
        'ParameterValue': crawler_bucket_name
    },
    {
        'ParameterKey': 'S3OutputAthenaBucketName',
        'ParameterValue': destination_bucket_name
    },
    {
        'ParameterKey': 'CodeGlueBucket',
        'ParameterValue': lambda_code_bucket
    },
    {
        'ParameterKey': 'CName',
        'ParameterValue': crawler_name
    },
    {
        'ParameterKey': 'LambdaCrawlerKey',
        'ParameterValue': lambda_glue_crawler
    },
    {
        'ParameterKey': 'LambdaGlueKey',
        'ParameterValue': lambda_glue_file
    },
    {
        'ParameterKey': 'GlueJobCsvFileName',
        'ParameterValue': glue_job_csv
    },
    {
        'ParameterKey': 'GlueJobJsonFileName',
        'ParameterValue': glue_job_json
    },
    {
        'ParameterKey': 'DynamoTableName',
        'ParameterValue': dynamodb_table_name
    },
    {
        'ParameterKey': 'GlueJobCsvName',
        'ParameterValue': glue_csv_name
    },
    {
        'ParameterKey': 'GlueJobJsonName',
        'ParameterValue': glue_json_name
    }
]

opening_temp = open(template_name)
reading = opening_temp.read()

call_create_stack = stack_deploy.StackCreation(stack_name, reading, parameter)

call_create_stack.create_stack()
call_create_stack.stack_status()