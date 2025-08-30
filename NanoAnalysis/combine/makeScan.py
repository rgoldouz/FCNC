import os
from multiprocessing import Pool

#WCs = ["ctp", "ctlS", "cte", "ctl", "ctlT", "ctZ", "cpt", "cpQM", "ctA", "cQe", "ctG", "cQlM"]
WCs = ["ctpF", "ctlSF", "cteF", "ctlF", "ctlTF", "ctZF", "cptF", "cpQMF", "ctAF", "cQeF", "ctGF", "cQlMF"]
WCnames = ["k_" + wc for wc in WCs]
R = "-2,2"
L = "-0.2,0.2"
ranges = {"k_ctpF": R, "k_ctZF": L, "k_cptF": R, "k_cpQMF": R, "k_ctAF": R, "k_ctGF": L, "k_cQlMF": R, "k_cQeF": R, "k_ctlF": R, "k_cteF": R, "k_ctlSF": R, "k_ctlTF": L}

year = ["2017"]
regions = ["1bLj", "1bHj"]
channels = ["2lss","3lonZ", "3loffZhigh"]
def make_commands(nameyear):
    card_list = []
    for ch in channels:
        for reg in regions:
            card_list.append(f"C{ch}_{nameyear}_{reg}.txt")
    card_str = " ".join(card_list)
    combine_card_cmd = f"combineCards.py {card_str} > {nameyear}_com.txt"
    workspace_cmd = (
        f"text2workspace.py {nameyear}_com.txt "
        "-P HiggsAnalysis.AnalyticAnomalousCoupling.AnomalousCouplingEFTNegative:analiticAnomalousCouplingEFTNegative "
        "-o model_test.root --X-allow-no-signal "
        "--PO eftOperators=" + ",".join(WCs)
    )

    return combine_card_cmd, workspace_cmd

def run_fit(namec):
    joined = ",".join(k for k in WCnames if k != namec)
    param_strAll = ",".join(f"{k}=0" for k in WCnames)
    param_str = ":".join(f"{k}={v}" for k, v in ranges.items())
    param_range_str = ":".join(f"{wc}=-10,10" for wc in WCnames if wc != namec)
    param_range_str=param_range_str+":"+namec+'='+ranges[namec]
    fit_cmd = (
        f"combineTool.py -M MultiDimFit --algo=grid --points 400 --verbose 1 -m 125 -n EFTFCNCFrozen{namec} "
        f"-d model_test.root --redefineSignalPOIs {namec} --setParameters r=1,{param_strAll} "
        f"--setParameterRanges {param_str} --freezeParameters r,{joined} -t -1 "
        f"--job-mode condor --split-points 20 --sub-opts='+JobFlavour=\"workday\"' --task-name Frozen{namec}"
    )
#    draw_cmd = (
#        f"mkEFTScan.py higgsCombineEFTFCNCFrozen{namec}.MultiDimFit.mH125.root -p {namec} "
#        f"-maxNLL 10 -lumi 138 -cms -preliminary -o scan_{namec} -ff png"
#    )

    fitFloat_cmd= (
        f"combineTool.py -M MultiDimFit --algo=grid --points 400 --verbose 1 -m 125 -n EFTFCNCFloat{namec} "
        f"-d model_test.root --redefineSignalPOIs {namec} --floatOtherPOIs=1 --setParameters r=1,{param_strAll} "
        f"--setParameterRanges {param_range_str} --freezeParameters r -t -1 "
        f"--job-mode condor --split-points 20 --sub-opts='+JobFlavour=\"workday\"' --task-name Float{namec}"
    )            

    print(f"Running fit for {namec}")
    os.system('ulimit -Ss 13107')
    print(fit_cmd)
    print(fitFloat_cmd)
    os.system(fitFloat_cmd)
    os.system(fit_cmd)
#    os.system(draw_cmd)

def run_fit2D():
    param_strAll = ",".join(f"{k}=0" for k in WCnames)
    param_str = ":".join(f"{k}={v}" for k, v in ranges.items())
    for w1,wc1 in enumerate(WCnames):
        for w2,wc2 in enumerate(WCnames):
            if wc1==wc2 or w2<w1:
                continue
            param_strAll = ",".join(f"{k}=0" for k in WCnames)
            param_range_str = ":".join(f"{wc}=-10,10" for wc in WCnames if (wc != wc1 and wc != wc2))
            param_range_str=param_range_str+":"+wc1+'='+ranges[wc1]+":"+wc2+'='+ranges[wc2]
            fitFloat2D_cmd= (
                f"combineTool.py -M MultiDimFit --algo=grid --points 600 --verbose 1 -m 125 -n EFTFCNCFloat{wc1}{wc2} "
                f"-d model_test.root --redefineSignalPOIs {wc1},{wc2} --floatOtherPOIs=1 --setParameters r=1,{param_strAll} "
                f"--setParameterRanges {param_range_str} --freezeParameters r -t -1 "
                f"--job-mode condor --split-points 20 --sub-opts='+JobFlavour=\"tomorrow\"'  --sub-opts='+RequestMemory=4000' --task-name {wc1}{wc2}"
             )    
            print(fitFloat2D_cmd)
            os.system(fitFloat2D_cmd)

def main():
    os.system('rm k_*')
    os.system('rm higgsCombineEFTFCNCF*')
    os.system('rm condor*')
    for nameyear in year:
        combine_cmd, workspace_cmd = make_commands(nameyear)
        print(">>", combine_cmd)
        os.system(combine_cmd)
        print(">>", workspace_cmd)
    #    os.system(workspace_cmd)

        # Parallel execution of EFT scans
        with Pool(processes=12) as pool:
            pool.map(run_fit, WCnames)
        run_fit2D()    

if __name__ == "__main__":
    main()
