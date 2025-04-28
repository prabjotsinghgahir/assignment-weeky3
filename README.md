# Assignment3

Below is a short description of different files:
1. .github/workflows/workflow.yaml : This is a github workflow file. This file runs when a push is happened on dev branch or pull request on main branch.
2. deploy_scripts/stack_deploy.py : This file creates a cloudformation stack using templates/glue-pipeline.yaml file. If the stack is already present then it will update the stack(if any updates are there to perform).
3. templates/glue-pipeline.yaml : Cloudformation template file. This creates 3 buckets, 2 glue job, 1 crawler, 2 lambda functions, sns, eventbridge rule, dynamodb and 3 iam roles.
4. main.py : This file orchestrate everything. This file contains cloudformation template parameter values and other variables. This file will call stack_deploy.py for creating or updating the stack. Then put items in dynamodb.
5. upload.sh : This file zips the lambda function code and upload it in code bucket. It also uploads glue job script in code bucket.
6. lambdas/lambda-glue.py : This is a lambda function code file. This file reads a small configuration from dynamodb and depending on the file type it run the appropriate glue job.
7. lambdas/lambda-crawler.py : This is the lambda function code file. It runs crawler and athena query to create a view.
8. glue_scripts/glue-job-csv.py : It is the Glue job script. It reads the file from s3 bucket. Change the column name and puts it in another s3 bucket. When a csv files lands in s3 bucket then lambda function runs this job. This reads csv file, change the column and write it as a csv.
9. glue_scripts/glue-job-json.py : It is the glue job script. It reads the file from s3 bucket. Change the column name and puts it in another s3 bucket. When a json files lands in s3 bucket then lambda function runs this job. This file reads json file, change the column name and write the file as csv.