#!usr/bin/env bash

rm -r site/*
cp -r static/. site
python3 bin/generator.py
