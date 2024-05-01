import os, atexit, subprocess
from os import walk, path, listdir
from subprocess import PIPE, TimeoutExpired
from difflib import unified_diff
from __types__ import *

# runner config
PROBLEM = "t9spelling"
MAIN_CLASS = "Main"

# grader config
FAIL_FAST = True
PRINT_DIFF = True
ALLOW_TLE = True
TLE_TIMEOUT_SECS = 0.5

walk2 = lambda: map(lambda v: (v[0].removeprefix("./"), v[2]), walk("."))

ls = lambda end: filter(lambda v: v.endswith(end), listdir())


def cleanup():
    for root, files in walk2():
        for f in files:
            if f.endswith(".class") or f.endswith(".out"):
                os.remove(path.join(root, f))


atexit.register(cleanup)


def tests(problem: str = PROBLEM) -> Iterator[tuple[str, str]]:
    basedir = problem + "_data"
    for root, fs in filter(lambda v: v[0].startswith(basedir), walk2()):
        for f in filter(lambda v: v.endswith(".in"), fs):
            input = path.join(root, f)
            answer = path.join(root, f.removesuffix(".in") + ".ans")
            assert path.isfile(input), f"File not found: {input}"
            assert path.isfile(answer), f"File not found: {answer}"
            yield input, answer


def read_file(f):
    with open(f, "r") as f:
        return f.read()


def compile_all_java(cwd=None):
    subprocess.run(["javac", *ls(".java")], cwd=cwd)


def get_diff(a, b):
    al, bl = read_file(a).splitlines(), read_file(b).splitlines()
    return list(unified_diff(al, bl, fromfile=a, tofile=b, lineterm=""))


def run(input_file, answer_file, cwd=None) -> Verdict:
    input_buffer = read_file(input_file).encode("utf8")
    with open("tmp.out", "w") as f:
        proc = subprocess.Popen(["java", MAIN_CLASS], cwd=cwd, stdin=PIPE, stdout=f)
        if ALLOW_TLE:
            try:
                proc.communicate(input=input_buffer, timeout=TLE_TIMEOUT_SECS)
            except TimeoutExpired:
                proc.kill()
                return "TLE"
        else:
            proc.communicate(input=input_buffer)
        if proc.wait(timeout=TLE_TIMEOUT_SECS) != 0:
            return "RTE"
    diff = get_diff("tmp.out", answer_file)
    if len(diff) > 0 and PRINT_DIFF:
        for line in diff:
            print(line)
        print("[tmp.out]")
        print(read_file("tmp.out"))
        print(f"[{answer_file}]")
        print(read_file(answer_file))
        return "WA"
    return "AC"


# Returns True if there is a difference
def same_logic(input_file, cwd0=None, cwd1=None) -> Verdict:
    input_buffer = read_file(input_file).encode("utf8")
    with open("0.out", "w") as f:
        proc = subprocess.Popen(["java", MAIN_CLASS], cwd=cwd0, stdin=PIPE, stdout=f)
        proc.communicate(input=input_buffer, timeout=TLE_TIMEOUT_SECS)
    with open("1.out", "w") as f:
        proc = subprocess.Popen(["java", MAIN_CLASS], cwd=cwd1, stdin=PIPE, stdout=f)
        proc.communicate(input=input_buffer, timeout=TLE_TIMEOUT_SECS)
    diff = get_diff("0.out", "1.out")
    if len(diff) > 0 and PRINT_DIFF:
        for line in diff:
            print(line)
        return False
    return True


class Verdicts:
    def __init__(self) -> None:
        self.verdicts = {}

    def add(self, verdict: Verdict):
        self.verdicts[verdict] = self.verdicts.get(verdict, 0) + 1

    def display(self):
        for k, v in self.verdicts.items():
            print(f"{k: <10}: {v}")
        total = "TOTAL"
        v = sum(self.verdicts.values())
        print(f"{total: <10}: {v}")


def evaluate(original=False):
    cwd = "__original__" if original else None
    compile_all_java(cwd=cwd)
    verdicts = Verdicts()
    for input, answer in tests():
        print(f"[{input}]", end=" ", flush=True)
        verdict = run(input, answer, cwd=cwd)
        print(verdict)
        verdicts.add(verdict)
        if verdict != "AC" and FAIL_FAST:
            break
    verdicts.display()


def compare():
    compile_all_java()
    compile_all_java(cwd="__original__")
    for input, _ in tests():
        print(f"diffing [{input}]...", end=" ", flush=True)
        if same_logic(input, cwd0="__original__"):
            print("Ok!")
        else:
            print("Nope!")
            if FAIL_FAST:
                exit(1)


def run_one(input="1.in"):
    compile_all_java()
    print(f"[{input}]")
    proc = subprocess.Popen(["java", MAIN_CLASS], stdin=PIPE)
    proc.communicate(input=read_file(input).encode("utf8"))


compare()
# run_one()
evaluate()
