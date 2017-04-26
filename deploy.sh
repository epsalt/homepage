#!usr/bin/env bash
source homepage.cfg
aws s3 sync site s3://$bucket_name \
    --delete

aws s3 cp site/css s3://$bucket_name/css \
    --metadata-directive REPLACE \
    --cache-control max-age=259200 \
    --recursive

aws s3 cp site/js s3://$bucket_name/js \
   --metadata-directive REPLACE \
   --cache-control max-age=259200 \
   --recursive

aws s3 cp site/images s3://$bucket_name/images \
   --metadata-directive REPLACE \
   --cache-control max-age=604800 \
   --recursive
