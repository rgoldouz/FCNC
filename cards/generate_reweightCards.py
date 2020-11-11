import os


#couplings =['ctG','cQq83','cQq81','ctq8']
#couplings =['cpQM','cpQ3','cpt','ctW','ctZ','ctG','cQq83','cQq81','cQu8','cQd8','ctq8','ctu8','ctd8','cQq13','cQq11','cQu1','cQd1','ctq1','ctu1','ctd1']
#couplings =[['ctpx31','ctpx13'],['cpQMx31','cpQMx13'],['cpQ3x31','cpQ3x13'],['cptx31','cptx13'],['cptbx31','cptbx13'],['ctAx31','ctAx13'],['ctZx31','ctZx13'],['cbWx31','cbWx13'],['ctGx31','ctGx13'],['cQl3x1x31','cQl3x2x31','cQl3x3x31','cQl3x1x13','cQl3x2x13','cQl3x3x13'],['cQlMx1x31','cQlMx2x31','cQlMx3x31','cQlMx1x13','cQlMx2x13','cQlMx3x13'],['cQex1x31','cQex2x31','cQex3x31','cQex1x13','cQex2x13','cQex3x13'],['ctlx1x31','ctlx2x31','ctlx3x31','ctlx1x13','ctlx2x13','ctlx3x13'],['ctex1x31','ctex2x31','ctex3x31','ctex1x13','ctex2x13','ctex3x13'],['ctlSx1x13','ctlSx2x13','ctlSx3x13','ctlSx1x31','ctlSx2x31','ctlSx3x31'],['ctlTx1x13','ctlTx2x13','ctlTx3x13','ctlTx1x31','ctlTx2x31','ctlTx3x31']]
couplings =[['ctpx31','ctpx13'],['cpQMx31'],['cpQ3x31'],['cptx31'],['cptbx31','cptbx13'],['ctAx31','ctAx13'],['ctZx31','ctZx13'],['cbWx31','cbWx13'],['ctGx31','ctGx13'],['cQl3x1x31','cQl3x2x31','cQl3x3x31'],['cQlMx1x31','cQlMx2x31','cQlMx3x31'],['cQex1x31','cQex2x31','cQex3x31'],['ctlx1x31','ctlx2x31','ctlx3x31'],['ctex1x31','ctex2x31','ctex3x31'],['ctlSx1x13','ctlSx2x13','ctlSx3x13','ctlSx1x31','ctlSx2x31','ctlSx3x31'],['ctlTx1x13','ctlTx2x13','ctlTx3x13','ctlTx1x31','ctlTx2x31','ctlTx3x31']]
couplingsName = ['ctp','cpQM','cpQ3','cpt','cptb','ctA','ctZ','cbW','ctG','cQl3','cQlM','cQe','ctl','cte','ctlS','ctlT']
Ivalue        = [3    ,2     ,10    ,2    ,10    ,1    ,0.25  ,10   ,0.04  ,10  ,1     ,1    ,1    ,1    ,1     ,0.3    ]
C4F = ['cQl3','cQlM','cQe','ctl','cte','ctlS','ctlT']
customizecards = ''
customizecards = customizecards + 'set param_card mass   6  172.5\n'
customizecards = customizecards + 'set param_card yukawa 6  172.5\n'
customizecards = customizecards + 'set param_card mass   25 125.0\n'
customizecards = customizecards + 'set dynamical_scale_choice 3\n'

scanValues = [1]

for gWC in couplings:
    for WC in gWC:
        customizecards = customizecards + 'set param_card '+WC+ ' ' + str(Ivalue[couplings.index(gWC)]) + '\n'     
open('ttllFCNC_customizecards.dat', 'wt').write(customizecards)
n=0
rwgtCards = ''
rwgtCards = rwgtCards + 'change rwgt_dir rwgt'+ '\n'+ '\n'

#dummy_point
rwgtCards = rwgtCards + 'launch --rwgt_name=dummy_point'+ '\n'
rwgtCards = rwgtCards + 'set ctZx31 0.1'+ '\n'
rwgtCards = rwgtCards +'\n'

#other points
for v in scanValues:
   for WC1 in couplingsName:
       n  = n+1
       rwgtCards = rwgtCards + '\n'
       rwgtCards = rwgtCards + 'launch --rwgt_name=EFTrwgt' + str(n) + '_'
       for WC2 in couplingsName:
           if WC1 == WC2:
               rwgtCards = rwgtCards + WC2 + '_' + str(v*Ivalue[couplingsName.index(WC1)]) + '_'
           else:
               rwgtCards = rwgtCards +WC2 + '_' + str(0) + '_'  
       rwgtCards = rwgtCards + '\n'
       for WC2 in couplingsName:
           if WC1 == WC2:
               for wcIndex in couplings[couplingsName.index(WC2)]:
                   rwgtCards = rwgtCards +'    set param_card ' + wcIndex + ' ' + str(v*Ivalue[couplingsName.index(WC1)])  + '\n'
           else:
               for wcIndex in couplings[couplingsName.index(WC2)]:
                   rwgtCards = rwgtCards  + '    set param_card ' + wcIndex + ' 0'  + '\n'
open('ttllFCNC_reweight_card.dat', 'wt').write(rwgtCards)

for WC1 in couplingsName:
    os.system('rm -rf ttllFCNC'+WC1)
    os.system('mkdir ttllFCNC'+WC1)
    os.system('cp ttllFCNC_extramodels.dat ttllFCNC'+WC1 + '/ttllFCNC'+WC1 +'_extramodels.dat')
    os.system('cp ttllFCNC_run_card.dat ttllFCNC'+WC1 + '/ttllFCNC'+WC1 +'_run_card.dat')
#    os.system('cp ttllFCNC_proc_card.dat ttllFCNC'+WC1 + '/ttllFCNC'+WC1 +'_proc_card.dat')
    Ccards = ''
    Ccards = Ccards + 'set param_card mass   6  172.5\n'
    Ccards = Ccards + 'set param_card yukawa 6  172.5\n'
    Ccards = Ccards + 'set param_card mass   25 125.0\n'
    Ccards = Ccards + 'set dynamical_scale_choice 3\n'
    for wcIndex in couplings[couplingsName.index(WC1)]:
        Ccards = Ccards + 'set param_card ' + wcIndex + ' 1' +'\n'
    open('ttllFCNC'+WC1+'_customizecards.dat', 'wt').write(Ccards)
    os.system('mv ttllFCNC'+WC1+'_customizecards.dat ttllFCNC'+WC1)
    process = ''
    if WC1 in C4F:
        process = process + 'import model dim6top_LO_UFO-' + WC1 + ' --modelname' + '\n'
    else:
        process = process + 'import model dim6top_LO_UFO-full --modelname' + '\n'
    process = process + 'define p = g u c d s u~ c~ d~ s~ b b' + '\n'
    process = process + 'define j = g u c d s u~ c~ d~ s~ b b~' + '\n'
    process = process + 'define l+ = e+ mu+ ta+' + '\n'
    process = process + 'define l- = e- mu- ta-' + '\n'
    process = process + 'generate  p p > t  l+ l- DIM6=0 FCNC=1@0' + '\n'
    process = process + 'add process p p > t~  l+ l- DIM6=0 FCNC=1@01' + '\n'
    process = process + 'output ttllFCNC' + WC1 + ' -f -nojpeg'
    open('ttllFCNC'+WC1 +'_proc_card.dat', 'wt').write(process)
    os.system('mv ttllFCNC'+WC1+'_proc_card.dat ttllFCNC'+WC1)

