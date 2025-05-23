import math
import gc
import sys
import ROOT
import numpy as np
import copy
import os


BDTs={}
BDTs["ctlS"]  =['"ctlS_TMVA.root"']
BDTs["cte"]   =['"cte_TMVA.root"'] 
BDTs["ctl"]   =['"ctl_TMVA.root"']
BDTs["ctlT"]  =['"ctlT_TMVA.root"']
BDTs["cQe"]   =['"cQe_TMVA.root"']
BDTs["cQlM"]  =['"cQlM_TMVA.root"']

BDTs["ctZ"]   =['"ctZ_TMVA.root"']
BDTs["cpt"]   =['"cpt_TMVA.root"']
BDTs["cpQM"]  =['"cpQM_TMVA.root"']

BDTs["ctA"]   =['"ctA_TMVA.root"']
BDTs["ctG"]   =['"ctG_TMVA.root"']
BDTs["ctp"]   =['"ctp_TMVA.root"']
for key in BDTs:
    text=''
    text=text+'{'
    text=text+'gSystem->Load("libTMVAGui");\n'
    text=text+'TMVA::mvas("dataset",'+BDTs[key][0]+',TMVA::kCompareType);\n'
    text=text+'canvas1->SaveAs("'+key+'_MVA.png");\n'
    text=text+'TMVA::variables("dataset",'+BDTs[key][0]+');\n'
    text=text+'canvas1->SaveAs("'+key+'_InputVar1.png");\n'
    text=text+'canvas2->SaveAs("'+key+'_InputVar2.png");\n'
    text=text+'canvas3->SaveAs("'+key+'_InputVar3.png");\n'
    text=text+'canvas4->SaveAs("'+key+'_InputVar4.png");\n'
    text=text+'TMVA::correlations("dataset",'+BDTs[key][0]+');\n'
    text=text+'CorrelationMatrixS->SaveAs("'+key+'_CorrelationMatrixS.png");\n'
    text=text+'CorrelationMatrixB->SaveAs("'+key+'_CorrelationMatrixB.png");\n'
    text=text+'TMVA::efficiencies("dataset",'+BDTs[key][0]+',2);\n'
    text=text+'c->SaveAs("'+key+'_ROC.png");\n'
    text=text+'}'
    os.system('rm *.png')
    open('Cppcode', 'wt').write(text)
    os.system('root -l -q -b Cppcode')
    os.system('mkdir MVAOutput_'+key)
    os.system('mv *.png MVAOutput_'+key)
