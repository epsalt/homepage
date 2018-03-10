#!make
-include site.conf

build:
	rm -r site/*
	cp -r static/. site
	python3 bin/generator.py

serve:
	python3 bin/server.py site

deploy:
	aws s3 sync site s3://$(bucket_name) \
	    --exclude "*" \
	    --include "*.css" \
	    --include "*.js" \
	    --metadata-directive REPLACE \
	    --cache-control max-age=1209600

	aws s3 sync site/images s3://$(bucket_name)/images \
	    --metadata-directive REPLACE \
	    --cache-control max-age=2592000

	aws s3 sync site s3://$(bucket_name)/ \
	    --exclude "*.*" \
	    --exclude "rss" \
	    --include "*.html" \
	    --metadata-directive REPLACE \
	    --cache-control max-age=86400 \
	    --content-type 'text/html'

	aws s3 sync site s3://$(bucket_name) \
	    --exclude "*" \
	    --include "rss" \
	    --metadata-directive REPLACE \
	    --cache-control max-age=86400 \
	    --content-type 'application/xml'
