#!/bin/sh

rm -r output cache
rm content/*~

pelican content -s publishconf.py
# Minify stuff
find output/ -name '*.css' -or -name '*.js' | xargs -I filename yui-compressor filename -o filename.min
find output/ -name '*.min' | sed s/\\.min// | xargs -I filename mv filename.min filename
# Compress
find output/ -name '*.css' -or -name '*.js' -or -name '*.html' | xargs -I filename gzip -n -9 "filename"
find output/ -name '*.gz' | sed s/\\.gz// | xargs -I filename mv "filename.gz" "filename"

# Optimize
find output/ -name '*.jpg' | xargs -I filename jpegoptim --strip-all filename
rm -r output/feeds

#Upload
echo "Uploading html"
s3cmd -c s3cfg --exclude '*' --include '*.html' --mime-type="text/html"  --add-header='Content-Encoding: gzip' --add-header='Cache-Control: max-age=259200' sync output/* s3://www.chrisstucchio.com/
echo "Uploading css"
s3cmd -c s3cfg --exclude '*' --include '*.css'  --mime-type="text/css" --add-header='Content-Encoding: gzip' --add-header='Cache-Control: max-age=259200'  sync output/* s3://www.chrisstucchio.com/
echo "Uploading javascript"
s3cmd -c s3cfg --exclude '*' --include '*.js'   --mime-type="text/javascript" --add-header='Content-Encoding: gzip' --add-header='Cache-Control: max-age=259200' sync output/* s3://www.chrisstucchio.com/
echo "Uploading everything else"
s3cmd -c s3cfg --exclude '*.html' --exclude '*.css' --exclude '*.js' sync output/ s3://www.chrisstucchio.com/
#s3cmd -c s3cfg --exclude '*' --include '*.html' --include '*.css' --include '*.js' --add-header='Content-Encoding: gzip' sync output/* s3://www.chrisstucchio.com

#s3cmd -c s3cfg --exclude '*' --include '*.html' --include '*.css' --include '*.js' --add-header='Content-Encoding: gzip' sync output/* s3://chrisstucchio.com
#s3cmd -c s3cfg --exclude '*.html' --exclude '*.css' --exclude '*.js' sync output/* s3://chrisstucchio.com

curl --verbose https://www.cloudflare.com/api_json.html -d 'a=fpurge_ts' -d "tkn=`cat cloudflare-key`" -d 'email=stucchio@gmail.com' -d 'z=chrisstucchio.com'  -d 'v=1'

rm -r output
