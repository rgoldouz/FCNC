import os
from multiprocessing import Pool
import numpy as np
import ROOT

FrozenSys=[]
#WCs = ["ctp", "ctlS", "cte", "ctl", "ctlT", "ctZ", "cpt", "cpQM", "ctA", "cQe", "ctG", "cQlM"]
WCs = ["ctpF", "ctlSF", "cteF", "ctlF", "ctlTF", "ctZF", "cptF", "cpQMF", "ctAF", "cQeF", "ctGF", "cQlMF"]
WCnames = ["k_" + wc for wc in WCs]
signal=["TU","TC"]
myDir="forLobster"
os.system("mkdir " + myDir)
ngrid=200
njobs = int(ngrid/5)
# Compute chunk size (some chunks may differ by 1 if ngrid % njobs != 0)
chunk_size = ngrid // njobs
remainder = ngrid % njobs

start = 0
ran = []

for i in range(njobs):
    # distribute the remainder one by one to the first "remainder" jobs
    extra = 1 if i < remainder else 0
    end = start + chunk_size + extra - 1
    ran.append((start, end))
    start = end + 1

text = "#!/bin/bash\n"
text +="ulimit -s unlimited\n"
for Sig in signal:
    ranges = {"k_ctpF": "-1.5,1.5", "k_ctZF": "-1.0,1.0", "k_cptF": "-2,2", "k_cpQMF": "-2,2", "k_ctAF": "-1,1", "k_ctGF": "-0.4,0.4", "k_cQlMF": "-1,1" , "k_cQeF":  "-1,1", "k_ctlF":  "-1,1", "k_cteF":  "-1,1", "k_ctlSF": "-1,1", "k_ctlTF": "-0.2,0.2"}
    if Sig=="TU":
        ranges = {"k_ctpF": "-1,1", "k_ctZF": "-0.3,0.3", "k_cptF": "-1,1", "k_cpQMF": "-1,1", "k_ctAF": "-0.5,0.5", "k_ctGF": "-0.1,0.1", "k_cQlMF": "-0.2,0.2", "k_cQeF": "-0.2,0.2", "k_ctlF": "-0.2,0.2", "k_cteF": "-0.2,0.2", "k_ctlSF": "-0.2,0.2", "k_ctlTF": "-0.05,0.05"}
    for namec in WCnames:
        freeze = ",".join(k for k in WCnames if k != namec)
        paramSet = ",".join(f"{k}=0" for k in WCnames)
#        param_str = ":".join(f"{k}={v}" for k, v in ranges.items())
        paramRange = ":".join(f"{wc}=-10,10" for wc in WCnames if wc != namec) +":"+namec+'='+ranges[namec]
        os.system(f"mkdir {myDir}/oneDEFTFCNC{Sig}Frozen{namec}")
        os.system(f"mkdir {myDir}/oneDEFTFCNC{Sig}Float{namec}")
        os.system(f"mkdir {myDir}/oneDEFTFCNC{Sig}FrozenStatOnly{namec}")
        for i, (lo, hi) in enumerate(ran):
            fitFrozen_cmd = (
                f"{text}"    
                f"python3 $(which combineTool.py) -M MultiDimFit --algo=grid --points 200 --verbose 1 -m 125 -n EFTFCNC{Sig}Frozen{namec} "
                f"-d model_test_{Sig}.root --redefineSignalPOIs {namec} --setParameters r=1,{paramSet} "
                f"--setParameterRanges {paramRange} --freezeParameters r,{freeze} -t -1 "
                f"--points {ngrid} --firstPoint {lo} --lastPoint {hi} -n EFTFCNC{Sig}Frozen{namec}.POINTS.{lo}.{hi}"
        #        f"--job-mode condor --split-points 20 --sub-opts='+JobFlavour=\"workday\"' --task-name {Sig}_Frozen{namec}"
            )
            with open(f"{myDir}/oneDEFTFCNC{Sig}Frozen{namec}/higgsCombineEFTFCNC{Sig}Frozen{namec}.POINTS.{lo}.{hi}.sh", "w") as sh:
                sh.write(fitFrozen_cmd)
    
    
            fitFloat_cmd= (
                f"{text}"    
                f"python3 $(which combineTool.py) -M MultiDimFit --algo=grid --points 200 --verbose 1 -m 125 -n EFTFCNC{Sig}Float{namec} "
                f"-d model_test_{Sig}.root --redefineSignalPOIs {namec} --floatOtherPOIs=1 --setParameters r=1,{paramSet} "
                f"--setParameterRanges {paramRange} --freezeParameters r -t -1 "
                f"--points {ngrid} --firstPoint {lo} --lastPoint {hi} -n EFTFCNC{Sig}Float{namec}.POINTS.{lo}.{hi}"
    #            f"--job-mode condor --split-points 20 --sub-opts='+JobFlavour=\"workday\"' --task-name {Sig}_Float{namec}"
            )            
            with open(f"{myDir}/oneDEFTFCNC{Sig}Float{namec}/higgsCombineEFTFCNC{Sig}Float{namec}.POINTS.{lo}.{hi}.sh", "w") as sh:
                sh.write(fitFloat_cmd)
    ###
            fitFrozenStatOnly_cmd = (
                f"{text}"    
                f"python3 $(which combineTool.py) -M MultiDimFit --algo=grid --points 200 --verbose 1 -m 125 -n EFTFCNC{Sig}FrozenStatOnly{namec} "
                f"-d model_test_{Sig}.root --redefineSignalPOIs {namec} --setParameters r=1,{paramSet} "
                f"--setParameterRanges {paramRange} --freezeParameters r,{freeze},allConstrainedNuisances -t -1 "
                f"--points {ngrid} --firstPoint {lo} --lastPoint {hi} -n EFTFCNC{Sig}FrozenStatOnly{namec}.POINTS.{lo}.{hi}"
    #            f"--job-mode condor --split-points 20 --sub-opts='+JobFlavour=\"workday\"' --task-name {Sig}_Frozen{namec}StatOnly"
            )
            with open(f"{myDir}/oneDEFTFCNC{Sig}FrozenStatOnly{namec}/higgsCombineEFTFCNC{Sig}FrozenStatOnly{namec}.POINTS.{lo}.{hi}.sh", "w") as sh:
                sh.write(fitFrozenStatOnly_cmd)
    
    for w1,wc1 in enumerate(WCnames):
        for w2,wc2 in enumerate(WCnames):
            if wc1==wc2 or w2<w1:
                continue
            paramRange = ":".join(f"{wc}=-10,10" for wc in WCnames if wc != wc1 and wc != wc2) 
            paramRange = f"{paramRange}:{wc1}={ranges[wc1]}:{wc2}={ranges[wc2]}"
            os.system(f"mkdir {myDir}/twoDEFTFCNC{Sig}Float{wc1}{wc2}")
            for i, (lo, hi) in enumerate(ran):
                paramSet = ",".join(f"{k}=0" for k in WCnames)
                paramRange = ":".join(f"{wc}=-10,10" for wc in WCnames if (wc != wc1 and wc != wc2))
                paramRange = paramRange+":"+wc1+'='+ranges[wc1]+":"+wc2+'='+ranges[wc2]
                fitFloattwoD_cmd= (
                    f"{text}"    
                    f"python3 $(which combineTool.py) -M MultiDimFit --algo=grid --points 400 --verbose 1 -m 125 -n EFTFCNC{Sig}Float{wc1}{wc2} "
                    f"-d model_test_{Sig}.root --redefineSignalPOIs {wc1},{wc2} --floatOtherPOIs=1 --setParameters r=1,{paramSet} "
                    f"--setParameterRanges {paramRange} --freezeParameters r -t -1 "
                    f"--points {ngrid} --firstPoint {lo} --lastPoint {hi} -n EFTFCNC{Sig}Float{wc1}{wc2}.POINTS.{lo}.{hi}"                    
    #                 f"--job-mode condor --split-points 20 --sub-opts='+JobFlavour=\"tomorrow\"'  --sub-opts='+RequestMemory=8000' --task-name {Sig}{wc1}{wc2}"
                )
                with open(f"{myDir}/twoDEFTFCNC{Sig}Float{wc1}{wc2}/higgsCombineEFTFCNC{Sig}Float{wc1}{wc2}.POINTS.{lo}.{hi}.sh", "w") as sh:
                    sh.write(fitFloattwoD_cmd)

    allPOI = ",".join(k for k in WCnames)
    os.system(f"mkdir {myDir}/impact{Sig}")
    fitPoint = {"k_ctpF": "1.0", "k_ctZF": "0.4", "k_cptF": "1.0", "k_cpQMF": "2.0", "k_ctAF": "1.0", "k_ctGF": "0.14", "k_cQlMF": "2.0" , "k_cQeF":  "2.0", "k_ctlF":  "2.0", "k_cteF":  "2.0", "k_ctlSF": "2.0", "k_ctlTF": "0.4"}
    if Sig=="TU":
        fitPoint = {"k_ctpF": "0.7", "k_ctZF": "0.2", "k_cptF": "0.5", "k_cpQMF": "1.2", "k_ctAF": "0.5", "k_ctGF": "0.07", "k_cQlMF": "0.5", "k_cQeF": "0.5", "k_ctlF": "0.5", "k_cteF": "0.5", "k_ctlSF": "0.5", "k_ctlTF": "0.1"}    
    fitPoint_str = ",".join(f"{k}={v}" for k, v in fitPoint.items())   
    Nuisance = []
    f = ROOT.TFile.Open(f'CombinedFilesFCNC_v2/model_test_{Sig}.root')  # Replace with your actual file
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
    for i, sys in enumerate(Nuisance):
        if sys in FrozenSys:
            continue
        paramRange = ":".join(f"{wc}=-10,10" for wc in WCnames)
        impact_cmd = (
            f"{text}"    
            f"python3 $(which combineTool.py) -M MultiDimFit --algo impact --robustFit 1 -m 125 "
            f"-n _paramFit_EFTFCNC{Sig}Float_{sys} -d model_test_{Sig}.root --redefineSignalPOIs {allPOI} "
            f"-P {sys} --floatOtherPOIs 1 -t -1 --saveInactivePOI 1 --verbose 1 "
            f"--setParameters r=1,{fitPoint_str} --setParameterRanges {paramRange} "
            f"--freezeParameters r"
        )   
        with open(f"{myDir}/impact{Sig}/higgsCombine_paramFit_EFTFCNC{Sig}Float_{sys}.sh", "w") as sh:
            sh.write(impact_cmd)
    for sys, value in ranges.items():
        impact_cmd = (
            f"{text}"    
            f"python3 $(which combineTool.py) -M MultiDimFit --algo impact --robustFit 1 -m 125 "
            f"-n _paramFit_EFTFCNC{Sig}Float_{sys} -d model_test_{Sig}.root --redefineSignalPOIs {allPOI} "
            f"-P {sys} --floatOtherPOIs 1 -t -1 --saveInactivePOI 1 --verbose 1 "
            f"--setParameters r=1,{fitPoint_str} --setParameterRanges {paramRange} "
            f"--freezeParameters r"
        )
        with open(f"{myDir}/impact{Sig}/higgsCombine_paramFit_EFTFCNC{Sig}Float_{sys}.sh", "w") as sh:
            sh.write(impact_cmd)        

    info=(
        f"Before submitting lobster jobs for the nuisance scans you should run the initial fit;\n"
    )
    print (info)
    for namec in WCnames:
        info=(
            f"nohup combineTool.py -M Impacts -m 125 --doInitialFit --robustFit 1 --redefineSignalPOIs {namec} --floatOtherPOIs 1 -n EFTFCNC{Sig}Float{namec} "
            f"-d model_test_{Sig}.root --verbose 1 -t -1 --setParameters r=1,{fitPoint_str} --setParameterRanges {paramRange} --freezeParameters r > initialFit{Sig}{namec}.log 2>&1 & \n"
        )
        print (info)        
