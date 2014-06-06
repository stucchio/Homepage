#!/bin/sh

rm -r output
pelican content -s publishconf.py
# Minify stuff
find output/ -name '*.css' -or -name '*.js' | xargs -I filename yui-compressor filename -o filename.min
find output/ -name '*.min' | sed s/\\.min// | xargs -I filename mv filename.min filename
# Compress
find output/ -name '*.css' -or -name '*.js' -or -name '*.html' | xargs -I filename gzip -n -9 "filename"
find output/ -name '*.gz' | sed s/\\.gz// | xargs -I filename mv "filename.gz" "filename"

# Optimize
find output/ -name '*.jpg' | xargs -I filename jpegoptim --strip-all filename

#Upload
s3cmd -c s3cfg --exclude '*' --include '*.html' --include '*.css' --include '*.js' --add-header='Content-Encoding:gzip' sync output/index.html s3://www.chrisstucchio.com/index.html
s3cmd -c s3cfg --exclude '*' --include '*.html' --include '*.css' --include '*.js' --add-header='Content-Encoding:gzip' sync output/* s3://www.chrisstucchio.com
s3cmd -c s3cfg --exclude '*.html' --exclude '*.css' --exclude '*.js' sync output/* s3://www.chrisstucchio.com

s3cmd -c s3cfg --exclude '*' --include '*.html' --include '*.css' --include '*.js' --add-header='Content-Encoding:gzip' sync output/* s3://chrisstucchio.com
s3cmd -c s3cfg --exclude '*.html' --exclude '*.css' --exclude '*.js' sync output/* s3://chrisstucchio.com

#s3cmd -c s3cfg --exclude '*' --include '*.html' --include '*.css' --include '*.js' --add-header='Content-Encoding:gzip' sync output/* s3://cs-blog-preview
#s3cmd -c s3cfg --exclude '*.html' --exclude '*.css' --exclude '*.js' sync output/* s3://cs-blog-preview

rm -r output
