import os
import shutil
import subprocess
import multiprocessing

# List of TMVA macro files to run
macro_files = [
    "TMVAClassification_TU_3lonZ.C",
    "TMVAClassification_TC_2lss.C",
    "TMVAClassification_TC_3loffZ.C",
    "TMVAClassification_TU_3loffZ.C",
    "TMVAClassification_TC_3lonZ.C",
    "TMVAClassification_TU_2lss.C"
]

base_dir = os.getcwd()

def run_macro(macro_file):
    tmp_dir = os.path.join(base_dir, "tmp_" + os.path.splitext(macro_file)[0])
    if not os.path.exists(tmp_dir):
        os.makedirs(tmp_dir)

    # Copy macro to temp dir
    shutil.copy(os.path.join(base_dir, macro_file), tmp_dir)

    # Run macro in temp dir
    cmd = 'root -l -q {}'.format(macro_file)
    try:
        subprocess.check_call(cmd, shell=True, cwd=tmp_dir)
        print("Finished: {}".format(macro_file))
    except subprocess.CalledProcessError as e:
        print("Error in {}: {}".format(macro_file, e))

    # Optional: copy TMVA.root back to main dir with unique name
    # out_file = os.path.join(tmp_dir, "TMVA.root")
    # if os.path.exists(out_file):
    #     shutil.copy(out_file, os.path.join(base_dir, macro_file + ".root"))

if __name__ == "__main__":
    pool = multiprocessing.Pool(processes=6)
    pool.map(run_macro, macro_files)
    pool.close()
    pool.join()
