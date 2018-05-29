#!/usr/bin/env python3
import sys
import argparse
import os
parser = argparse.ArgumentParser(description="Literate Programming")
parser.add_argument('PATH')
parser.add_argument('--no-exec', action="store_false", dest="run")
parser.add_argument('--no-build', action="store_false", dest="build")
res = parser.parse_args(sys.argv[1:])

path = res.PATH
output_file = ""
lang = "python"
ext = "py"
try:
    f = open("cfg.py").read()
    exec(f)
except FileNotFoundError:
    print("No config file found, using default")
try:
    f = open(path, "r").read().split("\n")
    in_code_block = False
    for line in f:
        if in_code_block:
            if line == "```":
                in_code_block = False
            else:
                output_file += line + "\n"
        elif line == ("```" + lang) or line == ("```" + ext):
            in_code_block = True
except FileNotFoundError:
    print("File does not exist", file=sys.stderr)
    sys.exit(1)
if res.run and not res.build and lang != "python":
    print("Cannot use exec and --no-build for", file=sys.stderr)
if res.build:
    output_path = path.split(".")[0] + "." + ext
    open(output_path, "w+").write(output_file)

if res.run:
    if lang == "python":
        exec(output_file)
    else:
        os.system("{} {}".format(lang, output_path))
