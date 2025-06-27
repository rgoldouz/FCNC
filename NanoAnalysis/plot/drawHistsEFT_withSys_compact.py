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
TGaxis.SetMaxDigits(2)

def EFTtoNormal(H, wc):
    nbins = H.GetNbinsX()
    bin_edges = [H.GetBinLowEdge(i + 1) for i in range(nbins)]
    bin_edges.append(H.GetXaxis().GetBinUpEdge(nbins))
    bin_array = array.array('d', bin_edges)
    hpx = ROOT.TH1F(H.GetName(), H.GetName(), nbins, bin_array)
    r=1
    for b in range(hpx.GetNbinsX()+1):
        content = H.GetBinContent(b+1,wc)
        if math.isnan(content):
            print  H.GetName()+"Bin content is NaN"
        if math.isinf(content):
            print  H.GetName()+"Bin content is inf"
        hpx.SetBinContent(b+1, H.GetBinContent(b+1,wc))
        hpx.SetBinError(b+1, H.GetBinError(b+1))
    hpx.SetBinContent(hpx.GetXaxis().GetNbins(), hpx.GetBinContent(hpx.GetXaxis().GetNbins()) + hpx.GetBinContent(hpx.GetXaxis().GetNbins()+1))
    hpx.SetBinError(hpx.GetXaxis().GetNbins(), (H.GetBinError(hpx.GetXaxis().GetNbins())**2 + H.GetBinError(hpx.GetXaxis().GetNbins()+1)**2)**0.5)
    hpx.SetLineColor(H.GetLineColor())
    hpx.SetLineStyle(H.GetLineStyle())
#    if hpx.Integral()>0:
#        hpx.Scale(1/hpx.Integral())
    return hpx


def sysEFTtoNormal(H, sys, c):
    wc = ROOT.WCPoint("EFTrwgt4_cnmb_1.0")
    hist = {}
    nbins = H.GetNbinsX()
    bin_edges = [H.GetBinLowEdge(i + 1) for i in range(nbins)]
    bin_edges.append(H.GetXaxis().GetBinUpEdge(nbins))
    bin_array = array.array('d', bin_edges)
    hpx = ROOT.TH1F(H.GetName(), H.GetName(), nbins, bin_array)

    for n, s in enumerate(sys):
        h = hpx.Clone("{}_{}".format(H.GetName(), s))
       # H.GetSumFit().save("a.txt")
        for b in range(0, nbins+2 ):  # include underflow (0) and overflow (nbins + 1)
            if H.GetBinContent(b,wc)==0:
                continue
            fit = H.GetBinFit(b)
            val = fit.getCoefficient(n)
            h.SetBinContent(b, val)
        h.SetLineColor(c[n]) 
        h.SetBinContent(h.GetXaxis().GetNbins(), h.GetBinContent(h.GetXaxis().GetNbins()) + h.GetBinContent(h.GetXaxis().GetNbins()+1))
        hist[s] = h

    return hist

def compareError(histsup,histsdown, sys, ch = "channel", reg = "region", year='2016', var="sample", varname="v", prefix = 'Theory'):
    if not os.path.exists('sysCompact/'+year):
       os.makedirs('sysCompact/'+ year)
    if not os.path.exists('sysCompact/'+year + '/' + ch):
       os.makedirs('sysCompact/'+year + '/' + ch)
    if not os.path.exists('sysCompact/'+year + '/' + ch +'/'+reg):
       os.makedirs('sysCompact/'+year + '/' + ch +'/'+reg)

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

    pad2.cd()
    maxi=0
    for n,G in enumerate(histsup):
        histsup[n].SetLineColor(n+1)
        histsup[n].SetLineWidth(2)
        histsup[n].SetFillColor(0)
        legend.AddEntry(histsup[n],sys[n],'L')
        if(histsup[n].GetMaximum()>maxi):
            maxi=G.GetMaximum()
        histsdown[n].SetLineColor(n+1)
        histsdown[n].SetFillColor(0)
        histsdown[n].SetLineWidth(2)
        if n==4:
            histsup[n].SetLineColor(ROOT.kOrange)
            histsdown[n].SetLineColor(ROOT.kOrange)
        if n==7:
            histsup[n].SetLineColor(ROOT.kGreen-1)
            histsdown[n].SetLineColor(ROOT.kGreen-1)
        if n==8:
            histsup[n].SetLineColor(28)
            histsdown[n].SetLineColor(28)
        if n==9:
            histsup[n].SetLineColor(46)
            histsdown[n].SetLineColor(46)
        if n==10:
            histsup[n].SetLineColor(30)
            histsdown[n].SetLineColor(30)
        if n==11:
            histsup[n].SetLineColor(38)
            histsdown[n].SetLineColor(38)
        if n==12:
            histsup[n].SetLineColor(17)
            histsdown[n].SetLineColor(17)
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
    canvas.Print('sysCompact/'+ year + '/' + ch +'/'+reg+'/sysCompact'+ prefix +'_'+var + ".png")
    del canvas
    gc.collect()
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

def stackPlots(hists, SignalHists, Fnames,FnamesS,errorRatio, ch = "channel", reg = "region", year='2016', var="sample", varname="v"):
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
    h_total = hs.GetStack().Last().Clone("h_total")  # Get the top of the stack (total)
    error_total=errorRatio.Clone()

    n_points = errorRatio.GetN()    
    for i in range(n_points):
        x = errorRatio.GetX()[i]             # keep X the same
        y_new = h_total.GetBinContent(i+1)   # modify Y
        exl = error_total.GetErrorXlow(i)     # keep X errors unchanged
        exh = error_total.GetErrorXhigh(i)
        eyl = error_total.GetErrorYlow(i) * y_new   # for example: scale Y low error
        eyh = error_total.GetErrorYhigh(i) * y_new  # scale Y high error
        error_total.SetPoint(i, x, y_new)
        error_total.SetPointError(i, exl, exh, eyl, eyh)

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
    error_total.SetFillColor(13)
    error_total.SetLineColor(13)
    error_total.SetFillStyle(3004)
    error_total.Draw("2same")

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
    dummy_ratio.GetYaxis().SetRangeUser(0.5,1.5)
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
    errorRatio.SetFillColor(13)
    errorRatio.SetLineColor(13)
    errorRatio.SetFillStyle(3004)
    errorRatio.Draw("2same")
    pad2.Update()
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
variables=["lep1Pt","lep1Eta","lep1Phi","lep2Pt","lep2Eta","lep2Phi","llM","llPt","llDr","llDphi","jet1Pt","jet1Eta","jet1Phi","njet","nbjet","Met","MetPhi","nVtx","llMZw",
"lep3Pt","lep3Eta", "bJetPt", "bJetEta", "tH_topMass", "tH_HMass","tH_WtopMass", "tH_W1HMass","tH_W2HMass", "tH_HPt", "tH_HEta","tH_topPt", "tH_topEta", "tH_drWtopB",  "tH_drW1HW2H", "tZ_topMass", "tZ_ZMass", "tZ_WtopMass","tZ_ZPt","tZ_ZEta","tZ_topPt", "tZ_topEta", "MVATU","MVATC"]
variablesName=["p_{T}(leading lepton)","#eta(leading lepton)","#Phi(leading lepton)","p_{T}(sub-leading lepton)","#eta(sub-leading lepton)","#Phi(sub-leading lepton)","M(ll)","p_{T}(ll)","#Delta R(ll)","#Delta #Phi(ll)","p_{T}(leading jet)","#eta(leading jet)","#Phi(leading jet)","Number of jets","Number of b-tagged jets","MET","#Phi(MET)","Number of vertices", "M(ll) [z window]","lep3Pt","lep3Eta", "bJetPt", "bJetEta", "tH_topMass", "tH_HMass","tH_WtopMass", "tH_W1HMass","tH_W2HMass", "tH_HPt", "tH_HEta","tH_topPt", "tH_topEta", "tH_drWtopB",  "tH_drW1HW2H", "tZ_topMass", "tZ_ZMass", "tZ_WtopMass","tZ_ZPt","tZ_ZEta","tZ_topPt", "tZ_topEta","Likelihood ratio TU", "Likelihood ratio TC"]

variablesFR=["lep1Pt","lep1Eta","lep1Phi","lep2Pt","lep2Eta","lep2Phi","jet1Pt","jet1Eta","jet1Phi","njet", "MVATU","MVATC"]
variablesNameFR=["p_{T}(leading lepton)","#eta(leading lepton)","#Phi(leading lepton)","p_{T}(sub-leading lepton)","#eta(sub-leading lepton)","#Phi(sub-leading lepton)","p_{T}(leading jet)","#eta(leading jet)","#Phi(leading jet)","Number of jets","MVATU","MVATC"]
HistAddress = '/users/rgoldouz/FCNC/NanoAnalysis/hists/'
variablesSys=["lep1Pt","lep1Eta","jet1Pt","jet1Eta","njet","Met", "nVtx", "MVATU","MVATC"]
variablesTh=["MVATU","MVATC"]

Samples = ['data.root','Triboson.root', 'Diboson.root', 'ttbar.root', 'ST.root','DY.root', 'Conv.root','TTX.root','FCNCTUProduction.root','FCNCTUDecay.root']
SamplesNormErr = [0, 0.1, 0.06, 0.05, 0.1, 0.05, 0.05, 0.15,0,0]
#Samples = ['data.root','FCNCTUProduction.root']
SamplesName = ['Data','Triboson', 'Diboson', 't#bar{t}', 'Single top','DY', 'Conv','TTX+TX','FCNC-Production','FCNC-Decay']#
fakeMC=['ttbar.root', 'ST.root','WJets.root']
channelsSys=["2lss", "3lonZ", "3loffZhigh"]
sys = ["eleRecoIdIso","muRecoIdIso","triggerSF","pu","prefiring","bcTagSfCorr","LTagSfCorr","bcTagSfUnCorr","LTagSfUnCorr","JetPuID"]
jetSys=["Jes","Jer"]
ThSys=["PDF","Renormalization","Factorization", "ISR", "FSR"]
colors =  [ROOT.kBlack,ROOT.TColor.GetColor("#3f90da"),ROOT.TColor.GetColor("#ffa90e"), ROOT.TColor.GetColor("#bd1f01"),ROOT.TColor.GetColor("#94a4a2"), ROOT.TColor.GetColor("#832db6"),ROOT.TColor.GetColor("#a96b59"),ROOT.TColor.GetColor("#e76300"),ROOT.TColor.GetColor("#b9ac70"),ROOT.TColor.GetColor("#717581"),ROOT.TColor.GetColor("#92dadd"),ROOT.kBlack,ROOT.TColor.GetColor("#3f90da"),ROOT.TColor.GetColor("#ffa90e"), ROOT.TColor.GetColor("#bd1f01"),ROOT.TColor.GetColor("#94a4a2"), ROOT.TColor.GetColor("#832db6"),ROOT.TColor.GetColor("#a96b59")]

fakeMap={
"2lss":"2lss_LF",
"3lonZ":"3lonZ_LLF",
"3loffZhigh":"3loffZhigh_LLF",
"3loffZlow":"3loffZlow_LLF"
}

bins = array.array( 'd',[0.01,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,2,50] )
binsDic = {
'2l':array.array( 'd',[0.01,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,2,4,50] ),
'3lonZ':array.array( 'd',[0.01,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.2,1.4,1.6,1.8,2,2.5,3,5.0,10.0,20.0,50.0] ),
'3loffZ':array.array( 'd',[0.01,0.1,0.2,0.3,0.6,1.0,2.0,5.0,50.0] ),
}

wc1 = ROOT.WCPoint("EFTrwgt4_cpQM_1.0_cpt_1.0_ctA_1.0_ctZ_0.5_ctG_0.1_cQlM_1.0_cQe_1.0_ctl_1.0_cte_1.0_ctlS_1.0_ctlT_0.05_ctp_1.0")

Hists = {}
HistsSysUp = {}
HistsSysDown = {}
HistsSysJecUp = {}
HistsSysJecDown = {}
Hists_copy = {}
HistsFake = {}
drawFakeRegions=True

for nameyear in year:
    Hists[nameyear] = {}
    Hists_copy[nameyear] = {}
    HistsSysUp[nameyear] = {}
    HistsSysDown[nameyear] = {}
    HistsSysJecUp[nameyear] = {}
    HistsSysJecDown[nameyear] = {}
    for f, sample in enumerate(Samples):
        sample_key = sample
        Hists[nameyear][sample_key] = {}
        Hists_copy[nameyear][sample_key] = {}
        HistsSysUp[nameyear][sample_key] = {}
        HistsSysDown[nameyear][sample_key] = {}
        HistsSysJecUp[nameyear][sample_key] = {}
        HistsSysJecDown[nameyear][sample_key] = {}
        file = ROOT.TFile.Open(HistAddress + nameyear + '_' + sample)
        for ch in channels:
            for reg in regions:
                for var in variables:
                    hist_key = "{}_{}_{}".format(ch,reg,var)
                    h = file.Get(hist_key)
                    h = EFTtoNormal(h, wc1)

                    # Apply binning if needed
                    if 'MVA' in var:
                        for key in binsDic:
                            if key in ch:
                                bins = binsDic[key]
                                h = h.Rebin(len(bins) - 1, "", bins)
                                break
                    h.SetFillColor(colors[f])
                    h.SetLineColor(colors[f])

                    # Store nominal histogram
                    Hists[nameyear][sample_key][hist_key] = h.Clone()
                    Hists_copy[nameyear][sample_key][hist_key]= h.Clone()
                    # Only get systematics for non-data samples and specific channels/vars
                    if f > 0 and ch in channelsSys:
                        HistsSysUp[nameyear][sample_key][hist_key] = {}
                        HistsSysDown[nameyear][sample_key][hist_key] = {}
                        # Up variation
                        h_up = file.Get("{}_{}_{}__Up".format(ch,reg,var))
                        hSys_up = sysEFTtoNormal(h_up, sys, colors)                            
                        HistsSysUp[nameyear][sample_key][hist_key]=hSys_up

                        # Down variation
                        h_down = file.Get("{}_{}_{}__Down".format(ch,reg,var))
                        hSys_down = sysEFTtoNormal(h_down, sys, colors)                            
                        HistsSysDown[nameyear][sample_key][hist_key]=hSys_down

                        HistsSysJecUp[nameyear][sample_key][hist_key] = {}
                        HistsSysJecDown[nameyear][sample_key][hist_key] = {}
                        for numsys, namesys in enumerate(jetSys):
                        # Up variation
                            h_up = file.Get("{}_{}_{}_{}__Up".format(ch,reg,var,namesys))
                            HistsSysJecUp[nameyear][sample_key][hist_key][namesys]=h_up

                        # Down variation
                            h_down = file.Get("{}_{}_{}_{}__Down".format(ch,reg,var,namesys))
                            HistsSysJecDown[nameyear][sample_key][hist_key][namesys]=h_down
for nameyear in year:
    HistsFake[nameyear] = {}
    for f, sample in enumerate(Samples):
        sample_key = sample
        HistsFake[nameyear][sample_key] = {}
        file = ROOT.TFile.Open(HistAddress + nameyear + '_' + sample)
        for ch in channelsFake:
            for reg in regions:
                for var in variables:
                    hist_key = "{}_{}_{}".format(ch,reg,var)
                    h = file.Get(hist_key)
                    h = EFTtoNormal(h, wc1)

                    # Apply binning if needed
                    if 'MVA' in var:
                        for key in binsDic:
                            if key in ch:
                                bins = binsDic[key]
                                h = h.Rebin(len(bins) - 1, "", bins)
                                break
                    h.SetFillColor(colors[f])
                    h.SetLineColor(colors[f])

                    # Store nominal histogram
                    HistsFake[nameyear][sample_key][hist_key] = h.Clone()

for numyear, nameyear in enumerate(year):
    for numreg, namereg in enumerate(regions):
        for numvar, namevar in enumerate(variables):
            HistsFake[nameyear][Samples[0]]["2lss_LF_{}_{}".format(namereg,namevar)].Add(HistsFake[nameyear][Samples[0]]["2lss_FF_{}_{}".format(namereg,namevar)],-1)
            HistsFake[nameyear][Samples[0]]["3lonZ_LLF_{}_{}".format(namereg,namevar)].Add(HistsFake[nameyear][Samples[0]]["3lonZ_LFF_{}_{}".format(namereg,namevar)],-1)
            HistsFake[nameyear][Samples[0]]["3lonZ_LLF_{}_{}".format(namereg,namevar)].Add(HistsFake[nameyear][Samples[0]]["3lonZ_FFF_{}_{}".format(namereg,namevar)])
            HistsFake[nameyear][Samples[0]]["3loffZhigh_LLF_{}_{}".format(namereg,namevar)].Add(HistsFake[nameyear][Samples[0]]["3loffZhigh_LFF_{}_{}".format(namereg,namevar)],-1)
            HistsFake[nameyear][Samples[0]]["3loffZhigh_LLF_{}_{}".format(namereg,namevar)].Add(HistsFake[nameyear][Samples[0]]["3loffZhigh_FFF_{}_{}".format(namereg,namevar)])
            HistsFake[nameyear][Samples[0]]["3loffZlow_LLF_{}_{}".format(namereg,namevar)].Add(HistsFake[nameyear][Samples[0]]["3loffZlow_LFF_{}_{}".format(namereg,namevar)],-1)
            HistsFake[nameyear][Samples[0]]["3loffZlow_LLF_{}_{}".format(namereg,namevar)].Add(HistsFake[nameyear][Samples[0]]["3loffZlow_FFF_{}_{}".format(namereg,namevar)])

for f in range(1,len(Samples)):
    for numyear, nameyear in enumerate(year):
        for numch, namech in enumerate(channels):
            for numreg, namereg in enumerate(regions):
                for numvar, namevar in enumerate(variables):
                    hist_key = "{}_{}_{}".format(namech,namereg,namevar)
                    if f>0 and namech in channelsSys:
                        glistup = []
                        glistdown = []
                        for numsys2, namesys2 in enumerate(sys):
                            hup = HistsSysUp[nameyear][Samples[f]][hist_key][namesys2].Clone()
                            hdown = HistsSysDown[nameyear][Samples[f]][hist_key][namesys2].Clone()
                            if hup.Integral()>0 or hdown.Integral()>0:
                                for b in range(hup.GetNbinsX()):
                                    cv = Hists_copy[nameyear][Samples[f]][hist_key].GetBinContent(b+1)
                                    rb = 0
                                    if cv>0:
                                        rb = 100/cv
                                    hup.SetBinContent(b+1, 0 + abs(max((HistsSysUp[nameyear][Samples[f]][hist_key][namesys2].GetBinContent(b+1)-cv)*rb, (HistsSysDown[nameyear][Samples[f]][hist_key][namesys2].GetBinContent(b+1)-cv)*rb,0)))
                                    hdown.SetBinContent(b+1, 0 - abs(min((HistsSysUp[nameyear][Samples[f]][hist_key][namesys2].GetBinContent(b+1)-cv)*rb, (HistsSysDown[nameyear][Samples[f]][hist_key][namesys2].GetBinContent(b+1)-cv)*rb,0)))
                            glistup.append(hup)
                            glistdown.append(hdown)
                        compareError(glistup,glistdown, sys, namech, namereg, nameyear,namevar,variablesName[numvar], 'ExpNonJets_'+Samples[f]+'_')

for f in range(1,len(Samples)):
    for numyear, nameyear in enumerate(year):
        for numch, namech in enumerate(channels):
            for numreg, namereg in enumerate(regions):
                for numvar, namevar in enumerate(variables):
                    hist_key = "{}_{}_{}".format(namech,namereg,namevar)
                    if f>0 and namech in channelsSys:
                        glistup = []
                        glistdown = []
                        for numsys2, namesys2 in enumerate(jetSys):
                            hup = HistsSysJecUp[nameyear][Samples[f]][hist_key][namesys2].Clone()
                            hdown = HistsSysJecDown[nameyear][Samples[f]][hist_key][namesys2].Clone()
                            if hup.Integral()>0 or hdown.Integral()>0:
                                for b in range(hup.GetNbinsX()):
                                    cv = Hists_copy[nameyear][Samples[f]][hist_key].GetBinContent(b+1)
                                    rb = 0
                                    if cv>0:
                                        rb = 100/cv
                                    hup.SetBinContent(b+1, 0 + abs(max((HistsSysJecUp[nameyear][Samples[f]][hist_key][namesys2].GetBinContent(b+1)-cv)*rb, (HistsSysJecDown[nameyear][Samples[f]][hist_key][namesys2].GetBinContent(b+1)-cv)*rb,0)))
                                    hdown.SetBinContent(b+1, 0 - abs(min((HistsSysJecUp[nameyear][Samples[f]][hist_key][namesys2].GetBinContent(b+1)-cv)*rb, (HistsSysJecDown[nameyear][Samples[f]][hist_key][namesys2].GetBinContent(b+1)-cv)*rb,0)))
                            glistup.append(hup)
                            glistdown.append(hdown)
                        compareError(glistup,glistdown, jetSys, namech, namereg, nameyear,namevar,variablesName[numvar], 'ExpJets_'+Samples[f]+'_')

for numyear, nameyear in enumerate(year):
    for numch, namech in enumerate(channels):
        for numreg, namereg in enumerate(regions):
            for numvar, namevar in enumerate(variables):
                hist_key = "{}_{}_{}".format(namech,namereg,namevar)
                for f in range(2,len(Samples)):
                    if 'FCNC' in Samples[f]:
                        continue
                    Hists_copy[nameyear][Samples[1]][hist_key].Add(Hists_copy[nameyear][Samples[f]][hist_key])
                if namech in channelsSys:
                    for numsys2, namesys2 in enumerate(sys):
                        for f in range(2,len(Samples)):
                            if 'FCNC' in Samples[f]:
                                continue
                            HistsSysUp[nameyear][Samples[1]][hist_key][namesys2].Add(HistsSysUp[nameyear][Samples[f]][hist_key][namesys2])
                            HistsSysDown[nameyear][Samples[1]][hist_key][namesys2].Add(HistsSysDown[nameyear][Samples[f]][hist_key][namesys2])
                    for numsys2, namesys2 in enumerate(jetSys):
                        for f in range(2,len(Samples)):
                            if 'FCNC' in Samples[f]:
                                continue
                            HistsSysJecUp[nameyear][Samples[1]][hist_key][namesys2].Add(HistsSysJecUp[nameyear][Samples[f]][hist_key][namesys2])
                            HistsSysJecDown[nameyear][Samples[1]][hist_key][namesys2].Add(HistsSysJecDown[nameyear][Samples[f]][hist_key][namesys2])


for numyear, nameyear in enumerate(year):
    for numch, namech in enumerate(channels):
        for numreg, namereg in enumerate(regions):
            for numvar, namevar in enumerate(variables):
                hist_key = "{}_{}_{}".format(namech,namereg,namevar)
                HH=[]
                HHsignal=[]
                SN=[]
                SNsignal=[]
                for f in range(len(Samples)):
                    if 'FCNC' in Samples[f]:
                        text = 'EFTrwgt4_cpQM_1.0_cpt_1.0_ctA_1.0_ctZ_0.5_ctG_0.1_cQlM_1.0_cQe_1.0_ctl_1.0_cte_1.0_ctlS_1.0_ctlT_0.05_ctp_1.0'
                        Hists[nameyear][Samples[f]][hist_key].SetLineColor(1)
                        HHsignal.append(Hists[nameyear][Samples[f]][hist_key])
                        SNsignal.append(SamplesName[f])
                    else:
                        HH.append(Hists[nameyear][Samples[f]][hist_key])
                        SN.append(SamplesName[f])
                if namech in fakeMap:
                    HistsFake[nameyear][Samples[0]]["{}_{}_{}".format(fakeMap[namech],namereg,namevar)].SetFillColor(ROOT.kYellow+2)
                    HistsFake[nameyear][Samples[0]]["{}_{}_{}".format(fakeMap[namech],namereg,namevar)].SetLineColor(ROOT.kYellow+2)
                    HH.append(HistsFake[nameyear][Samples[0]]["{}_{}_{}".format(fakeMap[namech],namereg,namevar)])
                    SN.append("Fake")
                if namech=="2lss":
                    Hists[nameyear][Samples[0]]["2los_Weighted_{}_{}".format(namereg,namevar)].SetFillColor(ROOT.TColor.GetColor("#92dadd"))
                    Hists[nameyear][Samples[0]]["2los_Weighted_{}_{}".format(namereg,namevar)].SetLineColor(ROOT.TColor.GetColor("#92dadd"))
                   # HH.append(Hists[numyear][0][channels.index("2los_Weighted")][numreg][numvar])
                   # SN.append("ChargeFlip")
                    index = SN.index("DY")
                    HH[index]=Hists[nameyear][Samples[0]]["2los_Weighted_{}_{}".format(namereg,namevar)]
                    SN[index]="ChargeFlip"
                #Find errors
                nbins =  Hists_copy[nameyear][Samples[1]][hist_key].GetNbinsX()
                binwidth= array.array( 'f' )
                x_vals = array.array( 'f' )
                y_vals = array.array( 'f' )
                err_up = array.array( 'f' )
                err_down = array.array( 'f' )
                total = Hists_copy[nameyear][Samples[1]][hist_key]
                for b in range(0, nbins):
                    total_up_sq =  pow(total.GetBinError(b+1), 2) + 1.6*1.6 + 1
                    total_down_sq = pow(total.GetBinError(b+1), 2) + 1.6*1.6 + 1
                
                    x_center = total.GetBinCenter(b+1)
                    y_value = total.GetBinContent(b+1)
                    binwidth.append(total.GetBinWidth(b+1)/2)
                    cv = y_value
                    if namech in channelsSys:
                        for numsys2, namesys2 in enumerate(sys):                
                            h_up = HistsSysUp[nameyear][Samples[1]][hist_key][namesys2]
                            h_down = HistsSysDown[nameyear][Samples[1]][hist_key][namesys2]
                            total_up_sq += pow(abs(max((h_up.GetBinContent(b+1)-cv), (h_down.GetBinContent(b+1)-cv),0)), 2)
                            total_down_sq += pow(abs(min((h_up.GetBinContent(b+1)-cv), (h_down.GetBinContent(b+1)-cv),0)), 2)
                        for numsys2, namesys2 in enumerate(jetSys):
                            h_up = HistsSysJecUp[nameyear][Samples[1]][hist_key][namesys2]
                            h_down = HistsSysJecDown[nameyear][Samples[1]][hist_key][namesys2]
                            total_up_sq += pow(abs(max((h_up.GetBinContent(b+1)-cv), (h_down.GetBinContent(b+1)-cv),0)), 2)
                            total_down_sq += pow(abs(min((h_up.GetBinContent(b+1)-cv), (h_down.GetBinContent(b+1)-cv),0)), 2)
                    for f in range(len(Samples)):
                        total_up_sq += pow(Hists[nameyear][Samples[f]][hist_key].GetBinContent(b+1) * SamplesNormErr[f], 2)
                        total_down_sq += pow(Hists[nameyear][Samples[f]][hist_key].GetBinContent(b+1) * SamplesNormErr[f], 2)
                    if namech=="2lss":
                        total_up_sq += pow(HH[index].GetBinContent(b+1)*0.3, 2)
                        total_down_sq += pow(HH[index].GetBinContent(b+1)*0.3, 2)
                
                    x_vals.append(x_center)
                    y_vals.append(1.0)
                    if cv>0:
                        err_up.append(pow(total_up_sq, 0.5)/cv)
                        err_down.append(pow(total_down_sq, 0.5)/cv)
                    else:
                        err_up.append(0)
                        err_down.append(0)
                
                # Create the TGraphAsymmErrors
                gErr = ROOT.TGraphAsymmErrors(len(x_vals))
                for i in range(len(x_vals)):
                    gErr.SetPoint(i, x_vals[i], y_vals[i])
                    gErr.SetPointError(i, binwidth[i], binwidth[i], err_down[i], err_up[i])
                stackPlots(HH, HHsignal, SN, SNsignal, gErr, namech, namereg, nameyear,namevar,variablesName[numvar])
    os.system('tar -cvf '+nameyear+'.tar ' +nameyear)

os.system('tar -cvf sys.tar sys')
