import logging
import boto3
import os
from botocore.config import Config

config = Config(
    retries={
        'max_attempts': 30
    }
)

glue_client = boto3.client('glue', config=config)
athena_client = boto3.client('athena')


def lambda_handler(event, context):
    crawler_name = os.getenv('crawlername')
    out_bucket = 's3://'+os.getenv('outputbucket')
    dbase = os.getenv('databasename')
    try:
        glue_client.start_crawler(Name=crawler_name)
        crawler_state = glue_client.get_crawler(Name=crawler_name)['Crawler']['State']
        print(crawler_state)
        while crawler_state == 'RUNNING':
            crawler_state = glue_client.get_crawler(Name=crawler_name)['Crawler']['State']
        print(crawler_state)
    except glue_client.exceptions.CrawlerRunningException:
        logging.warning("Crawler already running")
    try:
        crawler_table = glue_client.get_tables(DatabaseName=dbase)['TableList'][0]['Name']
        print(f"Printing crawler table: {crawler_table}")
    except IndexError:
        logging.error("Table not found")
        raise Exception("Table not found")
    athena_client.start_query_execution(
        QueryString='CREATE OR REPLACE VIEW test AS SELECT * FROM %s' % crawler_table,
        QueryExecutionContext={
            'Database': dbase
        },
        ResultConfiguration={
            'OutputLocation': out_bucket
        }
    )
