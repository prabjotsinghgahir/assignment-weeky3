#!/usr/bin/env bash

bucket=$1
echo "${bucket}"

echo "Running script to zip and upload lambda"
for f in lambdas/*;do
  echo "${f}"
  zipfile=$(echo ${f} | cut -f 1 -d '.').zip
  zip -j "${zipfile}" "${f}"
  #echo "$(cut -f 1 -d '.').zip"
  aws s3 cp --no-progress "${zipfile}" "s3://${bucket}"
done

echo "Running upload glue scripts to s3"
for f in glue_scripts/*;do
  echo "${f}"
  aws s3 cp --no-progress "${f}" "s3://${bucket}"
done