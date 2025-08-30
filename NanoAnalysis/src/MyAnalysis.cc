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
#if not defined(__CINT__) || defined(__MAKECINT__)
#include "TMVA/Tools.h"
#include "TMVA/Reader.h"
#include "TMVA/MethodCuts.h"
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
#include <TFileMerger.h>
#include <malloc.h>
#include <thread>
#include <sys/resource.h>

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
  for (size_t i=0;i<K.size();++i){
    K[i]=-1;
  }
}

void resetVecIntofInt(std::vector<std::vector<int>> &K){
  for (size_t i=0;i<K.size();++i){
    for (size_t j=0;j<K[i].size();++j){
      K[i][j]=-1;
    }
  }
}

void resetVecFloat(std::vector<float> &K){
  for (size_t i=0;i<K.size();++i){
    K[i]=0;
  }
}

void resetVecFloatOfFloat(std::vector<std::vector<float>> &K){
  for (size_t i=0;i<K.size();++i){
    for (size_t j=0;j<K[i].size();++j){
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
    int resultVmm = -1;
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


void printMemoryUsage() {
    struct rusage r_usage;
    getrusage(RUSAGE_SELF, &r_usage);
    std::cout << "Memory usage: " << r_usage.ru_maxrss/1000000.0 << " GB" << std::endl;
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


void MyAnalysis::Analyze(TString fname, TString data, TString dataset ,string year, TString Run, float xs, float lumi, float Nevent, int iseft, int nRuns, int onlyGen, MyAnalysis *Evt){
  ROOT::DisableImplicitMT();
  if (fChain == 0) return;
  inputs(data, year);
  Long64_t ntr = fChain->GetEntries ();
  Long64_t CHUNK_SIZE = 1000;
  if (data == "data") CHUNK_SIZE = 1000;
  
  Long64_t chunkStart = 0;
  while (chunkStart < ntr) {
    Long64_t chunkEnd = std::min(chunkStart + CHUNK_SIZE, ntr);
    std::cout << "Processing events from " << chunkStart << " to " << chunkEnd - 1 << std::endl;

    Loop(fname, data, dataset , year, Run, xs, lumi, Nevent, iseft, nRuns, onlyGen, Evt, chunkStart, chunkEnd);

    chunkStart = chunkEnd; // move forward by the actual number of events processed

    if (memory < 1000000 && CHUNK_SIZE<25000) {
        std::cout << "Memory used less than 1GB (" << memory / 1000000.0 << "), doubling CHUNK_SIZE for next iteration." << std::endl;
        CHUNK_SIZE *= 2;
    }
  }
}

void MyAnalysis::Loop(TString fname, TString data, TString dataset ,string year, TString Run, float xs, float lumi, float Nevent, int iseft, int nRuns, int onlyGen, MyAnalysis *Evt, Long64_t start, Long64_t end){
//*** decide if you want to run with or without saving systematic uncertainty histograms
  bool ifSys=true;
//*** make the histograms and all needed information ready to start the analysis 
  initiateHists(data, year, ifSys);
//  example_Zll("jigsaw.root");

  JigsawRecTZFCNC *jigsawTzFCNC;
  jigsawTzFCNC = new JigsawRecTZFCNC();
  JigsawRecTHFCNC *jigsawThFCNC;
  jigsawThFCNC = new JigsawRecTHFCNC();

//  genLevelAnalysis genAnalysis(Evt);

  TH1EFT  *crossSection = new TH1EFT("crossSection","crossSection",1,0,1);
  PU wPU;

  auto myLumiMask = LumiMask::fromJSON(gLumiMask,fRun,lRun);
  TRandom3 Tr;

  float DibosonCorr[10]={1.0,1.0,1.20, 1.48, 1.77, 2.05,2.34, 2.62,1.0,1.0};
  Double_t ptBins[11] = {30., 40., 60., 80., 100., 150., 200., 300., 400., 500., 1000.};
  Double_t etaBins [4]= {0., 0.6, 1.2, 2.4};

  TH1F *mll_SS_Zwindow_0jet = new TH1F("mll_SS_Zwindow_0jet","mll_SS_Zwindow_0jet",10,85,95);

  TH2D *h2_BTaggingEff_Denom_b    = new TH2D("h2_BTaggingEff_Denom_b"   , ";p_{T} [GeV];#eta", 10 , ptBins, 3 , etaBins);
  TH2D *h2_BTaggingEff_Denom_c    = new TH2D("h2_BTaggingEff_Denom_c"   , ";p_{T} [GeV];#eta", 10 , ptBins, 3 , etaBins);
  TH2D *h2_BTaggingEff_Denom_udsg = new TH2D("h2_BTaggingEff_Denom_udsg", ";p_{T} [GeV];#eta", 10 , ptBins, 3 , etaBins);
  TH2D *h2_BTaggingEff_Num_b      = new TH2D("h2_BTaggingEff_Num_b"     , ";p_{T} [GeV];#eta", 10 , ptBins, 3 , etaBins);
  TH2D *h2_BTaggingEff_Num_c      = new TH2D("h2_BTaggingEff_Num_c"     , ";p_{T} [GeV];#eta", 10 , ptBins, 3 , etaBins);
  TH2D *h2_BTaggingEff_Num_udsg   = new TH2D("h2_BTaggingEff_Num_udsg"  , ";p_{T} [GeV];#eta", 10 , ptBins, 3 , etaBins);


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


  std::vector<string> wc_names_lst={};
  std::vector<string> wc_names_lst_BNV={"cT", "cS"};
  std::vector<string> wc_names_lst_FCNC={"ctp","ctlS","cte","ctl","ctlT","ctZ","cpt","cpQM","ctA","cQe","ctG","cQlM"};
  std::vector<string> wc_names_lst_SMEFT={"ctu1","cqd1","cqq13","ctu8","cqu1","cqq11","cqq83","ctd1","ctd8","ctg","ctq1","cqq81","cqu8","cqd8","ctq8"};
  if (fname.Contains("BNV") && iseft) wc_names_lst = wc_names_lst_BNV;
  if (fname.Contains("FCNC") && iseft) wc_names_lst = wc_names_lst_FCNC;
  if (fname.Contains("SMEFT") && iseft) wc_names_lst = wc_names_lst_SMEFT;
  string listWC="";

  WCFit *eft_fit;

  TLorentzVector wp, wm, b, ab, top, atop;
  TLorentzVector recoTop, recoBjet, recoW, recoNu, recoL1, recoL2, highPtMu;
  bool leptonPass;
  bool metFilterPass;
  int ch;
  int chFA;
  int chOSppWeighted;
  int sumCharge;
  int sumFlavour;
  int myreg;
  bool onZ;
  bool offZhigh;
  float weight_Lumi;
  float weight_lep;
  float weight_lepB;
  float weight_EFT;
  int nAccept=0;
  float sumWeight=0;
  int nbjet;
  float HTjets;
  float MVAS_TU;
  float MVAB_TU;
  float MVAS_TC;
  float MVAB_TC;
  float MVAS_TUFA;
  float MVAB_TUFA;
  float MVAS_TCFA;
  float MVAB_TCFA;
  std::vector<Float_t> probs;
  float rawBDT;
  float ttKFactor;
  //in order to save systematic variations in one histogram, I use the TH1EFT feature and consider each EFT constant for knowing sum of event weights in each bin
  //for Dim number of WC, TH1EFT keep track of (Dim + 1) * (Dim + 2) / 2 constant. We use one constant for one uncertainty
  //number of systematic sources is 17 so 5 constant is enough
  const int Dim = 3;  
  const int N = (Dim + 1) * (Dim + 2) / 2;
  Float_t sysFitCoefficientsUp[N];
  Float_t sysFitCoefficientsDown[N];
  std::vector<std::string> sys_std;
  for (int i = 0; i < Dim; ++i) {
        sys_std.push_back("S" + std::to_string(i));
  }
  const int DimTh = 14;
  const int NTh = (DimTh + 1) * (DimTh + 2) / 2;
  Float_t sysThFitCoefficients[NTh];
  std::vector<std::string> sysTh_std;
  for (int i = 0; i < DimTh; ++i) {
        sysTh_std.push_back("Th" + std::to_string(i));
  }
  
  // Fill all with zero

  UInt_t nss=2;
  std::vector<int> reg(regions.size());
  std::vector<int> allCh(nss);
  std::vector<int> allChFA(1);
  std::vector<std::vector<float>> wgt(nss);
  std::vector<std::vector<float>> wgtSysUp(nss);
  std::vector<std::vector<float>> wgtSysDown(nss);
  for (UInt_t i = 0 ; i < nss ; i++) {
    wgt[i].resize(regions.size());
    wgtSysUp[i].resize(regions.size());
    wgtSysDown[i].resize(regions.size());
  }
  std::vector<std::vector<WCFit>> wcfit(nss);
  std::vector<std::vector<WCFit>> wcfitSysUp(nss);
  std::vector<std::vector<WCFit>> wcfitSysDown(nss);
  for (UInt_t i = 0 ; i < nss ; i++) {
    wcfit[i].resize(regions.size());
    wcfitSysUp[i].resize(regions.size());
    wcfitSysDown[i].resize(regions.size());
  }

  std::vector<std::vector<float>> wgtFA(1);
  wgtFA[0].resize(regions.size());
  std::vector<std::vector<WCFit>> wcfitFA(1);
  wcfitFA[0].resize(regions.size());
  int nLHEl;
  float fakeRate;
  std::vector<float> sysDownWeightsFA;
  std::vector<float> sysUpWeightsFA;
  sysUpWeightsFA.assign(sysFA.size(), 1);
  sysDownWeightsFA.assign(sysFA.size(), 1);
  float fi;
  float probChOS;
  int lZp;
  int lZfp;
  TLorentzVector top_tZFCNC, bt_tZFCNC, Wt_tZFCNC, lt_tZFCNC, nut_tZFCNC, Z_tZFCNC, lpZ_tZFCNC, lmZ_tZFCNC ;
  TLorentzVector hL_tHFCNC, hNu_tHFCNC, hU_tHFCNC, hD_tHFCNC, tNu_tHFCNC, tB_tHFCNC, tL_tHFCNC, met_tHFCNC;
  WCPoint *A = new WCPoint("EFTrwgt4_cpQM_1.0_cpt_1.0_ctA_1.0_ctZ_0.5_ctG_0.1_cQlM_1.0_cQe_1.0_ctl_1.0_cte_1.0_ctlS_1.0_ctlT_0.05_ctp_1.0");

  if (fChain == 0) return;
  Long64_t nentries = fChain->GetEntriesFast();
  Long64_t nbytes = 0, nb = 0;
  Long64_t ntr = fChain->GetEntries ();

//Loop over events
cout<<"starting loop with  Virtual Memory: "<<getValue()/1048576.0<<" GB"<<endl;
//  for (Long64_t jentry=0; jentry<nentries;jentry++) {
  for (Long64_t jentry=start; jentry<end;jentry++) {
    Long64_t ientry = LoadTree(jentry);
    if (ientry < 0) break;
    nb = fChain->GetEntry(jentry);   nbytes += nb;
    displayProgress(jentry, ntr) ;
    if (jentry % 1000 == 0) cout<<"Virtual Memory: "<<getValue()/1048576.0<<" GB"<<endl;
    tH_topMass_=-999;    tH_HMass_=-999;    tH_WtopMass_=-999;    tH_W1HMass_=-999;    tH_W2HMass_=-999;    tH_HPt_=-999;    tH_HEta_=-999;    tH_topPt_=-999;    tH_topEta_=-999;    tH_drWtopB_=-999;    tH_drW1HW2H_=-999;
    tZ_topMass_=-999; tZ_ZMass_=-999; tZ_WtopMass_=-999; tZ_ZPt_=-999; tZ_ZEta_=-999; tZ_topPt_=-999; tZ_topEta_=-999;
//write out the WCs at the begining of the code to make sure what you have set is used in the sample
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
    //put the Lumi mask
    if(data == "data"){
      if(!myLumiMask.accept(run, luminosityBlock)) continue;
    }
   //photon overlap removal
   //find the cuts here: /cvmfs/cms.cern.ch/phys_generator/gridpacks/UL/13TeV/madgraph/V5_2.6.5/TTGamma_Dilept/ttGamma_Dilept_5f_ckm_LO_1line_slc7_amd64_gcc700_CMSSW_10_6_19_tarball.tar.xz
   //find the cuts here: /cvmfs/cms.cern.ch/phys_generator/gridpacks/2017/13TeV/madgraph/V5_2.6.1/QCD_ZA_FXFX/ZATo2LA01j_5f_NLO_FXFX_slc6_amd64_gcc481_CMSSW_7_1_30_tarball.tar.xz
   if(data == "mc" && fname.Contains("TTTo") || fname.Contains("WJetsToLNu") || fname.Contains("DY") || fname.Contains("t_channel")){
     if (overlapRemoval(15.0, 5.0, 0.4, false,false)) {
       continue;
     }
   }
   if(data == "mc" && fname.Contains("TTGamma") || fname.Contains("WGToLNuG") || fname.Contains("ZGToLLG") || fname.Contains("TGJets")){
     if (overlapRemoval(15.0, 5.0, 0.4, false,true)) {
       continue;
     }
   }
//    if(jentry==0 && fname.Contains("FCNC")){
//      listWC="";
//      for (UInt_t i=0;i<nWCnames;++i){
//         char ch[4];
//         for(int j = 0; j < 4; j++) ch[j] = (WCnames[i] >> (4-1-j)*8) & 0xFF;
//         for(int n=0 ; n<4 ; ++n) listWC += ch[n];
//      }
//      cout<<"\n original WC list= {"<<listWC<<"}"<<endl;
//      listWC=std::regex_replace(listWC, std::regex("-"), std::string(""));
//      listWC=std::regex_replace(listWC, std::regex("c"), std::string("\",\"c"));
//      listWC.erase(0,2);
//      listWC+="\"";
//      cout<<"\n WC list = {"<<listWC<<"}"<<endl;
//      cout<<"\n  WC list in this code = {";
//      for (auto i: wc_names_lst) {
//        std::cout << i << ',';} cout<<"}"<<endl;
//    }

    Z_tZFCNC.SetPtEtaPhiM(0,0,0,0); top_tZFCNC.SetPtEtaPhiM(0,0,0,0); bt_tZFCNC.SetPtEtaPhiM(0,0,0,0); Wt_tZFCNC.SetPtEtaPhiM(0,0,0,0); lt_tZFCNC.SetPtEtaPhiM(0,0,0,0); lpZ_tZFCNC.SetPtEtaPhiM(0,0,0,0); lmZ_tZFCNC.SetPtEtaPhiM(0,0,0,0);
    if(data == "mc" && fname.Contains("FCNC")){
      for (UInt_t l=0;l<nGenPart;l++){
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
      for (UInt_t l=0;l<nGenPart;l++){
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
//    if(data == "mc" && onlyGen){
//      if(iseft && fname.Contains("rwgt")) genAnalysis.fillGENHists(1.0/nRuns,wc_names_lst);
//      else if(iseft && !fname.Contains("rwgt")) genAnalysis.fillGENHists(LHEWeight_originalXWGTUP/nRuns,wc_names_lst);
//      else  genAnalysis.fillGENHists(xs/Nevent,wc_names_lst);
//      continue;
//    }
//    if(data == "mc" && !onlyGen){
//      if(iseft && fname.Contains("rwgt")) genAnalysis.fillGENHists(1.0/nRuns,wc_names_lst);
//      else if(iseft && !fname.Contains("rwgt")) genAnalysis.fillGENHists(LHEWeight_originalXWGTUP/nRuns,wc_names_lst);
//      else  genAnalysis.fillGENHists(xs/Nevent,wc_names_lst);
//    }
//    nLHEl=0;
//    if(data == "mc"){
//      for (UInt_t l=0;l<nLHEPart;l++){
//        if(abs(LHEPart_pdgId[l]) ==11 || abs(LHEPart_pdgId[l]) ==13 ){
//          if(LHEPart_pt[l]>20 && abs(LHEPart_eta[l])<2.4) nLHEl++;
//        }
//      }
//      for (UInt_t l=0;l<nGenPart;l++){
//        if(abs(GenPart_pdgId[l])==11 || abs(GenPart_pdgId[l])==13){
//          if(abs(GenPart_pdgId[GenPart_genPartIdxMother[l]])==24 && GenPart_pt[l]>20 &&  abs(GenPart_eta[l])<2.4) nLHEl++;
//        }
//      }
//    }

    metFilterPass = false;
    leptonPass = false;
    ch =100;
    chFA=100;
    chOSppWeighted=100;
    reg_=100;
    sumCharge =0;
    sumFlavour = 0;
    onZ = false;
    offZhigh = false;
    weight_Lumi =1;
    weight_lep =1;
    weight_lepB =1;
    weight_EFT =1;
    nbjet=0;
    MVAS_TU=0;
    MVAB_TU=1;
    MVAS_TC=0;
    MVAB_TC=1;
    MVAS_TUFA=0;
    MVAB_TUFA=1;
    MVAS_TCFA=0;
    MVAB_TCFA=1;
    HTjets=0;
    ttKFactor=1;
    if (fname.Contains("Decay")) ttKFactor=831.7/445.0;
    else ttKFactor=1;

    fakeRate=1;
    fi=1;
    probChOS=1;
    for (int n=0;n<sysFA.size();++n){
      sysUpWeightsFA[n] =1;
      sysDownWeightsFA[n] =1;
    }
    if (iseft) {
      eft_fit = new WCFit(nWCnames, wc_names_lst, nEFTfitCoefficients, EFTfitCoefficients, (xs/Nevent)*(1.0/LHEWeight_originalXWGTUP));
//      eft_fit = new WCFit(nWCnames, wc_names_lst, nEFTfitCoefficients, EFTfitCoefficients, 1.0/nRuns);
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
    for (UInt_t l=0;l<wc_names_lst.size();l++){
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
//*** MET Filters
    if(year == "2017" || year == "2018"){
      if ( Flag_goodVertices  &&  Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter &&  Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_eeBadScFilter && Flag_ecalBadCalibFilter && Flag_BadPFMuonDzFilter) metFilterPass = true;
    }
    else{
      if ( Flag_goodVertices  &&  Flag_globalSuperTightHalo2016Filter && Flag_HBHENoiseFilter &&  Flag_HBHENoiseIsoFilter && Flag_EcalDeadCellTriggerPrimitiveFilter && Flag_BadPFMuonFilter && Flag_eeBadScFilter && Flag_BadPFMuonDzFilter) metFilterPass = true;
    }
    if(!metFilterPass) continue;
//*** trigger condition
    if(!trigger(data, dataset,year)) continue;
//*** object selection
    objectSelection(data,year);
//**** jet veto map
    bool jetVetoMap=false;
    for (UInt_t l=0;l<selectedJets->size();l++){
    if (jetVetoMaps_H->GetBinContent(jetVetoMaps_H->GetXaxis()->FindBin((*selectedJets)[l]->eta_),jetVetoMaps_H->GetYaxis()->FindBin((*selectedJets)[l]->phi_))>0) jetVetoMap=true;
      HTjets=HTjets+(*selectedJets)[l]->pt_;
      if((*selectedJets)[l]->btag_) nbjet++;
    }
    if(jetVetoMap) continue;
    if (data == "mc") weight_Lumi = (1000*xs*lumi*ttKFactor)/Nevent;
//*** Event selection
    for (UInt_t i=0;i<selectedPLeptons->size();i++){
      sumCharge += (*selectedPLeptons)[i]->charge_;
      sumFlavour += (*selectedPLeptons)[i]->lep_;
    }
    if(selectedPLeptons->size() ==2){ 
      if ((*selectedPLeptons)[0]->pt_ > 25 && (*selectedPLeptons)[1]->pt_ > 15 &&  ((*selectedPLeptons)[0]->p4_ + (*selectedPLeptons)[1]->p4_).M()>20) leptonPass=true;  
//opposite-sign dilepton channels 
      if (leptonPass && sumFlavour== 2 && sumCharge==0 && tightCharge((*selectedPLeptons)[0]->indice_ , (*selectedPLeptons)[0]->pdgid_) && tightCharge((*selectedPLeptons)[1]->indice_ , (*selectedPLeptons)[1]->pdgid_)) ch=getVecPos(channels,"2los_EpEm_CR");
      if (leptonPass && sumFlavour== 11 && sumCharge==0 && tightCharge((*selectedPLeptons)[0]->indice_ , (*selectedPLeptons)[0]->pdgid_) && tightCharge((*selectedPLeptons)[1]->indice_ , (*selectedPLeptons)[1]->pdgid_)) ch=getVecPos(channels,"2los_EpmMUmp_CR");
      if (leptonPass && sumFlavour== 20 && sumCharge==0 && tightCharge((*selectedPLeptons)[0]->indice_ , (*selectedPLeptons)[0]->pdgid_) && tightCharge((*selectedPLeptons)[1]->indice_ , (*selectedPLeptons)[1]->pdgid_)) ch=getVecPos(channels,"2los_MUpMUm_CR");
//same-sign dilepton channels
      if (leptonPass &&  (sumCharge>0 || sumCharge<0) && tightCharge((*selectedPLeptons)[0]->indice_ , (*selectedPLeptons)[0]->pdgid_) && tightCharge((*selectedPLeptons)[1]->indice_ , (*selectedPLeptons)[1]->pdgid_) && isMatched((*selectedPLeptons)[0]->indice_ , (*selectedPLeptons)[0]->pdgid_,data, true) && isMatched((*selectedPLeptons)[1]->indice_ , (*selectedPLeptons)[1]->pdgid_,data,true) && sumFlavour== 2) ch=getVecPos(channels,"2lssEE");
      if (leptonPass &&  (sumCharge>0 || sumCharge<0) && tightCharge((*selectedPLeptons)[0]->indice_ , (*selectedPLeptons)[0]->pdgid_) && tightCharge((*selectedPLeptons)[1]->indice_ , (*selectedPLeptons)[1]->pdgid_) && isMatched((*selectedPLeptons)[0]->indice_ , (*selectedPLeptons)[0]->pdgid_,data, true) && isMatched((*selectedPLeptons)[1]->indice_ , (*selectedPLeptons)[1]->pdgid_,data,true) && sumFlavour== 11) ch=getVecPos(channels,"2lssEM");
      if (leptonPass &&  (sumCharge>0 || sumCharge<0) && tightCharge((*selectedPLeptons)[0]->indice_ , (*selectedPLeptons)[0]->pdgid_) && tightCharge((*selectedPLeptons)[1]->indice_ , (*selectedPLeptons)[1]->pdgid_) && isMatched((*selectedPLeptons)[0]->indice_ , (*selectedPLeptons)[0]->pdgid_,data, true) && isMatched((*selectedPLeptons)[1]->indice_ , (*selectedPLeptons)[1]->pdgid_,data,true) && sumFlavour== 20) ch=getVecPos(channels,"2lssMM");      
          if (leptonPass && sumCharge==0 && tightCharge((*selectedPLeptons)[0]->indice_ , (*selectedPLeptons)[0]->pdgid_) && tightCharge((*selectedPLeptons)[1]->indice_ , (*selectedPLeptons)[1]->pdgid_) && isMatched((*selectedPLeptons)[0]->indice_ , (*selectedPLeptons)[0]->pdgid_,data, false) && isMatched((*selectedPLeptons)[1]->indice_ , (*selectedPLeptons)[1]->pdgid_,data,false) && sumFlavour== 20) nAccept++;
//      if (leptonPass &&  (sumCharge>0 || sumCharge<0) && tightCharge((*selectedPLeptons)[0]->indice_ , (*selectedPLeptons)[0]->pdgid_) && tightCharge((*selectedPLeptons)[1]->indice_ , (*selectedPLeptons)[1]->pdgid_)) ch=getVecPos(channels,"2lss");
//charged flip application regions
      if(sumFlavour== 2 && sumCharge==0){
        if (leptonPass && tightCharge((*selectedPLeptons)[0]->indice_ , (*selectedPLeptons)[0]->pdgid_) && tightCharge((*selectedPLeptons)[1]->indice_ , (*selectedPLeptons)[1]->pdgid_) && isMatched((*selectedPLeptons)[0]->indice_ , (*selectedPLeptons)[0]->pdgid_,data,false) && isMatched((*selectedPLeptons)[1]->indice_ , (*selectedPLeptons)[1]->pdgid_,data,false)) {
          chOSppWeighted=getVecPos(channels,"2losEE_Weighted");
            //the probability that one is mis-measured and the other is correct:
            //P(\text{same-sign}) = p1 (1 - p2) + (1 - p1) p2 
            probChOS= scale_factor(cf_ele_H, (*selectedPLeptons)[0]->pt_, abs((*selectedPLeptons)[0]->eta_),"central", true, false) *(1-scale_factor(cf_ele_H, (*selectedPLeptons)[1]->pt_, abs((*selectedPLeptons)[1]->eta_),"central", true, false)) + scale_factor(cf_ele_H, (*selectedPLeptons)[1]->pt_, abs((*selectedPLeptons)[1]->eta_),"central", true, false) *(1-scale_factor(cf_ele_H, (*selectedPLeptons)[0]->pt_, abs((*selectedPLeptons)[0]->eta_),"central", true, false));
        }
      }
      if(sumFlavour== 11 && sumCharge==0){
        if (leptonPass && tightCharge((*selectedPLeptons)[0]->indice_ , (*selectedPLeptons)[0]->pdgid_) && tightCharge((*selectedPLeptons)[1]->indice_ , (*selectedPLeptons)[1]->pdgid_) && isMatched((*selectedPLeptons)[0]->indice_ , (*selectedPLeptons)[0]->pdgid_,data,false) && isMatched((*selectedPLeptons)[1]->indice_ , (*selectedPLeptons)[1]->pdgid_,data,false)) {
          if((*selectedPLeptons)[0]->lep_==1){
            chOSppWeighted=getVecPos(channels,"2losEM_Weighted");
            probChOS= scale_factor(cf_ele_H, (*selectedPLeptons)[0]->pt_, abs((*selectedPLeptons)[0]->eta_),"central", true, false);
          }
          if((*selectedPLeptons)[1]->lep_==1){
            chOSppWeighted=getVecPos(channels,"2losEM_Weighted");
            probChOS= scale_factor(cf_ele_H, (*selectedPLeptons)[1]->pt_, abs((*selectedPLeptons)[1]->eta_),"central", true, false);
          }
        }
      }
    }
//*** three and four lepton final state
    float zValue=0;
    int zIndex = 0;
    if(Z_P->size()>0){
      zValue = (*Z_P)[0]->mass_;
      zIndex = 0;
      for (UInt_t i = 1; i < Z_P->size(); ++i) {
        if (std::abs((*Z_P)[i]->mass_ - 91.1876) > std::abs(zValue - 91.1876)) {
          zValue = (*Z_P)[i]->mass_;
          zIndex = i;
        }
      }
      if(abs((*Z_P)[zIndex]->mass_ - 91.1876) > 10) {
        offZhigh=true;
        lZp=zIndex;
      }
      zValue = (*Z_P)[0]->mass_;
      zIndex = 0;
      for (UInt_t i = 1; i < Z_P->size(); ++i) {
        if (std::abs((*Z_P)[i]->mass_ - 91.1876) < std::abs(zValue - 91.1876)) {
          zValue = (*Z_P)[i]->mass_;
          zIndex = i;
        }
      }
      if(abs((*Z_P)[zIndex]->mass_- 91.1876)<10) {
        onZ=true;
        lZp=zIndex;
      }
    }

    if(selectedPLeptons->size() ==3){
      if ((*selectedPLeptons)[0]->pt_ > 25 && (*selectedPLeptons)[1]->pt_ > 15) leptonPass=true;
      if((*selectedPLeptons)[2]->lep_== 1 && (*selectedPLeptons)[2]->pt_ <15) leptonPass=false;

      if (leptonPass && onZ && isMatched((*selectedPLeptons)[0]->indice_ , (*selectedPLeptons)[0]->pdgid_,data,false) && isMatched((*selectedPLeptons)[1]->indice_ , (*selectedPLeptons)[1]->pdgid_,data,false)  && isMatched((*selectedPLeptons)[2]->indice_ , (*selectedPLeptons)[2]->pdgid_,data,false)) ch=getVecPos(channels,"3lonZ");
      if (leptonPass && !onZ && offZhigh && isMatched((*selectedPLeptons)[0]->indice_ , (*selectedPLeptons)[0]->pdgid_,data,false) && isMatched((*selectedPLeptons)[1]->indice_ , (*selectedPLeptons)[1]->pdgid_,data,false)  && isMatched((*selectedPLeptons)[2]->indice_ , (*selectedPLeptons)[2]->pdgid_,data,false)) ch=getVecPos(channels,"3loffZhigh");
      if (leptonPass && !onZ && !offZhigh && isMatched((*selectedPLeptons)[0]->indice_ , (*selectedPLeptons)[0]->pdgid_,data,false) && isMatched((*selectedPLeptons)[1]->indice_ , (*selectedPLeptons)[1]->pdgid_,data,false)  && isMatched((*selectedPLeptons)[2]->indice_ , (*selectedPLeptons)[2]->pdgid_,data,false)) ch=getVecPos(channels,"3loffZlow");
    }
    if(selectedPLeptons->size() > 3 ){
      if ((*selectedPLeptons)[0]->pt_ > 25 && (*selectedPLeptons)[1]->pt_ > 15) leptonPass=true;
      if(((*selectedPLeptons)[2]->lep_== 1 && (*selectedPLeptons)[2]->pt_ <15) || ((*selectedPLeptons)[3]->lep_== 1 && (*selectedPLeptons)[3]->pt_ <15)) leptonPass=false;
      if (leptonPass) ch=getVecPos(channels,"4l_CR");
    }
//*** non-prompt lepton estimation
    onZ=false;
    offZhigh=false;
    zValue=0;
    zIndex = 0;
    if(Z_FP->size()>0){
      zValue = (*Z_FP)[0]->mass_;
      zIndex = 0;
      for (UInt_t i = 1; i < Z_FP->size(); ++i) {
        if (std::abs((*Z_FP)[i]->mass_ - 91.1876) > std::abs(zValue - 91.1876)) {
          zValue = (*Z_FP)[i]->mass_;
          zIndex = i;
        }
      }
      if(abs((*Z_FP)[zIndex]->mass_ - 91.1876) > 10) {
        offZhigh=true;
        lZfp=zIndex;
      }
      zValue = (*Z_FP)[0]->mass_;
      zIndex = 0;
      for (UInt_t i = 1; i < Z_FP->size(); ++i) {
        if (std::abs((*Z_FP)[i]->mass_ - 91.1876) < std::abs(zValue - 91.1876)) {
          zValue = (*Z_FP)[i]->mass_;
          zIndex = i;
        }
      }
      if(abs((*Z_FP)[zIndex]->mass_- 91.1876)<10) {
        onZ=true;
        lZfp=zIndex;
      }
    }
    sumCharge=0;
    sumFlavour=0;
    for (UInt_t i=0;i<selectedLeptons->size();i++){
      sumCharge += (*selectedLeptons)[i]->charge_;
      sumFlavour += (*selectedLeptons)[i]->lep_;
    }
    if(selectedFLeptons->size()==1){
      leptonPass=false;
      if(selectedPLeptons->size() ==1){
        if ((*selectedLeptons)[0]->pt_ > 25 && (*selectedLeptons)[1]->pt_ > 15 &&  ((*selectedLeptons)[0]->p4_ + (*selectedLeptons)[1]->p4_).M()>20) leptonPass=true;
        if (leptonPass && sumCharge !=0 && tightCharge((*selectedLeptons)[0]->indice_ , (*selectedLeptons)[0]->pdgid_) && tightCharge((*selectedLeptons)[1]->indice_ , (*selectedLeptons)[1]->pdgid_)&& isMatched((*selectedLeptons)[0]->indice_ , (*selectedLeptons)[0]->pdgid_,data, true) && isMatched((*selectedLeptons)[1]->indice_ , (*selectedLeptons)[1]->pdgid_,data,true) && sumFlavour==2) chFA=getVecPos(channelsFA,"2lssEE_LF");
	if (leptonPass && sumCharge !=0 && tightCharge((*selectedLeptons)[0]->indice_ , (*selectedLeptons)[0]->pdgid_) && tightCharge((*selectedLeptons)[1]->indice_ , (*selectedLeptons)[1]->pdgid_)&& isMatched((*selectedLeptons)[0]->indice_ , (*selectedLeptons)[0]->pdgid_,data, true) && isMatched((*selectedLeptons)[1]->indice_ , (*selectedLeptons)[1]->pdgid_,data,true) && sumFlavour==11) chFA=getVecPos(channelsFA,"2lssEM_LF");
	if (leptonPass && sumCharge !=0 && tightCharge((*selectedLeptons)[0]->indice_ , (*selectedLeptons)[0]->pdgid_) && tightCharge((*selectedLeptons)[1]->indice_ , (*selectedLeptons)[1]->pdgid_)&& isMatched((*selectedLeptons)[0]->indice_ , (*selectedLeptons)[0]->pdgid_,data, true) && isMatched((*selectedLeptons)[1]->indice_ , (*selectedLeptons)[1]->pdgid_,data,true) && sumFlavour==20) chFA=getVecPos(channelsFA,"2lssMM_LF");
      }

      if(selectedPLeptons->size() ==2){
        if ((*selectedLeptons)[0]->pt_ > 25 && (*selectedLeptons)[1]->pt_ > 15) leptonPass=true;
        if((*selectedLeptons)[2]->lep_== 1 && (*selectedLeptons)[2]->pt_ <15) leptonPass=false;
        if (leptonPass && onZ && isMatched((*selectedLeptons)[0]->indice_ , (*selectedLeptons)[0]->pdgid_,data,false) && isMatched((*selectedLeptons)[1]->indice_ , (*selectedLeptons)[1]->pdgid_,data,false)  && isMatched((*selectedLeptons)[2]->indice_ , (*selectedLeptons)[2]->pdgid_,data,false)) chFA=getVecPos(channelsFA,"3lonZ_LLF");
        if (leptonPass && !onZ && offZhigh && isMatched((*selectedLeptons)[0]->indice_ , (*selectedLeptons)[0]->pdgid_,data,false) && isMatched((*selectedLeptons)[1]->indice_ , (*selectedLeptons)[1]->pdgid_,data,false)  && isMatched((*selectedLeptons)[2]->indice_ , (*selectedLeptons)[2]->pdgid_,data,false)) chFA=getVecPos(channelsFA,"3loffZhigh_LLF");
        if (leptonPass && !onZ && !offZhigh && isMatched((*selectedLeptons)[0]->indice_ , (*selectedLeptons)[0]->pdgid_,data,false) && isMatched((*selectedLeptons)[1]->indice_ , (*selectedLeptons)[1]->pdgid_,data,false)  && isMatched((*selectedLeptons)[2]->indice_ , (*selectedLeptons)[2]->pdgid_,data,false)) chFA=getVecPos(channelsFA,"3loffZlow_LLF");
      }
    }
    if(selectedFLeptons->size()==2){
      leptonPass=false;
      if(selectedPLeptons->size() ==0){
        if ((*selectedLeptons)[0]->pt_ > 25 && (*selectedLeptons)[1]->pt_ > 15 &&  ((*selectedLeptons)[0]->p4_ + (*selectedLeptons)[1]->p4_).M()>20) leptonPass=true;
        if (leptonPass &&  sumCharge!=0 && tightCharge((*selectedLeptons)[0]->indice_ , (*selectedLeptons)[0]->pdgid_) && tightCharge((*selectedLeptons)[1]->indice_ , (*selectedLeptons)[1]->pdgid_) && isMatched((*selectedLeptons)[0]->indice_ , (*selectedLeptons)[0]->pdgid_,data, true) && isMatched((*selectedLeptons)[1]->indice_ , (*selectedLeptons)[1]->pdgid_,data,true) && sumFlavour==2) chFA=getVecPos(channelsFA,"2lssEE_FF");
	if (leptonPass &&  sumCharge!=0 && tightCharge((*selectedLeptons)[0]->indice_ , (*selectedLeptons)[0]->pdgid_) && tightCharge((*selectedLeptons)[1]->indice_ , (*selectedLeptons)[1]->pdgid_) && isMatched((*selectedLeptons)[0]->indice_ , (*selectedLeptons)[0]->pdgid_,data, true) && isMatched((*selectedLeptons)[1]->indice_ , (*selectedLeptons)[1]->pdgid_,data,true) && sumFlavour==11) chFA=getVecPos(channelsFA,"2lssEM_FF");
	if (leptonPass &&  sumCharge!=0 && tightCharge((*selectedLeptons)[0]->indice_ , (*selectedLeptons)[0]->pdgid_) && tightCharge((*selectedLeptons)[1]->indice_ , (*selectedLeptons)[1]->pdgid_) && isMatched((*selectedLeptons)[0]->indice_ , (*selectedLeptons)[0]->pdgid_,data, true) && isMatched((*selectedLeptons)[1]->indice_ , (*selectedLeptons)[1]->pdgid_,data,true) && sumFlavour==20) chFA=getVecPos(channelsFA,"2lssMM_FF");
      }

      if(selectedPLeptons->size() ==1){
        if ((*selectedLeptons)[0]->pt_ > 25 && (*selectedLeptons)[1]->pt_ > 15) leptonPass=true;
        if((*selectedLeptons)[2]->lep_== 1 && (*selectedLeptons)[2]->pt_ <15) leptonPass=false;
        if (leptonPass && onZ && isMatched((*selectedLeptons)[0]->indice_ , (*selectedLeptons)[0]->pdgid_,data,false) && isMatched((*selectedLeptons)[1]->indice_ , (*selectedLeptons)[1]->pdgid_,data,false)  && isMatched((*selectedLeptons)[2]->indice_ , (*selectedLeptons)[2]->pdgid_,data,false)) chFA=getVecPos(channelsFA,"3lonZ_LFF");
        if (leptonPass && !onZ && offZhigh && isMatched((*selectedLeptons)[0]->indice_ , (*selectedLeptons)[0]->pdgid_,data,false) && isMatched((*selectedLeptons)[1]->indice_ , (*selectedLeptons)[1]->pdgid_,data,false)  && isMatched((*selectedLeptons)[2]->indice_ , (*selectedLeptons)[2]->pdgid_,data,false)) chFA=getVecPos(channelsFA,"3loffZhigh_LFF");
        if (leptonPass && !onZ && !offZhigh && isMatched((*selectedLeptons)[0]->indice_ , (*selectedLeptons)[0]->pdgid_,data,false) && isMatched((*selectedLeptons)[1]->indice_ , (*selectedLeptons)[1]->pdgid_,data,false)  && isMatched((*selectedLeptons)[2]->indice_ , (*selectedLeptons)[2]->pdgid_,data,false) ) chFA=getVecPos(channelsFA,"3loffZlow_LFF");
      }
    }
    if(selectedFLeptons->size()==3){
      leptonPass=false;
      if(selectedPLeptons->size() ==0){
        if ((*selectedLeptons)[0]->pt_ > 25 && (*selectedLeptons)[1]->pt_ > 15) leptonPass=true;
        if((*selectedLeptons)[2]->lep_== 1 && (*selectedLeptons)[2]->pt_ <15) leptonPass=false;
        if (leptonPass && onZ && isMatched((*selectedLeptons)[0]->indice_ , (*selectedLeptons)[0]->pdgid_,data,false) && isMatched((*selectedLeptons)[1]->indice_ , (*selectedLeptons)[1]->pdgid_,data,false)  && isMatched((*selectedLeptons)[2]->indice_ , (*selectedLeptons)[2]->pdgid_,data,false)) chFA=getVecPos(channelsFA,"3lonZ_FFF");
        if (leptonPass && !onZ && offZhigh && isMatched((*selectedLeptons)[0]->indice_ , (*selectedLeptons)[0]->pdgid_,data,false) && isMatched((*selectedLeptons)[1]->indice_ , (*selectedLeptons)[1]->pdgid_,data,false)  && isMatched((*selectedLeptons)[2]->indice_ , (*selectedLeptons)[2]->pdgid_,data,false)) chFA=getVecPos(channelsFA,"3loffZhigh_FFF");
        if (leptonPass && !onZ && !offZhigh && isMatched((*selectedLeptons)[0]->indice_ , (*selectedLeptons)[0]->pdgid_,data,false) && isMatched((*selectedLeptons)[1]->indice_ , (*selectedLeptons)[1]->pdgid_,data,false)  && isMatched((*selectedLeptons)[2]->indice_ , (*selectedLeptons)[2]->pdgid_,data,false)) chFA=getVecPos(channelsFA,"3loffZlow_FFF");
      }
   }
//if (ch==getVecPos(channels,"LFpp")) cout<<run<<":"<<luminosityBlock<<":"<<event<<endl;
   sysUpWeights[getVecPos(sys,"triggerSF")] = 1.02;
   sysDownWeights[getVecPos(sys,"triggerSF")] =0.98;
   if(ch>30 && chFA>30) {
     objectSelectionEnd();
     continue;
   }
//Fill histograms
   if (data == "mc"){
     if(ch<30){
//calculate the trigger SFs
       if (channels[ch].Contains("2l")){
         if((*selectedPLeptons)[0]->lep_ + (*selectedPLeptons)[1]->lep_ == 2) {
           nominalWeights[getVecPos(sys,"triggerSF")] = scale_factor(sf_triggeree_H, (*selectedPLeptons)[0]->pt_,(*selectedPLeptons)[1]->pt_,"central",false, true);
         }
         if((*selectedPLeptons)[0]->lep_ + (*selectedPLeptons)[1]->lep_ == 11) {
           nominalWeights[getVecPos(sys,"triggerSF")] = scale_factor(sf_triggeremu_H, (*selectedPLeptons)[0]->pt_,(*selectedPLeptons)[1]->pt_,"central",false, true);
         }
         if((*selectedPLeptons)[0]->lep_ + (*selectedPLeptons)[1]->lep_ == 20) {
           nominalWeights[getVecPos(sys,"triggerSF")] = scale_factor(sf_triggermumu_H, (*selectedPLeptons)[0]->pt_,(*selectedPLeptons)[1]->pt_,"central",false, true);
         }
         sysUpWeights[getVecPos(sys,"triggerSF")] = nominalWeights[getVecPos(sys,"triggerSF")] * sysUpWeights[getVecPos(sys,"triggerSF")];
         sysDownWeights[getVecPos(sys,"triggerSF")] = nominalWeights[getVecPos(sys,"triggerSF")] * sysDownWeights[getVecPos(sys,"triggerSF")];
//correct for the electron SF in the dilepton regions
         for (UInt_t i=0;i<selectedPLeptons->size();i++){
           if((*selectedPLeptons)[i]->lep_== 1) nominalWeights[getVecPos(sys,"eleRecoIdIso")] = nominalWeights[getVecPos(sys,"eleRecoIdIso")] * (scale_factor(sf_eleLooseMVATight2lss_H, abs((*selectedPLeptons)[i]->eta_),(*selectedPLeptons)[i]->pt_,"central",false, true)/scale_factor(sf_eleLooseMVATight_H, abs((*selectedPLeptons)[i]->eta_),(*selectedPLeptons)[i]->pt_,"central",false, true));
         }
       }
     }
     weight_lep  = weight_Lumi * signnum_typical(LHEWeight_originalXWGTUP)*nominalWeights[getVecPos(sys,"eleRecoIdIso")]*nominalWeights[getVecPos(sys,"muRecoIdIso")]*nominalWeights[getVecPos(sys,"triggerSF")]*nominalWeights[getVecPos(sys,"pu")]*nominalWeights[getVecPos(sys,"prefiring")]*nominalWeights[getVecPos(sys,"JetPuID")]; 
     weight_lepB = weight_lep* nominalWeights[getVecPos(sys,"bcTagSfUnCorr")];
     weight_EFT = weight_Lumi* signnum_typical(LHEWeight_originalXWGTUP)*(1.0/LHEWeight_originalXWGTUP)*nominalWeights[getVecPos(sys,"eleRecoIdIso")]*nominalWeights[getVecPos(sys,"muRecoIdIso")]*nominalWeights[getVecPos(sys,"triggerSF")]*nominalWeights[getVecPos(sys,"pu")]*nominalWeights[getVecPos(sys,"prefiring")]*nominalWeights[getVecPos(sys,"bcTagSfUnCorr")]*nominalWeights[getVecPos(sys,"JetPuID")];
     if(abs(weight_lepB)>100){
       cout<<"Warning: event weight too large ="<<weight_lepB<<endl;
       continue;
     }
     if(fname.Contains("_WZTo3LNu")) weight_lepB = weight_lepB * DibosonCorr[selectedJets->size()];
//cout<< weight_Lumi<<":"<<signnum_typical(LHEWeight_originalXWGTUP)<<":"<<(1.0/LHEWeight_originalXWGTUP)<<":"<<nominalWeights[getVecPos(sys,"eleRecoIdIso")]<<":"<<nominalWeights[getVecPos(sys,"muRecoIdIso")]<<":"<<nominalWeights[getVecPos(sys,"triggerSF")]<<":"<<nominalWeights[getVecPos(sys,"pu")]<<":"<<nominalWeights[getVecPos(sys,"prefiring")]<<":"<<nominalWeights[getVecPos(sys,"bcTagSfUnCorr")]<<":"<<nominalWeights[getVecPos(sys,"JetPuID")]<<endl;
//  for (int n=0;n<sys.size();++n){
//    if(std::isnan(nominalWeights[n]) || !std::isfinite(nominalWeights[n])) cout<<sys[n]<<" is nan/inf "<<nominalWeights[n]<<endl;
//    if(std::isnan(nominalWeights[n]) || !std::isfinite(nominalWeights[n])) std::cerr<<sys[n]<<" is nan/inf "<<nominalWeights[n]<<std::endl;
//    if(std::isnan(nominalWeights[n]) || !std::isfinite(nominalWeights[n])) std::cout <<sys[n]<<" is nan/inf "<<nominalWeights[n]<<std::flush;
//  }

   }
   for (UInt_t i=0;i<selectedFLeptons->size();i++){
     if ((*selectedFLeptons)[i]->lep_ == 1) fi = scale_factor(fr_ele_H, conept_TTH((*selectedFLeptons)[i]->indice_,11), abs((*selectedFLeptons)[i]->eta_),"central", true, false);
     else fi =scale_factor(fr_mu_H, conept_TTH((*selectedFLeptons)[i]->indice_,13), abs((*selectedFLeptons)[i]->eta_),"central", true, false);
     fakeRate=fakeRate*(fi/(1-fi));
     if ((*selectedFLeptons)[i]->lep_ == 1) fi = scale_factor(fr_ele_H_up, conept_TTH((*selectedFLeptons)[i]->indice_,11), abs((*selectedFLeptons)[i]->eta_),"central", true, false);
     else fi =scale_factor(fr_mu_H_up, conept_TTH((*selectedFLeptons)[i]->indice_,13), abs((*selectedFLeptons)[i]->eta_),"central", true, false);
     sysUpWeightsFA[0]=sysUpWeightsFA[0]*(fi/(1-fi));
     if ((*selectedFLeptons)[i]->lep_ == 1) fi = scale_factor(fr_ele_H_down, conept_TTH((*selectedFLeptons)[i]->indice_,11), abs((*selectedFLeptons)[i]->eta_),"central", true, false);
     else fi =scale_factor(fr_mu_H_down, conept_TTH((*selectedFLeptons)[i]->indice_,13), abs((*selectedFLeptons)[i]->eta_),"central", true, false);
     sysDownWeightsFA[0]=sysDownWeightsFA[0]*(fi/(1-fi));
     if ((*selectedFLeptons)[i]->lep_ == 1) fi = scale_factor(fr_ele_H_ptUp, conept_TTH((*selectedFLeptons)[i]->indice_,11), abs((*selectedFLeptons)[i]->eta_),"central", true, false);
     else fi =scale_factor(fr_mu_H_ptUp, conept_TTH((*selectedFLeptons)[i]->indice_,13), abs((*selectedFLeptons)[i]->eta_),"central", true, false);
     sysUpWeightsFA[1]=sysUpWeightsFA[1]*(fi/(1-fi));
     if ((*selectedFLeptons)[i]->lep_ == 1) fi = scale_factor(fr_ele_H_ptDown, conept_TTH((*selectedFLeptons)[i]->indice_,11), abs((*selectedFLeptons)[i]->eta_),"central", true, false);
     else fi =scale_factor(fr_mu_H_ptDown, conept_TTH((*selectedFLeptons)[i]->indice_,13), abs((*selectedFLeptons)[i]->eta_),"central", true, false);
     sysDownWeightsFA[1]=sysDownWeightsFA[1]*(fi/(1-fi));
     if ((*selectedFLeptons)[i]->lep_ == 1) fi = scale_factor(fr_ele_H_etaUp, conept_TTH((*selectedFLeptons)[i]->indice_,11), abs((*selectedFLeptons)[i]->eta_),"central", true, false);
     else fi =scale_factor(fr_mu_H_etaUp, conept_TTH((*selectedFLeptons)[i]->indice_,13), abs((*selectedFLeptons)[i]->eta_),"central", true, false);
     sysUpWeightsFA[2]=sysUpWeightsFA[2]*(fi/(1-fi));
     if ((*selectedFLeptons)[i]->lep_ == 1) fi = scale_factor(fr_ele_H_etaDown, conept_TTH((*selectedFLeptons)[i]->indice_,11), abs((*selectedFLeptons)[i]->eta_),"central", true, false);
     else fi =scale_factor(fr_mu_H_etaDown, conept_TTH((*selectedFLeptons)[i]->indice_,13), abs((*selectedFLeptons)[i]->eta_),"central", true, false);
     sysDownWeightsFA[2]=sysDownWeightsFA[2]*(fi/(1-fi));
   }
   if (iseft) eft_fit = new WCFit(nWCnames, wc_names_lst, nEFTfitCoefficients, EFTfitCoefficients, weight_EFT);
   else eft_fit = new WCFit(0,wc_names_lst,1, &genWeight, 1.0);
   resetVecInt(reg);
   resetVecInt(allCh);
   resetVecInt(allChFA);
   if(ch<30) allCh[0]=ch;
   if(chFA<30) allChFA[0]=chFA;
   if(chOSppWeighted<30) allCh[1]=chOSppWeighted;
   myreg = findRegion(selectedJets, ch, chFA);
   reg_=myreg;
   if (myreg>=0){
     reg[myreg]=myreg;
     wgt[0][myreg]=weight_lepB;
     wgt[1][myreg]=weight_lepB*probChOS*chargeFlipNorm;
     wgtFA[0][myreg]=weight_lepB*fakeRate;
     wcfit[0][myreg]= *eft_fit;
     wcfit[1][myreg]= *eft_fit;
     wcfitFA[0][myreg]= *eft_fit;
   }
   if(ch<30 && channels[ch].Contains("2lss") && myreg==-1) mll_SS_Zwindow_0jet->Fill( ((*selectedPLeptons)[0]->p4_ + (*selectedPLeptons)[1]->p4_).M(),weight_lepB);
   if(ch<30 || chOSppWeighted<30){
     evaluateMVA(selectedJets, selectedPLeptons, Z_P, channels[ch], MET_pt, MET_phi, MVAS_TU, MVAB_TU, MVAS_TC, MVAB_TC);
     FillD3Hists(Hists, allCh, reg, vInd(vars,"lep1Pt"), (*selectedPLeptons)[0]->pt_ ,wgt, wcfit);
     FillD3Hists(Hists, allCh, reg, vInd(vars,"lep1Eta"), (*selectedPLeptons)[0]->eta_ ,wgt, wcfit); 
     FillD3Hists(Hists, allCh, reg, vInd(vars,"lep1Phi"), (*selectedPLeptons)[0]->phi_ ,wgt, wcfit); 
     FillD3Hists(Hists, allCh, reg, vInd(vars,"lep2Pt"), (*selectedPLeptons)[1]->pt_ ,wgt, wcfit); 
     FillD3Hists(Hists, allCh, reg, vInd(vars,"lep2Eta"), (*selectedPLeptons)[1]->eta_ ,wgt, wcfit); 
     FillD3Hists(Hists, allCh, reg, vInd(vars,"lep2Phi"), (*selectedPLeptons)[1]->phi_ ,wgt, wcfit); 
     FillD3Hists(Hists, allCh, reg, vInd(vars,"llM"), ((*selectedPLeptons)[0]->p4_ + (*selectedPLeptons)[1]->p4_).M() ,wgt, wcfit); 
     FillD3Hists(Hists, allCh, reg, vInd(vars,"llPt"), ((*selectedPLeptons)[0]->p4_ + (*selectedPLeptons)[1]->p4_).Pt() ,wgt, wcfit); 
     FillD3Hists(Hists, allCh, reg, vInd(vars,"llDr"), deltaR((*selectedPLeptons)[0]->eta_,(*selectedPLeptons)[0]->phi_,(*selectedPLeptons)[1]->eta_,(*selectedPLeptons)[1]->phi_) ,wgt, wcfit); 
     FillD3Hists(Hists, allCh, reg, vInd(vars,"llDphi"), abs(deltaPhi((*selectedPLeptons)[0]->phi_,(*selectedPLeptons)[1]->phi_)) ,wgt, wcfit); 
     FillD3Hists(Hists, allCh, reg, vInd(vars,"njet"), selectedJets->size() ,wgt, wcfit); 
     FillD3Hists(Hists, allCh, reg, vInd(vars,"nbjet"), nbjet ,wgt, wcfit); 
     FillD3Hists(Hists, allCh, reg, vInd(vars,"Met"), MET_pt ,wgt, wcfit);
     FillD3Hists(Hists, allCh, reg, vInd(vars,"MetPhi"), MET_phi ,wgt, wcfit);
     FillD3Hists(Hists, allCh, reg, vInd(vars,"nVtx"), PV_npvs ,wgt, wcfit);
     FillD3Hists(Hists, allCh, reg, vInd(vars,"llMZw"), ((*selectedPLeptons)[0]->p4_ + (*selectedPLeptons)[1]->p4_).M() ,wgt, wcfit);
     FillD3Hists(Hists, allCh, reg, vInd(vars,"MVATU"), MVAS_TU/MVAB_TU ,wgt, wcfit);
     FillD3Hists(Hists, allCh, reg, vInd(vars,"MVATC"), MVAS_TC/MVAB_TC ,wgt, wcfit);
     FillD3Hists(Hists, allCh, reg, vInd(vars,"lep3Pt"), MVA_lep3Pt,wgt, wcfit);
     FillD3Hists(Hists, allCh, reg, vInd(vars,"lep3Eta"), MVA_lep3Eta ,wgt, wcfit);
     FillD3Hists(Hists, allCh, reg, vInd(vars,"bJetPt"), MVA_bJetPt ,wgt, wcfit);
     FillD3Hists(Hists, allCh, reg, vInd(vars,"bJetEta"), MVA_bJetEta ,wgt, wcfit);
     FillD3Hists(Hists, allCh, reg, vInd(vars,"tH_topMass"), MVA_tH_topMass ,wgt, wcfit);
     FillD3Hists(Hists, allCh, reg, vInd(vars,"tH_HMass"), MVA_tH_HMass ,wgt, wcfit);
     FillD3Hists(Hists, allCh, reg, vInd(vars,"tH_WtopMass"), MVA_tH_WtopMass ,wgt, wcfit);
     FillD3Hists(Hists, allCh, reg, vInd(vars,"tH_W1HMass"), MVA_tH_W1HMass ,wgt, wcfit);
     FillD3Hists(Hists, allCh, reg, vInd(vars,"tH_W2HMass"), MVA_tH_W2HMass ,wgt, wcfit);
     FillD3Hists(Hists, allCh, reg, vInd(vars,"tH_HPt"), MVA_tH_HPt,wgt, wcfit);
     FillD3Hists(Hists, allCh, reg, vInd(vars,"tH_HEta"), MVA_tH_HEta,wgt, wcfit);
     FillD3Hists(Hists, allCh, reg, vInd(vars,"tH_topPt"),MVA_tH_topPt ,wgt, wcfit);
     FillD3Hists(Hists, allCh, reg, vInd(vars,"tH_topEta"),MVA_tH_topEta ,wgt, wcfit);
     FillD3Hists(Hists, allCh, reg, vInd(vars,"tH_drWtopB"), MVA_tH_drWtopB ,wgt, wcfit);
     FillD3Hists(Hists, allCh, reg, vInd(vars,"tH_drW1HW2H"), MVA_tH_drW1HW2H ,wgt, wcfit);
     FillD3Hists(Hists, allCh, reg, vInd(vars,"tZ_topMass"), MVA_tZ_topMass ,wgt, wcfit);
     FillD3Hists(Hists, allCh, reg, vInd(vars,"tZ_ZMass"),MVA_tZ_ZMass ,wgt, wcfit);
     FillD3Hists(Hists, allCh, reg, vInd(vars,"tZ_WtopMass"),MVA_tZ_WtopMass ,wgt, wcfit);
     FillD3Hists(Hists, allCh, reg, vInd(vars,"tZ_ZPt"),MVA_tZ_ZPt ,wgt, wcfit);
     FillD3Hists(Hists, allCh, reg, vInd(vars,"tZ_ZEta"),MVA_tZ_ZEta ,wgt, wcfit);
     FillD3Hists(Hists, allCh, reg, vInd(vars,"tZ_topPt"), MVA_tZ_topPt ,wgt, wcfit);
     FillD3Hists(Hists, allCh, reg, vInd(vars,"tZ_topEta"), MVA_tZ_topEta,wgt, wcfit);
     if(selectedJets->size()>0){
       FillD3Hists(Hists, allCh, reg, vInd(vars,"jet1Pt"), (*selectedJets)[0]->pt_ ,wgt, wcfit);
       FillD3Hists(Hists, allCh, reg, vInd(vars,"jet1Eta"), (*selectedJets)[0]->eta_ ,wgt, wcfit);
       FillD3Hists(Hists, allCh, reg, vInd(vars,"jet1Phi"), (*selectedJets)[0]->phi_ ,wgt, wcfit);
     }
  }
  if(chFA<30){ 
     evaluateMVA(selectedJets, selectedLeptons, Z_FP, channelsFA[chFA], MET_pt, MET_phi, MVAS_TUFA, MVAB_TUFA, MVAS_TCFA, MVAB_TCFA);
     FillD3Hists(HistsFA, allChFA, reg, vInd(varsFA,"lep1Pt"), (*selectedLeptons)[0]->pt_ ,wgtFA, wcfitFA);
     FillD3Hists(HistsFA, allChFA, reg, vInd(varsFA,"lep1Eta"), (*selectedLeptons)[0]->eta_ ,wgtFA, wcfitFA);
     FillD3Hists(HistsFA, allChFA, reg, vInd(varsFA,"lep1Phi"), (*selectedLeptons)[0]->phi_ ,wgtFA, wcfitFA);
     FillD3Hists(HistsFA, allChFA, reg, vInd(varsFA,"lep2Pt"), (*selectedLeptons)[1]->pt_ ,wgtFA, wcfitFA);
     FillD3Hists(HistsFA, allChFA, reg, vInd(varsFA,"lep2Eta"), (*selectedLeptons)[1]->eta_ ,wgtFA, wcfitFA);
     FillD3Hists(HistsFA, allChFA, reg, vInd(varsFA,"lep2Phi"), (*selectedLeptons)[1]->phi_ ,wgtFA, wcfitFA);
     FillD3Hists(HistsFA, allChFA, reg, vInd(varsFA,"llM"), ((*selectedLeptons)[0]->p4_ + (*selectedLeptons)[1]->p4_).M() ,wgtFA, wcfitFA);
     FillD3Hists(HistsFA, allChFA, reg, vInd(varsFA,"llPt"), ((*selectedLeptons)[0]->p4_ + (*selectedLeptons)[1]->p4_).Pt() ,wgtFA, wcfitFA);
     FillD3Hists(HistsFA, allChFA, reg, vInd(varsFA,"llDr"), deltaR((*selectedLeptons)[0]->eta_,(*selectedLeptons)[0]->phi_,(*selectedLeptons)[1]->eta_,(*selectedLeptons)[1]->phi_) ,wgtFA, wcfitFA);
     FillD3Hists(HistsFA, allChFA, reg, vInd(varsFA,"llDphi"), abs(deltaPhi((*selectedLeptons)[0]->phi_,(*selectedLeptons)[1]->phi_)) ,wgtFA, wcfitFA);
     FillD3Hists(HistsFA, allChFA, reg, vInd(varsFA,"njet"), selectedJets->size() ,wgtFA, wcfitFA);
     FillD3Hists(HistsFA, allChFA, reg, vInd(varsFA,"nbjet"), nbjet ,wgtFA, wcfitFA);
     FillD3Hists(HistsFA, allChFA, reg, vInd(varsFA,"Met"), MET_pt ,wgtFA, wcfitFA);
     FillD3Hists(HistsFA, allChFA, reg, vInd(varsFA,"MetPhi"), MET_phi ,wgtFA, wcfitFA);
     FillD3Hists(HistsFA, allChFA, reg, vInd(varsFA,"nVtx"), PV_npvs ,wgtFA, wcfitFA);
     FillD3Hists(HistsFA, allChFA, reg, vInd(varsFA,"llMZw"), ((*selectedLeptons)[0]->p4_ + (*selectedLeptons)[1]->p4_).M() ,wgtFA, wcfitFA);
     FillD3Hists(HistsFA, allChFA, reg, vInd(varsFA,"MVATU"), MVAS_TUFA/MVAB_TUFA ,wgtFA, wcfitFA);
     FillD3Hists(HistsFA, allChFA, reg, vInd(varsFA,"MVATC"), MVAS_TCFA/MVAB_TCFA ,wgtFA, wcfitFA);
     FillD3Hists(HistsFA, allChFA, reg, vInd(varsFA,"lep3Pt"), MVA_lep3Pt,wgtFA, wcfitFA);
     FillD3Hists(HistsFA, allChFA, reg, vInd(varsFA,"lep3Eta"), MVA_lep3Eta ,wgtFA, wcfitFA);
     FillD3Hists(HistsFA, allChFA, reg, vInd(varsFA,"bJetPt"), MVA_bJetPt ,wgtFA, wcfitFA);
     FillD3Hists(HistsFA, allChFA, reg, vInd(varsFA,"bJetEta"), MVA_bJetEta ,wgtFA, wcfitFA);
     FillD3Hists(HistsFA, allChFA, reg, vInd(varsFA,"tH_topMass"), MVA_tH_topMass ,wgtFA, wcfitFA);
     FillD3Hists(HistsFA, allChFA, reg, vInd(varsFA,"tH_HMass"), MVA_tH_HMass ,wgtFA, wcfitFA);
     FillD3Hists(HistsFA, allChFA, reg, vInd(varsFA,"tH_WtopMass"), MVA_tH_WtopMass ,wgtFA, wcfitFA);
     FillD3Hists(HistsFA, allChFA, reg, vInd(varsFA,"tH_W1HMass"), MVA_tH_W1HMass ,wgtFA, wcfitFA);
     FillD3Hists(HistsFA, allChFA, reg, vInd(varsFA,"tH_W2HMass"), MVA_tH_W2HMass ,wgtFA, wcfitFA);
     FillD3Hists(HistsFA, allChFA, reg, vInd(varsFA,"tH_HPt"), MVA_tH_HPt,wgtFA, wcfitFA);
     FillD3Hists(HistsFA, allChFA, reg, vInd(varsFA,"tH_HEta"), MVA_tH_HEta,wgtFA, wcfitFA);
     FillD3Hists(HistsFA, allChFA, reg, vInd(varsFA,"tH_topPt"),MVA_tH_topPt ,wgtFA, wcfitFA);
     FillD3Hists(HistsFA, allChFA, reg, vInd(varsFA,"tH_topEta"),MVA_tH_topEta ,wgtFA, wcfitFA);
     FillD3Hists(HistsFA, allChFA, reg, vInd(varsFA,"tH_drWtopB"), MVA_tH_drWtopB ,wgtFA, wcfitFA);
     FillD3Hists(HistsFA, allChFA, reg, vInd(varsFA,"tH_drW1HW2H"), MVA_tH_drW1HW2H ,wgtFA, wcfitFA);
     FillD3Hists(HistsFA, allChFA, reg, vInd(varsFA,"tZ_topMass"), MVA_tZ_topMass ,wgtFA, wcfitFA);
     FillD3Hists(HistsFA, allChFA, reg, vInd(varsFA,"tZ_ZMass"),MVA_tZ_ZMass ,wgtFA, wcfitFA);
     FillD3Hists(HistsFA, allChFA, reg, vInd(varsFA,"tZ_WtopMass"),MVA_tZ_WtopMass ,wgtFA, wcfitFA);
     FillD3Hists(HistsFA, allChFA, reg, vInd(varsFA,"tZ_ZPt"),MVA_tZ_ZPt ,wgtFA, wcfitFA);
     FillD3Hists(HistsFA, allChFA, reg, vInd(varsFA,"tZ_ZEta"),MVA_tZ_ZEta ,wgtFA, wcfitFA);
     FillD3Hists(HistsFA, allChFA, reg, vInd(varsFA,"tZ_topPt"), MVA_tZ_topPt ,wgtFA, wcfitFA);
     FillD3Hists(HistsFA, allChFA, reg, vInd(varsFA,"tZ_topEta"), MVA_tZ_topEta,wgtFA, wcfitFA);
     if(selectedJets->size()>0){
       FillD3Hists(HistsFA, allChFA, reg, vInd(varsFA,"jet1Pt"), (*selectedJets)[0]->pt_ ,wgtFA, wcfitFA);
       FillD3Hists(HistsFA, allChFA, reg, vInd(varsFA,"jet1Eta"), (*selectedJets)[0]->eta_ ,wgtFA, wcfitFA);
       FillD3Hists(HistsFA, allChFA, reg, vInd(varsFA,"jet1Phi"), (*selectedJets)[0]->phi_ ,wgtFA, wcfitFA);
     }
     //Fake sys 
     if (myreg>=0){
       for(int n=0;n<sysFA.size();++n){
         wgtSysUp[0][myreg]=wgtFA[0][myreg]*(sysUpWeightsFA[n]/fakeRate);
         wcfitSysUp[0][myreg]= *eft_fit;
         FillD4Hists(HistsFAUp, allChFA, reg, vInd(varsFullSys,"MVATU"), MVAS_TUFA/MVAB_TUFA ,wgtSysUp, wcfitSysUp,n);
         FillD4Hists(HistsFAUp, allChFA, reg, vInd(varsFullSys,"MVATC"), MVAS_TCFA/MVAB_TCFA ,wgtSysUp, wcfitSysUp,n);

         wgtSysUp[0][myreg]=wgtFA[0][myreg]*(sysDownWeightsFA[n]/fakeRate);
         FillD4Hists(HistsFADown, allChFA, reg, vInd(varsFullSys,"MVATU"), MVAS_TUFA/MVAB_TUFA ,wgtSysUp, wcfitSysUp,n);
         FillD4Hists(HistsFADown, allChFA, reg, vInd(varsFullSys,"MVATC"), MVAS_TCFA/MVAB_TCFA ,wgtSysUp, wcfitSysUp,n);
       }
     }
   }
   delete eft_fit;
//Fill syst histsi 
   if (data == "mc"  && ifSys && ch<30 && std::find(channelsSys.begin(), channelsSys.end(), channels[ch]) != channelsSys.end() && myreg>=0){
     for (int i = 0, idx = 0; i <= Dim; ++i) {
         for (int j = 0; j <= i; ++j, ++idx) {
             sysFitCoefficientsUp[idx] = 0.0f; 
             sysFitCoefficientsDown[idx] = 0.0f;
         }
     }
     for (int i = 0, idx = 0; i <= DimTh; ++i) {
         for (int j = 0; j <= i; ++j, ++idx) {
             sysThFitCoefficients[idx] = 0.0f;
         }
     }

     auto it = std::find(channelsSys.begin(), channelsSys.end(), channels[ch]);
     size_t index = std::distance(channelsSys.begin(), it);
     allCh[0]=index; allCh[1]=-1;  
     for(int n=0;n<sys.size();++n){
       if (std::find(sysNotWeight.begin(), sysNotWeight.end(), sys[n]) != sysNotWeight.end()) continue;
       if (iseft) eft_fit = new WCFit(nWCnames, wc_names_lst, nEFTfitCoefficients, EFTfitCoefficients, weight_EFT*(sysUpWeights[n]/nominalWeights[n]));
       else eft_fit = new WCFit(0,wc_names_lst,1, &genWeight, 1.0);
       wgtSysUp[0][myreg]=wgt[0][myreg]*(sysUpWeights[n]/nominalWeights[n]);
       wcfitSysUp[0][myreg]= *eft_fit;
       FillD4Hists(HistsSysUp, allCh, reg, vInd(varsFullSys,"MVATU"), MVAS_TU/MVAB_TU ,wgtSysUp, wcfitSysUp, n);
       FillD4Hists(HistsSysUp, allCh, reg, vInd(varsFullSys,"MVATC"), MVAS_TC/MVAB_TC ,wgtSysUp, wcfitSysUp, n);
       sysFitCoefficientsUp[n]=wgt[0][myreg]*(sysUpWeights[n]/nominalWeights[n]);

       delete eft_fit;
       if (iseft) eft_fit = new WCFit(nWCnames, wc_names_lst, nEFTfitCoefficients, EFTfitCoefficients, weight_EFT*(sysDownWeights[n]/nominalWeights[n]));
       else eft_fit = new WCFit(0,wc_names_lst,1, &genWeight, 1.0);
       wgtSysDown[0][myreg]=wgt[0][myreg]*(sysDownWeights[n]/nominalWeights[n]);
       wcfitSysDown[0][myreg]= *eft_fit;
       FillD4Hists(HistsSysDown, allCh, reg, vInd(varsFullSys,"MVATU"), MVAS_TU/MVAB_TU ,wgtSysDown, wcfitSysDown, n);
       FillD4Hists(HistsSysDown, allCh, reg, vInd(varsFullSys,"MVATC"), MVAS_TC/MVAB_TC ,wgtSysDown, wcfitSysDown, n);
       delete eft_fit;
       sysFitCoefficientsDown[n]=wgt[0][myreg]*(sysDownWeights[n]/nominalWeights[n]);
     }
//Theory uncertainty {RenUp, RenDown, FacUp, FacDown, IsrUp, IsrDown, FsrUp, FsrDown, PDF1, PDF2,..., PDF100}
//Qscale uncertainty
     if (iseft){
       sysThFitCoefficients[0]=wgt[0][myreg]*(LHEScaleWeight[6])*csetScale->evaluate({std::string(fname.Data()), 6});
       sysThFitCoefficients[1]=wgt[0][myreg]*(LHEScaleWeight[1])*csetScale->evaluate({std::string(fname.Data()), 1});
       sysThFitCoefficients[2]=wgt[0][myreg]*(LHEScaleWeight[4])*csetScale->evaluate({std::string(fname.Data()), 4});
       sysThFitCoefficients[3]=wgt[0][myreg]*(LHEScaleWeight[3])*csetScale->evaluate({std::string(fname.Data()), 3});
     }
     else{
       sysThFitCoefficients[0]=wgt[0][myreg]*(LHEScaleWeight[7])*csetScale->evaluate({std::string(fname.Data()), 7});
       sysThFitCoefficients[1]=wgt[0][myreg]*(LHEScaleWeight[1])*csetScale->evaluate({std::string(fname.Data()), 1});
       sysThFitCoefficients[2]=wgt[0][myreg]*(LHEScaleWeight[5])*csetScale->evaluate({std::string(fname.Data()), 5});
       sysThFitCoefficients[3]=wgt[0][myreg]*(LHEScaleWeight[3])*csetScale->evaluate({std::string(fname.Data()), 3});
     }       
//ISR/FSR uncertainty
     sysThFitCoefficients[4]=wgt[0][myreg]*(PSWeight[0]);
     sysThFitCoefficients[5]=wgt[0][myreg]*(PSWeight[2]);
     sysThFitCoefficients[6]=wgt[0][myreg]*(PSWeight[1]);
     sysThFitCoefficients[7]=wgt[0][myreg]*(PSWeight[3]);
//PDF uncertainty
     for (int n=0;n<100;++n){
       if(isnan(LHEPdfWeight[n]) || isinf(LHEPdfWeight[n])) continue;
       sysThFitCoefficients[n+8]= wgt[0][myreg]*LHEPdfWeight[n]*csetPDF->evaluate({std::string(fname.Data()), n});
     }
     eft_fit = new WCFit(DimTh, sysTh_std, NTh, sysThFitCoefficients, 1.0f);
//cout<<eft_fit->evalPoint("S1",1)<<" "<<eft_fit->evalPoint("S2",1)<<endl;
     if (myreg>=0){
       wcfit[0][myreg]= *eft_fit;
     }
     FillD3Hists(HistsTh, allCh, reg, vInd(varsFullSys,"MVATU"), MVAS_TU/MVAB_TU ,wgt, wcfit);
     FillD3Hists(HistsTh, allCh, reg, vInd(varsFullSys,"MVATC"), MVAS_TC/MVAB_TC ,wgt, wcfit);
     delete eft_fit;
//Fill JES(6)+Jer(1) histograms
     if (iseft) eft_fit = new WCFit(nWCnames, wc_names_lst, nEFTfitCoefficients, EFTfitCoefficients, weight_EFT);
     else eft_fit = new WCFit(0,wc_names_lst,1, &genWeight, 1.0);
     for (int n=0;n<nsrc+1;++n){
      auto itt = std::find(sys.begin(), sys.end(), sysJec[n]);
      int it = std::distance(sys.begin(), itt);
      auto normalItt = std::find(sysNormal.begin(), sysNormal.end(), sysJec[n]);  // looks for "JER/JES"

      resetVecInt(reg);
      myreg = findRegion(&(*JECsysUp)[n],  ch, chFA);
      if (myreg>=0){
        reg[myreg]=myreg;
        wgt[0][myreg]=weight_lepB;
        wcfit[0][myreg]= *eft_fit;
      }
       evaluateMVA(&(*JECsysUp)[n], selectedPLeptons, Z_P, channels[ch], (*MetJECsysUp)[n], (*MetPhiJECsysUp)[n],  MVAS_TU, MVAB_TU, MVAS_TC, MVAB_TC);
       FillD4Hists(HistsSysUp, allCh, reg, vInd(varsFullSys,"MVATU"), MVAS_TU/MVAB_TU ,wgt, wcfit,it);
       FillD4Hists(HistsSysUp, allCh, reg, vInd(varsFullSys,"MVATC"), MVAS_TC/MVAB_TC ,wgt, wcfit,it);
       if(normalItt!= sysNormal.end()) {
         int nIt = std::distance(sysNormal.begin(), normalItt);
         normalFillD4Hists(HistsNormalSysUp, allCh, reg, vInd(vars,"lep1Pt"), (*selectedPLeptons)[0]->pt_ ,wgt, nIt);
         normalFillD4Hists(HistsNormalSysUp, allCh, reg, vInd(vars,"lep1Eta"), (*selectedPLeptons)[0]->eta_ ,wgt, nIt);
         normalFillD4Hists(HistsNormalSysUp, allCh, reg, vInd(vars,"lep1Phi"), (*selectedPLeptons)[0]->phi_ ,wgt, nIt);
         normalFillD4Hists(HistsNormalSysUp, allCh, reg, vInd(vars,"lep2Pt"), (*selectedPLeptons)[1]->pt_ ,wgt, nIt);
         normalFillD4Hists(HistsNormalSysUp, allCh, reg, vInd(vars,"lep2Eta"), (*selectedPLeptons)[1]->eta_ ,wgt, nIt);
         normalFillD4Hists(HistsNormalSysUp, allCh, reg, vInd(vars,"lep2Phi"), (*selectedPLeptons)[1]->phi_ ,wgt, nIt);
         normalFillD4Hists(HistsNormalSysUp, allCh, reg, vInd(vars,"llM"), ((*selectedPLeptons)[0]->p4_ + (*selectedPLeptons)[1]->p4_).M() ,wgt, nIt);
         normalFillD4Hists(HistsNormalSysUp, allCh, reg, vInd(vars,"llPt"), ((*selectedPLeptons)[0]->p4_ + (*selectedPLeptons)[1]->p4_).Pt() ,wgt, nIt);
         normalFillD4Hists(HistsNormalSysUp, allCh, reg, vInd(vars,"llDr"), deltaR((*selectedPLeptons)[0]->eta_,(*selectedPLeptons)[0]->phi_,(*selectedPLeptons)[1]->eta_,(*selectedPLeptons)[1]->phi_) ,wgt,nIt);
         normalFillD4Hists(HistsNormalSysUp, allCh, reg, vInd(vars,"llDphi"), abs(deltaPhi((*selectedPLeptons)[0]->phi_,(*selectedPLeptons)[1]->phi_)) ,wgt, nIt);
         normalFillD4Hists(HistsNormalSysUp, allCh, reg, vInd(vars,"njet"), (*JECsysUp)[n].size() ,wgt, nIt);
         normalFillD4Hists(HistsNormalSysUp, allCh, reg, vInd(vars,"nbjet"), NbTag ,wgt, nIt);
         normalFillD4Hists(HistsNormalSysUp, allCh, reg, vInd(vars,"Met"), (*MetJECsysUp)[n] ,wgt, nIt);
         normalFillD4Hists(HistsNormalSysUp, allCh, reg, vInd(vars,"MetPhi"),  (*MetPhiJECsysUp)[n] ,wgt, nIt);
         normalFillD4Hists(HistsNormalSysUp, allCh, reg, vInd(vars,"nVtx"), PV_npvs ,wgt, nIt);
         normalFillD4Hists(HistsNormalSysUp, allCh, reg, vInd(vars,"llMZw"), ((*selectedPLeptons)[0]->p4_ + (*selectedPLeptons)[1]->p4_).M() ,wgt, nIt);
         normalFillD4Hists(HistsNormalSysUp, allCh, reg, vInd(vars,"MVATU"), MVAS_TU/MVAB_TU ,wgt, nIt);
         normalFillD4Hists(HistsNormalSysUp, allCh, reg, vInd(vars,"MVATC"), MVAS_TC/MVAB_TC ,wgt, nIt);
         normalFillD4Hists(HistsNormalSysUp, allCh, reg, vInd(vars,"lep3Pt"), MVA_lep3Pt,wgt, nIt);
         normalFillD4Hists(HistsNormalSysUp, allCh, reg, vInd(vars,"lep3Eta"), MVA_lep3Eta ,wgt, nIt);
         normalFillD4Hists(HistsNormalSysUp, allCh, reg, vInd(vars,"bJetPt"), MVA_bJetPt ,wgt, nIt);
         normalFillD4Hists(HistsNormalSysUp, allCh, reg, vInd(vars,"bJetEta"), MVA_bJetEta ,wgt, nIt);
         normalFillD4Hists(HistsNormalSysUp, allCh, reg, vInd(vars,"tH_topMass"), MVA_tH_topMass ,wgt, nIt);
         normalFillD4Hists(HistsNormalSysUp, allCh, reg, vInd(vars,"tH_HMass"), MVA_tH_HMass ,wgt, nIt);
         normalFillD4Hists(HistsNormalSysUp, allCh, reg, vInd(vars,"tH_WtopMass"), MVA_tH_WtopMass ,wgt, nIt);
         normalFillD4Hists(HistsNormalSysUp, allCh, reg, vInd(vars,"tH_W1HMass"), MVA_tH_W1HMass ,wgt, nIt);
         normalFillD4Hists(HistsNormalSysUp, allCh, reg, vInd(vars,"tH_W2HMass"), MVA_tH_W2HMass ,wgt, nIt);
         normalFillD4Hists(HistsNormalSysUp, allCh, reg, vInd(vars,"tH_HPt"), MVA_tH_HPt,wgt, nIt);
         normalFillD4Hists(HistsNormalSysUp, allCh, reg, vInd(vars,"tH_HEta"), MVA_tH_HEta,wgt, nIt);
         normalFillD4Hists(HistsNormalSysUp, allCh, reg, vInd(vars,"tH_topPt"),MVA_tH_topPt ,wgt, nIt);
         normalFillD4Hists(HistsNormalSysUp, allCh, reg, vInd(vars,"tH_topEta"),MVA_tH_topEta ,wgt, nIt);
         normalFillD4Hists(HistsNormalSysUp, allCh, reg, vInd(vars,"tH_drWtopB"), MVA_tH_drWtopB ,wgt, nIt);
         normalFillD4Hists(HistsNormalSysUp, allCh, reg, vInd(vars,"tH_drW1HW2H"), MVA_tH_drW1HW2H ,wgt, nIt);
         normalFillD4Hists(HistsNormalSysUp, allCh, reg, vInd(vars,"tZ_topMass"), MVA_tZ_topMass ,wgt, nIt);
         normalFillD4Hists(HistsNormalSysUp, allCh, reg, vInd(vars,"tZ_ZMass"),MVA_tZ_ZMass ,wgt, nIt);
         normalFillD4Hists(HistsNormalSysUp, allCh, reg, vInd(vars,"tZ_WtopMass"),MVA_tZ_WtopMass ,wgt, nIt);
         normalFillD4Hists(HistsNormalSysUp, allCh, reg, vInd(vars,"tZ_ZPt"),MVA_tZ_ZPt ,wgt, nIt);
         normalFillD4Hists(HistsNormalSysUp, allCh, reg, vInd(vars,"tZ_ZEta"),MVA_tZ_ZEta ,wgt, nIt);
         normalFillD4Hists(HistsNormalSysUp, allCh, reg, vInd(vars,"tZ_topPt"), MVA_tZ_topPt ,wgt, nIt);
         normalFillD4Hists(HistsNormalSysUp, allCh, reg, vInd(vars,"tZ_topEta"), MVA_tZ_topEta,wgt,nIt);
         if((*JECsysUp)[n].size()>0){
           normalFillD4Hists(HistsNormalSysUp, allCh, reg, vInd(vars,"jet1Pt"), (*JECsysUp)[n][0]->pt_ ,wgt, nIt);
           normalFillD4Hists(HistsNormalSysUp, allCh, reg, vInd(vars,"jet1Eta"), (*JECsysUp)[n][0]->eta_ ,wgt, nIt);
           normalFillD4Hists(HistsNormalSysUp, allCh, reg, vInd(vars,"jet1Phi"), (*JECsysUp)[n][0]->phi_ ,wgt, nIt);
         }
       }


      resetVecInt(reg);
      myreg = findRegion(&(*JECsysDown)[n],  ch, chFA);
      if (myreg>=0){
        reg[myreg]=myreg;
        wgt[0][myreg]=weight_lepB;
        wcfit[0][myreg]= *eft_fit;
      }
       evaluateMVA(&(*JECsysDown)[n], selectedPLeptons, Z_P, channels[ch], (*MetJECsysDown)[n], (*MetPhiJECsysDown)[n], MVAS_TU, MVAB_TU, MVAS_TC, MVAB_TC);
       FillD4Hists(HistsSysDown, allCh, reg, vInd(varsFullSys,"MVATU"), MVAS_TU/MVAB_TU ,wgt, wcfit,it);
       FillD4Hists(HistsSysDown, allCh, reg, vInd(varsFullSys,"MVATC"), MVAS_TC/MVAB_TC ,wgt, wcfit,it);
       if(normalItt!= sysNormal.end()) {
         int nIt = std::distance(sysNormal.begin(), normalItt);
         normalFillD4Hists(HistsNormalSysDown, allCh, reg, vInd(vars,"lep1Pt"), (*selectedPLeptons)[0]->pt_ ,wgt, nIt);
         normalFillD4Hists(HistsNormalSysDown, allCh, reg, vInd(vars,"lep1Eta"), (*selectedPLeptons)[0]->eta_ ,wgt, nIt);
         normalFillD4Hists(HistsNormalSysDown, allCh, reg, vInd(vars,"lep1Phi"), (*selectedPLeptons)[0]->phi_ ,wgt, nIt);
         normalFillD4Hists(HistsNormalSysDown, allCh, reg, vInd(vars,"lep2Pt"), (*selectedPLeptons)[1]->pt_ ,wgt, nIt);
         normalFillD4Hists(HistsNormalSysDown, allCh, reg, vInd(vars,"lep2Eta"), (*selectedPLeptons)[1]->eta_ ,wgt, nIt);
         normalFillD4Hists(HistsNormalSysDown, allCh, reg, vInd(vars,"lep2Phi"), (*selectedPLeptons)[1]->phi_ ,wgt, nIt);
         normalFillD4Hists(HistsNormalSysDown, allCh, reg, vInd(vars,"llM"), ((*selectedPLeptons)[0]->p4_ + (*selectedPLeptons)[1]->p4_).M() ,wgt, nIt);
         normalFillD4Hists(HistsNormalSysDown, allCh, reg, vInd(vars,"llPt"), ((*selectedPLeptons)[0]->p4_ + (*selectedPLeptons)[1]->p4_).Pt() ,wgt, nIt);
         normalFillD4Hists(HistsNormalSysDown, allCh, reg, vInd(vars,"llDr"), deltaR((*selectedPLeptons)[0]->eta_,(*selectedPLeptons)[0]->phi_,(*selectedPLeptons)[1]->eta_,(*selectedPLeptons)[1]->phi_) ,wgt,nIt);
         normalFillD4Hists(HistsNormalSysDown, allCh, reg, vInd(vars,"llDphi"), abs(deltaPhi((*selectedPLeptons)[0]->phi_,(*selectedPLeptons)[1]->phi_)) ,wgt, nIt);
         normalFillD4Hists(HistsNormalSysDown, allCh, reg, vInd(vars,"njet"), (*JECsysDown)[n].size() ,wgt, nIt);
         normalFillD4Hists(HistsNormalSysDown, allCh, reg, vInd(vars,"nbjet"), NbTag ,wgt, nIt);
         normalFillD4Hists(HistsNormalSysDown, allCh, reg, vInd(vars,"Met"), (*MetJECsysDown)[n] ,wgt, nIt);
         normalFillD4Hists(HistsNormalSysDown, allCh, reg, vInd(vars,"MetPhi"), (*MetPhiJECsysDown)[n] ,wgt, nIt);
         normalFillD4Hists(HistsNormalSysDown, allCh, reg, vInd(vars,"nVtx"), PV_npvs ,wgt, nIt);
         normalFillD4Hists(HistsNormalSysDown, allCh, reg, vInd(vars,"llMZw"), ((*selectedPLeptons)[0]->p4_ + (*selectedPLeptons)[1]->p4_).M() ,wgt, nIt);
         normalFillD4Hists(HistsNormalSysDown, allCh, reg, vInd(vars,"MVATU"), MVAS_TU/MVAB_TU ,wgt, nIt);
         normalFillD4Hists(HistsNormalSysDown, allCh, reg, vInd(vars,"MVATC"), MVAS_TC/MVAB_TC ,wgt, nIt);
         normalFillD4Hists(HistsNormalSysDown, allCh, reg, vInd(vars,"lep3Pt"), MVA_lep3Pt,wgt, nIt);
         normalFillD4Hists(HistsNormalSysDown, allCh, reg, vInd(vars,"lep3Eta"), MVA_lep3Eta ,wgt, nIt);
         normalFillD4Hists(HistsNormalSysDown, allCh, reg, vInd(vars,"bJetPt"), MVA_bJetPt ,wgt, nIt);
         normalFillD4Hists(HistsNormalSysDown, allCh, reg, vInd(vars,"bJetEta"), MVA_bJetEta ,wgt, nIt);
         normalFillD4Hists(HistsNormalSysDown, allCh, reg, vInd(vars,"tH_topMass"), MVA_tH_topMass ,wgt, nIt);
         normalFillD4Hists(HistsNormalSysDown, allCh, reg, vInd(vars,"tH_HMass"), MVA_tH_HMass ,wgt, nIt);
         normalFillD4Hists(HistsNormalSysDown, allCh, reg, vInd(vars,"tH_WtopMass"), MVA_tH_WtopMass ,wgt, nIt);
         normalFillD4Hists(HistsNormalSysDown, allCh, reg, vInd(vars,"tH_W1HMass"), MVA_tH_W1HMass ,wgt, nIt);
         normalFillD4Hists(HistsNormalSysDown, allCh, reg, vInd(vars,"tH_W2HMass"), MVA_tH_W2HMass ,wgt, nIt);
         normalFillD4Hists(HistsNormalSysDown, allCh, reg, vInd(vars,"tH_HPt"), MVA_tH_HPt,wgt, nIt);
         normalFillD4Hists(HistsNormalSysDown, allCh, reg, vInd(vars,"tH_HEta"), MVA_tH_HEta,wgt, nIt);
         normalFillD4Hists(HistsNormalSysDown, allCh, reg, vInd(vars,"tH_topPt"),MVA_tH_topPt ,wgt, nIt);
         normalFillD4Hists(HistsNormalSysDown, allCh, reg, vInd(vars,"tH_topEta"),MVA_tH_topEta ,wgt, nIt);
         normalFillD4Hists(HistsNormalSysDown, allCh, reg, vInd(vars,"tH_drWtopB"), MVA_tH_drWtopB ,wgt, nIt);
         normalFillD4Hists(HistsNormalSysDown, allCh, reg, vInd(vars,"tH_drW1HW2H"), MVA_tH_drW1HW2H ,wgt, nIt);
         normalFillD4Hists(HistsNormalSysDown, allCh, reg, vInd(vars,"tZ_topMass"), MVA_tZ_topMass ,wgt, nIt);
         normalFillD4Hists(HistsNormalSysDown, allCh, reg, vInd(vars,"tZ_ZMass"),MVA_tZ_ZMass ,wgt, nIt);
         normalFillD4Hists(HistsNormalSysDown, allCh, reg, vInd(vars,"tZ_WtopMass"),MVA_tZ_WtopMass ,wgt, nIt);
         normalFillD4Hists(HistsNormalSysDown, allCh, reg, vInd(vars,"tZ_ZPt"),MVA_tZ_ZPt ,wgt, nIt);
         normalFillD4Hists(HistsNormalSysDown, allCh, reg, vInd(vars,"tZ_ZEta"),MVA_tZ_ZEta ,wgt, nIt);
         normalFillD4Hists(HistsNormalSysDown, allCh, reg, vInd(vars,"tZ_topPt"), MVA_tZ_topPt ,wgt, nIt);
         normalFillD4Hists(HistsNormalSysDown, allCh, reg, vInd(vars,"tZ_topEta"), MVA_tZ_topEta,wgt,nIt);
         if((*JECsysDown)[n].size()>0){
           normalFillD4Hists(HistsNormalSysDown, allCh, reg, vInd(vars,"jet1Pt"),  (*JECsysDown)[n][0]->pt_ ,wgt, nIt);
           normalFillD4Hists(HistsNormalSysDown, allCh, reg, vInd(vars,"jet1Eta"),  (*JECsysDown)[n][0]->eta_ ,wgt, nIt);
           normalFillD4Hists(HistsNormalSysDown, allCh, reg, vInd(vars,"jet1Phi"),  (*JECsysDown)[n][0]->phi_ ,wgt, nIt);
         }
       }
     }
     delete eft_fit;

//    for (int i = 0, idx = 0; i <= Dim; ++i) {
//      if(i>0) cout<<sys[i-1]<<endl;
//      for (int j = 0; j <= i; ++j, ++idx) {
//        std::cout << "(" << i << "," << j << "): "<< std::setw(5) << sysFitCoefficientsUp[idx] << "\n";
//      }
//    }

    eft_fit = new WCFit(Dim, sys_std, N, sysFitCoefficientsUp, 1.0f);
//cout<<eft_fit->evalPoint("S1",1)<<" "<<eft_fit->evalPoint("S2",1)<<endl;
    resetVecInt(reg);
    myreg = findRegion(selectedJets, ch, chFA);
    if (myreg>=0){
      reg[myreg]=myreg;
      wgt[0][myreg]=weight_lepB;
      wcfit[0][myreg]= *eft_fit;
    }
    evaluateMVA(selectedJets, selectedPLeptons, Z_P, channels[ch],  MET_pt ,MET_phi, MVAS_TU, MVAB_TU, MVAS_TC, MVAB_TC);
    FillD3Hists(HistsSysCompactUp, allCh, reg, vInd(vars,"lep1Pt"), (*selectedPLeptons)[0]->pt_ ,wgt, wcfit);
    FillD3Hists(HistsSysCompactUp, allCh, reg, vInd(vars,"lep1Eta"), (*selectedPLeptons)[0]->eta_ ,wgt, wcfit);
    FillD3Hists(HistsSysCompactUp, allCh, reg, vInd(vars,"lep1Phi"), (*selectedPLeptons)[0]->phi_ ,wgt, wcfit);
    FillD3Hists(HistsSysCompactUp, allCh, reg, vInd(vars,"lep2Pt"), (*selectedPLeptons)[1]->pt_ ,wgt, wcfit);
    FillD3Hists(HistsSysCompactUp, allCh, reg, vInd(vars,"lep2Eta"), (*selectedPLeptons)[1]->eta_ ,wgt, wcfit);
    FillD3Hists(HistsSysCompactUp, allCh, reg, vInd(vars,"lep2Phi"), (*selectedPLeptons)[1]->phi_ ,wgt, wcfit);
    FillD3Hists(HistsSysCompactUp, allCh, reg, vInd(vars,"llM"), ((*selectedPLeptons)[0]->p4_ + (*selectedPLeptons)[1]->p4_).M() ,wgt, wcfit);
    FillD3Hists(HistsSysCompactUp, allCh, reg, vInd(vars,"llPt"), ((*selectedPLeptons)[0]->p4_ + (*selectedPLeptons)[1]->p4_).Pt() ,wgt, wcfit);
    FillD3Hists(HistsSysCompactUp, allCh, reg, vInd(vars,"llDr"), deltaR((*selectedPLeptons)[0]->eta_,(*selectedPLeptons)[0]->phi_,(*selectedPLeptons)[1]->eta_,(*selectedPLeptons)[1]->phi_) ,wgt, wcfit);
    FillD3Hists(HistsSysCompactUp, allCh, reg, vInd(vars,"llDphi"), abs(deltaPhi((*selectedPLeptons)[0]->phi_,(*selectedPLeptons)[1]->phi_)) ,wgt, wcfit);
    FillD3Hists(HistsSysCompactUp, allCh, reg, vInd(vars,"njet"), selectedJets->size() ,wgt, wcfit);
    FillD3Hists(HistsSysCompactUp, allCh, reg, vInd(vars,"nbjet"), nbjet ,wgt, wcfit);
    FillD3Hists(HistsSysCompactUp, allCh, reg, vInd(vars,"Met"), MET_pt ,wgt, wcfit);
    FillD3Hists(HistsSysCompactUp, allCh, reg, vInd(vars,"MetPhi"), MET_phi ,wgt, wcfit);
    FillD3Hists(HistsSysCompactUp, allCh, reg, vInd(vars,"nVtx"), PV_npvs ,wgt, wcfit);
    FillD3Hists(HistsSysCompactUp, allCh, reg, vInd(vars,"llMZw"), ((*selectedPLeptons)[0]->p4_ + (*selectedPLeptons)[1]->p4_).M() ,wgt, wcfit);
    FillD3Hists(HistsSysCompactUp, allCh, reg, vInd(vars,"MVATU"), MVAS_TU/MVAB_TU ,wgt, wcfit);
    FillD3Hists(HistsSysCompactUp, allCh, reg, vInd(vars,"MVATC"), MVAS_TC/MVAB_TC ,wgt, wcfit);
    FillD3Hists(HistsSysCompactUp, allCh, reg, vInd(vars,"lep3Pt"), MVA_lep3Pt,wgt, wcfit);
    FillD3Hists(HistsSysCompactUp, allCh, reg, vInd(vars,"lep3Eta"), MVA_lep3Eta ,wgt, wcfit);
    FillD3Hists(HistsSysCompactUp, allCh, reg, vInd(vars,"bJetPt"), MVA_bJetPt ,wgt, wcfit);
    FillD3Hists(HistsSysCompactUp, allCh, reg, vInd(vars,"bJetEta"), MVA_bJetEta ,wgt, wcfit);
    FillD3Hists(HistsSysCompactUp, allCh, reg, vInd(vars,"tH_topMass"), MVA_tH_topMass ,wgt, wcfit);
    FillD3Hists(HistsSysCompactUp, allCh, reg, vInd(vars,"tH_HMass"), MVA_tH_HMass ,wgt, wcfit);
    FillD3Hists(HistsSysCompactUp, allCh, reg, vInd(vars,"tH_WtopMass"), MVA_tH_WtopMass ,wgt, wcfit);
    FillD3Hists(HistsSysCompactUp, allCh, reg, vInd(vars,"tH_W1HMass"), MVA_tH_W1HMass ,wgt, wcfit);
    FillD3Hists(HistsSysCompactUp, allCh, reg, vInd(vars,"tH_W2HMass"), MVA_tH_W2HMass ,wgt, wcfit);
    FillD3Hists(HistsSysCompactUp, allCh, reg, vInd(vars,"tH_HPt"), MVA_tH_HPt,wgt, wcfit);
    FillD3Hists(HistsSysCompactUp, allCh, reg, vInd(vars,"tH_HEta"), MVA_tH_HEta,wgt, wcfit);
    FillD3Hists(HistsSysCompactUp, allCh, reg, vInd(vars,"tH_topPt"),MVA_tH_topPt ,wgt, wcfit);
    FillD3Hists(HistsSysCompactUp, allCh, reg, vInd(vars,"tH_topEta"),MVA_tH_topEta ,wgt, wcfit);
    FillD3Hists(HistsSysCompactUp, allCh, reg, vInd(vars,"tH_drWtopB"), MVA_tH_drWtopB ,wgt, wcfit);
    FillD3Hists(HistsSysCompactUp, allCh, reg, vInd(vars,"tH_drW1HW2H"), MVA_tH_drW1HW2H ,wgt, wcfit);
    FillD3Hists(HistsSysCompactUp, allCh, reg, vInd(vars,"tZ_topMass"), MVA_tZ_topMass ,wgt, wcfit);
    FillD3Hists(HistsSysCompactUp, allCh, reg, vInd(vars,"tZ_ZMass"),MVA_tZ_ZMass ,wgt, wcfit);
    FillD3Hists(HistsSysCompactUp, allCh, reg, vInd(vars,"tZ_WtopMass"),MVA_tZ_WtopMass ,wgt, wcfit);
    FillD3Hists(HistsSysCompactUp, allCh, reg, vInd(vars,"tZ_ZPt"),MVA_tZ_ZPt ,wgt, wcfit);
    FillD3Hists(HistsSysCompactUp, allCh, reg, vInd(vars,"tZ_ZEta"),MVA_tZ_ZEta ,wgt, wcfit);
    FillD3Hists(HistsSysCompactUp, allCh, reg, vInd(vars,"tZ_topPt"), MVA_tZ_topPt ,wgt, wcfit);
    FillD3Hists(HistsSysCompactUp, allCh, reg, vInd(vars,"tZ_topEta"), MVA_tZ_topEta,wgt, wcfit);
    if(selectedJets->size()>0){
      FillD3Hists(HistsSysCompactUp, allCh, reg, vInd(vars,"jet1Pt"), (*selectedJets)[0]->pt_ ,wgt, wcfit);
      FillD3Hists(HistsSysCompactUp, allCh, reg, vInd(vars,"jet1Eta"), (*selectedJets)[0]->eta_ ,wgt, wcfit);
      FillD3Hists(HistsSysCompactUp, allCh, reg, vInd(vars,"jet1Phi"), (*selectedJets)[0]->phi_ ,wgt, wcfit);
    }
 
    delete eft_fit;
    eft_fit = new WCFit(Dim, sys_std, N, sysFitCoefficientsDown, 1.0f);
    if (myreg>=0){
      wcfit[0][myreg]= *eft_fit;
    }
    FillD3Hists(HistsSysCompactDown, allCh, reg, vInd(vars,"lep1Pt"), (*selectedPLeptons)[0]->pt_ ,wgt, wcfit);
    FillD3Hists(HistsSysCompactDown, allCh, reg, vInd(vars,"lep1Eta"), (*selectedPLeptons)[0]->eta_ ,wgt, wcfit);
    FillD3Hists(HistsSysCompactDown, allCh, reg, vInd(vars,"lep1Phi"), (*selectedPLeptons)[0]->phi_ ,wgt, wcfit);
    FillD3Hists(HistsSysCompactDown, allCh, reg, vInd(vars,"lep2Pt"), (*selectedPLeptons)[1]->pt_ ,wgt, wcfit);
    FillD3Hists(HistsSysCompactDown, allCh, reg, vInd(vars,"lep2Eta"), (*selectedPLeptons)[1]->eta_ ,wgt, wcfit);
    FillD3Hists(HistsSysCompactDown, allCh, reg, vInd(vars,"lep2Phi"), (*selectedPLeptons)[1]->phi_ ,wgt, wcfit);
    FillD3Hists(HistsSysCompactDown, allCh, reg, vInd(vars,"llM"), ((*selectedPLeptons)[0]->p4_ + (*selectedPLeptons)[1]->p4_).M() ,wgt, wcfit);
    FillD3Hists(HistsSysCompactDown, allCh, reg, vInd(vars,"llPt"), ((*selectedPLeptons)[0]->p4_ + (*selectedPLeptons)[1]->p4_).Pt() ,wgt, wcfit);
    FillD3Hists(HistsSysCompactDown, allCh, reg, vInd(vars,"llDr"), deltaR((*selectedPLeptons)[0]->eta_,(*selectedPLeptons)[0]->phi_,(*selectedPLeptons)[1]->eta_,(*selectedPLeptons)[1]->phi_) ,wgt, wcfit);
    FillD3Hists(HistsSysCompactDown, allCh, reg, vInd(vars,"llDphi"), abs(deltaPhi((*selectedPLeptons)[0]->phi_,(*selectedPLeptons)[1]->phi_)) ,wgt, wcfit);
    FillD3Hists(HistsSysCompactDown, allCh, reg, vInd(vars,"njet"), selectedJets->size() ,wgt, wcfit);
    FillD3Hists(HistsSysCompactDown, allCh, reg, vInd(vars,"nbjet"), nbjet ,wgt, wcfit);
    FillD3Hists(HistsSysCompactDown, allCh, reg, vInd(vars,"Met"), MET_pt ,wgt, wcfit);
    FillD3Hists(HistsSysCompactDown, allCh, reg, vInd(vars,"MetPhi"), MET_phi ,wgt, wcfit);
    FillD3Hists(HistsSysCompactDown, allCh, reg, vInd(vars,"nVtx"), PV_npvs ,wgt, wcfit);
    FillD3Hists(HistsSysCompactDown, allCh, reg, vInd(vars,"llMZw"), ((*selectedPLeptons)[0]->p4_ + (*selectedPLeptons)[1]->p4_).M() ,wgt, wcfit);
    FillD3Hists(HistsSysCompactDown, allCh, reg, vInd(vars,"MVATU"), MVAS_TU/MVAB_TU ,wgt, wcfit);
    FillD3Hists(HistsSysCompactDown, allCh, reg, vInd(vars,"MVATC"), MVAS_TC/MVAB_TC ,wgt, wcfit);
    FillD3Hists(HistsSysCompactDown, allCh, reg, vInd(vars,"lep3Pt"), MVA_lep3Pt,wgt, wcfit);
    FillD3Hists(HistsSysCompactDown, allCh, reg, vInd(vars,"lep3Eta"), MVA_lep3Eta ,wgt, wcfit);
    FillD3Hists(HistsSysCompactDown, allCh, reg, vInd(vars,"bJetPt"), MVA_bJetPt ,wgt, wcfit);
    FillD3Hists(HistsSysCompactDown, allCh, reg, vInd(vars,"bJetEta"), MVA_bJetEta ,wgt, wcfit);
    FillD3Hists(HistsSysCompactDown, allCh, reg, vInd(vars,"tH_topMass"), MVA_tH_topMass ,wgt, wcfit);
    FillD3Hists(HistsSysCompactDown, allCh, reg, vInd(vars,"tH_HMass"), MVA_tH_HMass ,wgt, wcfit);
    FillD3Hists(HistsSysCompactDown, allCh, reg, vInd(vars,"tH_WtopMass"), MVA_tH_WtopMass ,wgt, wcfit);
    FillD3Hists(HistsSysCompactDown, allCh, reg, vInd(vars,"tH_W1HMass"), MVA_tH_W1HMass ,wgt, wcfit);
    FillD3Hists(HistsSysCompactDown, allCh, reg, vInd(vars,"tH_W2HMass"), MVA_tH_W2HMass ,wgt, wcfit);
    FillD3Hists(HistsSysCompactDown, allCh, reg, vInd(vars,"tH_HPt"), MVA_tH_HPt,wgt, wcfit);
    FillD3Hists(HistsSysCompactDown, allCh, reg, vInd(vars,"tH_HEta"), MVA_tH_HEta,wgt, wcfit);
    FillD3Hists(HistsSysCompactDown, allCh, reg, vInd(vars,"tH_topPt"),MVA_tH_topPt ,wgt, wcfit);
    FillD3Hists(HistsSysCompactDown, allCh, reg, vInd(vars,"tH_topEta"),MVA_tH_topEta ,wgt, wcfit);
    FillD3Hists(HistsSysCompactDown, allCh, reg, vInd(vars,"tH_drWtopB"), MVA_tH_drWtopB ,wgt, wcfit);
    FillD3Hists(HistsSysCompactDown, allCh, reg, vInd(vars,"tH_drW1HW2H"), MVA_tH_drW1HW2H ,wgt, wcfit);
    FillD3Hists(HistsSysCompactDown, allCh, reg, vInd(vars,"tZ_topMass"), MVA_tZ_topMass ,wgt, wcfit);
    FillD3Hists(HistsSysCompactDown, allCh, reg, vInd(vars,"tZ_ZMass"),MVA_tZ_ZMass ,wgt, wcfit);
    FillD3Hists(HistsSysCompactDown, allCh, reg, vInd(vars,"tZ_WtopMass"),MVA_tZ_WtopMass ,wgt, wcfit);
    FillD3Hists(HistsSysCompactDown, allCh, reg, vInd(vars,"tZ_ZPt"),MVA_tZ_ZPt ,wgt, wcfit);
    FillD3Hists(HistsSysCompactDown, allCh, reg, vInd(vars,"tZ_ZEta"),MVA_tZ_ZEta ,wgt, wcfit);
    FillD3Hists(HistsSysCompactDown, allCh, reg, vInd(vars,"tZ_topPt"), MVA_tZ_topPt ,wgt, wcfit);
    FillD3Hists(HistsSysCompactDown, allCh, reg, vInd(vars,"tZ_topEta"), MVA_tZ_topEta,wgt, wcfit);
    if(selectedJets->size()>0){
      FillD3Hists(HistsSysCompactDown, allCh, reg, vInd(vars,"jet1Pt"), (*selectedJets)[0]->pt_ ,wgt, wcfit);
      FillD3Hists(HistsSysCompactDown, allCh, reg, vInd(vars,"jet1Eta"), (*selectedJets)[0]->eta_ ,wgt, wcfit);
      FillD3Hists(HistsSysCompactDown, allCh, reg, vInd(vars,"jet1Phi"), (*selectedJets)[0]->phi_ ,wgt, wcfit);
    }
    delete eft_fit;
  }
//Fill a tree for doing MVA training
   if (nbjet==1 && ((ch<30 && !channels[ch].Contains("CR")) || chFA<30)) {
     bt_tZFCNC.SetPtEtaPhiM(0,0,0,0); nut_tZFCNC.SetPtEtaPhiM(0,0,0,0);
     hU_tHFCNC.SetPtEtaPhiM(0,0,0,0); hD_tHFCNC.SetPtEtaPhiM(0,0,0,0); met_tHFCNC.SetPtEtaPhiM(0,0,0,0); tB_tHFCNC.SetPtEtaPhiM(0,0,0,0);
     for (UInt_t l=0;l<selectedJets->size();l++){
       if((*selectedJets)[l]->btag_){
         tB_tHFCNC=(*selectedJets)[l]->p4_;
         bt_tZFCNC.SetPtEtaPhiM((*selectedJets)[l]->pt_,(*selectedJets)[l]->eta_,(*selectedJets)[l]->phi_,0);
           break;
       }
     }
     met_tHFCNC.SetPtEtaPhiM(MET_pt,0,MET_phi,0);
     nut_tZFCNC.SetPtEtaPhiM(MET_pt,0,MET_phi,0);
     float bestMass=10000;
     for (UInt_t i=0;i<selectedJets->size();i++){
       if(selectedJets->size()==2 && !(*selectedJets)[i]->btag_) hU_tHFCNC=(*selectedJets)[i]->p4_;
         for (UInt_t j=i+1;j<selectedJets->size();j++){
           if((*selectedJets)[i]->btag_ || (*selectedJets)[j]->btag_) continue;
           if(abs(((*selectedJets)[i]->p4_ + (*selectedJets)[j]->p4_).M()-80)<bestMass){
            hU_tHFCNC=(*selectedJets)[i]->p4_; hD_tHFCNC=(*selectedJets)[j]->p4_;
            bestMass=((*selectedJets)[i]->p4_ + (*selectedJets)[j]->p4_).M();
          }
        }
     }
     lt_tZFCNC.SetPtEtaPhiM(0,0,0,0); lpZ_tZFCNC.SetPtEtaPhiM(0,0,0,0); lmZ_tZFCNC.SetPtEtaPhiM(0,0,0,0);
     hL_tHFCNC.SetPtEtaPhiM(0,0,0,0); tL_tHFCNC.SetPtEtaPhiM(0,0,0,0);
     tL_tHFCNC=(*selectedLeptons)[0]->p4_;
     hL_tHFCNC=(*selectedLeptons)[1]->p4_;
     jigsawThFCNC->Analyze(tL_tHFCNC, hL_tHFCNC, tB_tHFCNC, hU_tHFCNC, hD_tHFCNC, met_tHFCNC);
     if(Z_FP->size()>0 && selectedLeptons->size()>2){
       lpZ_tZFCNC.SetPtEtaPhiM((*selectedLeptons)[(*Z_FP)[lZfp]->lep1_]->pt_,(*selectedLeptons)[(*Z_FP)[lZfp]->lep1_]->eta_,(*selectedLeptons)[(*Z_FP)[lZfp]->lep1_]->phi_,0);
       lmZ_tZFCNC.SetPtEtaPhiM((*selectedLeptons)[(*Z_FP)[lZfp]->lep2_]->pt_,(*selectedLeptons)[(*Z_FP)[lZfp]->lep2_]->eta_,(*selectedLeptons)[(*Z_FP)[lZfp]->lep2_]->phi_,0);
       for (UInt_t l=0;l<selectedLeptons->size();l++){
         if(l!=(*Z_FP)[lZfp]->lep1_ && l!=(*Z_FP)[lZfp]->lep2_)  lt_tZFCNC.SetPtEtaPhiM((*selectedLeptons)[l]->pt_,(*selectedLeptons)[l]->eta_,(*selectedLeptons)[l]->phi_,0);
       }
     }
     else{
      if(selectedLeptons->size()>0) lpZ_tZFCNC.SetPtEtaPhiM((*selectedLeptons)[0]->pt_,(*selectedLeptons)[0]->eta_,(*selectedLeptons)[0]->phi_,0);
      if(selectedLeptons->size()>1) lmZ_tZFCNC.SetPtEtaPhiM((*selectedLeptons)[1]->pt_,(*selectedLeptons)[1]->eta_,(*selectedLeptons)[1]->phi_,0);
      if(selectedLeptons->size()>2) lt_tZFCNC.SetPtEtaPhiM((*selectedLeptons)[2]->pt_,(*selectedLeptons)[2]->eta_,(*selectedLeptons)[2]->phi_,0);
     }
     jigsawTzFCNC->Analyze(lt_tZFCNC, lpZ_tZFCNC, lmZ_tZFCNC, bt_tZFCNC,nut_tZFCNC);

     tH_topMass_=jigsawThFCNC->T->GetMass();
     tH_HMass_=jigsawThFCNC->H->GetMass();
     tH_WtopMass_=jigsawThFCNC->WT->GetMass();
     tH_W1HMass_=jigsawThFCNC->W1H->GetMass();
     tH_W2HMass_=jigsawThFCNC->W2H->GetMass();
     tH_HPt_=jigsawThFCNC->H->GetFourVector().Pt();
     tH_HEta_=jigsawThFCNC->H->GetFourVector().Eta();
     tH_topPt_=jigsawThFCNC->T->GetFourVector().Pt();
     tH_topEta_=jigsawThFCNC->T->GetFourVector().Eta();
     tH_drWtopB_=deltaR(jigsawThFCNC->WT->GetFourVector().Eta(),jigsawThFCNC->WT->GetFourVector().Phi(),tB_tHFCNC.Eta(),tB_tHFCNC.Phi());
     tH_drW1HW2H_=deltaR(jigsawThFCNC->W1H->GetFourVector().Eta(),jigsawThFCNC->W1H->GetFourVector().Phi(),jigsawThFCNC->W2H->GetFourVector().Eta(),jigsawThFCNC->W2H->GetFourVector().Phi());

     tZ_topMass_=jigsawTzFCNC->T->GetMass();
     tZ_ZMass_=jigsawTzFCNC->Z->GetMass();
     tZ_WtopMass_=jigsawTzFCNC->W->GetMass();;
     tZ_ZPt_=jigsawTzFCNC->Z->GetFourVector().Pt();
     tZ_ZEta_=jigsawTzFCNC->Z->GetFourVector().Eta();
     tZ_topPt_=jigsawTzFCNC->T->GetFourVector().Pt();
     tZ_topEta_=jigsawTzFCNC->T->GetFourVector().Eta();

     HT_=HTjets;
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
      for (UInt_t l=0;l<selectedJets->size();l++){
        if((*selectedJets)[l]->btag_){
          bJetPt_=(*selectedJets)[l]->pt_;
          bJetEta_=(*selectedJets)[l]->eta_;
          break;
        }
      }
     }
     ch_=ch;
     chFA_=chFA;
     weightSM_=weight_lepB;
     weightSMfake_=weight_lepB*fakeRate;

     if (iseft) eft_fit = new WCFit(nWCnames, wc_names_lst, nEFTfitCoefficients, EFTfitCoefficients, weight_EFT);
     else eft_fit = new WCFit(0,wc_names_lst,1, &genWeight, 1.0);
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
     delete eft_fit;
  
    if(MVAB_TU!=0) MVATU_=MVAS_TU/MVAB_TU;
    else MVATU_= -1;
 //   tree_out->Fill();
   }

   objectSelectionEnd();
//cout<<1<<" "; printMemoryUsage();
  }
  memory = getValue(); 
  cout<<"Virtual Memory: "<<getValue()/1000000.0<<" GB"<<endl;
  printMemoryUsage();
  cout<<"Loop is completed"<<endl;
  cout<<"from "<<ntr<<" events, "<<nAccept<<" events are accepted"<<endl;
  TFile file_out (("ANoutput" + std::to_string(end) + ".root").c_str(),"RECREATE");
  endHists(data, year, ifSys);
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
  mll_SS_Zwindow_0jet->Write("",TObject::kOverwrite);
//  genAnalysis.writeGENHists();
  file_out.Close() ;

  delete jigsawTzFCNC;
  delete jigsawThFCNC;
  delete h2_BTaggingEff_Denom_b    ;
  delete h2_BTaggingEff_Denom_c    ;
  delete h2_BTaggingEff_Denom_udsg ;
  delete h2_BTaggingEff_Num_b      ;
  delete h2_BTaggingEff_Num_c      ;
  delete h2_BTaggingEff_Num_udsg   ;
  delete JigsawWmass ;
  delete JigsawTmass ;
  delete JigsawWmassReco;
  delete JigsawTmassReco;
  delete JigsawWmass_tHFCNC;
  delete JigsawTmass_tHFCNC;
  delete JigsawHmass_tHFCNC;
  delete JigsawWmassReco_tHFCNC;
  delete JigsawTmassReco_tHFCNC;
  delete JigsawHmassReco_tHFCNC;
  delete DRij;
  delete DRtH;
  delete DRWHWH;
  delete DPhitH;
  delete HmassVsnJet;
  delete crossSection;
  delete mll_SS_Zwindow_0jet;
  malloc_trim(0);
  cout<<  "File ANoutput" + std::to_string(end) + ".root is made"<<endl;
  cout<<"Job is finished"<<endl;
  cout<<"Total Virtual Memory: "<<getValue()/1048576.0<<" GB"<<endl;

}


void MyAnalysis::FillD3Hists(D3HistsContainer H3, std::vector<int> v1, std::vector<int> v2, int v3, float value, std::vector<std::vector<float>> weight, std::vector<std::vector<WCFit>> wcfit){
  for (UInt_t i = 0; i < v1.size(); ++i) {
    for (UInt_t j = 0; j < v2.size(); ++j) {
      if(v1[i]<0 || v2[j]<0) continue;
//      std::cout << "Accessing hist at [" << v1[i] << "][" << v2[j] << "]["<<v3<< std::endl;
      H3[v1[i]][v2[j]][v3]->Fill(value, weight[i][j], wcfit[i][j]);
    }
  }
}

void MyAnalysis::FillD4Hists(D4HistsContainer H4, std::vector<int> v1, std::vector<int> v2, int v3, float value, std::vector<std::vector<float>> weight, std::vector<std::vector<WCFit>> wcfit, int n){
  for (UInt_t i = 0; i < v1.size(); ++i) {
    for (UInt_t j = 0; j < v2.size(); ++j) {
      if(v1[i]<0 || v2[j]<0) continue;
      H4[v1[i]][v2[j]][v3][n]->Fill(value, weight[i][j], wcfit[i][j]);
    }
  }
}

void MyAnalysis::normalFillD4Hists(normalD4HistsContainer H4, std::vector<int> v1, std::vector<int> v2, int v3, float value, std::vector<std::vector<float>> weight, int n){
  for (UInt_t i = 0; i < v1.size(); ++i) {
    for (UInt_t j = 0; j < v2.size(); ++j) {
      if(v1[i]<0 || v2[j]<0) continue;
      H4[v1[i]][v2[j]][v3][n]->Fill(value, weight[i][j]);
    }
  }
}
