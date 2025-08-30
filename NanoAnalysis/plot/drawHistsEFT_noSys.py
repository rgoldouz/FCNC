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
from my_utils import *

#year=['2018']
channels=["2lssEE", "2lssEM","2lssMM", "2losEE_Weighted", "2losEM_Weighted", "2los_EpEm_CR", "2los_MUpMUm_CR", "2los_EpmMUmp_CR", "3lonZ", "3loffZhigh", "3loffZlow","4l_CR"]
channelsFake=["2lssEE_LF", "2lssEE_FF", "2lssEM_LF", "2lssEM_FF","2lssMM_LF", "2lssMM_FF", "3lonZ_LLF", "3lonZ_LFF","3lonZ_FFF","3loffZhigh_LLF", "3loffZhigh_LFF","3loffZhigh_FFF", "3loffZlow_LLF", "3loffZlow_LFF","3loffZlow_FFF"]
#variables=["llM"]

Hists = {}
HistsCFrate = {}
HistsFake = {}

for nameyear in year:
    Hists[nameyear] = {}
    HistsCFrate[nameyear] = {}
    for f, sample in enumerate(Samples):
        sample_key = sample
        Hists[nameyear][sample_key] = {}
        file = ROOT.TFile.Open(HistAddress + nameyear + '_' + sample)
        HistsCFrate[nameyear][sample_key] = file.Get('mll_SS_Zwindow_0jet')
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
                    if 'MVA' in var:
                        for key in binsDic:
                            if key in ch:
                                bins = binsDic[key]
                                h = h.Rebin(len(bins) - 1, "", bins)
                                break
                    h.SetFillColor(colors[f])
                    h.SetLineColor(colors[f])
                    HistsFake[nameyear][sample_key][hist_key] = h.Clone()
for nameyear in year:
    for reg in regions:
        for var in variables:
            hist_key = "2lss_{}_{}".format(reg,var)
            hist_key1 = "2lssEE_{}_{}".format(reg,var)
            hist_key2 = "2lssEM_{}_{}".format(reg,var)
            hist_key3 = "2lssMM_{}_{}".format(reg,var)
            mergeChReg_histograms(Hists, nameyear, new_key=hist_key, merge_keys=[hist_key1,hist_key2,hist_key3])

            hist_key = "2lss_LF_{}_{}".format(reg,var)
            hist_key1 = "2lssEE_LF_{}_{}".format(reg,var)
            hist_key2 = "2lssEM_LF_{}_{}".format(reg,var)
            hist_key3 = "2lssMM_LF_{}_{}".format(reg,var)
            mergeChReg_histograms(HistsFake, nameyear, new_key=hist_key, merge_keys=[hist_key1,hist_key2,hist_key3])
            hist_key = "2lss_FF_{}_{}".format(reg,var)
            hist_key1 = "2lssEE_FF_{}_{}".format(reg,var)
            hist_key2 = "2lssEM_FF_{}_{}".format(reg,var)
            hist_key3 = "2lssMM_FF_{}_{}".format(reg,var)
            mergeChReg_histograms(HistsFake, nameyear, new_key=hist_key, merge_keys=[hist_key1,hist_key2,hist_key3])

            hist_key = "2los_Weighted_{}_{}".format(reg,var)
            hist_key1 = "2losEE_Weighted_{}_{}".format(reg,var)
            hist_key2 = "2losEM_Weighted_{}_{}".format(reg,var)
            mergeChReg_histograms(Hists, nameyear, new_key=hist_key, merge_keys=[hist_key1,hist_key2])

channels.append("2lss")           
channels.append("2los_Weighted")
channelsFake.append("2lss_LF")
channelsFake.append("2lss_FF")

mergeYear_histograms(Hists, 'Run2', year)
mergeYear_histograms(HistsFake, 'Run2', year)
year.append('Run2')

mergeSample_histograms(HistsFake, new_sample="MCsum", samples_to_merge=['Triboson.root', 'Diboson.root', 'ttbar.root', 'ST.root','DY.root', 'Conv.root','TTX.root','WJets.root'])

drawFakeRegions=False
if drawFakeRegions:
    for numyear, nameyear in enumerate(year):
        for numch, namech in enumerate(channelsFake):
            for numreg, namereg in enumerate(regions):
                for numvar, namevar in enumerate(variables):
                    hist_key = "{}_{}_{}".format(namech,namereg,namevar)
                    HH=[]
                    HHsignal=[]
                    SN=[]
                    SNsignal=[]
                    for f in range(len(Samples)):
                        if 'FCNC' in Samples[f]:
                            HistsFake[nameyear][Samples[f]][hist_key].SetLineColor(1)
                            HHsignal.append(HistsFake[nameyear][Samples[f]][hist_key])
                            SNsignal.append(SamplesName[f])
                        else:
                            HH.append(HistsFake[nameyear][Samples[f]][hist_key])
                            SN.append(SamplesName[f])
                    stackPlotsNoSys(HH, HHsignal, SN, SNsignal,'noSysPlots', namech, namereg, nameyear,namevar,variablesName[numvar])


for numyear, nameyear in enumerate(year):
    for numreg, namereg in enumerate(regions):
        for numvar, namevar in enumerate(variables):
            HistsFake[nameyear][Samples[0]]["2lss_LF_{}_{}".format(namereg,namevar)].Add(HistsFake[nameyear][Samples[0]]["2lss_FF_{}_{}".format(namereg,namevar)],-1)
            HistsFake[nameyear][Samples[0]]["2lss_LF_{}_{}".format(namereg,namevar)].Add(HistsFake[nameyear]["MCsum"]["2lss_LF_{}_{}".format(namereg,namevar)],-1)

            HistsFake[nameyear][Samples[0]]["2lssEE_LF_{}_{}".format(namereg,namevar)].Add(HistsFake[nameyear][Samples[0]]["2lssEE_FF_{}_{}".format(namereg,namevar)],-1)
            HistsFake[nameyear][Samples[0]]["2lssEE_LF_{}_{}".format(namereg,namevar)].Add(HistsFake[nameyear]["MCsum"]["2lssEE_LF_{}_{}".format(namereg,namevar)],-1)

            HistsFake[nameyear][Samples[0]]["2lssEM_LF_{}_{}".format(namereg,namevar)].Add(HistsFake[nameyear][Samples[0]]["2lssEM_FF_{}_{}".format(namereg,namevar)],-1)
            HistsFake[nameyear][Samples[0]]["2lssEM_LF_{}_{}".format(namereg,namevar)].Add(HistsFake[nameyear]["MCsum"]["2lssEM_LF_{}_{}".format(namereg,namevar)],-1)

            HistsFake[nameyear][Samples[0]]["2lssMM_LF_{}_{}".format(namereg,namevar)].Add(HistsFake[nameyear][Samples[0]]["2lssMM_FF_{}_{}".format(namereg,namevar)],-1)
            HistsFake[nameyear][Samples[0]]["2lssMM_LF_{}_{}".format(namereg,namevar)].Add(HistsFake[nameyear]["MCsum"]["2lssMM_LF_{}_{}".format(namereg,namevar)],-1)

            HistsFake[nameyear][Samples[0]]["3lonZ_LLF_{}_{}".format(namereg,namevar)].Add(HistsFake[nameyear][Samples[0]]["3lonZ_LFF_{}_{}".format(namereg,namevar)],-1)
            HistsFake[nameyear][Samples[0]]["3lonZ_LLF_{}_{}".format(namereg,namevar)].Add(HistsFake[nameyear]["MCsum"]["3lonZ_LLF_{}_{}".format(namereg,namevar)],-1)
            HistsFake[nameyear][Samples[0]]["3lonZ_LLF_{}_{}".format(namereg,namevar)].Add(HistsFake[nameyear][Samples[0]]["3lonZ_FFF_{}_{}".format(namereg,namevar)])

            HistsFake[nameyear][Samples[0]]["3loffZhigh_LLF_{}_{}".format(namereg,namevar)].Add(HistsFake[nameyear][Samples[0]]["3loffZhigh_LFF_{}_{}".format(namereg,namevar)],-1)
            HistsFake[nameyear][Samples[0]]["3loffZhigh_LLF_{}_{}".format(namereg,namevar)].Add(HistsFake[nameyear]["MCsum"]["3loffZhigh_LLF_{}_{}".format(namereg,namevar)],-1)
            HistsFake[nameyear][Samples[0]]["3loffZhigh_LLF_{}_{}".format(namereg,namevar)].Add(HistsFake[nameyear][Samples[0]]["3loffZhigh_FFF_{}_{}".format(namereg,namevar)])
            HistsFake[nameyear][Samples[0]]["3loffZlow_LLF_{}_{}".format(namereg,namevar)].Add(HistsFake[nameyear][Samples[0]]["3loffZlow_LFF_{}_{}".format(namereg,namevar)],-1)
            HistsFake[nameyear][Samples[0]]["3loffZlow_LLF_{}_{}".format(namereg,namevar)].Add(HistsFake[nameyear]["MCsum"]["3loffZlow_LLF_{}_{}".format(namereg,namevar)],-1)
            HistsFake[nameyear][Samples[0]]["3loffZlow_LLF_{}_{}".format(namereg,namevar)].Add(HistsFake[nameyear][Samples[0]]["3loffZlow_FFF_{}_{}".format(namereg,namevar)])



fakeMap={
"2lss":"2lss_LF",
"2lssEE":"2lssEE_LF",
"2lssEM":"2lssEM_LF",
"2lssMM":"2lssMM_LF",
"3lonZ":"3lonZ_LLF", 
"3loffZhigh":"3loffZhigh_LLF", 
"3loffZlow":"3loffZlow_LLF"
}

chargeFlipMap={"2lss":"2los_Weighted", "2lssEE":"2losEE_Weighted", "2lssEM":"2losEM_Weighted"}
for numyear, nameyear in enumerate(year):
    if nameyear=='Run2':
        continue
    HH=[]
    HHsignal=[]
    SN=[]
    SNsignal=[]
    for f in range(len(Samples)):
        if 'FCNC' in Samples[f]:
            HistsCFrate[nameyear][Samples[f]].SetLineColor(1)
            HHsignal.append(HistsCFrate[nameyear][Samples[f]])
            SNsignal.append(SamplesName[f])
        else:
            HH.append(HistsCFrate[nameyear][Samples[f]])  
            SN.append(SamplesName[f])
#    stackPlots(HH, HHsignal, SN, SNsignal, 'ss', '0b0j', nameyear,'mll',"M(ll) [z window]")        


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
                if "2lss" in namech and 'MM' not in namech:
                    Hists[nameyear][Samples[0]]["{}_{}_{}".format(chargeFlipMap[namech],namereg,namevar)].SetFillColor(ROOT.TColor.GetColor("#92dadd"))
                    Hists[nameyear][Samples[0]]["{}_{}_{}".format(chargeFlipMap[namech],namereg,namevar)].SetLineColor(ROOT.TColor.GetColor("#92dadd"))
                    HH.append(Hists[nameyear][Samples[0]]["{}_{}_{}".format(chargeFlipMap[namech],namereg,namevar)])
                    SN.append("ChargeFlip")
                    #index = SN.index("DY")
                    #if 'Run2'==nameyear:
                    #    HH[index].Scale((HistsCFrate[year[0]][Samples[0]].Integral()+HistsCFrate[year[1]][Samples[0]].Integral()+HistsCFrate[year[2]][Samples[0]].Integral()+HistsCFrate[year[3]][Samples[0]].Integral())/(HistsCFrate[year[0]]['DY.root'].Integral()+HistsCFrate[year[1]]['DY.root'].Integral()+HistsCFrate[year[2]]['DY.root'].Integral()+HistsCFrate[year[3]]['DY.root'].Integral()))
                    #else:
                    #    HH[index].Scale(HistsCFrate[nameyear][Samples[0]].Integral()/HistsCFrate[nameyear]['DY.root'].Integral())
                   # SN[index]="ChargeFlip"
                stackPlotsNoSys(HH, HHsignal, SN, SNsignal, 'noSysPlots',namech, namereg, nameyear,namevar,variablesName[numvar])
os.system('tar -cvf noSysPlots.tar noSysPlots')

le = '\\documentclass{article}' + "\n"
le += '\\usepackage{rotating}' + "\n"
le += '\\usepackage{rotating}' + "\n"
le += '\\begin{document}' + "\n"

print le
#    for numch, namech in enumerate(channels):
#        cutFlowTable(Hists, SamplesNameLatex, regionsName, numch, numyear, nameyear + ' ' + namech, 6 )
print '\\end{document}' + "\n"


