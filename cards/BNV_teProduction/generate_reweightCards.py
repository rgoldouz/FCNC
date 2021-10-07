import os
import random

#couplings =['ctG','cQq83','cQq81','ctq8']
#couplings =['cpQM','cpQ3','cpt','ctW','ctZ','ctG','cQq83','cQq81','cQu8','cQd8','ctq8','ctu8','ctd8','cQq13','cQq11','cQu1','cQd1','ctq1','ctu1','ctd1']
#couplings =[['ctpx31','ctpx13'],['cpQMx31','cpQMx13'],['cpQ3x31','cpQ3x13'],['cptx31','cptx13'],['cptbx31','cptbx13'],['ctAx31','ctAx13'],['ctZx31','ctZx13'],['cbWx31','cbWx13'],['ctGx31','ctGx13'],['cQl3x1x31','cQl3x2x31','cQl3x3x31','cQl3x1x13','cQl3x2x13','cQl3x3x13'],['cQlMx1x31','cQlMx2x31','cQlMx3x31','cQlMx1x13','cQlMx2x13','cQlMx3x13'],['cQex1x31','cQex2x31','cQex3x31','cQex1x13','cQex2x13','cQex3x13'],['ctlx1x31','ctlx2x31','ctlx3x31','ctlx1x13','ctlx2x13','ctlx3x13'],['ctex1x31','ctex2x31','ctex3x31','ctex1x13','ctex2x13','ctex3x13'],['ctlSx1x13','ctlSx2x13','ctlSx3x13','ctlSx1x31','ctlSx2x31','ctlSx3x31'],['ctlTx1x13','ctlTx2x13','ctlTx3x13','ctlTx1x31','ctlTx2x31','ctlTx3x31']]
couplings =[
['CStdue',0.1],  
['CStdce',1 ],
['CStsue',1 ],
['CStsce',10],
['CStbue',1 ],
['CStbce',10],
['CTtdue',0.1],
['CTtdce',1 ],
['CTtsue',1 ],
['CTtsce',10],
['CTtbue',1 ],
['CTtbce',10]
]
customizecards = ''

scanValues = 120

for WC in couplings:
    customizecards = customizecards + 'set param_card '+WC[0]+ ' ' + str(WC[1]) + '\n'     
open('BNV_teProduction_customizecards.dat', 'wt').write(customizecards)
n=-1
rwgtCards = ''
rwgtCards = rwgtCards + 'change rwgt_dir rwgt'+ '\n'+ '\n'
#dummy_point
rwgtCards = rwgtCards + 'launch --rwgt_name=reference_point'+ '\n'
rwgtCards = rwgtCards +'\n'
#other points
for v in range(scanValues):
    randomWC = []
    for WC in couplings:
        r = random.uniform(-2*WC[1], 2*WC[1])
        randomWC.append(round(r,3))
    n  = n+1
    rwgtCards = rwgtCards + '\n'
    rwgtCards = rwgtCards + 'launch --rwgt_name=EFTrwgt' + str(n) + '_'
    for count,WC1 in enumerate(couplings):
        rwgtCards = rwgtCards + WC1[0] + '_' + str(randomWC[count]) + '_'
    rwgtCards = rwgtCards[:-1]
    rwgtCards = rwgtCards + '\n'
    for count,WC1 in enumerate(couplings):
        rwgtCards = rwgtCards +'    set param_card ' + WC1[0] + ' ' + str(randomWC[count])  + '\n'
open('BNV_teProduction_reweight_card.dat', 'wt').write(rwgtCards)
os.system('rm -rf BNV_teProduction')
os.system('mkdir BNV_teProduction')
process = ''
process = process + 'import model bnv-Reza --modelname' + '\n'
process = process + 'define p = g u c d s u~ c~ d~ s~ b b~' + '\n'
process = process + 'define j = g u c d s u~ c~ d~ s~ b b~' + '\n'
process = process + 'define l+ = e+ m+ tt+' + '\n'
process = process + 'define l- = e- m- tt-' + '\n'
process = process + 'generate  p p > t~ e+  @0' + '\n'
process = process + 'add process  p p > t e- @1' + '\n'
process = process + 'output BNV_teProduction  -f -nojpeg'
open('BNV_teProduction_proc_card.dat', 'wt').write(process)
os.system('mv BNV_teProduction_proc_card.dat BNV_teProduction')
os.system('cp BNV_teProduction_reweight_card.dat BNV_teProduction/BNV_teProduction_reweight_card.dat')
os.system('cp BNV_teProduction_customizecards.dat BNV_teProduction/BNV_teProduction_customizecards.dat')
os.system('cp tllFCNC_run_card.dat BNV_teProduction/BNV_teProduction_run_card.dat')
#os.system('cp tllFCNC_extramodels.dat BNV_teProduction/BNV_teProduction_extramodels.dat')

#for WC1 in couplingsName:
#    os.system('rm -rf tllFCNC'+WC1)
#    os.system('rm -rf tllFcncProduction'+WC1)
#    os.system('rm -rf BNV_teProduction'+WC1)
#    os.system('mkdir BNV_teProduction'+WC1)
#    os.system('cp tllFCNC_extramodels.dat BNV_teProduction'+WC1 + '/BNV_teProduction'+WC1 +'_extramodels.dat')
#    os.system('cp tllFCNC_run_card.dat BNV_teProduction'+WC1 + '/BNV_teProduction'+WC1 +'_run_card.dat')
##    os.system('cp tllFCNC_madspin_card.dat BNV_teProduction'+WC1 + '/BNV_teProduction'+WC1 +'_madspin_card.dat')
#    os.system('cp tllFCNC_extramodels.dat BNV_teProduction'+WC1 + '/BNV_teProduction'+WC1 +'_extramodels.dat')
##    os.system('cp tllFCNC_proc_card.dat tllFCNC'+WC1 + '/tllFCNC'+WC1 +'_proc_card.dat')
#    Ccards = ''
#    Ccards = Ccards + '    set param_card mass   6  172.5\n'
#    Ccards = Ccards + '    set param_card yukawa 6  172.5\n'
#    Ccards = Ccards + '    set param_card mass   25 125.0\n'
##    Ccards = Ccards + 'set dynamical_scale_choice 3\n'
#    for WC2 in couplingsName:
#        if WC1 == WC2:
#            for wcIndex in couplings[couplingsName.index(WC2)]:
#                Ccards = Ccards +'    set param_card ' + wcIndex + ' ' + str(1)  + '\n'
#        else:
#            for wcIndex in couplings[couplingsName.index(WC2)]:
#                Ccards = Ccards  + '    set param_card ' + wcIndex + ' 0.0001'  + '\n'
#    open('BNV_teProduction'+WC1+'_customizecards.dat', 'wt').write(Ccards)
#    os.system('mv BNV_teProduction'+WC1+'_customizecards.dat BNV_teProduction'+WC1)
#    process = ''
##    if WC1 in C4F:
##        process = process + 'import model dim6top_LO_UFO-' + WC1 + ' --modelname' + '\n'
##    else:
##        process = process + 'import model dim6top_LO_UFO-full --modelname' + '\n'
#    process = process + 'import model dim6top_LO_UFO-full --modelname' + '\n'
#    process = process + 'define p = g u c d s u~ c~ d~ s~' + '\n'
#    process = process + 'define j = g u c d s u~ c~ d~ s~' + '\n'
#    process = process + 'define l+ = e+ mu+ ta+' + '\n'
#    process = process + 'define l- = e- mu- ta-' + '\n'
#    process = process + 'generate  p p > t h DIM6=0 FCNC=1 , (t > w+ b DIM6=0 FCNC=0, w+ > l+ vl DIM6=0 FCNC=0)@0' + '\n'
#    process = process + 'add process  p p > t~ h DIM6=0 FCNC=1 , (t~ > w- b~ DIM6=0 FCNC=0, w- > l- vl~ DIM6=0 FCNC=0) @1' + '\n'
#    process = process + 'output BNV_teProduction' + WC1 + ' -f -nojpeg'
#    open('BNV_teProduction'+WC1 +'_proc_card.dat', 'wt').write(process)
#    os.system('mv BNV_teProduction'+WC1+'_proc_card.dat BNV_teProduction'+WC1)
#
