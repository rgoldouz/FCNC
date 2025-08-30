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

def AnalyticAnomalousCoupling(H,Wcs,name):
    AACList=[]
    hpx    = ROOT.TH1F( H.GetName(), H.GetName(), H.GetXaxis().GetNbins(), H.GetXaxis().GetXmin(),H.GetXaxis().GetXmax() )
    for i in range(len(Wcs)):
        quad=hpx.Clone()    
        sm_lin_quad=hpx.Clone()
        for b in range(hpx.GetNbinsX()):
            binFit=H.GetBinFit(b+1)
            coeff=binFit.getCoefficient(Wcs[i],Wcs[i])
            quad.SetBinContent(b+1, coeff)
            quad.SetBinError(b+1, 0)     
            sm_lin_quad.SetBinContent(b+1, coeff)
            sm_lin_quad.SetBinError(b+1, 0)
        if quad.Integral()<0.01:
            print "***WARNING--> WC "+Wcs[i]+' is not relevant for the '+name+' process, so it is ignored'
            continue    
        quad.SetName(name+'_quad_'+Wcs[i]+'F')
        AACList.append(quad)
        sm_lin_quad.SetName(name+'_sm_lin_quad_'+Wcs[i]+'F')
        AACList.append(sm_lin_quad)
        for j in range(i+1,len(Wcs)):
            coeffSum=H.GetSumFit()
            if coeffSum.getCoefficient(Wcs[j],Wcs[j])<0.01:
                continue
            sm_lin_quad_mixed=hpx.Clone()
            for b in range(hpx.GetNbinsX()):
                binFit=H.GetBinFit(b+1)
                coeff1=binFit.getCoefficient(Wcs[i],Wcs[i])
                coeff2=binFit.getCoefficient(Wcs[j],Wcs[j])
                coeffMix=binFit.getCoefficient(Wcs[i],Wcs[j])
                sm_lin_quad_mixed.SetBinContent(b+1, coeff1+coeff2+(2*coeffMix))
                sm_lin_quad_mixed.SetBinError(b+1, 0)
            sm_lin_quad_mixed.SetName(name+'_sm_lin_quad_mixed_'+Wcs[i]+'F'+'_'+Wcs[j]+'F')
            sm_lin_quad_mixed.SetBinError(b+1, 0)
            AACList.append(sm_lin_quad_mixed)
    return AACList


def noNegativeBin(h):
   for b in range(h.GetNbinsX()):
       if h.GetBinContent(b+1)<=0:
           h.SetBinContent(b+1,0.00001)
           h.SetBinError(b+1,0.0)

Sig="TU"
year=['2016preVFP', '2016postVFP', '2017','2018']
ULyear=['UL16preVFP', 'UL16postVFP', 'UL17','UL18']
year=['2017']
ULyear=['UL17']
LumiErr = [0.018, 0.018, 0.018, 0.018]
regions=["1bLj","1bHj","G1b"]
channels=["2lss",  "3lonZ", "3loffZhigh"]
channelsFA=["2lss_LF", "2lss_FF", "3lonZ_LLF", "3lonZ_LFF","3lonZ_FFF","3loffZhigh_LLF", "3loffZhigh_LFF","3loffZhigh_FFF", "3loffZlow_LLF", "3loffZlow_LFF","3loffZlow_FFF"]
variables=["MVA"+Sig]
#lep1Pt"]
sys = ["eleRecoIdIso","muRecoIdIso","triggerSF","pu","prefiring","bcTagSfCorr","LTagSfCorr","bcTagSfUnCorr","LTagSfUnCorr","LTagSfUnCorr","JetPuID", "JesFlavorQCD", "JesBBEC1", "JesAbsolute", "JesRelativeBal", "JesRelativeSample","Jer"]
HistAddress = '/users/rgoldouz/FCNC/NanoAnalysis/hists/'
Samples = ['data.root','Triboson.root', 'Diboson.root', 'ttbar.root', 'ST.root','DY.root', 'Conv.root','TTX.root','FCNC'+Sig+'Production.root','FCNC'+Sig+'Decay.root']
SamplesName = ['Data','Triboson', 'Diboson', 't#bar{t}', 'Single top','DY', 'Conv','TTX+TX','FCNC'+Sig+'-Production','FCNC'+Sig+'-Decay']#
SamplesNameCombined = ['data_obs','Triboson', 'Diboson','tt','ST','DY', 'Conv','TTXTX','FCNC'+Sig+'-Prod','FCNC'+Sig+'-Dec']
WCs=["ctp","ctlS","cte","ctl","ctlT","ctZ","cpt","cpQM","ctA","cQe","ctG","cQlM"]
#WCs=["cpQM","ctZ"]
channelsSys=["2lss", "3lonZ", "3loffZhigh"]
sys = ["eleRecoIdIso","muRecoIdIso","triggerSF","pu","prefiring","bcTagSfCorr","LTagSfCorr","bcTagSfUnCorr","LTagSfUnCorr","LTagSfUnCorr","JetPuID", "JesFlavorQCD", "JesBBEC1", "JesAbsolute", "JesRelativeBal", "JesRelativeSample","Jer"]
sysFA=["fakeAll","fakePt","fakeEta"]
sysTh=["RenUp","RenDown","FacUp","FacDown","IsrUp","IsrDown","FsrUp","FsrDown","PDF1","PDF2","PDF3","PDF4","PDF5","PDF6","PDF7","PDF8","PDF9","PDF10","PDF11","PDF12","PDF13","PDF14","PDF15","PDF16","PDF17","PDF18","PDF19","PDF20","PDF21","PDF22","PDF23","PDF24","PDF25","PDF26","PDF27","PDF28","PDF29","PDF30","PDF31","PDF32","PDF33","PDF34","PDF35","PDF36","PDF37","PDF38","PDF39","PDF40","PDF41","PDF42","PDF43","PDF44","PDF45","PDF46","PDF47","PDF48","PDF49","PDF50","PDF51","PDF52","PDF53","PDF54","PDF55","PDF56","PDF57","PDF58","PDF59","PDF60","PDF61","PDF62","PDF63","PDF64","PDF65","PDF66","PDF67","PDF68","PDF69","PDF70","PDF71","PDF72","PDF73","PDF74","PDF75","PDF76","PDF77","PDF78","PDF79","PDF80","PDF81","PDF82","PDF83","PDF84","PDF85","PDF86","PDF87","PDF88","PDF89","PDF90","PDF91","PDF92","PDF93","PDF94","PDF95","PDF96","PDF97","PDF98","PDF99","PDF100"]
sysThName=['Ren','Fac','Isr','Fsr','PDF']
colors =  [ROOT.kBlack,ROOT.TColor.GetColor("#3f90da"),ROOT.TColor.GetColor("#ffa90e"), ROOT.TColor.GetColor("#bd1f01"),ROOT.TColor.GetColor("#94a4a2"), ROOT.TColor.GetColor("#832db6"),ROOT.TColor.GetColor("#a96b59"),ROOT.TColor.GetColor("#e76300"),ROOT.TColor.GetColor("#b9ac70"),ROOT.TColor.GetColor("#717581"),ROOT.TColor.GetColor("#92dadd"),ROOT.kBlack,ROOT.TColor.GetColor("#3f90da"),ROOT.TColor.GetColor("#ffa90e"), ROOT.TColor.GetColor("#bd1f01"),ROOT.TColor.GetColor("#94a4a2"), ROOT.TColor.GetColor("#832db6"),ROOT.TColor.GetColor("#a96b59")]

channelsFake=["2lss_LF", "2lss_FF", "3lonZ_LLF", "3lonZ_LFF","3lonZ_FFF","3loffZhigh_LLF", "3loffZhigh_LFF","3loffZhigh_FFF", "3loffZlow_LLF", "3loffZlow_LFF","3loffZlow_FFF"]
wc1 = ROOT.WCPoint("EFTrwgt1_cT_1_cS_0")
wcName = "cT"
print 'making combine files'

bins = array.array( 'd',[0.01,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,2,50] )
binsDic = {
'2l':array.array( 'd',[0.01,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.1,1.2,1.3,1.4,1.5,1.6,1.7,2,4,50] ),
'3lonZ':array.array( 'd',[0.01,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.2,1.4,1.6,1.8,2,2.5,3,5.0,10.0,20.0,50.0] ),
'3loffZ':array.array( 'd',[0.01,0.1,0.2,0.3,0.6,1.0,2.0,5.0,50.0] ),
}
HistsOrg={}
Hists = {}
HistsSysUp = {}
HistsSysDown = {}
HistsSysThUp = {}
Hists_copy = {}
HistsFA = {}


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
#                            h_up=h_up.Rebin(len(bins) - 1, "", bins)
                            HistsSysUp[nameyear][sample_key][hist_key][namesys]=h_up
                            h_down = file.Get("{}_{}_{}_{}_Down".format(namech,namereg,namevar,namesys))
#                            h_down.Rebin(len(bins) - 1, "", bins)
                            HistsSysDown[nameyear][sample_key][hist_key][namesys]=h_down

HistsFA = {}
HistsSysFAUp = {}
HistsSysFADown = {}
for nameyear in year:
    HistsFA[nameyear] = {}
    HistsSysFAUp[nameyear] = {}
    HistsSysFADown[nameyear] = {}
    for f, sample in enumerate(Samples):
        sample_key = sample
        HistsFA[nameyear][sample_key] = {}
        HistsSysFAUp[nameyear][sample_key] = {}
        HistsSysFADown[nameyear][sample_key] = {}
        file = ROOT.TFile.Open(HistAddress + nameyear + '_' + sample)
        for namech in channelsFA:
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
                    HistsFA[nameyear][sample_key][hist_key] = h.Clone()
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

for numyear, nameyear in enumerate(year):
    for numreg, namereg in enumerate(regions):
        for numvar, namevar in enumerate(variables):
            HistsFA[nameyear][Samples[0]]["2lss_LF_{}_{}".format(namereg,namevar)].Add(HistsFA[nameyear][Samples[0]]["2lss_FF_{}_{}".format(namereg,namevar)],-1)
            HistsFA[nameyear][Samples[0]]["3lonZ_LLF_{}_{}".format(namereg,namevar)].Add(HistsFA[nameyear][Samples[0]]["3lonZ_LFF_{}_{}".format(namereg,namevar)],-1)
            HistsFA[nameyear][Samples[0]]["3lonZ_LLF_{}_{}".format(namereg,namevar)].Add(HistsFA[nameyear][Samples[0]]["3lonZ_FFF_{}_{}".format(namereg,namevar)])
            HistsFA[nameyear][Samples[0]]["3loffZhigh_LLF_{}_{}".format(namereg,namevar)].Add(HistsFA[nameyear][Samples[0]]["3loffZhigh_LFF_{}_{}".format(namereg,namevar)],-1)
            HistsFA[nameyear][Samples[0]]["3loffZhigh_LLF_{}_{}".format(namereg,namevar)].Add(HistsFA[nameyear][Samples[0]]["3loffZhigh_FFF_{}_{}".format(namereg,namevar)])
            for numsys2, namesys2 in enumerate(sysFA):
                HistsSysFAUp[nameyear][Samples[0]]["2lss_LF_{}_{}".format(namereg,namevar)][namesys2].Add(HistsSysFAUp[nameyear][Samples[0]]["2lss_FF_{}_{}".format(namereg,namevar)][namesys2],-1)
                HistsSysFAUp[nameyear][Samples[0]]["3lonZ_LLF_{}_{}".format(namereg,namevar)][namesys2].Add(HistsSysFAUp[nameyear][Samples[0]]["3lonZ_LFF_{}_{}".format(namereg,namevar)][namesys2],-1)
                HistsSysFAUp[nameyear][Samples[0]]["3lonZ_LLF_{}_{}".format(namereg,namevar)][namesys2].Add(HistsSysFAUp[nameyear][Samples[0]]["3lonZ_FFF_{}_{}".format(namereg,namevar)][namesys2])
                HistsSysFAUp[nameyear][Samples[0]]["3loffZhigh_LLF_{}_{}".format(namereg,namevar)][namesys2].Add(HistsSysFAUp[nameyear][Samples[0]]["3loffZhigh_LFF_{}_{}".format(namereg,namevar)][namesys2],-1)
                HistsSysFAUp[nameyear][Samples[0]]["3loffZhigh_LLF_{}_{}".format(namereg,namevar)][namesys2].Add(HistsSysFAUp[nameyear][Samples[0]]["3loffZhigh_FFF_{}_{}".format(namereg,namevar)][namesys2])
                HistsSysFADown[nameyear][Samples[0]]["2lss_LF_{}_{}".format(namereg,namevar)][namesys2].Add(HistsSysFADown[nameyear][Samples[0]]["2lss_FF_{}_{}".format(namereg,namevar)][namesys2],-1)
                HistsSysFADown[nameyear][Samples[0]]["3lonZ_LLF_{}_{}".format(namereg,namevar)][namesys2].Add(HistsSysFADown[nameyear][Samples[0]]["3lonZ_LFF_{}_{}".format(namereg,namevar)][namesys2],-1)
                HistsSysFADown[nameyear][Samples[0]]["3lonZ_LLF_{}_{}".format(namereg,namevar)][namesys2].Add(HistsSysFADown[nameyear][Samples[0]]["3lonZ_FFF_{}_{}".format(namereg,namevar)][namesys2])
                HistsSysFADown[nameyear][Samples[0]]["3loffZhigh_LLF_{}_{}".format(namereg,namevar)][namesys2].Add(HistsSysFADown[nameyear][Samples[0]]["3loffZhigh_LFF_{}_{}".format(namereg,namevar)][namesys2],-1)
                HistsSysFADown[nameyear][Samples[0]]["3loffZhigh_LLF_{}_{}".format(namereg,namevar)][namesys2].Add(HistsSysFADown[nameyear][Samples[0]]["3loffZhigh_FFF_{}_{}".format(namereg,namevar)][namesys2])

HistsRatioThUp = {}
HistsRatioThDown = {}
for nameyear in year:
    HistsRatioThUp[nameyear] = {}
    HistsRatioThDown[nameyear] = {}
    for f, sample in enumerate(Samples):
        sample_key = sample
        HistsRatioThUp[nameyear][sample_key] = {}
        HistsRatioThDown[nameyear][sample_key] = {}
        for namech in channels:
            for namereg in regions:
                for namevar in variables:
                    hist_key = "{}_{}_{}".format(namech,namereg,namevar)
                    HistsRatioThUp[nameyear][sample_key][hist_key] = {}
                    HistsRatioThDown[nameyear][sample_key][hist_key] = {}

# Find PDF uncertainties as ratio histograms
for f in range(1,len(Samples)):
    for numyear, nameyear in enumerate(year):
        for numch, namech in enumerate(channels):
            for numreg, namereg in enumerate(regions):
                for numvar, namevar in enumerate(variables):
                    hist_key = "{}_{}_{}".format(namech,namereg,namevar)
                    if f>0 and namech in channelsSys:
                        PDF=defaultdict(float)
                        for numsys2 in range(0, len(sysTh)):
                            namesys2=sysTh[numsys2]
                            if 'PDF' in namesys2:
                                for b in range(Hists_copy[nameyear][Samples[f]][hist_key].GetNbinsX()):
                                    PDF[b] = PDF[b] + (HistsSysThUp[nameyear][Samples[f]][hist_key][sysTh[numsys2]].GetBinContent(b+1) - Hists_copy[nameyear][Samples[f]][hist_key].GetBinContent(b+1))**2
                            for s in sysThName:
                                if namesys2==s+'Up':
                                    HistsSysThUp[nameyear][Samples[f]][hist_key][sysTh[numsys2]].Add(Hists_copy[nameyear][Samples[f]][hist_key],-1)
                                    HistsRatioThUp[nameyear][Samples[f]][hist_key][s]= HistsSysThUp[nameyear][Samples[f]][hist_key][sysTh[numsys2]]
                                if namesys2==s+'Down':
                                    HistsRatioThDown[nameyear][Samples[f]][hist_key][s]= HistsSysThUp[nameyear][Samples[f]][hist_key][sysTh[numsys2]].Add(Hists_copy[nameyear][Samples[f]][hist_key],-1)
                                    HistsRatioThDown[nameyear][Samples[f]][hist_key][s]= HistsSysThUp[nameyear][Samples[f]][hist_key][sysTh[numsys2]]
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

if not os.path.exists('CombinedFilesFCNC'):
    os.makedirs('CombinedFilesFCNC')
else:
    os.system('rm -rf CombinedFilesFCNC/'+ wcName +'_*')

Integrals=OrderedDict()
nuisances={}
F=ROOT.TFile.Open(HistAddress + nameyear+ '_' + Samples[0])
for nameyear in year:
    Integrals[nameyear] = OrderedDict()
    for numch, namech in enumerate(channels):
        for numreg, namereg in enumerate(regions):
            for numvar, namevar in enumerate(variables):
                hist_key = "{}_{}_{}".format(namech,namereg,namevar)
                Integrals[nameyear][hist_key] = OrderedDict()

for nameyear in year:
    for numch, namech in enumerate(channels):
        for numreg, namereg in enumerate(regions):
            for numvar, namevar in enumerate(variables):
                hfile = ROOT.TFile( 'CombinedFilesFCNC_v2/{}_{}_{}_{}.root'.format(nameyear,namech,namereg,namevar), 'RECREATE', 'combine input histograms' )
                hist_key = "{}_{}_{}".format(namech,namereg,namevar)
                if 'MVA' in namevar:
                    for key in binsDic:
                        if key in namech:
                            bins = binsDic[key]

                #write the fake histograms
                if '2l' in namech:
                    noNegativeBin(HistsFA[nameyear][Samples[0]]["2lss_LF_{}_{}".format(namereg,namevar)])
                    Integrals[nameyear][hist_key]["DD_Fake"]=HistsFA[nameyear][Samples[0]]["2lss_LF_{}_{}".format(namereg,namevar)].Integral()
                    HistsFA[nameyear][Samples[0]]["2lss_LF_{}_{}".format(namereg,namevar)].SetName("DD_Fake")
                    HistsFA[nameyear][Samples[0]]["2lss_LF_{}_{}".format(namereg,namevar)].Write()
                    for numsys2, namesys in enumerate(sysFA):
                        noNegativeBin(HistsSysFAUp[nameyear][Samples[0]]["2lss_LF_{}_{}".format(namereg,namevar)][namesys])
                        HistsSysFAUp[nameyear][Samples[0]]["2lss_LF_{}_{}".format(namereg,namevar)][namesys].SetName('DD_Fake_'+namesys+'Up')
                        HistsSysFAUp[nameyear][Samples[0]]["2lss_LF_{}_{}".format(namereg,namevar)][namesys].Write()
                        noNegativeBin(HistsSysFADown[nameyear][Samples[0]]["2lss_LF_{}_{}".format(namereg,namevar)][namesys])
                        HistsSysFADown[nameyear][Samples[0]]["2lss_LF_{}_{}".format(namereg,namevar)][namesys].SetName('DD_Fake_'+namesys+'Down')
                        HistsSysFADown[nameyear][Samples[0]]["2lss_LF_{}_{}".format(namereg,namevar)][namesys].Write()
                if '3lonZ' in namech:
                    noNegativeBin(HistsFA[nameyear][Samples[0]]["3lonZ_LLF_{}_{}".format(namereg,namevar)])
                    Integrals[nameyear][hist_key]["DD_Fake"]=HistsFA[nameyear][Samples[0]]["3lonZ_LLF_{}_{}".format(namereg,namevar)].Integral()
                    HistsFA[nameyear][Samples[0]]["3lonZ_LLF_{}_{}".format(namereg,namevar)].SetName("DD_Fake")
                    HistsFA[nameyear][Samples[0]]["3lonZ_LLF_{}_{}".format(namereg,namevar)].Write()
                    for numsys2, namesys in enumerate(sysFA):
                        noNegativeBin(HistsSysFAUp[nameyear][Samples[0]]["3lonZ_LLF_{}_{}".format(namereg,namevar)][namesys])
                        HistsSysFAUp[nameyear][Samples[0]]["3lonZ_LLF_{}_{}".format(namereg,namevar)][namesys].SetName('DD_Fake_'+namesys+'Up')
                        HistsSysFAUp[nameyear][Samples[0]]["3lonZ_LLF_{}_{}".format(namereg,namevar)][namesys].Write()
                        noNegativeBin(HistsSysFADown[nameyear][Samples[0]]["3lonZ_LLF_{}_{}".format(namereg,namevar)][namesys])
                        HistsSysFADown[nameyear][Samples[0]]["3lonZ_LLF_{}_{}".format(namereg,namevar)][namesys].SetName('DD_Fake_'+namesys+'Down')
                        HistsSysFADown[nameyear][Samples[0]]["3lonZ_LLF_{}_{}".format(namereg,namevar)][namesys].Write()
                if '3loffZhigh' in namech:
                    noNegativeBin(HistsFA[nameyear][Samples[0]]["3loffZhigh_LLF_{}_{}".format(namereg,namevar)])
                    Integrals[nameyear][hist_key]["DD_Fake"]=HistsFA[nameyear][Samples[0]]["3loffZhigh_LLF_{}_{}".format(namereg,namevar)].Integral()
                    HistsFA[nameyear][Samples[0]]["3loffZhigh_LLF_{}_{}".format(namereg,namevar)].SetName("DD_Fake")
                    HistsFA[nameyear][Samples[0]]["3loffZhigh_LLF_{}_{}".format(namereg,namevar)].Write()
                    for numsys2, namesys in enumerate(sysFA):
                        noNegativeBin(HistsSysFAUp[nameyear][Samples[0]]["3loffZhigh_LLF_{}_{}".format(namereg,namevar)][namesys])
                        HistsSysFAUp[nameyear][Samples[0]]["3loffZhigh_LLF_{}_{}".format(namereg,namevar)][namesys].SetName('DD_Fake_'+namesys+'Up')
                        HistsSysFAUp[nameyear][Samples[0]]["3loffZhigh_LLF_{}_{}".format(namereg,namevar)][namesys].Write()
                        noNegativeBin(HistsSysFADown[nameyear][Samples[0]]["3loffZhigh_LLF_{}_{}".format(namereg,namevar)][namesys])
                        HistsSysFADown[nameyear][Samples[0]]["3loffZhigh_LLF_{}_{}".format(namereg,namevar)][namesys].SetName('DD_Fake_'+namesys+'Down')
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
                            for numsys2, namesys in enumerate(sysThName):
                                HistsRatioThUp[nameyear][Samples[f]][hist_key][namesys].Multiply(Hists[nameyear][Samples[f]][hist_key])
                                noNegativeBin(HistsRatioThUp[nameyear][Samples[f]][hist_key][namesys])
                                HistsRatioThUp[nameyear][Samples[f]][hist_key][namesys].SetName(SamplesNameCombined[f]+'_'+namesys+'Up')
                                HistsRatioThUp[nameyear][Samples[f]][hist_key][namesys].Write()
                                HistsRatioThDown[nameyear][Samples[f]][hist_key][namesys].Multiply(Hists[nameyear][Samples[f]][hist_key])
                                noNegativeBin(HistsRatioThDown[nameyear][Samples[f]][hist_key][namesys])
                                HistsRatioThDown[nameyear][Samples[f]][hist_key][namesys].SetName(SamplesNameCombined[f]+'_'+namesys+'Down')
                                HistsRatioThDown[nameyear][Samples[f]][hist_key][namesys].Write()                           
                            #write BG histograms sys
                            for numsys, namesys in enumerate(sys):
                                h=EFTtoNormal(HistsSysUp[nameyear][Samples[f]][hist_key][namesys], wc1)
                                h=h.Rebin(len(bins) - 1, "", bins)
                                noNegativeBin(h)
                                h.SetName(SamplesNameCombined[f]+'_'+namesys+'Up')
                                h.Write()
                                h=EFTtoNormal(HistsSysDown[nameyear][Samples[f]][hist_key][namesys], wc1)
                                h=h.Rebin(len(bins) - 1, "", bins)
                                noNegativeBin(h)
                                h.SetName(SamplesNameCombined[f]+'_'+namesys+'Down')
                                h.Write()
                        else:
                            SignalH=AnalyticAnomalousCoupling(HistsOrg[nameyear][Samples[f]][hist_key],WCs,SamplesNameCombined[f])
                            for H in SignalH:
                                H=H.Rebin(len(bins) - 1, "", bins)
                                noNegativeBin(H)
                                H.Write()
                                Integrals[nameyear][hist_key][H.GetName()]=H.Integral()
                                for numsys2, namesys in enumerate(sysThName):
                                    HHup=H.Clone()
                                    HHup.Multiply(HistsRatioThUp[nameyear][Samples[f]][hist_key][namesys])
                                    noNegativeBin(HHup)
                                    HHup.SetName(H.GetName()+'_'+namesys+'Up')
                                    HHup.Write()
                                    HHdown=H.Clone()
                                    HHdown.Multiply(HistsRatioThDown[nameyear][Samples[f]][hist_key][namesys])
                                    noNegativeBin(HHdown)
                                    HHdown.SetName(H.GetName()+'_'+namesys+'Down')
                                    HHdown.Write()
                            for numsys, namesys in enumerate(sys):
                                SignalH=AnalyticAnomalousCoupling(HistsSysUp[nameyear][Samples[f]][hist_key][namesys],WCs,SamplesNameCombined[f]) 
                                for H in SignalH:
                                    H=H.Rebin(len(bins) - 1, "", bins)
                                    noNegativeBin(H)
                                    H.SetName(H.GetName()+'_'+namesys+'Up')
                                    H.Write()
                                SignalH=AnalyticAnomalousCoupling(HistsSysDown[nameyear][Samples[f]][hist_key][namesys],WCs,SamplesNameCombined[f])
                                for H in SignalH:
                                    H=H.Rebin(len(bins) - 1, "", bins)
                                    noNegativeBin(H)
                                    H.SetName(H.GetName()+'_'+namesys+'Down')
                                    H.Write()
                hfile.Write()
                hfile.Close()
#####
for numyear, nameyear in enumerate(year):
    for numch, namech in enumerate(channels):
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
                ThLumi16 = 'lumi2016'.ljust(45)+'lnN'.ljust(10)
                ThLumi17 = 'lumi2017'.ljust(45)+'lnN'.ljust(10)
                ThLumi18 = 'lumi2018'.ljust(45)+'lnN'.ljust(10)
                ThLumi16_161718 = 'lumiCorr16-17-18'.ljust(45)+'lnN'.ljust(10)
                ThLumi17_161718 = 'lumiCorr16-17-18'.ljust(45)+'lnN'.ljust(10)
                ThLumi18_161718 = 'lumiCorr16-17-18'.ljust(45)+'lnN'.ljust(10)
                ThLumi17_1718 = 'lumiCorr17-18'.ljust(45)+'lnN'.ljust(10)
                ThLumi18_1718 = 'lumiCorr17-18'.ljust(45)+'lnN'.ljust(10)
                TDiboson = 'Diboson_norm'.ljust(35)+'lnN'.ljust(10)
                TtXttX = 'tXttX_norm'.ljust(35)+'lnN'.ljust(10)
                Tconversion = 'conversion_norm'.ljust(35)+'lnN'.ljust(10)
                TFake= 'Fake_norm'.ljust(35)+'lnN'.ljust(10)
                TChargFlip= 'DY_norm'.ljust(35)+'lnN'.ljust(10)

                for key, value in Integrals[nameyear][hist_key].iteritems():
                    if 'data' not in key:                
                      if 'DD' in key:
                          ThLumi16 = ThLumi16 + '-'.ljust(45)
                          ThLumi17 = ThLumi17 + '-'.ljust(45)
                          ThLumi18 = ThLumi18 + '-'.ljust(45)
                          ThLumi16_161718 = ThLumi16_161718 + '-'.ljust(45)
                          ThLumi17_161718 = ThLumi17_161718 + '-'.ljust(45)
                          ThLumi18_161718 = ThLumi18_161718 + '-'.ljust(45)
                          ThLumi17_1718 = ThLumi17_1718 + '-'.ljust(45)
                          ThLumi18_1718 = ThLumi18_1718 + '-'.ljust(45)
                          TDiboson = TDiboson + '-'.ljust(45)
                          TtXttX = TtXttX  + '-'.ljust(45)
                          Tconversion = Tconversion + '-'.ljust(45)
                          if key=='DD_Fake':
                              TFake = TFake + '1.1'.ljust(45)
                          else:
                              TFake = TFake + '-'.ljust(45)
                          if key=='DY':
                              TChargFlip = TChargFlip + '1.05'.ljust(45)
                          else:
                              TChargFlip = TChargFlip + '-'.ljust(45)
                      else:
                          ThLumi16 = ThLumi16 + '1.01'.ljust(45)
                          ThLumi17 = ThLumi17 + '1.02'.ljust(45)
                          ThLumi18 = ThLumi18 + '1.015'.ljust(45)
                          ThLumi16_161718 = ThLumi16_161718 + '1.006'.ljust(45)
                          ThLumi17_161718 = ThLumi17_161718 + '1.009'.ljust(45)
                          ThLumi18_161718 = ThLumi18_161718 + '1.02'.ljust(45)
                          ThLumi17_1718 = ThLumi17_1718 + '1.006'.ljust(45)
                          ThLumi18_1718 = ThLumi18_1718 + '1.002'.ljust(45)
                          TFake = TFake + '-'.ljust(45)
                          TChargFlip = TChargFlip + '-'.ljust(45)
                          if key=='Diboson':
                              TDiboson = TDiboson + '1.06'.ljust(45)
                          else:
                              TDiboson = TDiboson + '-'.ljust(45)
                          if key=='TTXTX':
                              TtXttX = TtXttX  + '1.15'.ljust(45)
                          else:
                              TtXttX = TtXttX  + '-'.ljust(45)
                          if key=='Conv':
                              Tconversion = Tconversion + '1.05'.ljust(45)
                          else:
                              Tconversion = Tconversion + '-'.ljust(45)
                if '2016' in nameyear:
                    T1 = T1 + ThLumi16 + '\n'
                    T1 = T1 + ThLumi16_161718 + '\n'
                if '2017' in nameyear:
                    T1 = T1 + ThLumi17 + '\n'
                    T1 = T1 + ThLumi17_161718 + '\n'
                    T1 = T1 + ThLumi17_1718 + '\n'
                if '2018' in nameyear:
                    T1 = T1 + ThLumi18 + '\n'
                    T1 = T1 + ThLumi18_161718 + '\n'
                    T1 = T1 + ThLumi18_1718 + '\n'
                T1 = T1 + TDiboson + '\n'
                T1 = T1 + TtXttX + '\n'
                T1 = T1 + Tconversion + '\n'
                T1 = T1 + TFake + '\n'
                T1 = T1 + TChargFlip + '\n'
                for numsys, namesys in enumerate(sys):
                    Tsys=namesys.ljust(27)  +'shape'.ljust(10)
                    for key, value in Integrals[nameyear][hist_key].iteritems():
                        if 'data' not in key:
                           if 'DD' in key:
                               Tsys=Tsys+'-'.ljust(25)
                           else:
                               Tsys=Tsys+'1'.ljust(25)
                    T1 = T1 + Tsys + '\n'
                for numsys, namesys in enumerate(sysThName):
                    Tsys=namesys.ljust(27)  +'shape'.ljust(10)
                    for key, value in Integrals[nameyear][hist_key].iteritems():
                        if 'data' not in key:
                           if 'DD' in key:
                               Tsys=Tsys+'-'.ljust(25)
                           else:
                               Tsys=Tsys+'1'.ljust(25)
                    T1 = T1 + Tsys + '\n'
                for numsys, namesys in enumerate(sysFA):
                    Tsys=namesys.ljust(27)  +'shape'.ljust(10)
                    for key, value in Integrals[nameyear][hist_key].iteritems():
                        if 'data' not in key:
                           if 'DD' in key:
                               Tsys=Tsys+'1'.ljust(25)
                           else:
                               Tsys=Tsys+'-'.ljust(25)
                    T1 = T1 + Tsys + '\n'
                T1 = T1 +'------------\n' 
                T1 = T1 + '* autoMCStats 10' + '\n'
                open('CombinedFilesFCNC_v2/' + cardName +'.txt', 'wt').write(T1)
