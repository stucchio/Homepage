#!/bin/sh

rm -r content/blog/tags/ deploy
./pyenv/bin/hyde serve
