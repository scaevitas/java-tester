from halo import Halo
import os.path,subprocess
from subprocess import STDOUT,PIPE
import json
import re
import inquirer

loading = {
    "interval": 100,
    "frames": ['⠋', '⠙', '⠹', '⠸', '⠼', '⠴', '⠦', '⠧', '⠇', '⠏']
}

def testTemplate(motivation, stdin, expected):
    return '        {\n'+ f'            "motivation": "{motivation}",\n            "input": "{stdin}",\n            "output": "{expected}"\n'+ '        }'

def compile_java(java_file):
    subprocess.check_call(['javac', java_file])

@Halo(text=f"running test", spinner=loading, text_color="green", color="yellow")
def run_test(java_file, stdin):
    java_class,ext = os.path.splitext(java_file)
    cmd = ['java', java_class]
    proc = subprocess.Popen(cmd, stdin=PIPE, stdout=PIPE, stderr=STDOUT)
    stdout,stderr = proc.communicate(stdin.encode("utf-8"))
    output = stdout.decode("utf-8")
    return output

if __name__ == "__main__":
    if not os.path.isfile("minimal_test_set.json"):
        print("\x1b[31mcould not find json file in cwd.\x1b[0m")
        res = inquirer.prompt([inquirer.List("cnf", message="create new file?", choices=["yes", "no"])])
        if (res["cnf"] == "no"):
            exit()
        with open("minimal_test_set.json", "w") as testSet:
            r = re.compile(".*\.java")
            files = list(filter(r.match, os.listdir()))
            if (len(files)):
                res = inquirer.prompt([inquirer.List("file", message="choose file a file", choices=files)])
            else:
                print("could not find any java files in cwd")
                res = inquirer.prompt([inquirer.Text("file", message="file name")])
            testSet.write('{\n' + f'    "file": "{res["file"].replace(".java", "")}.java",\n    "tests": [\n')
            while True:
                res = inquirer.prompt([
                    inquirer.Text("motivation", message="motivation", choices=["yes", "no"]),
                    inquirer.Text("input", message="input",choices=["yes", "no"]),
                    inquirer.Text("expected", message="expected",choices=["yes", "no"])
                    ])
                testSet.write(testTemplate(res["motivation"], res["input"], res["expected"]))
                res = inquirer.prompt([inquirer.List("continue", message="continue?", choices=["yes", "no"])])
                if (res["continue"] == "no"):
                    testSet.write("\n    ]\n}")
                    break
                testSet.write(",\n")
    f = open("minimal_test_set.json")
    data = json.load(f)
    file = data["file"]
    spinner = Halo(text=f"compiling {file}", spinner=loading, text_color="green", color="yellow")
    spinner.start()
    compile_java(file)
    spinner.stop()
    print("\x1b[33mstarting tests\x1b[0m")
    score = 0
    with open("minimal_test_set.txt", "w") as logs:
        logs.write(f"Minimal test set for {file}\n\nAUTHORS:\n- Matheus Tran 1777513\n")
        for a,b in enumerate(data["tests"]):
            print(f'\x1b[34mtest {a+1}: {b["motivation"]}\x1b[0m')
            sanitize = re.compile('[\n\r \t]+$')
            out = run_test(file, b["input"])
            out = sanitize.sub("", out)
            logs.write(f"\nTEST CASE {a+1}\nmotivation  : {b['motivation']}\ninput       : {b['input']}\noutput      : {out}\n\n")
            if (out == b["output"]):
                print("\x1b[32m✔ passed\x1b[0m")
                score += 1
            else:
                print(f'\x1b[31m✖ Failed. Expected: "{b["output"]}"; got: "{out}";\x1b[0m')
        print(f"score: \x1b[33m({score}/{len(data['tests'])})\x1b[0m")