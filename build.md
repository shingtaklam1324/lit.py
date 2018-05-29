# Build Script for Lit.py

Glob imports. Subprocess is used to get the exit code for stage 2, os is used
to execute commands, sys is for stderr.

```python
from subprocess import Popen, PIPE
from os import system
from sys import stderr
```

Back up the current version to be used if the build fails

```python
system("cp bin/lit.py bin/lit.py.bk")
```

## Stages

| Stage | Description                                                                                            |
| ----- | ------------------------------------------------------------------------------------------------------ |
| 0     | Old version                                                                                            |
| 1     | Generated using the old version using the new code, to check that the source is valid                  |
| 2     | Generated using the new version using the new code, to check that the changes in code are valid syntax |
| 3     | Generated using the new version using the new code, to check the changes in algorithm are valid        |

Use the current version to generate the next version using the source.
This stage shouldn't fail as it is using a known good version of the toolchain.

```python
system("./bin/lit.py bin/lit.md --no-exec")
```

Get the exit code from the stage. If the stage is invalid and invalid python code is
generated, then this stage would fail, as the new version cannot parse/generate
valid source.

```python
def stage():
    process = Popen(["./bin/lit.py", "bin/lit.md", "--no-exec"], stdout=PIPE)
    exit_code = process.wait()
```

If the program fails, then revert to the known good version, and exit with code
1.

```python
    if exit_code != 0:
        print("Build failed, reverting to previous version")
        system("mv bin/lit.py.bk bin/lit.py")
        exit(1)
```

Step through stage 2 and 3

```python
stage()
stage()
```

If nothing has gone wrong, then the old version can be deleted.

```python
print("Build Successful, deleting backup")
system("rm bin/lit.py.bk")

```