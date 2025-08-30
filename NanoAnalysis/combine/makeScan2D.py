import os
#####WCs=["cQlM", "cQe", "ctl", "cte", "ctlS", "ctlT"]
#####WCnames=["c_{QlM}", "c_{Qe}", "c_{tl}", "c_{te}", "c_{tlS}", "c_{tlT}"]
#####ranges={
#####"cQlM":"-0.1,0.1","cQe":"-0.1,0.1","ctl":"-0.1,0.1","cte":"-0.1,0.1", "ctlS":"-0.1,0.1","ctlT":"-0.01,0.01"}
#####for numc,  namec in enumerate(WCs):
#####    for numc2 in range(numc+1,len(WCs)):
#####        coup=WCs[numc]+WCs[numc2]
#####        cardName = namec+WCs[numc2]+'_3LoffZp_2017_1Bjet.txt'
#####        POIs = {
#####        'FCNC-Prod_' + WCs[numc] :  WCs[numc],
#####        'FCNC-Deca_' + WCs[numc] :  WCs[numc],
#####        'FCNC-Prod_' + WCs[numc2] :  WCs[numc2],
#####        'FCNC-Deca_' + WCs[numc2] :  WCs[numc2],
#####        }
#####        WS='text2workspace.py ' + cardName + ' -o workspace.root -P HiggsAnalysis.CombinedLimit.PhysicsModel:multiSignalModel --PO verbose'
#####        for key, value in POIs.items():
#####            WS += '  --PO \'map=.*/' + key + ":" + value + '[0,' + ranges[value]+']\''
#####        os.system(WS)
#####        os.system('combine -M MultiDimFit --algo=grid --points 400 --verbose 1 -m 125   -n Exp_' + coup + ' -d workspace.root  --setParameters r=0 --setParameterRanges ' +  WCs[numc]+'='+ranges[namec]+':'+  WCs[numc2]+'='+ranges[WCs[numc2]] +' -t -1')
#####        os.system('combine -M MultiDimFit --algo=grid --points 400 --verbose 1 -m 125   -n Obs_' + coup + ' -d workspace.root  --setParameters r=0 --setParameterRanges ' +  WCs[numc]+'='+ranges[namec]+':'+  WCs[numc2]+'='+ranges[WCs[numc2]])
#####        os.system('python /afs/crc.nd.edu/user/r/rgoldouz/AnalyticAnomalousCoupling/CMSSW_10_2_13/src/HiggsAnalysis/AnalyticAnomalousCoupling/scripts/mkEFTScan.py higgsCombineExp_' + coup + '.MultiDimFit.mH125.root --output ' + coup + 'Exp -p '+WCs[numc]+' '+WCs[numc2]+'  -maxNLL 10 -lumi 41.53 -cms -preliminary -xlabel "' + WCs[numc] + ' [TeV^{-2}]" -ylabel "' + WCs[numc2] +' [TeV^{-2}]"')
#####        os.system('python /afs/crc.nd.edu/user/r/rgoldouz/AnalyticAnomalousCoupling/CMSSW_10_2_13/src/HiggsAnalysis/AnalyticAnomalousCoupling/scripts/mkEFTScan.py higgsCombineObs_' + coup + '.MultiDimFit.mH125.root --output ' + coup + 'Obs -p '+WCs[numc]+' '+WCs[numc2]+'  -maxNLL 10 -lumi 41.53 -cms -preliminary -xlabel "' + WCs[numc] + ' [TeV^{-2}]" -ylabel "' + WCs[numc2] +' [TeV^{-2}]"')
######    os.system('text2workspace.py ' + WCs[i] + '_3LoffZp_2017_1Bjet.txt')
######    os.system('combine -M MultiDimFit --algo=grid --points 400 --verbose 1 -m 125   -n Exp_' + WCs[i] + ' -d ' + WCs[i] + '_3LoffZp_2017_1Bjet.root  --setParameters r=0 --setParameterRanges r='+ranges[i] +' -t -1')
######    os.system('combine -M MultiDimFit --algo=grid --points 400 --verbose 1 -m 125   -n Obs_' + WCs[i] + ' -d ' + WCs[i] + '_3LoffZp_2017_1Bjet.root  --setParameters r=0 --setParameterRanges r='+ranges[i] )
######    os.system('python /afs/crc.nd.edu/user/r/rgoldouz/AnalyticAnomalousCoupling/CMSSW_10_2_13/src/HiggsAnalysis/AnalyticAnomalousCoupling/scripts/mkEFTScan.py higgsCombineObs_' + WCs[i] + '.MultiDimFit.mH125.root --output ' + WCs[i] + ' -p r -maxNLL 10 -lumi 41.53 -cms -preliminary -xlabel "' + WCnames[i] + ' [TeV^{-2}]" --others higgsCombineExp_' + WCs[i] + '.MultiDimFit.mH125.root:2:1:"Expected" --main-label "Observed"')
######    os.system('python /afs/crc.nd.edu/user/r/rgoldouz/AnalyticAnomalousCoupling/CMSSW_10_2_13/src/HiggsAnalysis/AnalyticAnomalousCoupling/scripts/mkEFTScan.py higgsCombineObs_' + WCs[i] + '.MultiDimFit.mH125.root --output ' + WCs[i] + 'Obs -p r -maxNLL 10 -lumi 41.53 -cms -preliminary -xlabel "' + WCnames[i] + ' [TeV^{-2}]"')
######        os.system('python /afs/crc.nd.edu/user/r/rgoldouz/AnalyticAnomalousCoupling/CMSSW_10_2_13/src/HiggsAnalysis/AnalyticAnomalousCoupling/scripts/mkEFTScan.py higgsCombineExp_' + coup + '.MultiDimFit.mH125.root --output ' + coup + 'Exp -p '+WCs[numc]+' '+WCs[numc2]+'  -maxNLL 10 -lumi 41.53 -cms -preliminary -xlabel "' + WCs[numc] + ' [TeV^{-2}]" -ylabel "' + WCs[numc2] +' [TeV^{-2}]" --others higgsCombineObs_' + coup + '.MultiDimFit.mH125.root:4:1:"Observed" --main-label "Expected"')



WCs=["ctp","ctlS","cte","ctl","ctlT","ctZ","cpt","cpQM","ctA","cQe","ctG","cQlM"]
WCnames=["k_ctp","k_ctlS","k_cte","k_ctl","k_ctlT","k_ctZ","k_cpt","k_cpQM","k_ctA","k_cQe","k_ctG","k_cQlM"]
R='-5,5'
L='-1,1'
ranges={"k_ctp":R,"k_ctZ":L,"k_cpt":R,"k_cpQM":R,"k_ctA":R,"k_ctG":L,"k_cQlM":R,"k_cQe":R,"k_ctl":R,"k_cte":R, "k_ctlS":R,"k_ctlT":L}
#Frozen fits
print ('making Frozen fits')
year=['2017']
regions=["1bLj","1bHj"]
channels=["2lss","3lonZ", "3loffZhigh"]
channels=["2lss"]
for numyear, nameyear in enumerate(year):
    cardName=''
    for numch, namech in enumerate(channels):
        for numreg, namereg in enumerate(regions):
            cardName = cardName + ' C'+namech+'_'+nameyear+'_' + namereg+'.txt'
    print ('combineCards.py ' + cardName + ' > datacard.txt')
    print ('text2workspace.py '+nameyear+ '_com.txt -P HiggsAnalysis.AnalyticAnomalousCoupling.AnomalousCouplingEFTNegative:analiticAnomalousCouplingEFTNegative  -o   model_test.root  --X-allow-no-signal --PO eftOperators=ctp,ctlS,cte,ctl,ctlT,ctZ,cpt,cpQM,ctA,cQe,ctG,cQlM')
#    os.system('combineCards.py ' + cardName + ' > '  + nameyear+ '_com.txt')
#    os.system('text2workspace.py '+nameyear+ '_com.txt -P HiggsAnalysis.AnalyticAnomalousCoupling.AnomalousCouplingEFTNegative:analiticAnomalousCouplingEFTNegative  -o   model_test.root  --X-allow-no-signal --PO eftOperators=ctp,ctlS,cte,ctl,ctlT,ctZ,cpt,cpQM,ctA,cQe,ctG,cQlM')
    for numc,  namec in enumerate(WCnames):
        joined = ",".join([s for s in WCnames if s != namec])
        param_strAll = ",".join("{}=0".format(name) for name in WCnames)
        param_str = ":".join("{}={}".format(k, v) for k, v in ranges.items())
        text = "combine -M MultiDimFit --algo=grid --points 50 --verbose 1 -m 125 -n EFTFCNC -d model_test.root --redefineSignalPOIs " + namec + " --setParameters r=1,"+param_strAll + " --setParameterRanges " + param_str + " --freezeParameters r,"+joined+ " -t -1"
#        draw='python /users/rgoldouz/AnalyticAnomalousCoupling/CMSSW_10_2_13/src/HiggsAnalysis/AnalyticAnomalousCoupling/scripts/mkEFTScan.py higgsCombineEFTFCNC.MultiDimFit.mH125.root --output '+namec + ' -p ' +namec + ' -maxNLL 10 -lumi 41.53 -cms -preliminary -xlabel "'+WCs[numc] +'[TeV^{-2}]"'
#        draw='python /users/rgoldouz/Limit_combined/forLobster/CMSSW_10_2_13/src/HiggsAnalysis/AnalyticAnomalousCoupling/scripts/mkEFTScan.py higgsCombineEFTFCNC.MultiDimFit.mH125.root --output '+namec + ' -p ' +namec + ' -maxNLL 10 -lumi 41.53 -cms -preliminary -xlabel "'+WCs[numc] +'[TeV^{-2}]"'
        draw='mkEFTScan.py higgsCombineEFTFCNC.MultiDimFit.mH125.root -p ' +namec + ' k_ctp -maxNLL 10 -lumi 138 -cms -preliminary -o scan_' +namec + ' -ff png'
        print (text)
        print (draw)
#        os.system(text)
#        os.system(draw)
