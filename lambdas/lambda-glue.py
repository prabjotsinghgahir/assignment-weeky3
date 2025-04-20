import boto3
import os
import logging

logging.getLogger().setLevel("INFO")
dynamodb_client = boto3.client('dynamodb')
glue_client = boto3.client('glue')


def dynamodb_item(file_type):
    try:
        res = dynamodb_client.get_item(
                TableName=os.getenv('dynamotablename'),
                Key={
                    'fileType': {'S': file_type}
                }
            )
        return res['Item']['glueJobName']['S']
    except dynamodb_client.exceptions.ResourceNotFoundException as err:
        logging.error("dynamodb Table not found")
        raise Exception(err)
    except KeyError as er:
        logging.error("Above file is not compatible")
        raise Exception(er)
    except dynamodb_client.exceptions.ClientError as e:
        logging.error("Key does not match the schema")
        raise Exception(e)


def lambda_handler(event, context):

    file_name = event['Records'][0]['s3']['object']['key']
    #file_name = "some.csv"
    glue_job_name = dynamodb_item(file_name.split(".")[-1])
    logging.info(f"Printing glue job name: {glue_job_name}")
    try:
        result = glue_client.start_job_run(
            JobName=glue_job_name,
            Arguments={"--file_name": file_name}
        )

        job_status = glue_client.get_job_run(
            JobName=glue_job_name,
            RunId=result['JobRunId']
        )['JobRun']['JobRunState']

        if job_status == "RUNNING" or job_status == "STARTING":
            logging.info(f"Glue Job {glue_job_name} started successfully")

    except glue_client.exceptions.ConcurrentRunsExceededException:
        logging.error("Maximum concurrent run threshold exceeded")
