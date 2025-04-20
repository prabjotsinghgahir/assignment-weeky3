
import sys
from awsglue.transforms import *
from awsglue.utils import getResolvedOptions
from pyspark.context import SparkContext
from awsglue.context import GlueContext
from awsglue.job import Job

args = getResolvedOptions(sys.argv, ["JOB_NAME", "file_name", "s3_input", "s3_output_path"])
sc = SparkContext()
glueContext = GlueContext(sc)
spark = glueContext.spark_session
job = Job(glueContext)
job.init(args["JOB_NAME"], args)

# Script for Amazon S3 read
AmazonS3_read = glueContext.create_dynamic_frame.from_options(
    format_options={"multiline": True},
    connection_type="s3",
    format="json",
    connection_options={"paths": [args['s3_input'] + args['file_name']]}
)

# Script for Rename Field
RenameModify = RenameField.apply(
    frame=AmazonS3_read,
    old_name="age",
    new_name="oldage"
)

# Script for Amazon S3 write
AmazonS3_write = glueContext.write_dynamic_frame.from_options(
    frame=RenameModify,
    connection_type="s3",
    format="csv",
    connection_options={"path": args['s3_output_path']}
)

job.commit()
