#!/bin/sh

rm -r content/blog/tags/ deploy
hyde gen
# Minify stuff
find deploy/media/ -name '*.css' -or -name '*.js' | xargs -I filename yui-compressor filename -o filename.min
find deploy/media/ -name '*.min' | sed s/\\.min// | xargs -I filename mv filename.min filename
# Compress
find deploy/media/ -name '*.css' -or -name '*.js' | xargs gzip -9
find deploy/media/ -name '*.gz' | sed s/\\.gz// | xargs -I filename mv filename.gz filename

#Upload
s3cmd -c s3cfg sync deploy/* s3://www.chrisstucchio.com
#Upload media with cache headers
s3cmd -c s3cfg --add-header='Cache-Control:max-age=604800, public' --add-header='Content-Encoding:gzip' put --recursive deploy/media/* s3://www.chrisstucchio.com/media/

#Repeat for non-www
s3cmd -c s3cfg sync deploy/* s3://chrisstucchio.com
s3cmd -c s3cfg --add-header='Cache-Control:max-age=604800, public' --add-header='Content-Encoding:gzip' put --recursive deploy/media/* s3://chrisstucchio.com/media/
rm -r deploy
