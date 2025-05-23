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
TGaxis.SetMaxDigits(2)

colors =  [ROOT.kBlack,ROOT.TColor.GetColor("#3f90da"),ROOT.TColor.GetColor("#ffa90e"), ROOT.TColor.GetColor("#bd1f01"),ROOT.TColor.GetColor("#94a4a2"), ROOT.TColor.GetColor("#832db6"),ROOT.TColor.GetColor("#a96b59"),ROOT.TColor.GetColor("#e76300"),ROOT.TColor.GetColor("#b9ac70"),ROOT.TColor.GetColor("#717581"),ROOT.TColor.GetColor("#92dadd")]

def EFTtoNormal(H, wc):
    hpx    = ROOT.TH1F( H.GetName(), H.GetName(), H.GetXaxis().GetNbins(), H.GetXaxis().GetXmin(),H.GetXaxis().GetXmax() )
    r=1
    for b in range(hpx.GetNbinsX()):
        if H.GetBinContent(b+1,ROOT.WCPoint("NONE"))>0:
            r = H.GetBinError(b+1)/H.GetBinContent(b+1,ROOT.WCPoint("NONE"))
        hpx.SetBinContent(b+1, H.GetBinContent(b+1,wc))
        hpx.SetBinError(b+1, r*H.GetBinContent(b+1,wc))
    hpx.SetLineColor(H.GetLineColor())
    hpx.SetLineStyle(H.GetLineStyle())
#    if hpx.Integral()>0:
#        hpx.Scale(1/hpx.Integral())
    return hpx

def compareHistsTest(hists,Fnames, ch = "channel", reg = "region", var="sample", varname="v"):
#    for num in range(len(hists)):
#        if (hists[num].Integral() <= 0):
#            print "negative integral, so no print plot for "+ '/' + ch +'/'+reg+'/'+var + ".png"
#            return
    Fol = 'compareHistsTest'
    if not os.path.exists(Fol):
       os.makedirs(Fol)
    if not os.path.exists(Fol + '/' + ch):
       os.makedirs(Fol + '/' + ch)
    if not os.path.exists(Fol + '/' + ch +'/'+reg):
       os.makedirs(Fol + '/' + ch +'/'+reg)
#    for num in range(len(hists)):
#        hists[num].SetBinContent(hists[num].GetXaxis().GetNbins(), hists[num].GetBinContent(hists[num].GetXaxis().GetNbins()) + hists[num].GetBinContent(hists[num].GetXaxis().GetNbins()+1))
#        hists[num].Scale(1/hists[num].Integral())

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
        hists[H].SetLineWidth(2)
        hists[H].SetFillColor(0)
#        hists[H].SetLineColor(colors[H])
        if 'Dec' in Fnames[H]:
            hists[H].SetLineStyle(2)
    y_min=1
    if hists[0].Integral()<2:
        y_min=0.001
    y_max=1.8* maxH
    hists[0].SetTitle("")
    hists[0].GetYaxis().SetTitle('Events')
    hists[0].GetXaxis().SetLabelSize(0.03)
    hists[0].GetYaxis().SetTitleOffset(1.1)
    hists[0].GetYaxis().SetTitleSize(0.05)
    hists[0].GetYaxis().SetLabelSize(0.04)
    hists[0].GetYaxis().SetRangeUser(y_min,y_max)
    hists[0].GetXaxis().SetTitle(varname)
    hists[0].Draw("Hist")
    hists[0].SetLineWidth(2)
    hists[0].SetFillColor(17)
    hists[0].SetLineColor(17)
    for H in range(1,len(hists)):
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
    Label_channel.Draw("same")

    pad1.Update()
    pad2.cd()
    legend = ROOT.TLegend(0.0,0.1,0.7,0.9)
    legend.SetBorderSize(0)
    legend.SetTextFont(42)
    legend.SetTextSize(0.11)
    for num in range(0,len(hists)):
        legend.AddEntry(hists[num],Fnames[num],'L')
    legend.Draw("same")

    pad2.Update()
    canvas.Print(Fol + '/' + ch +'/'+reg+'/'+var + ".png")
    del canvas
    gc.collect()

year=['2017']
regions=["All","1b1j", "1bG1j","G1b"]
regionsName=["All","1b1j", "1b$>$1j", "$>$1Bjet"]
channels=["LLss",  "3LonZ", "3LoffZhigh", "3LoffZlow"]
variables=["lep1Pt","lep1Eta","lep1Phi","lep2Pt","lep2Eta","lep2Phi","llM","llPt","llDr","llDphi","jet1Pt","jet1Eta","jet1Phi","njet","nbjet","Met","MetPhi","nVtx","llMZw","MVA"]
#variables=["lep1Pt"]
variablesName=["p_{T}(leading lepton)","#eta(leading lepton)","#Phi(leading lepton)","p_{T}(sub-leading lepton)","#eta(sub-leading lepton)","#Phi(sub-leading lepton)","M(ll)","p_{T}(ll)","#Delta R(ll)","#Delta #Phi(ll)","p_{T}(leading jet)","#eta(leading jet)","#Phi(leading jet)","Number of jets","Number of b-tagged jets","MET","#Phi(MET)","Number of vertices", "M(ll) [z window]","MVA"]

HistAddress = '/afs/crc.nd.edu/user/r/rgoldouz/FCNC/NanoAnalysis/'


Samples = ['SIG.root','BG.root']
SamplesName = ['TU_Prod','TU_Dec','TC_Prod','TC_Dec']# , 'BNV_ST_TBCE', 'BNV_ST_TBUE', 'BNV_ST_TDCE',  'BNV_ST_TDUE',  'BNV_ST_TSCE',  'BNV_ST_TSUE']
colors =  [ROOT.kBlack,ROOT.TColor.GetColor("#3f90da"),ROOT.TColor.GetColor("#ffa90e"), ROOT.TColor.GetColor("#bd1f01"),ROOT.TColor.GetColor("#94a4a2"), ROOT.TColor.GetColor("#832db6"),ROOT.TColor.GetColor("#a96b59"),ROOT.TColor.GetColor("#e76300"),ROOT.TColor.GetColor("#b9ac70"),ROOT.TColor.GetColor("#717581"),ROOT.TColor.GetColor("#92dadd")]
FCNC=["ctp","ctlT","ctlS","cte","ctZ","cpt","cpQM","ctA","ctG"];
FCNCz=["ctZ","cpt","cpQM"];
FCNC2l2q=["ctlS","cte","ctl","ctlT","cQe","cQlM"];

wc1 = ROOT.WCPoint("EFTrwgt1_cS_1_cT_1")

Hists = []
for numyear, nameyear in enumerate(year):
    l0=[]
    Files = []
    for f in range(len(Samples)):
        l1=[]
        Files.append(ROOT.TFile.Open(HistAddress + nameyear+ '_' + Samples[f]))
        for numch, namech in enumerate(channels):
            l2=[]
            for numreg, namereg in enumerate(regions):
                l3=[]
                for numvar, namevar in enumerate(variables):
                    h= Files[f].Get(namech + '_' + namereg + '_' + namevar)
                    h.SetFillColor(colors[f])
                    h.SetLineColor(colors[f])
                    l3.append(h)
                l2.append(l3)
            l1.append(l2)
        l0.append(l1)
    Hists.append(l0)       

#Draw histogram and compare the importance of couplings in different channels and regions
for numyear, nameyear in enumerate(year):
    for numch, namech in enumerate(channels):
        for numreg, namereg in enumerate(regions):
            for numvar, namevar in enumerate(variables):
                HH=[]
                HHname=[]
                myhist= EFTtoNormal(Hists[numyear][1][numch][numreg][numvar],wc1)
                myhist.SetLineColor(17)
                HH.append(myhist)
                HHname.append('BG')
                for n,c in enumerate(FCNC):
                    text = 'EFTrwgt4_'+c+'_1.0'
                    wc1 = ROOT.WCPoint(text)
                    for f in range(0,1):
                        myhist= EFTtoNormal(Hists[numyear][f][numch][numreg][numvar],wc1)
                        myhist.SetLineColor(colors[n])
                        if myhist.Integral()>5:
                            HH.append(myhist)
                            HHname.append(SamplesName[f]+'('+c+'=1)')
                if len(HH)>0:
                    compareHistsTest(HH,HHname, namech,namereg,'TU'+namevar,variablesName[numvar])

##Draw histogram and compare the shape of couplings that are important in Z mass
#for numyear, nameyear in enumerate(year):
#    for numch, namech in enumerate(channels):
#        if namech!='3LonZ':
#            continue
#        for numreg, namereg in enumerate(regions):
#            for numvar, namevar in enumerate(variables):
#                HH=[]
#                HHname=[]
#                myhist= EFTtoNormal(Hists[numyear][4][numch][numreg][numvar],wc1).Clone()
#                myhist.Scale(1/myhist.Integral())
#                myhist.SetLineColor(17)
#                HH.append(myhist)
#                HHname.append('BG')
#                for n,c in enumerate(FCNCz):
#                    text = 'EFTrwgt4_'+c+'_1.0'
#                    wc1 = ROOT.WCPoint(text)
#                    for f in range(0,2):
#                        myhist= EFTtoNormal(Hists[numyear][f][numch][numreg][numvar],wc1).Clone()
#                        myhist.SetLineColor(colors[n])
#                        myhist.Scale(1/myhist.Integral())
#                        if myhist.Integral()>0:
#                            HH.append(myhist)
#                            HHname.append(SamplesName[f]+'('+c+'=1)')
#                if len(HH)>0:
#                    compareHistsTest(HH,HHname, namech+'-Normalise-Z',namereg,'TU'+namevar,variablesName[numvar])
#                HH=[]
#                HHname=[]
#                myhist= EFTtoNormal(Hists[numyear][4][numch][numreg][numvar],wc1).Clone()
#                myhist.Scale(1/myhist.Integral())
#                myhist.SetLineColor(17)
#                HH.append(myhist)
#                HHname.append('BG')
#                for n,c in enumerate(FCNCz):
#                    text = 'EFTrwgt4_'+c+'_1.0'
#                    wc1 = ROOT.WCPoint(text)
#                    for f in range(2,4):
#                        myhist= EFTtoNormal(Hists[numyear][f][numch][numreg][numvar],wc1).Clone()
#                        myhist.Scale(1/myhist.Integral())
#                        myhist.SetLineColor(colors[n])
#                        if myhist.Integral()>0:
#                            HH.append(myhist)
#                            HHname.append(SamplesName[f]+'('+c+'=1)')
#                if len(HH)>0:
#                    compareHistsTest(HH,HHname, namech+'-Normalise-Z',namereg,'TC'+namevar,variablesName[numvar])

#Draw histogram and compare the shape of couplings that are important in off Z mass
for numyear, nameyear in enumerate(year):
    for numch, namech in enumerate(channels):
        if namech!='3LoffZhigh':
            continue
        for numreg, namereg in enumerate(regions):
            for numvar, namevar in enumerate(variables):
                HH=[]
                HHname=[]
                myhist= EFTtoNormal(Hists[numyear][1][numch][numreg][numvar],wc1).Clone()
                myhist.Scale(1/myhist.Integral())
                myhist.SetLineColor(17)
                HH.append(myhist)
                HHname.append('BG')
                for n,c in enumerate(FCNC2l2q):
                    text = 'EFTrwgt4_'+c+'_1.0'
                    wc1 = ROOT.WCPoint(text)
                    for f in range(0,1):
                        myhist= EFTtoNormal(Hists[numyear][f][numch][numreg][numvar],wc1).Clone()
                        myhist.SetLineColor(colors[n])
                        myhist.Scale(1/myhist.Integral())
                        if myhist.Integral()>0:
                            HH.append(myhist)
                            HHname.append(SamplesName[f]+'('+c+'=1)')
                if len(HH)>0:
                    compareHistsTest(HH,HHname, namech+'-Normalise-2l2q',namereg,'TU'+namevar,variablesName[numvar])

os.system('tar -cvf compareHistsTest.tar compareHistsTest')
