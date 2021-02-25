import os
import sys
from io import StringIO
import pandas as pd
from shutil import rmtree
from pdb import set_trace

class Mutate:

    def __init__(self, path):
        if os.path.exists(path):
            self.path = os.path.realpath(path)
        else:
            raise Exception("Input Path Does Not Exist.")
        self.mutated = None


    def mutate(self, file):
        self.mutated = str(file) + ".mutated"
        os.rename(file, self.mutated)

    def recover(self):
        os.rename(self.mutated, self.mutated[:-8])
        self.mutated = None

    def find_all_files(self):
        self.tests = []
        self.codes = []
        for root, dirs, files in os.walk(self.path):
            for file in files:
                if file.endswith('.py') and not file.startswith("__"):
                    full_path = os.path.join(root, file)
                    if file.startswith("test_"):
                        self.tests.append(full_path)
                    else:
                        self.codes.append(full_path)

    def mutation_test(self):
        self.find_all_files()
        df = []
        for file in self.codes:
            self.mutate(file)
            result = self.test()
            self.recover()
            row = {test: 1 if test in result else 0 for test in self.tests}
            row["Source Code"] = file
            df.append(row)
        self.df = pd.DataFrame(df, columns = ["Source Code"]+self.tests)
        return self.df


    def test(self):
        if "pytest" in sys.modules:
            sys.modules.pop("pytest")
        import pytest
        original_output = sys.stdout
        sys.stdout = StringIO()
        set_trace()
        exit_code = pytest.main(['-rfEpP', '--rootdir='+self.path, self.path])
        output = sys.stdout.getvalue()
        sys.stdout.close()
        sys.stdout = original_output
        print(output)
        result = []
        for line in output.split('\n'):
            break_line = line.split()
            if break_line and (break_line[0] == "FAILED" or break_line[0] == "ERROR"):
                result.append(os.path.realpath(break_line[1].split("::")[0]))

        rmtree(os.path.join(self.path, ".pytest_cache"))
        for root, dirs, files in os.walk(self.path):
            for dir in dirs:
                if dir == "__pycache__":
                    rmtree(os.path.join(root, dir))

        return set(result)


if __name__ == "__main__":
    try:
        path = sys.argv[1]
    except:
        path = '.'
    runner = Mutate(path)
    df = runner.mutation_test()
    print(df)


