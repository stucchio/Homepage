#!/bin/sh

rm -r content/blog/tags/ deploy
hyde gen
# Minify stuff
find deploy/media/ -name '*.css' -or -name '*.js' | xargs -I filename yui-compressor filename -o filename.min
find deploy/media/ -name '*.min' | sed s/\\.min// | xargs -I filename mv filename.min filename
# Compress
find deploy/ -name '*.css' -or -name '*.js' -or -name '*.html' | xargs -I filename gzip -n -9 "filename"
find deploy/ -name '*.gz' | sed s/\\.gz// | xargs -I filename mv "filename.gz" "filename"

# Optimize
find deploy/ -name '*.jpg' | xargs -I filename jpegoptim --strip-all filename

#Upload
s3cmd -c s3cfg --exclude '*' --include '*.html' --include '*.css' --include '*.js' --add-header='Content-Encoding:gzip' sync deploy/* s3://www.chrisstucchio.com
s3cmd -c s3cfg --exclude '*.html' --exclude '*.css' --exclude '*.js' sync deploy/* s3://www.chrisstucchio.com

s3cmd -c s3cfg --exclude '*' --include '*.html' --include '*.css' --include '*.js' --add-header='Content-Encoding:gzip' sync deploy/* s3://chrisstucchio.com
s3cmd -c s3cfg --exclude '*.html' --exclude '*.css' --exclude '*.js' sync deploy/* s3://chrisstucchio.com


rm -r deploy
