import math
import gc
import sys
import numpy as np
import copy
import os
import subprocess

command = "lobster status Lobster_Analysis.py"  # the shell command
process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)

#Launch the shell command:
output, error = process.communicate()

fileList = error.split('\n')
text ='rm -rf '
for F in fileList:
    if 'Analysis' in F:
        n=F.count("100.0")
        if n==0:
            text += F.split()[0]
            text += ' '
            print F.split()[0]
print text

