from subprocess import Popen, PIPE
from os import system
from sys import stderr
system("cp bin/lit.py bin/lit.py.bk")
system("./bin/lit.py bin/lit.md --no-exec")
def stage():
    process = Popen(["./bin/lit.py", "bin/lit.md", "--no-exec"], stdout=PIPE)
    exit_code = process.wait()
    if exit_code != 0:
        print("Build failed, reverting to previous version")
        system("mv bin/lit.py.bk bin/lit.py")
        exit(1)
stage()
stage()
print("Build Successful, deleting backup")
system("rm bin/lit.py.bk")

