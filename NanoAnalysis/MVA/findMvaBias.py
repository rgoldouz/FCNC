import math
import gc
import sys
import ROOT
import numpy as np
import copy
import os
from ROOT import TFile
from array import array
from ROOT import TColor
from ROOT import TGaxis
from ROOT import THStack
from ROOT import gPad
from ROOT import gDirectory

filename='ctp_TMVA.root'
fi = TFile.Open(filename)
tree_test = fi.Get('dataset/TestTree')
tree_train = fi.Get('dataset/TrainTree')

variables=["lep1Pt","lep2Pt","lep1Eta", "lep2Eta","llM", "llPt","llDr","llDphi", "bJetPt","bJetEta", "nJets","topMass", "HZMass","WtopMass","W1HMass","W2HMass", "HZPt","HZEta","topPt", "topEta","drWtopB", "drW1HW2H"]
#variables=["lep1Eta","lep2Eta","llDr","llDphi","bJetEta", "nJets","HZEta","topEta","drWtopB", "drW1HW2H"]

for var in variables:
    canvas = ROOT.TCanvas(var,var,50,50,865,780)
    canvas.SetGrid();
    canvas.SetLogy(ROOT.kTRUE)
    canvas.cd()
#    pad1=ROOT.TPad("pad1", "pad1", 0, 0.0, 1, 0.99 , 0)#used for the hist plot
#    pad1.cd()
#    pad1.SetLogy(ROOT.kTRUE)
    tree_test.Draw(var+">>test","classID==1")
    test1=(gDirectory.Get("test")).Clone()
    #gPad.GetPrimitive("htemp")
    tree_train.Draw(var+">>test","classID==1");
    train=gDirectory.Get("test").Clone()
    test1.SetLineColor(2)
    train.SetLineColor(4)
    test1.Draw()
    train.Draw("same")
    canvas.Print(var+".png")
    canvas.Clear()
    del canvas
    del test1
    del train
    gDirectory.Delete("test")
#    gDirectory.Delete("train")
    gc.collect()
