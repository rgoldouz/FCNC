import ROOT
ROOT.gROOT.SetBatch(ROOT.kTRUE)
ROOT.gROOT.ProcessLine("gErrorIgnoreLevel = 1;")
ROOT.TH1.AddDirectory(ROOT.kFALSE)
ROOT.gStyle.SetOptStat(0)
from ROOT import TMVA, TFile, TCanvas, TGraph, TH1F, TH2F
import math
import gc
import sys
import numpy as np
import copy
import os

def draw2dHist(hist,Fname, ch = "channel", reg = "region", var="sample", varname="v"):
    Fol = 'MVAhists'
    if not os.path.exists(Fol):
       os.makedirs(Fol)
    if not os.path.exists(Fol + '/' + ch):
       os.makedirs(Fol + '/' + ch)
    if not os.path.exists(Fol + '/' + ch +'/'+reg):
       os.makedirs(Fol + '/' + ch +'/'+reg)
    canvas = ROOT.TCanvas(ch+reg+var,ch+reg+var,50,50,865,780)
    canvas.SetGrid();
    canvas.SetBottomMargin(0.17)
    canvas.cd()
    hist.GetYaxis().SetLabelSize(0.025)
    hist.GetXaxis().SetLabelSize(0.025)
    hist.Draw("colz");
    canvas.Print(Fol + '/' + ch +'/'+reg+'/'+var + ".png")
    del canvas
    gc.collect()

def compareHists(hists,Fnames, ch = "channel", reg = "region", var="sample", varname="v"):
    Fol = 'MVAhists'
    if not os.path.exists(Fol):
       os.makedirs(Fol)
    if not os.path.exists(Fol + '/' + ch):
       os.makedirs(Fol + '/' + ch)
    if not os.path.exists(Fol + '/' + ch +'/'+reg):
       os.makedirs(Fol + '/' + ch +'/'+reg)
    canvas = ROOT.TCanvas(ch+reg+var,ch+reg+var,50,50,865,780)
    canvas.SetGrid();
    canvas.SetBottomMargin(0.17)
    canvas.cd()

    pad1=ROOT.TPad("pad1", "pad1", 0.05, 0.05, 0.85, 0.99 , 0)#used for the hist plot
    pad2=ROOT.TPad("pad2", "pad2", 0.79, 0.2, 0.99, 0.99 , 0)#used for the hist plot
    pad1.Draw()
    pad2.Draw()
    pad1.cd()

    pad1.SetLogx(ROOT.kFALSE)
    pad1.SetLogy(ROOT.kTRUE)
    maxH=0
    for H in range(len(hists)):
        if hists[H].GetMaximum()>maxH:
            maxH=hists[H].GetMaximum()
#        hists[H].SetLineColor(colors[H])
        if 'Dec' in Fnames[H]:
            hists[H].SetLineStyle(2)
    y_min=1
    if hists[0].Integral()<2:
        y_min=0.001
    y_max=1.8* maxH
    hists[0].SetTitle("")
    hists[0].GetYaxis().SetTitle('A.U.')
    hists[0].GetXaxis().SetLabelSize(0.03)
    hists[0].GetYaxis().SetTitleOffset(0.8)
    hists[0].GetYaxis().SetTitleSize(0.05)
    hists[0].GetYaxis().SetLabelSize(0.04)
    hists[0].GetYaxis().SetRangeUser(y_min,y_max)
    hists[0].GetXaxis().SetTitle(varname)
    hists[0].Draw("Hist")
    for H in range(1,len(hists)):
        if 'Test' in Fnames[H]:
            hists[H].Draw("histESAME")
        else:
            hists[H].Draw("histSAME")
    hists[0].Draw("AXISSAMEY+")
    hists[0].Draw("AXISSAMEX+")
    label_cms="CMS"
    Label_cms = ROOT.TLatex(0.128,0.92,label_cms)
    Label_cms.SetNDC()
    Label_cms.SetTextSize(0.05)
    Label_cms.Draw()
    Label_cmsprelim = ROOT.TLatex(0.23,0.92,"Simulation")
    Label_cmsprelim.SetNDC()
    Label_cmsprelim.SetTextSize(0.04)
    Label_cmsprelim.SetTextFont(51)
    Label_cmsprelim.Draw()
    Label_lumi = ROOT.TLatex(0.6,0.92,"41.48 fb^{-1} (13 TeV)")
    Label_lumi.SetNDC()
    Label_lumi.SetTextFont(42)
    Label_lumi.SetTextSize(0.035)
    Label_lumi.Draw("same")
    Label_channel = ROOT.TLatex(0.2,0.8,ch+" ("+reg+")")
    Label_channel.SetNDC()
    Label_channel.SetTextFont(42)
#    Label_channel.Draw("same")
    pad1.Update()
    pad2.cd()
    legend = ROOT.TLegend(0.0,0.1,0.7,0.9)
    legend.SetBorderSize(0)
    legend.SetTextFont(42)
    legend.SetTextSize(0.09)
    for num in range(0,len(hists)):
        if 'Test' in Fnames[num]:
            legend.AddEntry(hists[num],Fnames[num],'lep')
        else:
            legend.AddEntry(hists[num],Fnames[num],'F')
    legend.Draw("same")

    pad2.Update()
    canvas.Print(Fol + '/' + ch +'/'+reg+'/'+var + ".png")
    del canvas
    gc.collect()

# Initialize TMVA tools
TMVA.Tools.Instance()
MVAs=["TU","TC"]
variables=["lep1Pt","lep2Pt","llDr","llDphi", "lep3Pt", "jet1Pt", "bJetPt", "tZ_topMass", "tZ_WtopMass", "tZ_ZPt", "tZ_ZEta", "tZ_topPt", "tZ_topEta", "nJets"]
FCNC2l2q=["ctZ","cpQM","cpt"]

# Open the TMVA output file
for MVA in MVAs:
    file = TFile.Open('tmp_TMVAClassification_'+MVA+'_3lonZ/TMVAOutput_'+MVA+'_3lonZ.root')
    if not file or file.IsZombie():
        print("Error: Cannot open TMVA output file")
        exit()
    for n,c in enumerate(FCNC2l2q):
        HH=[]
        HHname=[]
        print 'dataset/Method_BDT/BDT/MVA_BDT_Train_'+c+'_prob_for_'+c
        hist1 = file.Get('dataset/Method_BDT/BDT/MVA_BDT_Train_'+c+'_prob_for_'+c)
        hist1.SetLineColor(ROOT.kBlue+2)
        hist1.SetFillColorAlpha(ROOT.kBlue, 0.3)
        HH.append(hist1)
        HHname.append('Train_Sig('+c+')')
        hist1 = file.Get('dataset/Method_BDT/BDT/MVA_BDT_Train_'+c+'_prob_for_Background')
        hist1.SetLineColor(ROOT.kRed+2)
        hist1.SetFillColorAlpha(ROOT.kRed, 0.3)
        HH.append(hist1)
        HHname.append('Train_BG')
        hist1 = file.Get('dataset/Method_BDT/BDT/MVA_BDT_Test_'+c+'_prob_for_'+c)
        hist1.SetLineColor(ROOT.kBlue+2)
        hist1.SetLineWidth(2)
        HH.append(hist1)
        HHname.append('Test_Sig('+c+')')
        hist1 = file.Get('dataset/Method_BDT/BDT/MVA_BDT_Test_'+c+'_prob_for_Background')
        hist1.SetLineColor(ROOT.kRed+2)
        hist1.SetLineWidth(2)
        HH.append(hist1)
        HHname.append('Test_BG')
        compareHists(HH,HHname, '3lonZ',MVA,c,'probability')

        hist1 = file.Get('dataset/CorrelationMatrix'+c)
        draw2dHist(hist1,'', '3lonZ',MVA,'CorrelationMatrix'+c,'')
    hist1 = file.Get('dataset/CorrelationMatrixBackground')
    draw2dHist(hist1,'', '3lonZ',MVA,'CorrelationMatrixBackground','')
    
    colors =  [ROOT.kBlack,ROOT.TColor.GetColor("#3f90da"),ROOT.TColor.GetColor("#ffa90e"), ROOT.TColor.GetColor("#bd1f01"),ROOT.TColor.GetColor("#94a4a2"), ROOT.TColor.GetColor("#832db6"),ROOT.TColor.GetColor("#a96b59"),ROOT.TColor.GetColor("#e76300"),ROOT.TColor.GetColor("#b9ac70"),ROOT.TColor.GetColor("#717581"),ROOT.TColor.GetColor("#92dadd")]
    for numvar, namevar in enumerate(variables):
        print namevar
        HH=[]
        HHname=[]
        hist1 = file.Get('dataset/InputVariables_Id/'+namevar+'__Background_Id')
        hist1.Scale(1/hist1.Integral())
        hist1.SetLineColor(ROOT.kBlue+2)
        hist1.SetFillColorAlpha(ROOT.kBlue, 0.3)
        HH.append(hist1)    
        HHname.append('BG')
        for n,c in enumerate(FCNC2l2q):
            hist1 = file.Get('dataset/InputVariables_Id/'+namevar+'__'+c+'_Id')
            hist1.Scale(1/hist1.Integral())
            hist1.SetLineColor(colors[n])
            hist1.SetLineWidth(2)
            HH.append(hist1)
            HHname.append(c)
        compareHists(HH,HHname, '3lonZ',MVA,'IV_'+namevar,namevar)
    os.system('tar -cvf MVAhists.tar MVAhists')
