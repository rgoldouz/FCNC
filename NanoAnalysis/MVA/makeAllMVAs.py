import math
import gc
import sys
import ROOT
import numpy as np
import copy
import os

#root -l 'TMVAClassification.C("","cpQM","ch==5 && weightcpQM >0","ch==5 && weightcpQM >0","weightcpQM","weightSM")'

BDTs={}
BDTs["ctlS"]=['"ch==6 || ch==7"','"ch==6 || ch==7"','"weightctlS"']
BDTs["cte"]=['"ch==6 || ch==7"','"ch==6 || ch==7"','"weightcte"']
BDTs["ctl"]=['"ch==6 || ch==7"','"ch==6 || ch==7"','"weightctl"']
BDTs["ctlT"]=['"ch==6 || ch==7"','"ch==6 || ch==7"','"weightctlT"']
BDTs["cQe"]=['"ch==6 || ch==7"','"ch==6 || ch==7"','"weightcQe"']
BDTs["cQlM"]=['"ch==6 || ch==7"','"ch==6 || ch==7"','"weightcQlM"']

#BDTs["ctZ"]=['"ch==5" && weightctZ>0.005 ','"ch==5"','"weightctZ"']
#BDTs["cpt"]=['"ch==5 && weightcpt>0.005"','"ch==5"','"weightcpt"']
#BDTs["cpQM"]=['"ch==5 && weightcpQM>0.005"','"ch==5"','"weightcpQM"']
#
#BDTs["ctA"]=['"(ch==3 || ch==4)  && weightctA>0.005"','"ch==3 || ch==4"','"weightctA"']
#BDTs["ctG"]=['"(ch==3 || ch==4)   && weightctG>0.005"','"ch==3 || ch==4"','"weightctG"']
#BDTs["ctp"]=['"(ch==3 || ch==4)   && weightctp>0.005"','"ch==3 || ch==4"','"weightctp"']

for key in BDTs:
    print 'root -l \'TMVAClassification.C("","' + key + '",' + BDTs[key][0] +',' + BDTs[key][1] +',' + BDTs[key][2] +',"weightSM")\' '
#    os.system('nohup root -l \'TMVAClassification.C("","' + key + '",' + BDTs[key][0] +',' + BDTs[key][1] +',' + BDTs[key][2] +',"weightSM")\'  >& ' + key +'.log &')   
#    os.system('root -l \'TMVAClassification.C("","+cpQM","ch==5 && weightcpQM >0","ch==5 && weightcpQM >0","weightcpQM","weightSM")\'')
