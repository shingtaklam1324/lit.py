# Lit.py source code

This file contains the source code for the program, written in the literate
programming style. To update the program, use `lit.py build.md` and it
should update itself.

Glob imports. `sys` is used for the arguments, `argparse` parses them, and `os`
is used to execute other language's files

```python
#!/usr/bin/env python3
import sys
import argparse
import os
```

First a new argument parser needs to be created. This takes in one positional
argument, the path of the file being parsed, and two flags, `--no-exec` which 
is used to tell `lit.py` to not run the output, and `--no-build` which can be
used to not create an output file for Python source, as the program can execute
it directly.

```python
parser = argparse.ArgumentParser(description="Literate Programming")
parser.add_argument('PATH')
parser.add_argument('--no-exec', action="store_false", dest="run")
parser.add_argument('--no-build', action="store_false", dest="build")
res = parser.parse_args(sys.argv[1:])

path = res.PATH
```

Here are the default settings for the program to use, and the `output_file`,
which stores the actual code.

```python
output_file = ""
lang = "python"
ext = "py"
run = res.run
build = res.build
interpreter = None
```

The program then tries to read the config file, given in `cfg.py` in the same
directory as the input file. It should contain the values like above, only with
the language specific settings. The `output_file` can be used to add a header to
the code which is prepended to the output program.

`run` and `build` can be used to specify the default behaviour for the
code, whether it is ran/built or not.

```python
try:
    f = open("cfg.py").read()
    exec(f)
except FileNotFoundError:
    print("No config file found, using default")
```

The input from the flags will override the config input. So now it is going to
process that.

| Flags | Config | Output |
| ----- | ------ | ------ |
| 0     | 0      | 0      |
| 0     | 1      | 0      |
| 1     | 0      | 0      |
| 1     | 1      | 1      |

```python
run = run and res.run
build = build and res.build
```

Here the program reads the input file line by line. It is currently able to read
markdown files using code blocks labelled with either the `lang` name or the `ext`.
So for example, it can recognise both `py` and `python`.

```python
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
```

If the user tells the program to run the output, but not build, and the language
is not python, that is an error

```python
if run and not build and interpreter is None:
    print("Cannot use exec and --no-build for {} files, perhaps specify an interpreter?".format(lang), file=sys.stderr)
```

If the user does not specify the flags, then the default is to build and run
the output file.

```python
if build:
    output_path = path.split(".")[0] + "." + ext
    open(output_path, "w+").write(output_file)

if run:
    if lang == "python":
        exec(output_file)
    else:
        os.system("{} {}".format(interpreter, output_path))
```