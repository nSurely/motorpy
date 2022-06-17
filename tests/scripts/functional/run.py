
# some_file.py
import sys
import os

# add cwd to path
# get absolute path to this file
# get absolute path to the parent directory
# add the parent directory to the path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + "/../../motorpy")
import motorpy

def test_run_script():
    print(motorpy.__version__)


if __name__ == "__main__":
    test_run_script()
