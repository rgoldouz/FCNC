import os


#couplings =['ctG','cQq83','cQq81','ctq8']
#couplings =['cpQM','cpQ3','cpt','ctW','ctZ','ctG','cQq83','cQq81','cQu8','cQd8','ctq8','ctu8','ctd8','cQq13','cQq11','cQu1','cQd1','ctq1','ctu1','ctd1']
couplings =[['ctpx31','ctpx13'],['cpQMx31'],['cpQ3x31'],['cptx31'],['cptbx31','cptbx13'],['ctAx31','ctAx13'],['ctZx31','ctZx13'],['cbWx31','cbWx13'],['ctGx31','ctGx13'],['cQl3x1x31','cQl3x2x31','cQl3x3x31'],['cQlMx1x31','cQlMx2x31','cQlMx3x31'],['cQex1x31','cQex2x31','cQex3x31'],['ctlx1x31','ctlx2x31','ctlx3x31'],['ctex1x31','ctex2x31','ctex3x31'],['ctlSx1x13','ctlSx2x13','ctlSx3x13','ctlSx1x31','ctlSx2x31','ctlSx3x31'],['ctlTx1x13','ctlTx2x13','ctlTx3x13','ctlTx1x31','ctlTx2x31','ctlTx3x31']]
couplingsName = ['ctp','cpQM','cpQ3','cpt','cptb','ctA','ctZ','cbW','ctG','cQl3','cQlM','cQe','ctl','cte','ctlS','ctlT']
Ivalue        = [1    ,1     ,1     ,1    ,1     ,1    ,1    ,1    ,1    ,1     ,1     ,1    ,1    ,1    ,1     ,1     ]
customizecards = ''
customizecards = customizecards + 'set param_card mass   6  172.5\n'
customizecards = customizecards + 'set param_card yukawa 6  172.5\n'
customizecards = customizecards + 'set param_card mass   25 125.0\n'

scanValues = [1]

n=0
rwgtCards = ''
rwgtCards = rwgtCards + 'import model dim6top_LO_UFO --modelname'+ '\n'
rwgtCards = rwgtCards + 'define p = g u c d s u~ c~ d~ s~ b b~'+ '\n'
rwgtCards = rwgtCards + 'define j = g u c d s u~ c~ d~ s~ b b~'+ '\n'
rwgtCards = rwgtCards + 'define l+ = e+ mu+ ta+'+ '\n'
rwgtCards = rwgtCards + 'define l- = e- mu- ta-'+ '\n'
rwgtCards = rwgtCards + 'generate  p p > t  l+ l- DIM6=0 FCNC=1@0'+ '\n'
rwgtCards = rwgtCards + 'add process p p > t~  l+ l- DIM6=0 FCNC=1@01'+ '\n'
rwgtCards = rwgtCards + 'output ttllFCNC -f -nojpeg'+ '\n'

#other points
for v in scanValues:
   for WC1 in couplingsName:
       rwgtCards = rwgtCards + '\n'
       rwgtCards = rwgtCards + 'launch -n ' + WC1 + '\n'
       rwgtCards = rwgtCards + '    set pdlabel lhapdf'+ '\n'
       rwgtCards = rwgtCards + '    set lhaid 306000'+ '\n'
       rwgtCards = rwgtCards + '    set drll 0.001'+ '\n'
       rwgtCards = rwgtCards + '    set etal 5'+ '\n'
       for WC2 in couplingsName:
           if WC1 == WC2:
               for wcIndex in couplings[couplingsName.index(WC2)]:
                   rwgtCards = rwgtCards +'    set param_card ' + wcIndex + ' ' + str(v*Ivalue[couplingsName.index(WC1)])  + '\n'
           else:
               for wcIndex in couplings[couplingsName.index(WC2)]:
                   rwgtCards = rwgtCards  + '    set param_card ' + wcIndex + ' 0'  + '\n'
open('ttllFCNC_MGscan.dat', 'wt').write(rwgtCards)






