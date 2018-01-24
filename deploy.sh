#!usr/bin/env bash

source homepage.cfg

aws s3 sync site s3://$bucket_name

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

aws s3 cp s3://$bucket_name/rss s3://$bucket_name/rss \
    --metadata-directive REPLACE \
    --content-type 'application/xml'

aws s3 cp s3://$bucket_name/ s3://$bucket_name/ \
    --metadata-directive REPLACE \
    --content-type 'text/html' \
    --exclude "*.*" \
    --exclude "rss" \
    --recursive
