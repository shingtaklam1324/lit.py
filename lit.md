# Litpy Source Code

This is the annotated source code for litpy. You should be able to build this using

```shell
python3 lit.md -b
```

and it should be able to update the `lit.py` program by itself. Yay for self hosting!

```python
#!/usr/bin/env python3
import sys
```

First it needs to check whether or not a file name is actually provided

```python
if len(sys.argv) == 1:
    print("No file name provided")
    sys.exit(1)
```

Then it needs to get the file path from the args provided

```python
path = sys.argv[1]

output_file = ""

try:
    f = open(path, "r").read().split("\n")
```

Here the program begins to read through the source line by line, and only pulls out the lines which are in code blocks delimited by "\`\`\`py" or "\`\`\`python", and it will ignore code blocks for other languages

```python
    in_code_block = False
    for line in f:
        if in_code_block:
            if line == "```":
                in_code_block = False
            else:
                output_file += line + "\n"
        elif line == "```python" or line == "```py":
            in_code_block = True
```

If the file does not exist, then it will exit and tell the user that the file does not exist

```python
except FileNotFoundError:
    print("File does not exist")
    sys.exit(1)
```

If the `-b` flag is supplied, then the script will only build and not execute the code. If the flag is not supplied, then the code will only be executed and no file will be generated.

```python
if len(sys.argv) > 2:
    if "-b" in sys.argv:
        output_path = path.split(".")[0] + ".py"
        open(output_path, "w+").write(output_file)
```

The `-r` flag can be used to run the program, so that the program can be ran and saved, using `-r -b`

```python
    if "-r" in sys.argv:
        exec(output_file)
```

Finally, it just executes the python source code, so `lit.py` can be used in place of `python`, except the python flags are not supported as of right now

```python
else:
    exec(output_file)
```