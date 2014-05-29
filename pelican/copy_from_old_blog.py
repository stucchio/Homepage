import os
import yaml
import shutil
import re

def read_metadata(filename):
    f = open(filename).read()
    empty, metadata_str, content = f.split("---\n", 2)
    metadata = yaml.load(metadata_str)
    return (metadata, content)

def _uses_mathjax(content):
    return (content.find('$$') > 0) or (content.find('$@') > 0)


_to_strip = ['{% block tailjavascript %}', '{% endblock %}', '{% mark excerpt -%}', '{% mark excerpt %}', '{%- endmark %}', '{% raw %}', '{% endraw %}']
def _process_content(content):
    for s in _to_strip:
        content = content.replace(s, '')
    # Replace /blog/foo/test.png with /blog_media/foo/test.png
    content = re.sub('\[([^\]]*)\]\(/blog/([^\)]+)([^(html)\)])\)', r"[\1](/blog_media/\2\3)", content)
    for i in range(5):
        content = re.sub('<img src="(/blog/([^\)]+)([^(html)\)]))"\s*>', r'<img src="/blog_media/\2\3\">', content)
    return content

def transfer_blogpost(filename, metadata, content):
    filename = filename.replace(".html", ".md")
    with open(filename, 'w') as f:
        header = """title: """ + metadata['title'] + """
date: """ + metadata['created'].strftime("%Y-%m-%d %H:%M") + """
category: blog
author: Chris Stucchio
"""
        if len(metadata.get('tags', [])) > 0:
            header = header + "tags: " + ", ".join(metadata.get('tags', [])) + "\n"
        if _uses_mathjax(content):
            header = header + "mathjax: true\n"
        if metadata.has_key("remoteurl"):
            header = header + "remoteurl: " + metadata['remoteurl'] + "\n"

        header = header + "\n\n"
        f.write(header)

        content = _process_content(content)
        f.write(content)

def _split_path(dir):
    return dir.replace("../content/blog/", '')

if __name__=="__main__":
    #Remove tags
    try:
        shutil.rmtree("../content/blog/tags")
    except OSError:
        pass

    for d in ['work', 'pubs', 'media']:
        destdir = os.path.join("content", d)
        if os.path.exists(destdir):
            shutil.rmtree(destdir)
        shutil.copytree(os.path.join("../content/", d), destdir)

    for (dir, arg, filenames) in os.walk("../content/blog/"):
        for filename in filenames:
            fullpath = os.path.join(dir, filename)
            if (fullpath[-4:] == "html") and (not filename.endswith("index.html")):
                metadata, content = read_metadata(fullpath)
                transfer_blogpost(os.path.join("content", filename), metadata, content)
            else:
                if filename.endswith(".xml"):
                    continue
                newdir = os.path.join("content/blog_media/", _split_path(dir))
                try:
                    os.makedirs(newdir)
                except OSError:
                    pass
                shutil.copyfile(os.path.join(dir, filename), os.path.join(newdir, filename))
