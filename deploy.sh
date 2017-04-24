#!usr/bin/env bash
source homepage.cfg
aws s3 sync site s3://$bucket_name \
    --exclude "*css/*" \
    --exclude "*js/*" \
    --exclude "*images/*" \
    --delete

aws s3 sync site/css s3://$bucket_name/css \
   --cache-control 'max-age=259200' \
   --delete

aws s3 sync site/js s3://$bucket_name/js \
   --cache-control 'max-age=259200' \
   --delete

aws s3 sync site/images s3://$bucket_name/images \
   --cache-control 'max-age=604800' \
   --delete
