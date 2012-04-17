#!/bin/sh

rm -r content/blog/tags/ deploy
hyde gen
s3cmd -c s3cfg sync deploy/* s3://www.chrisstucchio.com
rm -r deploy
