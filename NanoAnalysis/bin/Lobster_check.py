import subprocess
import sys
import os

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
text += '    t1->Loop("' + val[0]+'", "' + val[1] + '" , "'+ val[2] + '" , "'+ val[3] + '" , "'+ val[4] + '" , ' + val[5] + ' , '+ val[6] + ' , '+ val[7] + ' , '+ val[8] + ' , '+ val[9] + ' , '+ val[10] +', t1);\n'
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
os.system('mv temp.txt MyAnalysis.h')
os.system('source /afs/crc.nd.edu/user/r/rgoldouz/FCNC/NanoAnalysis/RestFrames/setup_RestFrames.sh') 
os.environ["CPATH"] = "/afs/crc.nd.edu/user/r/rgoldouz/FCNC/NanoAnalysis/RestFrames/include"
os.system('root -b -q -l libRestFrames.so.1.0.0 libCondFormatsJetMETObjects.so libcorrectionlib.so libEFTGenReaderEFTHelperUtilities.so libmain.so main.C')
