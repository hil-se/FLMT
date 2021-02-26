import pytest
import sys
import os
from io import StringIO
from shutil import rmtree

if __name__ == "__main__":

    path = sys.argv[1]

    original_output = sys.stdout
    sys.stdout = StringIO()
    exit_code = pytest.main(['-rfEpP', '--rootdir=' + path, path])
    output = sys.stdout.getvalue()
    sys.stdout.close()
    sys.stdout = original_output
    result = []
    for line in output.split('\n'):
        break_line = line.split()
        if break_line and (break_line[0] == "FAILED" or break_line[0] == "ERROR"):
            result.append(os.path.realpath(break_line[1].split("::")[0]))

    rmtree(os.path.join(path, ".pytest_cache"))
    print(" ".join(result))