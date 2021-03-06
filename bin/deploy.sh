#!/bin/bash

aws s3 sync site s3://${BUCKET} \
    --size-only \
    --delete \
    --exclude "*" \
    --include "rss" \
    --cache-control max-age=${LONG_CACHE} \
    --content-type 'application/xml'

aws s3 sync site s3://${BUCKET}/ \
    --size-only \
    --delete \
    --exclude "*.*" \
    --include "*.html" \
    --cache-control max-age=${SHORT_CACHE} \
    --content-type 'text/html'

aws s3 sync site s3://${BUCKET} \
    --size-only \
    --delete \
    --cache-control max-age=${LONG_CACHE}

if [[ ! -z "${CHALLENGE_BUCKET}" ]]; then
    aws s3 cp s3://${CHALLENGE_BUCKET} s3://${BUCKET}/ \
	--recursive
fi

if [[ ! -z "${CLOUDFRONT_ID}" ]]; then
    aws cloudfront create-invalidation --distribution-id ${CLOUDFRONT_ID} --paths '/*'
fi
