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
#variables=["lep1Pt","lep1Eta", "jet1Pt","jet1Eta", "njet","nbjet","Met", "MVATU","MVATC"]
#variablesName=["p_{T}(leading lepton)","#eta(leading lepton)", "p_{T}(leading jet)","#eta(leading jet)", "Number of jets","Number of b-tagged jets","MET", "Likelihood ratio TU", "Likelihood ratio TC"]


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
        print sample
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
                        if 'MVA' in var:
                            for key, value in hSys_up.items():
                                hSys_up[key] = value.Rebin(len(bins) - 1, "", bins)
                        HistsSysUp[nameyear][sample_key][hist_key]=hSys_up

                        # Down variation
                        h_down = file.Get("{}_{}_{}__Down".format(ch,reg,var))
                        hSys_down = sysEFTtoNormal(h_down, sys, colors)                            
                        if 'MVA' in var:
                            for key, value in hSys_down.items():
                                hSys_down[key] = value.Rebin(len(bins) - 1, "", bins)
                        HistsSysDown[nameyear][sample_key][hist_key]=hSys_down

                        HistsSysJecUp[nameyear][sample_key][hist_key] = {}
                        HistsSysJecDown[nameyear][sample_key][hist_key] = {}
                        for numsys, namesys in enumerate(jetSys):
                        # Up variation
                            h_up = file.Get("{}_{}_{}_{}__Up".format(ch,reg,var,namesys))
                            h_up.SetBinContent(h_up.GetXaxis().GetNbins(), h_up.GetBinContent(h_up.GetXaxis().GetNbins()) + h_up.GetBinContent(h_up.GetXaxis().GetNbins()+1))
                            if 'MVA' in var:
                                h_up = h_up.Rebin(len(bins) - 1, "", bins)
                            HistsSysJecUp[nameyear][sample_key][hist_key][namesys]=h_up

                        # Down variation
                            h_down = file.Get("{}_{}_{}_{}__Down".format(ch,reg,var,namesys))
                            h_down.SetBinContent(h_down.GetXaxis().GetNbins(), h_down.GetBinContent(h_down.GetXaxis().GetNbins()) + h_down.GetBinContent(h_down.GetXaxis().GetNbins()+1))
                            if 'MVA' in var:
                                h_down = h_down.Rebin(len(bins) - 1, "", bins)
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

for nameyear in year:
    for reg in regions:
        for var in variables:
            hist_key = "2lss_{}_{}".format(reg,var)
            hist_key1 = "2lssEE_{}_{}".format(reg,var)
            hist_key2 = "2lssEM_{}_{}".format(reg,var)
            hist_key3 = "2lssMM_{}_{}".format(reg,var)
            mergeChReg_histograms(Hists, nameyear, new_key=hist_key, merge_keys=[hist_key1,hist_key2,hist_key3])
            mergeChReg_histograms(Hists_copy, nameyear, new_key=hist_key, merge_keys=[hist_key1,hist_key2,hist_key3])
            for numsys2, namesys2 in enumerate(sys):
                mergeChRegSys_histograms(HistsSysUp, nameyear, new_key=hist_key, merge_keys=[hist_key1,hist_key2,hist_key3],sys=namesys2)
                mergeChRegSys_histograms(HistsSysDown, nameyear, new_key=hist_key, merge_keys=[hist_key1,hist_key2,hist_key3],sys=namesys2)
            for numsys, namesys in enumerate(jetSys):
                mergeChRegSys_histograms(HistsSysJecUp, nameyear, new_key=hist_key, merge_keys=[hist_key1,hist_key2,hist_key3],sys=namesys)
                mergeChRegSys_histograms(HistsSysJecDown, nameyear, new_key=hist_key, merge_keys=[hist_key1,hist_key2,hist_key3],sys=namesys)
            hist_key = "2los_Weighted_{}_{}".format(reg,var)
            hist_key1 = "2losEE_Weighted_{}_{}".format(reg,var)
            hist_key2 = "2losEM_Weighted_{}_{}".format(reg,var)
            mergeChReg_histograms(Hists, nameyear, new_key=hist_key, merge_keys=[hist_key1,hist_key2])
            mergeChReg_histograms(Hists_copy, nameyear, new_key=hist_key, merge_keys=[hist_key1,hist_key2])
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

channels.append("2lss")
channels.append("2los_Weighted")
channelsFake.append("2lss_LF")
channelsFake.append("2lss_FF")

mergeYear_histograms(Hists, 'Run2', year)
mergeYear_histograms(Hists_copy, 'Run2', year)
mergeYear_histograms(HistsFake, 'Run2', year)
mergeYear_histograms_sys(HistsSysUp, 'Run2', year)
mergeYear_histograms_sys(HistsSysDown, 'Run2', year)
mergeYear_histograms_sys(HistsSysJecUp, 'Run2', year)
mergeYear_histograms_sys(HistsSysJecDown, 'Run2', year)
year.append('Run2')

mergeSample_histograms(HistsFake, new_sample="MCsum", samples_to_merge=['Triboson.root', 'Diboson.root', 'ttbar.root', 'ST.root','DY.root', 'Conv.root','TTW.root','TTH.root','TTZ.root','Else.root'])

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
#                        compareError(glistup,glistdown, sys, 'sysCompact', namech, namereg, nameyear,namevar,variablesName[numvar], 'ExpNonJets_'+Samples[f]+'_')

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
#                        compareError(glistup,glistdown, jetSys, 'sysCompact', namech, namereg, nameyear,namevar,variablesName[numvar], 'ExpJets_'+Samples[f]+'_')

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
                    SN.append("Non-prompt")
                if "2lss" in namech and 'MM' not in namech:
                    Hists[nameyear][Samples[0]]["{}_{}_{}".format(chargeFlipMap[namech],namereg,namevar)].SetFillColor(ROOT.TColor.GetColor("#228c68"))
                    Hists[nameyear][Samples[0]]["{}_{}_{}".format(chargeFlipMap[namech],namereg,namevar)].SetLineColor(ROOT.TColor.GetColor("#228c68"))
                    HH.append(Hists[nameyear][Samples[0]]["{}_{}_{}".format(chargeFlipMap[namech],namereg,namevar)])
                    SN.append("Charge misID")
                    #Hists[nameyear][Samples[0]]["2los_Weighted_{}_{}".format(namereg,namevar)].SetFillColor(ROOT.TColor.GetColor("#92dadd"))
                    #Hists[nameyear][Samples[0]]["2los_Weighted_{}_{}".format(namereg,namevar)].SetLineColor(ROOT.TColor.GetColor("#92dadd"))
                    #index = SN.index("DY")
                    #HH[index]=Hists[nameyear][Samples[0]]["2los_Weighted_{}_{}".format(namereg,namevar)]
                    #SN[index]="ChargeFlip"
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
                    for f in range(1,len(Samples)):
                        if 'FCNC' in Samples[f]:
                            continue                        
                        total_up_sq += pow(Hists[nameyear][Samples[f]][hist_key].GetBinContent(b+1) * SamplesNormErr[f], 2)
                        total_down_sq += pow(Hists[nameyear][Samples[f]][hist_key].GetBinContent(b+1) * SamplesNormErr[f], 2)
                    if "2lss" in namech and 'MM' not in namech:
                        index = SN.index("Charge misID")
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

                threshold = 0.04 * HH[0].Integral()  # 5% of data histogram
                merged_hist = None
                kept_hists = []
                kept_hists_name = []
                for n,h in enumerate(HH):
                    h.SetName(SN[n])
                    if h.Integral() < threshold:
                        if merged_hist is None:
                            merged_hist = h.Clone("merged_small")
                        else:
                            merged_hist.Add(h)
                    else:
                        kept_hists.append(h)
                # Add the merged histogram to the list if it exists
                if merged_hist:
                    merged_hist.SetName('Others')
                    kept_hists.append(merged_hist)
                kept_hists[1:] = sorted(kept_hists[1:], key=lambda h: h.Integral())    
                for h in kept_hists:
                    kept_hists_name.append(h.GetName())
                stackPlots(kept_hists, HHsignal, kept_hists_name, SNsignal, gErr, 'SysPlots',namech, namereg, nameyear,namevar,variablesName[numvar])

os.system('tar -cvf SysPlots.tar SysPlots')
os.system('tar -cvf sysCompact.tar sysCompact')
