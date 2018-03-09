#!usr/bin/env bash

source homepage.cfg

aws s3 sync site s3://$bucket_name \
    --exclude "*" \
    --include "*.css" \
    --include "*.js" \
    --metadata-directive REPLACE \
    --cache-control max-age=259200

aws s3 sync site/images s3://$bucket_name/images \
    --metadata-directive REPLACE \
    --cache-control max-age=604800

# Set all html files, and files without a file type (except RSS file)
# as content-type 'text/html'
aws s3 sync site s3://$bucket_name/ \
    --exclude "*.*" \
    --exclude "rss" \
    --include "*.html" \
    --metadata-directive REPLACE \
    --cache-control max-age=86400 \
    --content-type 'text/html'

# Set RSS file as content-type 'application\xml'
aws s3 sync site s3://$bucket_name \
    --exclude "*" \
    --include "rss" \
    --metadata-directive REPLACE \
    --cache-control max-age=86400 \
    --content-type 'application/xml'
