#!bin/bash

if [ -d "./site" ]; then
   find ./site -mindepth 1 ! -regex '^./site/dist\(/.*\)?' -delete
fi
