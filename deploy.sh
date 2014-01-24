#!/bin/sh

rm -r content/blog/tags/ deploy
hyde gen
# Minify stuff
find deploy/media/ -name '*.css' -or -name '*.js' | xargs -I filename yui-compressor filename -o filename.min
find deploy/media/ -name '*.min' | sed s/\\.min// | xargs -I filename mv filename.min filename
# Compress
find deploy/ -name '*.css' -or -name '*.js' -or -name '*.html' | xargs -I filename gzip -9 "filename"
find deploy/ -name '*.gz' | sed s/\\.gz// | xargs -I filename mv "filename.gz" "filename"

# Optimize
find deploy/ -name '*.jpg' | xargs -I filename jpegoptim --strip-all filename

#Upload
s3cmd -c s3cfg --exclude '*.html' --exclude '*.css' --exclude '*.js' sync deploy/* s3://www.chrisstucchio.com
#Upload media with cache headers
find deploy/ -name '*.css' -or -name "*.js" -or -name "*.html" | sed s/^deploy\\/// |xargs -I filename s3cmd -c s3cfg --add-header='Content-Encoding:gzip' put deploy/filename s3://www.chrisstucchio.com/filename

#Repeat for non-www
s3cmd -c s3cfg --exclude '*.html' --exclude '*.css' --exclude '*.js' sync deploy/* s3://chrisstucchio.com
#Upload media with cache headers
find deploy/ -name '*.css' -or -name "*.js" -or -name "*.html" | sed s/^deploy\\/// |xargs -I filename s3cmd -c s3cfg --add-header='Content-Encoding:gzip' put deploy/filename s3://chrisstucchio.com/filename


rm -r deploy
