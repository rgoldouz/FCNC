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
from ROOT import TFile
import gc
import sys
import os
import subprocess
import readline
import string
MCSAMPLES = {}

HistAddress = '/afs/crc.nd.edu/user/r/rgoldouz/FCNC/NanoAnalysis/MVA/'
WC=["ctp","ctlS","cte","ctl","ctlT","ctZ","cpt","cpQM","ctA","cQe","ctG","cQlM"]
for i in WC:
    MCSAMPLES[i]= 'weight'+i

variable=["lep1Pt","lep1Eta","lep2Pt","lep2Eta","llM","llPt","llDr","llDphi"]
variable=["llM"]
variableRange=[[50,0,500],[20,-5,5],[50,0,500],[20,-5,5],[50,0,500],[50,0,500],[20,0,7],[20,0,7]]
filename=['2017_FCNCProduction.root']


for fname in filename:
    os.system('mkdir ' +fname.split('.')[0])
    fi = TFile.Open(HistAddress+fname)
    evtTree = fi.Get('FCNC')
    for numi, namei in enumerate(WC):
        for numv, namev in enumerate(variable):
            H=ROOT.TH1F ( namei+namev ,namei+namev ,variableRange[numv][0],variableRange[numv][1],variableRange[numv][2])
            canvas = ROOT.TCanvas(namei+namev,namei+namev,50,50,865,780)
            canvas.SetGrid()
            for i in range( evtTree.GetEntries() ):
               evtTree.GetEntry (i)
               ch = getattr(evtTree, 'ch')
               if ch!=6:
                   continue
               H.Fill(getattr(evtTree, namev), getattr(evtTree, MCSAMPLES[namei]))
            canvas = ROOT.TCanvas(namei+namev,namei+namev,50,50,865,780)
            canvas.SetGrid();
            H.Draw()
            canvas.Print(fname.split('.')[0]+'/'+namei+namev + ".png")
            del canvas
            gc.collect()
 
