#!make
-include site.conf

build:
	rm -r site/*
	cp -r static/. site
	python3 bin/generator.py

serve:
	python3 bin/server.py site

autoreload:
	watchmedo shell-command \
	--ignore-patterns="*/site/*" \
	-D \
	-R \
	-c 'make build'

deploy:
	aws s3 cp site s3://$(bucket_name) \
	    --recursive \
	    --exclude "*" \
	    --include "*.css" \
	    --include "*.js" \
	    --metadata-directive REPLACE \
	    --cache-control max-age=1209600

	aws s3 cp site/images s3://$(bucket_name)/images \
            --recursive \
	    --metadata-directive REPLACE \
	    --cache-control max-age=2592000

	aws s3 cp site s3://$(bucket_name)/ \
            --recursive \
	    --exclude "*.*" \
	    --exclude "rss" \
	    --include "*.html" \
	    --metadata-directive REPLACE \
	    --cache-control max-age=86400 \
	    --content-type 'text/html'

	aws s3 cp site s3://$(bucket_name) \
            --recursive \
	    --exclude "*" \
	    --include "rss" \
	    --metadata-directive REPLACE \
	    --cache-control max-age=86400 \
	    --content-type 'application/xml'

	aws s3 sync site s3://$(bucket_name) \
            --delete
