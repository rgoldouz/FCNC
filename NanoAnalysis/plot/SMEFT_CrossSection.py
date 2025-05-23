import math
import gc
import sys
import ROOT
import numpy as np
import copy
import os
ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.gROOT.ProcessLine("gErrorIgnoreLevel = 1;")
ROOT.TH1.AddDirectory(ROOT.kFALSE)
ROOT.gStyle.SetOptStat(0)
from array import array
from ROOT import TColor
from ROOT import TGaxis
from ROOT import THStack
import gc
#TGaxis.SetMaxDigits(2)

bins=[5,10,20,30,40]
HistAddress = '/afs/crc.nd.edu/user/r/rgoldouz/FCNC/NanoAnalysis/hists/'
dir_list = os.listdir(HistAddress)
for key in dir_list:
    if 'FCNC' not in key:
        continue
    print key
    FR = ROOT.TFile.Open(HistAddress +key)
    HEFT = FR.Get("crossSection")
    HEFT.GetSumFit().save('Coup/' + key.split(".")[0]+'.tex')
