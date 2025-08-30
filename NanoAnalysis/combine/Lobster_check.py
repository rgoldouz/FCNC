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

infiles = sys.argv[1:]
print("Input files:", infiles)

# ensure unlimited stack
subprocess.run(["ulimit", "-s", "unlimited"], shell=True)

for f in infiles:
    local_file = os.path.basename(f.split(':')[-1])
    # copy file locally
    subprocess.run(["cp", f.split(':')[-1], "."], check=True)
    # run the shell script
    subprocess.run(["bash", "./" + local_file], check=True)

# rename output
rootfile = f"{local_file[:-3]}.MultiDimFit.mH125.root"
subprocess.run(["mv", rootfile, "combine.root"], check=True)

## check output
#if os.path.isfile("combine.root"):
#    size = os.path.getsize("combine.root")
#    if size < 1000:
#        print("Run has some problem.")
#        sys.exit(1)
#    else:
#        print("combine.root found and looks OK.")
#        sys.exit(0)
#else:
#    print("combine.root not found!")
#    sys.exit(1)
