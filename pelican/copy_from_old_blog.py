import os
import yaml
import shutil

def read_metadata(filename):
    f = open(filename).read()
    empty, metadata_str, content = f.split("---\n", 2)
    metadata = yaml.load(metadata_str)
    return (metadata, content)


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
                print read_metadata(fullpath)[0]
