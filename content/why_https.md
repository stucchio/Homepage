title: Why my blog is now HTTPS, and why yours should be too
date: 2014-12-15 12:00
author: Chris Stucchio
nolinkback: true
tags: https, advertising, spam

![stupid ad](|filename|blog_media/2014/why_https/AB-binani.jpeg)

It was a stupid advertisement like the one you see above that made me realize: I need to be on HTTPS. Seeing Amitabh Bachchan hawking life insurance or soap is an everyday occurrence. But what was surprising about this patricular ad was that it appeared **on my blog**. This is quite odd - I didn't put any advertisements on my blog, except for a few affiliate links for books I've personally purchased. Wondering if I'd been hacked, I resolved to investigate further when I got home.

Weirdly, the advertisement appeared only on my phone; it wasn't present on the desktop version of my site. Curious, I tethered my computer to my phone, and sure enough, my blog had an ad for shaadi.com on it. And when I switched my phone to use wifi rather than mobile data, the ad vanished. Apparently Idea (my mobile carrier) is inserting advertisements into unsecured webpages, including mine.

This is a problem. Among other things, my blog is partially used for advertising myself, and I do not want to be associated with the content of remnant ads.

![stupid ad](/blog_media/2014/why_https/stupid_wtf.jpg)

We all know the way forward: HTTPS. It was time to switch. And it's probably time for you to switch too, unless you want your visitors browsing habits being tracked and seeing stupid advertisements on **your page**.

Luckily cloudflare had just made HTTPS a free feature for everyone, so it wasn't costly for me to do. Thanks [Cloudflare](https://cloudflare.com)!

# How to do it

It was actually quite simple for me to switch.

The first thing I needed to do was change link types from http to https. This was mostly just a search and replace.

The second thing I needed to do was alter a few S3 headers (my blog is hosted on amazon) so as not to confuse [cloudflare](https://cloudflare.com). Specifically:

```bash
s3cmd -c s3cfg --exclude '*' --include '*.html' --mime-type="text/html"  --add-header='Content-Encoding: gzip' --add-header='Cache-Control: max-age=259200' sync output/* s3://www.chrisstucchio.com/
s3cmd -c s3cfg --exclude '*' --include '*.css'  --mime-type="text/css" --add-header='Content-Encoding: gzip' --add-header='Cache-Control: max-age=259200'  sync output/* s3://www.chrisstucchio.com/
s3cmd -c s3cfg --exclude '*' --include '*.js'   --mime-type="text/javascript" --add-header='Content-Encoding: gzip' --add-header='Cache-Control: max-age=259200' sync output/* s3://www.chrisstucchio.com/
s3cmd -c s3cfg --exclude '*.html' --exclude '*.css' --exclude '*.js' sync output/ s3://www.chrisstucchio.com/
```
The third thing was turning on https. To do this, go to cloudflare settings and turn on SSL. I also needed go into "Page Rules" and create a rule for `http://www.chrisstucchio.com/*` and set it to "always use HTTPS".

That was all it took. Now I don't need to worry about Idea or any other data providers inserting ads into my site. If you run a blog of your own, I encourage you to do this as well. Pervasive [man in the middle attacks](https://en.wikipedia.org/wiki/Man-in-the-middle_attack) are here; to protect you and your readers from nasty surprises, encryption is necessary.

![stupid ad](/blog_media/2014/why_https/stupid_ad3.jpg)
