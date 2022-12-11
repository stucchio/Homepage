#!/bin/bash

OUTPUTDIR=/tmp/pelican_output

rm -r $OUTPUTDIR
rm -r cache
rm content/*~

pelican content -s publishconf.py  -o $OUTPUTDIR
if [ $? -ne 0 ]; then
    echo "Error - could not run pelican"
    exit -1;
else
    echo "Finished running pelican, output in $OUTPUTDIR"
fi

# Minify stuff
find $OUTPUTDIR/ -name '*.css' -or -name '*.js' | xargs -I filename yui-compressor filename -o filename.min
find $OUTPUTDIR/ -name '*.min' | sed s/\\.min// | xargs -I filename mv filename.min filename
# Compress
find $OUTPUTDIR/ -name '*.css' -or -name '*.js' -or -name '*.html' | xargs -I filename gzip -n -9 "filename"
find $OUTPUTDIR/ -name '*.gz' | sed s/\\.gz// | xargs -I filename mv "filename.gz" "filename"

# Optimize
find $OUTPUTDIR/ -name '*.jpg' | xargs -I filename jpegoptim --strip-all filename
rm -r $OUTPUTDIR/feeds

#Upload
echo "Uploading html"
s3cmd -c s3cfg --exclude '*' --include '*.html' --mime-type="text/html"  --add-header='Content-Encoding: gzip' --add-header='Cache-Control: max-age=259200' sync $OUTPUTDIR/ s3://www.chrisstucchio.com/
echo "Uploading css"
s3cmd -c s3cfg --exclude '*' --include '*.css'  --mime-type="text/css" --add-header='Content-Encoding: gzip' --add-header='Cache-Control: max-age=604800'  sync $OUTPUTDIR/ s3://www.chrisstucchio.com/
echo "Uploading javascript"
s3cmd -c s3cfg --exclude '*' --include '*.js'   --mime-type="text/javascript" --add-header='Content-Encoding: gzip' --add-header='Cache-Control: max-age=604800' sync $OUTPUTDIR/ s3://www.chrisstucchio.com/
echo "Uploading everything else"
s3cmd -c s3cfg --exclude '*.html' --exclude '*.css' --exclude '*.js' --add-header='Cache-Control: max-age=604800' sync $OUTPUTDIR/ s3://www.chrisstucchio.com/

#s3cmd -c s3cfg --exclude '*' --include '*.html' --include '*.css' --include '*.js' --add-header='Content-Encoding: gzip' sync $OUTPUTDIR/* s3://www.chrisstucchio.com

#s3cmd -c s3cfg --exclude '*' --include '*.html' --include '*.css' --include '*.js' --add-header='Content-Encoding: gzip' sync $OUTPUTDIR/* s3://chrisstucchio.com
#s3cmd -c s3cfg --exclude '*.html' --exclude '*.css' --exclude '*.js' sync $OUTPUTDIR/* s3://chrisstucchio.com

#curl --verbose https://www.cloudflare.com/api_json.html -d 'a=fpurge_ts' -d "tkn=`cat cloudflare-key`" -d 'email=stucchio@gmail.com' -d 'z=chrisstucchio.com'  -d 'v=1'

curl -X POST "https://api.cloudflare.com/client/v4/zones/`cat cloudflare-zone`/purge_cache" \
     -H "X-Auth-Email: stucchio@pm.me" \
     -H "X-Auth-Key: `cat cloudflare-key`" \
     -H "Content-Type: application/json" \
     --data '{"purge_everything":true}'

rm -r $OUTPUTDIR
