#define MyAnalysis_cxx
#include "MyAnalysis.h"
#include "objectSelection.h"
#include "genLevelAnalysis.h"
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>
#include "PU_reWeighting.h"
#include "sumOfWeights.h"
#include "sumOfWeightsSignal.h"
#include "lepton_candidate.h"
#include "jet_candidate.h"
#include "JigsawRecTZFCNC.h"
#include "JigsawRecTHFCNC.h"
#include "LumiMask.h"
#include "TRandom.h"
#include "TRandom3.h"
#include "TDirectory.h"
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <TRandom3.h>
#include <TLorentzVector.h>
#include <time.h>
#include <cstdio>
#include <iostream>
#include <cmath>
#include <vector>
#include "RoccoR.h"
#include "BTagCalibrationStandalone.h"
#if not defined(__CINT__) || defined(__MAKECINT__)
#include "TMVA/Tools.h"
#include "TMVA/Reader.h"
#include "TMVA/MethodCuts.h"
#include "CondFormats/Serialization/interface/Archive.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectorParameters.h"
#include "CondFormats/JetMETObjects/interface/JetCorrectionUncertainty.h"
//#include "Archive.h"
//#include "JetCorrectorParameters.h"
//#include "JetCorrectionUncertainty.h"
#include "GEScaleSyst.h"
#include "Utils.h"
#include "correction.h"
#include "WCPoint.h"
#include "WCFit.h"
#include "TH1EFT.h"
#include <map>
#include "sys/types.h"
#include "sys/sysinfo.h"
#include "stdlib.h"
#include "stdio.h"
#include "string.h"
#include <regex>
#endif

#define COMPILER (!defined(__CINT__) && !defined(__CLING__))
#if defined(__MAKECINT__) || defined(__ROOTCLING__) || COMPILER
#include "RestFrames/RestFrames.hh"
#else
RestFrames::RFKey ensure_autoload(1);
#endif
using namespace RestFrames;

using namespace correction;
using namespace std;

/*
void example_Zll(const std::string& output_name = "output_Zll.root"){

  double mZ = 91.188; // GeV, PDG 2016
  double wZ = 2.495;

  // Number of events to generate
  int Ngen = 100000;

  /////////////////////////////////////////////////////////////////////////////////////////
  g_Log << LogInfo << "Initializing generator frames and tree..." << LogEnd;
  /////////////////////////////////////////////////////////////////////////////////////////
  LabGenFrame       LAB_Gen("LAB_Gen","LAB");
  ResonanceGenFrame Z_Gen("Z_Gen","Z");
  VisibleGenFrame   Lp_Gen("Lp_Gen","#it{l}^{+}");
  VisibleGenFrame   Lm_Gen("Lm_Gen","#it{l}^{-}");

  //-//-//-//-//-//-//-//-//-//-//-//-//-//-//-//-//-//-//-//-//-//-//-//-//-//-//-//-//-//

  LAB_Gen.SetChildFrame(Z_Gen);
  Z_Gen.AddChildFrame(Lp_Gen);
  Z_Gen.AddChildFrame(Lm_Gen);

  if(LAB_Gen.InitializeTree())
    g_Log << LogInfo << "...Successfully initialized generator tree" << LogEnd;
  else
    g_Log << LogError << "...Failed initializing generator tree" << LogEnd;

  //-//-//-//-//-//-//-//-//-//-//-//-//-//-//-//-//-//-//-//-//-//-//-//-//-//-//-//-//-//

  // Set Z pole mass and width
  Z_Gen.SetMass(mZ);                   Z_Gen.SetWidth(wZ);

  // set lepton pT and eta cuts
  Lp_Gen.SetPtCut(15.);                 Lp_Gen.SetEtaCut(2.5);
  Lm_Gen.SetPtCut(15.);                 Lm_Gen.SetEtaCut(2.5);

  if(LAB_Gen.InitializeAnalysis())
    g_Log << LogInfo << "...Successfully initialized generator analysis" << std::endl << LogEnd;
  else
    g_Log << LogError << "...Failed initializing generator analysis" << LogEnd;
  /////////////////////////////////////////////////////////////////////////////////////////
  /////////////////////////////////////////////////////////////////////////////////////////

  /////////////////////////////////////////////////////////////////////////////////////////
  g_Log << LogInfo << "Initializing reconstruction frames and trees..." << LogEnd;
  /////////////////////////////////////////////////////////////////////////////////////////
  LabRecoFrame     LAB("LAB","LAB");
  DecayRecoFrame   Z("Z","Z");
  VisibleRecoFrame Lp("Lp","#it{l}^{+}");
  VisibleRecoFrame Lm("Lm","#it{l}^{-}");

  //-//-//-//-//-//-//-//-//-//-//-//-//-//-//-//-//-//-//-//-//-//-//-//-//-//-//-//-//-//

  LAB.SetChildFrame(Z);
  Z.AddChildFrame(Lp);
  Z.AddChildFrame(Lm);
  if(LAB.InitializeTree())
    g_Log << LogInfo << "...Successfully initialized reconstruction trees" << LogEnd;
  else
    g_Log << LogError << "...Failed initializing reconstruction trees" << LogEnd;

  if(LAB.InitializeAnalysis())
    g_Log << LogInfo << "...Successfully initialized analyses" << LogEnd;
  else
    g_Log << LogError << "...Failed initializing analyses" << LogEnd;

  /////////////////////////////////////////////////////////////////////////////////////////
  /////////////////////////////////////////////////////////////////////////////////////////

  TreePlot* tree_plot = new TreePlot("TreePlot","TreePlot");

  // generator tree
  tree_plot->SetTree(LAB_Gen);
  tree_plot->Draw("GenTree", "Generator Tree", true);

  // reco tree
  tree_plot->SetTree(LAB);
  tree_plot->Draw("RecoTree", "Reconstruction Tree");

  //-//-//-//-//-//-//-//-//-//-//-//-//-//-//-//-//-//-//-//-//-//-//-//-//-//-//-//-//-//

  // Declare observables for histogram booking
  HistPlot* hist_plot = new HistPlot("HistPlot","Z #rightarrow #it{l}^{+} #it{l}^{-}");

  const HistPlotVar& MZ     = hist_plot->GetNewVar("MZ", "M_{Z}", 70., 110., "[GeV]");
  const HistPlotVar& cosZ   = hist_plot->GetNewVar("cosZ","cos #theta_{Z}", -1., 1.);
  const HistPlotVar& dphiZ  = hist_plot->GetNewVar("dphiZ", "#Delta #phi_{Z}", 0., 2.*acos(-1.));

  hist_plot->AddPlot(MZ);
  hist_plot->AddPlot(cosZ);
  hist_plot->AddPlot(dphiZ);
  hist_plot->AddPlot(cosZ, MZ);

  for(int igen = 0; igen < Ngen; igen++){
    if(igen%((std::max(Ngen,10))/10) == 0)
      g_Log << LogInfo << "Generating event " << igen << " of " << Ngen << LogEnd;

    // generate event
    LAB_Gen.ClearEvent();                             // clear the gen tree

    double PTZ = mZ*gRandom->Rndm();
    LAB_Gen.SetTransverseMomentum(PTZ);               // give the Z some Pt
    double PzZ = mZ*(2.*gRandom->Rndm()-1.);
    LAB_Gen.SetLongitudinalMomentum(PzZ);             // give the Z some Pz

    LAB_Gen.AnalyzeEvent();                           // generate a new event

    // analyze event
    LAB.ClearEvent();                                 // clear the reco tree

    Lp.SetLabFrameFourVector(Lp_Gen.GetFourVector(), 1); // Set lepton 4-vec and charge
    Lm.SetLabFrameFourVector(Lm_Gen.GetFourVector(),-1); // Set lepton 4-vec and charge

    LAB.AnalyzeEvent();                               // analyze the event

    // calculate observables
    MZ    = Z.GetMass();
    cosZ  = Z.GetCosDecayAngle();
    dphiZ = LAB.GetDeltaPhiDecayPlanes(Z);

    hist_plot->Fill();
  }

  hist_plot->Draw();

  TFile fout(output_name.c_str(),"RECREATE");
  fout.Close();
  hist_plot->WriteOutput(output_name);
  hist_plot->WriteHist(output_name);
  tree_plot->WriteOutput(output_name);

}
*/
void resetVecInt(std::vector<int> &K){
  for (int i=0;i<K.size();++i){
    K[i]=-1;
  }
}

void resetVecIntofInt(std::vector<std::vector<int>> &K){
  for (int i=0;i<K.size();++i){
    for (int j=0;j<K[i].size();++j){
      K[i][j]=-1;
    }
  }
}

void resetVecFloat(std::vector<float> &K){
  for (int i=0;i<K.size();++i){
    K[i]=0;
  }
}

void resetVecFloatOfFloat(std::vector<std::vector<float>> &K){
  for (int i=0;i<K.size();++i){
    for (int j=0;j<K[i].size();++j){
      K[i][j]=0;
    }
  }
}


int parseLine(char* line){
    // This assumes that a digit will be found and the line ends in " Kb".
    int i = strlen(line);
    const char* p = line;
    while (*p <'0' || *p > '9') p++;
    line[i-3] = '\0';
    i = atoi(p);
    return i;
}

int getValue(){ //Note: this value is in KB!
    FILE* file = fopen("/proc/self/status", "r");
    int result = -1;
    char line[128];

    while (fgets(line, 128, file) != NULL){
        if (strncmp(line, "VmRSS:", 6) == 0){
            result = parseLine(line);
            break;
        }
    }
    fclose(file);
    return result;
}

float topPtPowheg(float pt){
  return (0.973 - (0.000134 * pt) + (0.103 * exp(pt * (-0.0118))));
}

float topPtMGLO(float x){
  return (0.688 -  0.0000174*x + 0.824*exp(-0.0000253*x)/(pow(x,0.2185)));
}


bool ifSysNeeded(std::vector<lepton_candidate*> *lep, float cut){
  bool pass=false;
  if (lep->size()==2){
    if(((*lep)[0]->p4_ + (*lep)[1]->p4_).M()> cut) pass=true;
  }
  return pass;
}     


int getVecPos(std::vector<TString> vec, string element){
    int i;
    for(i = 0; i < vec.size(); i++){
        if(vec[i] == element){
            break;
        }
    }
    if(i == vec.size()){
        std::cout<<"No such element as "<<element<<" found. Please enter again: ";
        std::cin>>element;
        i = getVecPos(vec, element);
    }

    return i;
}

void MyAnalysis::Loop(TString fname, TString data, TString dataset ,string year, TString Run, float xs, float lumi, float Nevent, int iseft, int nRuns, int onlyGen, MyAnalysis *Evt){

//  example_Zll("jigsaw.root");
  JigsawRecTZFCNC *jigsawTzFCNC;
  jigsawTzFCNC = new JigsawRecTZFCNC();

  JigsawRecTHFCNC *jigsawThFCNC;
  jigsawThFCNC = new JigsawRecTHFCNC();

  objectSelection obj(Evt, year);
  genLevelAnalysis genAnalysis(Evt);

  TH1EFT  *crossSection = new TH1EFT("crossSection","crossSection",1,0,1);
  TH2F  btagEff_b_H;
  TH2F  btagEff_c_H;
  TH2F  btagEff_udsg_H;
  TH2F  sf_triggeree_H;
  TH2F  sf_triggeremu_H;
  TH2F  sf_triggermumu_H;
  TH2F  jetVetoMaps_H;
  TH2F  highPtMuRecoSF_pVsAbsEta_H;
  TH2F  sf_muonIsoIp_H;
  TH2F  sf_muonLooseMVATight_H;
  TH2F  sf_eleLoose_H;
  TH2F  sf_eleIsoIp_H;
  TH2F  sf_eleLooseMVATight_H;
  TH2F  sf_eleLooseMVATight2lss_H;
  TH2F  fr_mu_H;
  TH2F  fr_ele_H;
  TH2F  cf_ele_H;
  string rochesterFile;
  string btagFile;
  string eleSF;
  string muSF;
  string bSF;
  string JECFile;
  string jetSF;
  string lepFR;
  string yearName;
  string yearNameS;
  string gLumiMask;
  unsigned int fRun;
  unsigned int lRun;
  GEScaleSyst *GE = new GEScaleSyst();
  PU wPU;
  RoccoR  rc;
  float chargeFlipNorm;

  yearName=year;
  if(year == "2016preVFP") yearName="2016APV";
  if(year == "2016postVFP") yearName="2016";
  yearNameS=year;
  if(year == "2016preVFP") yearNameS="2016apv";
  if(year == "2016postVFP") yearNameS="2016";

  if(data == "mc"){
    TFile *f_btagEff_Map = new TFile("/afs/crc.nd.edu/user/r/rgoldouz/FCNC/NanoAnalysis/input/btagEffs_TopEFT_2022_05_16.root");
    btagEff_b_H = *(TH2F*)f_btagEff_Map->Get(("BtagSFB_DeepFlavM_" + yearNameS).c_str());
    btagEff_c_H = *(TH2F*)f_btagEff_Map->Get(("BtagSFC_DeepFlavM_" + yearNameS).c_str());
    btagEff_udsg_H = *(TH2F*)f_btagEff_Map->Get(("BtagSFL_DeepFlavM_" + yearNameS).c_str());
    f_btagEff_Map->Close();
    delete f_btagEff_Map;

    TFile *f_trigger = new TFile(("/afs/crc.nd.edu/user/r/rgoldouz/FCNC/NanoAnalysis/input/triggerScaleFactors_" + yearName + ".root").c_str());
    sf_triggeree_H = *(TH2F*)f_trigger->Get("sf_2l_ee");
    sf_triggeremu_H = *(TH2F*)f_trigger->Get("sf_2l_em");
    sf_triggermumu_H = *(TH2F*)f_trigger->Get("sf_2l_mm");
    f_trigger->Close();
    delete f_trigger;

    TFile *f_HighPtMuRecoSF = new TFile(("/afs/crc.nd.edu/user/r/rgoldouz/FCNC/NanoAnalysis/input/HighPtMuRecoSF_" + year + ".root").c_str());
    highPtMuRecoSF_pVsAbsEta_H = *(TH2F*)f_HighPtMuRecoSF->Get("h2_HighPtMuRecoSF_pVsAbsEta");
    f_HighPtMuRecoSF->Close();
    delete f_HighPtMuRecoSF;

    TFile *f_muonIsoIp = new TFile(("/afs/crc.nd.edu/user/r/rgoldouz/FCNC/NanoAnalysis/data/topCoffeaData/leptonSF/muon/egammaEffi" + yearName + "_iso_EGM2D.root").c_str());
    sf_muonIsoIp_H = *(TH2F*)f_muonIsoIp->Get("EGamma_SF2D");
    f_muonIsoIp->Close();
    delete f_muonIsoIp;

    TFile *f_muonLooseMVATight = new TFile(("/afs/crc.nd.edu/user/r/rgoldouz/FCNC/NanoAnalysis/data/topCoffeaData/leptonSF/muon/egammaEffi" + yearName + "_EGM2D.root").c_str());
    sf_muonLooseMVATight_H = *(TH2F*)f_muonLooseMVATight->Get("EGamma_SF2D");
    f_muonLooseMVATight->Close();
    delete f_muonLooseMVATight;

    TFile *f_eleLoose = new TFile(("/afs/crc.nd.edu/user/r/rgoldouz/FCNC/NanoAnalysis/data/topCoffeaData/leptonSF/elec/egammaEffi" + yearName + "_recoToloose_EGM2D.root").c_str());
    sf_eleLoose_H = *(TH2F*)f_eleLoose->Get("EGamma_SF2D");
    f_eleLoose->Close();
    delete f_eleLoose;

    TFile *f_eleIsoIp = new TFile(("/afs/crc.nd.edu/user/r/rgoldouz/FCNC/NanoAnalysis/data/topCoffeaData/leptonSF/elec/egammaEffi" + yearName + "_iso_EGM2D.root").c_str());
    sf_eleIsoIp_H = *(TH2F*)f_eleIsoIp->Get("EGamma_SF2D");
    f_eleIsoIp->Close();
    delete f_eleIsoIp;

    TFile *f_eleLooseMVATight = new TFile(("/afs/crc.nd.edu/user/r/rgoldouz/FCNC/NanoAnalysis/data/topCoffeaData/leptonSF/elecNEWmva/egammaEffi" + yearName + "_3l_EGM2D.root").c_str());
    sf_eleLooseMVATight_H = *(TH2F*)f_eleLooseMVATight->Get("EGamma_SF2D");
    f_eleLooseMVATight->Close();
    delete f_eleLooseMVATight;

    TFile *f_eleLooseMVATight2lss = new TFile(("/afs/crc.nd.edu/user/r/rgoldouz/FCNC/NanoAnalysis/data/topCoffeaData/leptonSF/elecNEWmva/egammaEffi" + yearName + "_2lss_EGM2D.root").c_str());
    sf_eleLooseMVATight2lss_H = *(TH2F*)f_eleLooseMVATight2lss->Get("EGamma_SF2D");
    f_eleLooseMVATight2lss->Close();
    delete f_eleLooseMVATight2lss;

  }
  if(year == "2016preVFP"){
    JECFile = "/afs/crc.nd.edu/user/r/rgoldouz/FCNC/NanoAnalysis/input/Summer19UL16APV_V7_MC/Summer19UL16APV_V7_MC_UncertaintySources_AK4PFchs.txt";
    rochesterFile = "/afs/crc.nd.edu/user/r/rgoldouz/FCNC/NanoAnalysis/input/RoccoR2016aUL.txt";
    eleSF="/afs/crc.nd.edu/user/r/rgoldouz/FCNC/NanoAnalysis/data/POG/EGM/2016preVFP_UL/electron.json.gz";
    muSF= "/afs/crc.nd.edu/user/r/rgoldouz/FCNC/NanoAnalysis/data/POG/MUO/2016preVFP_UL/muon_Z.json.gz";
    bSF="/afs/crc.nd.edu/user/r/rgoldouz/FCNC/NanoAnalysis/data/POG/BTV/2016preVFP_UL/btagging.json.gz";
    jetSF="/afs/crc.nd.edu/user/r/rgoldouz/FCNC/NanoAnalysis/data/POG/JME/2016preVFP_UL/UL16preVFP_jmar.json.gz";
    TFile *Map2016preVFP = new TFile("/afs/crc.nd.edu/user/r/rgoldouz/FCNC/NanoAnalysis/input/hotjets-UL16.root");
    jetVetoMaps_H = *(TH2F*)Map2016preVFP->Get("h2hot_ul16_plus_hbm2_hbp12_qie11");
    Map2016preVFP->Close();
    delete Map2016preVFP;
    TFile *lepFR = new TFile("/afs/crc.nd.edu/user/r/rgoldouz/FCNC/NanoAnalysis/data/topCoffeaData/fromTTH/fakerate/fr_2016APV_2016_recorrected.root");
    fr_mu_H = *(TH2F*)lepFR->Get("FR_mva085_mu_data_comb_recorrected");
    fr_ele_H = *(TH2F*)lepFR->Get("FR_mva090_el_data_comb_NC_recorrected");
    lepFR->Close();
    delete lepFR;
    TFile *lepCF = new TFile("/afs/crc.nd.edu/user/r/rgoldouz/FCNC/NanoAnalysis/input/fliprates_frommc_UL16APV_recorrected.root");
    cf_ele_H = *(TH2F*)lepCF->Get("chargeMisId");
    delete lepCF;
    chargeFlipNorm=0.79;
    gLumiMask="/afs/crc.nd.edu/user/r/rgoldouz/FCNC/NanoAnalysis/input/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt";
    fRun=271036;
    lRun=284044;
  }
  if(year == "2016postVFP"){
    JECFile = "/afs/crc.nd.edu/user/r/rgoldouz/FCNC/NanoAnalysis/input/Summer19UL16_V7_MC/Summer19UL16_V7_MC_UncertaintySources_AK4PFchs.txt";
    rochesterFile = "/afs/crc.nd.edu/user/r/rgoldouz/FCNC/NanoAnalysis/input/RoccoR2016bUL.txt";
    eleSF="/afs/crc.nd.edu/user/r/rgoldouz/FCNC/NanoAnalysis/data/POG/EGM/2016postVFP_UL/electron.json.gz";
    muSF= "/afs/crc.nd.edu/user/r/rgoldouz/FCNC/NanoAnalysis/data/POG/MUO/2016postVFP_UL/muon_Z.json.gz";
    bSF="/afs/crc.nd.edu/user/r/rgoldouz/FCNC/NanoAnalysis/data/POG/BTV/2016postVFP_UL/btagging.json.gz";
    jetSF="/afs/crc.nd.edu/user/r/rgoldouz/FCNC/NanoAnalysis/data/POG/JME/2016postVFP_UL/UL16postVFP_jmar.json.gz";
    TFile *Map2016postVFP = new TFile("/afs/crc.nd.edu/user/r/rgoldouz/FCNC/NanoAnalysis/input/hotjets-UL16.root");
    jetVetoMaps_H = *(TH2F*)Map2016postVFP->Get("h2hot_ul16_plus_hbm2_hbp12_qie11");
    Map2016postVFP->Close();
    delete Map2016postVFP;
    TFile *lepFR = new TFile("/afs/crc.nd.edu/user/r/rgoldouz/FCNC/NanoAnalysis/data/topCoffeaData/fromTTH/fakerate/fr_2016APV_2016_recorrected.root");
    fr_mu_H = *(TH2F*)lepFR->Get("FR_mva085_mu_data_comb_recorrected");
    fr_ele_H = *(TH2F*)lepFR->Get("FR_mva090_el_data_comb_NC_recorrected");
    lepFR->Close();
    delete lepFR;
    TFile *lepCF = new TFile("/afs/crc.nd.edu/user/r/rgoldouz/FCNC/NanoAnalysis/input/fliprates_frommc_UL16_recorrected.root");
    cf_ele_H = *(TH2F*)lepCF->Get("chargeMisId");
    delete lepCF;
    chargeFlipNorm=0.81;
    gLumiMask="/afs/crc.nd.edu/user/r/rgoldouz/FCNC/NanoAnalysis/input/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt";
    fRun=271036;
    lRun=284044;
  }
  if(year == "2017"){
    JECFile = "/afs/crc.nd.edu/user/r/rgoldouz/FCNC/NanoAnalysis/input/Summer19UL17_V5_MC/Summer19UL17_V5_MC_UncertaintySources_AK4PFchs.txt";
    rochesterFile = "/afs/crc.nd.edu/user/r/rgoldouz/FCNC/NanoAnalysis/input/RoccoR2017UL.txt";
    eleSF="/afs/crc.nd.edu/user/r/rgoldouz/FCNC/NanoAnalysis/data/POG/EGM/2017_UL/electron.json.gz";
    muSF= "/afs/crc.nd.edu/user/r/rgoldouz/FCNC/NanoAnalysis/data/POG/MUO/2017_UL/muon_Z.json.gz";
    bSF="/afs/crc.nd.edu/user/r/rgoldouz/FCNC/NanoAnalysis/data/POG/BTV/2017_UL/btagging.json.gz";
    jetSF="/afs/crc.nd.edu/user/r/rgoldouz/FCNC/NanoAnalysis/data/POG/JME/2017_UL/UL17_jmar.json.gz";
    TFile *Map2017 = new TFile("/afs/crc.nd.edu/user/r/rgoldouz/FCNC/NanoAnalysis/input/hotjets-UL17_v2.root");
    jetVetoMaps_H = *(TH2F*)Map2017->Get("h2hot_ul17_plus_hep17_plus_hbpw89");
    Map2017->Close();
    delete Map2017;
    TFile *lepFR = new TFile("/afs/crc.nd.edu/user/r/rgoldouz/FCNC/NanoAnalysis/data/topCoffeaData/fromTTH/fakerate/fr_2017_recorrected.root");
    fr_mu_H = *(TH2F*)lepFR->Get("FR_mva085_mu_data_comb_recorrected");
    fr_ele_H = *(TH2F*)lepFR->Get("FR_mva090_el_data_comb_NC_recorrected");
    lepFR->Close();
    delete lepFR;
    TFile *lepCF = new TFile("/afs/crc.nd.edu/user/r/rgoldouz/FCNC/NanoAnalysis/input/fliprates_frommc_UL17_recorrected.root");
    cf_ele_H = *(TH2F*)lepCF->Get("chargeMisId");
    delete lepCF;
    gLumiMask="/afs/crc.nd.edu/user/r/rgoldouz/FCNC/NanoAnalysis/input/Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.txt";
    chargeFlipNorm=1.22;
    fRun=294927; 
    lRun=306462;
  }
  if(year == "2018"){
    JECFile = "/afs/crc.nd.edu/user/r/rgoldouz/FCNC/NanoAnalysis/input/Summer19UL18_V5_MC/Summer19UL18_V5_MC_UncertaintySources_AK4PFchs.txt";
    rochesterFile = "/afs/crc.nd.edu/user/r/rgoldouz/FCNC/NanoAnalysis/input/RoccoR2018UL.txt";
    eleSF="/afs/crc.nd.edu/user/r/rgoldouz/FCNC/NanoAnalysis/data/POG/EGM/2018_UL/electron.json.gz";
    muSF= "/afs/crc.nd.edu/user/r/rgoldouz/FCNC/NanoAnalysis/data/POG/MUO/2018_UL/muon_Z.json.gz";
    bSF="/afs/crc.nd.edu/user/r/rgoldouz/FCNC/NanoAnalysis/data/POG/BTV/2018_UL/btagging.json.gz";
    jetSF="/afs/crc.nd.edu/user/r/rgoldouz/FCNC/NanoAnalysis/data/POG/JME/2018_UL/UL18_jmar.json.gz";
    TFile *Map2018 = new TFile("/afs/crc.nd.edu/user/r/rgoldouz/FCNC/NanoAnalysis/input/hotjets-UL18.root");
    jetVetoMaps_H = *(TH2F*)Map2018->Get("h2hot_ul18_plus_hem1516_and_hbp2m1");
    Map2018->Close();
    delete Map2018;
    TFile *lepFR = new TFile("/afs/crc.nd.edu/user/r/rgoldouz/FCNC/NanoAnalysis/data/topCoffeaData/fromTTH/fakerate/fr_2018_recorrected.root");
    fr_mu_H = *(TH2F*)lepFR->Get("FR_mva085_mu_data_comb_recorrected");
    fr_ele_H = *(TH2F*)lepFR->Get("FR_mva090_el_data_comb_NC_recorrected");
    lepFR->Close();
    delete lepFR;
    TFile *lepCF = new TFile("/afs/crc.nd.edu/user/r/rgoldouz/FCNC/NanoAnalysis/input/fliprates_frommc_UL18_recorrected.root");
    cf_ele_H = *(TH2F*)lepCF->Get("chargeMisId");
    delete lepCF;
    gLumiMask="/afs/crc.nd.edu/user/r/rgoldouz/FCNC/NanoAnalysis/input/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt";
    chargeFlipNorm=1.12;
    fRun=314472;
    lRun=325175;
  }

  auto myLumiMask = LumiMask::fromJSON(gLumiMask,fRun,lRun);
  

  rc.init(rochesterFile);
  auto csetFileEleSF = CorrectionSet::from_file(eleSF);
  auto csetEleIdReco = csetFileEleSF->at("UL-Electron-ID-SF");

  auto csetFileMuSF = CorrectionSet::from_file(muSF);
  auto csetMuReco = csetFileMuSF->at("NUM_TrackerMuons_DEN_genTracks");
  auto csetMuLoose = csetFileMuSF->at("NUM_LooseID_DEN_TrackerMuons");

  auto csetFilebSF = CorrectionSet::from_file(bSF);
  auto csetLightJetSF = csetFilebSF->at("deepJet_incl");
//  auto csetBcJetSF = csetFilebSF->at("deepCSV_mujets");
  auto csetBcJetSF = csetFilebSF->at("deepJet_comb");

  auto csetFileJetSF = CorrectionSet::from_file(jetSF);
  auto csetJetPuID = csetFileJetSF->at("PUJetID_eff");
  TRandom3 Tr;

  Double_t ptBins[11] = {30., 40., 60., 80., 100., 150., 200., 300., 400., 500., 1000.};
  Double_t etaBins [4]= {0., 0.6, 1.2, 2.4};
  TH2D *h2_BTaggingEff_Denom_b    = new TH2D("h2_BTaggingEff_Denom_b"   , ";p_{T} [GeV];#eta", 10 , ptBins, 3 , etaBins);
  TH2D *h2_BTaggingEff_Denom_c    = new TH2D("h2_BTaggingEff_Denom_c"   , ";p_{T} [GeV];#eta", 10 , ptBins, 3 , etaBins);
  TH2D *h2_BTaggingEff_Denom_udsg = new TH2D("h2_BTaggingEff_Denom_udsg", ";p_{T} [GeV];#eta", 10 , ptBins, 3 , etaBins);
  TH2D *h2_BTaggingEff_Num_b      = new TH2D("h2_BTaggingEff_Num_b"     , ";p_{T} [GeV];#eta", 10 , ptBins, 3 , etaBins);
  TH2D *h2_BTaggingEff_Num_c      = new TH2D("h2_BTaggingEff_Num_c"     , ";p_{T} [GeV];#eta", 10 , ptBins, 3 , etaBins);
  TH2D *h2_BTaggingEff_Num_udsg   = new TH2D("h2_BTaggingEff_Num_udsg"  , ";p_{T} [GeV];#eta", 10 , ptBins, 3 , etaBins);


  typedef vector<std::shared_ptr<TH1EFT>> Dim1;
  typedef vector<Dim1> Dim2;
  typedef vector<Dim2> Dim3;
  typedef vector<Dim3> Dim4;

  std::vector<TString> channels{"EpEm", "MUpMUm", "EpmMUmp","LLpp","LLmm", "3LonZ", "3LoffZp", "3LoffZm","4L", "LLOSpp","LLOSmm",
                                "LFpp", "FFpp", "LFmm", "FFmm",
                                "LLFonZ", "LFFonZ","FFFonZ",
                                "LLFoffZp", "LFFoffZp","FFFoffZp",
                                "LLFoffZm", "LFFoffZm","FFFoffZm"};
  std::vector<TString> regions{"All","0Bjet","1Bjet", "G1Bjet"};
  std::vector<TString> sys{"eleRecoIdIso","muRecoIdIso","triggerSF","pu","preFire"};
  const std::map<TString, std::vector<float>> vars =
  {
    {"lep1Pt",                         {0,      60,   0,  1500}},
    {"lep1Eta",                        {1,      20,   -3, 3   }},
    {"lep1Phi",                        {2,      25,   -4, 4   }},
    {"lep2Pt",                         {3,      25,   0,  1000}},
    {"lep2Eta",                        {4,      20,   -3, 3   }},
    {"lep2Phi",                        {5,      25,   -4, 4   }},
    {"llM",                            {6,      30,    0, 500 }},
    {"llPt",                           {7,      20,    0, 200 }},
    {"llDr",                           {8,      25,    0, 7   }},
    {"llDphi",                         {9,      15,    0, 4   }},
    {"jet1Pt",                         {10,     20,    0, 300 }},
    {"jet1Eta",                        {11,     20,    -3, 3  }},
    {"jet1Phi",                        {12,     25,    -4, 4  }},
    {"njet",                           {13,     10,    0, 10  }},
    {"nbjet",                          {14,     6,     0, 6   }},
    {"Met",                            {15,     30,    0, 210 }},
    {"MetPhi",                         {16,     20,    -4, 4  }},
    {"nVtx",                           {17,     70,    0, 70  }},
    {"llMZw",                          {18,     80,    70, 110}},
  };

//  D3HistsContainer Hists;
  Hists.resize(channels.size());
  for (int i=0;i<channels.size();++i){
    Hists[i].resize(regions.size());
    for (int k=0;k<regions.size();++k){
      Hists[i][k].resize(vars.size());
    }
  }

  std::stringstream name;
  TH1EFT *h_test;
  for (int i=0;i<channels.size();++i){
    for (int k=0;k<regions.size();++k){
      for( auto it = vars.cbegin() ; it != vars.cend() ; ++it ){
        name<<channels[i]<<"_"<<regions[k]<<"_"<<it->first;
        h_test = new TH1EFT((name.str()).c_str(),(name.str()).c_str(),it->second.at(1), it->second.at(2), it->second.at(3));
        h_test->StatOverflows(kTRUE);
        h_test->Sumw2(kTRUE);
        Hists[i][k][it->second.at(0)] = h_test;
        name.str("");
      }
    }
  }

  TH1F  *JigsawWmass = new TH1F("JigsawWmass","JigsawWmass",50,0,500);
  TH1F  *JigsawTmass = new TH1F("JigsawTmass","JigsawTmass",50,0,500);
  TH1F  *JigsawWmassReco = new TH1F("JigsawWmassReco","JigsawWmassReco",50,0,500);
  TH1F  *JigsawTmassReco = new TH1F("JigsawTmassReco","JigsawTmassReco",50,0,500);

  TH1F  *JigsawWmass_tHFCNC = new TH1F("JigsawWmass_tHFCNC","JigsawWmass_tHFCNC",50,0,500);
  TH1F  *JigsawTmass_tHFCNC = new TH1F("JigsawTmass_tHFCNC","JigsawTmass_tHFCNC",50,0,500);
  TH1F  *JigsawHmass_tHFCNC = new TH1F("JigsawHmass_tHFCNC","JigsawHmass_tHFCNC",50,0,500);

  TH1F  *JigsawWmassReco_tHFCNC = new TH1F("JigsawWmassReco_tHFCNC","JigsawWmassReco_tHFCNC",50,0,500);
  TH1F  *JigsawTmassReco_tHFCNC = new TH1F("JigsawTmassReco_tHFCNC","JigsawTmassReco_tHFCNC",50,0,500);
  TH1F  *JigsawHmassReco_tHFCNC = new TH1F("JigsawHmassReco_tHFCNC","JigsawHmassReco_tHFCNC",50,0,500);
  TH1F  *DRij = new TH1F("DRij","DRij",15,0,8);
  TH1F  *DRtH = new TH1F("DRtH","DRtH",15,0,8);
  TH1F  *DRWHWH = new TH1F("DRWHWH","DRWHWH",15,0,8);
  TH1F  *DPhitH = new TH1F("DPhitH","DPhitH",15,-4,4);
  TH2F  *HmassVsnJet = new TH2F("HmassVsnJet","HmassVsnJet",20,0,500,6,0,6);

  float lep1Pt_;
  float lep1Eta_;
  float lep2Pt_;
  float lep2Eta_;
  float lep3Pt_;
  float lep3Eta_;
  float llM_;
  float llPt_;
  float llDr_;
  float llDphi_;
  float jet1Pt_;
  float jet1Eta_;
  float bJetPt_;
  float bJetEta_;
  int nJets_;
  float weightSM_;
  float topMass_;
  float HZMass_;
  float WtopMass_;
  float W1HMass_;
  float W2HMass_;
  float HZPt_;
  float HZEta_;
  float topPt_;
  float topEta_;
  float drWtopB_;
  float drW1HW2H_;
  int ch_;
  float weightctp_;
  float weightctlS_;
  float weightcte_;
  float weightctl_;
  float weightctlT_;
  float weightctZ_;
  float weightcpt_;
  float weightcpQM_;
  float weightctA_;
  float weightcQe_;
  float weightctG_;
  float weightcQlM_;

  TTree tree_out("FCNC","Top FCNC analysis") ;
  tree_out.Branch("lep1Pt"      , &lep1Pt_ , "lep1Pt/F" ) ;
  tree_out.Branch("lep1Eta"      , &lep1Eta_ , "lep1Eta/F" ) ;
  tree_out.Branch("lep2Pt"      , &lep2Pt_ , "lep2Pt/F" ) ;
  tree_out.Branch("lep2Eta"      , &lep2Eta_ , "lep2Eta/F" ) ;
  tree_out.Branch("lep3Pt"      , &lep3Pt_ , "lep3Pt/F" ) ;
  tree_out.Branch("lep3Eta"      , &lep3Eta_ , "lep3Eta/F" ) ;
  tree_out.Branch("llM"      , &llM_ , "llM/F" ) ;
  tree_out.Branch("llPt"      , &llPt_ , "llPt/F" ) ;
  tree_out.Branch("llDr"      , &llDr_ , "llDr/F" ) ;
  tree_out.Branch("llDphi"      , &llDphi_ , "llDphi/F" ) ;
  tree_out.Branch("jet1Pt"      , &jet1Pt_ , "jet1Pt/F" ) ;
  tree_out.Branch("jet1Eta"      , &jet1Eta_ , "jet1Eta/F"  ) ;
  tree_out.Branch("bJetPt"      , &bJetPt_ , "bJetPt/F" ) ;
  tree_out.Branch("bJetEta"      , &bJetEta_ , "bJetEta/F"  ) ;
  tree_out.Branch("nJets"      , &nJets_ , "nJets/I"  ) ;
  tree_out.Branch("topMass"      , &topMass_ , "topMass/F"  ) ;
  tree_out.Branch("HZMass"      , &HZMass_ , "HZMass/F"  ) ;
  tree_out.Branch("WtopMass"      , &WtopMass_ , "WtopMass/F"  ) ;
  tree_out.Branch("W1HMass"      , &W1HMass_ , "W1HMass/F"  ) ;
  tree_out.Branch("W2HMass"      , &W2HMass_ , "W2HMass/F"  ) ;
  tree_out.Branch("HZPt"      , &HZPt_ , "HZPt/F"  ) ;
  tree_out.Branch("HZEta"      , &HZEta_ , "HZEta/F"  ) ;
  tree_out.Branch("topPt"      , &topPt_ , "topPt/F"  ) ;
  tree_out.Branch("topEta"      , &topEta_ , "topEta/F"  ) ;
  tree_out.Branch("drWtopB"      , &drWtopB_ , "drWtopB/F"  ) ;
  tree_out.Branch("drW1HW2H"      , &drW1HW2H_ , "drW1HW2H/F"  ) ;
  tree_out.Branch("weightSM"      , &weightSM_ , "weightSM/F" ) ;
  tree_out.Branch("weightctp"      , &weightctp_ , "weightctp/F" ) ;
  tree_out.Branch("weightctlS"      , &weightctlS_ , "weightctlS/F" ) ;
  tree_out.Branch("weightcte"      , &weightcte_ , "weightcte/F" ) ;
  tree_out.Branch("weightctl"      , &weightctl_ , "weightctl/F" ) ;
  tree_out.Branch("weightctlT"      , &weightctlT_ , "weightctlT/F" ) ;
  tree_out.Branch("weightctZ"      , &weightctZ_ , "weightctZ/F" ) ;
  tree_out.Branch("weightcpt"      , &weightcpt_ , "weightcpt/F" ) ;
  tree_out.Branch("weightcpQM"      , &weightcpQM_ , "weightcpQM/F" ) ;
  tree_out.Branch("weightctA"      , &weightctA_ , "weightctA/F" ) ;
  tree_out.Branch("weightcQe"      , &weightcQe_ , "weightcQe/F" ) ;
  tree_out.Branch("weightctG"      , &weightctG_ , "weightctG/F" ) ;
  tree_out.Branch("weightcQlM"      , &weightcQlM_ , "weightcQlM/F" ) ;
  tree_out.Branch("ch"      , &ch_, "ch/I" ) ;

  std::vector<string> wc_names_lst={};
  std::vector<string> wc_names_lst_BNV={"cT", "cS"};
  std::vector<string> wc_names_lst_FCNC={"ctp","ctlS","cte","ctl","ctlT","ctZ","cpt","cpQM","ctA","cQe","ctG","cQlM"};
  std::vector<string> wc_names_lst_SMEFT={"ctu1","cqd1","cqq13","ctu8","cqu1","cqq11","cqq83","ctd1","ctd8","ctg","ctq1","cqq81","cqu8","cqd8","ctq8"};
  if (fname.Contains("BNV") && iseft) wc_names_lst = wc_names_lst_BNV;
  if (fname.Contains("FCNC") && iseft) wc_names_lst = wc_names_lst_FCNC;
  if (fname.Contains("SMEFT") && iseft) wc_names_lst = wc_names_lst_SMEFT;
  string listWC="";
//  TFile file_out ("ANoutput.root","RECREATE");

  std::vector<lepton_candidate*> *selectedPLeptons;
  std::vector<lepton_candidate*> *selectedFLeptons;
  std::vector<lepton_candidate*> *selectedLeptons;
  std::vector<lepton_candidate*> *selectedLooseLeptons;
  std::vector<jet_candidate*> *selectedJets;
  WCFit *eft_fit;


  TLorentzVector wp, wm, b, ab, top, atop;
  std::vector<float> nominalWeights;
  nominalWeights.assign(sys.size(), 1);
  TLorentzVector recoTop, recoBjet, recoW, recoNu, recoL1, recoL2, highPtMu;
  bool leptonPass;
  bool triggerPass;
  bool DyPass;
  bool MetPass;
  bool triggerPassE;
  bool triggerPassEE;
  bool triggerPassEMu;
  bool triggerPassMu;
  bool triggerPassMuMu;
  bool metFilterPass;
  bool ifTopPt=false;
  float ttKFactor;
  int ch;
  int chOSpp;
  int chOSmm;
  int sumCharge;
  int sumFlavour;
  bool onZ;
  float MetCut=60;
  float sf_Ele_Reco;
  float sf_Ele_ID;
  float sf_Mu_ID;
  float sf_Mu_ISO;
  float sf_Trigger;
  float sf_JetPuId;
  float weight_PU;
  float weight_Lumi;
  float weight_lep;
  float weight_lepB;
  float weight_EFT;
  float weight_prefiring;
  float weight_topPtPowheg;
  float weight_topPtMGLO;
  float MVAoutputJerUp;
  float MVAoutputJerDown;
  float MVAoutputJesUp;
  float MVAoutputJesDown;
  float MVAoutputMuScaleUp;
  float MVAoutputMuScaleDown;
  float MVAoutputEleScaleUp;
  float MVAoutputEleScaleDown;
  float MVAoutputMuResUp;
  float MVAoutputMuResDown;
  float MVAoutputUnclusMETUp;
  float MVAoutputUnclusMETDown;
  float metUnclusMETUp;
  float metUnclusMETDown;
  float metUnclusMETPhiUp;
  float metUnclusMETPhiDown;
  float MVAoutput;
  double P_bjet_data;
  double P_bjet_mc;
  int nAccept=0;
  float sumWeight=0;
  float sumPuWeight=0;
  float sumPreFireWeight=0;
  float sumWeightMuID=0;
  float sumWeightMuIso=0;
  float sumWeighttTrigger=0;
  float sumWeightEleID=0;
  float sumWeightEleReco=0;
  float sumWeightBtag=0;
  float correctMuonPt=0;
  float correctMuonPtUp=0;
  float correctMuonPtDown=0;
  int nbjetGen;
  int nbjet;
  int nbjetJesUp;
  int nbjetJesDown;
  int nbjetJerUp;
  int nbjetJerDown;
  float JECMETUpx;
  float JECMETUpy;
  float JECMETDownx;
  float JECMETDowny;
  float pt_res;
  double muPtSFRochester;
  int R;
  double sup = 0;
  double sdw = 0;
  bool jetlepfail;
  float BJetSF;
  float CJetSF;
  float LJetSF;
  float BJetSF_UpCorr;
  float CJetSF_UpCorr;
  float LJetSF_UpCorr;
  float BJetSF_UpUnCorr;
  float CJetSF_UpUnCorr;
  float LJetSF_UpUnCorr;
  float BJetSF_DownCorr;
  float CJetSF_DownCorr;
  float LJetSF_DownCorr;
  float BJetSF_DownUnCorr;
  float CJetSF_DownUnCorr;
  float LJetSF_DownUnCorr;
  float BJetEff;
  float CJetEff;
  float LJetEff;
  float SmearedMuonPt;
  float myMET;
  std::vector<int> reg(regions.size());
  std::vector<int> allCh(3);
  std::vector<std::vector<float>> wgt(3);
  for (int i = 0 ; i < 3 ; i++) {
    wgt[i].resize(regions.size());
  }
  std::vector<std::vector<WCFit>> wcfit(3);
  for (int i = 0 ; i < 3 ; i++) {
    wcfit[i].resize(regions.size());
  }
  int nLHEl;
  int checkEvent=27130105;
  float fakeRate;
  float fi;
  float probChOSpp;
  float probChOSmm;
  int lZ1;
  int lZ2;
  TLorentzVector top_tZFCNC, bt_tZFCNC, Wt_tZFCNC, lt_tZFCNC, nut_tZFCNC, Z_tZFCNC, lpZ_tZFCNC, lmZ_tZFCNC ;
  TLorentzVector hL_tHFCNC, hNu_tHFCNC, hU_tHFCNC, hD_tHFCNC, tNu_tHFCNC, tB_tHFCNC, tL_tHFCNC, met_tHFCNC;
  WCPoint *A = new WCPoint("EFTrwgt4_cpQM_1.0_cpt_1.0_ctA_1.0_ctZ_0.5_ctG_0.1_cQlM_1.0_cQe_1.0_ctl_1.0_cte_1.0_ctlS_1.0_ctlT_0.05_ctp_1.0");

  if (fname.Contains("TTTo2L2Nu") || fname.Contains("sys") || fname.Contains("TTFCNC")) ifTopPt=true;
  if (fChain == 0) return;
  Long64_t nentries = fChain->GetEntriesFast();
  Long64_t nbytes = 0, nb = 0;
  Long64_t ntr = fChain->GetEntries ();
//Loop over events
  for (Long64_t jentry=0; jentry<nentries;jentry++) {
//  for (Long64_t jentry=0; jentry<1000;jentry++) {
    Long64_t ientry = LoadTree(jentry);
    if (ientry < 0) break;
    nb = fChain->GetEntry(jentry);   nbytes += nb;
    displayProgress(jentry, ntr) ;
    topMass_=-999;    HZMass_=-999;    WtopMass_=-999;    W1HMass_=-999;    W2HMass_=-999;    HZPt_=-999;    HZEta_=-999;    topPt_=-999;    topEta_=-999;    drWtopB_=-999;    drW1HW2H_=-999;
    if(jentry==0 && fname.Contains("FCNC")){
      listWC="";
      for (UInt_t i=0;i<nWCnames;++i){
         char ch[4];
         for(int j = 0; j < 4; j++) ch[j] = (WCnames[i] >> (4-1-j)*8) & 0xFF;
         for(int n=0 ; n<4 ; ++n) listWC += ch[n];
      }
      cout<<"\n original WC list= {"<<listWC<<"}"<<endl;
      listWC=std::regex_replace(listWC, std::regex("-"), std::string(""));
      listWC=std::regex_replace(listWC, std::regex("c"), std::string("\",\"c"));
      listWC.erase(0,2);
      listWC+="\"";
      cout<<"\n WC list = {"<<listWC<<"}"<<endl;
      cout<<"\n  WC list in this code = {";
      for (auto i: wc_names_lst) {
        std::cout << i << ',';} cout<<"}"<<endl;
      }
    if(data == "data"){
      if(!myLumiMask.accept(run, luminosityBlock)) continue;
    }
/*
    if(jentry==0 && fname.Contains("FCNC")){
      listWC="";
      for (UInt_t i=0;i<nWCnames;++i){
         char ch[4];
         for(int j = 0; j < 4; j++) ch[j] = (WCnames[i] >> (4-1-j)*8) & 0xFF;
         for(int n=0 ; n<4 ; ++n) listWC += ch[n];
      }
      cout<<"\n original WC list= {"<<listWC<<"}"<<endl;
      listWC=std::regex_replace(listWC, std::regex("-"), std::string(""));
      listWC=std::regex_replace(listWC, std::regex("c"), std::string("\",\"c"));
      listWC.erase(0,2);
      listWC+="\"";
      cout<<"\n WC list = {"<<listWC<<"}"<<endl;
      cout<<"\n  WC list in this code = {";
      for (auto i: wc_names_lst) {
        std::cout << i << ',';} cout<<"}"<<endl;
    }
*/
    Z_tZFCNC.SetPtEtaPhiM(0,0,0,0); top_tZFCNC.SetPtEtaPhiM(0,0,0,0); bt_tZFCNC.SetPtEtaPhiM(0,0,0,0); Wt_tZFCNC.SetPtEtaPhiM(0,0,0,0); lt_tZFCNC.SetPtEtaPhiM(0,0,0,0); lpZ_tZFCNC.SetPtEtaPhiM(0,0,0,0); lmZ_tZFCNC.SetPtEtaPhiM(0,0,0,0);
    if(data == "mc" && fname.Contains("FCNC")){
      for (int l=0;l<nGenPart;l++){
        if(isnan(GenPart_pt[l]) || isinf(GenPart_pt[l]) || GenPart_pt[l]==0) continue;
//        if(GenPart_statusFlags[l] & (1<<13)){
//          cout<<l<<":"<<GenPart_pdgId[l]<<":"<<GenPart_pdgId[GenPart_genPartIdxMother[l]]<<":pt:"<<GenPart_pt[l]<<endl;
          if(abs(GenPart_pdgId[l])==24) Wt_tZFCNC.SetPtEtaPhiM(GenPart_pt[l], GenPart_eta[l], GenPart_phi[l], GenPart_mass[l]);
          if(abs(GenPart_pdgId[l])==6) top_tZFCNC.SetPtEtaPhiM(GenPart_pt[l], GenPart_eta[l], GenPart_phi[l], GenPart_mass[l]);
          if(abs(GenPart_pdgId[l])==23) Z_tZFCNC.SetPtEtaPhiM(GenPart_pt[l], GenPart_eta[l], GenPart_phi[l], GenPart_mass[l]);
          if(abs(GenPart_pdgId[l])==11 || abs(GenPart_pdgId[l])==13 || abs(GenPart_pdgId[l])==15){
            if(abs(GenPart_pdgId[GenPart_genPartIdxMother[l]])==24) lt_tZFCNC.SetPtEtaPhiM(GenPart_pt[l], GenPart_eta[l], GenPart_phi[l], GenPart_mass[l]);
            if(abs(GenPart_pdgId[GenPart_genPartIdxMother[l]])==23 && GenPart_pdgId[l]>0) lpZ_tZFCNC.SetPtEtaPhiM(GenPart_pt[l], GenPart_eta[l], GenPart_phi[l], GenPart_mass[l]);
            if(abs(GenPart_pdgId[GenPart_genPartIdxMother[l]])==23 && GenPart_pdgId[l]<0) lmZ_tZFCNC.SetPtEtaPhiM(GenPart_pt[l], GenPart_eta[l], GenPart_phi[l], GenPart_mass[l]);
          }
          if(abs(GenPart_pdgId[l])==12 || abs(GenPart_pdgId[l])==14 || abs(GenPart_pdgId[l])==16){
            if(abs(GenPart_pdgId[GenPart_genPartIdxMother[l]])==24) nut_tZFCNC.SetPtEtaPhiM(GenPart_pt[l], 0, GenPart_phi[l], 0);
          }
          if(abs(GenPart_pdgId[l])==5) bt_tZFCNC.SetPtEtaPhiM(GenPart_pt[l], GenPart_eta[l], GenPart_phi[l], GenPart_mass[l]);
//        }
      }
    if(Z_tZFCNC.Pt()>0 && lpZ_tZFCNC.Pt()>15 && lmZ_tZFCNC.Pt()>15){
       jigsawTzFCNC->Analyze(lt_tZFCNC, lpZ_tZFCNC, lmZ_tZFCNC, bt_tZFCNC,nut_tZFCNC);
       JigsawWmass->Fill(jigsawTzFCNC->W->GetMass());
       JigsawTmass->Fill(jigsawTzFCNC->T->GetMass());
//cout<<jigsawTzFCNC->W->GetMass()<<":"<<(lt_tZFCNC+nut_tZFCNC).M()<<endl;
    }
//tH FCNC
      hL_tHFCNC.SetPtEtaPhiM(0,0,0,0); hNu_tHFCNC.SetPtEtaPhiM(0,0,0,0); hU_tHFCNC.SetPtEtaPhiM(0,0,0,0); hD_tHFCNC.SetPtEtaPhiM(0,0,0,0); tNu_tHFCNC.SetPtEtaPhiM(0,0,0,0); tB_tHFCNC.SetPtEtaPhiM(0,0,0,0); tL_tHFCNC.SetPtEtaPhiM(0,0,0,0);
      for (int l=0;l<nGenPart;l++){
        if(isnan(GenPart_pt[l]) || isinf(GenPart_pt[l]) || GenPart_pt[l]==0) continue;
          if(abs(GenPart_pdgId[l])==11 || abs(GenPart_pdgId[l])==13 || abs(GenPart_pdgId[l])==15){
             if(abs(GenPart_pdgId[GenPart_genPartIdxMother[l]])==24){
               if(tL_tHFCNC.Pt()==0) tL_tHFCNC.SetPtEtaPhiM(GenPart_pt[l], GenPart_eta[l], GenPart_phi[l], GenPart_mass[l]);
               else hL_tHFCNC.SetPtEtaPhiM(GenPart_pt[l], GenPart_eta[l], GenPart_phi[l], GenPart_mass[l]);
             }
           }
          if(abs(GenPart_pdgId[l])==5) tB_tHFCNC.SetPtEtaPhiM(GenPart_pt[l], GenPart_eta[l], GenPart_phi[l], GenPart_mass[l]);
          if(abs(GenPart_pdgId[l])==2 || abs(GenPart_pdgId[l])==4 ){
             if(abs(GenPart_pdgId[GenPart_genPartIdxMother[l]])==24) hU_tHFCNC.SetPtEtaPhiM(GenPart_pt[l], GenPart_eta[l], GenPart_phi[l], GenPart_mass[l]);
           }
          if(abs(GenPart_pdgId[l])==1 || abs(GenPart_pdgId[l])==3 ){
             if(abs(GenPart_pdgId[GenPart_genPartIdxMother[l]])==24) hD_tHFCNC.SetPtEtaPhiM(GenPart_pt[l], GenPart_eta[l], GenPart_phi[l], GenPart_mass[l]);
           }
       }
       met_tHFCNC.SetPtEtaPhiM(GenMET_pt,0,GenMET_phi,0);
//      if(tL_tHFCNC.Pt()>0 && hL_tHFCNC.Pt()>15 && hU_tHFCNC.Pt()>15){
//       jigsawThFCNC->Analyze(tL_tHFCNC, hL_tHFCNC, tB_tHFCNC, hU_tHFCNC, hD_tHFCNC, met_tHFCNC);
//       JigsawWmass_tHFCNC->Fill(jigsawThFCNC->WT->GetMass());
//       JigsawTmass_tHFCNC->Fill(jigsawThFCNC->T->GetMass());
//       JigsawHmass_tHFCNC->Fill(jigsawThFCNC->H->GetMass());
//      }
//cout<<"Gen top mass:"<<top_tZFCNC.M()<<" W:"<<Wt_tZFCNC.M()<<" Z:"<<Z_tZFCNC.M()<<" top l pt:"<<lt_tZFCNC.Pt()<<" b pt:"<<bt_tZFCNC.Pt()<<" l+ pt:"<<lpZ_tZFCNC.Pt()<<" l- pt:"<<lmZ_tZFCNC.Pt()<<endl;
    }
    if(data == "mc" && onlyGen){
      if(iseft && fname.Contains("rwgt")) genAnalysis.fillGENHists(1.0/nRuns,wc_names_lst);
      else if(iseft && !fname.Contains("rwgt")) genAnalysis.fillGENHists(LHEWeight_originalXWGTUP/nRuns,wc_names_lst);
      else  genAnalysis.fillGENHists(xs/Nevent,wc_names_lst);
      continue;
    }
    if(data == "mc" && !onlyGen){
      if(iseft && fname.Contains("rwgt")) genAnalysis.fillGENHists(1.0/nRuns,wc_names_lst);
      else if(iseft && !fname.Contains("rwgt")) genAnalysis.fillGENHists(LHEWeight_originalXWGTUP/nRuns,wc_names_lst);
      else  genAnalysis.fillGENHists(xs/Nevent,wc_names_lst);
    }
    nLHEl=0;
    if(data == "mc"){
      for (int l=0;l<nLHEPart;l++){
        if(abs(LHEPart_pdgId[l]) ==11 || abs(LHEPart_pdgId[l]) ==13 ){
          if(LHEPart_pt[l]>20 && abs(LHEPart_eta[l])<2.4) nLHEl++;
        }
      }
      for (int l=0;l<nGenPart;l++){
        if(abs(GenPart_pdgId[l])==11 || abs(GenPart_pdgId[l])==13){
          if(abs(GenPart_pdgId[GenPart_genPartIdxMother[l]])==24 && GenPart_pt[l]>20 &&  abs(GenPart_eta[l])<2.4) nLHEl++;
        }
      }
    }

    if(nLHEl >1) nAccept++;

    triggerPassEE = false;
    triggerPassEMu = false;
    triggerPassMuMu = false;
    triggerPassE = false;
    triggerPassMu = false;
    triggerPass= false;
    metFilterPass = false;
    leptonPass = false;
    triggerPass = false;
    DyPass = false;
    MetPass = false;
    ch =100;
    chOSpp=100;
    chOSmm=100;
    sumCharge =0;
    sumFlavour = 0;
    onZ = false;
    ttKFactor=1;
    sf_Ele_Reco =1;
    sf_Ele_ID =1;
    sf_Mu_ID =1;
    sf_Mu_ISO =1;
    sf_Trigger =1;
    sf_JetPuId =1;
    muPtSFRochester=1;
    weight_PU =1;
    weight_Lumi =1;
    weight_lep =1;
    weight_lepB =1;
    weight_EFT =1;
    weight_prefiring =1;
    weight_topPtPowheg =1;
    weight_topPtMGLO =1;
    P_bjet_data =1;
    P_bjet_mc =1;
    MVAoutput=0;
    nbjetGen=0;
    nbjet=0;
    nbjetJerUp=0;
    nbjetJerDown=0;
    nbjetJesUp=0;
    nbjetJesDown=0;
    metUnclusMETUp=0;
    metUnclusMETDown=0;
    metUnclusMETPhiUp=0;
    metUnclusMETPhiDown=0;
    myMET= MET_T1_pt;

    BJetSF=1;
    CJetSF=1;
    LJetSF=1;
    BJetSF_UpCorr=1;
    CJetSF_UpCorr=1;
    LJetSF_UpCorr=1;
    BJetSF_UpUnCorr=1;
    CJetSF_UpUnCorr=1;
    LJetSF_UpUnCorr=1;
    BJetSF_DownCorr=1;
    CJetSF_DownCorr=1;
    LJetSF_DownCorr=1;
    BJetSF_DownUnCorr=1;
    CJetSF_DownUnCorr=1;
    LJetSF_DownUnCorr=1;
    BJetEff=1;
    CJetEff=1;
    LJetEff=1;
    fakeRate=1;
    fi=1;
    probChOSpp=1;
    probChOSmm=-1;
    for (int n=0;n<sys.size();++n){
      nominalWeights[n] =1;
    //  sysUpWeights[n] =1;
    //  sysDownWeights[n] =1;
    }  

//MET filters

    if (iseft) {
      eft_fit = new WCFit(nWCnames, wc_names_lst, nEFTfitCoefficients, EFTfitCoefficients, 1.0/nRuns);
//      for (UInt_t i=0;i<nWCnames;++i){
//         char ch[4];
////         for(int j = 0; j < 4; j++) ch[j] = (WCnames[i] >> (4-1-j)*8) & 0xFF;
//         cout<< " - "<<WCnames[i] <<endl;
////         for(int n=0 ; n<4 ; ++n) cout << ch[n];
////         cout<<" : "<<endl;;
//      }
      
    }
    else {
      eft_fit = new WCFit(0,wc_names_lst,1, &genWeight, 1.0); 
    }

//cout<<run<<":"<<luminosityBlock<<":"<<event<<endl;
    for (int l=0;l<wc_names_lst.size();l++){
      if(wc_names_lst[l]!="cpQM") continue;
      A= new WCPoint("EFTrwgt131_"+wc_names_lst[l]+"_1.0");
//      cout<<"EFTrwgt131_"+wc_names_lst[l]+"_1.0"<<endl;
//      if(eft_fit->evalPoint(A)>0.1) cout<<wc_names_lst[l]<<":"<<eft_fit->evalPoint(A)<<endl;
      delete A;
    }
    crossSection->Fill(0.5, 1,*eft_fit);
//cout<<eft_fit->getCoefficient("sm","sm")<<endl;
//cout<<eft_fit->getCoefficient("ctp","ctp")<<endl;
    delete eft_fit; 
//You should add Flag_BadPFMuonDzFilter to the MET filter list but since it is not available in v8, lets remove it for now.
    if(year == "2017" || year == "2018"){
      if ( Flag_goodVertices  &&  Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter &&  Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_eeBadScFilter && Flag_ecalBadCalibFilter && Flag_BadPFMuonDzFilter) metFilterPass = true;
    }
    else{
      if ( Flag_goodVertices  &&  Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter &&  Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_eeBadScFilter && Flag_BadPFMuonDzFilter) metFilterPass = true;
    }

//trigger MC
    if(data == "mc" && (year == "2016preVFP" || year == "2016postVFP")){
      if(HLT_IsoMu24 || HLT_IsoTkMu24 || HLT_Ele27_WPTight_Gsf || HLT_Ele25_eta2p1_WPTight_Gsf || HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ || HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL || HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL || HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ || HLT_TripleMu_12_10_5 || HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL || HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Ele16_Ele12_Ele8_CaloIdL_TrackIdL || HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL || HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL || HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu23_TrkIsoVVL_Ele8_CaloIdL_TrackIdL_IsoVL || HLT_Mu8_DiEle12_CaloIdL_TrackIdL || HLT_DiMu9_Ele9_CaloIdL_TrackIdL) triggerPass =true;
    }

    if(data == "mc" && year == "2017"){
      if(HLT_IsoMu24 || HLT_IsoMu27 || 
         HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ || HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8 || HLT_TripleMu_12_10_5 ||
         HLT_Ele32_WPTight_Gsf_L1DoubleEG || HLT_Ele35_WPTight_Gsf ||
         HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL || HLT_Ele16_Ele12_Ele8_CaloIdL_TrackIdL ||
         HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL || HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu8_DiEle12_CaloIdL_TrackIdL || HLT_Mu8_DiEle12_CaloIdL_TrackIdL_DZ || HLT_DiMu9_Ele9_CaloIdL_TrackIdL_DZ) triggerPass =true;
    }

    if(data == "mc" && year == "2018"){
      if(HLT_IsoMu24 || HLT_IsoMu27 || HLT_Ele32_WPTight_Gsf || HLT_Ele35_WPTight_Gsf || HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL || HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Ele16_Ele12_Ele8_CaloIdL_TrackIdL || HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ || HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8 || HLT_TripleMu_12_10_5 || HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL || HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu8_DiEle12_CaloIdL_TrackIdL || HLT_Mu8_DiEle12_CaloIdL_TrackIdL_DZ || HLT_DiMu9_Ele9_CaloIdL_TrackIdL_DZ) triggerPass =true;
    }

//trigger DATA
    if(data == "data"){
      if(year == "2016preVFP" || year == "2016postVFP"){
        triggerPassMu = (HLT_IsoMu24 || HLT_IsoTkMu24);
        triggerPassMuMu = (HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ || HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL || HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL || HLT_Mu17_TrkIsoVVL_TkMu8_TrkIsoVVL_DZ|| HLT_TripleMu_12_10_5);
        triggerPassE = (HLT_Ele27_WPTight_Gsf || HLT_Ele25_eta2p1_WPTight_Gsf);
        triggerPassEE = (HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL || HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Ele16_Ele12_Ele8_CaloIdL_TrackIdL);
        triggerPassEMu = (HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL || HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL || HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu23_TrkIsoVVL_Ele8_CaloIdL_TrackIdL_IsoVL ||  HLT_Mu8_DiEle12_CaloIdL_TrackIdL || HLT_DiMu9_Ele9_CaloIdL_TrackIdL);

        if(dataset=="SingleMuon"){
          if (triggerPassMu) triggerPass=true;
        }
        if(dataset=="DoubleMuon"){
          if (!triggerPassMu && triggerPassMuMu) triggerPass=true;
        }
        if(dataset=="SingleElectron"){
          if (!triggerPassMu && !triggerPassMuMu && triggerPassE) triggerPass=true;
        }
        if(dataset=="DoubleEG"){
          if (!triggerPassMu && !triggerPassMuMu && !triggerPassE && triggerPassEE) triggerPass=true;
        }
        if(dataset=="MuonEG"){
          if (!triggerPassMu && !triggerPassMuMu && !triggerPassE && !triggerPassEE && triggerPassEMu) triggerPass=true;
        }
      }
      if(year == "2017"){
        triggerPassMu = (HLT_IsoMu24 || HLT_IsoMu27);
        triggerPassMuMu = (HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ || HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8 || HLT_TripleMu_12_10_5);
        triggerPassE = (HLT_Ele32_WPTight_Gsf_L1DoubleEG || HLT_Ele35_WPTight_Gsf);
        triggerPassEE = (HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL ||  HLT_Ele16_Ele12_Ele8_CaloIdL_TrackIdL);
        triggerPassEMu = (HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL || HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu8_DiEle12_CaloIdL_TrackIdL || HLT_Mu8_DiEle12_CaloIdL_TrackIdL_DZ || HLT_DiMu9_Ele9_CaloIdL_TrackIdL_DZ);

        if(dataset=="SingleMuon"){
          if (triggerPassMu) triggerPass=true;
        }
        if(dataset=="DoubleMuon"){
          if (!triggerPassMu && triggerPassMuMu) triggerPass=true;
        }
        if(dataset=="SingleElectron"){
          if (!triggerPassMu && !triggerPassMuMu && triggerPassE) triggerPass=true;
        }
        if(dataset=="DoubleEG"){
          if (!triggerPassMu && !triggerPassMuMu && !triggerPassE && triggerPassEE) triggerPass=true;
        }
        if(dataset=="MuonEG"){
          if (!triggerPassMu && !triggerPassMuMu && !triggerPassE && !triggerPassEE && triggerPassEMu) triggerPass=true;
        }
      }
      if(year == "2018"){
        triggerPassMu = (HLT_IsoMu24 || HLT_IsoMu27);
        triggerPassMuMu = (HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ || HLT_Mu17_TrkIsoVVL_Mu8_TrkIsoVVL_DZ_Mass3p8 || HLT_TripleMu_12_10_5);
        triggerPassE = (HLT_Ele32_WPTight_Gsf || HLT_Ele35_WPTight_Gsf || HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL || HLT_Ele23_Ele12_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Ele16_Ele12_Ele8_CaloIdL_TrackIdL);
        triggerPassEMu = (HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL || HLT_Mu23_TrkIsoVVL_Ele12_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu12_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ ||
            HLT_Mu8_TrkIsoVVL_Ele23_CaloIdL_TrackIdL_IsoVL_DZ || HLT_Mu8_DiEle12_CaloIdL_TrackIdL ||  HLT_Mu8_DiEle12_CaloIdL_TrackIdL_DZ || HLT_DiMu9_Ele9_CaloIdL_TrackIdL_DZ);
        if(dataset=="SingleMuon"){
          if (triggerPassMu) triggerPass=true;
        }
        if(dataset=="DoubleMuon"){
          if (!triggerPassMu && triggerPassMuMu) triggerPass=true;
        }
        if(dataset=="EGamma"){
          if (!triggerPassMu && !triggerPassMuMu && triggerPassE) triggerPass=true;
        }
        if(dataset=="MuonEG"){
          if (!triggerPassMu && !triggerPassMuMu && !triggerPassE && triggerPassEMu) triggerPass=true;
        }
      }
    }
    if(!triggerPass) continue;
    if(!metFilterPass) continue;

    selectedPLeptons = new std::vector<lepton_candidate*>();
    selectedFLeptons = new std::vector<lepton_candidate*>();
    selectedLooseLeptons = new std::vector<lepton_candidate*>();
// electron
    for (int l=0;l<nElectron;l++){
      if(obj.looseElectron(l) && Electron_pt[l]>7) selectedLooseLeptons->push_back(new lepton_candidate(Electron_pt[l],Electron_eta[l],Electron_phi[l],Electron_charge[l],l,1, Electron_pdgId[l]));
      if(obj.looseElectron(l) && obj.tightElectron(l) && Electron_pt[l] >10){
        selectedPLeptons->push_back(new lepton_candidate(Electron_pt[l],Electron_eta[l],Electron_phi[l],Electron_charge[l],l,1, Electron_pdgId[l]));
        if (data == "mc"  && Electron_pt[l]>10){
          if(Electron_pt[l]>20) nominalWeights[0] = nominalWeights[0] * csetEleIdReco->evaluate({year, "sf", "RecoAbove20", Electron_eta[l],Electron_pt[l]});
          else if(Electron_pt[l]<20) nominalWeights[0] = nominalWeights[0] * csetEleIdReco->evaluate({year, "sf", "RecoBelow20", Electron_eta[l],Electron_pt[l]});
          nominalWeights[0] = nominalWeights[0] * scale_factor(&sf_eleLoose_H, abs(Electron_eta[l]),Electron_pt[l],"central",false, true);
          nominalWeights[0] = nominalWeights[0] * scale_factor(&sf_eleIsoIp_H, abs(Electron_eta[l]),Electron_pt[l],"central",false, true);
          nominalWeights[0] = nominalWeights[0] * scale_factor(&sf_eleLooseMVATight_H, abs(Electron_eta[l]),Electron_pt[l],"central",false, true);
        }
      }
      if(obj.looseElectron(l) && obj.fakeElectron(l) && !obj.tightElectron(l) && obj.conept_TTH(l,11)>10) selectedFLeptons->push_back(new lepton_candidate(obj.conept_TTH(l,11),Electron_eta[l],Electron_phi[l],Electron_charge[l],l,1, Electron_pdgId[l]));
if(checkEvent == event) cout<<"electron "<<l<<": if loose:"<<obj.looseElectron(l)<<" if FO:"<<obj.fakeElectron(l)<<" if tight:"<<obj.tightElectron(l)<< "MVA:"<<Electron_mvaTTHUL[l]<<" pt:"<<Electron_pt[l]<<":"<<Electron_charge[l]<<endl;
    }
// Muon selection
    for (int l=0;l<nMuon;l++){
      if(Muon_pt[l] > 7 && obj.looseMuon(l)) selectedLooseLeptons->push_back(new lepton_candidate(Muon_pt[l],Muon_eta[l],Muon_phi[l],Muon_charge[l],l,10, Muon_pdgId[l]));
      muPtSFRochester=1;
      if(data == "data" && Muon_pt[l]>20 && abs(Muon_eta[l])<2.4) muPtSFRochester = rc.kScaleDT(Muon_charge[l], Muon_pt[l],Muon_eta[l],Muon_phi[l], 0, 0);
      if (data == "mc" && Muon_pt[l]>20 && abs(Muon_eta[l])<2.4){
        if (Muon_genPartIdx[l]>=0 && Muon_genPartIdx[l]<=nGenPart) muPtSFRochester = rc.kSpreadMC(Muon_charge[l], Muon_pt[l],Muon_eta[l],Muon_phi[l], GenPart_pt[Muon_genPartIdx[l]],0, 0);
        if (Muon_genPartIdx[l]<0) muPtSFRochester = rc.kSmearMC(Muon_charge[l], Muon_pt[l],Muon_eta[l],Muon_phi[l], Muon_nTrackerLayers[l] , gRandom->Rndm(),0, 0);
      }
      if(obj.looseMuon(l) && obj.tightMuon(l) && muPtSFRochester * Muon_pt[l] >10){
        selectedPLeptons->push_back(new lepton_candidate(muPtSFRochester*Muon_pt[l],Muon_eta[l],Muon_phi[l],Muon_charge[l],l,10, Muon_pdgId[l]));
        if (data == "mc" && Muon_pt[l] > 15){
        nominalWeights[1] = nominalWeights[1] * csetMuReco->evaluate({year + "_UL", abs(Muon_eta[l]),  muPtSFRochester *Muon_pt[l], "sf"});
        nominalWeights[1] = nominalWeights[1] * csetMuLoose->evaluate({year + "_UL", abs(Muon_eta[l]),  muPtSFRochester *Muon_pt[l], "sf"}); 
        nominalWeights[1] = nominalWeights[1] * scale_factor(&sf_muonIsoIp_H, abs(Muon_eta[l]),muPtSFRochester *Muon_pt[l],"central",false, true);
        nominalWeights[1] = nominalWeights[1] * scale_factor(&sf_muonLooseMVATight_H, abs(Muon_eta[l]),muPtSFRochester *Muon_pt[l],"central",false, true);
        }
      }
      if(obj.looseMuon(l) && obj.fakeMuon(l) && !obj.tightMuon(l) && obj.conept_TTH(l,13)>10) selectedFLeptons->push_back(new lepton_candidate(obj.conept_TTH(l,13),Muon_eta[l],Muon_phi[l],Muon_charge[l],l,10,Muon_pdgId[l]));
if(checkEvent == event) cout<<"muon "<<l<<": if loose:"<<obj.looseMuon(l)<<" if FO:"<<obj.fakeMuon(l)<<" if tight:"<<obj.tightMuon(l)<<" MVA:"<<Muon_mvaTTHUL[l]<<" pt:"<<Muon_pt[l]<<":"<<Muon_charge[l]<<endl;
    }
    sort(selectedPLeptons->begin(), selectedPLeptons->end(), ComparePtLep);
    sort(selectedFLeptons->begin(), selectedFLeptons->end(), ComparePtLep);
//jets
    selectedJets = new std::vector<jet_candidate*>();
    for (int l=0;l<nJet;l++){
      if(Jet_jetId[l]==0) continue;
      jetlepfail = false;
      for (int i=0;i<selectedLooseLeptons->size();i++){
        if(deltaR((*selectedLooseLeptons)[i]->eta_,(*selectedLooseLeptons)[i]->phi_,Jet_eta[l],Jet_phi[l]) < 0.4 ) jetlepfail=true;
      }
      if(jetlepfail) continue;
      if(data == "mc" && abs(Jet_eta[l]) < 2.4){
        if(Jet_pt[l] >30) {
          selectedJets->push_back(new jet_candidate(Jet_pt[l],Jet_eta[l],Jet_phi[l],Jet_mass[l],Jet_btagDeepFlavB[l], year,Jet_partonFlavour[l]));
          }
        }
      if(data == "data" && Jet_pt[l] >30 && abs(Jet_eta[l]) < 2.4){
        selectedJets->push_back(new jet_candidate(Jet_pt[l],Jet_eta[l],Jet_phi[l],Jet_mass[l],Jet_btagDeepFlavB[l],year,0));
      }
    }
    sort(selectedJets->begin(), selectedJets->end(), ComparePtJet);

// Btag SF
    for (int l=0;l<selectedJets->size();l++){
      if((*selectedJets)[l]->btag_) nbjet++;
      if(data == "data") continue;
      BJetSF=csetBcJetSF->evaluate({"central", "M", 5, abs((*selectedJets)[l]->eta_),(*selectedJets)[l]->pt_});
      CJetSF=csetBcJetSF->evaluate({"central", "M", 4, abs((*selectedJets)[l]->eta_),(*selectedJets)[l]->pt_});
      LJetSF=csetLightJetSF->evaluate({"central", "M", 0, abs((*selectedJets)[l]->eta_),(*selectedJets)[l]->pt_});
      BJetEff=scale_factor(&btagEff_b_H, (*selectedJets)[l]->pt_, abs((*selectedJets)[l]->eta_),"central", true, false);
      CJetEff=scale_factor(&btagEff_c_H, (*selectedJets)[l]->pt_, abs((*selectedJets)[l]->eta_),"central", true, false);
      LJetEff=scale_factor(&btagEff_udsg_H, (*selectedJets)[l]->pt_, abs((*selectedJets)[l]->eta_),"central", true, false);

//b-quark
      if( abs((*selectedJets)[l]->flavor_) == 5){
        nbjetGen++;
        if( (*selectedJets)[l]->btag_ ) {
          P_bjet_mc = P_bjet_mc * BJetEff;
          P_bjet_data = P_bjet_data * BJetEff * BJetSF;
        }
        if( !(*selectedJets)[l]->btag_ ) {
          P_bjet_mc = P_bjet_mc * (1 - BJetEff);
          P_bjet_data = P_bjet_data * (1- (BJetEff * BJetSF));
        }
if(checkEvent == event) cout<<(*selectedJets)[l]->flavor_<<"  Btagged:"<<(*selectedJets)[l]->btag_<<"  Pt:"<<(*selectedJets)[l]->pt_<<"  eta:"<<(*selectedJets)[l]->eta_<<"  Eff:"<<BJetEff<<"  SF"<<BJetSF<<endl;
      }
//c-quark
      if( abs((*selectedJets)[l]->flavor_) == 4){
        if( (*selectedJets)[l]->btag_) {
          P_bjet_mc = P_bjet_mc * CJetEff;
          P_bjet_data = P_bjet_data * CJetEff * CJetSF;
        }
        if( !(*selectedJets)[l]->btag_ ) {
          P_bjet_mc = P_bjet_mc * (1 - CJetEff);
          P_bjet_data = P_bjet_data * (1- (CJetEff * CJetSF));
        }
if(checkEvent == event) cout<<(*selectedJets)[l]->flavor_<<"  Btagged:"<<(*selectedJets)[l]->btag_<<"  Pt:"<<(*selectedJets)[l]->pt_<<"  eta:"<<(*selectedJets)[l]->eta_<<"  Eff:"<<CJetEff<<"  SF"<<CJetSF<<endl;
      }
//light-quark
      if( abs((*selectedJets)[l]->flavor_) != 4 && abs((*selectedJets)[l]->flavor_) != 5){
        if( (*selectedJets)[l]->btag_) {
          P_bjet_mc = P_bjet_mc * LJetEff;
          P_bjet_data = P_bjet_data * LJetEff * LJetSF;
        }
        if( !(*selectedJets)[l]->btag_ ) {
          P_bjet_mc = P_bjet_mc * (1 - LJetEff);
          P_bjet_data = P_bjet_data * (1- (LJetEff * LJetSF));
        }
	if(checkEvent == event) cout<<(*selectedJets)[l]->flavor_<<"Btagged:"<<(*selectedJets)[l]->btag_<<"Pt:"<<(*selectedJets)[l]->pt_<<"eta:"<<(*selectedJets)[l]->eta_<<"Eff:"<<LJetEff<<"SF"<<LJetSF<<endl;
      }
    }

//PU reweighting
    if (data == "mc" && year == "2016preVFP") {
      nominalWeights[3] = wPU.PU_2016preVFP(int(Pileup_nTrueInt),"nominal");
    }
    if (data == "mc" && year == "2016postVFP") {
      nominalWeights[3] = wPU.PU_2016postVFP(int(Pileup_nTrueInt),"nominal");
    }
    if (data == "mc" && year == "2017") {
      nominalWeights[3] = wPU.PU_2017(int(Pileup_nTrueInt),"nominal");
    }
    if (data == "mc" && year == "2018") {
      nominalWeights[3] = wPU.PU_2018(int(Pileup_nTrueInt),"nominal");
    }
    if (data == "mc"){
        nominalWeights[4] = L1PreFiringWeight_Nom;
    }

    if (data == "mc") weight_Lumi = (1000*xs*lumi)/Nevent;

//Check if analysis cuts are passed and then categorize dilepton channels
//cout<<selectedPLeptons->size()<<"::::"<<selectedFLeptons->size()<<endl;
    for (int i=0;i<selectedPLeptons->size();i++){
      sumCharge += (*selectedPLeptons)[i]->charge_;
      sumFlavour += (*selectedPLeptons)[i]->lep_;
    }
    if(selectedPLeptons->size() ==2){ 
      if ((*selectedPLeptons)[0]->pt_ > 25 && (*selectedPLeptons)[1]->pt_ > 15) leptonPass=true;  
//opposite-sign dilepton channels 
      if (leptonPass && sumFlavour== 2 && sumCharge==0 && obj.tightCharge((*selectedPLeptons)[0]->indice_ , (*selectedPLeptons)[0]->pdgid_) && obj.tightCharge((*selectedPLeptons)[1]->indice_ , (*selectedPLeptons)[1]->pdgid_)) ch=getVecPos(channels,"EpEm");
      if (leptonPass && sumFlavour== 11 && sumCharge==0 && obj.tightCharge((*selectedPLeptons)[0]->indice_ , (*selectedPLeptons)[0]->pdgid_) && obj.tightCharge((*selectedPLeptons)[1]->indice_ , (*selectedPLeptons)[1]->pdgid_)) ch=getVecPos(channels,"EpmMUmp");
      if (leptonPass && sumFlavour== 20 && sumCharge==0 && obj.tightCharge((*selectedPLeptons)[0]->indice_ , (*selectedPLeptons)[0]->pdgid_) && obj.tightCharge((*selectedPLeptons)[1]->indice_ , (*selectedPLeptons)[1]->pdgid_)) ch=getVecPos(channels,"MUpMUm");
//same-sign dilepton channels
      if (leptonPass &&  sumCharge>0 && obj.tightCharge((*selectedPLeptons)[0]->indice_ , (*selectedPLeptons)[0]->pdgid_) && obj.tightCharge((*selectedPLeptons)[1]->indice_ , (*selectedPLeptons)[1]->pdgid_) && obj.isMatched((*selectedPLeptons)[0]->indice_ , (*selectedPLeptons)[0]->pdgid_,data, true) && obj.isMatched((*selectedPLeptons)[1]->indice_ , (*selectedPLeptons)[1]->pdgid_,data,true) ) ch=getVecPos(channels,"LLpp");
      if (leptonPass &&  sumCharge<0 && obj.tightCharge((*selectedPLeptons)[0]->indice_ , (*selectedPLeptons)[0]->pdgid_) && obj.tightCharge((*selectedPLeptons)[1]->indice_ , (*selectedPLeptons)[1]->pdgid_) && obj.isMatched((*selectedPLeptons)[0]->indice_ , (*selectedPLeptons)[0]->pdgid_,data,true) && obj.isMatched((*selectedPLeptons)[1]->indice_ , (*selectedPLeptons)[1]->pdgid_,data,true)) ch=getVecPos(channels,"LLmm");
//charged flip application regions
      if(sumFlavour== 2 && sumCharge==0){
        if (leptonPass && obj.tightCharge((*selectedPLeptons)[0]->indice_ , (*selectedPLeptons)[0]->pdgid_) && obj.tightCharge((*selectedPLeptons)[1]->indice_ , (*selectedPLeptons)[1]->pdgid_) && obj.isMatched((*selectedPLeptons)[0]->indice_ , (*selectedPLeptons)[0]->pdgid_,data,true) && obj.isMatched((*selectedPLeptons)[1]->indice_ , (*selectedPLeptons)[1]->pdgid_,data,true)) {
          chOSpp=getVecPos(channels,"LLOSpp");
          chOSmm=getVecPos(channels,"LLOSmm");
          if((*selectedPLeptons)[0]->charge_>0){
            probChOSpp= scale_factor(&cf_ele_H, (*selectedPLeptons)[1]->pt_, abs((*selectedPLeptons)[1]->eta_),"central", true, false);
            probChOSmm= scale_factor(&cf_ele_H, (*selectedPLeptons)[0]->pt_, abs((*selectedPLeptons)[0]->eta_),"central", true, false);
          }
          else{
            probChOSpp= scale_factor(&cf_ele_H, (*selectedPLeptons)[0]->pt_, abs((*selectedPLeptons)[0]->eta_),"central", true, false);
            probChOSmm= scale_factor(&cf_ele_H, (*selectedPLeptons)[1]->pt_, abs((*selectedPLeptons)[1]->eta_),"central", true, false);
          }
        }
      }
      if(sumFlavour== 11 && sumCharge==0){
        if (leptonPass && obj.tightCharge((*selectedPLeptons)[0]->indice_ , (*selectedPLeptons)[0]->pdgid_) && obj.tightCharge((*selectedPLeptons)[1]->indice_ , (*selectedPLeptons)[1]->pdgid_) && obj.isMatched((*selectedPLeptons)[0]->indice_ , (*selectedPLeptons)[0]->pdgid_,data,true) && obj.isMatched((*selectedPLeptons)[1]->indice_ , (*selectedPLeptons)[1]->pdgid_,data,true)) {
          if((*selectedPLeptons)[0]->lep_==1 && (*selectedPLeptons)[0]->charge_>0){
            chOSmm=getVecPos(channels,"LLOSmm");
            probChOSmm= scale_factor(&cf_ele_H, (*selectedPLeptons)[0]->pt_, abs((*selectedPLeptons)[0]->eta_),"central", true, false);
          }
          if((*selectedPLeptons)[0]->lep_==1 && (*selectedPLeptons)[0]->charge_<0){
            chOSpp=getVecPos(channels,"LLOSpp");
            probChOSpp= scale_factor(&cf_ele_H, (*selectedPLeptons)[0]->pt_, abs((*selectedPLeptons)[0]->eta_),"central", true, false);
          }
          if((*selectedPLeptons)[1]->lep_==1 && (*selectedPLeptons)[1]->charge_>0){
            chOSmm=getVecPos(channels,"LLOSmm");
            probChOSmm= scale_factor(&cf_ele_H, (*selectedPLeptons)[1]->pt_, abs((*selectedPLeptons)[1]->eta_),"central", true, false);
          }
          if((*selectedPLeptons)[1]->lep_==1 && (*selectedPLeptons)[1]->charge_<0){
            chOSpp=getVecPos(channels,"LLOSpp");
            probChOSpp= scale_factor(&cf_ele_H, (*selectedPLeptons)[1]->pt_, abs((*selectedPLeptons)[1]->eta_),"central", true, false);
          }
        }
      }
    }

    if((ch==getVecPos(channels,"LLmm") || ch==getVecPos(channels,"LLpp")) && nbjet==1){

//      for (int l=0;l<nGenPart;l++){
//        if(abs(GenPart_pdgId[GenPart_genPartIdxMother[GenPart_genPartIdxMother[l]]])==25) cout<<GenPart_pdgId[GenPart_genPartIdxMother[GenPart_genPartIdxMother[l]]]<<":"<<GenPart_pdgId[l]<<":"<<GenPart_pt[l]<<":"<<GenPart_eta[l]<<endl;
//        if(abs(GenPart_pdgId[GenPart_genPartIdxMother[GenPart_genPartIdxMother[l]]])==6) cout<<GenPart_pdgId[GenPart_genPartIdxMother[GenPart_genPartIdxMother[l]]]<<":"<<GenPart_pdgId[l]<<":"<<GenPart_pt[l]<<":"<<GenPart_eta[l]<<endl;
//       }
//cout<<"------------------"<<endl;
//      if(tL_tHFCNC.Pt()>0 && hL_tHFCNC.Pt()>15 && hU_tHFCNC.Pt()>15){
       jigsawThFCNC->Analyze(tL_tHFCNC, hL_tHFCNC, tB_tHFCNC, hU_tHFCNC, hD_tHFCNC, met_tHFCNC);
       JigsawWmass_tHFCNC->Fill(jigsawThFCNC->WT->GetMass());
       JigsawTmass_tHFCNC->Fill(jigsawThFCNC->T->GetMass());
       JigsawHmass_tHFCNC->Fill(jigsawThFCNC->H->GetMass());
      DRij->Fill(deltaR(hU_tHFCNC.Eta(),hU_tHFCNC.Phi(),hD_tHFCNC.Eta(),hD_tHFCNC.Phi()));
//cout<<"l1:"<<tL_tHFCNC.Pt()<<" l2:"<<hL_tHFCNC.Pt()<<" b:"<<tB_tHFCNC.Pt()<<","<<tB_tHFCNC.Eta()<<" u:"<<hU_tHFCNC.Pt()<<","<<hU_tHFCNC.Eta()<<" d:"<<hD_tHFCNC.Pt()<<","<<hD_tHFCNC.Eta()<<" met:"<<met_tHFCNC.Pt()<<endl;
      hL_tHFCNC.SetPtEtaPhiM(0,0,0,0); hNu_tHFCNC.SetPtEtaPhiM(0,0,0,0); hU_tHFCNC.SetPtEtaPhiM(0,0,0,0); hD_tHFCNC.SetPtEtaPhiM(0,0,0,0); tNu_tHFCNC.SetPtEtaPhiM(0,0,0,0); tB_tHFCNC.SetPtEtaPhiM(0,0,0,0); tL_tHFCNC.SetPtEtaPhiM(0,0,0,0);
//cout<<endl;     
//cout<<"Wmass="<<jigsawThFCNC->WT->GetMass()<<" Higgs mass="<<jigsawThFCNC->H->GetMass()<<" TopMass="<<jigsawThFCNC->T->GetMass()<<endl;
      for (int l=0;l<selectedJets->size();l++){
        if((*selectedJets)[l]->btag_){
          tB_tHFCNC=(*selectedJets)[l]->p4_;
          break;
        }
      }
    bool fjet=false;
    for (int l=0;l<nFatJet;l++){
      if(abs(FatJet_eta[l]) > 2.4 ||  FatJet_jetId[l]<6) continue;
      if(FatJet_particleNet_WvsQCD[l]>0.71){
           fjet=true;
           hU_tHFCNC.SetPtEtaPhiM(SubJet_pt[FatJet_subJetIdx1[l]], SubJet_eta[FatJet_subJetIdx1[l]], SubJet_phi[FatJet_subJetIdx1[l]], SubJet_mass[FatJet_subJetIdx1[l]]);
           hD_tHFCNC.SetPtEtaPhiM(SubJet_pt[FatJet_subJetIdx2[l]], SubJet_eta[FatJet_subJetIdx2[l]], SubJet_phi[FatJet_subJetIdx2[l]], SubJet_mass[FatJet_subJetIdx2[l]]);
           break;
      }
    } 
    if(!fjet){
      float bestMass=10000;
      for (int i=0;i<selectedJets->size();i++){
        if(selectedJets->size()==2 && !(*selectedJets)[i]->btag_) hU_tHFCNC=(*selectedJets)[i]->p4_;
//cout<<i<<":"<<(*selectedJets)[i]->pt_<<":"<<(*selectedJets)[i]->eta_<<endl;
        for (int j=i+1;j<selectedJets->size();j++){
          if((*selectedJets)[i]->btag_ || (*selectedJets)[j]->btag_) continue;
          if(abs(((*selectedJets)[i]->p4_ + (*selectedJets)[j]->p4_).M()-80)<bestMass){
            hU_tHFCNC=(*selectedJets)[i]->p4_; hD_tHFCNC=(*selectedJets)[j]->p4_;
            bestMass=((*selectedJets)[i]->p4_ + (*selectedJets)[j]->p4_).M();
          }
       }
      } 
      }
//if(fjet) cout<<"W jet:"<<(hU_tHFCNC+hD_tHFCNC).M()<<" :"<<selectedJets->size()<<endl;
//else cout<<(hU_tHFCNC+hD_tHFCNC).M()<<" :"<<selectedJets->size()<<endl;

      met_tHFCNC.SetPtEtaPhiM(MET_pt,0,MET_phi,0);
      tL_tHFCNC=(*selectedPLeptons)[0]->p4_;
      hL_tHFCNC=(*selectedPLeptons)[1]->p4_;
      jigsawThFCNC->Analyze(tL_tHFCNC, hL_tHFCNC, tB_tHFCNC, hU_tHFCNC, hD_tHFCNC, met_tHFCNC);
      JigsawWmassReco_tHFCNC->Fill(jigsawThFCNC->WT->GetMass());
      JigsawTmassReco_tHFCNC->Fill(jigsawThFCNC->T->GetMass());
      JigsawHmassReco_tHFCNC->Fill(jigsawThFCNC->H->GetMass());

      topMass_=jigsawThFCNC->T->GetMass();
      HZMass_=jigsawThFCNC->H->GetMass();
      WtopMass_=jigsawThFCNC->WT->GetMass();
      W1HMass_=jigsawThFCNC->W1H->GetMass();
      W2HMass_=jigsawThFCNC->W2H->GetMass();
      HZPt_=jigsawThFCNC->H->GetFourVector().Pt();
      HZEta_=jigsawThFCNC->H->GetFourVector().Eta();
      topPt_=jigsawThFCNC->T->GetFourVector().Pt();
      topEta_=jigsawThFCNC->T->GetFourVector().Eta();
      drWtopB_=deltaR(jigsawThFCNC->WT->GetFourVector().Eta(),jigsawThFCNC->WT->GetFourVector().Phi(),tB_tHFCNC.Eta(),tB_tHFCNC.Phi());
      drW1HW2H_=deltaR(jigsawThFCNC->W1H->GetFourVector().Eta(),jigsawThFCNC->W1H->GetFourVector().Phi(),jigsawThFCNC->W2H->GetFourVector().Eta(),jigsawThFCNC->W2H->GetFourVector().Phi());

HmassVsnJet->Fill(jigsawThFCNC->H->GetMass(),selectedJets->size());
DRtH->Fill(deltaR(jigsawThFCNC->T->GetFourVector().Eta(),jigsawThFCNC->T->GetFourVector().Phi(),jigsawThFCNC->H->GetFourVector().Eta(),jigsawThFCNC->H->GetFourVector().Phi()));
DPhitH->Fill(deltaPhi(jigsawThFCNC->T->GetFourVector().Phi(),jigsawThFCNC->H->GetFourVector().Phi()));
DRWHWH->Fill(deltaR(jigsawThFCNC->W1H->GetFourVector().Eta(),jigsawThFCNC->W1H->GetFourVector().Phi(),jigsawThFCNC->W2H->GetFourVector().Eta(),jigsawThFCNC->W2H->GetFourVector().Phi()));
//cout<<fjet<<endl;
//cout<<"l1:"<<tL_tHFCNC.Pt()<<" l2:"<<hL_tHFCNC.Pt()<<" b:"<<tB_tHFCNC.Pt()<<","<<tB_tHFCNC.Eta()<<" u:"<<hU_tHFCNC.Pt()<<","<<hU_tHFCNC.Eta()<<" d:"<<hD_tHFCNC.Pt()<<","<<hD_tHFCNC.Eta()<<" met:"<<met_tHFCNC.Pt()<<endl;
//cout<<"Wmass="<<jigsawThFCNC->WT->GetMass()<<" Higgs mass="<<jigsawThFCNC->H->GetMass()<<" TopMass="<<jigsawThFCNC->T->GetMass()<<endl;
//      }
     }
    if(selectedPLeptons->size() ==3){
      if ((*selectedPLeptons)[0]->pt_ > 25 && (*selectedPLeptons)[1]->pt_ > 15) leptonPass=true;
      if((*selectedPLeptons)[2]->lep_== 1 && (*selectedPLeptons)[2]->pt_ <15) leptonPass=false;
      for (int i=0;i<selectedPLeptons->size();i++){
        for (int j=i+1;j<selectedPLeptons->size();j++){
          if(((*selectedPLeptons)[i]->lep_ + (*selectedPLeptons)[j]->lep_ == 2 || (*selectedPLeptons)[i]->lep_ + (*selectedPLeptons)[j]->lep_ == 20) && 
             (*selectedPLeptons)[i]->charge_ + (*selectedPLeptons)[j]->charge_ ==0 && 
             abs(((*selectedPLeptons)[i]->p4_ + (*selectedPLeptons)[j]->p4_).M() - 91.1876)<10){
               onZ=true;
               lZ1=i;
               lZ2=j;
          }
        }
      }

      if (leptonPass && onZ && obj.isMatched((*selectedPLeptons)[0]->indice_ , (*selectedPLeptons)[0]->pdgid_,data,false) && obj.isMatched((*selectedPLeptons)[1]->indice_ , (*selectedPLeptons)[1]->pdgid_,data,false)  && obj.isMatched((*selectedPLeptons)[2]->indice_ , (*selectedPLeptons)[2]->pdgid_,data,false)) ch=getVecPos(channels,"3LonZ");
      if (leptonPass && !onZ && sumCharge>0 && obj.isMatched((*selectedPLeptons)[0]->indice_ , (*selectedPLeptons)[0]->pdgid_,data,false) && obj.isMatched((*selectedPLeptons)[1]->indice_ , (*selectedPLeptons)[1]->pdgid_,data,false)  && obj.isMatched((*selectedPLeptons)[2]->indice_ , (*selectedPLeptons)[2]->pdgid_,data,false)) ch=getVecPos(channels,"3LoffZp");
      if (leptonPass && !onZ && sumCharge<0 && obj.isMatched((*selectedPLeptons)[0]->indice_ , (*selectedPLeptons)[0]->pdgid_,data,false) && obj.isMatched((*selectedPLeptons)[1]->indice_ , (*selectedPLeptons)[1]->pdgid_,data,false)  && obj.isMatched((*selectedPLeptons)[2]->indice_ , (*selectedPLeptons)[2]->pdgid_,data,false)) ch=getVecPos(channels,"3LoffZm");
      if(ch==getVecPos(channels,"3LonZ") && nbjet==1){
        Z_tZFCNC.SetPtEtaPhiM(0,0,0,0); top_tZFCNC.SetPtEtaPhiM(0,0,0,0); bt_tZFCNC.SetPtEtaPhiM(0,0,0,0); Wt_tZFCNC.SetPtEtaPhiM(0,0,0,0); lt_tZFCNC.SetPtEtaPhiM(0,0,0,0); lpZ_tZFCNC.SetPtEtaPhiM(0,0,0,0); lmZ_tZFCNC.SetPtEtaPhiM(0,0,0,0);
        lpZ_tZFCNC.SetPtEtaPhiM((*selectedPLeptons)[lZ1]->pt_,(*selectedPLeptons)[lZ1]->eta_,(*selectedPLeptons)[lZ1]->phi_,0);
        lmZ_tZFCNC.SetPtEtaPhiM((*selectedPLeptons)[lZ2]->pt_,(*selectedPLeptons)[lZ2]->eta_,(*selectedPLeptons)[lZ2]->phi_,0);
        lt_tZFCNC.SetPtEtaPhiM((*selectedPLeptons)[3-lZ1-lZ2]->pt_,(*selectedPLeptons)[3-lZ1-lZ2]->eta_,(*selectedPLeptons)[3-lZ1-lZ2]->phi_,0);
        for (int l=0;l<selectedJets->size();l++){
          if((*selectedJets)[l]->btag_) bt_tZFCNC.SetPtEtaPhiM((*selectedJets)[l]->pt_,(*selectedJets)[l]->eta_,(*selectedJets)[l]->phi_,0);
        }
        nut_tZFCNC.SetPtEtaPhiM(MET_pt,0,MET_phi,0);
        jigsawTzFCNC->Analyze(lt_tZFCNC, lpZ_tZFCNC, lmZ_tZFCNC, bt_tZFCNC,nut_tZFCNC);
        JigsawWmassReco->Fill(jigsawTzFCNC->W->GetMass());
        JigsawTmassReco->Fill(jigsawTzFCNC->T->GetMass());
      }
    }
    if(selectedPLeptons->size() > 3 ){
      if ((*selectedPLeptons)[0]->pt_ > 25 && (*selectedPLeptons)[1]->pt_ > 15) leptonPass=true;
      if(((*selectedPLeptons)[2]->lep_== 1 && (*selectedPLeptons)[2]->pt_ <15) || ((*selectedPLeptons)[3]->lep_== 1 && (*selectedPLeptons)[3]->pt_ <15)) leptonPass=false;
      if (leptonPass) ch=getVecPos(channels,"4L");
    }

    selectedLeptons = new std::vector<lepton_candidate*>();
    selectedLeptons->insert(selectedLeptons->end(), selectedPLeptons->begin(), selectedPLeptons->end());
    selectedLeptons->insert(selectedLeptons->end(), selectedFLeptons->begin(), selectedFLeptons->end());
    sort(selectedLeptons->begin(), selectedLeptons->end(), ComparePtLep);
    if(selectedFLeptons->size()==1){
      sumCharge=0;
      sumFlavour=0;
      leptonPass=false;
      onZ=false;
      for (int i=0;i<selectedLeptons->size();i++){
        sumCharge += (*selectedLeptons)[i]->charge_;
        sumFlavour += (*selectedLeptons)[i]->lep_;
      }
      if(selectedPLeptons->size() ==1){
        if ((*selectedLeptons)[0]->pt_ > 25 && (*selectedLeptons)[1]->pt_ > 15) leptonPass=true;
        if (leptonPass &&  sumCharge>0 && obj.tightCharge((*selectedLeptons)[0]->indice_ , (*selectedLeptons)[0]->pdgid_) && obj.tightCharge((*selectedLeptons)[1]->indice_ , (*selectedLeptons)[1]->pdgid_)) ch=getVecPos(channels,"LFpp");
        if (leptonPass &&  sumCharge<0  && obj.tightCharge((*selectedLeptons)[0]->indice_ , (*selectedLeptons)[0]->pdgid_) && obj.tightCharge((*selectedLeptons)[1]->indice_ , (*selectedLeptons)[1]->pdgid_) ) ch=getVecPos(channels,"LFmm");
      }

      if(selectedPLeptons->size() ==2){
        if ((*selectedLeptons)[0]->pt_ > 25 && (*selectedLeptons)[1]->pt_ > 15) leptonPass=true;
        if((*selectedLeptons)[2]->lep_== 1 && (*selectedLeptons)[2]->pt_ <15) leptonPass=false;
        for (int i=0;i<selectedLeptons->size();i++){
          for (int j=i+1;j<selectedLeptons->size();j++){
            if(((*selectedLeptons)[i]->lep_ + (*selectedLeptons)[j]->lep_ == 2 || (*selectedLeptons)[i]->lep_ + (*selectedLeptons)[j]->lep_ == 20) &&
               (*selectedLeptons)[i]->charge_ + (*selectedLeptons)[j]->charge_ ==0 &&
               abs(((*selectedLeptons)[i]->p4_ + (*selectedLeptons)[j]->p4_).M() - 91.1876)<10) onZ=true;
          }
        }

        if (leptonPass && onZ) ch=getVecPos(channels,"LLFonZ");
        if (leptonPass && !onZ && sumCharge>0 ) ch=getVecPos(channels,"LLFoffZp");
        if (leptonPass && !onZ && sumCharge<0 ) ch=getVecPos(channels,"LLFoffZm");
      }
    }

    if(selectedFLeptons->size()==2){
      sumCharge=0;
      sumFlavour=0;
      leptonPass=false;
      onZ=false;
      for (int i=0;i<selectedLeptons->size();i++){
        sumCharge += (*selectedLeptons)[i]->charge_;
        sumFlavour += (*selectedLeptons)[i]->lep_;
      }
      if(selectedPLeptons->size() ==0){
        if ((*selectedLeptons)[0]->pt_ > 25 && (*selectedLeptons)[1]->pt_ > 15) leptonPass=true;
        if (leptonPass &&  sumCharge>0 && obj.tightCharge((*selectedLeptons)[0]->indice_ , (*selectedLeptons)[0]->pdgid_) && obj.tightCharge((*selectedLeptons)[1]->indice_ , (*selectedLeptons)[1]->pdgid_) ) ch=getVecPos(channels,"FFpp");
        if (leptonPass &&  sumCharge<0 && obj.tightCharge((*selectedLeptons)[0]->indice_ , (*selectedLeptons)[0]->pdgid_) && obj.tightCharge((*selectedLeptons)[1]->indice_ , (*selectedLeptons)[1]->pdgid_)) ch=getVecPos(channels,"FFmm");
      }

      if(selectedPLeptons->size() ==1){
        if ((*selectedLeptons)[0]->pt_ > 25 && (*selectedLeptons)[1]->pt_ > 15) leptonPass=true;
        if((*selectedLeptons)[2]->lep_== 1 && (*selectedLeptons)[2]->pt_ <15) leptonPass=false;
        for (int i=0;i<selectedLeptons->size();i++){
          for (int j=i+1;j<selectedLeptons->size();j++){
            if(((*selectedLeptons)[i]->lep_ + (*selectedLeptons)[j]->lep_ == 2 || (*selectedLeptons)[i]->lep_ + (*selectedLeptons)[j]->lep_ == 20) &&
               (*selectedLeptons)[i]->charge_ + (*selectedLeptons)[j]->charge_ ==0 &&
               abs(((*selectedLeptons)[i]->p4_ + (*selectedLeptons)[j]->p4_).M() - 91.1876)<10) onZ=true;
          }
        }

        if (leptonPass && onZ) ch=getVecPos(channels,"LFFonZ");
        if (leptonPass && !onZ && sumCharge>0 ) ch=getVecPos(channels,"LFFoffZp");
        if (leptonPass && !onZ && sumCharge<0 ) ch=getVecPos(channels,"LFFoffZm");
      }
   }

    if(selectedFLeptons->size()==3){
      sumCharge=0;
      sumFlavour=0;
      leptonPass=false;
      onZ=false;
      for (int i=0;i<selectedLeptons->size();i++){
        sumCharge += (*selectedLeptons)[i]->charge_;
        sumFlavour += (*selectedLeptons)[i]->lep_;
      }
      if(selectedPLeptons->size() ==0){
        if ((*selectedLeptons)[0]->pt_ > 25 && (*selectedLeptons)[1]->pt_ > 15) leptonPass=true;
        if((*selectedLeptons)[2]->lep_== 1 && (*selectedLeptons)[2]->pt_ <15) leptonPass=false;
        for (int i=0;i<selectedLeptons->size();i++){
          for (int j=i+1;j<selectedLeptons->size();j++){
            if(((*selectedLeptons)[i]->lep_ + (*selectedLeptons)[j]->lep_ == 2 || (*selectedLeptons)[i]->lep_ + (*selectedLeptons)[j]->lep_ == 20) &&
               (*selectedLeptons)[i]->charge_ + (*selectedLeptons)[j]->charge_ ==0 &&
               abs(((*selectedLeptons)[i]->p4_ + (*selectedLeptons)[j]->p4_).M() - 91.1876)<10) onZ=true;
          }
        }

        if (leptonPass && onZ) ch=getVecPos(channels,"FFFonZ");
        if (leptonPass && !onZ && sumCharge>0 ) ch=getVecPos(channels,"FFFoffZp");
        if (leptonPass && !onZ && sumCharge<0 ) ch=getVecPos(channels,"FFFoffZm");
      }
   }
/*
if(event==157045400) {
cout<<event<<":ch:"<<ch<<":SPL:"<<selectedPLeptons->size()<<":SFL:"<<selectedFLeptons->size()<<":ch:"<<channels[ch]<<":"<<obj.tightCharge((*selectedLeptons)[0]->indice_ , (*selectedLeptons)[0]->pdgid_)<<":"<<obj.tightCharge((*selectedLeptons)[1]->indice_ , (*selectedLeptons)[1]->pdgid_)<<leptonPass<<sumCharge<<endl;
cout<<(*selectedLeptons)[0]->lep_<<":"<<(*selectedLeptons)[0]->pt_<<endl;
cout<<(*selectedLeptons)[1]->lep_<<":"<<(*selectedLeptons)[1]->pt_<<endl;
}
*/
//if (ch==getVecPos(channels,"LFpp")) cout<<run<<":"<<luminosityBlock<<":"<<event<<endl;
   if(ch>30) {
     for (int l=0;l<selectedPLeptons->size();l++){
     delete (*selectedPLeptons)[l];
     }
     selectedPLeptons->clear();
     selectedPLeptons->shrink_to_fit();
     delete selectedPLeptons;
     for (int l=0;l<selectedFLeptons->size();l++){
     delete (*selectedFLeptons)[l];
     }
     selectedFLeptons->clear();
     selectedFLeptons->shrink_to_fit();
     delete selectedFLeptons;
     selectedLeptons->clear();
     selectedLeptons->shrink_to_fit();
     delete selectedLeptons;
     for (int l=0;l<selectedJets->size();l++){
       delete (*selectedJets)[l];
     }
     selectedJets->clear();
     selectedJets->shrink_to_fit();
     delete selectedJets;
     for (int l=0;l<selectedLooseLeptons->size();l++){
     delete (*selectedLooseLeptons)[l];
     }
     selectedLooseLeptons->clear();
     selectedLooseLeptons->shrink_to_fit();
     delete selectedLooseLeptons;
     continue;
  }
//Fill histograms
   if (data == "mc"){
//calculate the trigger SFs
     if (channels[ch]=="LLpp" || channels[ch]=="LLmm" || channels[ch]=="EpEm" || channels[ch]=="MUpMUm" || channels[ch]=="EpmMUmp"){
       if((*selectedPLeptons)[0]->lep_ + (*selectedPLeptons)[1]->lep_ == 2) nominalWeights[2] = scale_factor(&sf_triggeree_H, (*selectedPLeptons)[0]->pt_,(*selectedPLeptons)[1]->pt_,"central",false, true);
       if((*selectedPLeptons)[0]->lep_ + (*selectedPLeptons)[1]->lep_ == 11) nominalWeights[2] = scale_factor(&sf_triggeremu_H, (*selectedPLeptons)[0]->pt_,(*selectedPLeptons)[1]->pt_,"central",false, true);
       if((*selectedPLeptons)[0]->lep_ + (*selectedPLeptons)[1]->lep_ == 20) nominalWeights[2] = scale_factor(&sf_triggermumu_H, (*selectedPLeptons)[0]->pt_,(*selectedPLeptons)[1]->pt_,"central",false, true);
     }
//correct for the electron SF in the dilepton regions
     if (channels[ch]=="LLpp" || channels[ch]=="LLmm" || channels[ch]=="EpEm" || channels[ch]=="MUpMUm" || channels[ch]=="EpmMUmp"){
       for (int i=0;i<selectedPLeptons->size();i++){
         nominalWeights[0] = nominalWeights[0] * (scale_factor(&sf_eleLooseMVATight2lss_H, abs((*selectedPLeptons)[i]->eta_),(*selectedPLeptons)[i]->pt_,"central",false, true)/scale_factor(&sf_eleLooseMVATight_H, abs((*selectedPLeptons)[i]->eta_),(*selectedPLeptons)[i]->pt_,"central",false, true));
       }
     }
     if (ch==getVecPos(channels,"EpEm")) sumWeight =  sumWeight + weight_Lumi * signnum_typical(LHEWeight_originalXWGTUP);
     weight_lep  = weight_Lumi * signnum_typical(LHEWeight_originalXWGTUP)*nominalWeights[0]*nominalWeights[1]*nominalWeights[2]*nominalWeights[3]*nominalWeights[4]; // * sf_Ele_Reco * sf_Ele_ID * sf_Mu_ID * sf_Mu_ISO * sf_Trigger * weight_PU * weight_prefiring * weight_topPtPowheg * ttKFactor * sf_JetPuId;
     weight_lepB = weight_lep* (P_bjet_data/P_bjet_mc);
     weight_EFT = lumi * (1000.0/nRuns)*nominalWeights[0]*nominalWeights[1]*nominalWeights[2]*nominalWeights[3]*nominalWeights[4]*(P_bjet_data/P_bjet_mc);//  * sf_Ele_Reco * sf_Ele_ID * sf_Mu_ID * sf_Mu_ISO* (P_bjet_data/P_bjet_mc) * sf_Trigger * weight_PU * weight_prefiring * weight_topPtPowheg * ttKFactor * sf_JetPuId;
   }
   for (int i=0;i<selectedFLeptons->size();i++){
     if ((*selectedFLeptons)[i]->lep_ == 1) fi = scale_factor(&fr_ele_H, (*selectedFLeptons)[i]->pt_, abs((*selectedFLeptons)[i]->eta_),"central", true, false);
     else fi =scale_factor(&fr_mu_H, (*selectedFLeptons)[i]->pt_, abs((*selectedFLeptons)[i]->eta_),"central", true, false);
     fakeRate=fakeRate*(fi/(1-fi));
   }
   if (channels[ch].Contains("F")){
       weight_lep=weight_lep*fakeRate;
       weight_lepB=weight_lepB*fakeRate;
   }
   if (iseft) eft_fit = new WCFit(nWCnames, wc_names_lst, nEFTfitCoefficients, EFTfitCoefficients, weight_EFT);
   else eft_fit = new WCFit(0,wc_names_lst,1, &genWeight, 1.0);
//   if (ch<10) cout<<ch<<":"<<eft_fit->evalPoint(A)<<endl;
   resetVecInt(reg);
   resetVecInt(allCh);
   allCh[0]=ch;
   if(chOSmm<30) allCh[1]= chOSmm;   
   if(chOSpp<30) allCh[2]=chOSpp;
   reg[0]=0;
   wgt[0][0]=weight_lep;
   wgt[1][0]=weight_lep*probChOSmm*chargeFlipNorm;
   wgt[2][0]=weight_lep*probChOSpp*chargeFlipNorm;
   wcfit[0][0]= *eft_fit;
   wcfit[1][0]= *eft_fit;
   wcfit[2][0]= *eft_fit;
   if(nbjet==0){
     reg[1]=1;
     wgt[0][1]=weight_lepB;
     wgt[1][1]=weight_lepB*probChOSmm*chargeFlipNorm;
     wgt[2][1]=weight_lepB*probChOSpp*chargeFlipNorm;
     wcfit[0][1]= *eft_fit;
     wcfit[1][1]= *eft_fit;
     wcfit[2][1]= *eft_fit;
   }
   if(nbjet==1){
     reg[2]=2;
     wgt[0][2]=weight_lepB;
     wgt[1][2]=weight_lepB*probChOSmm*chargeFlipNorm;
     wgt[2][2]=weight_lepB*probChOSpp*chargeFlipNorm;
     wcfit[0][2]= *eft_fit;
     wcfit[1][2]= *eft_fit;
     wcfit[2][2]= *eft_fit;
   }
   if(nbjet>1){
     reg[3]=3;
     wgt[0][3]=weight_lepB;
     wgt[1][3]=weight_lepB*probChOSmm*chargeFlipNorm;
     wgt[2][3]=weight_lepB*probChOSpp*chargeFlipNorm;
     wcfit[0][3]= *eft_fit;
     wcfit[1][3]= *eft_fit;
     wcfit[2][3]= *eft_fit;
   }
  
   FillD3Hists(Hists, allCh, reg, vInd(vars,"lep1Pt"), (*selectedLeptons)[0]->pt_ ,wgt, wcfit);
   FillD3Hists(Hists, allCh, reg, vInd(vars,"lep1Eta"), (*selectedLeptons)[0]->eta_ ,wgt, wcfit); 
   FillD3Hists(Hists, allCh, reg, vInd(vars,"lep1Phi"), (*selectedLeptons)[0]->phi_ ,wgt, wcfit); 
   FillD3Hists(Hists, allCh, reg, vInd(vars,"lep2Pt"), (*selectedLeptons)[1]->pt_ ,wgt, wcfit); 
   FillD3Hists(Hists, allCh, reg, vInd(vars,"lep2Eta"), (*selectedLeptons)[1]->eta_ ,wgt, wcfit); 
   FillD3Hists(Hists, allCh, reg, vInd(vars,"lep2Phi"), (*selectedLeptons)[1]->phi_ ,wgt, wcfit); 
   FillD3Hists(Hists, allCh, reg, vInd(vars,"llM"), ((*selectedLeptons)[0]->p4_ + (*selectedLeptons)[1]->p4_).M() ,wgt, wcfit); 
   FillD3Hists(Hists, allCh, reg, vInd(vars,"llPt"), ((*selectedLeptons)[0]->p4_ + (*selectedLeptons)[1]->p4_).Pt() ,wgt, wcfit); 
   FillD3Hists(Hists, allCh, reg, vInd(vars,"llDr"), deltaR((*selectedLeptons)[0]->eta_,(*selectedLeptons)[0]->phi_,(*selectedLeptons)[1]->eta_,(*selectedLeptons)[1]->phi_) ,wgt, wcfit); 
   FillD3Hists(Hists, allCh, reg, vInd(vars,"llDphi"), abs(deltaPhi((*selectedLeptons)[0]->phi_,(*selectedLeptons)[1]->phi_)) ,wgt, wcfit); 
   FillD3Hists(Hists, allCh, reg, vInd(vars,"njet"), selectedJets->size() ,wgt, wcfit); 
   FillD3Hists(Hists, allCh, reg, vInd(vars,"nbjet"), nbjet ,wgt, wcfit); 
   FillD3Hists(Hists, allCh, reg, vInd(vars,"Met"), MET_pt ,wgt, wcfit);
   FillD3Hists(Hists, allCh, reg, vInd(vars,"MetPhi"), MET_phi ,wgt, wcfit);
   FillD3Hists(Hists, allCh, reg, vInd(vars,"nVtx"), PV_npvs ,wgt, wcfit);
   FillD3Hists(Hists, allCh, reg, vInd(vars,"llMZw"), ((*selectedLeptons)[0]->p4_ + (*selectedLeptons)[1]->p4_).M() ,wgt, wcfit);
   if(selectedJets->size()>0){
     FillD3Hists(Hists, allCh, reg, vInd(vars,"jet1Pt"), (*selectedJets)[0]->pt_ ,wgt, wcfit);
     FillD3Hists(Hists, allCh, reg, vInd(vars,"jet1Eta"), (*selectedJets)[0]->eta_ ,wgt, wcfit);
     FillD3Hists(Hists, allCh, reg, vInd(vars,"jet1Phi"), (*selectedJets)[0]->phi_ ,wgt, wcfit);
   }

   if(nbjet==1){
     lep1Pt_= (*selectedLeptons)[0]->pt_;
     lep1Eta_= (*selectedLeptons)[0]->eta_;
     lep2Pt_= (*selectedLeptons)[1]->pt_;
     lep2Eta_= (*selectedLeptons)[1]->eta_;
     llM_= ((*selectedLeptons)[0]->p4_ + (*selectedLeptons)[1]->p4_).M();
     llPt_=  ((*selectedLeptons)[0]->p4_ + (*selectedLeptons)[1]->p4_).Pt();
     llDr_= deltaR((*selectedLeptons)[0]->eta_,(*selectedLeptons)[0]->phi_,(*selectedLeptons)[1]->eta_,(*selectedLeptons)[1]->phi_);
     llDphi_= abs(deltaPhi((*selectedLeptons)[0]->phi_,(*selectedLeptons)[1]->phi_));
     if(selectedLeptons->size()>2){
       lep3Pt_= (*selectedLeptons)[2]->pt_;
       lep3Eta_= (*selectedLeptons)[2]->eta_;
     }
     nJets_=selectedJets->size();
     jet1Pt_=0;
     jet1Eta_=-999;
     if(selectedJets->size()>0){
       jet1Pt_=(*selectedJets)[0]->pt_;
       jet1Eta_=(*selectedJets)[0]->eta_;
      for (int l=0;l<selectedJets->size();l++){
        if((*selectedJets)[l]->btag_){
          bJetPt_=(*selectedJets)[l]->pt_;
          bJetEta_=(*selectedJets)[l]->eta_;
          break;
        }
      }
     }
     ch_=ch;
     weightSM_=weight_lepB;
     weightctp_ = eft_fit->evalPoint("ctp",1);
     weightctlS_= eft_fit->evalPoint("ctlS",1);
     weightcte_= eft_fit->evalPoint("cte",1);
     weightctl_= eft_fit->evalPoint("ctl",1);
     weightctlT_= eft_fit->evalPoint("ctlT",1);
     weightctZ_= eft_fit->evalPoint("ctZ",1);
     weightcpt_= eft_fit->evalPoint("cpt",1);
     weightcpQM_= eft_fit->evalPoint("cpQM",1);
     weightctA_= eft_fit->evalPoint("ctA",1);
     weightcQe_= eft_fit->evalPoint("cQe",1);
     weightctG_= eft_fit->evalPoint("ctG",1);
     weightcQlM_= eft_fit->evalPoint("cQlM",1);
     tree_out.Fill();
   }

   delete eft_fit;

   for (int l=0;l<selectedPLeptons->size();l++){
   delete (*selectedPLeptons)[l];
   }
   selectedPLeptons->clear();
   selectedPLeptons->shrink_to_fit();
   delete selectedPLeptons;
   for (int l=0;l<selectedFLeptons->size();l++){
   delete (*selectedFLeptons)[l];
   }
   selectedFLeptons->clear();
   selectedFLeptons->shrink_to_fit();
   delete selectedFLeptons;
   selectedLeptons->clear();
   selectedLeptons->shrink_to_fit();
   delete selectedLeptons;
   for (int l=0;l<selectedJets->size();l++){
     delete (*selectedJets)[l];
   }
   selectedJets->clear();
   selectedJets->shrink_to_fit();
   delete selectedJets;
     for (int l=0;l<selectedLooseLeptons->size();l++){
     delete (*selectedLooseLeptons)[l];
     }
     selectedLooseLeptons->clear();
     selectedLooseLeptons->shrink_to_fit();
     delete selectedLooseLeptons;
     continue;
  }
  cout<<"Loop is completed"<<endl;
  cout<<"from "<<ntr<<" events, "<<nAccept<<" events are accepted"<<endl;

  TFile file_out ("ANoutput.root","RECREATE");
  for (int i=0;i<channels.size();++i){
    for (int k=0;k<regions.size();++k){
      for (int l=0;l<vars.size();++l){
        Hists[i][k][l]  ->Write("",TObject::kOverwrite);
      }
    }
  }

  h2_BTaggingEff_Denom_b   ->Write("",TObject::kOverwrite);
  h2_BTaggingEff_Denom_c   ->Write("",TObject::kOverwrite);
  h2_BTaggingEff_Denom_udsg->Write("",TObject::kOverwrite);
  h2_BTaggingEff_Num_b     ->Write("",TObject::kOverwrite);
  h2_BTaggingEff_Num_c     ->Write("",TObject::kOverwrite);
  h2_BTaggingEff_Num_udsg  ->Write("",TObject::kOverwrite);
  crossSection             ->Write("",TObject::kOverwrite);

  JigsawWmass->Write("",TObject::kOverwrite);
  JigsawTmass->Write("",TObject::kOverwrite);
  JigsawWmassReco->Write("",TObject::kOverwrite);
  JigsawTmassReco->Write("",TObject::kOverwrite);

  JigsawWmass_tHFCNC->Write("",TObject::kOverwrite);
  JigsawTmass_tHFCNC->Write("",TObject::kOverwrite);
  JigsawHmass_tHFCNC->Write("",TObject::kOverwrite);
  JigsawWmassReco_tHFCNC->Write("",TObject::kOverwrite);
  JigsawTmassReco_tHFCNC->Write("",TObject::kOverwrite);
  JigsawHmassReco_tHFCNC->Write("",TObject::kOverwrite);
  DRij->Write("",TObject::kOverwrite);
  DRtH->Write("",TObject::kOverwrite);
  DPhitH->Write("",TObject::kOverwrite);
  DRWHWH->Write("",TObject::kOverwrite);
  HmassVsnJet->Write("",TObject::kOverwrite);

  genAnalysis.writeGENHists();
  tree_out.Write() ; 
  file_out.Close() ;
  cout<<"Cleaning the memory"<<endl;
  Hists.clear();
  cout<<"Job is finished"<<endl;
  cout<<"some of weight="<<sumWeight<<endl;

cout<<"Total Virtual Memory: "<<getValue()<<endl;

}


void MyAnalysis::FillD3Hists(D3HistsContainer H3, std::vector<int> v1, std::vector<int> v2, int v3, float value, std::vector<std::vector<float>> weight, std::vector<std::vector<WCFit>> wcfit){
  for (int i = 0; i < v1.size(); ++i) {
    for (int j = 0; j < v2.size(); ++j) {
      if(v1[i]<0 || v2[j]<0) continue;
      H3[v1[i]][v2[j]][v3]->Fill(value, weight[i][j], wcfit[i][j]);
    }
  }
}

void MyAnalysis::FillD4Hists(D4HistsContainer H4, int v1, std::vector<int> v2, int v3, int v4, float value, std::vector<float> weight, std::vector<WCFit> wcfit){
  for (int i = 0; i < v2.size(); ++i) {
    H4[v1][v2[i]][v3][v4]->Fill(value, weight[i], wcfit[i]);
  }
}
