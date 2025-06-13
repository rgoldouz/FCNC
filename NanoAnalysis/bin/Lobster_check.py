import subprocess
import sys
import os
# Fix missing $HOME to avoid ROOT crash
if not os.environ.get("HOME"):
    tmp_home = "/tmp/" + os.environ.get("USER", "default_user")
    os.environ["HOME"] = tmp_home
    if not os.path.exists(tmp_home):
        os.makedirs(tmp_home)
os.environ["ROOTIGNOREMIMES"] = "1"


infiles = sys.argv[12:]
print infiles
val = sys.argv[1:12]
print val
text = ''
text += '    TChain* ch    = new TChain("Events") ;\n'
for fn in infiles:
    a, b = fn.split(':')
    text += '    ch ->Add("' +  b + '");\n'
text += '    MyAnalysis * t1 = new MyAnalysis(ch);\n'
text += '    t1->Analyze("' + val[0]+'", "' + val[1] + '" , "'+ val[2] + '" , "'+ val[3] + '" , "'+ val[4] + '" , ' + val[5] + ' , '+ val[6] + ' , '+ val[7] + ' , '+ val[8] + ' , '+ val[9] + ' , '+ val[10] +', t1);\n'
text += '    delete t1;'
SHNAME1 = 'main.C'
SHFILE1='#include "MyAnalysis.h"\n' +\
'int main(){\n' +\
text +\
'}'


open(SHNAME1, 'wt').write(SHFILE1)
#os.system("echo '" + SHFILE1+ "' > main.C && ls -l && cat main.C && root  -b -q -l main.so main.C && ls -l")
#os.system('echo ' + SHFILE1+ ' > main.C && ls -l && cat main.C && root -l main.so main.C && ls -l')
#os.system('cat main.C')
with open("MyAnalysis.h", "r") as input:
    with open("temp.txt", "w") as output:
        # iterate all lines from file
        for line in input:
            # if substring contain in a line then don't write it
            if "TH1EFT.h" not in line.strip("\n"):
                output.write(line)

# replace file with original name
os.system('cp temp.txt MyAnalysis.h')
#os.system('ls /afs/crc.nd.edu/user/r/rgoldouz/FCNC/NanoAnalysis')
#os.system('ls /users')
#os.system('ls /users/rgoldouz')
#os.system('ls /users/rgoldouz/FCNC')
#os.system('ls /users/rgoldouz/FCNC/NanoAnalysis')
#os.system('ls /users/rgoldouz/FCNC/NanoAnalysis/RestFrames')
#os.system('ls /users/rgoldouz/FCNC/NanoAnalysis/RestFrames/setup_RestFrames.sh')
os.system('export OMP_NUM_THREADS=1')
os.system('export MKL_NUM_THREADS=1')
os.system('export OPENBLAS_NUM_THREADS=1')
os.system('export ROOT_DISABLE_IMT=1')
os.system('source /users/rgoldouz/FCNC/NanoAnalysis/RestFrames/setup_RestFrames.sh') 
os.environ["CPATH"] = "/users/rgoldouz/FCNC/NanoAnalysis/RestFrames/include:/users/rgoldouz/FCNC/NanoAnalysis/include"
os.system('root -b -q -l libRestFrames.so.1.0.0 libJetMETCorrectionsModules.so libcorrectionlib.so libEFTGenReaderEFTHelperUtilities.so libboost_serialization.so libmain.so main.C')
os.system('hadd ANoutput.root ANoutput*')
#os.system('source /afs/crc.nd.edu/user/r/rgoldouz/FCNC/NanoAnalysis/RestFrames/setup_RestFrames.sh')
#os.environ["CPATH"] = "/afs/crc.nd.edu/user/r/rgoldouz/FCNC/NanoAnalysis/RestFrames/include:/afs/crc.nd.edu/user/r/rgoldouz/FCNC/NanoAnalysis/include"
#os.system('root -b -q -l libRestFrames.so.1.0.0 libJetMETCorrectionsModules.so libcorrectionlib.so libEFTGenReaderEFTHelperUtilities.so libboost_serialization.so libmain.so main.C')
