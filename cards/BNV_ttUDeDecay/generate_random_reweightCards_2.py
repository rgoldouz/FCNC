import os
import random

#see Eq.2 in https://arxiv.org/pdf/1107.3805.pdf

#S-ch = tDUE
#T-ch = tEUD

MG = [
['generate  p p > t t~ BNV=0 /h a z ,  (t > u~ d~ e+) @0','add process  p p > t t~ BNV=0 /h a z , (t~ > u d e-)@1'],
['generate  p p > t t~ BNV=0 /h a z ,  (t > c~ d~ e+) @0','add process  p p > t t~ BNV=0 /h a z , (t~ > c d e-)@1'],
['generate  p p > t t~ BNV=0 /h a z ,  (t > u~ s~ e+) @0','add process  p p > t t~ BNV=0 /h a z , (t~ > u s e-)@1'],
['generate  p p > t t~ BNV=0 /h a z ,  (t > c~ s~ e+) @0','add process  p p > t t~ BNV=0 /h a z , (t~ > c s e-)@1'],
['generate  p p > t t~ BNV=0 /h a z ,  (t > u~ b~ e+) @0','add process  p p > t t~ BNV=0 /h a z , (t~ > u b e-)@1'],
['generate  p p > t t~ BNV=0 /h a z ,  (t > c~ b~ e+) @0','add process  p p > t t~ BNV=0 /h a z , (t~ > c b e-)@1'],
]

processName=[
'TDUE',
'TDCE',
'TSUE',
'TSCE',
'TBUE',
'TBCE',
]

couplingsName = [
['cS','cT'],
['cS','cT'],
['cS','cT'],
['cS','cT'],
['cS','cT'],
['cS','cT']
]


couplings =[
[['aaa3x1','bbb3x1','ccc1x1','ddd1x1'],['aaaprime3x1','bbbprime3x1','cccprime1x1','dddprime1x1']],
[['aaa3x1','bbb3x1','ccc2x1','ddd2x1'],['aaaprime3x1','bbbprime3x1','cccprime2x1','dddprime2x1']],
[['aaa3x2','bbb3x2','ccc1x1','ddd1x1'],['aaaprime3x1','bbbprime3x1','cccprime1x2','dddprime1x2']],
[['aaa3x2','bbb3x2','ccc2x1','ddd2x1'],['aaaprime3x1','bbbprime3x1','cccprime2x2','dddprime2x2']],
[['aaa3x3','bbb3x3','ccc1x1','ddd1x1'],['aaaprime3x1','bbbprime3x1','cccprime1x3','dddprime1x3']],
[['aaa3x3','bbb3x3','ccc2x1','ddd2x1'],['aaaprime3x1','bbbprime3x1','cccprime2x3','dddprime2x3']]
#['aaaprime3x1','bbbprime3x1','cccprime1x1','dddprime1x1'],
#['aaaprime3x1','bbbprime3x1','cccprime2x1','dddprime2x1'],
#['aaaprime3x1','bbbprime3x1','cccprime1x2','dddprime1x2'],
#['aaaprime3x1','bbbprime3x1','cccprime2x2','dddprime2x2'],
#['aaaprime3x1','bbbprime3x1','cccprime1x3','dddprime1x3'],
#['aaaprime3x1','bbbprime3x1','cccprime2x3','dddprime2x3'],
]

scanValues = 20

for num, name in enumerate(processName):
    os.system('rm -rf BNV_TT_' + name)
    os.system('mkdir BNV_TT_' + name)
    customizecards = ''
    customizecards = customizecards + 'set param_card mass   6  172.5\n'
    customizecards = customizecards + 'set param_card yukawa 6  172.5\n'
    customizecards = customizecards + 'set param_card mass   25 125.0\n'
    customizecards = customizecards + 'set dynamical_scale_choice 3\n'
    for gWC in couplings[num]:
        for WC in gWC:
            customizecards = customizecards + 'set param_card '+WC+ ' ' + str(1) + '\n'     
    open('BNV_TT_' + name + '/BNV_TT_' + name + '_customizecards.dat', 'wt').write(customizecards)
    n=-1
    rwgtCards = ''
    rwgtCards = rwgtCards + 'change rwgt_dir rwgt'+ '\n'+ '\n'
    for v in range(scanValues):
        randomWC = []
        for WC1 in couplingsName[num]:
            r = random.uniform(0,10)
            randomWC.append(round(r,2))
        n  = n+1
        rwgtCards = rwgtCards + '\n'
        rwgtCards = rwgtCards + 'launch --rwgt_name=EFTrwgt' + str(n) + '_'
        for WC1 in couplingsName[num]:
            rwgtCards = rwgtCards + WC1 + '_' + str(randomWC[couplingsName[num].index(WC1)]) + '_'
        rwgtCards = rwgtCards[:-1]
        rwgtCards = rwgtCards + '\n'
        for WC1 in couplingsName[num]:
            for wcIndex in couplings[num][couplingsName[num].index(WC1)]:
                rwgtCards = rwgtCards +'    set param_card ' + wcIndex + ' ' + str(randomWC[couplingsName[num].index(WC1)])  + '\n'
    open('BNV_TT_' + name + '/BNV_TT_' + name + '_reweight_card.dat', 'wt').write(rwgtCards)
    
    process = ''
    process = process + 'import model bnv_mediator_ufo' + '\n'
    process = process + 'define p = g u c d s u~ c~ d~ s~' + '\n'
    process = process + MG[num][0] + '\n'
    process = process + MG[num][1] + '\n'
    process = process + 'output BNV_TT_' + name + ' -f -nojpeg'
    open('BNV_TT_' + name + '/BNV_TT_' + name + '_proc_card.dat', 'wt').write(process)
    os.system('cp tllFCNC_run_card.dat BNV_TT_' + name + '/BNV_TT_' + name + '_run_card.dat')

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
#    process = process + 'generate  p p > t  l+ l- /h DIM6=0 FCNC=1 , (t > w+ b DIM6=0 FCNC=0, w+ > l+ vl DIM6=0 FCNC=0)@0' + '\n'
#    process = process + 'add process  p p > t~  l+ l- /h DIM6=0 FCNC=1 , (t~ > w- b~ DIM6=0 FCNC=0, w- > l- vl~ DIM6=0 FCNC=0) @1' + '\n'
#    process = process + 'output BNV_teProduction' + WC1 + ' -f -nojpeg'
#    open('BNV_teProduction'+WC1 +'_proc_card.dat', 'wt').write(process)
#    os.system('mv BNV_teProduction'+WC1+'_proc_card.dat BNV_teProduction'+WC1)

