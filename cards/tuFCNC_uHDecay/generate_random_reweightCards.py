import os
import random

couplings =[['cpQMx31'],['cptx31'],['ctAx31','ctAx13'],['ctZx31','ctZx13'],['ctGx31','ctGx13'],['cQlMx1x31','cQlMx2x31','cQlMx3x31'],['cQex1x31','cQex2x31','cQex3x31'],['ctlx1x31','ctlx2x31','ctlx3x31'],['ctex1x31','ctex2x31','ctex3x31'],['ctlSx1x13','ctlSx2x13','ctlSx3x13','ctlSx1x31','ctlSx2x31','ctlSx3x31'],['ctlTx1x13','ctlTx2x13','ctlTx3x13','ctlTx1x31','ctlTx2x31','ctlTx3x31'],['ctpx31','ctpx13']]
couplingsName = ['cpQM','cpt','ctA','ctZ','ctG','cQlM','cQe','ctl','cte','ctlS','ctlT', 'ctp']
#Ivalue        = [2     ,2    ,1    ,0.5   ,0.2  ,1.5    ,1.5  ,1.5  ,2  ,2.5     ,0.7    ]
Ivalue        = [0.285     ,0.285    ,0.264    ,0.075   ,0.0158  ,0.14    ,0.14  ,0.14  ,0.14  ,0.14     ,0.03, 3]

customizecards = ''
customizecards = customizecards + 'set param_card mass   6  172.5\n'
customizecards = customizecards + 'set param_card yukawa 6  172.5\n'
customizecards = customizecards + 'set param_card mass   25 125.0\n'

customizecards = ''
customizecards = customizecards + 'set param_card mass   6  172.5\n'
customizecards = customizecards + 'set param_card yukawa 6  172.5\n'
customizecards = customizecards + 'set param_card mass   25 125.0\n'
#customizecards = customizecards + 'set dynamical_scale_choice 3\n'

scanValues = 100

for gWC in couplings:
    for WC in gWC:
        customizecards = customizecards + 'set param_card '+WC+ ' ' + str(Ivalue[couplings.index(gWC)]) + '\n'     
open('tllFCNC_customizecards.dat', 'wt').write(customizecards)
n=-1
rwgtCards = ''
rwgtCards = rwgtCards + 'change rwgt_dir rwgt'+ '\n'+ '\n'

#dummy_point
rwgtCards = rwgtCards + 'launch --rwgt_name=reference_point'+ '\n'
rwgtCards = rwgtCards +'\n'

#other points
for v in range(scanValues):
    randomWC = []
    for WC1 in couplingsName:
        r = random.uniform(-2*Ivalue[couplingsName.index(WC1)], 2*Ivalue[couplingsName.index(WC1)])
        randomWC.append(round(r,3))
    n  = n+1
    rwgtCards = rwgtCards + '\n'
    rwgtCards = rwgtCards + 'launch --rwgt_name=EFTrwgt' + str(n) + '_'
    for WC1 in couplingsName:
        idWgt = str(randomWC[couplingsName.index(WC1)])
        idWgt= idWgt.replace(".", "p" )
        idWgt =idWgt.replace("-", "m" )
        rwgtCards = rwgtCards + WC1 + '_' + idWgt + '_'
    rwgtCards = rwgtCards[:-1]
    rwgtCards = rwgtCards + '\n'
    for WC1 in couplingsName:
        for wcIndex in couplings[couplingsName.index(WC1)]:
            rwgtCards = rwgtCards +'    set param_card ' + wcIndex + ' ' + str(randomWC[couplingsName.index(WC1)])  + '\n'
open('tllFCNC_reweight_card.dat', 'wt').write(rwgtCards)
os.system('rm -rf tuFCNC_uHDecay')
os.system('mkdir tuFCNC_uHDecay')
process = ''
process = process + 'import model dim6top_LO_UFO-full --modelname' + '\n'
process = process + 'define p = g u c d s u~ c~ d~ s~' + '\n'
process = process + 'define j = g u c d s u~ c~ d~ s~' + '\n'
process = process + 'define ell+ = e+ mu+ ta+' + '\n'
process = process + 'define ell- = e- mu- ta-' + '\n'
process = process + 'define vell = ve vm vt' + '\n'
process = process + 'define vell~ = ve~ vm~ vt~' + '\n'
process = process + 'generate  p p > t  t~ DIM6=0 FCNC=0 , (t~ > u~ h DIM6=0 FCNC=1) , (t  > w+ b DIM6=0 FCNC=0,  w+ > ell+ vell DIM6=0 FCNC=0 ) @0' + '\n'
process = process + 'add process  p p > t t~  DIM6=0 FCNC=0 , (t~  > w- b~ DIM6=0 FCNC=0,  w- > ell- vell~ DIM6=0 FCNC=0 ), (t > u h DIM6=0 FCNC=1) @1' + '\n'
process = process + 'output tuFCNC_uHDecay -f -nojpeg'
open('tuFCNC_uHDecay_proc_card.dat', 'wt').write(process)
os.system('mv tuFCNC_uHDecay_proc_card.dat tuFCNC_uHDecay')
os.system('cp tllFCNC_reweight_card.dat tuFCNC_uHDecay/tuFCNC_uHDecay_reweight_card.dat')
os.system('cp tllFCNC_customizecards.dat tuFCNC_uHDecay/tuFCNC_uHDecay_customizecards.dat')
os.system('cp tllFCNC_run_card.dat tuFCNC_uHDecay/tuFCNC_uHDecay_run_card.dat')
os.system('cp tllFCNC_extramodels.dat tuFCNC_uHDecay/tuFCNC_uHDecay_extramodels.dat')

