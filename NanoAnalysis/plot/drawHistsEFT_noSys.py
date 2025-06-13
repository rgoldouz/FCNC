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

def EFTtoNormal(H, wc):
    hpx    = ROOT.TH1F( H.GetName(), H.GetName(), H.GetXaxis().GetNbins(), H.GetXaxis().GetXmin(),H.GetXaxis().GetXmax() )
    r=1
    for b in range(hpx.GetNbinsX()):
        content = H.GetBinContent(b+1,wc)
        if math.isnan(content):
            print  H.GetName()+"Bin content is NaN"
        if math.isinf(content):
            print  H.GetName()+"Bin content is inf"
#        if H.GetBinContent(b+1,ROOT.WCPoint("NONE"))>0:
#            r = H.GetBinError(b+1)/H.GetBinContent(b+1,ROOT.WCPoint("NONE"))
        hpx.SetBinContent(b+1, H.GetBinContent(b+1,wc))
        hpx.SetBinError(b+1, H.GetBinError(b+1))
    hpx.SetLineColor(H.GetLineColor())
    hpx.SetLineStyle(H.GetLineStyle())
    hpx.SetBinContent(hpx.GetXaxis().GetNbins(), hpx.GetBinContent(hpx.GetXaxis().GetNbins()) + hpx.GetBinContent(hpx.GetXaxis().GetNbins()+1))
#    if hpx.Integral()>0:
#        hpx.Scale(1/hpx.Integral())
    return hpx

def cutFlowTable(hists, samples, regions, ch, year,caption='2016', nsig=6):
    mcSum = list(0 for i in xrange(0,len(regions)))
    for ids, s in enumerate(samples):
        if ids==0:
            continue
        for idr, r in enumerate(regions):
            if ids<nsig:
                mcSum[idr] += hists[year][ids][ch][idr][2].Integral() 
#    table = '\\begin{sidewaystable*}' + "\n"
    table = '\\begin{table*}' + "\n"
    table += '\\centering' + "\n"
    table += '\\caption{' + caption +": Number of expected signal and background events, compared to the event yields in the data, after various selection steps. Percentage event fractions of the MC predictions are given in brackets.}\n"
#    table += '\\resizebox{\\textwidth}{!}{ \n'
    table += '\\begin{tabular}{|l|l|l|l|l|l|l|l|l|l|l|}' + "\n"
    table += '\\hline' + "\n"
    table += 'Samples & ' + ' & '.join(regions) + '\\\\' + "\n"
    table += '\\hline' + "\n"
    for ids, s in enumerate(samples):
        if ids==0:
            continue
        table += s 
        for idr, r in enumerate(regions):
            if ids<nsig:
                table += (' & ' + str(round(hists[year][ids][ch][idr][2].Integral(),2)) + '[' + str(round((100*hists[year][ids][ch][idr][2].Integral())/mcSum[idr],2)) +'\%]')
            else:
                table += (' & ' + str(round(hists[year][ids][ch][idr][2].Integral(),2)))
#            if hists[year][ids][ch][idr][2].Integral()>0:
#                print s+' ***********stat Error:' +str(math.sqrt(hists[year][ids][ch][idr][2].GetSumw2().GetSum())/hists[year][ids][ch][idr][2].Integral()) 
        table += '\\\\' + "\n"    
    table += '\\hline' + "\n"
    table += 'Prediction '
    for idr, r in enumerate(mcSum):
        table += (' & ' + str(round(r,2)))
    table += '\\\\' + "\n"
    table += '\\hline' + "\n"
    table += 'Data '
    for idr, r in enumerate(regions):
        table += (' & ' + str(hists[year][0][ch][idr][2].Integral()))
    table += '\\\\' + "\n"
    table += '\\hline' + "\n"
    table += 'Data$/$Pred. '
    for idr, r in enumerate(mcSum):
        table += (' & ' + str(round(hists[year][0][ch][idr][2].Integral()/r,2)))
    table += '\\\\' + "\n"
    table += '\\hline' + "\n"
    table += '\\end{tabular}' + "\n"
    table += '\\end{table*}' + "\n"
#    table += '\\end{sidewaystable*}' + "\n"
    print table

def stackPlots(hists, SignalHists, Fnames,FnamesS, ch = "channel", reg = "region", year='2016', var="sample", varname="v"):
    Blinded=False

    if ch=="3lonZ" or ch=="3loffZhigh" or ch=="2lss":
        if reg=="1bLj" or reg== "1bHj":
            Blinded=True
    if not os.path.exists(year):
       os.makedirs(year)
    if not os.path.exists(year + '/' + ch):
       os.makedirs(year + '/' + ch)
    if not os.path.exists(year + '/' + ch +'/'+reg):
       os.makedirs(year + '/' + ch +'/'+reg)
    hs = ROOT.THStack("hs","")
    for num in range(1,len(hists)):
        hs.Add(hists[num])
    dummy = hists[0].Clone()
    canvas = ROOT.TCanvas(year+ch+reg+var,year+ch+reg+var,50,50,865,780)
    canvas.SetGrid();
    canvas.SetBottomMargin(0.17)
    canvas.cd()

    legend = ROOT.TLegend(0.7,0.45,0.9,0.88)
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
    bin_max_x=0
    if 'MVA' in var:
        pad1.SetLogy(ROOT.kTRUE)
        y_min=0.1
        y_max=1000*dummy.GetMaximum()
        for H in range(len(SignalHists)):
            last_bin = SignalHists[H].GetNbinsX()
            while last_bin >= 1 and SignalHists[H].GetBinContent(last_bin) == 0:
                last_bin -= 1
            if last_bin>bin_max_x:
                bin_max_x=last_bin
    xlimit=dummy.GetXaxis().GetBinUpEdge(bin_max_x)
    dummy.SetMarkerStyle(20)
    dummy.SetMarkerSize(1.2)
    dummy.SetTitle("")
    dummy.GetYaxis().SetTitle('Events')
    dummy.GetXaxis().SetLabelSize(0)
    dummy.GetYaxis().SetTitleOffset(0.8)
    dummy.GetYaxis().SetTitleSize(0.07)
    dummy.GetYaxis().SetLabelSize(0.04)
    dummy.GetYaxis().SetRangeUser(y_min,y_max)
    if Blinded:
        dummy.SetMarkerColor(0)
        dummy.SetLineColor(0)
        dummy.SetFillColor(0)
    dummy.Draw("e")
    if 'MVA' in var:
        pad1.SetLogx(ROOT.kTRUE)
        dummy.GetXaxis().SetRangeUser(0.01, 2*math.ceil(xlimit))

    hs.Draw("histSAME")
    for h in range(len(SignalHists)):
        SignalHists[h].SetLineWidth(2)
        SignalHists[h].SetFillColor(0)
        SignalHists[h].SetLineStyle(h+1)
        SignalHists[h].Draw("histSAME")
    if not Blinded:
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

    if Blinded:
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

    if (hs.GetStack().Last().Integral()>0 and not Blinded):
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
#    dummy_ratio.GetXaxis().SetMoreLogLabels()
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
    dummy_ratio.GetYaxis().SetRangeUser(0.8,1.2)
    dummy_ratio.Divide(SumofMC)
    dummy_ratio.SetStats(ROOT.kFALSE)
    dummy_ratio.GetYaxis().SetTitle('Data/Pred.')
    dummy_ratio.Draw("AXISSAMEY")
    dummy_ratio.Draw("AXISSAMEX")
    dummy_ratio.Draw("AXISSAMEY+")
    dummy_ratio.Draw("AXISSAMEX+")
    if Blinded:
        for b in range(dummy_ratio.GetNbinsX()):
            dummy_ratio.SetBinContent(b+1,100)
    dummy_ratio.Draw()
    if 'MVA' in var:
        pad2.SetLogx(ROOT.kTRUE)
        dummy_ratio.GetXaxis().SetRangeUser(0.01, 2*math.ceil(xlimit))
    canvas.Print(year + '/' + ch +'/'+reg+'/'+var + ".png")
    del canvas
    gc.collect()


#year=['2016','2017','2018','All']
year=['2016preVFP', '2016postVFP', '2017','2018']
year=['2017']
regions=["0b","1bLj", "1bHj","G1b"]
regionsName=["0b","1bxj", "1b$>$xj", "$>$1Bjet"]
channels=["2lss", "2los_Weighted", "2los_EpEm_CR", "2los_MUpMUm_CR", "2los_EpmMUmp_CR", "3lonZ", "3loffZhigh", "3loffZlow","4l_CR"]
channelsFake=["2lss_LF", "2lss_FF", "3lonZ_LLF", "3lonZ_LFF","3lonZ_FFF","3loffZhigh_LLF", "3loffZhigh_LFF","3loffZhigh_FFF", "3loffZlow_LLF", "3loffZlow_LFF","3loffZlow_FFF"]
variables=["lep1Pt","lep1Eta","lep1Phi","lep2Pt","lep2Eta","lep2Phi","llM","llPt","llDr","llDphi","jet1Pt","jet1Eta","jet1Phi","njet","nbjet","Met","MetPhi","nVtx","llMZw", "MVATU","MVATC", 
"lep3Pt","lep3Eta", "bJetPt", "bJetEta", "tH_topMass", "tH_HMass","tH_WtopMass", "tH_W1HMass","tH_W2HMass", "tH_HPt", "tH_HEta","tH_topPt", "tH_topEta", "tH_drWtopB",  "tH_drW1HW2H", "tZ_topMass", "tZ_ZMass", "tZ_WtopMass","tZ_ZPt","tZ_ZEta","tZ_topPt", "tZ_topEta"]
#variables=["lep1Pt",  "MVATU","MVATC"]
variablesName=["p_{T}(leading lepton)","#eta(leading lepton)","#Phi(leading lepton)","p_{T}(sub-leading lepton)","#eta(sub-leading lepton)","#Phi(sub-leading lepton)","M(ll)","p_{T}(ll)","#Delta R(ll)","#Delta #Phi(ll)","p_{T}(leading jet)","#eta(leading jet)","#Phi(leading jet)","Number of jets","Number of b-tagged jets","MET","#Phi(MET)","Number of vertices", "M(ll) [z window]","Likelihood ratio TU", "Likelihood ratio TC","lep3Pt","lep3Eta", "bJetPt", "bJetEta", "tH_topMass", "tH_HMass","tH_WtopMass", "tH_W1HMass","tH_W2HMass", "tH_HPt", "tH_HEta","tH_topPt", "tH_topEta", "tH_drWtopB",  "tH_drW1HW2H", "tZ_topMass", "tZ_ZMass", "tZ_WtopMass","tZ_ZPt","tZ_ZEta","tZ_topPt", "tZ_topEta"]
variablesFR=["lep1Pt","lep1Eta","lep1Phi","lep2Pt","lep2Eta","lep2Phi","llM","llPt","llDr","llDphi","jet1Pt","jet1Eta","jet1Phi","njet","nbjet","Met","MetPhi","nVtx","llMZw", "MVATU","MVATC",
"lep3Pt","lep3Eta", "bJetPt", "bJetEta", "tH_topMass", "tH_HMass","tH_WtopMass", "tH_W1HMass","tH_W2HMass", "tH_HPt", "tH_HEta","tH_topPt", "tH_topEta", "tH_drWtopB",  "tH_drW1HW2H", "tZ_topMass", "tZ_ZMass", "tZ_WtopMass","tZ_ZPt","tZ_ZEta","tZ_topPt", "tZ_topEta"]
variablesNameFR=["p_{T}(leading lepton)","#eta(leading lepton)","#Phi(leading lepton)","p_{T}(sub-leading lepton)","#eta(sub-leading lepton)","#Phi(sub-leading lepton)","M(ll)","p_{T}(ll)","#Delta R(ll)","#Delta #Phi(ll)","p_{T}(leading jet)","#eta(leading jet)","#Phi(leading jet)","Number of jets","Number of b-tagged jets","MET","#Phi(MET)","Number of vertices", "M(ll) [z window]","Likelihood ratio TU", "Likelihood ratio TC","lep3Pt","lep3Eta", "bJetPt", "bJetEta", "tH_topMass", "tH_HMass","tH_WtopMass", "tH_W1HMass","tH_W2HMass", "tH_HPt", "tH_HEta","tH_topPt", "tH_topEta", "tH_drWtopB",  "tH_drW1HW2H", "tZ_topMass", "tZ_ZMass", "tZ_WtopMass","tZ_ZPt","tZ_ZEta","tZ_topPt", "tZ_topEta"]
HistAddress = '/users/rgoldouz/FCNC/NanoAnalysis/hists/'


Samples = ['data.root','Triboson.root', 'Diboson.root', 'ttbar.root', 'ST.root','DY.root', 'Conv.root','TTX.root','FCNCProduction.root','FCNCDecay.root']
SamplesName = ['Data','Triboson', 'Diboson', 't#bar{t}', 'Single top','DY', 'Conv','TTX+TX','FCNC-Production','FCNC-Decay']# , 'BNV_ST_TBCE', 'BNV_ST_TBUE', 'BNV_ST_TDCE',  'BNV_ST_TDUE',  'BNV_ST_TSCE',  'BNV_ST_TSUE']
Samples = ['data.root','Triboson.root', 'Diboson.root', 'ttbar.root', 'ST.root','DY.root', 'Conv.root','TTX.root','FCNCTUProduction.root','FCNCTUDecay.root']
SamplesName = ['Data','Triboson', 'Diboson', 't#bar{t}', 'Single top','DY', 'Conv','TTX+TX','FCNC-Production','FCNC-Decay']#
fakeMC=['ttbar.root', 'ST.root','WJets.root']
colors =  [ROOT.kBlack,ROOT.TColor.GetColor("#3f90da"),ROOT.TColor.GetColor("#ffa90e"), ROOT.TColor.GetColor("#bd1f01"),ROOT.TColor.GetColor("#94a4a2"), ROOT.TColor.GetColor("#832db6"),ROOT.TColor.GetColor("#a96b59"),ROOT.TColor.GetColor("#e76300"),ROOT.TColor.GetColor("#b9ac70"),ROOT.TColor.GetColor("#717581"),ROOT.TColor.GetColor("#92dadd")]


bins = array( 'd',[0.01,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,2,50] )
binsDic = {
'2l':array( 'd',[0.01,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,2,4,50] ),
'3lonZ':array( 'd',[0.01,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.2,1.4,1.6,1.8,2,2.5,3,5.0,10.0,20.0,50.0] ),
'3loffZ':array( 'd',[0.01,0.1,0.2,0.3,0.6,1.0,2.0,5.0,50.0] ),
}

wc1 = ROOT.WCPoint("EFTrwgt4_cpQM_1.0_cpt_1.0_ctA_1.0_ctZ_0.5_ctG_0.1_cQlM_1.0_cQe_1.0_ctl_1.0_cte_1.0_ctlS_1.0_ctlT_0.05_ctp_1.0")

Hists = []
HistsFake = []
drawFakeRegions=True

for numyear, nameyear in enumerate(year):
    l0=[]
    Files = []
    for f in range(len(Samples)):
        l1=[]
        Files.append(ROOT.TFile.Open(HistAddress + nameyear+ '_' + Samples[f]))
        print HistAddress + nameyear+ '_' + Samples[f]
        for numch, namech in enumerate(channels):
            l2=[]
            for numreg, namereg in enumerate(regions):
                l3=[]
                for numvar, namevar in enumerate(variables):
                    for key in binsDic:
                        if key in namech:
                            bins=binsDic[key]
                    h= Files[f].Get(namech + '_' + namereg + '_' + namevar)
#                    print Samples[f] + '_' + namech + '_' + namereg + '_' + namevar + ":" + str(h.Integral())
#                    if 'njet' in namevar:
#                        print namech + '_' + namereg + '_' + namevar + str(h.GetBinFit(3).getDim())
#                        print namech + '_' + namereg + '_' + namevar + str(h.GetBinContent(3,wc1))
                    h= EFTtoNormal(h,wc1)
                    if 'MVA' in namevar:
                        h=h.Rebin(len(bins)-1,"",bins)
                    h.SetFillColor(colors[f])
                    h.SetLineColor(colors[f])
                    l3.append(h)
                l2.append(l3)
            l1.append(l2)
        l0.append(l1)
    Hists.append(l0)       

for numyear, nameyear in enumerate(year):
    l0=[]
    Files = []
    for f in range(len(Samples)):
        l1=[]
        Files.append(ROOT.TFile.Open(HistAddress + nameyear+ '_' + Samples[f]))
        print HistAddress + nameyear+ '_' + Samples[f]
        for numch, namech in enumerate(channelsFake):
            l2=[]
            for numreg, namereg in enumerate(regions):
                l3=[]
                for numvar, namevar in enumerate(variablesFR):
                    for key in binsDic:
                        if key in namech:
                            bins=binsDic[key]
                    h= Files[f].Get(namech + '_' + namereg + '_' + namevar)
#                    print Samples[f] + '_' + namech + '_' + namereg + '_' + namevar + ":" + str(h.Integral())
#                    print namevar + ":" + str(h.Integral())
#                    if 'njet' in namevar:
#                        print namech + '_' + namereg + '_' + namevar + str(h.GetBinFit(3).getDim())
#                        print namech + '_' + namereg + '_' + namevar + str(h.GetBinContent(3,wc1))
                    h= Files[f].Get(namech + '_' + namereg + '_' + namevar)
                    h= EFTtoNormal(h,wc1)
                    if 'MVA' in namevar:
                        h=h.Rebin(len(bins)-1,"",bins)
#                    h.SetFillColor(ROOT.kYellow+2)
#                    h.SetLineColor(ROOT.kYellow+2)
                    h.SetFillColor(colors[f])
                    h.SetLineColor(colors[f])
                    l3.append(h)
                l2.append(l3)
            l1.append(l2)
        l0.append(l1)
    HistsFake.append(l0)

if drawFakeRegions:
    for numyear, nameyear in enumerate(year):
        for numch, namech in enumerate(channelsFake):
            for numreg, namereg in enumerate(regions):
                for numvar, namevar in enumerate(variablesFR):
                    HH=[]
                    HHsignal=[]
                    SN=[]
                    SNsignal=[]
                    for f in range(len(Samples)):
                        if 'FCNC' in Samples[f]:
                            HistsFake[numyear][f][numch][numreg][numvar].SetLineColor(1)
                            HHsignal.append(HistsFake[numyear][f][numch][numreg][numvar])
                            SNsignal.append(SamplesName[f])
                        else:
                            HH.append(HistsFake[numyear][f][numch][numreg][numvar])
                            SN.append(SamplesName[f])
                    stackPlots(HH, HHsignal, SN, SNsignal, namech, namereg, nameyear,namevar,variablesNameFR[numvar])


for numyear, nameyear in enumerate(year):
    for numreg, namereg in enumerate(regions):
        for numvar, namevar in enumerate(variablesFR):
            HistsFake[numyear][0][channelsFake.index('2lss_LF')][numreg][numvar].Add(HistsFake[numyear][0][channelsFake.index('2lss_FF')][numreg][numvar],-1)
            HistsFake[numyear][0][channelsFake.index('3lonZ_LLF')][numreg][numvar].Add(HistsFake[numyear][0][channelsFake.index('3lonZ_LFF')][numreg][numvar],-1)
            HistsFake[numyear][0][channelsFake.index('3lonZ_LLF')][numreg][numvar].Add(HistsFake[numyear][0][channelsFake.index('3lonZ_FFF')][numreg][numvar])
            HistsFake[numyear][0][channelsFake.index('3loffZhigh_LLF')][numreg][numvar].Add(HistsFake[numyear][0][channelsFake.index('3loffZhigh_LFF')][numreg][numvar],-1)
            HistsFake[numyear][0][channelsFake.index('3loffZhigh_LLF')][numreg][numvar].Add(HistsFake[numyear][0][channelsFake.index('3loffZhigh_FFF')][numreg][numvar])
            HistsFake[numyear][0][channelsFake.index('3loffZlow_LLF')][numreg][numvar].Add(HistsFake[numyear][0][channelsFake.index('3loffZlow_LFF')][numreg][numvar],-1)
            HistsFake[numyear][0][channelsFake.index('3loffZlow_LLF')][numreg][numvar].Add(HistsFake[numyear][0][channelsFake.index('3loffZlow_FFF')][numreg][numvar])

fakeMap={
"2lss":"2lss_LF",
"3lonZ":"3lonZ_LLF", 
"3loffZhigh":"3loffZhigh_LLF", 
"3loffZlow":"3loffZlow_LLF"
}



for numyear, nameyear in enumerate(year):
    for numch, namech in enumerate(channels):
        for numreg, namereg in enumerate(regions):
            for numvar, namevar in enumerate(variables):
                HH=[]
                HHsignal=[]
                SN=[]
                SNsignal=[]
                for f in range(len(Samples)):
#                    if namech in fakeMap and Samples[f] in fakeMC:
#                        continue
#                    if '3L' in namech and 'DY' in SamplesName[f]:
#                        continue
                    if 'FCNC' in Samples[f]:
                        text = 'EFTrwgt4_cpQM_1.0_cpt_1.0_ctA_1.0_ctZ_0.5_ctG_0.1_cQlM_1.0_cQe_1.0_ctl_1.0_cte_1.0_ctlS_1.0_ctlT_0.05_ctp_1.0'
#                        text = 'EFTrwgt4_ctZ_0.5'
#                        wc1 = ROOT.WCPoint(text)
#                        Hists[numyear][f][numch][numreg][numvar].Scale(wc1)
                        Hists[numyear][f][numch][numreg][numvar].SetLineColor(1)
                        HHsignal.append(Hists[numyear][f][numch][numreg][numvar])
                        SNsignal.append(SamplesName[f])
                    else:
                        HH.append(Hists[numyear][f][numch][numreg][numvar])
                        SN.append(SamplesName[f])
                if namech in fakeMap and namevar in variablesFR:
                    HistsFake[numyear][0][channelsFake.index(fakeMap[namech])][numreg][variablesFR.index(namevar)].SetFillColor(ROOT.kYellow+2)
                    HistsFake[numyear][0][channelsFake.index(fakeMap[namech])][numreg][variablesFR.index(namevar)].SetLineColor(ROOT.kYellow+2)
                    HH.append(HistsFake[numyear][0][channelsFake.index(fakeMap[namech])][numreg][variablesFR.index(namevar)])
                    SN.append("Fake")
                if namech=="2lss":
                    Hists[numyear][0][channels.index("2los_Weighted")][numreg][numvar].SetFillColor(ROOT.TColor.GetColor("#92dadd"))
                    Hists[numyear][0][channels.index("2los_Weighted")][numreg][numvar].SetLineColor(ROOT.TColor.GetColor("#92dadd"))
                    HH.append(Hists[numyear][0][channels.index("2los_Weighted")][numreg][numvar])
                    SN.append("ChargeFlip")
                stackPlots(HH, HHsignal, SN, SNsignal, namech, namereg, nameyear,namevar,variablesName[numvar])
    os.system('tar -cvf '+nameyear+'.tar ' +nameyear)

le = '\\documentclass{article}' + "\n"
le += '\\usepackage{rotating}' + "\n"
le += '\\usepackage{rotating}' + "\n"
le += '\\begin{document}' + "\n"

print le
#    for numch, namech in enumerate(channels):
#        cutFlowTable(Hists, SamplesNameLatex, regionsName, numch, numyear, nameyear + ' ' + namech, 6 )
print '\\end{document}' + "\n"


