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
import os.path
#TGaxis.SetMaxDigits(2)

def EFTtoNormal(H, wc):
    hpx    = ROOT.TH1F( H.GetName(), H.GetName(), H.GetXaxis().GetNbins(), H.GetXaxis().GetXmin(),H.GetXaxis().GetXmax() )
    r=1
    for b in range(hpx.GetNbinsX()):               
        if H.GetBinContent(b+1,ROOT.WCPoint("NONE"))>0:
            r = H.GetBinError(b+1)/H.GetBinContent(b+1,ROOT.WCPoint("NONE")) 
        hpx.SetBinContent(b+1, H.GetBinContent(b+1,wc))
        hpx.SetBinError(b+1, r*H.GetBinContent(b+1,wc)) 
    if hpx.Integral()>0:
        hpx.Scale(1/hpx.Integral())
    return hpx

def stackPlots(hists, SignalHists, Fnames, ch = "channel", reg = "region", year='2016', var="sample", varname="v"):
    if not os.path.exists(year):
       os.makedirs(year)
    if not os.path.exists(year + '/' + ch):
       os.makedirs(year + '/' + ch)
    if not os.path.exists(year + '/' + ch +'/'+reg):
       os.makedirs(year + '/' + ch +'/'+reg)
    hs = ROOT.THStack("hs","")
    for num in range(len(hists)):
        hists[num].SetBinContent(hists[num].GetXaxis().GetNbins(), hists[num].GetBinContent(hists[num].GetXaxis().GetNbins()) + hists[num].GetBinContent(hists[num].GetXaxis().GetNbins()+1))
    for num in range(len(SignalHists)):
        SignalHists[num].SetBinContent(SignalHists[num].GetXaxis().GetNbins(),SignalHists[num].GetBinContent(SignalHists[num].GetXaxis().GetNbins()) + SignalHists[num].GetBinContent(SignalHists[num].GetXaxis().GetNbins()+1))
    for num in range(1,len(hists)):
        hs.Add(hists[num])

    dummy = hists[0].Clone()

    
    canvas = ROOT.TCanvas(year+ch+reg+var,year+ch+reg+var,50,50,865,780)
    canvas.SetGrid();
    canvas.SetBottomMargin(0.17)
    canvas.cd()

    legend = ROOT.TLegend(0.7,0.55,0.9,0.88)
    legend.SetBorderSize(0)
    legend.SetTextFont(42)
    legend.SetTextSize(0.04)

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
    dummy.Draw("e")
    hs.Draw("histSAME")
    for H in SignalHists:
        H.SetLineWidth(2)
        H.SetFillColor(0)
        H.SetLineStyle(9)
        H.Draw("histSAME")
    dummy.Draw("eSAME")
    dummy.Draw("AXISSAMEY+")
    dummy.Draw("AXISSAMEX+")

    Lumi = '137.42'
    if (year == '2016'):
        Lumi = '35.92'
    if (year == '2017'):
        Lumi = '41.53'
    if (year == '2018'):
        Lumi = '59.97'
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


    legend.AddEntry(dummy,Fnames[0],'ep')
    for num in range(1,len(hists)):
        legend.AddEntry(hists[num],Fnames[num],'F')
    for H in range(len(SignalHists)):
        legend.AddEntry(SignalHists[H], Fnames[len(hists)+H],'L')
    legend.Draw("same")

    if (hs.GetStack().Last().Integral()>0):
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
    dummy_ratio.Draw()
    dummy_ratio.Draw("AXISSAMEY+")
    dummy_ratio.Draw("AXISSAMEX+")
    canvas.Print(year + '/' + ch +'/'+reg+'/'+var + ".png")
    del canvas
    gc.collect()

def drawHistallW(A,AN, R, I, Xlabel):
    canvas = ROOT.TCanvas(R+I,R+I,10,10,1100,628)
    canvas.cd()

    pad_name = "pad"
    pad1=ROOT.TPad(pad_name, pad_name, 0, 0, 1, 1 , 0)
    pad1.Draw()
    pad1.SetLeftMargin(0.12)
    pad1.SetRightMargin(0.05)
    pad1.SetBottomMargin(0.12)
    pad1.SetFillStyle(0)
    pad1.cd()
#    pad1.SetLogy()
    A[0].SetTitle(R.split('_')[0] + ' (' + R.split('_')[-2] + ')')
    A[0].GetXaxis().SetTitle(R.split('_')[-1])
    if R.split('_')[-1]=="massLlNotFromTopMc":
        A[0].GetXaxis().SetTitle("M(ll) [OS-SF]")
    A[0].GetYaxis().SetTitle(Xlabel)
    A[0].GetYaxis().SetTitleSize(0.06)
    A[0].GetXaxis().SetTitleSize(0.06)
    A[0].SetTitleSize(0.06)
    A[0].GetYaxis().SetTitleOffset(0.8)
    A[0].GetXaxis().SetTitleOffset(0.8)

    maxi=A[0].GetMaximum()
    mini=A[0].GetMinimum()
    for i in range(len(A)):
        A[i].SetLineColor(i+1)
        A[i].SetLineWidth(2)
        if (i+1)==5:
            A[i].SetLineColor(28)
        if A[i].GetMaximum()>maxi:
            maxi=A[i].GetMaximum()
        if A[i].GetMinimum()<mini:
            mini=A[i].GetMinimum()
        if i==9:
            A[i].SetMarkerColor(12);

    A[0].SetMinimum(0);
    A[0].SetMaximum(maxi * 1.35);

    leg = ROOT.TLegend(0.67,0.72,0.88,0.88)

    for i in range(len(A)):
        A[i].Draw("eHIST SAME")
        leg.AddEntry(A[i], AN[i]                           , "L");

    A[0].Draw("AXISSAMEY+")
    A[0].Draw("AXISSAMEX+")

    leg.SetBorderSize(0)
    leg.SetTextFont(42)
    leg.SetTextSize(0.05)
    leg.Draw("same")

    canvas.Print(R+".png")
    del canvas
    gc.collect()


def drawHistXS(A,AN, R, I, Xlabel):
    canvas = ROOT.TCanvas(R+I,R+I,10,10,628,628)
    canvas.cd()

    pad_name = "pad"
    pad1=ROOT.TPad(pad_name, pad_name, 0, 0, 1, 1 , 0)
    pad1.Draw()
    pad1.SetLeftMargin(0.12)
    pad1.SetRightMargin(0.5)
    pad1.SetBottomMargin(0.12)
    pad1.SetFillStyle(0)
    pad1.cd()
    pad1.SetLogy()
    A[0].SetTitle(R.split('_')[0] + ' (' + R.split('_')[-2] + ')')
    A[0].GetXaxis().SetTitle('')
    A[0].GetYaxis().SetTitle(Xlabel)
    A[0].GetYaxis().SetTitleSize(0.06)
    A[0].GetXaxis().SetTitleSize(0.06)
    A[0].GetXaxis().SetLabelSize(0)
    A[0].SetTitleSize(0.06)
    A[0].GetYaxis().SetTitleOffset(0.8)
    A[0].GetXaxis().SetTitleOffset(0.8)

    maxi=A[0].GetMaximum()
    mini=A[0].GetMinimum()
    for i in range(len(A)):
        A[i].SetLineColor(i+1)
        A[i].SetLineWidth(2)
        if (i+1)==5:
            A[i].SetLineColor(28)
        if A[i].GetMaximum()>maxi:
            maxi=A[i].GetMaximum()
        if A[i].GetMinimum()<mini:
            mini=A[i].GetMinimum()
        if i>8:
            A[i].SetLineColor(i+29);
    for i in range(len(A)):
        A[i].SetMinimum(mini*0.8);
        A[i].SetMaximum(maxi * 1.35);
        A[i].SetLineStyle(i);

    leg = ROOT.TLegend(0.52,0.1,0.95,0.88)

    for i in range(len(A)):
        A[i].Draw("eHIST SAME")
        leg.AddEntry(A[i], AN[i]                           , "L");

    A[0].Draw("AXISSAMEY+")
    A[0].Draw("AXISSAMEX+")

    leg.SetBorderSize(0)
    leg.SetTextFont(42)
    leg.SetTextSize(0.05)
    leg.Draw("same")

    canvas.Print(R+".png")
    del canvas
    gc.collect()


HistAddress = '/afs/crc.nd.edu/user/r/rgoldouz/FCNC/NanoAnalysis/hists/'
couplingsName = ['cpQM','cpt','ctA','ctZ','ctG','cQlM','cQe','ctl','cte','ctlS','ctlT', 'ctp']
QF= 'c'
processname = ['tHProduction',  'tllProduction_noH',  QF+'HDecay',    QF+'llDecay_noH']

RefrencePoints = {
'tHProduction':[0.285     ,0.285    ,0.264    ,0.075   ,0.2  ,0.14    ,0.14  ,0.14  ,0.14  ,0.14     ,0.03, 3],
'tllProduction_noH':[0.22     ,0.22    ,0.22    ,0.07   ,0.0158  ,0.14    ,0.14  ,0.14  ,0.2  ,0.2     ,0.03, 3],
QF+'HDecay':[0.285     ,0.285    ,0.264    ,0.075   ,0.0158  ,0.14    ,0.14  ,0.14  ,0.14  ,0.14     ,0.03, 3],
QF+'llDecay_noH':[2     ,2    ,1    ,0.5  ,1.0  ,0.2  ,1.5    ,1.5  ,1.5  ,1.5  ,2.2     ,0.3   ]
}
Ivalue        = [0.285     ,0.285    ,0.264    ,0.075   ,0.0158  ,0.14    ,0.14  ,0.14  ,0.14  ,0.14     ,0.03, 3]

variables=[
"topPtLHE",
"aTopPtLHE",
"topEtaLHE",
"aTopEtaLHE",
"leadingLeptonPtMc",
"leadingLeptonEtaMc",
"massLlNotFromTopMc",
"ZPtMc",
"ZEtaMc",
"HPtMc",
"HEtaMc",
"eventsAll"]

for i in range(len(processname)):
    FilesRwgt = ROOT.TFile.Open(HistAddress+'2017_t'+QF+'FCNCrwgt_' +processname[i] + '.root')
    FilesRwgt.Get('eventsAll').GetSumFit().save(processname[i]+'.tex')
    text = 'EFTrwgt1_'
    for c in range(len(RefrencePoints[processname[i]])):
        text = text+ couplingsName[c] + '_' + str(RefrencePoints[processname[i]][c]) +'_' 
    cs = FilesRwgt.Get('eventsAll')
    wc1 = ROOT.WCPoint(text[:-1])
    cs.Scale(wc1)
    txs = cs.Integral()
    print processname[i] + ' total xs=' + str(cs.Integral()) 

    text = 'EFTrwgt1_'
    for c in range(len(RefrencePoints[processname[i]])):
        if couplingsName[c] in ['ctG']:
            text = text+ couplingsName[c] + '_' + str(RefrencePoints[processname[i]][c]) +'_'
        else:
            text = text+ couplingsName[c] + '_0.001_'
    wc1 = ROOT.WCPoint(text[:-1])
    cs.Scale(wc1)
    print processname[i] + ' ctG xs=' + str(cs.Integral()) + ' fr=' + str(cs.Integral()/txs)

    text = 'EFTrwgt1_'
    for c in range(len(RefrencePoints[processname[i]])):
        if couplingsName[c] in ['ctA']:
            text = text+ couplingsName[c] + '_' + str(RefrencePoints[processname[i]][c]) +'_'
        else:
            text = text+ couplingsName[c] + '_0.001_'
    wc1 = ROOT.WCPoint(text[:-1])
    cs.Scale(wc1)
    print processname[i] + ' ctA xs=' + str(cs.Integral()) + ' fr=' + str(cs.Integral()/txs)

    text = 'EFTrwgt1_'
    for c in range(len(RefrencePoints[processname[i]])):
        if couplingsName[c] in ['cpQM','cpt','ctZ']:
            text = text+ couplingsName[c] + '_' + str(RefrencePoints[processname[i]][c]) +'_'
        else:
            text = text+ couplingsName[c] + '_0.001_'
    wc1 = ROOT.WCPoint(text[:-1])
    cs.Scale(wc1)
    print processname[i] + ' cpqm+cpt+ctz xs=' + str(cs.Integral()) + ' fr=' + str(cs.Integral()/txs)

    text = 'EFTrwgt1_'
    for c in range(len(RefrencePoints[processname[i]])):
        if couplingsName[c] in ['cQlM','cQe','ctl','cte','ctlS','ctlT']:
            text = text+ couplingsName[c] + '_' + str(RefrencePoints[processname[i]][c]) +'_'
        else:
            text = text+ couplingsName[c] + '_0.001_'
    wc1 = ROOT.WCPoint(text[:-1])
    cs.Scale(wc1)
    print processname[i] + ' four fermi xs=' + str(cs.Integral()) + ' fr=' + str(cs.Integral()/txs)
 
    for j in range(len(couplingsName)):
        if not os.path.isfile(HistAddress+'2017_t'+QF+'FCNC_' +processname[i] + couplingsName[j] +'.root'):
            continue
        FilesFix = ROOT.TFile.Open(HistAddress+'2017_t'+QF+'FCNC_' +processname[i] + couplingsName[j] +'.root')
        for numvar, namevar in enumerate(variables):
            HH=[]
            HHName=[]
            Rwgt = FilesRwgt.Get(namevar)
            Fix = FilesFix.Get(namevar)
            Rwgt2 = Rwgt.Clone()
            text = 'EFTrwgt1_'
            for C in couplingsName:
                if C==couplingsName[j]:
                    text = text+ C + '_1_'
                else:
                    text = text+ C + '_0.001_'
            wc1 = ROOT.WCPoint(text[:-1])
            Rwgt.Scale(wc1)
            HH.extend([Rwgt,Fix])
            HHName.extend(['Reweighted', 'Fixed, ' + couplingsName[j] + ' = 1'])
            drawHistallW(HH,HHName, processname[i] + '_'  + couplingsName[j] + '_' +namevar , "","cross section [pb]")
    os.system('mkdir plot_t' +QF+'FCNC_' + processname[i])
    os.system('mv *.png plot_t'+QF+'FCNC_' + processname[i])

##for i in range(len(processname)):
##    HH=[]
##    HHName=[]
##    FilesRwgt = ROOT.TFile.Open(HistAddress+'tuFCNC_' +processname[i] + '_rwgt.root')
##    if processname[i]=='uHDecay':
##        continue
##    for j in range(len(couplingsName)):
##        if not os.path.isfile(HistAddress+'tuFCNC_' +processname[i] + couplingsName[j] +'.root'):
##            continue
##        for numvar, namevar in enumerate(variables):
##            if not namevar =="eventsAll":
##                continue
##            Rwgt = FilesRwgt.Get(namevar)
##            text = 'EFTrwgt1_' + couplingsName[j] + '_1'
##            wc1 = ROOT.WCPoint(text)
##            Rwgt.ScaleFits(0.01)
##            Rwgt.Scale(wc1)
##            HH.append(Rwgt)
##            HHName.append(couplingsName[j] + " [" + str(round(Rwgt.Integral(),1)) + " fb]")
##            print couplingsName[j]+' cross section = '+str(Rwgt.Integral())
##            print couplingsName[j]+' for 1pb xs = '+str(math. sqrt(1/Rwgt.Integral()))
##    drawHistXS(HH,HHName, processname[i]  + '_XS_XS'   , "","cross section [fb]")
##
##FilesRwgt = ROOT.TFile.Open(HistAddress+'tuFCNC_' +'uHDecay'+ '_rwgt.root')
##HH=[]
##HHName=[]
##Rwgt = FilesRwgt.Get("eventsAll")
##text = 'EFTrwgt1_ctp_1'
##wc1 = ROOT.WCPoint(text)
##Rwgt.ScaleFits(0.01)
##Rwgt.Scale(wc1)
##HH.append(Rwgt)
##HHName.append('ctp' + " [" + str(round(Rwgt.Integral(),1)) + " fb]")
##drawHistXS(HH,HHName,'uHDecay' + '_XS_XS'   , "","cross section [fb]")
##
##
##FilesRwgt = ROOT.TFile.Open(HistAddress+'tuFCNC_tllProduction_noH_rwgt.root')
##FilesRwgtOld = ROOT.TFile.Open(HistAddress+'tuFCNC_tllProduction_noH_rwgtOld.root')
##for numvar, namevar in enumerate(variables):
##    HH=[]
##    HHName=[]
##    Rwgt = FilesRwgt.Get(namevar)
##    Rwgt2 = Rwgt.Clone()
##    RwgtOld = FilesRwgtOld.Get(namevar)
##    text = 'EFTrwgt1_cpQM_2.0_cpt_2_ctA_2_ctZ_1_ctG_0.3_cQlM_1.5_cQe_0.5_ctl_0.5_cte_1_ctlS_1_ctlT_0.3'
##    wc1 = ROOT.WCPoint(text)
##    Rwgt.Scale(wc1)
##    text2 = 'EFTrwgt1_cpQM_2.0_cpt_2_ctA_2_ctZ_1_ctG_0.1_cQlM_1.5_cQe_2.5_ctl_0.5_cte_1_ctlS_1_ctlT_0.4'
##    wc2 = ROOT.WCPoint(text2)
##    Rwgt2.Scale(wc2)
##    RwgtOld.Scale(wc1)
##    HH.extend([Rwgt,RwgtOld,    Rwgt2])
##    HHName.extend(['Reweighted to Ref1', 'Fixed at Ref1', 'Reweighted to Ref2'])
##    drawHistallW(HH,HHName, 'tllProduction_All' + '_' +namevar , "","N events/bin (L=100/fb)")

#FR =  ROOT.TFile.Open(HistAddress + 'ullDecay_noH_Henry.root')
##FR = ROOT.TFile.Open(HistAddress + 'ullDecay_noH.root')
#ROOT.TFile.Open(HistAddress +processname[0] + '.root').Get("weight").GetSumFit().save('Coup.tex')
##canvas = ROOT.TCanvas('a','a',50,50,865,780)
##A=FR.Get("l1Pt")
###A.Draw()
##B=A.Clone()
##wc1=ROOT.WCPoint("smpt")
##B.Scale(wc1)
##B.SetLineColor(2)
###B.Draw("same")
##B.ScaleFits(1/B.Integral())
##C=A.Clone()
##wc2=ROOT.WCPoint("EFTrwgt1_ctlT2_10_ctlT1_10")
##C.Scale(wc2)
##C.ScaleFits(1/C.Integral())
##C.SetLineColor(1)
##C.Divide(B)
##C.SetMinimum(0);
##C.SetMaximum(2);
##C.Draw("same")
##D=A.Clone()
##wc3=ROOT.WCPoint("EFTrwgt1_cQl32_10_cQl31_10")
##D.Scale(wc3)
##D.SetLineColor(6)
###D.Draw("same")
##canvas.Print("W.png")
#
#for numvar, namevar in enumerate(variables):
#    HH=[]
#    HHName=[]
#    for i in range(len(processname)):
#        h2 = Hists[i][numvar].Clone()
##        h1 = FR.Get(namevar).Clone()
##        h1.GetSumFit().save("FIT.txt"+namevar)
#        text = 'EFTrwgt1_ctA_1'
##        print couplingsName[f] + ' , ' + str(h1.GetSumFit().evalPoint(ROOT.WCPoint(text))/41530.0)
#        wc1 = ROOT.WCPoint(text)
#        h2.Scale(wc1)
##        h2.ScaleFits(1/h2.Integral())
##        print str(h2.Integral())
##        HH.append(EFTtoNormal(h2,wc1))
#        HH.append(h2)
#        print str(h2.Integral())
#        HHName.append(processname[i])
##        HH.append(h2)
##        HHName.append('nominal ' + couplingsName[f] + '=1')
#    HH.append(FR.Get(namevar))
##    HH.append(EFTtoNormal(FR.Get(namevar),wc1))
#    HHName.append('ullDecay_noH_Henry')
##    print str(FR.Get(namevar).Integral()) +" & " + str(FRH.Get(namevar).Integral()) +" & " + str(h2.Integral())
##    print str(FR.Get(namevar).GetEntries()) +" & " + str(FRH.Get(namevar).GetEntries() )
#    drawHistallW(HH,HHName, namevar , "","Normalized entries")
#
##for numvar, namevar in enumerate(variables):
##    for f in range(len(couplingsName)):
##        for i in range(len(processname)):
##            HH=[]
##            HHName=[]
##            h2 = Hists[f][i][numvar].Clone()
##            text = 'EFTrwgt1_cS_1_cT_1'
##            wc1 = ROOT.WCPoint(text)
##            h2.Scale(wc1)
##            HH.append(h2)
##            HHName.append(processname[i]+couplingsName[f]+"(S=1,T=1)")
##            h2 = Hists[f][i][numvar].Clone()
##            text = 'EFTrwgt1_cS_1_cT_0'
##            wc1 = ROOT.WCPoint(text)
##            h2.Scale(wc1)
##            HH.append(h2)
##            HHName.append(processname[i]+couplingsName[f]+"(S=1,T=0)")
##            h2 = Hists[f][i][numvar].Clone()
##            text = 'EFTrwgt1_cS_0_cT_1'
##            wc1 = ROOT.WCPoint(text)
##            h2.Scale(wc1)
##            HH.append(h2)
##            HHName.append(processname[i]+couplingsName[f]+"(S=0,T=1)")
##            drawHistallW(HH,HHName, namevar , processname[i]+couplingsName[f],"N events (2017)")
