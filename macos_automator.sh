#!/bin/zsh

for f in "$@"
do
	script=/Users/snoway/Documents/Businesses/Code/github/kicad_gost_2.701_2008/main.py
  /Users/snoway/.pyenv/shims/python $script "$f"
done