# epsalt.ca
This repository contains the source code for [epsalt.ca][website]. The
website is a static site generated from Markdown, with Jinja2
templates, using Python 3.

## Content
Posts and other content pages are writtent in Markdown and live in the
`content` directory. YAML metadata in the page header is used to store
titles, tags, dates, and other information.

```
---
type: post
template: post
title: This is a Test Post
date: 2017-12-20 14:15:00 -0900
updated: 2018-01-01 12:30:00 -0900
url: test
tags: tests
---

This is a sentence of post content. Beautiful, beautiful content.
```

## Build
To generate the static site, run `make build`. The site will be
generated into the `site` directory.

## Preview
Run `make serve` and navigate to http://localhost:8080/ to preview.

## Deploy
Running `make deploy` syncs the site with an AWS S3 bucket. To sync to
your own bucket, set the $BUCKET environment variable in your build
environment or add `BUCKET := YOUR_S3_BUCKET` to the makefile.

## Requirements
The following Python 3 packages are required:

- Markdown
- Jinja2
- feedgen
- python-dateutil
- libsass
- watchdog (for autoreload)

The deployment script uses the [aws-cli][aws] to deploy the site to a
S3 bucket.

## License

Except where noted, all content on this website is
licensed [CC-BY][cc-by]. All code in this repo is licensed under the
terms of the GPLv3 License (see the file LICENSE.md).

[website]: http://epsalt.ca
[aws]: https://aws.amazon.com/cli/
[cc-by]: https://creativecommons.org/licenses/by/4.0/
