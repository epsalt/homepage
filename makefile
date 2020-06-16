#!make

build:
	rm -rf site/*
	cp -r static/. site
	pysassc scss/site.scss -s compressed > site/css/styles.min.css
	litesite config.yaml

LONG_CACHE := 86400
SHORT_CACHE := 3600

deploy:
	aws s3 sync site s3://$(BUCKET) \
		--size-only \
		--delete \
		--exclude "*" \
		--include "rss" \
		--cache-control max-age=$(LONG_CACHE) \
		--content-type 'application/xml'

	aws s3 sync site s3://$(BUCKET)/ \
		--size-only \
		--delete \
		--exclude "*.*" \
		--include "*.html" \
		--cache-control max-age=$(SHORT_CACHE) \
		--content-type 'text/html'

	aws s3 sync site s3://$(BUCKET) \
		--size-only \
		--delete \
		--cache-control max-age=$(LONG_CACHE)

challenges:
	aws s3 cp s3://$(CHALLENGE_BUCKET) s3://$(BUCKET)/ \
		--recursive

invalidate:
	aws cloudfront create-invalidation --distribution-id $(CLOUDFRONT_ID) --paths '/*'
