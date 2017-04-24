#!usr/bin/env bash
source homepage.cfg
aws s3 sync site s3://$bucket_name --delete
