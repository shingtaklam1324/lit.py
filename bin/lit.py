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
run = res.run
build = res.build
interpreter = None
try:
    f = open("cfg.py").read()
    exec(f)
except FileNotFoundError:
    print("No config file found, using default")
run = run and res.run
build = build and res.build
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
    print("{} does not exist".format(path), file=sys.stderr)
    sys.exit(1)
if run and not build and interpreter is None:
    print("Cannot use exec and --no-build for {} files, perhaps specify an interpreter?".format(lang), file=sys.stderr)
if build:
    output_path = path.split(".")[0] + "." + ext
    open(output_path, "w+").write(output_file)

if run:
    if lang == "python":
        exec(output_file)
    else:
        os.system("{} {}".format(interpreter, output_path))
