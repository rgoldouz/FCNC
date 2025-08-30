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
from ROOT import TFile
from ROOT import TGaxis
from ROOT import THStack
import gc
from operator import truediv
import copy
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

def EFTtoNormalNoWC(H):
    nbins = H.GetNbinsX()
    bin_edges = [H.GetBinLowEdge(i + 1) for i in range(nbins)]
    bin_edges.append(H.GetXaxis().GetBinUpEdge(nbins))
    bin_array = array.array('d', bin_edges)
    hpx = ROOT.TH1F(H.GetName(), H.GetName(), nbins, bin_array)
    r=1
    for b in range(hpx.GetNbinsX()+1):
        content = H.GetBinContentNoWC(b+1)
        if math.isnan(content):
            print  H.GetName()+"Bin content is NaN"
        if math.isinf(content):
            print  H.GetName()+"Bin content is inf"
        hpx.SetBinContent(b+1, H.GetBinContentNoWC(b+1))
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
        if n<len(c):
            h.SetLineColor(c[n])
        h.SetBinContent(h.GetXaxis().GetNbins(), h.GetBinContent(h.GetXaxis().GetNbins()) + h.GetBinContent(h.GetXaxis().GetNbins()+1))
        hist[s] = h

    return hist


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


def SumofWeight(add):
    genEventSumw = 0
    genEventSumwScale = [0]*9
    genEventSumwPdf = [0]*100
    for root, dirs, files in os.walk(add):
        if len(files) == 0:
            continue
        for f in files:
            filename = root + '/' + f
            if 'fail' in f:
                continue
            fi = TFile.Open(filename)
            tree_meta = fi.Get('Runs')
            for i in range( tree_meta.GetEntries() ):
                tree_meta.GetEntry(i)
                genEventSumw += tree_meta.genEventSumw
                for pdf in range(100):
                    genEventSumwPdf[pdf] += tree_meta.LHEPdfSumw[pdf]*tree_meta.genEventSumw
                for Q in range(len(tree_meta.LHEScaleSumw)):
                    genEventSumwScale[Q] += tree_meta.LHEScaleSumw[Q]*tree_meta.genEventSumw
            tree_meta.Reset()
            tree_meta.Delete()
            fi.Close()
    if genEventSumwScale[8]==0:
        del genEventSumwScale[8]
    return [genEventSumw/x for x in genEventSumwScale] , [genEventSumw/x for x in genEventSumwPdf]

HistAddress = '/afs/crc.nd.edu/user/r/rgoldouz/FCNC/NanoAnalysis/hists/'
year=['2016preVFP', '2016postVFP', '2017','2018']
ULyear=['UL16preVFP', 'UL16postVFP', 'UL17','UL18']
year=['2017']
ULyear=['UL17']
LumiErr = [0.018, 0.018, 0.018, 0.018]
regions=["1bLj","1bHj"]
channels=["2lss",  "3lonZ", "3loffZhigh"]
variables=["MVATU"]
#lep1Pt"]
sys = ["eleRecoIdIso","muRecoIdIso","triggerSF","pu","prefiring","bcTagSfCorr","LTagSfCorr","bcTagSfUnCorr","LTagSfUnCorr","LTagSfUnCorr","JetPuID", "JesFlavorQCD", "JesBBEC1", "JesAbsolute", "JesRelativeBal", "JesRelativeSample","Jer"]
HistAddress = '/users/rgoldouz/FCNC/NanoAnalysis/hists/'
Samples = ['data.root','Triboson.root', 'Diboson.root', 'ttbar.root', 'ST.root','DY.root', 'Conv.root','TTX.root','FCNCTUProduction.root','FCNCTUDecay.root']
SamplesName = ['Data','Triboson', 'Diboson', 't#bar{t}', 'Single top','DY', 'Conv','TTX+TX','FCNC-Production','FCNC-Decay']#
SamplesNameCombined = ['data_obs','Triboson', 'Diboson','tt','ST','DY', 'Conv','TTXTX','FCNC-Prod','FCNC-Dec']
colors =  [ROOT.kBlack,ROOT.kGreen,ROOT.kBlue+8,ROOT.kRed-4,ROOT.kOrange-3, ROOT.kCyan+1, ROOT.kYellow, ROOT.kMagenta-4,ROOT.kBlue, ROOT.kGray+1,ROOT.kGray+3,]
WCs=["ctp","ctlS","cte","ctl","ctlT","ctZ","cpt","cpQM","ctA","cQe","ctG","cQlM"]
#WCs=["cpQM","ctZ"]
channelsSys=["2lss", "3lonZ", "3loffZhigh"]
sys = ["eleRecoIdIso","muRecoIdIso","triggerSF","pu","prefiring","bcTagSfCorr","LTagSfCorr","bcTagSfUnCorr","LTagSfUnCorr","LTagSfUnCorr","JetPuID", "JesFlavorQCD", "JesBBEC1", "JesAbsolute", "JesRelativeBal", "JesRelativeSample","Jer"]
variablesSys=["MVATU"]
channelsFake=["2lss_LF", "2lss_FF", "3lonZ_LLF", "3lonZ_LFF","3lonZ_FFF","3loffZhigh_LLF", "3loffZhigh_LFF","3loffZhigh_FFF", "3loffZlow_LLF", "3loffZlow_LFF","3loffZlow_FFF"]
variablesFR=["MVATU"]
wc1 = ROOT.WCPoint("EFTrwgt1_cT_1_cS_0")
wcName = "cT"
print 'making combine files'

bins = array( 'd',[0.01,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,2,50] )
binsDic = {
'2l':array( 'd',[0.01,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,2,4,50] ),
'3lonZ':array( 'd',[0.01,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1.0,1.2,1.4,1.6,1.8,2,2.5,3,5.0,10.0,20.0,50.0] ),
'3loffZ':array( 'd',[0.01,0.1,0.2,0.3,0.6,1.0,2.0,5.0,50.0] ),
}

Hists = []
HistsSysUp = []
HistsSysDown = []
Hists_copy =[]
HistsFake = []
drawFakeRegions=True

for numyear, nameyear in enumerate(year):
    l0=[]
    copyl0=[]
    SysUpl0=[]
    SysDownl0=[]
    Files = []
    for f in range(len(Samples)):
        l1=[]
        copyl1=[]
        SysUpl1=[]
        SysDownl1=[]
        Files.append(ROOT.TFile.Open(HistAddress + nameyear+ '_' + Samples[f]))
        for numch, namech in enumerate(channels):
            l2=[]
            copyl2=[]
            SysUpl2=[]
            SysDownl2=[]
            for numreg, namereg in enumerate(regions):
                l3=[]
                copyl3=[]
                SysUpl3=[]
                SysDownl3=[]
                for numvar, namevar in enumerate(variables):
                    SysUpl4=[]
                    SysDownl4=[]
                    for key in binsDic:
                        if key in namech:
                            bins=binsDic[key]
                    h= Files[f].Get(namech + '_' + namereg + '_' + namevar)
                    l3.append(h)
                    #print Samples[f] + '-' + namech + '_' + namereg + '_' + namevar+ ':'+ str(h.Integral())
                    copyl3.append(h.Clone())
                    if f>0 and namech in channelsSys and namevar in variablesSys:
                        for numsys, namesys in enumerate(sys):
                            h= Files[f].Get(namech + '_' + namereg + '_' + namevar+ '_' + namesys+ '_Up')
                            SysUpl4.append(h)
                            h= Files[f].Get(namech + '_' + namereg + '_' + namevar+ '_' + namesys+ '_Down')
                            SysDownl4.append(h)
                    SysUpl3.append(SysUpl4)
                    SysDownl3.append(SysDownl4)
                l2.append(l3)
                copyl2.append(copyl3)
                SysUpl2.append(SysUpl3)
                SysDownl2.append(SysDownl3)
            l1.append(l2)
            copyl1.append(copyl2)
            SysUpl1.append(SysUpl2)
            SysDownl1.append(SysDownl2)
        l0.append(l1)
        copyl0.append(copyl1)
        SysUpl0.append(SysUpl1)
        SysDownl0.append(SysDownl1)
    Hists.append(l0)
    Hists_copy.append(copyl0)
    HistsSysUp.append(SysUpl0)
    HistsSysDown.append(SysDownl0)

for numyear, nameyear in enumerate(year):
    l0=[]
    Files = []
    for f in range(len(Samples)):
        l1=[]
        Files.append(ROOT.TFile.Open(HistAddress + nameyear+ '_' + Samples[f]))
        for numch, namech in enumerate(channelsFake):
            l2=[]
            for numreg, namereg in enumerate(regions):
                l3=[]
                for numvar, namevar in enumerate(variablesFR):
                    h= Files[f].Get(namech + '_' + namereg + '_' + namevar)
                    l3.append(h)
                l2.append(l3)
            l1.append(l2)
        l0.append(l1)
    HistsFake.append(l0)


if not os.path.exists('CombinedFilesFCNC'):
    os.makedirs('CombinedFilesFCNC')
else:
    os.system('rm -rf CombinedFilesFCNC/'+ wcName +'_*')

processes=[]
Integrals=[]
nuisances={}
F=ROOT.TFile.Open(HistAddress + nameyear+ '_' + Samples[0])
for numyear, nameyear in enumerate(year):
    HL1=[]
    HI1=[]
    for numch, namech in enumerate(channels):
        HL2=[]
        HI2=[]
        for key in binsDic:
             if key in namech:
                 bins=binsDic[key]        
        for numreg, namereg in enumerate(regions):
            HL3=[]
            HI3=[]
            #first write the observed data hist
            hfile = ROOT.TFile( 'CombinedFilesFCNC/' +  nameyear+'_'+namech+'_'+namereg+'.root', 'RECREATE', 'combine input histograms' )
            hNormal = EFTtoNormal(Hists[numyear][0][numch][numreg][0],wc1)
            hNormal =hNormal.Rebin(len(bins)-1,"",bins)
            hNormal.SetName(SamplesNameCombined[0])
            hNormal.Write()
            #Then write the fakes
            if '2l' in namech:
                hNormal=EFTtoNormal(HistsFake[numyear][0][channelsFake.index('2lss_LF')][numreg][numvar],wc1)
                hNormal =hNormal.Rebin(len(bins)-1,"",bins)
                hNormal2=EFTtoNormal(HistsFake[numyear][0][channelsFake.index('2lss_FF')][numreg][numvar],wc1)
                hNormal2 =hNormal2.Rebin(len(bins)-1,"",bins)
                hNormal.Add(hNormal2,-1)
                for b in range(hNormal.GetNbinsX()):
                    if hNormal.GetBinContent(b+1)<=0:
                        hNormal.SetBinContent(b+1,0.00001)
                        hNormal.SetBinError(b+1,0.0)
                hNormal.SetName("DD_Fake")
                hNormal.Write()
                HL3.append(["DD_Fake"]) 
                HI3.append([hNormal.Integral()])
            if '3lonZ' in namech:
                hNormal=EFTtoNormal(HistsFake[numyear][0][channelsFake.index('3lonZ_LLF')][numreg][numvar],wc1)
                hNormal =hNormal.Rebin(len(bins)-1,"",bins)
                hNormal2=EFTtoNormal(HistsFake[numyear][0][channelsFake.index('3lonZ_LFF')][numreg][numvar],wc1)
                hNormal2 =hNormal2.Rebin(len(bins)-1,"",bins)
                hNormal3=EFTtoNormal(HistsFake[numyear][0][channelsFake.index('3lonZ_FFF')][numreg][numvar],wc1)
                hNormal3 =hNormal2.Rebin(len(bins)-1,"",bins)
                hNormal.Add(hNormal2,-1)
                hNormal.Add(hNormal3,1)
                for b in range(hNormal.GetNbinsX()):
                    if hNormal.GetBinContent(b+1)<=0:
                        hNormal.SetBinContent(b+1,0.00001)
                        hNormal.SetBinError(b+1,0.0)
                hNormal.SetName("DD_Fake")
                hNormal.Write()
                HL3.append(["DD_Fake"])
                HI3.append([hNormal.Integral()])
            if '3loffZhigh' in namech:
                hNormal=EFTtoNormal(HistsFake[numyear][0][channelsFake.index('3loffZhigh_LLF')][numreg][numvar],wc1)
                hNormal =hNormal.Rebin(len(bins)-1,"",bins)
                hNormal2=EFTtoNormal(HistsFake[numyear][0][channelsFake.index('3loffZhigh_LFF')][numreg][numvar],wc1)
                hNormal2 =hNormal2.Rebin(len(bins)-1,"",bins)
                hNormal3=EFTtoNormal(HistsFake[numyear][0][channelsFake.index('3loffZhigh_FFF')][numreg][numvar],wc1)
                hNormal3 =hNormal2.Rebin(len(bins)-1,"",bins)
                hNormal.Add(hNormal2,-1)
                hNormal.Add(hNormal3,1)
                for b in range(hNormal.GetNbinsX()):
                    if hNormal.GetBinContent(b+1)<=0:
                        hNormal.SetBinContent(b+1,0.00001)
                        hNormal.SetBinError(b+1,0.0)
                hNormal.SetName("DD_Fake")
                hNormal.Write()
                HL3.append(["DD_Fake"])
                HI3.append([hNormal.Integral()])
            #write charged flip
            if '2l' in namech:
                hNormal= EFTtoNormal(F.Get('2los_Weighted' + '_' + namereg + '_' + namevar),wc1)
                for b in range(hNormal.GetNbinsX()):
                    if hNormal.GetBinContent(b+1)<=0:
                        hNormal.SetBinContent(b+1,0.00001)
                        hNormal.SetBinError(b+1,0.0)
                hNormal.SetName("DD_chargeFlip")
                hNormal.Write()
                HL3.append(["DD_chargeFlip"])
                HI3.append([hNormal.Integral()])
            for f in range(1,len(Samples)):
                HL4=[]
                HI4=[]
                if 'FCNC' not in SamplesNameCombined[f]:
                    hNormal = EFTtoNormal(Hists[numyear][f][numch][numreg][0],wc1)
                    hNormal =hNormal.Rebin(len(bins)-1,"",bins)
                    for b in range(hNormal.GetNbinsX()):
                        if hNormal.GetBinContent(b+1)<=0:
                            hNormal.SetBinContent(b+1,0.00001)
                            hNormal.SetBinError(b+1,0.0)
                    hNormal.SetName(SamplesNameCombined[f])
                    hNormal.Write()
                    HL4.append(SamplesNameCombined[f])
                    HI4.append(hNormal.Integral())                        
                    if f>0 and namech in channelsSys and namevar in variablesSys:
                        for numsys, namesys in enumerate(sys):
                            hNormal = EFTtoNormal(HistsSysUp[numyear][f][numch][numreg][0][numsys],wc1)
                            hNormal =hNormal.Rebin(len(bins)-1,"",bins)
                            for b in range(hNormal.GetNbinsX()):
                                if hNormal.GetBinContent(b+1)<=0:
                                    hNormal.SetBinContent(b+1,0.00001)
                                    hNormal.SetBinError(b+1,0.0)
                            hNormal.SetName(SamplesNameCombined[f]+'_'+namesys+'Up')
                            hNormal.Write()
                            hNormal = EFTtoNormal(HistsSysDown[numyear][f][numch][numreg][0][numsys],wc1)
                            hNormal =hNormal.Rebin(len(bins)-1,"",bins)
                            for b in range(hNormal.GetNbinsX()):
                                if hNormal.GetBinContent(b+1)<=0:
                                    hNormal.SetBinContent(b+1,0.00001)
                                    hNormal.SetBinError(b+1,0.0)
                            hNormal.SetName(SamplesNameCombined[f]+'_'+namesys+'Down')
                            hNormal.Write()
                else:
                    Hists[numyear][f][numch][numreg][0].GetSumFit().save(Samples[f]+namech+'tex')
                    SignalH=AnalyticAnomalousCoupling(Hists[numyear][f][numch][numreg][0],WCs,SamplesNameCombined[f])       
                    for H in SignalH:
                        H=H.Rebin(len(bins)-1,"",bins)
                        for b in range(H.GetNbinsX()):
                            if H.GetBinContent(b+1)<=0:
                                H.SetBinContent(b+1,0.00001)
                                H.SetBinError(b+1,0.0)
                        H.Write()             
                        HL4.append(H.GetName())
                        HI4.append(H.Integral())
                    if f>0 and namech in channelsSys and namevar in variablesSys:
                        for numsys, namesys in enumerate(sys):
                            SignalH=AnalyticAnomalousCoupling(HistsSysUp[numyear][f][numch][numreg][0][numsys],WCs,SamplesNameCombined[f])
                            for H in SignalH:
                                H=H.Rebin(len(bins)-1,"",bins)
                                for b in range(H.GetNbinsX()):
                                    if H.GetBinContent(b+1)<=0:
                                        H.SetBinContent(b+1,0.00001)
                                        H.SetBinError(b+1,0.0)
                                H.SetName(H.GetName()+'_'+namesys+'Up')
                                H.Write()
                            SignalH=AnalyticAnomalousCoupling(HistsSysDown[numyear][f][numch][numreg][0][numsys],WCs,SamplesNameCombined[f])
                            for H in SignalH:
                                H=H.Rebin(len(bins)-1,"",bins)
                                for b in range(H.GetNbinsX()):
                                    if H.GetBinContent(b+1)<=0:
                                        H.SetBinContent(b+1,0.00001)
                                        H.SetBinError(b+1,0.0)
                                H.SetName(H.GetName()+'_'+namesys+'Down')
                                H.Write()
                HL3.append(HL4)
                HI3.append(HI4)
            HL2.append(HL3)
            HI2.append(HI3)
            hfile.Write()
            hfile.Close()
            os.system('mv CombinedFilesFCNC/'+nameyear+'_'+namech+'_'+namereg+'.root CombinedFilesFCNC/org.root')
            f1 = ROOT.TFile.Open('CombinedFilesFCNC/org.root',"READ")
            hfile = ROOT.TFile( 'CombinedFilesFCNC/' + nameyear+'_'+namech+'_'+namereg+'.root', 'RECREATE', 'combine input histograms' )
            my_list = f1.GetListOfKeys()
            for obj in my_list: # obj is TKey
                if obj.GetClassName() == "TH1F":
                    RF = f1.Get(obj.GetName())
                    RF.SetName(obj.GetName())
                   # RF= RF.Rebin(len(bins)-1,"",bins)
                   # for b in range(RF.GetNbinsX()):
                   #     if RF.GetBinContent(b+1)<=0:
                   #         RF.SetBinContent(b+1,0.00001)
                   # print bins
                   # print str(RF.GetNbinsX())
                  #  print obj.GetName() +":"+ str(RF.Integral())
                    hfile.WriteObject(RF, RF.GetName())
            f1.Close()
            os.system('rm CombinedFilesFCNC/org.root')
            hfile.Write()
            hfile.Close()
        HL1.append(HL2)
        HI1.append(HI2)
    processes.append(HL1)
    Integrals.append(HI1)

for numyear, nameyear in enumerate(year):
    for numch, namech in enumerate(channels):
        for numreg, namereg in enumerate(regions):
            cardName = 'C'+namech+'_'+nameyear+'_' + namereg
            T1 = 'max 1 number of categories \n' +\
                 'jmax * number of samples minus one\n' +\
                 'kmax * number of nuisance parameters\n' +\
                 '------------\n'+\
                 'shapes * * '  + nameyear+'_'+namech+'_'+namereg+'.root' + ' $PROCESS $PROCESS_$SYSTEMATIC\n' +\
                 '------------\n'+\
                 'bin'.ljust(45) + cardName + '\n'+\
                 'observation'.ljust(45) + str(Hists[numyear][0][numch][numreg][0].Integral()) +'\n'+\
                 '------------\n'
            T1 = T1 +'bin'.ljust(45)
            for i in range(len(processes[numyear][numch][numreg])):
                for j in range(len(processes[numyear][numch][numreg][i])):
                    T1 = T1 + cardName.ljust(45)
            T1 = T1 + '\n'
            T1 = T1 +'process'.ljust(45)
            c=1
            l=0
            for i in range(len(processes[numyear][numch][numreg])):
                for j in range(len(processes[numyear][numch][numreg][i])):
                    if 'FCNC' in processes[numyear][numch][numreg][i][j]:
                        print str(l).ljust(45) + processes[numyear][numch][numreg][i][j].ljust(45)+str(Integrals[numyear][numch][numreg][i][j]).ljust(45)
                        T1 = T1 + str(l).ljust(45)
                        l=l-1                         
                    else:
                        T1 = T1 + str(c).ljust(45)
                        c=c+1
            T1 = T1 + '\n'
            T1 = T1 +'process'.ljust(45)
            for i in range(len(processes[numyear][numch][numreg])):
                for j in range(len(processes[numyear][numch][numreg][i])):
                    T1 = T1 + processes[numyear][numch][numreg][i][j].ljust(45)
            T1 = T1 + '\n'
            T1 = T1 +'rate'.ljust(45)
            for i in range(len(processes[numyear][numch][numreg])):
                for j in range(len(processes[numyear][numch][numreg][i])):
                    T1 = T1 + str(Integrals[numyear][numch][numreg][i][j]).ljust(45)
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
            TChargFlip= 'ChargFlip_norm'.ljust(35)+'lnN'.ljust(10)
            
            for i in range(len(processes[numyear][numch][numreg])):
              for j in range(len(processes[numyear][numch][numreg][i])):
                  if 'DD' in processes[numyear][numch][numreg][i][j]:
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
                      if processes[numyear][numch][numreg][i][j]=='DD_Fake':
                          TFake = TFake + '1.1'.ljust(45)
                      else:
                          TFake = TFake + '-'.ljust(45)
                      if processes[numyear][numch][numreg][i][j]=='DD_ChargeFlip':
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
                      if processes[numyear][numch][numreg][i][j]=='Diboson':
                          TDiboson = TDiboson + '1.06'.ljust(45)
                      else:
                          TDiboson = TDiboson + '-'.ljust(45)
                      if processes[numyear][numch][numreg][i][j]=='TTXTX':
                          TtXttX = TtXttX  + '1.15'.ljust(45)
                      else:
                          TtXttX = TtXttX  + '-'.ljust(45)
                      if processes[numyear][numch][numreg][i][j]=='Conv':
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
                for i in range(len(processes[numyear][numch][numreg])):
                   for j in range(len(processes[numyear][numch][numreg][i])):

                       Tsys=Tsys+'1'.ljust(25)
                T1 = T1 + Tsys + '\n'
            T1 = T1 +'------------\n' 
#                  'bin'.ljust(45) + cardName.ljust(40) + cardName.ljust(40) + cardName.ljust(40) + cardName.ljust(40) + cardName.ljust(40) + cardName.ljust(40) +'\n'+\
#                  
#                  'process'.ljust(45) +'-1'.ljust(40) +'0'.ljust(40) + '1'.ljust(40) + '2'.ljust(40) + '3'.ljust(40) + '4'.ljust(40) +'\n'+\
#                  'process'.ljust(45) +valueD[0].ljust(40) +valueD[1].ljust(40)+ SamplesNameCombined[1].ljust(40) + SamplesNameCombined[2].ljust(40) +\
#                  SamplesNameCombined[3].ljust(40) + SamplesNameCombined[4].ljust(40) +'\n'+\
#                  'rate'.ljust(45) + str(Hists[numyear][Sid0][numch][numreg][0].Integral()*scaleSignal).ljust(40) + str(Hists[numyear][Sid1][numch][numreg][0].Integral()*scaleSignal).ljust(40) + str(Hists[numyear][1][numch][numreg][0].Integral()).ljust(40) + str(Hists[numyear][2][numch][numreg][0].Integral()).ljust(40)+\
#                  str(Hists[numyear][3][numch][numreg][0].Integral()).ljust(40) + str(Hists[numyear][4][numch][numreg][0].Integral()).ljust(40) + '\n'+\
#                  '------------\n'+\
#                  'Other_norm'.ljust(35)+'lnN'.ljust(10) + '-'.ljust(40) + '-'.ljust(40)  + '1.5'.ljust(40) + '-'.ljust(40) + '-'.ljust(40) + '-'.ljust(40) +'\n'+\
#                  'DY_norm'.ljust(35)+'lnN'.ljust(10) + '-'.ljust(40) + '-'.ljust(40) + '-'.ljust(40) + '1.3'.ljust(40) + '-'.ljust(40) + '-'.ljust(40) +'\n'+\
#                  'tt_norm'.ljust(35)+'lnN'.ljust(10) + '-'.ljust(40) + '-'.ljust(40) + '-'.ljust(40) + '-'.ljust(40) + '1.05'.ljust(40) + '-'.ljust(40) +'\n'+\
#                  'tW_norm'.ljust(35)+'lnN'.ljust(10) + '-'.ljust(40) + '-'.ljust(40) + '-'.ljust(40) + '-'.ljust(40) + '-'.ljust(40) + '1.1'.ljust(40) +'\n'+\
#                  'MuIDSF'.ljust(35)+'lnN'.ljust(10) + '1.01'.ljust(40) + '1.01'.ljust(40) + '1.01'.ljust(40) + '1.01'.ljust(40) + '1.01'.ljust(40) + '1.01'.ljust(40) +'\n'
#             if '2016' in nameyear:
#                 T1 = T1 + 'lumi2016'.ljust(35)+'lnN'.ljust(10) + '1.01'.ljust(40) + '1.01'.ljust(40) + '1.01'.ljust(40) + '1.01'.ljust(40) + '1.01'.ljust(40) + '1.01'.ljust(40) +'\n'    
#                 T1 = T1 + 'lumiCorr16-17-18'.ljust(35)+'lnN'.ljust(10) + '1.006'.ljust(40) + '1.006'.ljust(40) + '1.006'.ljust(40) + '1.006'.ljust(40) + '1.006'.ljust(40) + '1.006'.ljust(40) +'\n'
#                 T1 = T1 + 'DY_METmodel2016'.ljust(35)+'lnN'.ljust(10) + '-'.ljust(40) + '-'.ljust(40) + '-'.ljust(40) + '1.2'.ljust(40) + '-'.ljust(40) + '-'.ljust(40) +'\n'
#             if '2017' in nameyear:
#                 T1 = T1 + 'lumi2017'.ljust(35)+'lnN'.ljust(10) + '1.02'.ljust(40) + '1.02'.ljust(40) + '1.02'.ljust(40) + '1.02'.ljust(40) + '1.02'.ljust(40) + '1.02'.ljust(40) +'\n'
#                 T1 = T1 + 'lumiCorr16-17-18'.ljust(35)+'lnN'.ljust(10) + '1.009'.ljust(40) + '1.009'.ljust(40) + '1.009'.ljust(40) + '1.009'.ljust(40) + '1.009'.ljust(40) + '1.009'.ljust(40) +'\n'
#                 T1 = T1 + 'lumiCorr17-18'.ljust(35)+'lnN'.ljust(10) + '1.006'.ljust(40) + '1.006'.ljust(40) + '1.006'.ljust(40) + '1.006'.ljust(40) + '1.006'.ljust(40) + '1.006'.ljust(40) +'\n'
#                 T1 = T1 + 'DY_METmodel2017'.ljust(35)+'lnN'.ljust(10) + '-'.ljust(40) + '-'.ljust(40) + '-'.ljust(40) + '1.2'.ljust(40) + '-'.ljust(40) + '-'.ljust(40) +'\n'
#             if '2018' in nameyear:
#                 T1 = T1 + 'lumi2018'.ljust(35)+'lnN'.ljust(10) + '1.015'.ljust(40) + '1.015'.ljust(40) + '1.015'.ljust(40) + '1.015'.ljust(40) + '1.015'.ljust(40) + '1.015'.ljust(40) +'\n'
#                 T1 = T1 + 'lumiCorr16-17-18'.ljust(35)+'lnN'.ljust(10) + '1.02'.ljust(40) + '1.02'.ljust(40) + '1.02'.ljust(40) + '1.02'.ljust(40) + '1.02'.ljust(40) + '1.02'.ljust(40) +'\n'
#                 T1 = T1 + 'lumiCorr17-18'.ljust(35)+'lnN'.ljust(10) + '1.002'.ljust(40) + '1.002'.ljust(40) + '1.002'.ljust(40) + '1.002'.ljust(40) + '1.002'.ljust(40) + '1.002'.ljust(40) +'\n'
#                 T1 = T1 + 'DY_METmodel2018'.ljust(35)+'lnN'.ljust(10) + '-'.ljust(40) + '-'.ljust(40) + '-'.ljust(40) + '2.0'.ljust(40) + '-'.ljust(40) + '-'.ljust(40) +'\n'
#             if 'Mu' in namesig:
#                 T1 = T1 + 'MuTtDyDiff'.ljust(35)+'lnN'.ljust(10) + '1.005'.ljust(40) + '1.005'.ljust(40) + '1.005'.ljust(40) + '1.005'.ljust(40) + '1.005'.ljust(40) + '1.005'.ljust(40) +'\n'
#             else:
#                 T1 = T1 + 'EleTtDyDiff'.ljust(35)+'lnN'.ljust(10) + '1.01'.ljust(40) + '1.01'.ljust(40) + '1.01'.ljust(40) + '1.01'.ljust(40) + '1.01'.ljust(40) + '1.01'.ljust(40) +'\n'
#             for numsys, namesys in enumerate(sysJecNamesCorr):
#                 T1 = T1 +  'jes' + namesys.ljust(32)  +'shape'.ljust(10)  + '1'.ljust(40) +  '1'.ljust(40) + '1'.ljust(40) + '1'.ljust(40) + '1'.ljust(40) + '1'.ljust(40) +'\n'
#             for numsys, namesys in enumerate(sysJecNamesUnCorr):
#                 T1 = T1 + 'Y'+  nameyear + 'jes' + namesys.ljust(27)  +'shape'.ljust(10)  + '1'.ljust(40) + '1'.ljust(40) + '1'.ljust(40) + '1'.ljust(40) + '1'.ljust(40) + '1'.ljust(40) +'\n'
#             for b in sys:
#                 if 'jer' in b or 'unclusMET' in b or 'UnCorr' in b or 'topPt' in b or "muonScale" in b or "muonRes" in b:
#                     continue 
#                 T1 = T1 +  b.ljust(35)  +'shape'.ljust(10)  + '1'.ljust(40) + '1'.ljust(40)  + '1'.ljust(40) + '1'.ljust(40) + '1'.ljust(40) + '1'.ljust(40) +'\n'
#             T1 = T1 +  'muonScale'.ljust(35)  +'shape'.ljust(10)  + '-'.ljust(40) + '-'.ljust(40)  + '1'.ljust(40) + '1'.ljust(40) + '1'.ljust(40) + '1'.ljust(40) +'\n'
#             T1 = T1 +  'muonRes'.ljust(35)  +'shape'.ljust(10)  + '-'.ljust(40) + '-'.ljust(40)  + '1'.ljust(40) + '1'.ljust(40) + '1'.ljust(40) + '1'.ljust(40) +'\n'
#             T1 = T1 +  'topPt'.ljust(35)  +'shape'.ljust(10)  + '-'.ljust(40) + '-'.ljust(40)  + '-'.ljust(40) + '-'.ljust(40) + '1'.ljust(40) + '-'.ljust(40) +'\n'
#             T1 = T1 + 'Y'+ nameyear + 'unclusMET'.ljust(30)  +'shape'.ljust(10)  + '1'.ljust(40) + '1'.ljust(40) + '1'.ljust(40) + '1'.ljust(40) + '1'.ljust(40) + '1'.ljust(40) +'\n'
#             T1 = T1 + 'Y'+ nameyear + 'bcTagSfUnCorr'.ljust(30)  +'shape'.ljust(10)  + '1'.ljust(40) + '1'.ljust(40) + '1'.ljust(40) + '1'.ljust(40) + '1'.ljust(40) + '1'.ljust(40) +'\n'
#             T1 = T1 + 'Y'+ nameyear + 'LTagSfUnCorr'.ljust(30)  +'shape'.ljust(10)  + '1'.ljust(40) + '1'.ljust(40) + '1'.ljust(40) + '1'.ljust(40) + '1'.ljust(40) + '1'.ljust(40) +'\n'
#             T1 = T1 + 'Y'+ nameyear + 'jer'.ljust(30)  +'shape'.ljust(10)  + '1'.ljust(40) + '1'.ljust(40) + '1'.ljust(40) + '1'.ljust(40) + '1'.ljust(40) + '1'.ljust(40) +'\n'
#             T1 = T1 +  'pdf'.ljust(35)  +'shape'.ljust(10)  + '1'.ljust(40) + '1'.ljust(40) + '-'.ljust(40) + '-'.ljust(40) + '1'.ljust(40) + '-'.ljust(40) +'\n'
#             bpb= 'tt_QS'
#             T1 = T1 +  bpb.ljust(35)  +'shape'.ljust(10)  + '-'.ljust(40) + '1'.ljust(40) + '-'.ljust(40) + '-'.ljust(40) + '1'.ljust(40) + '-'.ljust(40) +'\n'                    
#             bpb= 'tt_ISR'
#             T1 = T1 +  bpb.ljust(35)  +'shape'.ljust(10)  + '-'.ljust(40) + '1'.ljust(40) + '-'.ljust(40) + '-'.ljust(40) + '1'.ljust(40) + '-'.ljust(40) +'\n'
#             for b in ttSysOther:
#                 bpb= 'tt_' + b
#                 T1 = T1 +  bpb.ljust(35)  +'shape'.ljust(10)  + '-'.ljust(40) + '-'.ljust(40) + '-'.ljust(40) + '-'.ljust(40) + '1'.ljust(40) + '-'.ljust(40) +'\n'
#             for b in ttsysCR:
#                 bpb= 'tt_' + b
#                 T1 = T1 +  bpb.ljust(35)  +'shape'.ljust(10)  + '-'.ljust(40) + '-'.ljust(40) + '-'.ljust(40) + '-'.ljust(40) + '1'.ljust(40) + '-'.ljust(40) +'\n'
#             T1 = T1 + 'FSR'.ljust(35)+'shape'.ljust(10) + '1'.ljust(40) + '1'.ljust(40) + '-'.ljust(40) + '-'.ljust(40) + '1'.ljust(40) + '-'.ljust(40) +'\n'
#             T1 = T1 + 'Signal_ISR'.ljust(35)+'shape'.ljust(10) + '1'.ljust(40) + '-'.ljust(40) + '-'.ljust(40) + '-'.ljust(40) + '-'.ljust(40) + '-'.ljust(40) +'\n'
#             bpb= 'Signal_QS' 
#             T1 = T1 +  bpb.ljust(35)  +'shape'.ljust(10)  + '1'.ljust(40) + '-'.ljust(40) + '-'.ljust(40) + '-'.ljust(40) + '-'.ljust(40) + '-'.ljust(40) +'\n'
            T1 = T1 + '* autoMCStats 10' + '\n'
            open('CombinedFilesFCNC/' + cardName +'.txt', 'wt').write(T1)
#    
#    
#    
    



