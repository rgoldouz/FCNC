import os
from multiprocessing import Pool

#WCs = ["ctp", "ctlS", "cte", "ctl", "ctlT", "ctZ", "cpt", "cpQM", "ctA", "cQe", "ctG", "cQlM"]
WCs = ["ctpF", "ctlSF", "cteF", "ctlF", "ctlTF", "ctZF", "cptF", "cpQMF", "ctAF", "cQeF", "ctGF", "cQlMF"]
WCnames = ["k_" + wc for wc in WCs]
R = "-1,1"
L = "-0.1,0.1"
S="-0.01,0.01"
#ranges = {"k_ctp": R, "k_ctZ": L, "k_cpt": R, "k_cpQM": R, "k_ctA": R, "k_ctG": L, "k_cQlM": R, "k_cQe": R, "k_ctl": L, "k_cte": R, "k_ctlS": R, "k_ctlT": S}
ranges = {"k_ctpF": R, "k_ctZF": L, "k_cptF": R, "k_cpQMF": R, "k_ctAF": R, "k_ctGF": L, "k_cQlMF": R, "k_cQeF": R, "k_ctlF": R, "k_cteF": R, "k_ctlSF": R, "k_ctlTF": L}

year = ["2017"]
regions = ["1bLj", "1bHj"]
channels = ["2lss","3lonZ", "3loffZhigh"]

def run_fit(namec):
    hadd_cmdFloat = (
        f"hadd -f higgsCombineEFTFCNCFloat{namec}.MultiDimFit.mH125.root higgsCombineEFTFCNCFloat{namec}.POINTS.*"
    )
    hadd_cmdFrozen = (
        f"hadd -f higgsCombineEFTFCNCFrozen{namec}.MultiDimFit.mH125.root higgsCombineEFTFCNCFrozen{namec}.POINTS.*"
    )
    draw_cmd = (
        f"mkEFTScan.py higgsCombineEFTFCNC{namec}.MultiDimFit.mH125.root -p {namec} "
        f"-maxNLL 10 -lumi 138 -cms -preliminary -o FF_{namec} -ff png "
        f"--others higgsCombineEFTFCNCFloat{namec}.MultiDimFit.mH125.root:4:1:\"Float\" --main-label \"Frozen\""
    )
    print(hadd_cmdFloat)
    print(hadd_cmdFrozen)
    print(draw_cmd)
    os.system(hadd_cmdFloat)
    os.system(hadd_cmdFrozen)
    os.system(draw_cmd)    

    
def main():
    print("=== Making Frozen Fits ===")
    for nameyear in year:
        # Parallel execution of EFT scans
        with Pool(processes=12) as pool:
            pool.map(run_fit, WCnames)
        for w1,wc1 in enumerate(WCnames):
            for w2,wc2 in enumerate(WCnames):
                if wc1==wc2 or w2<w1:
                    continue
                hadd2D_cmd = (
                    f"hadd -f higgsCombineEFTFCNCFloat{wc1}{wc2}.MultiDimFit.mH125.root higgsCombineEFTFCNCFloat{wc1}{wc2}.POINTS.*"
                )
                draw2D_cmd = (
                    f"mkEFTScan.py higgsCombineEFTFCNCFloat{wc1}{wc2}.MultiDimFit.mH125.root -p {wc1} {wc2} "
                    f"-maxNLL 10 -lumi 138 -cms -preliminary -o FF_{wc1}{wc2} -ff png "
                    f"--main-label \"Float\""
               )
                print(hadd2D_cmd)
                print(draw2D_cmd)    
                os.system(hadd2D_cmd)
                os.system(draw2D_cmd)
if __name__ == "__main__":
    main()
