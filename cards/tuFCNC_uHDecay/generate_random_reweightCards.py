import os
import random


couplings =[['ctpx31','ctpx13']]
couplingsName = ['ctp']
Ivalue        = [3]

customizecards = ''
customizecards = customizecards + 'set param_card mass   6  172.5\n'
customizecards = customizecards + 'set param_card yukawa 6  172.5\n'
customizecards = customizecards + 'set param_card mass   25 125.0\n'

customizecards = ''
customizecards = customizecards + 'set param_card mass   6  172.5\n'
customizecards = customizecards + 'set param_card yukawa 6  172.5\n'
customizecards = customizecards + 'set param_card mass   25 125.0\n'
#customizecards = customizecards + 'set dynamical_scale_choice 3\n'

scanValues = 20

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
        rwgtCards = rwgtCards + WC1 + '_' + str(randomWC[couplingsName.index(WC1)]) + '_'
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
process = process + 'generate  p p > t  t~ DIM6=0 FCNC=0 , (t~ > u~ h DIM6=0 FCNC=1) , (t  > w+ b DIM6=0 FCNC=0,  w+ > l+ vl DIM6=0 FCNC=0 ) @0' + '\n'
process = process + 'add process  p p > t t~  DIM6=0 FCNC=0 , (t~  > w- b~ DIM6=0 FCNC=0,  w- > l- vl~ DIM6=0 FCNC=0 ), (t > u h DIM6=0 FCNC=1) @1' + '\n'
process = process + 'output tuFCNC_uHDecay -f -nojpeg'
open('tuFCNC_uHDecay_proc_card.dat', 'wt').write(process)
os.system('mv tuFCNC_uHDecay_proc_card.dat tuFCNC_uHDecay')
os.system('cp tllFCNC_reweight_card.dat tuFCNC_uHDecay/tuFCNC_uHDecay_reweight_card.dat')
os.system('cp tllFCNC_customizecards.dat tuFCNC_uHDecay/tuFCNC_uHDecay_customizecards.dat')
os.system('cp tllFCNC_run_card.dat tuFCNC_uHDecay/tuFCNC_uHDecay_run_card.dat')
os.system('cp tllFCNC_extramodels.dat tuFCNC_uHDecay/tuFCNC_uHDecay_extramodels.dat')

