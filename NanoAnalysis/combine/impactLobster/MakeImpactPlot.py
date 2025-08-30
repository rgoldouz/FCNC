import datetime
import os
from os import path
import sys
import subprocess
import readline
import string
import glob
from joblib import Parallel, delayed
import ROOT 

def f(name='ABC'):
    print (name) 
#    os.chdir('impacts')
    os.system(name)
if __name__ == '__main__':
    Sig='TC'
    wf = []
    FrozenSys=[]
    processedSys=[]
    Exclude =''
    WCs = ["ctpF", "ctlSF", "cteF", "ctlF", "ctlTF", "ctZF", "cptF", "cpQMF", "ctAF", "cQeF", "ctGF", "cQlMF"]
    WCnames = ["k_" + wc for wc in WCs]
    if len(FrozenSys)>0:
        Exclude =' --freezeParameters ' + (','.join(FrozenSys))
    joined = ",".join(k for k in WCnames)
    Nuisance = []
    f = ROOT.TFile.Open(f"../CombinedFilesFCNC_v2/model_test_{Sig}.root")  # Replace with your actual file
    w = f.Get("w")  # Replace "w" with your actual workspace name
    model = w.obj("ModelConfig")
    nuis = model.GetNuisanceParameters()
    itr = nuis.createIterator()
    nuis_list = []
    var = itr.Next()
    i = 1
    while var:
    #    print(f"{i:2}: {var.GetName()}")
        Nuisance.append(f"{var.GetName()}")
        nuis_list.append(var.GetName())
        i += 1
        var = itr.Next()
    mypath = "/cms/cephfs/data/store/user/rgoldouz/FullProduction/combineFCNC"
    for coup in WCnames:
        os.system("rm *.root")
        os.system(f"cp ../CombinedFilesFCNC_v2/model_test_{Sig}.root .")
        os.system(f"cp ../CombinedFilesFCNC_v2/higgsCombine_initialFit_EFTFCNC{Sig}Float{coup}.MultiDimFit.mH125.root .")
        for entry in os.listdir(mypath):
            full_mypath = os.path.join(mypath, entry)
            if 'impact' not in entry:
                continue   
            if Sig not in entry:
                continue
            for nui in os.listdir(full_mypath):
                fi = ROOT.TFile.Open(f"{full_mypath}/{nui}")
                tree = fi.Get("limit")
                branch10 = tree.GetListOfBranches().At(10)
                if not branch10:
                    print(f"Skipping {nui}: null branch at index 10.")
                else:    
                    os.system(f"cp {full_mypath}/{nui} ./higgsCombine_paramFit_EFTFCNC{Sig}Float{coup}_{branch10.GetName()}.MultiDimFit.mH125.root")
                    processedSys.append(branch10.GetName())
                fi.Close()
        FrozenSys = [x for x in Nuisance if x not in processedSys]       
        exclude=",".join(k for k in FrozenSys) +','+ joined
        RunCommand1 = f"combineTool.py -M Impacts -m 125 -o Float{coup}_impacts{Sig}.json -n EFTFCNC{Sig}Float{coup} -d model_test_{Sig}.root --redefineSignalPOIs {coup} --floatOtherPOIs 1  -t -1  --exclude r,{exclude}"
        print(FrozenSys)
        print(RunCommand1)
        os.system(RunCommand1)
        RunCommand2 = f"plotImpacts.py -i Float{coup}_impacts{Sig}.json -o {Sig}{coup}_OthersFloat_impacts --max-pages 1 --label-size 0.03 --cms-label ,other_WCs_float --POI {coup}"
        os.system(RunCommand2)
    Jobs2=[]
#    for key in WCs:
#        RunCommand2 = f"plotImpacts.py -i Float_impacts.json -o {key}_OthersFloat_impacts --max-pages 1 --label-size 0.03 --cms-label ,other_WCs_float --POI {key}"
#        Jobs2.append(RunCommand2)
#    Parallel(n_jobs=30)(delayed(f)(i) for i in Jobs2)
