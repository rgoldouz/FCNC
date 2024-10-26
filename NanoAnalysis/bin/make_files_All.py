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
        fi = ROOT.TFile.Open(filename)
       # tree_in = f.Get('Runs')
        tree_meta = fi.Get('Runs')
        genEventCount = 0
        genEventSumw = 0
        evtTree = fi.Get('Events')
        evtTree.SetBranchStatus("*", 0)
        evtTree.SetBranchStatus("genWeight", 1)
        evtTree.SetBranchStatus("LHEWeight_originalXWGTUP", 1)
        if 'BNV' in name:
            for i in range( evtTree.GetEntries() ):
                evtTree.GetEntry(i)
                if evtTree.LHEWeight_originalXWGTUP not in nWeight:
                    nWeight.append(evtTree.LHEWeight_originalXWGTUP)
        evtTree.GetEntry(0)
        for i in range( tree_meta.GetEntries() ):
            tree_meta.GetEntry(i)
            genEventCount += tree_meta.genEventCount
            genEventSumw += tree_meta.genEventSumw
            nRuns +=1
        neventsweight += genEventCount
        neventsweightSumw += genEventSumw/abs(evtTree.genWeight)
        if tree_meta.GetEntries()>1:
            print 'Warning number of MC Runs is more than 1, be careful about sum of the weights'
        tree_meta.Reset()
        tree_meta.Delete()
        evtTree.Reset()
        evtTree.Delete()
        fi.Close()
    for key, value in MCSAMPLES.items():
        if key == name.split('/')[8]:
            value[0].append(name[19:])
            value[7] = str( float(value[8]) + neventsweightSumw)
            value[9] = str(len(nWeight))


if __name__ == '__main__':
#    MCSAMPLES = {}
    
    crossSection = {
    'ST_antitop_tchannel': '26.38',
    'ST_top_tchannel': '44.33',
    'ST_top_schannel': '3.36',
    'tW': '19.47',
    'tbarW': '19.47',
    'TTTo2L2Nu': '87.31',
    'TTJets': '831.76',
    'DY10to50': '18610',
    'DY50': '6077.22',
    'WZTo2L2Q':'5.595',
    'ZZTo2L2Nu':'0.564',
    'TTZToLLNuNu_M_10':'0.2529',
    'WJetsToLNu':'61526.7',
    'TTW':'0.2043',
    'WZTo3LNu':'4.43',
    'WWZ_4F':'0.1651',
    'ZZTo4L':'1.256 ',
    'WWW_4F':'0.2086',
    'ZZZ':'0.01398',
    'WWTo2L2Nu': '12.178'
    }
    
    blackList = ['ST_antitop_tchannel','ST_top_tchannel', 'ST_top_schannel', 'TTJets','fcnc', 'tbarW_Inclusive', 'tW_Inclusive']
    
    text = ''
    text += 'import sys \n'
    text += 'import os \n'
    text += 'import subprocess \n'
    text += 'import readline \n'
    text += 'import string \n'
    text += '\n'
    
    dirSamples = {
    'UL16preVFP': ['2016preVFP','/hadoop/store/user/rgoldouz/NanoAodPostProcessingUL/UL16preVFP/v1','19.52'],
    'UL16postVFP': ['2016postVFP','/hadoop/store/user/rgoldouz/NanoAodPostProcessingUL/UL16postVFP/v1','16.81'],
    '2017': ['2017' , '/hadoop/store/user/rgoldouz/NanoAodPostProcessingUL/UL17/v1',"41.48"],
    '2018': ['2018' , '/hadoop/store/user/rgoldouz/NanoAodPostProcessingUL/UL18/v1',"59.83"],
    }
    
    Slist=[]
    for key, value in dirSamples.items():
        dir_list = os.listdir(value[1])
        for key in dir_list:
            accept = True
            for S in blackList:
                if S in key:
                    accept = False
            if accept:
                if 'data' in key:
                    a,b,c,d = key.split("_")   
                    MCSAMPLES[key] = [    [],    "data",    d,    value[0],    c,    "1",    value[2],    "1",  "0", "1"]
                else:
                    MCSAMPLES[key] = [    [],    "mc",    "none",    value[0],    "none",    "1",    value[2],    "0",  "0", "1"]
    
        for root, dirs, files in os.walk(value[1]):
            if len(files) > 0:
        #        print root
        #        if 'TTTo2L2Nu' not in root:
        #            continue
                if 'data' in root:
                    for key, value in MCSAMPLES.items():
                        if key in root:
                            value[0].append(root[19:])
                else:
                    Slist.append(root)
    #                neventsweight = 0
    #                neventsweightSumw = 0
    #                nRuns = 0
    #                for fname in files:
    #                    filename = root + '/' + fname
    #                    if 'fail' in fname:
    #                        continue
    #                    f = ROOT.TFile.Open(filename)
    #        #            tree_in = f.Get('Runs')
    #                    tree_meta = f.Get('Runs')
    #                    genEventCount = 0
    #                    genEventSumw = 0
    #                    evtTree = f.Get('Events')
    #                    evtTree.SetBranchStatus("*", 0)
    #                    evtTree.SetBranchStatus("genWeight", 1)
    #                    evtTree.GetEntry(0)
    #                    for i in range( tree_meta.GetEntries() ):
    #                        tree_meta.GetEntry(i)
    #                        genEventCount += tree_meta.genEventCount
    #                        genEventSumw += tree_meta.genEventSumw
    #                        nRuns += 1
    #                    neventsweight += genEventCount
    #                    neventsweightSumw += genEventSumw/abs(evtTree.genWeight)
    #                    if tree_meta.GetEntries()>1:
    #                        print 'Warning number of MC Runs is more than 1, be careful about sum of the weights' 
    #                    tree_meta.Reset()
    #                    tree_meta.Delete()
    #    #                print str(evtTree.genWeight)
    #    #                print filename 
    #    #                print '-nevent:' + str(genEventCount) +' -neventsweightSumw:'+str(genEventSumw) +' -neventsweightSumw/w:'+str(genEventSumw/abs(evtTree.genWeight))
    #                    evtTree.Reset()
    #                    evtTree.Delete()
    #                    f.Close()
    #                for key, value in MCSAMPLES.items():
    #                    if key in root: 
    #                        value[0].append(root[19:])
    #                        value[7] = str( float(value[7]) + neventsweightSumw)
    #                        value[9] = str(nRuns)
    #                        print 'neventsweightSumw:'+ str(neventsweightSumw)
    #                        print 'neventsweight:'+str(neventsweight)
    print Slist 
    Parallel(n_jobs=40, require="sharedmem")(delayed(f)(i) for i in Slist)
    
    for key, value in MCSAMPLES.items():
        for S, xs in crossSection.items():
            if S in key:
                value[5]=xs
    
    for key, value in MCSAMPLES.items():
        if not ('BNV' in key or 'FCNC' in key):
            value[9] = "1"
            continue
        neventsweight = 0
        neventsweightSumw = 0
        value[8] = "1"
        print key
        print value
        files = os.listdir('/hadoop/store/user/'+value[0][0])
        for fname in files:
            filename = '/hadoop/store/user/'+value[0][0] + '/' + fname
            f = ROOT.TFile.Open(filename)
            tree_meta = f.Get('Events')
            neventsweight +=  tree_meta.GetEntries()
            neventsweightSumw +=  tree_meta.GetEntries()
            tree_meta.Reset()
            tree_meta.Delete()
            f.Close()    
        value[7] = str(neventsweight)
    
    
    text += 'UL17={'                
    #text += str(MCSAMPLES)
    text += '\n'
    
    for key, value in MCSAMPLES.items():
        if 'data' in key:
            continue
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
