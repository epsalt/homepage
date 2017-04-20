#!usr/bin/env bash
rm -r site/*
cp -r static/* site
python3 site_generator.py
