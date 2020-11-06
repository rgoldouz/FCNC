import os


#couplings =['ctG','cQq83','cQq81','ctq8']
#couplings =['cpQM','cpQ3','cpt','ctW','ctZ','ctG','cQq83','cQq81','cQu8','cQd8','ctq8','ctu8','ctd8','cQq13','cQq11','cQu1','cQd1','ctq1','ctu1','ctd1']
couplings =[['ctpx31','ctpx13'],['cpQMx31','cpQMx13'],['cpQ3x31','cpQ3x13'],['cptx31','cptx13'],['cptbx31','cptbx13'],['ctAx31','ctAx13'],['ctZx31','ctZx13'],['cbWx31','cbWx13'],['ctGx31','ctGx13'],['cQl3x1x31','cQl3x2x31','cQl3x3x31','cQl3x1x13','cQl3x2x13','cQl3x3x13'],['cQlMx1x31','cQlMx2x31','cQlMx3x31','cQlMx1x13','cQlMx2x13','cQlMx3x13'],['cQex1x31','cQex2x31','cQex3x31','cQex1x13','cQex2x13','cQex3x13'],['ctlx1x31','ctlx2x31','ctlx3x31','ctlx1x13','ctlx2x13','ctlx3x13'],['ctex1x31','ctex2x31','ctex3x31','ctex1x13','ctex2x13','ctex3x13'],['ctlSx1x13','ctlSx2x13','ctlSx3x13','ctlSx1x31','ctlSx2x31','ctlSx3x31'],['ctlTx1x13','ctlTx2x13','ctlTx3x13','ctlTx1x31','ctlTx2x31','ctlTx3x31']]
couplingsName = ['ctp','cpQM','cpQ3','cpt','cptb','ctA','ctZ','cbW','ctG','cQl3','cQlM','cQe','ctl','cte','ctlS','ctlT']
Ivalue        = [10   ,10    ,10    ,10   ,10    ,5   ,10   ,10   ,0.05  ,10    ,10    ,10   ,10   ,10   ,10    ,10    ]
customizecards = ''
customizecards = customizecards + 'set param_card mass   6  172.5\n'
customizecards = customizecards + 'set param_card yukawa 6  172.5\n'
customizecards = customizecards + 'set param_card mass   25 125.0\n'

scanValues = [-2,-1,1,2]

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






