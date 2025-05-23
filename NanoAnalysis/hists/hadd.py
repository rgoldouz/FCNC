import sys
import os
import subprocess
import readline
import string
import glob

sys.path.append('/afs/crc.nd.edu/user/r/rgoldouz/BNV/NanoAnalysis/bin/')
import Files_2017_nano
SAMPLES = {}
SAMPLES.update(Files_2017_nano.UL17)


addedFilesData = {"2016": [], "2017": [], "2018": []} 
addedFilesMcDY = {"2016": [], "2017": [], "2018": []}
addedFilesMcWJets = {"2016": [], "2017": [], "2018": []}
addedFilesMcttbar = {"2016": [], "2017": [], "2018": []}
addedFilesMctW = {"2016": [], "2017": [], "2018": []}
addedFilesMcother = {"2016": [], "2017": [], "2018": []}

os.system('rm *.root')
dist = "/hadoop/store/user/rgoldouz/FullProduction/TOPBNVAnalysis/Analysis_" 

for key, value in SAMPLES.items():
    year = value[3]
    hadd='hadd ' + key + '.root '
    for filename in os.listdir(dist + key):
        hadd += dist + key + '/' + filename + ' '
    os.system(hadd)
    if value[1]=='data':
        addedFilesData[year].append(key + '.root')
    elif 'DY' in key:
        addedFilesMcDY[year].append( key + '.root')
    elif 'WJetsToLNu' in key:
        addedFilesMcWJets[year].append(key + '.root')
    elif 'TTTo2L2Nu' in key:
        addedFilesMcttbar[year].append( key + '.root')
    elif 'tW' in key or 'tbarW' in key:
        addedFilesMctW[year].append( key + '.root')
    elif 'BNV' in key or 'FCNC' in key:
        os.system('mv ' + key + '.root ' + key.replace("UL17", "2017")+ '.root ') 
    else:
        addedFilesMcother[year].append(key + '.root')




#    print glob.glob("/hadoop/store/user/rgoldouz/FullProduction/Analysis/Analysis_"  + key + '/*.root')
#    year = value[3]
#    if value[1]=='data':
#        addedFilesData[year].append(glob.glob("/hadoop/store/user/rgoldouz/FullProduction/Analysis/Analysis_"  + key + '/*.root')[0])
#    elif 'QCDHT' in key:
#        addedFilesMcQCDHT[year].append(glob.glob("/hadoop/store/user/rgoldouz/FullProduction/Analysis/Analysis_"  + key + '/*.root')[0])
#    elif 'GJets' in key:
#        addedFilesMcGJets[year].append(glob.glob("/hadoop/store/user/rgoldouz/FullProduction/Analysis/Analysis_"  + key + '/*.root')[0])
#    elif 'WG' in key:
#        addedFilesMcWG[year].append(glob.glob("/hadoop/store/user/rgoldouz/FullProduction/Analysis/Analysis_"  + key + '/*.root')[0])
#    elif 'DY' in key:
#        addedFilesMcDY[year].append(glob.glob("/hadoop/store/user/rgoldouz/FullProduction/Analysis/Analysis_"  + key + '/*.root')[0])
#    elif ('tt' in key or 'ST' in key):
#        addedFilesMctop[year].append(glob.glob("/hadoop/store/user/rgoldouz/FullProduction/Analysis/Analysis_"  + key + '/*.root')[0])
#    else:
#        os.system('cp ' + glob.glob("/hadoop/store/user/rgoldouz/FullProduction/Analysis/Analysis_"  + key + '/*.root')[0] + ' ' + key + '.root')


hadddata_2017 ='hadd 2017_data' + '.root ' + ' '.join(addedFilesData['2017'])
os.system(hadddata_2017)

haddmc_2017_McDY ='hadd 2017_DY' + '.root ' + ' '.join(addedFilesMcDY['2017'])
haddmc_2017_McWJets ='hadd 2017_WJets' + '.root ' + ' '.join(addedFilesMcWJets['2017'])
haddmc_2017_Mcttbar ='hadd 2017_ttbar' + '.root ' + ' '.join(addedFilesMcttbar['2017'])
haddmc_2017_MctW ='hadd 2017_tW' + '.root ' + ' '.join(addedFilesMctW['2017'])
haddmc_2017_Mcother ='hadd 2017_other' + '.root ' + ' '.join(addedFilesMcother['2017'])

print haddmc_2017_McDY
print haddmc_2017_McWJets
print haddmc_2017_Mcttbar
print haddmc_2017_MctW
print haddmc_2017_Mcother

os.system(haddmc_2017_McDY)
os.system(haddmc_2017_McWJets)
os.system(haddmc_2017_Mcttbar)
os.system(haddmc_2017_MctW)
os.system(haddmc_2017_Mcother)

