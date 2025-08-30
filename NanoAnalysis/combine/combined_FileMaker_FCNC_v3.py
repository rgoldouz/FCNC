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
from ROOT import TFile
from ROOT import TGaxis
from ROOT import THStack
import gc
from operator import truediv
import copy
TGaxis.SetMaxDigits(2)
from collections import defaultdict
from collections import OrderedDict
sys.path.append(os.path.abspath('../plot'))
from my_utils import *

def AnalyticAnomalousCoupling(H,Wcs,name):
    AACList=[]
    nbins = H.GetNbinsX()
    bin_edges = [H.GetBinLowEdge(i + 1) for i in range(nbins)]
    bin_edges.append(H.GetXaxis().GetBinUpEdge(nbins))
    bin_array = array.array('d', bin_edges)
    hpx = ROOT.TH1F(H.GetName(), H.GetName(), nbins, bin_array)
    edges = array.array('d', bin_edges)  # 'd' for double precision
    for i in range(len(Wcs)):
        quad=hpx.Clone()    
        sm_lin_quad=hpx.Clone()
        for b in range(hpx.GetNbinsX()+1):
            binFit=H.GetBinFit(b+1)
            coeff=binFit.getCoefficient(Wcs[i],Wcs[i])
            quad.SetBinContent(b+1, coeff)
            quad.SetBinError(b+1, 0)     
            sm_lin_quad.SetBinContent(b+1, coeff)
            sm_lin_quad.SetBinError(b+1, 0)
        if quad.Integral()<0.001:
            print "***WARNING--> WC "+Wcs[i]+' is not relevant for the '+name+' process, so it is ignored'
            continue    
        quad.SetName(name+'_quad_'+Wcs[i]+'F')
        quad.SetBinContent(quad.GetXaxis().GetNbins(), quad.GetBinContent(quad.GetXaxis().GetNbins()) + quad.GetBinContent(quad.GetXaxis().GetNbins()+1))
        AACList.append(quad)
        sm_lin_quad.SetName(name+'_sm_lin_quad_'+Wcs[i]+'F')
        sm_lin_quad.SetBinContent(sm_lin_quad.GetXaxis().GetNbins(), sm_lin_quad.GetBinContent(sm_lin_quad.GetXaxis().GetNbins()) + sm_lin_quad.GetBinContent(sm_lin_quad.GetXaxis().GetNbins()+1))
        AACList.append(sm_lin_quad)
        for j in range(i+1,len(Wcs)):
            coeffSum=H.GetSumFit()
            if coeffSum.getCoefficient(Wcs[j],Wcs[j])<0.01:
                continue
            sm_lin_quad_mixed=hpx.Clone()
            for b in range(hpx.GetNbinsX()+1):
                binFit=H.GetBinFit(b+1)
                coeff1=binFit.getCoefficient(Wcs[i],Wcs[i])
                coeff2=binFit.getCoefficient(Wcs[j],Wcs[j])
                coeffMix=binFit.getCoefficient(Wcs[i],Wcs[j])
                sm_lin_quad_mixed.SetBinContent(b+1, coeff1+coeff2+(2*coeffMix))
                sm_lin_quad_mixed.SetBinError(b+1, 0)
            sm_lin_quad_mixed.SetName(name+'_sm_lin_quad_mixed_'+Wcs[i]+'F'+'_'+Wcs[j]+'F')
            sm_lin_quad_mixed.SetBinError(b+1, 0)
            sm_lin_quad_mixed.SetBinContent(sm_lin_quad_mixed.GetXaxis().GetNbins(), sm_lin_quad_mixed.GetBinContent(sm_lin_quad_mixed.GetXaxis().GetNbins()) + sm_lin_quad_mixed.GetBinContent(sm_lin_quad_mixed.GetXaxis().GetNbins()+1))
            AACList.append(sm_lin_quad_mixed)
    return AACList


def noNegativeBin(h):
   for b in range(h.GetNbinsX()):
       if h.GetBinContent(b+1)<=0:
           h.SetBinContent(b+1,0.00001)
           h.SetBinError(b+1,0.0)

Sig="TC"
year=['2016preVFP', '2016postVFP', '2017','2018']
ULyear=['UL16preVFP', 'UL16postVFP', 'UL17','UL18']
#year=['2018']
#ULyear=['UL18']
LumiErr = [0.018, 0.018, 0.018, 0.018]
regions=["1bLj","1bHj","G1b"]
#regions=["1bLj"]
channels=["2lssEE", "2lssEM","2lssMM", "2losEE_Weighted", "2losEM_Weighted", "3lonZ", "3loffZhigh"]
variables=["MVA"+Sig]
#lep1Pt"]
sys = ["eleRecoIdIso","muRecoIdIso","triggerSF","pu","prefiring","bcTagSfCorr","LTagSfCorr","bcTagSfUnCorr","LTagSfUnCorr","JetPuID", "JesFlavorQCD", "JesBBEC1", "JesAbsolute", "JesRelativeBal", "JesRelativeSample","Jer"]
sysName=["CMS_eff_e_total","CMS_eff_m_total","CMS_eff_em_trigger","CMS_pileup_13TeV","CMS_l1_ecal_prefiring_2017","CMS_eff_btag_heavy_correlated","CMS_eff_btag_light_correlated","CMS_eff_btag_heavy_uncorrelated","CMS_eff_btag_light_uncorrelated",
"CMS_eff_j_pileup","CMS_scale_j_FlavorQCD", "CMS_scale_j_BBEC1","CMS_scale_j_Absolute", "CMS_scale_j_RelativeBal", "CMS_scale_j_RelativeSample","CMS_res_j"]
Samples = ['data.root','Triboson.root', 'Diboson.root', 'ttbar.root', 'ST.root','DY.root', 'Conv.root','TTW.root','TTH.root','TTZ.root','Else.root','FCNC'+Sig+'Production.root','FCNC'+Sig+'Decay.root']
SamplesName = ['Data','Triboson', 'Diboson', 't#bar{t}', 'Single top','DY', 'Conversions','t#bar{t}W','t#bar{t}H','t#bar{t}Z','Wj+tWZ+4t','FCNC'+Sig+'-Production','FCNC'+Sig+'-Decay']#
SamplesNameCombined = ['data_obs','Triboson', 'Diboson','ttbar','ST','DY', 'Conv','ttW','ttH','ttZ','WptWZp4t','FCNC'+Sig+'-Prod','FCNC'+Sig+'-Dec']
WCs=["ctp","ctlS","cte","ctl","ctlT","ctZ","cpt","cpQM","ctA","cQe","ctG","cQlM"]
#WCs=["cpQM","ctZ"]
channelsCom=["2lss", "3lonZ", "3loffZhigh"]
sysUncor= ["bcTagSfUnCorr","LTagSfUnCorr","JesBBEC1", "JesAbsolute","Jer"]
sysFA=["fakeAll","fakePt","fakeEta"]
sysFAName=["CMS_TOP25015_fakeAll","CMS_TOP25015_fakePt","CMS_TOP25015_fakeEta"]
sysTh=["RenUp","RenDown","FacUp","FacDown","IsrUp","IsrDown","FsrUp","FsrDown","PDF1","PDF2","PDF3","PDF4","PDF5","PDF6","PDF7","PDF8","PDF9","PDF10","PDF11","PDF12","PDF13","PDF14","PDF15","PDF16","PDF17","PDF18","PDF19","PDF20","PDF21","PDF22","PDF23","PDF24","PDF25","PDF26","PDF27","PDF28","PDF29","PDF30","PDF31","PDF32","PDF33","PDF34","PDF35","PDF36","PDF37","PDF38","PDF39","PDF40","PDF41","PDF42","PDF43","PDF44","PDF45","PDF46","PDF47","PDF48","PDF49","PDF50","PDF51","PDF52","PDF53","PDF54","PDF55","PDF56","PDF57","PDF58","PDF59","PDF60","PDF61","PDF62","PDF63","PDF64","PDF65","PDF66","PDF67","PDF68","PDF69","PDF70","PDF71","PDF72","PDF73","PDF74","PDF75","PDF76","PDF77","PDF78","PDF79","PDF80","PDF81","PDF82","PDF83","PDF84","PDF85","PDF86","PDF87","PDF88","PDF89","PDF90","PDF91","PDF92","PDF93","PDF94","PDF95","PDF96","PDF97","PDF98","PDF99","PDF100"]
sysThName=['Ren','Fac','Isr','Fsr','PDF']
sysThNameCombined=['QCDscale_ren','QCDscale_fac','ps_isr','ps_fsr','pdf_alphas']
colors =  [ROOT.kBlack,ROOT.TColor.GetColor("#3f90da"),ROOT.TColor.GetColor("#ffa90e"), ROOT.TColor.GetColor("#bd1f01"),ROOT.TColor.GetColor("#94a4a2"), ROOT.TColor.GetColor("#832db6"),ROOT.TColor.GetColor("#a96b59"),ROOT.TColor.GetColor("#e76300"),ROOT.TColor.GetColor("#b9ac70"),ROOT.TColor.GetColor("#717581"),ROOT.TColor.GetColor("#92dadd"),ROOT.kBlack,ROOT.TColor.GetColor("#3f90da"),ROOT.TColor.GetColor("#ffa90e"), ROOT.TColor.GetColor("#bd1f01"),ROOT.TColor.GetColor("#94a4a2"), ROOT.TColor.GetColor("#832db6"),ROOT.TColor.GetColor("#a96b59")]

wc1 = ROOT.WCPoint("EFTrwgt1_cT_1_cS_0")
print 'making combine files'

HistsOrg={}
Hists = {}
HistsSysUp = {}
HistsSysDown = {}
HistsSysThUp = {}
Hists_copy = {}
HistsFake = {}

for nameyear in year:
    Hists[nameyear] = {}
    HistsOrg[nameyear] = {}
    Hists_copy[nameyear] = {}
    HistsSysUp[nameyear] = {}
    HistsSysDown[nameyear] = {}
    HistsSysThUp[nameyear] = {}
    for f, sample in enumerate(Samples):
        sample_key = sample
        Hists[nameyear][sample_key] = {}
        HistsOrg[nameyear][sample_key] = {}
        Hists_copy[nameyear][sample_key] = {}
        HistsSysUp[nameyear][sample_key] = {}
        HistsSysDown[nameyear][sample_key] = {}
        HistsSysThUp[nameyear][sample_key] = {}
        file = ROOT.TFile.Open(HistAddress + nameyear + '_' + sample)
        for namech in channels:
            for namereg in regions:
                for namevar in variables:
                    hist_key = "{}_{}_{}".format(namech,namereg,namevar)
                    ho = file.Get(hist_key)
                    h = EFTtoNormal(ho, wc1)
                    hCopy = EFTtoNormalNoWC(ho)
                    # Apply binning if needed
                    if 'MVA' in namevar:
                        for key in binsDic:
                            if key in namech:
                                bins = binsDic[key]
                                h = h.Rebin(len(bins) - 1, "", bins)
                                hCopy = hCopy.Rebin(len(bins) - 1, "", bins)
                                break
                    h.SetLineColor(colors[f])
                    Hists[nameyear][sample_key][hist_key] = h.Clone()
                    HistsOrg[nameyear][sample_key][hist_key] = ho.Clone()
                    Hists_copy[nameyear][sample_key][hist_key]= hCopy.Clone()

                    # Only get systematics for non-data samples and specific channels/vars
                    if f > 0 and namech in channelsSys:
                        h_up = file.Get("{}_{}_{}_Th".format(namech,namereg,namevar))
                        hSys_up = sysEFTtoNormal(h_up, sysTh, colors)
                        HistsSysThUp[nameyear][sample_key][hist_key]=hSys_up
                        for s in sysTh:
                            HistsSysThUp[nameyear][sample_key][hist_key][s]=HistsSysThUp[nameyear][sample_key][hist_key][s].Rebin(len(bins) - 1, "", bins)

                        HistsSysUp[nameyear][sample_key][hist_key] = {}
                        HistsSysDown[nameyear][sample_key][hist_key] = {}
                        for numsys, namesys in enumerate(sys):
                            h_up = file.Get("{}_{}_{}_{}_Up".format(namech,namereg,namevar,namesys))
                            HistsSysUp[nameyear][sample_key][hist_key][namesys]=h_up
                            h_down = file.Get("{}_{}_{}_{}_Down".format(namech,namereg,namevar,namesys))
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
        for namech in channelsFake:
            for namereg in regions:
                for namevar in variables:
                    hist_key = "{}_{}_{}".format(namech,namereg,namevar)
                    ho = file.Get(hist_key)
                    h = EFTtoNormal(ho, wc1)
                    # Apply binning if needed
                    if 'MVA' in namevar:
                        for key in binsDic:
                            if key in namech:
                                bins = binsDic[key]
                                h = h.Rebin(len(bins) - 1, "", bins)
                                break
                    h.SetLineColor(colors[f])
                    HistsFake[nameyear][sample_key][hist_key] = h.Clone()
                    HistsSysFAUp[nameyear][sample_key][hist_key] = {}
                    HistsSysFADown[nameyear][sample_key][hist_key] = {}
                    for numsys, namesys in enumerate(sysFA):
                    # Up variation
                        h_up = EFTtoNormal(file.Get("{}_{}_{}_{}_Up".format(namech,namereg,namevar,namesys)), wc1)
                        h_up=h_up.Rebin(len(bins) - 1, "", bins)
                        HistsSysFAUp[nameyear][sample_key][hist_key][namesys]=h_up
                        h_down = EFTtoNormal(file.Get("{}_{}_{}_{}_Down".format(namech,namereg,namevar,namesys)), wc1)
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
            mergeChReg_histograms(HistsOrg, nameyear, new_key=hist_key, merge_keys=[hist_key1,hist_key2,hist_key3])
            for numsys2, namesys2 in enumerate(sys):
                mergeChRegSys_histograms(HistsSysUp, nameyear, new_key=hist_key, merge_keys=[hist_key1,hist_key2,hist_key3],sys=namesys2)
                mergeChRegSys_histograms(HistsSysDown, nameyear, new_key=hist_key, merge_keys=[hist_key1,hist_key2,hist_key3],sys=namesys2)
            for numsys, namesys in enumerate(sysTh):
                mergeChRegSys_histograms(HistsSysThUp, nameyear, new_key=hist_key, merge_keys=[hist_key1,hist_key2,hist_key3],sys=namesys)
            hist_key = "2los_Weighted_{}_{}".format(reg,var)
            hist_key1 = "2losEE_Weighted_{}_{}".format(reg,var)
            hist_key2 = "2losEM_Weighted_{}_{}".format(reg,var)
            mergeChReg_histograms(Hists, nameyear, new_key=hist_key, merge_keys=[hist_key1,hist_key2])
            mergeChReg_histograms(Hists_copy, nameyear, new_key=hist_key, merge_keys=[hist_key1,hist_key2])
            mergeChReg_histograms(HistsOrg, nameyear, new_key=hist_key, merge_keys=[hist_key1,hist_key2])
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
channels.append("2los_Weighted")
channelsFake.append("2lss_LF")
channelsFake.append("2lss_FF")

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

HistsRatioThUp = {}
HistsRatioThDown = {}
HistsRatioThUpSmooth = {}
HistsRatioThDownSmooth = {}
for nameyear in year:
    HistsRatioThUp[nameyear] = {}
    HistsRatioThDown[nameyear] = {}
    HistsRatioThUpSmooth[nameyear] = {}
    HistsRatioThDownSmooth[nameyear] = {}
    for f, sample in enumerate(Samples):
        sample_key = sample
        HistsRatioThUp[nameyear][sample_key] = {}
        HistsRatioThDown[nameyear][sample_key] = {}
        HistsRatioThUpSmooth[nameyear][sample_key] = {}
        HistsRatioThDownSmooth[nameyear][sample_key] = {}
        for namech in channels:
            for namereg in regions:
                for namevar in variables:
                    hist_key = "{}_{}_{}".format(namech,namereg,namevar)
                    HistsRatioThUp[nameyear][sample_key][hist_key] = {}
                    HistsRatioThDown[nameyear][sample_key][hist_key] = {}
                    HistsRatioThUpSmooth[nameyear][sample_key][hist_key] = {}
                    HistsRatioThDownSmooth[nameyear][sample_key][hist_key] = {}

# Find PDF uncertainties as ratio histograms
for f in range(1,len(Samples)):
    for numyear, nameyear in enumerate(year):
        for numch, namech in enumerate(channels):
            for numreg, namereg in enumerate(regions):
                for numvar, namevar in enumerate(variables):
                    hist_key = "{}_{}_{}".format(namech,namereg,namevar)
                    if 'MVA' in namevar:
                        for key in binsDic:
                            if key in namech:
                                bins = binsDic[key]
                                break
                    if f>0 and namech in channelsSys:
                        PDF=defaultdict(float)
                        for numsys2 in range(0, len(sysTh)):
                            namesys2=sysTh[numsys2]
                            if 'PDF' in namesys2:
                                for b in range(Hists_copy[nameyear][Samples[f]][hist_key].GetNbinsX()):
                                    PDF[b] = PDF[b] + (HistsSysThUp[nameyear][Samples[f]][hist_key][sysTh[numsys2]].GetBinContent(b+1) - Hists_copy[nameyear][Samples[f]][hist_key].GetBinContent(b+1))**2
                            for s in sysThName:
                                if namesys2==s+'Up':
                                    th=HistsSysThUp[nameyear][Samples[f]][hist_key][sysTh[numsys2]].Clone()
                                    th.Add(Hists_copy[nameyear][Samples[f]][hist_key],-1)
                                    th.Divide(Hists_copy[nameyear][Samples[f]][hist_key])
                                    HistsRatioThUp[nameyear][Samples[f]][hist_key][s]= th
                                   # smoothNominal= SmoothingVariableBins(Hists_copy[nameyear][Samples[f]][hist_key],3,bins)
                                   # thSmooth=HistsSysThUp[nameyear][Samples[f]][hist_key][sysTh[numsys2]].Clone()
                                   # thSmooth.Add(smoothNominal,-1)
                                   # HistsRatioThUpSmooth[nameyear][Samples[f]][hist_key][s]=thSmooth
                                if namesys2==s+'Down':
                                    th=HistsSysThUp[nameyear][Samples[f]][hist_key][sysTh[numsys2]].Clone()
                                    th.Add(Hists_copy[nameyear][Samples[f]][hist_key],-1)
                                    th.Divide(Hists_copy[nameyear][Samples[f]][hist_key])
                                    HistsRatioThDown[nameyear][Samples[f]][hist_key][s]= th
                                   # smoothNominal= SmoothingVariableBins(Hists_copy[nameyear][Samples[f]][hist_key],3,bins)
                                   # thSmooth=HistsSysThUp[nameyear][Samples[f]][hist_key][sysTh[numsys2]].Clone()
                                   # thSmooth.Add(smoothNominal,-1)
                                   # HistsRatioThDownSmooth[nameyear][Samples[f]][hist_key][s]=thSmooth

                                    #HistsSysThUp[nameyear][Samples[f]][hist_key][sysTh[numsys2]].Add(Hists_copy[nameyear][Samples[f]][hist_key],-1)
                                    #HistsRatioThDown[nameyear][Samples[f]][hist_key][s]= HistsSysThUp[nameyear][Samples[f]][hist_key][sysTh[numsys2]]
                        hPdfUp=Hists_copy[nameyear][Samples[f]][hist_key].Clone()
                        hPdfDown=Hists_copy[nameyear][Samples[f]][hist_key].Clone()
                        for b in range(Hists_copy[nameyear][Samples[f]][hist_key].GetNbinsX()):
                            if Hists_copy[nameyear][Samples[f]][hist_key].GetBinContent(b+1)>0:
                                hPdfUp.SetBinContent(b+1, 0 + math.sqrt(PDF[b])/Hists_copy[nameyear][Samples[f]][hist_key].GetBinContent(b+1))
                                hPdfDown.SetBinContent(b+1, 0 - math.sqrt(PDF[b])/Hists_copy[nameyear][Samples[f]][hist_key].GetBinContent(b+1))
                        HistsRatioThUp[nameyear][Samples[f]][hist_key]['PDF']=hPdfUp
                        HistsRatioThDown[nameyear][Samples[f]][hist_key]['PDF']=hPdfDown
                        for s in sysThName:                     
                            for b in range(HistsRatioThUp[nameyear][Samples[f]][hist_key][s].GetNbinsX()+1):
                                HistsRatioThUp[nameyear][Samples[f]][hist_key][s].SetBinContent(b+1, HistsRatioThUp[nameyear][Samples[f]][hist_key][s].GetBinContent(b+1)+1)
                                HistsRatioThDown[nameyear][Samples[f]][hist_key][s].SetBinContent(b+1, HistsRatioThDown[nameyear][Samples[f]][hist_key][s].GetBinContent(b+1)+1)

if not os.path.exists('CombinedFilesFCNC_v2'):
    os.makedirs('CombinedFilesFCNC_v2')

Integrals=OrderedDict()
for nameyear in year:
    Integrals[nameyear] = OrderedDict()
    for numch, namech in enumerate(channels):
        for numreg, namereg in enumerate(regions):
            for numvar, namevar in enumerate(variables):
                hist_key = "{}_{}_{}".format(namech,namereg,namevar)
                Integrals[nameyear][hist_key] = OrderedDict()
#start making cards
for nameyear in year:
    for numch, namech in enumerate(channels):
        if namech not in channelsCom or namech in ["2lssEE", "2lssEM","2lssMM"]:
            continue
        for numreg, namereg in enumerate(regions):
            for numvar, namevar in enumerate(variables):
                hfile = ROOT.TFile( 'CombinedFilesFCNC_v2/{}_{}_{}_{}.root'.format(nameyear,namech,namereg,namevar), 'RECREATE', 'combine input histograms' )
                hist_key = "{}_{}_{}".format(namech,namereg,namevar)
                if 'MVA' in namevar:
                    for key in binsDic:
                        if key in namech:
                            bins = binsDic[key]
                if '2l' in namech:
                #write chargeFlip histograms
                    noNegativeBin(Hists[nameyear][Samples[0]]["{}_{}_{}".format(chargeFlipMap[namech],namereg,namevar)])
                    Integrals[nameyear][hist_key]["DD_chargeFlip"]=Hists[nameyear][Samples[0]]["{}_{}_{}".format(chargeFlipMap[namech],namereg,namevar)].Integral()
                    Hists[nameyear][Samples[0]]["{}_{}_{}".format(chargeFlipMap[namech],namereg,namevar)].SetName("DD_chargeFlip")
                    Hists[nameyear][Samples[0]]["{}_{}_{}".format(chargeFlipMap[namech],namereg,namevar)].Write()
                #write the fake histograms
                    noNegativeBin(HistsFake[nameyear][Samples[0]]["2lss_LF_{}_{}".format(namereg,namevar)])
                    Integrals[nameyear][hist_key]["DD_Fake"]=HistsFake[nameyear][Samples[0]]["2lss_LF_{}_{}".format(namereg,namevar)].Integral()
                    HistsFake[nameyear][Samples[0]]["2lss_LF_{}_{}".format(namereg,namevar)].SetName("DD_Fake")
                    HistsFake[nameyear][Samples[0]]["2lss_LF_{}_{}".format(namereg,namevar)].Write()
                    for numsys, namesys in enumerate(sysFA):
                        noNegativeBin(HistsSysFAUp[nameyear][Samples[0]]["2lss_LF_{}_{}".format(namereg,namevar)][namesys])
                        HistsSysFAUp[nameyear][Samples[0]]["2lss_LF_{}_{}".format(namereg,namevar)][namesys].SetName('DD_Fake_'+sysFAName[numsys]+'_'+nameyear+'Up')
                        HistsSysFAUp[nameyear][Samples[0]]["2lss_LF_{}_{}".format(namereg,namevar)][namesys].Write()
                        noNegativeBin(HistsSysFADown[nameyear][Samples[0]]["2lss_LF_{}_{}".format(namereg,namevar)][namesys])
                        HistsSysFADown[nameyear][Samples[0]]["2lss_LF_{}_{}".format(namereg,namevar)][namesys].SetName('DD_Fake_'+sysFAName[numsys]+'_'+nameyear+'Down')
                        HistsSysFADown[nameyear][Samples[0]]["2lss_LF_{}_{}".format(namereg,namevar)][namesys].Write()
                if '3lonZ' in namech:
                    noNegativeBin(HistsFake[nameyear][Samples[0]]["3lonZ_LLF_{}_{}".format(namereg,namevar)])
                    Integrals[nameyear][hist_key]["DD_Fake"]=HistsFake[nameyear][Samples[0]]["3lonZ_LLF_{}_{}".format(namereg,namevar)].Integral()
                    HistsFake[nameyear][Samples[0]]["3lonZ_LLF_{}_{}".format(namereg,namevar)].SetName("DD_Fake")
                    HistsFake[nameyear][Samples[0]]["3lonZ_LLF_{}_{}".format(namereg,namevar)].Write()
                    for numsys, namesys in enumerate(sysFA):
                        noNegativeBin(HistsSysFAUp[nameyear][Samples[0]]["3lonZ_LLF_{}_{}".format(namereg,namevar)][namesys])
                        HistsSysFAUp[nameyear][Samples[0]]["3lonZ_LLF_{}_{}".format(namereg,namevar)][namesys].SetName('DD_Fake_'+sysFAName[numsys]+'_'+nameyear+'Up')
                        HistsSysFAUp[nameyear][Samples[0]]["3lonZ_LLF_{}_{}".format(namereg,namevar)][namesys].Write()
                        noNegativeBin(HistsSysFADown[nameyear][Samples[0]]["3lonZ_LLF_{}_{}".format(namereg,namevar)][namesys])
                        HistsSysFADown[nameyear][Samples[0]]["3lonZ_LLF_{}_{}".format(namereg,namevar)][namesys].SetName('DD_Fake_'+sysFAName[numsys]+'_'+nameyear+'Down')
                        HistsSysFADown[nameyear][Samples[0]]["3lonZ_LLF_{}_{}".format(namereg,namevar)][namesys].Write()
                if '3loffZhigh' in namech:
                    noNegativeBin(HistsFake[nameyear][Samples[0]]["3loffZhigh_LLF_{}_{}".format(namereg,namevar)])
                    Integrals[nameyear][hist_key]["DD_Fake"]=HistsFake[nameyear][Samples[0]]["3loffZhigh_LLF_{}_{}".format(namereg,namevar)].Integral()
                    HistsFake[nameyear][Samples[0]]["3loffZhigh_LLF_{}_{}".format(namereg,namevar)].SetName("DD_Fake")
                    HistsFake[nameyear][Samples[0]]["3loffZhigh_LLF_{}_{}".format(namereg,namevar)].Write()
                    for numsys, namesys in enumerate(sysFA):
                        noNegativeBin(HistsSysFAUp[nameyear][Samples[0]]["3loffZhigh_LLF_{}_{}".format(namereg,namevar)][namesys])
                        HistsSysFAUp[nameyear][Samples[0]]["3loffZhigh_LLF_{}_{}".format(namereg,namevar)][namesys].SetName('DD_Fake_'+sysFAName[numsys]+'_'+nameyear+'Up')
                        HistsSysFAUp[nameyear][Samples[0]]["3loffZhigh_LLF_{}_{}".format(namereg,namevar)][namesys].Write()
                        noNegativeBin(HistsSysFADown[nameyear][Samples[0]]["3loffZhigh_LLF_{}_{}".format(namereg,namevar)][namesys])
                        HistsSysFADown[nameyear][Samples[0]]["3loffZhigh_LLF_{}_{}".format(namereg,namevar)][namesys].SetName('DD_Fake_'+sysFAName[numsys]+'_'+nameyear+'Down')
                        HistsSysFADown[nameyear][Samples[0]]["3loffZhigh_LLF_{}_{}".format(namereg,namevar)][namesys].Write()
	        for f, sample in enumerate(Samples):
                    sample_key = sample
                    if f==0:
                        Integrals[nameyear][hist_key][SamplesNameCombined[f]]=Hists[nameyear][Samples[f]][hist_key].Integral()
                        Hists[nameyear][Samples[f]][hist_key].SetName(SamplesNameCombined[f])              
                        Hists[nameyear][Samples[f]][hist_key].Write()
                    else:
                        if 'FCNC' not in SamplesNameCombined[f]:
                            #write BG histograms
                            noNegativeBin(Hists[nameyear][Samples[f]][hist_key])
                            Integrals[nameyear][hist_key][SamplesNameCombined[f]]=Hists[nameyear][Samples[f]][hist_key].Integral()
                            Hists[nameyear][Samples[f]][hist_key].SetName(SamplesNameCombined[f])
                            Hists[nameyear][Samples[f]][hist_key].Write()
                            for numsys, namesys in enumerate(sysThName):
                                HistsRatioThUp[nameyear][Samples[f]][hist_key][namesys].Multiply(Hists[nameyear][Samples[f]][hist_key])
                                noNegativeBin(HistsRatioThUp[nameyear][Samples[f]][hist_key][namesys])
                                HistsRatioThUp[nameyear][Samples[f]][hist_key][namesys].SetName(SamplesNameCombined[f]+'_'+sysThNameCombined[numsys]+'Up')
                                if namesys=='Ren' or namesys=='Fac' or namesys=='Isr' or namesys=='Fsr':
                                    HistsRatioThUp[nameyear][Samples[f]][hist_key][namesys].SetName(SamplesNameCombined[f]+'_'+sysThNameCombined[numsys]+'_'+SamplesNameCombined[f]+'Up')
                                HistsRatioThUp[nameyear][Samples[f]][hist_key][namesys].Write()
                                HistsRatioThDown[nameyear][Samples[f]][hist_key][namesys].Multiply(Hists[nameyear][Samples[f]][hist_key])
                                noNegativeBin(HistsRatioThDown[nameyear][Samples[f]][hist_key][namesys])
                                HistsRatioThDown[nameyear][Samples[f]][hist_key][namesys].SetName(SamplesNameCombined[f]+'_'+sysThNameCombined[numsys]+'Down')
                                if namesys=='Ren' or namesys=='Fac' or namesys=='Isr' or namesys=='Fsr':
                                    HistsRatioThDown[nameyear][Samples[f]][hist_key][namesys].SetName(SamplesNameCombined[f]+'_'+sysThNameCombined[numsys]+'_'+SamplesNameCombined[f]+'Down')
                                HistsRatioThDown[nameyear][Samples[f]][hist_key][namesys].Write()                           
                            #write BG histograms sys
                            for numsys, namesys in enumerate(sys):
                                h=EFTtoNormal(HistsSysUp[nameyear][Samples[f]][hist_key][namesys], wc1)
                                h=h.Rebin(len(bins) - 1, "", bins)
                                noNegativeBin(h)
                                print namesys +":"+sysName[numsys]
                                h.SetName(SamplesNameCombined[f]+'_'+sysName[numsys]+'Up')
                                if namesys in sysUncor:
                                    h.SetName(SamplesNameCombined[f]+'_'+ sysName[numsys]+'_'+nameyear+'Up')
                                h.Write()
                                h=EFTtoNormal(HistsSysDown[nameyear][Samples[f]][hist_key][namesys], wc1)
                                h=h.Rebin(len(bins) - 1, "", bins)
                                noNegativeBin(h)
                                h.SetName(SamplesNameCombined[f]+'_'+sysName[numsys]+'Down')
                                if namesys in sysUncor:
                                    h.SetName(SamplesNameCombined[f]+'_'+sysName[numsys]+'_'+nameyear+'Down')
                                h.Write()
                        else:
                            SignalH=AnalyticAnomalousCoupling(HistsOrg[nameyear][Samples[f]][hist_key],WCs,SamplesNameCombined[f])
                            #compareError([HistsRatioThUp[nameyear][Samples[f]][hist_key]['Fac'],HistsRatioThUpSmooth[nameyear][Samples[f]][hist_key]['Fac']],[HistsRatioThDown[nameyear][Samples[f]][hist_key]['Fac'],HistsRatioThDownSmooth[nameyear][Samples[f]][hist_key]['Fac']], ['Fac','FacSmoothed'], folder='THsys', ch = namech, reg = namereg, year=nameyear, var=Samples[f]+'Facsmooth', varname="v", prefix = 'Th')
                            #compareError(list(HistsRatioThUp[nameyear][Samples[f]][hist_key].values()),list(HistsRatioThDown[nameyear][Samples[f]][hist_key].values()), sysThName, folder='THsys', ch = namech, reg = namereg, year=nameyear, var=Samples[f], varname="v", prefix = 'Th')
                            for H in SignalH:
                                H=H.Rebin(len(bins) - 1, "", bins)
                                noNegativeBin(H)
                                H.Write()
                                Integrals[nameyear][hist_key][H.GetName()]=H.Integral()
                                for numsys, namesys in enumerate(sysThName):
                                    HHup=H.Clone()
                                    HHup.Multiply(HistsRatioThUp[nameyear][Samples[f]][hist_key][namesys])
                                    noNegativeBin(HHup)
                                    if (namesys=='Ren' or namesys=='Fac' or namesys=='Isr' or namesys=='Fsr') and 'Prod' in H.GetName():
                                        HHup.SetName(H.GetName()+'_'+sysThNameCombined[numsys]+'_FCNC'+Sig+'-ProdUp')
                                    elif (namesys=='Ren' or namesys=='Fac' or namesys=='Isr' or namesys=='Fsr') and 'Dec' in H.GetName():
                                        HHup.SetName(H.GetName()+'_'+sysThNameCombined[numsys]+'_FCNC'+Sig+'-DecUp')
                                    else:
                                        HHup.SetName(H.GetName()+'_'+sysThNameCombined[numsys]+'Up')
                                    HHup.Write()
                                    HHdown=H.Clone()
                                    HHdown.Multiply(HistsRatioThDown[nameyear][Samples[f]][hist_key][namesys])
                                    noNegativeBin(HHdown)
                                    if (namesys=='Ren' or namesys=='Fac' or namesys=='Isr' or namesys=='Fsr') and 'Prod' in H.GetName():
                                        HHdown.SetName(H.GetName()+'_'+sysThNameCombined[numsys]+'_FCNC'+Sig+'-ProdDown')
                                    elif (namesys=='Ren' or namesys=='Fac' or namesys=='Isr' or namesys=='Fsr') and 'Dec' in H.GetName():
                                        HHdown.SetName(H.GetName()+'_'+sysThNameCombined[numsys]+'_FCNC'+Sig+'-DecDown')
                                    else:
                                        HHdown.SetName(H.GetName()+'_'+sysThNameCombined[numsys]+'Down')
                                    HHdown.Write()
                            for numsys, namesys in enumerate(sys):
                                SignalH=AnalyticAnomalousCoupling(HistsSysUp[nameyear][Samples[f]][hist_key][namesys],WCs,SamplesNameCombined[f]) 
                                for H in SignalH:
                                    H=H.Rebin(len(bins) - 1, "", bins)
                                    noNegativeBin(H)
                                    if namesys in sysUncor:
                                        H.SetName(H.GetName()+'_'+sysName[numsys]+'_'+nameyear+'Up')
                                    else:
                                        H.SetName(H.GetName()+'_'+sysName[numsys]+'Up')
                                    H.Write()
                                SignalH=AnalyticAnomalousCoupling(HistsSysDown[nameyear][Samples[f]][hist_key][namesys],WCs,SamplesNameCombined[f])
                                for H in SignalH:
                                    H=H.Rebin(len(bins) - 1, "", bins)
                                    noNegativeBin(H)
                                    if namesys in sysUncor:
                                        H.SetName(H.GetName()+'_'+sysName[numsys]+'_'+nameyear+'Down')
                                    else:
                                        H.SetName(H.GetName()+'_'+sysName[numsys]+'Down')
                                    H.Write()
                hfile.Write()
                hfile.Close()
#####
for numyear, nameyear in enumerate(year):
    for numch, namech in enumerate(channels):
        if namech not in channelsCom:
            continue
        for numreg, namereg in enumerate(regions):
            for numvar, namevar in enumerate(variables):
                hist_key = "{}_{}_{}".format(namech,namereg,namevar)
                cardName = 'C{}_{}_{}_{}'.format(nameyear,namech,namereg,namevar) 
                T1 = 'max 1 number of categories \n' +\
                     'jmax * number of samples minus one\n' +\
                     'kmax * number of nuisance parameters\n' +\
                     '------------\n'+\
                     'shapes * * '  + nameyear+'_'+namech+'_'+namereg+'_' +namevar+'.root' + ' $PROCESS $PROCESS_$SYSTEMATIC\n' +\
                     '------------\n'+\
                     'bin'.ljust(45) + cardName + '\n'+\
                     'observation'.ljust(45) + str(Integrals[nameyear][hist_key][SamplesNameCombined[0]]) +'\n'+\
                     '------------\n'
                T1 = T1 +'bin'.ljust(45)
                for key, value in Integrals[nameyear][hist_key].iteritems():
                    if 'data' not in key:
                        T1 = T1 + cardName.ljust(45)
                T1 = T1 + '\n'
                T1 = T1 +'process'.ljust(45)
                c=1
                l=0
                for key, value in Integrals[nameyear][hist_key].iteritems():
                    if 'data' not in key:
                        if 'FCNC' in key:
                            print str(l).ljust(45) + key.ljust(45)+str(value).ljust(45)
                            T1 = T1 + str(l).ljust(45)
                            l=l-1                         
                        else:
                            T1 = T1 + str(c).ljust(45)
                            c=c+1
                T1 = T1 + '\n'
                T1 = T1 +'process'.ljust(45)
                for key, value in Integrals[nameyear][hist_key].iteritems():
                    if 'data' not in key:
                        T1 = T1 + key.ljust(45)
                T1 = T1 + '\n'
                T1 = T1 +'rate'.ljust(45)
                for key, value in Integrals[nameyear][hist_key].iteritems():
                    if 'data' not in key:
                        T1 = T1 + str(value).ljust(45)
                T1 = T1 + '\n'
                # Define systematics templates
                sys_templates = {
                    'lumi_2016': '1.01',
                    'lumi_2017': '1.02',
                    'lumi_2018': '1.015',
                    'lumi_13TeV_correlated#16': '1.006',
                    'lumi_13TeV_correlated#17': '1.009',
                    'lumi_13TeV_correlated#18': '1.02',
                    'lumi_13TeV_1718#17': '1.006',
                    'lumi_13TeV_1718#18': '1.002',
                    'cross_section_Diboson': '1.06',
                    'cross_section_Triboson': '1.10',
                    'cross_section_ttW': '1.15',
                    'cross_section_ttZ': '1.15',
                    'cross_section_ttH': '1.15',
                    'cross_section_WptWZp4t': '1.15',
                    'cross_section_conversion': '1.05',
                    'cross_section_ttbar':'1.05',
                    'cross_section_ST':'1.1',
                    'cross_section_DY':'1.05',
                    'cross_section_Fake': '1.1',
                    'cross_section_ChFlip': '1.3'
                }
                
                # Initialize lines
                lines = {k: k.ljust(45) + 'lnN'.ljust(10) if 'cross_section' in k else k.split("#")[0].ljust(45) + 'lnN'.ljust(10) for k in sys_templates}
                
                # Fill in systematic values
                for key in Integrals[nameyear][hist_key]:
                    if 'data' in key:
                        continue
                    isDD = 'DD' in key
                
                    for sys_key in sys_templates:
                        if 'lumi' in sys_key:
                            value = '-' if isDD else sys_templates[sys_key]
                            lines[sys_key] += value.ljust(45)
                        else:
                            if isDD:
                                if key == 'DD_Fake' and sys_key == 'cross_section_Fake':
                                    lines[sys_key] += '1.1'.ljust(45)
                                elif key == 'DD_chargeFlip' and sys_key == 'cross_section_ChFlip':
                                    lines[sys_key] += '1.30'.ljust(45)
                                else:
                                    lines[sys_key] += '-'.ljust(45)
                            else:
                                base_key = sys_key.split("_")[-1]
                                if key == base_key:
                                    lines[sys_key] += sys_templates[sys_key].ljust(45)
                                else:
                                    lines[sys_key] += '-'.ljust(45)
                
                if '2016' in nameyear:
                    T1 = T1 + lines['lumi_2016'] + '\n'
                    T1 = T1 + lines['lumi_13TeV_correlated#16'] + '\n'
                if '2017' in nameyear:
                    T1 = T1 + lines['lumi_2017'] + '\n'
                    T1 = T1 + lines['lumi_13TeV_correlated#17'] + '\n'
                    T1 = T1 + lines['lumi_13TeV_1718#17'] + '\n'
                if '2018' in nameyear:
                    T1 = T1 + lines['lumi_2018'] + '\n'
                    T1 = T1 + lines['lumi_13TeV_correlated#18'] + '\n'
                    T1 = T1 + lines['lumi_13TeV_1718#18'] + '\n'
                T1 += ''.join([lines[k] + '\n' for k in sys_templates if 'cross_section' in k and k in lines])
		for numsys, namesys in enumerate(sys):
                    Tsys=''
                    if namesys in sysUncor:
                        Tsys=(sysName[numsys]+'_'+nameyear).ljust(45)  +'shape'.ljust(10)
                    else:
                        Tsys=sysName[numsys].ljust(45)  +'shape'.ljust(10)
                    for key, value in Integrals[nameyear][hist_key].iteritems():
                        if 'data' not in key:
                           if 'DD' in key:
                               Tsys=Tsys+'-'.ljust(25)
                           else:
                               Tsys=Tsys+'1'.ljust(25)
                    T1 = T1 + Tsys + '\n'

#                sys_th = ['Triboson', 'Diboson', 'ttbar', 'ST', 'DY', 'Conv', 'ttW', 'ttH', 'ttZ', 'WptWZp4t', 'FCNC'+Sig+'-Prod', 'FCNC'+Sig+'-Dec']
                sys_th = ['Triboson', 'Diboson', 'ttW', 'ttH', 'ttZ', 'FCNC'+Sig+'-Prod', 'FCNC'+Sig+'-Dec']
                
                # Initialize lines dictionary with both Ren_ and Fac_ keys
                lines = {
                    'QCDscale_ren_' + k: ('QCDscale_ren_' + k).ljust(45) + 'shape'.ljust(10)
                    for k in sys_th
                }
                lines.update({
                    'QCDscale_fac_' + k: ('QCDscale_fac_' + k).ljust(45) + 'shape'.ljust(10)
                    for k in sys_th
                })
                lines.update({
                    'ps_isr_' + k: ('ps_isr_' + k).ljust(45) + 'shape'.ljust(10)
                    for k in sys_th
                })
                lines.update({
                    'ps_fsr_' + k: ('ps_fsr_' + k).ljust(45) + 'shape'.ljust(10)
                    for k in sys_th
                })
                
                # Fill in systematic values
                for key in Integrals[nameyear][hist_key]:
                    if 'data' in key:
                        continue
                    for sys_key in sys_th:
                        val = '1'.ljust(45) if sys_key in key else '-'.ljust(45)
                        lines['QCDscale_ren_' + sys_key] += val
                        lines['QCDscale_fac_' + sys_key] += val
                        lines['ps_isr_' + sys_key] += val
                        lines['ps_fsr_' + sys_key] += val
                T1 += ''.join([v + '\n' for v in lines.values()])
                
                # Add PDF/ISR
                sys_th2 = ['pdf_alphas']
                lines = {k: k.ljust(45) + 'shape'.ljust(10) for k in sys_th2}
                for key in Integrals[nameyear][hist_key]:
                    if 'data' in key:
                        continue
                    for sys_key in sys_th2:
                        val = '-' if 'DD' in key else '1'
                        lines[sys_key] += val.ljust(45)
                
                T1 += ''.join([v + '\n' for v in lines.values()])

                for numsys, namesys in enumerate(sysFA):
                    Tsys=(sysFAName[numsys]+'_'+nameyear).ljust(45)  +'shape'.ljust(10)
                    for key, value in Integrals[nameyear][hist_key].iteritems():
                        if 'data' not in key:
                           if 'DD_Fake' in key:
                               Tsys=Tsys+'1'.ljust(25)
                           else:
                               Tsys=Tsys+'-'.ljust(25)
                    T1 = T1 + Tsys + '\n'
                T1 = T1 +'------------\n' 
                T1 = T1 + '* autoMCStats 10' + '\n'
                open('CombinedFilesFCNC_v2/' + cardName +'.txt', 'wt').write(T1)
