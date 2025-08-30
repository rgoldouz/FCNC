#run this code using "python3.9 condor_doFitForNuisance.py"
import datetime
import os
from os import path
import sys
import ROOT
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
import array
from ROOT import TColor
from ROOT import TGaxis
from ROOT import THStack
import gc
from copy import deepcopy
TGaxis.SetMaxDigits(2)

colors = [
    ROOT.TColor.GetColor("#bd1f01"),  # Red    
    ROOT.kBlack,
    ROOT.TColor.GetColor("#3f90da"),  # Blue
    ROOT.TColor.GetColor("#ffa90e"),  # Orange
    ROOT.TColor.GetColor("#94a4a2"),  # Greyish
    ROOT.TColor.GetColor("#832db6"),  # Purple
    ROOT.TColor.GetColor("#a96b59"),  # Brownish
    ROOT.TColor.GetColor("#e76300"),  # Deep Orange
    ROOT.TColor.GetColor("#b9ac70"),  # Olive
    ROOT.TColor.GetColor("#717581"),  # Slate
    ROOT.TColor.GetColor("#92dadd"),  # Light Blue
    ROOT.TColor.GetColor("#009B77"),  # Teal Green
    ROOT.TColor.GetColor("#d62728"),  # Strong Red
    ROOT.TColor.GetColor("#17becf"),  # Cyan
    ROOT.TColor.GetColor("#bcbd22"),  # Yellow-green
    ROOT.TColor.GetColor("#9467bd"),  # Soft Purple
    ROOT.TColor.GetColor("#8c564b"),  # Muted Brown
    ROOT.TColor.GetColor("#e377c2"),  # Pink
    ROOT.TColor.GetColor("#7f7f7f"),  # Neutral Grey
    ROOT.TColor.GetColor("#1f77b4"),  # Classic Blue
    ROOT.TColor.GetColor("#2ca02c"),  # Green
    ROOT.TColor.GetColor("#ff7f0e"),  # Bright Orange
    ROOT.TColor.GetColor("#aec7e8"),  # Light Blue
    ROOT.TColor.GetColor("#ffbb78"),  # Light Orange
    ROOT.TColor.GetColor("#98df8a"),  # Light Green
    ROOT.TColor.GetColor("#c5b0d5"),  # Light Purple
    ROOT.TColor.GetColor("#c49c94"),  # Light Brown
    ROOT.TColor.GetColor("#f7b6d2"),  # Light Pink
    ROOT.TColor.GetColor("#dbdb8d"),  # Pale Olive
    ROOT.TColor.GetColor("#9edae5"),  # Pale Cyan
]

def compareError(histsup,histsdown, sys, folder='sys', ch = "channel", reg = "region", year='2016', var="sample", varname="v", prefix = 'Theory'):
    if not os.path.exists(folder):
       os.makedirs(folder)
    if not os.path.exists(folder +'/'+year):
       os.makedirs(folder +'/'+ year)
    if not os.path.exists(folder +'/'+year + '/' + ch):
       os.makedirs(folder +'/'+year + '/' + ch)
    if not os.path.exists(folder +'/'+year + '/' + ch +'/'+reg):
       os.makedirs(folder +'/'+year + '/' + ch +'/'+reg)

    canvas = ROOT.TCanvas(year+ch+reg+var,year+ch+reg+var,50,50,865,780)
    canvas.SetGrid();
    canvas.cd()

    legend = ROOT.TLegend(0.35,0.7,0.9,0.88)
    legend.SetBorderSize(0)
    legend.SetTextFont(42)
    legend.SetTextSize(0.03)
    legend.SetNColumns(3);

    pad2=ROOT.TPad("pad2", "pad2", 0.0, 0.0, 1, 1 , 0)#used for the ratio plot
    pad2.Draw()
#    pad2.SetGridy()
#    pad2.SetGridx()
    pad2.SetTickx()
    pad2.SetBottomMargin(0.1)
    pad2.SetLeftMargin(0.11)
    pad2.SetRightMargin(0.1)
    pad2.SetFillStyle(0)
    pad2.SetLogx(ROOT.kFALSE)
    pad2.SetLogx(ROOT.kTRUE)
    pad2.cd()
    maxi=0
    for n,G in enumerate(histsup):
        histsup[n].SetLineColor(colors[n])
        histsup[n].SetLineWidth(2)
        histsup[n].SetFillColor(0)
        legend.AddEntry(histsup[n],sys[n],'L')
        if(histsup[n].GetMaximum()>maxi):
            maxi=G.GetMaximum()
        histsdown[n].SetLineColor(colors[n])
        histsdown[n].SetFillColor(0)
        histsdown[n].SetLineWidth(1)
    bin_max_x=0
    if 'MVA' in var:
        for H in range(len(histsup)):
            last_bin = histsup[H].GetNbinsX()
            while last_bin >= 1 and histsup[H].GetBinContent(last_bin) == 0:
                last_bin -= 1
            if last_bin>bin_max_x:
                bin_max_x=last_bin
        xlimit=histsup[0].GetXaxis().GetBinUpEdge(bin_max_x)
        pad2.SetLogx(ROOT.kTRUE)
        histsup[0].GetXaxis().SetRangeUser(0.01, 2*math.ceil(xlimit))
    if bin_max_x>100:
        maxi=100

    histsup[0].SetTitle( '' )
    histsup[0].GetYaxis().SetTitle( 'Uncertainty (%)' )
    histsup[0].GetXaxis().SetTitle(varname)
    histsup[0].GetXaxis().SetLabelSize(0.04)
    histsup[0].GetYaxis().SetLabelSize(0.03)
    histsup[0].GetXaxis().SetTitleSize(0.04)
    histsup[0].GetYaxis().SetTitleSize(0.04)
    histsup[0].GetXaxis().SetTitleOffset(0.95)
    histsup[0].GetYaxis().SetTitleOffset(1)
    histsup[0].GetYaxis().SetNdivisions(804)
    histsup[0].GetXaxis().SetNdivisions(808)
    histsup[0].GetYaxis().SetRangeUser(-1.4*maxi,2*maxi)
#    histsup[0].GetYaxis().SetRangeUser(0.7,1.3)
    histsup[0].Draw('hist')
    for n,G in enumerate(histsup):
        histsup[n].Draw('samehist')
        histsdown[n].Draw('samehist')
    histsup[0].Draw('samehist')
    histsdown[0].Draw('samehist')
    histsup[0].Draw("AXISSAMEY+")
    histsup[0].Draw("AXISSAMEX+")
    Lumi = '137.19'
    if (year == '2016'):
        Lumi = '35.92'
    if (year == '2017'):
        Lumi = '41.53'
    if (year == '2018'):
        Lumi = '59.74'
    label_cms="CMS Simulation Preliminary"
    Label_cms = ROOT.TLatex(0.22,0.92,label_cms)
    Label_cms.SetTextSize(0.035)
    Label_cms.SetNDC()
    Label_cms.SetTextFont(61)
    Label_cms.Draw()
    Label_lumi = ROOT.TLatex(0.65,0.92,Lumi+" fb^{-1} (13 TeV)")
    Label_lumi.SetTextSize(0.035)
    Label_lumi.SetNDC()
    Label_lumi.SetTextFont(42)
    Label_lumi.Draw("same")
    Label_channel = ROOT.TLatex(0.15,0.8,year)
    Label_channel.SetNDC()
    Label_channel.SetTextFont(42)
    Label_channel.Draw("same")

    Label_channel2 = ROOT.TLatex(0.15,0.75,ch+" ("+reg+")")
    Label_channel2.SetNDC()
    Label_channel2.SetTextFont(42)
    Label_channel2.Draw("same")

    legend.Draw("same")
    canvas.Print(folder +'/'+ year + '/' + ch +'/'+reg+'/sysCompact'+ prefix +'_'+var + ".png")
    del canvas
    gc.collect()    


FrozenSys=[]
Exclude =''
Sig='TU'
wf = []
FrozenSys=[]
Exclude =''
WCs = ["ctpF", "ctlSF", "cteF", "ctlF", "ctlTF", "ctZF", "cptF", "cpQMF", "ctAF", "cQeF", "ctGF", "cQlMF"]
WCnames = ["k_" + wc for wc in WCs]
R = "-3,3"
L = "-0.3,0.3"
M="-0.5,0.5"
ranges = {"k_ctpF": R, "k_ctZF": M, "k_cptF": R, "k_cpQMF": R, "k_ctAF": R, "k_ctGF": L, "k_cQlMF": R, "k_cQeF": R, "k_ctlF": R, "k_cteF": R, "k_ctlSF": R, "k_ctlTF": L}
if len(FrozenSys)>0:
    Exclude =' --freezeParameters ' + (','.join(FrozenSys))
WorkSpace = 'CombinedFilesFCNC_v2/model_test_TU.root'

# get the nuisances
Nuisance = []
f = ROOT.TFile.Open(WorkSpace)  # Replace with your actual file
w = f.Get("w")  # Replace "w" with your actual workspace name
model = w.obj("ModelConfig")
nuis = model.GetNuisanceParameters()

itr = nuis.createIterator()
nuis_list = []

var = itr.Next()
i = 1
while var:
#    print(f"{i:2}: {var.GetName()}")
    Nuisance.append(f"{var.GetName()}")
    nuis_list.append(var.GetName())
    i += 1
    var = itr.Next()

fname='2018_3loffZhigh_1bHj_MVATU.root'
f1 = ROOT.TFile.Open('/users/rgoldouz/FCNC/NanoAnalysis/combine/CombinedFilesFCNC_v2/' + fname)
my_list = f1.GetListOfKeys()
Hists=[]
for obj in my_list: # obj is TKey
    if obj.GetClassName() == "TH1F":
        Hists.append(obj.GetName())
for H in Hists:
    if H[-2:]=='Up':
        hup=f1.Get(H).Clone()
        hdown=f1.Get(H[:-2]+'Down').Clone()
        unc=""
        for n in nuis_list:
            if n in H:
                unc=n
                break
#        print (H+":"+unc)    
#        print (H +":"+H.split(unc)[0][:-1])    
        if unc!="" and H.split(unc)[0][:-1] in Hists:
#            print (unc)
            h=f1.Get(H.split(unc)[0][:-1]).Clone()
            hup.Add(h,-1)
            hup.Divide(h)
            hdown.Add(h,-1)
            hdown.Divide(h)
            compareError([hup],[hdown], [unc], 'nuisance',fname.split('_')[1], fname.split('_')[2], fname.split('_')[0],'MVATU_'+H.split(unc)[0][:-1]+'_'+unc,'MVATU', 'nuis_')
#            print (H + ":"+H[:-2]+'Down'+":"+unc)
#            print (H.split(unc))
os.system('tar -cvf nuisance.tar nuisance')           
print (nuis_list)           
