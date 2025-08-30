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

year=['2016preVFP', '2016postVFP', '2017','2018']
#year=['2018']
regions=["0b","1bLj", "1bHj","G1b"]
regionsName=["0b","1bxj", "1b$>$xj", "$>$1Bjet"]
channels=["2lssEE", "2lssEM","2lssMM", "2losEE_Weighted", "2losEM_Weighted", "2los_EpEm_CR", "2los_MUpMUm_CR", "2los_EpmMUmp_CR", "3lonZ", "3loffZhigh", "3loffZlow","4l_CR"]
channelsFake=["2lssEE_LF", "2lssEE_FF", "2lssEM_LF", "2lssEM_FF","2lssMM_LF", "2lssMM_FF", "3lonZ_LLF", "3lonZ_LFF","3lonZ_FFF","3loffZhigh_LLF", "3loffZhigh_LFF","3loffZhigh_FFF", "3loffZlow_LLF", "3loffZlow_LFF","3loffZlow_FFF"]
variables=["lep1Pt","lep1Eta","lep1Phi","lep2Pt","lep2Eta","lep2Phi","llM","llPt","llDr","llDphi","jet1Pt","jet1Eta","jet1Phi","njet","nbjet","Met","MetPhi","nVtx","llMZw",
"lep3Pt","lep3Eta", "bJetPt", "bJetEta", "tH_topMass", "tH_HMass","tH_WtopMass", "tH_W1HMass","tH_W2HMass", "tH_HPt", "tH_HEta","tH_topPt", "tH_topEta", "tH_drWtopB",  "tH_drW1HW2H", "tZ_topMass", "tZ_ZMass", "tZ_WtopMass","tZ_ZPt","tZ_ZEta","tZ_topPt", "tZ_topEta", "MVATU","MVATC"]
#variables=["lep1Pt","llM"]
variablesName=["p_{T}(leading lepton)","#eta(leading lepton)","#Phi(leading lepton)","p_{T}(sub-leading lepton)","#eta(sub-leading lepton)","#Phi(sub-leading lepton)","M(ll)","p_{T}(ll)","#Delta R(ll)","#Delta #Phi(ll)","p_{T}(leading jet)","#eta(leading jet)","#Phi(leading jet)","Number of jets","Number of b-tagged jets","MET","#Phi(MET)","Number of vertices", "M(ll) [z window]","lep3Pt","lep3Eta", "bJetPt", "bJetEta", "tH_topMass", "tH_HMass","tH_WtopMass", "tH_W1HMass","tH_W2HMass", "tH_HPt", "tH_HEta","tH_topPt", "tH_topEta", "tH_drWtopB",  "tH_drW1HW2H", "tZ_topMass", "tZ_ZMass", "tZ_WtopMass","tZ_ZPt","tZ_ZEta","tZ_topPt", "tZ_topEta","Likelihood ratio TU", "Likelihood ratio TC"]

HistAddress = '/users/rgoldouz/FCNC/NanoAnalysis/hists/'

Samples = ['data.root','Triboson.root', 'Diboson.root', 'ttbar.root', 'ST.root','DY.root', 'Conv.root','TTW.root','TTH.root','TTZ.root','Else.root','FCNCTUProduction.root','FCNCTUDecay.root']
SamplesNormErr = [0, 0.1, 0.06, 0.05, 0.1, 0.05, 0.05, 0.15, 0.15, 0.15, 0.15,0,0]
SamplesName = ['Data','Triboson', 'Diboson', 't#bar{t}', 'Single top','DY', 'Conversions','t#bar{t}W','t#bar{t}H','t#bar{t}Z','Wj+tWZ+4t','FCNC-Production','FCNC-Decay']#
channelsSys=["2lss","2lssEE", "2lssEM","2lssMM", "3lonZ", "3loffZhigh"]
sys = ["eleRecoIdIso","muRecoIdIso","triggerSF","pu","prefiring","bcTagSfCorr","LTagSfCorr","bcTagSfUnCorr","LTagSfUnCorr","JetPuID"]
jetSys=["Jes","Jer"]
ThSys=["PDF","Renormalization","Factorization", "ISR", "FSR"]
colors = [
    ROOT.kBlack,
    ROOT.TColor.GetColor("#3f90da"),  # Blue
    ROOT.TColor.GetColor("#ffa90e"),  # Orange
    ROOT.TColor.GetColor("#bd1f01"),  # Red
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

fakeMap={
"2lssEE":"2lssEE_LF",
"2lssEM":"2lssEM_LF",
"2lssMM":"2lssMM_LF",
"2lss":"2lss_LF",
"3lonZ":"3lonZ_LLF",
"3loffZhigh":"3loffZhigh_LLF",
"3loffZlow":"3loffZlow_LLF"
}
chargeFlipMap={"2lss":"2los_Weighted", "2lssEE":"2losEE_Weighted", "2lssEM":"2losEM_Weighted"}
bins = array.array( 'd',[0.01,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,2,50] )
binsDic = {
'2l':array.array( 'd',[0.01,0.3,0.5,0.7,0.9,1.1,1.3,1.5,2,4,50] ),
'3lonZ':array.array( 'd',[0.01,0.2,0.4,0.8,1.6,3.2,8.4,16.8,50.0] ),
'3loffZ':array.array( 'd',[0.01,0.1,0.4,1.0,5.0,20,50.0] ),
}

wc1 = ROOT.WCPoint("EFTrwgt4_cpQM_1.0_cpt_1.0_ctA_1.0_ctZ_0.5_ctG_0.1_cQlM_1.0_cQe_1.0_ctl_1.0_cte_1.0_ctlS_1.0_ctlT_0.05_ctp_1.0")

def mergeYear_histograms(H, new_key, merge_keys, merge_axis="channel"):
    H[new_key] = {}

    # Loop over all samples
    all_samples = set()
    for k in merge_keys:
        all_samples.update(H.get(k, {}).keys())

    for sample in all_samples:
        H[new_key][sample] = {}
        all_hist_keys = set()

        # Get all hist_keys across the merge_keys
        for k in merge_keys:
            all_hist_keys.update(H.get(k, {}).get(sample, {}).keys())

        for hist_key in all_hist_keys:
            merged_hist = None
            for k in merge_keys:
                h = H.get(k, {}).get(sample, {}).get(hist_key)
                if h:
                    if merged_hist is None:
                        merged_hist = h.Clone()
                        merged_hist.SetDirectory(0)
                        merged_hist.SetName(new_key+sample+hist_key)
                    else:
                        merged_hist.Add(h)
            if merged_hist:
                H[new_key][sample][hist_key] = merged_hist

def mergeSample_histograms(H, new_sample, samples_to_merge):
    for year in H:
        H[year][new_sample] = {}
        all_hist_keys = set()

        # Collect all hist_keys from the samples to merge
        all_hist_keys.update(H[year].get(samples_to_merge[0], {}).keys())

        for hist_key in all_hist_keys:
            merged_hist = None
            for sample in samples_to_merge:
                h = H[year].get(sample, {}).get(hist_key)
                if h:
                    if merged_hist is None:
                        merged_hist = h.Clone()
                        merged_hist.SetDirectory(0)
                        merged_hist.SetName(year+new_sample+hist_key)
                    else:
                        merged_hist.Add(h)
            if merged_hist:
                H[year][new_sample][hist_key] = merged_hist

def mergeSampleSys_histograms(H, new_sample, samples_to_merge, sys):
    for year in H:
        if new_sample not in H[year]:
            H[year][new_sample] = {}  # Initialize new_sample dict

        all_hist_keys = set()
        # Collect all histogram keys from the samples to merge
        all_hist_keys.update(H[year].get(samples_to_merge[0], {}).keys())

        for hist_key in all_hist_keys:
            merged_hist = None
            for sample in samples_to_merge:
                h = H[year].get(sample, {}).get(hist_key, {}).get(sys)
                if h:
                    if merged_hist is None:
                        merged_hist = h.Clone()
                        merged_hist.SetDirectory(0)
                        merged_hist.SetName(year+new_sample+hist_key+sys)
                    else:
                        merged_hist.Add(h)

            if merged_hist:
                # Ensure nested structure exists before assignment
                if hist_key not in H[year][new_sample]:
                    H[year][new_sample][hist_key] = {}
                H[year][new_sample][hist_key][sys] = merged_hist


def mergeYear_histograms_sys(H, new_key, merge_keys, merge_axis="channel"):
    H[new_key] = {}

    # Collect all unique samples
    all_samples = set()
    for k in merge_keys:
        all_samples.update(H.get(k, {}).keys())

    for sample in all_samples:
        H[new_key][sample] = {}
        all_hist_keys = set()

        # Collect all unique hist_keys for this sample
        for k in merge_keys:
            all_hist_keys.update(H.get(k, {}).get(sample, {}).keys())

        for hist_key in all_hist_keys:
            H[new_key][sample][hist_key] = {}
            all_sys_keys = set()

            # Collect all unique systematics keys for this hist_key
            for k in merge_keys:
                all_sys_keys.update(H.get(k, {}).get(sample, {}).get(hist_key, {}).keys())

            for sys in all_sys_keys:
                merged_hist = None
                for k in merge_keys:
                    h = H.get(k, {}).get(sample, {}).get(hist_key, {}).get(sys)
                    if h:
                        if merged_hist is None:
                            merged_hist = h.Clone()
                            merged_hist.SetDirectory(0)
                            merged_hist.SetName(new_key+sample+hist_key+sys)
                        else:
                            merged_hist.Add(h)
                if merged_hist:
                    H[new_key][sample][hist_key][sys] = merged_hist

def mergeChReg_histograms(H, year, new_key, merge_keys):
    # Loop over all samples
    all_samples = set()
    all_samples.update(H.get(year, {}).keys())

    for sample in all_samples:
        merged_hist = None
        for hist_key in merge_keys:
            h = H.get(year, {}).get(sample, {}).get(hist_key)
            if h:
                if merged_hist is None:
                    merged_hist = h.Clone()
                    merged_hist.SetDirectory(0)
                    merged_hist.SetName(year+sample+new_key)
                else:
                    merged_hist.Add(h)
        if merged_hist:
#            print year+sample+new_key
            H[year][sample][new_key] = merged_hist

def mergeChRegSys_histograms(H, year, new_key, merge_keys,sys):
    # Loop over all samples
    all_samples = set()
    all_samples.update(H.get(year, {}).keys())

    for sample in all_samples:
        H.setdefault(year, {}).setdefault(sample, {}).setdefault(new_key, {}) 
#        H[year][sample][new_key]={}
        merged_hist = None
#        print year+sample+new_key+sys
        for hist_key in merge_keys:
            h = H.get(year, {}).get(sample, {}).get(hist_key,{}).get(sys)
            if h:
                if merged_hist is None:
                    merged_hist = h.Clone()
                    merged_hist.SetDirectory(0)
                    merged_hist.SetName(year+sample+new_key+sys)
                else:
                    merged_hist.Add(h)
        if merged_hist:
            H[year][sample][new_key][sys] = merged_hist

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
            print  'bin'+str(b+1)+":"+H.GetName()+"Bin content is NaN"
        if math.isinf(content):
            print  H.GetName()+"Bin content is inf"
        hpx.SetBinContent(b+1, H.GetBinContent(b+1,wc))
        hpx.SetBinError(b+1, H.GetBinError(b+1))
    hpx.SetBinContent(hpx.GetXaxis().GetNbins(), hpx.GetBinContent(hpx.GetXaxis().GetNbins()) + hpx.GetBinContent(hpx.GetXaxis().GetNbins()+1))
    hpx.SetBinError(hpx.GetXaxis().GetNbins(), (H.GetBinError(hpx.GetXaxis().GetNbins())**2 + H.GetBinError(hpx.GetXaxis().GetNbins()+1)**2)**0.5)
    hpx.SetBinContent(hpx.GetXaxis().GetNbins()+1,0)
    hpx.SetBinError(hpx.GetXaxis().GetNbins()+1,0)
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
#        h.SetLineColor(c[n]) 
        h.SetBinContent(h.GetXaxis().GetNbins(), h.GetBinContent(h.GetXaxis().GetNbins()) + h.GetBinContent(h.GetXaxis().GetNbins()+1))
        hist[s] = h
    for key, h in hist.items():
        h.SetBinContent(h.GetXaxis().GetNbins()+1,0)
        h.SetBinError(h.GetXaxis().GetNbins()+1,0)

    return hist

def EFTtoNormalNoWC(H):
    nbins = H.GetNbinsX()
    bin_edges = [H.GetBinLowEdge(i + 1) for i in range(nbins)]
    bin_edges.append(H.GetXaxis().GetBinUpEdge(nbins))
    bin_array = array.array('d', bin_edges)
    hpx = ROOT.TH1F(H.GetName(), H.GetName(), nbins, bin_array)
    r=1
    for b in range(hpx.GetNbinsX()+1):
        content = H.GetBinContentNoWC(b+1)
#        if math.isnan(content):
#            print  H.GetName()+"Bin content is NaN"
#        if math.isinf(content):
#            print  H.GetName()+"Bin content is inf"
        hpx.SetBinContent(b+1, H.GetBinContentNoWC(b+1))
        hpx.SetBinError(b+1, H.GetBinError(b+1))
    hpx.SetBinContent(hpx.GetXaxis().GetNbins(), hpx.GetBinContent(hpx.GetXaxis().GetNbins()) + hpx.GetBinContent(hpx.GetXaxis().GetNbins()+1))
    hpx.SetBinError(hpx.GetXaxis().GetNbins(), (H.GetBinError(hpx.GetXaxis().GetNbins())**2 + H.GetBinError(hpx.GetXaxis().GetNbins()+1)**2)**0.5)
    hpx.SetBinContent(hpx.GetXaxis().GetNbins()+1,0)
    hpx.SetBinError(hpx.GetXaxis().GetNbins()+1,0)
    hpx.SetLineColor(H.GetLineColor())
    hpx.SetLineStyle(H.GetLineStyle())
#    if hpx.Integral()>0:
#        hpx.Scale(1/hpx.Integral())
    return hpx

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
    if 'MVA' in var:
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
#    print table

def stackPlots(hists, SignalHists, Fnames,FnamesS,errorRatio, folder='folder', ch = "channel", reg = "region", year='2016', var="sample", varname="v"):
    Blinded=False

    if ch=="3lonZ" or ch=="3loffZhigh" or ch=="2lss":
        if reg=="1bLj" or reg== "1bHj":
            Blinded=True
    if not os.path.exists(folder):
       os.makedirs(folder)            
    if not os.path.exists(folder +'/'+year):
       os.makedirs('folder/'+year)
    if not os.path.exists(folder +'/'+year + '/' + ch):
       os.makedirs(folder +'/'+year + '/' + ch)
    if not os.path.exists(folder +'/'+year + '/' + ch +'/'+reg):
       os.makedirs(folder +'/'+year + '/' + ch +'/'+reg)
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
    for num in reversed(range(1, len(hists))):
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
    canvas.Print(folder +'/'+year + '/' + ch +'/'+reg+'/'+var + ".png")
    del canvas
    gc.collect()

def Smoothing(AS, merge):
    x = array.array( 'd' )
    source =  array.array( 'd' )
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

def SmoothingVariableBins(hist, merge, edges):
    widths = np.diff(edges)  # bin widths
    median_width = np.median(widths)
    bandwidth = median_width * merge

    nbins = hist.GetNbinsX()

    # Get bin centers and bin widths
    x_vals = array.array('d', [hist.GetBinCenter(i) for i in range(1, nbins + 1)])
    bin_widths = [hist.GetBinWidth(i) for i in range(1, nbins + 1)]

    # Convert bin contents to densities (per unit x) for fair smoothing
    y_density = array.array('d', [
        hist.GetBinContent(i) / bin_widths[i-1] if bin_widths[i-1] > 0 else 0
        for i in range(1, nbins + 1)
    ])

    # Create graph from densities
    smoother = ROOT.TGraphSmooth("normal")
    graph_in = ROOT.TGraph(nbins, x_vals, y_density)

    # Apply kernel smoothing
    graph_out = smoother.SmoothKern(graph_in, "normal", bandwidth)

    # Create a new histogram with smoothed *contents* (convert back from density)
    smooth_hist = hist.Clone(hist.GetName() + "_smooth")
    for i in range(1, nbins + 1):
        smoothed_density = graph_out.GetY()[i-1]
        smooth_hist.SetBinContent(i, smoothed_density * bin_widths[i-1])

    return smooth_hist

def stackPlotsNoSys(hists, SignalHists, Fnames,FnamesS, folder='noSysPlots',ch = "channel", reg = "region", year='2016', var="sample", varname="v"):
    Blinded=False

    if ch=="3lonZ" or ch=="3loffZhigh" or ch=="2lss":
        if reg=="1bLj" or reg== "1bHj":
            Blinded=True
    if not os.path.exists(folder):
       os.makedirs(folder)
    if not os.path.exists(folder+ '/' +year):
       os.makedirs(folder+ '/'+year)
    if not os.path.exists(folder+ '/'+year + '/' + ch):
       os.makedirs(folder+ '/'+year + '/' + ch)
    if not os.path.exists(folder+ '/'+year + '/' + ch +'/'+reg):
       os.makedirs(folder+ '/'+year + '/' + ch +'/'+reg)
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
    canvas.Print('noSysPlots/'+year + '/' + ch +'/'+reg+'/'+var + ".png")
    del canvas
    gc.collect()
