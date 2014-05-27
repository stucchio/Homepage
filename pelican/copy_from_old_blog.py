import os
import yaml
import shutil

def read_metadata(filename):
    f = open(filename).read()
    empty, metadata_str, content = f.split("---\n", 2)
    metadata = yaml.load(metadata_str)
    return (metadata, content)

def _uses_mathjax(content):
    return (content.find('$$') > 0) or (content.find('$@') > 0)

def write_file(filename, metadata, content):
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

        header = header + "\n\n"
        f.write(header)

        content = content.replace("{% mark excerpt -%}", "")
        content = content.replace("{% mark excerpt %}", "")
        content = content.replace("{%- endmark %}", "")
        f.write(content)

def exclude_filepath(filename):
    if filename[-4:] != "html":
        return True
    if filename.endswith("index.html"):
        return True
    return False


if __name__=="__main__":
    #Remove tags
    try:
        shutil.rmtree("../content/blog/tags")
    except OSError:
        pass

    for (dir, arg, filenames) in os.walk("../content/blog/"):
        for filename in filenames:
            fullpath = os.path.join(dir, filename)
            if exclude_filepath(fullpath):
                continue
            if fullpath[-4:] == "html":
                metadata, content = read_metadata(fullpath)
                write_file(os.path.join("content", filename), metadata, content)
