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
    addedFilesMcElse = {"2016preVFP": [],"2016postVFP": [], "2017": [], "2018": []}
    addedFilesMcttbar = {"2016preVFP": [],"2016postVFP": [], "2017": [], "2018": []}
    addedFilesMcDiboson = {"2016preVFP": [],"2016postVFP": [], "2017": [], "2018": []}
    addedFilesMcTriboson = {"2016preVFP": [],"2016postVFP": [], "2017": [], "2018": []}
    addedFilesMcTTZ = {"2016preVFP": [],"2016postVFP": [], "2017": [], "2018": []}
    addedFilesMcTTW = {"2016preVFP": [],"2016postVFP": [], "2017": [], "2018": []}
    addedFilesMcTTH = {"2016preVFP": [],"2016postVFP": [], "2017": [], "2018": []}
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
        elif 'TTG' in key or 'ZG' in key or 'TGJets' in key or  'WGToLNuG' in key:
            addedFilesMcConv[year].append( key + '.root')
        elif 'TTTo' in key and 'sys' not in key:
            addedFilesMcttbar[year].append( key + '.root')
#        elif 'WWTo' in key or 'WZTo' in key or 'ZZTo' in key or 'ZGTo' in key:
        elif '_WWTo' in key or '_WZTo' in key or '_ZZTo' in key:
            addedFilesMcDiboson[year].append( key + '.root')
        elif 'WWW' in key or 'WWZ' in key or 'WZZ' in key or 'ZZZ' in key:
            addedFilesMcTriboson[year].append( key + '.root')
        elif 'ST' in key or 'tW' in key or 'tbarW' in key or 'tZq' in key:
            addedFilesMcST[year].append( key + '.root')
        elif 'Production' in key and 'TC' in key:
            addedFilesMcFCNCTCprod[year].append( key + '.root')
        elif 'Decay' in key and 'TC' in key:
            addedFilesMcFCNCTCdecay[year].append( key + '.root')
        elif 'Production' in key and 'TU' in key:
            addedFilesMcFCNCTUprod[year].append( key + '.root')
        elif 'Decay' in key and 'TU' in key:
            addedFilesMcFCNCTUdecay[year].append( key + '.root')
        elif 'TTZToLL' in key:
            addedFilesMcTTZ[year].append(key + '.root')
        elif 'ttHnobb' in key:
            addedFilesMcTTH[year].append(key + '.root')
        elif 'TTWJetsToLNu' in key or 'ttWJetsToLNu_EWK' in key:
            addedFilesMcTTW[year].append(key + '.root')
        else:
            addedFilesMcElse[year].append(key + '.root')
    for key, value in addedFilesData.items():
#        if key != '2016preVFP':
#            continue
        Fmerged=[]
        hadddata = 'hadd -f ' +key+'_data.root ' + ' '.join(addedFilesData[key])
        haddmcDY ='hadd -f ' +key+'_DY.root ' + ' '.join(addedFilesMcDY[key])
        haddmcElse ='hadd -f ' +key+'_Else.root ' + ' '.join(addedFilesMcElse[key])
        haddmcttbar ='hadd -f ' +key+'_ttbar.root ' + ' '.join(addedFilesMcttbar[key])
        haddmcDiboson ='hadd -f ' +key+'_Diboson.root ' + ' '.join(addedFilesMcDiboson[key])
        haddmcTriboson ='hadd -f ' +key+'_Triboson.root ' + ' '.join(addedFilesMcTriboson[key])
        haddmcST ='hadd -f ' +key+'_ST.root ' + ' '.join(addedFilesMcST[key])
        haddmcTTH ='hadd -f ' +key+'_TTH.root ' + ' '.join(addedFilesMcTTH[key])
        haddmcTTW ='hadd -f ' +key+'_TTW.root ' + ' '.join(addedFilesMcTTW[key])
        haddmcTTZ ='hadd -f ' +key+'_TTZ.root ' + ' '.join(addedFilesMcTTZ[key])
        haddmcConv ='hadd -f ' +key+'_Conv.root ' + ' '.join(addedFilesMcConv[key])
        haddmcFCNCTCdecay ='hadd -f ' +key+'_FCNCTCDecay.root ' + ' '.join(addedFilesMcFCNCTCdecay[key])
        haddmcFCNCTCprod ='hadd -f ' +key+'_FCNCTCProduction.root ' + ' '.join(addedFilesMcFCNCTCprod[key])
        haddmcFCNCTUdecay ='hadd -f ' +key+'_FCNCTUDecay.root ' + ' '.join(addedFilesMcFCNCTUdecay[key])
        haddmcFCNCTUprod ='hadd -f ' +key+'_FCNCTUProduction.root ' + ' '.join(addedFilesMcFCNCTUprod[key])
        Fmerged.append(hadddata)
        Fmerged.append(haddmcDY)
        Fmerged.append(haddmcElse)
        Fmerged.append(haddmcttbar)
        Fmerged.append(haddmcDiboson)
        Fmerged.append(haddmcTriboson)
        Fmerged.append(haddmcTTW)
        Fmerged.append(haddmcTTZ)
        Fmerged.append(haddmcTTH)
        Fmerged.append(haddmcST)
        Fmerged.append(haddmcConv)
        Fmerged.append(haddmcFCNCTCdecay)
        Fmerged.append(haddmcFCNCTCprod)
        Fmerged.append(haddmcFCNCTUdecay)
        Fmerged.append(haddmcFCNCTUprod)
        Parallel(n_jobs=10)(delayed(f)(i) for i in Fmerged)
        os.system('hadd ' +key+'_totalBG.root '+key+'_DY.root ' +key+'_Else.root ' +key+'_ttbar.root ' +key+'_Diboson.root ' +key+'_Triboson.root '+key+'_ST.root ' +key+'_TTZ.root ' +key+'_TTW.root '+key+'_TTH.root '+key+'_Conv.root ')        
        print '\n \n \n hadddata:' + hadddata + '\n haddmcDY:' + haddmcDY + '\n haddmcElse:' + haddmcElse  + '\n haddmcttbar:' + haddmcttbar + '\n haddmcDiboson:' + haddmcDiboson + '\n haddmcTriboson:' + haddmcTriboson + '\n haddmcTTH:' + haddmcTTH+ '\n haddmcTTW:' + haddmcTTW+ '\n haddmcTTZ:' + haddmcTTZ + '\n haddmcST:' + haddmcST + '\n haddmcConv:' + haddmcConv + '\n haddmcFCNCTCdecay:' + haddmcFCNCTCdecay + '\n haddmcFCNCTCprod:' + haddmcFCNCTCprod + '\n haddmcFCNCTUdecay:' + haddmcFCNCTUdecay + '\n haddmcFCNCTUprod' + haddmcFCNCTUprod

