#!/usr/bin/env zsh

python3.12 generate.py 4096
echo "compiling.."
cc main.c -o fakespeare
echo "\a\a\a"
./fakespeare

