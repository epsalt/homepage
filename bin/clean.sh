#!bin/bash

find ./site -mindepth 1 ! -regex '^./site/dist\(/.*\)?' -delete
