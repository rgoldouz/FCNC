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
from collections import defaultdict
from my_utils import *

#HistAddress = '/users/rgoldouz/FCNC/NanoAnalysis/hists/old/'
year=['2018']
variables=[ "MVATU","MVATC"]
variablesName=["Likelihood ratio TU", "Likelihood ratio TC"]
sys = ["eleRecoIdIso","muRecoIdIso","triggerSF","pu","prefiring","bcTagSfCorr","LTagSfCorr","bcTagSfUnCorr","LTagSfUnCorr","LTagSfUnCorr","JetPuID", "JesFlavorQCD", "JesBBEC1", "JesAbsolute", "JesRelativeBal", "JesRelativeSample","Jes","Jer"]
sys = ["Jer"]
jetSys=["JetPuID", "JesFlavorQCD", "JesBBEC1", "JesAbsolute", "JesRelativeBal", "JesRelativeSample","Jes","Jer"]
sysFA=["fakeAll","fakePt","fakeEta"]
sysTh=["RenUp","RenDown","FacUp","FacDown","IsrUp","IsrDown","FsrUp","FsrDown","PDF1","PDF2","PDF3","PDF4","PDF5","PDF6","PDF7","PDF8","PDF9","PDF10","PDF11","PDF12","PDF13","PDF14","PDF15","PDF16","PDF17","PDF18","PDF19","PDF20","PDF21","PDF22","PDF23","PDF24","PDF25","PDF26","PDF27","PDF28","PDF29","PDF30","PDF31","PDF32","PDF33","PDF34","PDF35","PDF36","PDF37","PDF38","PDF39","PDF40","PDF41","PDF42","PDF43","PDF44","PDF45","PDF46","PDF47","PDF48","PDF49","PDF50","PDF51","PDF52","PDF53","PDF54","PDF55","PDF56","PDF57","PDF58","PDF59","PDF60","PDF61","PDF62","PDF63","PDF64","PDF65","PDF66","PDF67","PDF68","PDF69","PDF70","PDF71","PDF72","PDF73","PDF74","PDF75","PDF76","PDF77","PDF78","PDF79","PDF80","PDF81","PDF82","PDF83","PDF84","PDF85","PDF86","PDF87","PDF88","PDF89","PDF90","PDF91","PDF92","PDF93","PDF94","PDF95","PDF96","PDF97","PDF98","PDF99","PDF100"]
sysThName=['Ren','Fac','Isr','Fsr','PDF']

Hists = {}
HistsSysUp = {}
HistsSysDown = {}
HistsSysThUp = {}
Hists_copy = {}
HistsFake = {}
drawFakeRegions=True

for nameyear in year:
    Hists[nameyear] = {}
    Hists_copy[nameyear] = {}
    HistsSysUp[nameyear] = {}
    HistsSysDown[nameyear] = {}
    HistsSysThUp[nameyear] = {}
    for f, sample in enumerate(Samples):
        sample_key = sample
        Hists[nameyear][sample_key] = {}
        Hists_copy[nameyear][sample_key] = {}
        HistsSysUp[nameyear][sample_key] = {}
        HistsSysDown[nameyear][sample_key] = {}
        HistsSysThUp[nameyear][sample_key] = {}
        file = ROOT.TFile.Open(HistAddress + nameyear + '_' + sample)
        for ch in channels:
            for reg in regions:
                for var in variables:
                    hist_key = "{}_{}_{}".format(ch,reg,var)
                    ho = file.Get(hist_key)
                    h = EFTtoNormal(ho, wc1)
                    hCopy = EFTtoNormalNoWC(ho)
                    # Apply binning if needed
                    if 'MVA' in var:
                        for key in binsDic:
                            if key in ch:
                                bins = binsDic[key]
                                h = h.Rebin(len(bins) - 1, "", bins)
                                hCopy = hCopy.Rebin(len(bins) - 1, "", bins)
                                break
                    h.SetLineColor(colors[f])
                    Hists[nameyear][sample_key][hist_key] = h.Clone()
                    Hists_copy[nameyear][sample_key][hist_key]= hCopy.Clone()
                    
                    # Only get systematics for non-data samples and specific channels/vars
                    if f > 0 and ch in channelsSys:
                        h_up = file.Get("{}_{}_{}_Th".format(ch,reg,var))
                        hSys_up = sysEFTtoNormal(h_up, sysTh, colors)
                        HistsSysThUp[nameyear][sample_key][hist_key]=hSys_up
                        for s in sysTh:
                            HistsSysThUp[nameyear][sample_key][hist_key][s]=HistsSysThUp[nameyear][sample_key][hist_key][s].Rebin(len(bins) - 1, "", bins)

                        HistsSysUp[nameyear][sample_key][hist_key] = {}
                        HistsSysDown[nameyear][sample_key][hist_key] = {}
                        for numsys, namesys in enumerate(sys):
                            h_up = EFTtoNormal(file.Get("{}_{}_{}_{}_Up".format(ch,reg,var,namesys)), wc1)
                            h_up=h_up.Rebin(len(bins) - 1, "", bins)
                            HistsSysUp[nameyear][sample_key][hist_key][namesys]=h_up
                            h_down = EFTtoNormal(file.Get("{}_{}_{}_{}_Down".format(ch,reg,var,namesys)), wc1)
                            h_down = h_down.Rebin(len(bins) - 1, "", bins)
                            HistsSysDown[nameyear][sample_key][hist_key][namesys]=h_down

HistsFake = {}
HistsSysFAUp = {}
HistsSysFADown = {}
for nameyear in year:
    HistsFake[nameyear] = {}
    HistsSysFAUp[nameyear] = {}
    HistsSysFADown[nameyear] = {}
    for f, sample in enumerate(Samples):
        sample_key = sample
        HistsFake[nameyear][sample_key] = {}
        HistsSysFAUp[nameyear][sample_key] = {}
        HistsSysFADown[nameyear][sample_key] = {}
        file = ROOT.TFile.Open(HistAddress + nameyear + '_' + sample)
        for ch in channelsFake:
            for reg in regions:
                for var in variables:
                    hist_key = "{}_{}_{}".format(ch,reg,var)
                    ho = file.Get(hist_key)
                    h = EFTtoNormal(ho, wc1)
                    # Apply binning if needed
                    if 'MVA' in var:
                        for key in binsDic:
                            if key in ch:
                                bins = binsDic[key]
                                h = h.Rebin(len(bins) - 1, "", bins)
                                break
                    h.SetLineColor(colors[f])
                    HistsFake[nameyear][sample_key][hist_key] = h.Clone()
                    HistsSysFAUp[nameyear][sample_key][hist_key] = {}
                    HistsSysFADown[nameyear][sample_key][hist_key] = {}
                    for numsys, namesys in enumerate(sysFA):
                    # Up variation
                        h_up = EFTtoNormal(file.Get("{}_{}_{}_{}_Up".format(ch,reg,var,namesys)), wc1)
                        h_up=h_up.Rebin(len(bins) - 1, "", bins)
                        HistsSysFAUp[nameyear][sample_key][hist_key][namesys]=h_up
                        h_down = EFTtoNormal(file.Get("{}_{}_{}_{}_Down".format(ch,reg,var,namesys)), wc1)
                        h_down = h_down.Rebin(len(bins) - 1, "", bins)
                        HistsSysFADown[nameyear][sample_key][hist_key][namesys]=h_down

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
            for numsys, namesys in enumerate(sysTh):
                mergeChRegSys_histograms(HistsSysThUp, nameyear, new_key=hist_key, merge_keys=[hist_key1,hist_key2,hist_key3],sys=namesys)
            hist_key = "2lss_LF_{}_{}".format(reg,var)
            hist_key1 = "2lssEE_LF_{}_{}".format(reg,var)
            hist_key2 = "2lssEM_LF_{}_{}".format(reg,var)
            hist_key3 = "2lssMM_LF_{}_{}".format(reg,var)
            mergeChReg_histograms(HistsFake, nameyear, new_key=hist_key, merge_keys=[hist_key1,hist_key2,hist_key3])
            for numsys, namesys in enumerate(sysFA):
                mergeChRegSys_histograms(HistsSysFAUp, nameyear, new_key=hist_key, merge_keys=[hist_key1,hist_key2,hist_key3],sys=namesys)
                mergeChRegSys_histograms(HistsSysFADown, nameyear, new_key=hist_key, merge_keys=[hist_key1,hist_key2,hist_key3],sys=namesys)
            hist_key = "2lss_FF_{}_{}".format(reg,var)
            hist_key1 = "2lssEE_FF_{}_{}".format(reg,var)
            hist_key2 = "2lssEM_FF_{}_{}".format(reg,var)
            hist_key3 = "2lssMM_FF_{}_{}".format(reg,var)
            mergeChReg_histograms(HistsFake, nameyear, new_key=hist_key, merge_keys=[hist_key1,hist_key2,hist_key3])
            for numsys, namesys in enumerate(sysFA):
                mergeChRegSys_histograms(HistsSysFAUp,nameyear, new_key=hist_key, merge_keys=[hist_key1,hist_key2,hist_key3],sys=namesys)
                mergeChRegSys_histograms(HistsSysFADown,nameyear, new_key=hist_key, merge_keys=[hist_key1,hist_key2,hist_key3],sys=namesys)

channels.append("2lss")
channelsFake.append("2lss_LF")
channelsFake.append("2lss_FF")

mergeYear_histograms(Hists, 'Run2', year)
mergeYear_histograms(Hists_copy, 'Run2', year)
mergeYear_histograms(HistsFake, 'Run2', year)
mergeYear_histograms_sys(HistsSysUp, 'Run2', year)
mergeYear_histograms_sys(HistsSysDown, 'Run2', year)
mergeYear_histograms_sys(HistsSysThUp, 'Run2', year)
mergeYear_histograms_sys(HistsSysFAUp, 'Run2', year)
mergeYear_histograms_sys(HistsSysFADown, 'Run2', year)
year.append('Run2')

mergeSample_histograms(HistsFake, new_sample="MCsum", samples_to_merge=['Triboson.root', 'Diboson.root', 'ttbar.root', 'ST.root','DY.root', 'Conv.root','TTW.root','TTH.root','TTZ.root','Else.root'])
for numsys, namesys in enumerate(sysFA):
    mergeSampleSys_histograms(HistsSysFAUp, new_sample="MCsum", samples_to_merge=['Triboson.root', 'Diboson.root', 'ttbar.root', 'ST.root','DY.root', 'Conv.root','TTW.root','TTH.root','TTZ.root','Else.root'],sys=namesys)
    mergeSampleSys_histograms(HistsSysFADown, new_sample="MCsum", samples_to_merge=['Triboson.root', 'Diboson.root', 'ttbar.root', 'ST.root','DY.root', 'Conv.root','TTW.root','TTH.root','TTZ.root','Else.root'],sys=namesys)

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

            for numsys2, namesys2 in enumerate(sysFA):
                HistsSysFAUp[nameyear][Samples[0]]["2lss_LF_{}_{}".format(namereg,namevar)][namesys2].Add(HistsSysFAUp[nameyear][Samples[0]]["2lss_FF_{}_{}".format(namereg,namevar)][namesys2],-1)
                HistsSysFAUp[nameyear][Samples[0]]["2lss_LF_{}_{}".format(namereg,namevar)][namesys2].Add(HistsSysFAUp[nameyear]["MCsum"]["2lss_LF_{}_{}".format(namereg,namevar)][namesys2],-1)
                HistsSysFAUp[nameyear][Samples[0]]["2lssEE_LF_{}_{}".format(namereg,namevar)][namesys2].Add(HistsSysFAUp[nameyear][Samples[0]]["2lssEE_FF_{}_{}".format(namereg,namevar)][namesys2],-1)
                HistsSysFAUp[nameyear][Samples[0]]["2lssEE_LF_{}_{}".format(namereg,namevar)][namesys2].Add(HistsSysFAUp[nameyear]["MCsum"]["2lssEE_LF_{}_{}".format(namereg,namevar)][namesys2],-1)
                HistsSysFAUp[nameyear][Samples[0]]["2lssEM_LF_{}_{}".format(namereg,namevar)][namesys2].Add(HistsSysFAUp[nameyear][Samples[0]]["2lssEM_FF_{}_{}".format(namereg,namevar)][namesys2],-1)
                HistsSysFAUp[nameyear][Samples[0]]["2lssEM_LF_{}_{}".format(namereg,namevar)][namesys2].Add(HistsSysFAUp[nameyear]["MCsum"]["2lssEM_LF_{}_{}".format(namereg,namevar)][namesys2],-1)
                HistsSysFAUp[nameyear][Samples[0]]["2lssMM_LF_{}_{}".format(namereg,namevar)][namesys2].Add(HistsSysFAUp[nameyear][Samples[0]]["2lssMM_FF_{}_{}".format(namereg,namevar)][namesys2],-1)
                HistsSysFAUp[nameyear][Samples[0]]["2lssMM_LF_{}_{}".format(namereg,namevar)][namesys2].Add(HistsSysFAUp[nameyear]["MCsum"]["2lssMM_LF_{}_{}".format(namereg,namevar)][namesys2],-1)
                HistsSysFAUp[nameyear][Samples[0]]["3lonZ_LLF_{}_{}".format(namereg,namevar)][namesys2].Add(HistsSysFAUp[nameyear][Samples[0]]["3lonZ_LFF_{}_{}".format(namereg,namevar)][namesys2],-1)
                HistsSysFAUp[nameyear][Samples[0]]["3lonZ_LLF_{}_{}".format(namereg,namevar)][namesys2].Add(HistsSysFAUp[nameyear]["MCsum"]["3lonZ_LLF_{}_{}".format(namereg,namevar)][namesys2],-1)
                HistsSysFAUp[nameyear][Samples[0]]["3lonZ_LLF_{}_{}".format(namereg,namevar)][namesys2].Add(HistsSysFAUp[nameyear][Samples[0]]["3lonZ_FFF_{}_{}".format(namereg,namevar)][namesys2])
                HistsSysFAUp[nameyear][Samples[0]]["3loffZhigh_LLF_{}_{}".format(namereg,namevar)][namesys2].Add(HistsSysFAUp[nameyear][Samples[0]]["3loffZhigh_LFF_{}_{}".format(namereg,namevar)][namesys2],-1)
                HistsSysFAUp[nameyear][Samples[0]]["3loffZhigh_LLF_{}_{}".format(namereg,namevar)][namesys2].Add(HistsSysFAUp[nameyear]["MCsum"]["3loffZhigh_LLF_{}_{}".format(namereg,namevar)][namesys2],-1)
                HistsSysFAUp[nameyear][Samples[0]]["3loffZhigh_LLF_{}_{}".format(namereg,namevar)][namesys2].Add(HistsSysFAUp[nameyear][Samples[0]]["3loffZhigh_FFF_{}_{}".format(namereg,namevar)][namesys2])                
                
                HistsSysFADown[nameyear][Samples[0]]["2lss_LF_{}_{}".format(namereg,namevar)][namesys2].Add(HistsSysFADown[nameyear][Samples[0]]["2lss_FF_{}_{}".format(namereg,namevar)][namesys2],-1)
                HistsSysFADown[nameyear][Samples[0]]["2lss_LF_{}_{}".format(namereg,namevar)][namesys2].Add(HistsSysFADown[nameyear]["MCsum"]["2lss_LF_{}_{}".format(namereg,namevar)][namesys2],-1)
                HistsSysFADown[nameyear][Samples[0]]["2lssEE_LF_{}_{}".format(namereg,namevar)][namesys2].Add(HistsSysFADown[nameyear][Samples[0]]["2lssEE_FF_{}_{}".format(namereg,namevar)][namesys2],-1)
                HistsSysFADown[nameyear][Samples[0]]["2lssEE_LF_{}_{}".format(namereg,namevar)][namesys2].Add(HistsSysFADown[nameyear]["MCsum"]["2lssEE_LF_{}_{}".format(namereg,namevar)][namesys2],-1)
                HistsSysFADown[nameyear][Samples[0]]["2lssEM_LF_{}_{}".format(namereg,namevar)][namesys2].Add(HistsSysFADown[nameyear][Samples[0]]["2lssEM_FF_{}_{}".format(namereg,namevar)][namesys2],-1)
                HistsSysFADown[nameyear][Samples[0]]["2lssEM_LF_{}_{}".format(namereg,namevar)][namesys2].Add(HistsSysFADown[nameyear]["MCsum"]["2lssEM_LF_{}_{}".format(namereg,namevar)][namesys2],-1)
                HistsSysFADown[nameyear][Samples[0]]["2lssMM_LF_{}_{}".format(namereg,namevar)][namesys2].Add(HistsSysFADown[nameyear][Samples[0]]["2lssMM_FF_{}_{}".format(namereg,namevar)][namesys2],-1)
                HistsSysFADown[nameyear][Samples[0]]["2lssMM_LF_{}_{}".format(namereg,namevar)][namesys2].Add(HistsSysFADown[nameyear]["MCsum"]["2lssMM_LF_{}_{}".format(namereg,namevar)][namesys2],-1)
                HistsSysFADown[nameyear][Samples[0]]["3lonZ_LLF_{}_{}".format(namereg,namevar)][namesys2].Add(HistsSysFADown[nameyear][Samples[0]]["3lonZ_LFF_{}_{}".format(namereg,namevar)][namesys2],-1)
                HistsSysFADown[nameyear][Samples[0]]["3lonZ_LLF_{}_{}".format(namereg,namevar)][namesys2].Add(HistsSysFADown[nameyear]["MCsum"]["3lonZ_LLF_{}_{}".format(namereg,namevar)][namesys2],-1)
                HistsSysFADown[nameyear][Samples[0]]["3lonZ_LLF_{}_{}".format(namereg,namevar)][namesys2].Add(HistsSysFADown[nameyear][Samples[0]]["3lonZ_FFF_{}_{}".format(namereg,namevar)][namesys2])
                HistsSysFADown[nameyear][Samples[0]]["3loffZhigh_LLF_{}_{}".format(namereg,namevar)][namesys2].Add(HistsSysFADown[nameyear][Samples[0]]["3loffZhigh_LFF_{}_{}".format(namereg,namevar)][namesys2],-1)
                HistsSysFADown[nameyear][Samples[0]]["3loffZhigh_LLF_{}_{}".format(namereg,namevar)][namesys2].Add(HistsSysFADown[nameyear]["MCsum"]["3loffZhigh_LLF_{}_{}".format(namereg,namevar)][namesys2],-1)
                HistsSysFADown[nameyear][Samples[0]]["3loffZhigh_LLF_{}_{}".format(namereg,namevar)][namesys2].Add(HistsSysFADown[nameyear][Samples[0]]["3loffZhigh_FFF_{}_{}".format(namereg,namevar)][namesys2])

#year=['Run2']
for numyear, nameyear in enumerate(year):
    for numch, namech in enumerate(channelsFake):
        if namech.count('F')>1:
            continue
        for numreg, namereg in enumerate(regions):
            for numvar, namevar in enumerate(variables):
                hist_key = "{}_{}_{}".format(namech,namereg,namevar)
                glistup = []
                glistdown = []
                for numsys2, namesys2 in enumerate(sysFA):
                    hup = HistsSysFAUp[nameyear][Samples[0]][hist_key][namesys2].Clone()
                    hdown = HistsSysFADown[nameyear][Samples[0]][hist_key][namesys2].Clone()
                    if hup.Integral()>0 or hdown.Integral()>0:
                        for b in range(hup.GetNbinsX()):
                            cv = HistsFake[nameyear][Samples[0]][hist_key].GetBinContent(b+1)
                            rb = 0
                            if cv>0:
                                rb = 100/cv
                            hup.SetBinContent(b+1, 0 + abs(max((HistsSysFAUp[nameyear][Samples[0]][hist_key][namesys2].GetBinContent(b+1)-cv)*rb, (HistsSysFADown[nameyear][Samples[0]][hist_key][namesys2].GetBinContent(b+1)-cv)*rb,0)))
                            hdown.SetBinContent(b+1, 0 - abs(min((HistsSysFAUp[nameyear][Samples[0]][hist_key][namesys2].GetBinContent(b+1)-cv)*rb, (HistsSysFADown[nameyear][Samples[0]][hist_key][namesys2].GetBinContent(b+1)-cv)*rb,0)))
                    glistup.append(hup)
                    glistdown.append(hdown)
                compareError(glistup,glistdown, sysFA, 'sys', namech, namereg.split('_')[0], nameyear,namevar,variablesName[numvar], 'FA_'+Samples[0].split('.')[0])

for f in range(1,len(Samples)):
    for numyear, nameyear in enumerate(year):
        for numch, namech in enumerate(channels):
            for numreg, namereg in enumerate(regions):
                for numvar, namevar in enumerate(variables):
                    hist_key = "{}_{}_{}".format(namech,namereg,namevar)
                    if Hists[nameyear][Samples[f]][hist_key].Integral() < 0.15*Hists[nameyear][Samples[0]][hist_key].Integral():
                        continue
                    if f>0 and namech in channelsSys:
                        glistup = []
                        glistdown = []
                        for numsys2, namesys2 in enumerate(sys):
                            hup = HistsSysUp[nameyear][Samples[f]][hist_key][namesys2].Clone()
                            hdown = HistsSysDown[nameyear][Samples[f]][hist_key][namesys2].Clone()
                            if hup.Integral()>0 or hdown.Integral()>0:
                                for b in range(hup.GetNbinsX()):
                                    cv = Hists[nameyear][Samples[f]][hist_key].GetBinContent(b+1)
                                    rb = 0
                                    if cv>0:
                                        rb = 100/cv
                                    hup.SetBinContent(b+1, 0 + abs(max((HistsSysUp[nameyear][Samples[f]][hist_key][namesys2].GetBinContent(b+1)-cv)*rb, (HistsSysDown[nameyear][Samples[f]][hist_key][namesys2].GetBinContent(b+1)-cv)*rb,0)))
                                    hdown.SetBinContent(b+1, 0 - abs(min((HistsSysUp[nameyear][Samples[f]][hist_key][namesys2].GetBinContent(b+1)-cv)*rb, (HistsSysDown[nameyear][Samples[f]][hist_key][namesys2].GetBinContent(b+1)-cv)*rb,0)))
                            glistup.append(hup)
                            glistdown.append(hdown)
                        compareError(glistup,glistdown, sys, 'sys',namech, namereg, nameyear,namevar,variablesName[numvar], 'Exp_'+Samples[f].split('.')[0])

for f in range(1,len(Samples)):
    for numyear, nameyear in enumerate(year):
        for numch, namech in enumerate(channels):
            for numreg, namereg in enumerate(regions):
                for numvar, namevar in enumerate(variables):
                    hist_key = "{}_{}_{}".format(namech,namereg,namevar)
                    if Hists[nameyear][Samples[f]][hist_key].Integral() < 0.15*Hists[nameyear][Samples[0]][hist_key].Integral():
                        continue
                    if f>0 and namech in channelsSys:
                        glistup = []
                        glistdown = []
                        PDF=defaultdict(float)
                        for numsys2 in range(0, len(sysTh)):
                            namesys2=sysTh[numsys2]
                            if 'PDF' in namesys2:
                                for b in range(Hists_copy[nameyear][Samples[f]][hist_key].GetNbinsX()):
                                    PDF[b] = PDF[b] + (HistsSysThUp[nameyear][Samples[f]][hist_key][sysTh[numsys2]].GetBinContent(b+1) - Hists_copy[nameyear][Samples[f]][hist_key].GetBinContent(b+1))**2
                        for numsys2 in range(0, len(sysTh), 2):
                            namesys2=sysTh[numsys2]
                            if 'PDF' in namesys2:
                                continue
                            hup = HistsSysThUp[nameyear][Samples[f]][hist_key][namesys2].Clone()
                            hdown = HistsSysThUp[nameyear][Samples[f]][hist_key][namesys2].Clone()
                            if hup.Integral()>0 or hdown.Integral()>0:
                                for b in range(hup.GetNbinsX()):
                                    cv = Hists_copy[nameyear][Samples[f]][hist_key].GetBinContent(b+1)
                                    rb = 0
                                    if cv>0:
                                        rb = 100/cv
                                    hup.SetBinContent(b+1, 0 + abs(max((HistsSysThUp[nameyear][Samples[f]][hist_key][sysTh[numsys2]].GetBinContent(b+1)-cv)*rb, (HistsSysThUp[nameyear][Samples[f]][hist_key][sysTh[numsys2+1]].GetBinContent(b+1)-cv)*rb,0)))
                                    hdown.SetBinContent(b+1, 0 - abs(min((HistsSysThUp[nameyear][Samples[f]][hist_key][sysTh[numsys2]].GetBinContent(b+1)-cv)*rb, (HistsSysThUp[nameyear][Samples[f]][hist_key][sysTh[numsys2+1]].GetBinContent(b+1)-cv)*rb,0)))
                            glistup.append(hup)
                            glistdown.append(hdown)
                        hPdfUp=Hists_copy[nameyear][Samples[f]][hist_key].Clone()
                        hPdfDown=Hists_copy[nameyear][Samples[f]][hist_key].Clone()
                        for b in range(Hists_copy[nameyear][Samples[f]][hist_key].GetNbinsX()):
                            if Hists_copy[nameyear][Samples[f]][hist_key].GetBinContent(b+1)>0:
                                hPdfUp.SetBinContent(b+1, 0 + math.sqrt(PDF[b])/Hists_copy[nameyear][Samples[f]][hist_key].GetBinContent(b+1))
                                hPdfDown.SetBinContent(b+1, 0 - math.sqrt(PDF[b])/Hists_copy[nameyear][Samples[f]][hist_key].GetBinContent(b+1))
                        glistup.append(hPdfUp)
                        glistdown.append(hPdfDown)
                        compareError(glistup,glistdown, sysThName,'sys', namech, namereg, nameyear,namevar,variablesName[numvar], 'Th_'+Samples[f].split('.')[0])

os.system('tar -cvf sys.tar sys')

