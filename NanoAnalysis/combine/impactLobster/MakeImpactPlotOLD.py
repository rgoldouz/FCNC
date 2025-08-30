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
    Exclude =''
    WCs = ["ctpF", "ctlSF", "cteF", "ctlF", "ctlTF", "ctZF", "cptF", "cpQMF", "ctAF", "cQeF", "ctGF", "cQlMF"]
    WCnames = ["k_" + wc for wc in WCs]
    if len(FrozenSys)>0:
        Exclude =' --freezeParameters ' + (','.join(FrozenSys))
    os.system(f"cp ../CombinedFilesFCNC_v2/model_test_{Sig}.root .")
    os.system(f"cp ../CombinedFilesFCNC_v2/higgsCombine_initialFit_EFTFCNC{Sig}Float.MultiDimFit.mH125.root .")
    joined = ",".join(k for k in WCnames)
#    Nuisance = []
#    f = ROOT.TFile.Open(f"../CombinedFilesFCNC_v2/model_test_{Sig}.root")  # Replace with your actual file
#    w = f.Get("w")  # Replace "w" with your actual workspace name
#    model = w.obj("ModelConfig")
#    nuis = model.GetNuisanceParameters()
#    itr = nuis.createIterator()
#    nuis_list = []
#    var = itr.Next()
#    i = 1
#    while var:
#    #    print(f"{i:2}: {var.GetName()}")
#        Nuisance.append(f"{var.GetName()}")
#        nuis_list.append(var.GetName())
#        i += 1
#        var = itr.Next()
    mypath = "/cms/cephfs/data/store/user/rgoldouz/FullProduction/combineFCNC"
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
                os.system(f"cp {full_mypath}/{nui} ./higgsCombine_paramFit_EFTFCNC{Sig}Float_{branch10.GetName()}.MultiDimFit.mH125.root")
            fi.Close()
    RunCommand1 = f"combineTool.py -M Impacts -m 125 -o Float_impacts.json -n EFTFCNC{Sig}Float -d model_test_{Sig}.root --redefineSignalPOIs {joined} --floatOtherPOIs 1  -t -1  --exclude r"
    print(RunCommand1)
    os.system(RunCommand1)
    Jobs2=[]
    for key in WCs:
        RunCommand2 = f"plotImpacts.py -i Float_impacts.json -o {key}_OthersFloat_impacts --max-pages 1 --label-size 0.03 --cms-label ,other_WCs_float --POI {key}"
        Jobs2.append(RunCommand2)
#    Parallel(n_jobs=30)(delayed(f)(i) for i in Jobs2)
####        
####    Jobs=[]
####    Jobs1=[]
####    Jobs2=[]
####    RunCommand1 = 'combineTool.py -M Impacts -m 125 -o Float_impacts.json -n Float -d ' + WorkSpace + ' --redefineSignalPOIs ' + joined + ' --floatOtherPOIs 1  -t -1  --exclude r'
####    os.system(RunCommand1)
####    for key, value in ranges.items():
####        new_WCs = [wc for wc in WCs if wc != key]
####        RunCommand1 = 'combineTool.py -M Impacts -m 125 -o ' + key + '_impacts.json -n Float -d ' + WorkSpace + ' --redefineSignalPOIs ' + joined + ' --floatOtherPOIs 1  -t -1  --exclude r,'
####        RunCommand2 = 'plotImpacts.py -i ' + key + '_impacts.json -o OthersFixed_' + key + '_impacts --label-size 0.03 --cms-label ,other_WCs_float'
#####        Jobs1.append(RunCommand1)
#####        Jobs2.append(RunCommand2)
#####        RunCommand1 = 'combineTool.py -M Impacts -m 125 -o ' + key + 'OF_impacts.json -n Float -d ' + WorkSpace + ' --redefineSignalPOIs ' + key + ' --floatOtherPOIs 1 -t -1 ' + Exclude 
#####       RunCommand2 = 'plotImpacts.py -i ' + key + 'OF_impacts.json -o OthersFloat_' + key + '_impacts --label-size 0.03 --cms-label ,other_WCs_float'
#####       RunCommand3 = 'plotImpacts.py -i OF_impacts.json -o OthersFloat_' + key + '_onlySys_impacts --label-size 0.03 --cms-label ,other_WCs_float' + ' --POI ' + key
#####        print RunCommand2
#####        Jobs1.append(RunCommand1)
#####        Jobs2.append(RunCommand2)
#####        Jobs2.append(RunCommand3)
#####    Jobs1.append('combineTool.py -M Impacts -m 125 -o OF_impacts.json -n Float -d ' + WorkSpace + ' --redefineSignalPOIs ' + (','.join(Couplings)) + ' --floatOtherPOIs 1 -t -1 ' + Exclude)
####        RunCommand2 = 'plotImpacts.py -i Float_impacts.json -o '  + key +'_OthersFloat_impacts --max-pages 1 --label-size 0.03 --cms-label ,other_WCs_float --POI ' + key
####        Jobs2.append(RunCommand2)
#####    print 'combineTool.py -M Impacts -m 125 -o OF_impacts.json -n Float -d ' + WorkSpace + ' --redefineSignalPOIs ' + (','.join(Couplings)) + ' --floatOtherPOIs 1 -t -1 ' + Exclude
#####    Parallel(n_jobs=30)(delayed(f)(i) for i in Jobs1)
####    Parallel(n_jobs=30)(delayed(f)(i) for i in Jobs2)
