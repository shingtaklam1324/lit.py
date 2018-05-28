#!/usr/bin/env python3
import sys
if len(sys.argv) == 1:
    print("No file name provided")
    sys.exit(1)
path = sys.argv[1]

output_file = ""

try:
    f = open(path, "r").read().split("\n")
    in_code_block = False
    for line in f:
        if in_code_block:
            if line == "```":
                in_code_block = False
            else:
                output_file += line + "\n"
        elif line == "```python" or line == "```py":
            in_code_block = True
except FileNotFoundError:
    print("File does not exist")
    sys.exit(1)
if len(sys.argv) > 2:
    if "-b" in sys.argv:
        output_path = path.split(".")[0] + ".py"
        open(output_path, "w+").write(output_file)
    if "-r" in sys.argv:
        exec(output_file)
else:
    exec(output_file)
