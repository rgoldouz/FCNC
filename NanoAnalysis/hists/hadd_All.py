import sys
import os
import subprocess
import readline
import string
import glob
from joblib import Parallel, delayed
sys.path.append('/users/rgoldouz/FCNC/NanoAnalysis/bin/')
import Files_ULall_nano

def f(name):
    if 'ANoutput' not in name:
        print name
    os.system(name)

if __name__ == '__main__':
    Fhadd=[]
    SAMPLES = {}
    SAMPLES.update(Files_ULall_nano.UL17)
    
    
    addedFilesData = {"2016preVFP": [],"2016postVFP": [], "2017": [], "2018": []} 
    addedFilesMcDY = {"2016preVFP": [],"2016postVFP": [], "2017": [], "2018": []}
    addedFilesMcWJets = {"2016preVFP": [],"2016postVFP": [], "2017": [], "2018": []}
    addedFilesMcttbar = {"2016preVFP": [],"2016postVFP": [], "2017": [], "2018": []}
    addedFilesMcDiboson = {"2016preVFP": [],"2016postVFP": [], "2017": [], "2018": []}
    addedFilesMcTriboson = {"2016preVFP": [],"2016postVFP": [], "2017": [], "2018": []}
    addedFilesMcTTX = {"2016preVFP": [],"2016postVFP": [], "2017": [], "2018": []}
    addedFilesMcST = {"2016preVFP": [],"2016postVFP": [], "2017": [], "2018": []}
    addedFilesMcConv = {"2016preVFP": [],"2016postVFP": [], "2017": [], "2018": []}
    addedFilesMcFCNCTUprod = {"2016preVFP": [],"2016postVFP": [], "2017": [], "2018": []}
    addedFilesMcFCNCTUdecay = {"2016preVFP": [],"2016postVFP": [], "2017": [], "2018": []}
    addedFilesMcFCNCTCprod = {"2016preVFP": [],"2016postVFP": [], "2017": [], "2018": []}
    addedFilesMcFCNCTCdecay = {"2016preVFP": [],"2016postVFP": [], "2017": [], "2018": []}
    
    os.system('rm *.root')
    dist = "/cms/cephfs/data/store/user/rgoldouz/FullProduction/AnalysisTOPFCNC/Analysis_" 
    
    for keyUL, value in SAMPLES.items():
#        if "UL17" not in keyUL:
#            continue
        key = keyUL.replace("UL1", "201")
        hadd='hadd ' + key + '.root '
#        if not os.path.isdir(dist + keyUL):
#            print dist + keyUL+' does not exist'
#            continue
        for filename in os.listdir(dist + keyUL):
            hadd += dist + keyUL + '/' + filename + ' '
        Fhadd.append(hadd)
    Parallel(n_jobs=40)(delayed(f)(i) for i in Fhadd)
    #    os.system(hadd)
    for keyUL, value in SAMPLES.items():
        key = keyUL.replace("UL1", "201")
        year = value[3]
        if value[1]=='data':
            addedFilesData[year].append(key + '.root')
#        elif 'FCNC' in key:
#            continue
        elif 'DY' in key:
            addedFilesMcDY[year].append( key + '.root')
        elif 'TTG' in key or 'ZG' in key:
            addedFilesMcConv[year].append( key + '.root')
        elif '_WJetsToLNu' in key:
            addedFilesMcWJets[year].append(key + '.root')
        elif 'TTTo' in key and 'sys' not in key:
            addedFilesMcttbar[year].append( key + '.root')
#        elif 'WWTo' in key or 'WZTo' in key or 'ZZTo' in key or 'ZGTo' in key:
        elif '_WWTo' in key or '_WZTo' in key or '_ZZTo' in key:
            addedFilesMcDiboson[year].append( key + '.root')
        elif 'WWW' in key or 'WWZ' in key or 'WZZ' in key or 'ZZZ' in key:
            addedFilesMcTriboson[year].append( key + '.root')
        elif 'ST' in key or 'tW' in key or 'tbarW' in key:
            addedFilesMcST[year].append( key + '.root')
        elif 'TTG' in key:
            addedFilesMcConv[year].append( key + '.root')
        elif 'Production' in key and 'TC' in key:
            addedFilesMcFCNCTCprod[year].append( key + '.root')
        elif 'Decay' in key and 'TC' in key:
            addedFilesMcFCNCTCdecay[year].append( key + '.root')
        elif 'Production' in key and 'TU' in key:
            addedFilesMcFCNCTUprod[year].append( key + '.root')
        elif 'Decay' in key and 'TU' in key:
            addedFilesMcFCNCTUdecay[year].append( key + '.root')
        else:
            addedFilesMcTTX[year].append(key + '.root')
    for key, value in addedFilesData.items():
#        if key != '2016preVFP':
#            continue
        Fmerged=[]
        hadddata = 'hadd ' +key+'_data.root ' + ' '.join(addedFilesData[key])
        haddmcDY ='hadd ' +key+'_DY.root ' + ' '.join(addedFilesMcDY[key])
        haddmcWJets ='hadd ' +key+'_WJets.root ' + ' '.join(addedFilesMcWJets[key])
        haddmcttbar ='hadd ' +key+'_ttbar.root ' + ' '.join(addedFilesMcttbar[key])
        haddmcDiboson ='hadd ' +key+'_Diboson.root ' + ' '.join(addedFilesMcDiboson[key])
        haddmcTriboson ='hadd ' +key+'_Triboson.root ' + ' '.join(addedFilesMcTriboson[key])
        haddmcST ='hadd ' +key+'_ST.root ' + ' '.join(addedFilesMcST[key])
        haddmcTTX ='hadd ' +key+'_TTX.root ' + ' '.join(addedFilesMcTTX[key])
        haddmcConv ='hadd ' +key+'_Conv.root ' + ' '.join(addedFilesMcConv[key])
        haddmcFCNCTCdecay ='hadd ' +key+'_FCNCTCDecay.root ' + ' '.join(addedFilesMcFCNCTCdecay[key])
        haddmcFCNCTCprod ='hadd ' +key+'_FCNCTCProduction.root ' + ' '.join(addedFilesMcFCNCTCprod[key])
        haddmcFCNCTUdecay ='hadd ' +key+'_FCNCTUDecay.root ' + ' '.join(addedFilesMcFCNCTUdecay[key])
        haddmcFCNCTUprod ='hadd ' +key+'_FCNCTUProduction.root ' + ' '.join(addedFilesMcFCNCTUprod[key])
        Fmerged.append(hadddata)
        Fmerged.append(haddmcDY)
        Fmerged.append(haddmcWJets)
        Fmerged.append(haddmcttbar)
        Fmerged.append(haddmcDiboson)
        Fmerged.append(haddmcTriboson)
        Fmerged.append(haddmcTTX)
        Fmerged.append(haddmcST)
        Fmerged.append(haddmcConv)
        Fmerged.append(haddmcFCNCTCdecay)
        Fmerged.append(haddmcFCNCTCprod)
        Fmerged.append(haddmcFCNCTUdecay)
        Fmerged.append(haddmcFCNCTUprod)
        Parallel(n_jobs=10)(delayed(f)(i) for i in Fmerged)
        os.system('hadd ' +key+'_totalBG.root '+key+'_DY.root ' +key+'_WJets.root ' +key+'_ttbar.root ' +key+'_Diboson.root ' +key+'_Triboson.root '+key+'_ST.root ' +key+'_TTX.root ' +key+'_Conv.root ')        
        print hadddata + '\n' + haddmcDY + '\n' + haddmcWJets  + '\n' + haddmcttbar + '\n' + haddmcDiboson + '\n' + haddmcTriboson + '\n' + haddmcTTX + '\n' + haddmcST + '\n' + haddmcConv + '\n' + haddmcFCNCTCdecay + '\n' + haddmcFCNCTCprod + '\n' + haddmcFCNCTUdecay + '\n' + haddmcFCNCTUprod
#    BtagFiles=[]
#    for key, value in addedFilesData.items():
#        text = 'hadd ' + 'mc_' + key + '.root ' + key+'_DY.root ' +key+'_ttbar.root ' +key+'_tW.root '    
#        BtagFiles.append(text)
#    Parallel(n_jobs=4)(delayed(f)(i) for i in BtagFiles)
#
#    AllFiles=[]
#    proc = ['data', 'DY','WJets','ttbar','tW','other',
#'STBNV_TBCE',
#'STBNV_TBUE',
#'STBNV_TDCE',
#'STBNV_TDUE',
#'STBNV_TSCE',
#'STBNV_TSUE',
#'TTBNV_TBCE',
#'TTBNV_TBUE',
#'TTBNV_TDCE',
#'TTBNV_TDUE',
#'TTBNV_TSCE',
#'TTBNV_TSUE',
#'STBNV_TBCMu',
#'STBNV_TBUMu',
#'STBNV_TDCMu',
#'STBNV_TDUMu',
#'STBNV_TSCMu',
#'STBNV_TSUMu',
#'TTBNV_TBCMu',
#'TTBNV_TBUMu',
#'TTBNV_TDCMu',
#'TTBNV_TDUMu',
#'TTBNV_TSCMu',
#'TTBNV_TSUMu']
#    for p in proc:
#        text = 'hadd ' + 'All_' + p + '.root '
#        for key, value in addedFilesData.items():
#            text = text + key+'_'+p+'.root '   
#        AllFiles.append(text)
#
#    Parallel(n_jobs=len(proc))(delayed(f)(i) for i in AllFiles)   
#    addedFilesMcttbarSys = {"hdampUP": [],"hdampDOWN": [], "CR1": [], "CR2": [], "TuneCP5up": [], "TuneCP5down": [], "erdON": [], 'STBNV_TDUE':[], 'STBNV_TDUMu':[]}
#    for keyUL, value in SAMPLES.items():
#        key = keyUL.replace("UL", "20")
#        for keysys, valuesys in addedFilesMcttbarSys.items():
#            if keysys in key:
#                addedFilesMcttbarSys[keysys].append( key + '.root')
#    for keysys, valuesys in addedFilesMcttbarSys.items():
#        os.system( 'hadd All_' + valuesys[0].split('_',1)[1] + ' '+ ' '.join(addedFilesMcttbarSys[keysys]) )



