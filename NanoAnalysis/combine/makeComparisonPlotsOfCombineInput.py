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
from operator import truediv
import copy
TGaxis.SetMaxDigits(2)

def Smoothing(AS, merge):
    x = array( 'd' )
    source =  array( 'd' )
    for i in range(AS.GetNbinsX()):
        x.append(AS.GetBinCenter(i + 1))
        source.append(AS.GetBinContent(i + 1))
    gs = ROOT.TGraphSmooth("normal")
    grin = ROOT.TGraph(AS.GetNbinsX(),x,source);
    grout = gs.SmoothKern(grin,"normal",merge);
    smooth = AS.Clone()
    for i in range(AS.GetNbinsX()):
        smooth.SetBinContent(i + 1,grout.GetY()[i])
    return smooth

def Rebin(AS, xbins):
    AB = AS.Rebin(len(xbins)-1,"AB",xbins)
    return AB

def correctHist(nominal,histRatio):
    for i in range(nominal.GetNbinsX()):
        histRatio.SetBinContent(i + 1,histRatio.GetBinContent(i + 1)*nominal.GetBinContent(i + 1))
    return histRatio
    
def stackPlots(hists, SignalHists, Fnames,FnamesS, ch = "channel", reg = "region", year='2016', var="sample", varname="v"):
    if not os.path.exists(year):
       os.makedirs(year)
    if not os.path.exists(year + '/' + ch):
       os.makedirs(year + '/' + ch)
    if not os.path.exists(year + '/' + ch +'/'+reg):
       os.makedirs(year + '/' + ch +'/'+reg)
    hs = ROOT.THStack("hs","")
    for num in range(1,len(hists)):
        hists[num].SetFillColor(hists[num].GetLineColor())
        hs.Add(hists[num])
    dummy = hists[0].Clone()
    canvas = ROOT.TCanvas(year+ch+reg+var,year+ch+reg+var,50,50,865,780)
    canvas.SetGrid();
    canvas.SetBottomMargin(0.17)
    canvas.cd()

    legend = ROOT.TLegend(0.5,0.45,0.75,0.88)
    legend.SetBorderSize(0)
    legend.SetTextFont(42)
    legend.SetTextSize(0.035)

    pad1=ROOT.TPad("pad1", "pad1", 0, 0.315, 1, 0.99 , 0)#used for the hist plot
    pad2=ROOT.TPad("pad2", "pad2", 0, 0.0, 1, 0.305 , 0)#used for the ratio plot
    pad1.Draw()
    pad2.Draw()
    pad2.SetGridy()
    pad2.SetTickx()
    pad1.SetBottomMargin(0.02)
    pad1.SetLeftMargin(0.14)
    pad1.SetRightMargin(0.05)
    pad2.SetTopMargin(0.1)
    pad2.SetBottomMargin(0.4)
    pad2.SetLeftMargin(0.14)
    pad2.SetRightMargin(0.05)
    pad2.SetFillStyle(0)
    pad1.SetFillStyle(0)
    pad1.cd()
    pad1.SetLogx(ROOT.kFALSE)
    pad2.SetLogx(ROOT.kFALSE)
    pad1.SetLogy(ROOT.kFALSE)

    y_min=0
    y_max=1.6*dummy.GetMaximum()
    dummy.SetMarkerStyle(20)
    dummy.SetMarkerSize(1.2)
    dummy.SetTitle("")
    dummy.GetYaxis().SetTitle('Events')
    dummy.GetXaxis().SetLabelSize(0)
    dummy.GetYaxis().SetTitleOffset(0.8)
    dummy.GetYaxis().SetTitleSize(0.07)
    dummy.GetYaxis().SetLabelSize(0.04)
    dummy.GetYaxis().SetRangeUser(y_min,y_max)
    if reg == '1Bjet':
        dummy.SetLineColor(0)
        dummy.SetMarkerSize(0)
    dummy.Draw("e")
    hs.Draw("histSAME")
    for h in range(len(SignalHists)):
        SignalHists[h].SetLineWidth(2)
        SignalHists[h].SetFillColor(0)
        SignalHists[h].SetLineStyle(h+1)
        SignalHists[h].Draw("histSAME")
    if '1Bjet'!=reg:
        dummy.Draw("eSAME")
    dummy.Draw("AXISSAMEY+")
    dummy.Draw("AXISSAMEX+")

    Lumi = '138'
    if (year == '2016preVFP'):
        Lumi = '19.52'
    if (year == '2016postVFP'):
        Lumi = '16.81'
    if (year == '2017'):
        Lumi = '41.48'
    if (year == '2018'):
        Lumi = '59.83'
    label_cms="CMS Preliminary"
    Label_cms = ROOT.TLatex(0.2,0.92,label_cms)
    Label_cms.SetNDC()
    Label_cms.SetTextFont(61)
    Label_cms.Draw()
    Label_lumi = ROOT.TLatex(0.71,0.92,Lumi+" fb^{-1} (13 TeV)")
    Label_lumi.SetNDC()
    Label_lumi.SetTextFont(42)
    Label_lumi.Draw("same")
    Label_channel = ROOT.TLatex(0.2,0.8,year +" / "+ch+" ("+reg+")")
    Label_channel.SetNDC()
    Label_channel.SetTextFont(42)
    Label_channel.Draw("same")

    if '1Bjet'==reg:
        Label_BL = ROOT.TLatex(0.2,0.68,"SR (Blinded)")
        Label_BL.SetNDC()
        Label_BL.SetTextFont(42)
        Label_BL.Draw("same")

    legend.AddEntry(dummy,Fnames[0],'ep')
    for num in range(1,len(hists)):
        legend.AddEntry(hists[num],Fnames[num],'F')
    for H in range(len(SignalHists)):
        legend.AddEntry(SignalHists[H], FnamesS[H],'L')
    legend.Draw("same")
    if (hs.GetStack().Last().Integral()>0 and '1Bjet'!=reg):
        Label_DM = ROOT.TLatex(0.2,0.75,"Data/MC = " + str(round(hists[0].Integral()/hs.GetStack().Last().Integral(),2)))
        Label_DM.SetNDC()
        Label_DM.SetTextFont(42)
        Label_DM.Draw("same")

    pad1.Update()

    pad2.cd()
    SumofMC = hs.GetStack().Last()
    dummy_ratio = hists[0].Clone()
    dummy_ratio.SetTitle("")
    dummy_ratio.SetMarkerStyle(20)
    dummy_ratio.SetMarkerSize(1.2)
    dummy_ratio.GetXaxis().SetTitle(varname)
#    dummy_ratio.GetXaxis().CenterTitle()
    dummy_ratio.GetYaxis().CenterTitle()
    dummy_ratio.GetXaxis().SetMoreLogLabels()
    dummy_ratio.GetXaxis().SetNoExponent()
    dummy_ratio.GetXaxis().SetTitleSize(0.04/0.3)
    dummy_ratio.GetYaxis().SetTitleSize(0.04/0.3)
    dummy_ratio.GetXaxis().SetTitleFont(42)
    dummy_ratio.GetYaxis().SetTitleFont(42)
    dummy_ratio.GetXaxis().SetTickLength(0.05)
    dummy_ratio.GetYaxis().SetTickLength(0.05)
    dummy_ratio.GetXaxis().SetLabelSize(0.115)
    dummy_ratio.GetYaxis().SetLabelSize(0.089)
    dummy_ratio.GetXaxis().SetLabelOffset(0.02)
    dummy_ratio.GetYaxis().SetLabelOffset(0.01)
    dummy_ratio.GetYaxis().SetTitleOffset(0.42)
    dummy_ratio.GetXaxis().SetTitleOffset(1.1)
    dummy_ratio.GetYaxis().SetNdivisions(504)
    dummy_ratio.GetYaxis().SetRangeUser(0,2)
    dummy_ratio.Divide(SumofMC)
    dummy_ratio.SetStats(ROOT.kFALSE)
    dummy_ratio.GetYaxis().SetTitle('Data/Pred.')
    dummy_ratio.Draw("AXISSAMEY")
    dummy_ratio.Draw("AXISSAMEX")
    dummy_ratio.Draw("AXISSAMEY+")
    dummy_ratio.Draw("AXISSAMEX+")
    dummy_ratio.Draw("AXISSAMEX+")
    if '1Bjet'!=reg:
        dummy_ratio.Draw()
    canvas.Print(year + '/' + ch +'/'+reg+'/'+var + ".png")
    del canvas
    gc.collect()
def compare3Hist(A, B, C, textA="A", textB="B", textC="C",label_name="sample", can_name="can"):

    canvas = ROOT.TCanvas(can_name,can_name,10,10,1100,628)
    canvas.SetRightMargin(0.15)
    canvas.cd()

    pad_name = "pad"
    pad1=ROOT.TPad(pad_name, pad_name, 0.05, 0.3, 1, 0.99 , 0)
    pad1.Draw()
    pad1.SetLogy()
    pad2=ROOT.TPad(pad_name, pad_name, 0.05, 0.05, 1, 0.3 , 0)
    pad2.SetGridy();
    pad2.Draw()
    pad1.cd()

    A.SetLineColor( 1 )
    B.SetLineColor( 2 )
    C.SetLineColor( 4 )

    A.SetTitle("")
    A.GetXaxis().SetTitle('BDT output')
    A.GetYaxis().SetTitle('Event ')
    A.GetXaxis().SetTitleSize(0.05)
    A.GetYaxis().SetTitleSize(0.05)
    A.SetMaximum(1.2*max(A.GetMaximum(),B.GetMaximum(),C.GetMaximum()));
    A.SetMinimum(0.1);
    A.GetYaxis().SetTitleOffset(0.7)
    A.Draw()
    B.Draw('esame')
    C.Draw('esame')

    legend = ROOT.TLegend(0.7,0.75,1,1)
    legend.AddEntry(A ,textA,'l')
    legend.AddEntry(B ,textB,'l')
    legend.AddEntry(C ,textC,'l')
    legend.SetBorderSize(0)
    legend.SetTextFont(42)
    legend.SetTextSize(0.05)
    legend.Draw("same")

    Label_channel = ROOT.TLatex(0.15,0.8,can_name.split('_')[0])
    Label_channel.SetNDC()
    Label_channel.SetTextFont(42)
    Label_channel.Draw("same")
    Label_channel2 = ROOT.TLatex(0.15,0.65,'#color[2]{'+can_name.split('_')[-1]+'}')
    Label_channel2.SetNDC()
    Label_channel2.SetTextFont(42)
    Label_channel2.SetTextSize(0.085)
    Label_channel2.Draw("same")

    pad2.cd()
    ratioB = B.Clone()
    ratioB.Divide(A)
    ratioB.SetLineColor( 2 )
    ratioB.SetMaximum(1.2)
    ratioB.SetMinimum(0.98)
    r = ratioB.Clone()
    fontScale = 2
    nbin = ratioB.GetNbinsX()
    x_min= ratioB.GetBinLowEdge(1)
    x_max= ratioB.GetBinLowEdge(nbin)+ratioB.GetBinWidth(nbin)
#    ratio_y_min=0.95*r.GetBinContent(r.FindFirstBinAbove(0))
#    ratio_y_max=1.05*r.GetBinContent(r.GetMaximumBin())
    dummy_ratio = ROOT.TH2D("dummy_ratio","",nbin,x_min,x_max,1,0.6,1.4)
    dummy_ratio.SetStats(ROOT.kFALSE)
    dummy_ratio.GetYaxis().SetTitle('Ratio')
    dummy_ratio.GetXaxis().SetTitle("")
    dummy_ratio.GetXaxis().SetTitleSize(0.05*fontScale)
    dummy_ratio.GetXaxis().SetLabelSize(0.05*fontScale)
    dummy_ratio.GetXaxis().SetMoreLogLabels()
    dummy_ratio.GetXaxis().SetNoExponent()
    dummy_ratio.GetYaxis().SetNdivisions(505)
    dummy_ratio.GetYaxis().SetTitleSize(0.07*fontScale)
    dummy_ratio.GetYaxis().SetLabelSize(0.05 *fontScale)
    dummy_ratio.GetYaxis().SetTitleOffset(0.3)
    dummy_ratio.Draw('ex0')
    ratioB.Draw("esame")

    ratioC = C.Clone()
    ratioC.Divide(A)
    ratioC.SetLineColor( 4 )
    ratioC.Draw("esame")


    canvas.Print("3H_" + can_name + ".png")
    del canvas
    gc.collect()


if not os.path.exists('CombinedFilesRebinned'):
    os.makedirs('CombinedFilesRebinned')
if not os.path.exists('CombinedFilesRebinnedSmooth'):
    os.makedirs('CombinedFilesRebinnedSmooth')

year=['2016preVFP', '2016postVFP', '2017','2018']
year=['2018']
channels=["ee", "emu", "mumu"];
regions=["llB1"]

#nominalHists=['tt','LfvVectorEmutc', 'LfvVectorEmutu']
#nominalHists=['tt']
nominalHists=['tt']
nominalHists=['STBNV_TBCE','STBNV_TDUE']
#bins = array( 'd',[-0.6,-0.4,-0.2,-0.15,-0.1,-0.05,0,0.05,0.1,0.15,0.2,0.25,0.6,0.8] )
#bins = array( 'd',[-0.6,-0.5,-0.3,-0.2,-0.1,0,0.1,0.20,0.3,0.4] )
#bins = array( 'd',[-1,-0.5,-0.3,-0.25,-0.2,-0.15,-0.1,-0.05,0,0.05,0.1,0.15,0.20,0.25,0.4,1] )
#bins = array( 'd',[-1,-0.9,-0.8,-0.7,-0.6,-0.5,-0.4,-0.3,-0.2,-0.1,0.0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1] )
#bins = array( 'd',[-1,-0.8,-0.6,-0.4,-0.2,0.0,0.2,0.4,0.6,0.8,1] )
#bins = array( 'd',[-1,-0.8,-0.6,-0.4,-0.2,0.0,0.2,0.4,0.6,0.75,0.9,1] )
bins = array( 'd',[-1,-0.8,-0.6,-0.4,-0.2,0.0,0.2,0.4,0.6,0.8,1] )

couplings=['cS','cT']
os.system("rm -rf CombinedFilesRebinned")
os.system("rm -rf CombinedFilesRebinnedSmooth")
os.system("mkdir CombinedFilesRebinned")
os.system("mkdir CombinedFilesRebinnedSmooth")
smoothingSys=['CR','Tune','hdamp']
plotingSys=['CR','Tune','hdamp','muonRes', 'muonScale']
plotingSys=['pdf', 'Signal_QS']
samples=['Fakes'  ,'Diboson'  ,'TTX' ,'Other']
sn=["FCNC-Prod_quad_cQe", "FCNC-Deca_quad_cQe"]
sname={"FCNC-Prod_quad_cQe":"FCNC-Production (cQe=0.5)", "FCNC-Deca_quad_cQe":"FCNC-Decay (cQe=3)"}
for p in plotingSys:
    os.system("rm -rf error"+p)
    os.system("mkdir error"+p)
f1 = ROOT.TFile.Open('/users/rgoldouz/FCNC/NanoAnalysis/combine/CombinedFilesFCNC_v2/2018_3loffZhigh_1bHj_MVATU.root')
my_list = f1.GetListOfKeys()
Hists=[]
HistsDraw=[]
for obj in my_list: # obj is TKey
    if obj.GetClassName() == "TH1F":
        Hists.append(obj.GetName())
for H in Hists:
    if H[-2:]=='Up':
        nominalH='_'.join(H.split('_')[:-1])
        if '_'.join(H.split('_')[:-1]) not in Hists:
            nominalH='_'.join(H.split('_')[:-2])
        #print H
        print nominalH
        if "FCNC" not in H:
            continue
        if 'CMS_eff_m_total' not in H:
            continue
        A1 = f1.Get(nominalH)
     #   A1 = f1.Get(H[:-2])
        A2 = f1.Get(H)
        A3 = f1.Get(H[:-2]+'Down')
        compare3Hist(A1,A2,A3,'nominal', 'Up','Down',H[:-2] ,H[:-2])
###HH=[]
###HHname=[]
###HHsig=[]
###HHsigname=[]
###for H in Hists:
###    if 'data' in H:
###        HH.append(f1.Get(H))
###        HHname.append('data')
###    if H.split('_')[-1] in samples:
###        HH.append(f1.Get(H))
###        HHname.append(H.split('_')[-1])
###    if H in sn:
###        print H
###        BH=f1.Get(H)
###        if 'Prod' in H:
###            BH.Scale(0.25)
###        if 'Deca' in H:
###            BH.Scale(9)
###        HHsig.append(BH)
###        HHsigname.append(sname[H])
###stackPlots(HH, HHsig, HHname, HHsigname,'3l','off-Z','2017','sample','BDT output')
###f1.Close()

