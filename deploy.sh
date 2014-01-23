#!/bin/sh

rm -r content/blog/tags/ deploy
hyde gen
s3cmd -c s3cfg sync deploy/* s3://www.chrisstucchio.com
s3cmd -c s3cfg --add-header='Cache-Control:max-age=604800, public' put --recursive deploy/media/* s3://www.chrisstucchio.com/media/
s3cmd -c s3cfg sync deploy/* s3://chrisstucchio.com
s3cmd -c s3cfg --add-header='Cache-Control:max-age=604800, public' sync deploy/media/* s3://chrisstucchio.com/media/
rm -r deploy
