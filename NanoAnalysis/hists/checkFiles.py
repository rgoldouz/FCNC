import sys
import os
import subprocess
import glob
from joblib import Parallel, delayed
import math

sys.path.append('/users/rgoldouz/FCNC/NanoAnalysis/bin/')
import Files_ULall_nano

def f(name):
    os.system(name)

def check_file(keyUL, filename, base_dist):
    """Function to check the validity of a ROOT file and return results safely."""
    import ROOT  # Import ROOT inside function to avoid pickling issues
    
    dist = base_dist + 'Analysis_' + keyUL  # Ensure correct path formatting
    file_path = os.path.join(dist, filename)
    
#    print file_path  # Python 2 print statement

    file = ROOT.TFile(file_path, "READ")
    is_broken = False
    rm_command = ""

    if not file or not file.IsOpen():
        print file_path + " File is not open or does not exist."
        is_broken = True
        rm_command = 'rm -rf ' + dist + ' '
    elif file.GetNkeys() == 0:
        print file_path + " The ROOT file is empty."
        is_broken = True
        rm_command = 'rm -rf ' + dist + ' '

    H=file.Get("2los_MUpMUm_CR_1bLj_llM")
    for b in range(H.GetNbinsX()):
        content = H.GetBinContent(b+1,ROOT.WCPoint("NONE"))
        if math.isnan(content) or math.isinf(content):
            print  dist +'/'+filename+' ' + H.GetName()+"Bin content is NaN"
    file.Close()
    del file



    return (keyUL if is_broken else None, rm_command if is_broken else None)

if __name__ == '__main__':
    SAMPLES = {}
    SAMPLES.update(Files_ULall_nano.UL17)
    base_dist = "/cms/cephfs/data/store/user/rgoldouz/FullProduction/AnalysisTOPFCNC/"

    # Ensure keyUL is correctly formatted into the path
    tasks = []
    for keyUL in SAMPLES.keys():
        full_path = base_dist + 'Analysis_' + keyUL  # Construct the correct full path
        if os.path.exists(full_path) and os.path.isdir(full_path):  # Check if path exists
            for filename in os.listdir(full_path):
                tasks.append((keyUL, filename, base_dist))
        else:
            print "Warning: Directory does not exist -", full_path

    # Run in parallel with 40 jobs
    results = Parallel(n_jobs=40, backend="multiprocessing")(delayed(check_file)(keyUL, filename, base_dist) for keyUL, filename, base_dist in tasks)

    # Collect results safely
    buggySamples = [keyUL for keyUL, rm_command in results if keyUL]
    missedSamples = 'These samples have broken files. Please check and rerun the code:\n' + \
                    ''.join(rm_command for keyUL, rm_command in results if rm_command)

    print missedSamples  # Python 2 print statement
    print buggySamples
