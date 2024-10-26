import math
import gc
import sys
import ROOT
import numpy as np
import copy
import os
ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.gROOT.ProcessLine("gErrorIgnoreLevel = 1;")
ROOT.TH1.AddDirectory(ROOT.kFALSE)
ROOT.gStyle.SetOptStat(0)
from array import array
from ROOT import TColor
from ROOT import TGaxis
from ROOT import THStack
from ROOT import TFile
import gc
import sys
import os
import subprocess
import readline
import string
import glob
from joblib import Parallel, delayed
MCSAMPLES = {}

def f(name):
    print name
    neventsweight = 0
    neventsweightSumw = 0
    nRuns = 0
    nWeight = []
    for fname in os.listdir(name):
        filename = name + '/' + fname
        if 'fail' in fname:
            continue
        fi = TFile.Open(filename)
        tree_meta = fi.Get('Runs')
        genEventCount = 0
        genEventSumw = 0
        evtTree = fi.Get('Events')
        evtTree.SetBranchStatus("*", 0)
        evtTree.SetBranchStatus("genWeight", 1)
        evtTree.SetBranchStatus("LHEWeight_originalXWGTUP", 1)
        if 'FCNC' in name:  
            for i in range( evtTree.GetEntries() ):
                evtTree.GetEntry(i)
                if abs(evtTree.LHEWeight_originalXWGTUP) not in nWeight:
                    nWeight.append(abs(evtTree.LHEWeight_originalXWGTUP))
        evtTree.GetEntry(0)
        for i in range( tree_meta.GetEntries() ):
            tree_meta.GetEntry(i)
            genEventCount += tree_meta.genEventCount
            genEventSumw += tree_meta.genEventSumw
            nRuns +=1
        neventsweight += genEventCount
        neventsweightSumw += genEventSumw/abs(evtTree.genWeight)
#        if tree_meta.GetEntries()>1:
#            print filename + 'Warning number of MC Runs is more than 1, be careful about sum of the weights'
        tree_meta.Reset()
        tree_meta.Delete()
        evtTree.Reset()
        evtTree.Delete()
        fi.Close()
    if len(nWeight)>1:
        print filename + ' ***!!!!!!!!!!!!!!!*** Warning number of original weights is '+str(len(nWeight)) 
#    return name[19:],str(neventsweightSumw), str(len(nWeight))
    return name[19:],str(neventsweightSumw), str(nRuns) 
#    for key, value in MCSAMPLES.items():
#        if key == name.split('/')[8]:
#            value[0].append(name[19:])
#            value[7] = str( float(value[8]) + neventsweightSumw)
#            value[9] = str(len(nWeight))


if __name__ == '__main__':
#    MCSAMPLES = {}
    
    crossSection = {
    '_tZq': '0.0942',
#    '_tZq': '0.0758',
    '_ST_antitop_t_channel': '80.95',
    '_ST_top_t_channel': '136.02',
    '_ST_top_s_channel': '3.68',
    '_tW': '35.85',
    '_tbarW': '35.85',
    '_TTTo2L2Nu': '87.31',
    '_TTToSemiLeptonic':'364.35',
    '_TTJets': '831.76',
    '_DY10to50': '18610',
    '_DY50': '6077.22',
    '_TTGamma_Dilept':'1.513',
    '_TTGamma_SingleLept':'5.121',
    '_TTZ':'0.281',
    '_ttHnobb':'0.2151',
    '_tttt':'0.009103',
    '_WJetsToLNu':'61526.7',
    '_TTWJetsToLNu':'0.2043',
    '_WZTo3LNu':'5.28',
    '_WWZ_4F':'0.1651',
    '_WZZ':'0.05565',
    '_ZGToLLG':'55.78',
    '_ZZTo4L':'1.256 ',
    '_WWW_4F':'0.2086',
    '_ZZZ':'0.01398',
    '_WWTo2L2Nu': '12.178',
    '_TWZToLL_tlept_Whad':'0.003004',
    '_TWZToLL_tlept_Wlept':'0.0015',
    '_TWZToLL_thad_Wlept':'0.003004'
    }
    
    blackList = ['TTJets','TTGJets','SMEFT','gen','sim','digi','hlt','reco','mAOD','nano']
    
    text = ''
    text += 'import sys \n'
    text += 'import os \n'
    text += 'import subprocess \n'
    text += 'import readline \n'
    text += 'import string \n'
    text += '\n'
   
    dirSamples = {
    'dataSamples2':'/hadoop/store/user/awightma/skims/data/NAOD_ULv9_new-lepMVA-v2/2016APV/v1',
    'dataSamples1':'/hadoop/store/user/awightma/skims/data/NAOD_ULv9_new-lepMVA-v2/FullRun2/v3',
    'mcSamples9':'/hadoop/store/user/awightma/skims/mc/new-lepMVA-v2/central_bkgd_p7/TWZToLL/v1',
    'mcSamples8':'/hadoop/store/user/awightma/skims/mc/new-lepMVA-v2/central_bkgd_p6/jsons_for_lo_ttgamma/v1',
    'mcSamples7':'/hadoop/store/user/awightma/skims/mc/new-lepMVA-v2/central_bkgd_p5/fix_ext_stats_jsons/v1',
    'mcSamples6':'/hadoop/store/user/awightma/skims/mc/new-lepMVA-v2/central_bkgd_p5/add_ext_bkg/v1',
    'mcSamples5':'/hadoop/store/user/awightma/skims/mc/new-lepMVA-v2/central_bkgd_p4/WZTo3LNuPowheg/v2',
    'mcSamples4':'/hadoop/store/user/awightma/skims/mc/new-lepMVA-v2/central_bkgd_p3/TTbarPowheg_ZG/v1',
    'mcSamples3':'/hadoop/store/user/awightma/skims/mc/new-lepMVA-v2/central_bkgd_p2/ZZTo4l_TTJets/v1',
    'mcSamples2':'/hadoop/store/user/awightma/skims/mc/new-lepMVA-v2/central_bkgd_p1/2016APV/v1',
    'mcSamples1':'/hadoop/store/user/awightma/skims/mc/new-lepMVA-v2/central_bkgd_p1/FullRun2/v2',
    'signalSamples2':'/hadoop/store/user/awightma/skims/mc/new-lepMVA-v2/central_sgnl/tZqPowheg/v1',
    'signalSamples1':'/hadoop/store/user/awightma/skims/mc/new-lepMVA-v2/central_sgnl/FullRun2/v1',
#    'FcncGenSamples2':'/hadoop/store/user/rgoldouz/FullProduction/nanoGen',
    'FcncGenSamples1':'/hadoop/store/user/rgoldouz/FullProduction/FullR2/UL17/FullSimFCNC/postLHE_step/v1',
    }
 
    years = {
    'UL16APV': ['UL16preVFP','','19.52','2016preVFP'],
    'HIPM_UL2016': ['UL16preVFP','','19.52','2016preVFP'],
    'ver1_HIPM_UL2016': ['UL16preVFP','v1','19.52','2016preVFP'],
    'ver2_HIPM_UL2016': ['UL16preVFP','v2','19.52','2016preVFP'],
    'UL16': ['UL16','','16.81','2016postVFP'],
    'UL17': ['UL17' , '',"41.48",'2017'],
    'UL18': ['UL18' , '',"59.83",'2018'],
    'UL2016': ['UL16','','16.81','2016postVFP'],
    'UL2017': ['UL17' , '',"41.48",'2017'],
    'UL2018': ['UL18' , '',"59.83",'2018'],
    'NanoGen': ['UL17' , '',"41.48",'2017'],
    }
    
    Slist=[]
    Sclean=[]
    Sclean2=[]
    for key, value in dirSamples.items():
        dir_list = os.listdir(value)
        for Skey in dir_list:
            if Skey in Sclean:
                continue
            else:
                Sclean.append(Skey)
            accept = True
            for S in blackList:
                if S in Skey:
                    accept = False
            if accept:
                if 'data' in key:
                    a = Skey.split("_")[0]   
                    b = Skey.split("_")[1]
                    c = '_'.join(Skey.split("_")[2:])
                    n= 'data_'+years[c][0]+'_'+b+ years[c][1]+'_'+a
                    MCSAMPLES[n] = [    [],    "data",    a,    years[c][3],    b+ years[c][1],    "1",    years[c][2],    "1",  "0", "1", "0", Skey]
                else:
                    a = Skey.split("_")[0]
                    n= years[a][0]+'_'+'_'.join(Skey.split("_")[1:])
                    MCSAMPLES[n] = [    [],    "mc",    "none",    years[a][3],    "none",    "1",    years[a][2],    "0",  "0", "1", "0", Skey]
    
        for root, dirs, files in os.walk(value):
            if len(files) > 0:
                for keyS, valueS in MCSAMPLES.items():
                    if valueS[-1] in root.split('/') and valueS[-1] not in Sclean2:
                        Sclean2.append(valueS[-1])
                        if 'data' in root:
                            valueS[0].append(root[19:])
                        else:
                            Slist.append(root)
    res = Parallel(n_jobs=40)(delayed(f)(i) for i in Slist)
    Address = [item[0] for item in res]
    Sumw = [item[1] for item in res]
    SumRuns = [item[2] for item in res]

    for a in range(len(Address)):
        print Address[a] + ' ' + Sumw[a] +" " +SumRuns[a]
        for key, value in MCSAMPLES.items():
            if value[-1] in Address[a].split("/"):
                value[0].append(Address[a])
                value[7] = Sumw[a]
                value[9] = SumRuns[a]

    for key, value in MCSAMPLES.items():
        for S, xs in crossSection.items():
            if S in key:
                value[5]=xs
    
    for key, value in MCSAMPLES.items():
        if not ('BNV' in key or 'FCNC' in key):
            value[9] = "1"
            continue
        isNanoGen=True
#        value[10] = "1"
        neventsweight = 0
        neventsweightSumw = 0
        value[8] = "1"
        print key
        print value
        if len(value[0])==0:
            print 'sample ' + MCSAMPLES[key] + ' is deleted'
            del MCSAMPLES[key]
            continue
        files = os.listdir('/hadoop/store/user/'+value[0][0])
        for fname in files:
            filename = '/hadoop/store/user/'+value[0][0] + '/' + fname
            f = ROOT.TFile.Open(filename)
            tree_meta = f.Get('Events')
            if tree_meta.GetNbranches()>200:
                isNanoGen=False
            neventsweight +=  tree_meta.GetEntries()
            neventsweightSumw +=  tree_meta.GetEntries()
            tree_meta.Reset()
            tree_meta.Delete()
            f.Close()    
        value[7] = str(neventsweight)
        if isNanoGen:
            value[10] = "1"    
    
    text += 'UL17={'                
    #text += str(MCSAMPLES)
    text += '\n'
    
    for key, value in MCSAMPLES.items():
        if 'data' in key:
            continue
        if 'UL16preVFP_' not in key:
            continue
        del value[-1]
        text += '"'
        text += key
        text += '":'
        text += str(value)
        text += ','
        text += '\n'
    text += '\n \n'
    for key, value in MCSAMPLES.items():
        if 'data' in key:
            continue
        if 'UL16_' not in key:
            continue
        del value[-1]
        text += '"'
        text += key
        text += '":'
        text += str(value)
        text += ','
        text += '\n'
    text += '\n \n'
    for key, value in MCSAMPLES.items():
        if 'data' in key:
            continue
        if 'UL17_' not in key:
            continue
        del value[-1]
        text += '"'
        text += key
        text += '":'
        text += str(value)
        text += ','
        text += '\n'
    text += '\n \n'
    for key, value in MCSAMPLES.items():
        if 'data' in key:
            continue
        if 'UL18_' not in key:
            continue
        del value[-1]
        text += '"'
        text += key
        text += '":'
        text += str(value)
        text += ','
        text += '\n'
    text += '\n \n'
    
    text += '\n \n'
    for key, value in MCSAMPLES.items():
        if 'data' not in key:
            continue
        if 'UL16preVFP_' not in key:
            continue
        del value[-1]
        text += '"'
        text += key
        text += '":'
        text += str(value)
        text += ','
        text += '\n'
    text += '\n \n'
    for key, value in MCSAMPLES.items():
        if 'data' not in key:
            continue
        if 'UL16_' not in key:
            continue
        del value[-1]
        text += '"'
        text += key
        text += '":'
        text += str(value)
        text += ','
        text += '\n'
    text += '\n \n'
    for key, value in MCSAMPLES.items():
        if 'data' not in key:
            continue
        if 'UL17_' not in key:
            continue
        del value[-1]
        text += '"'
        text += key
        text += '":'
        text += str(value)
        text += ','
        text += '\n'
    text += '\n \n'
    for key, value in MCSAMPLES.items():
        if 'data' not in key:
            continue
        if 'UL18_' not in key:
            continue
        del value[-1]
        text += '"'
        text += key
        text += '":'
        text += str(value)
        text += ','
        text += '\n'
        print(key, ' : ', value)
    text += '}'
    #
    print text
    open('Files_ULall_nano.py', 'wt').write(text)