import os.path,subprocess
from subprocess import STDOUT,PIPE
import sys

args = sys.argv

def run_test(java_file, stdin):
    java_class,ext = os.path.splitext(java_file)
    cmd = ['java', java_class]
    proc = subprocess.Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    stdout,stderr = proc.communicate(stdin.encode("utf-8"))
    output = stdout.decode("utf-8").replace("\n", "")
    print(output)

run_test(args[1], args[2])