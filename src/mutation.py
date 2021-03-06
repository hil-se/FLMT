import os
import sys
import pandas as pd
from pdb import set_trace
import subprocess

class Mutate:

    def __init__(self, path):
        if os.path.exists(path):
            self.path = os.path.realpath(path)
            self.name = self.path.split("/")[-1]
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
            row = {self.name.join(test.split(self.name)[1:])[1:]: 1 if test in result else 0 for test in self.tests}
            row["Source Code"] = self.name.join(file.split(self.name)[1:])[1:]
            df.append(row)
        self.df = pd.DataFrame(df, columns = ["Source Code"]+[self.name.join(test.split(self.name)[1:])[1:] for test in self.tests])
        self.df.to_csv("../output/" + self.path.split('/')[-1]+".csv", index=False)
        return self.df


    def test(self):
        result = subprocess.run([sys.executable, "./single_pytest.py", self.path], capture_output=True, text=True)
        return set(result.stdout.split())


if __name__ == "__main__":
    path = sys.argv[1]
    runner = Mutate(path)
    df = runner.mutation_test()
    print(df)


