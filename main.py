print("This is test *****")
import os
import subprocess
print(os.getcwd())
print(subprocess.getoutput("ls -l /"))
print(subprocess.getoutput("ls -la"))

import os
import re
import sys
print('sys args->',sys.argv)
os.chdir("/kedro-poc/test_repo/")
from kedro.framework.cli import main
main()
