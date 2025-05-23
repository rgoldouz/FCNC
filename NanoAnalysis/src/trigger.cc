#include "MyAnalysis.h"
#include "TH1EFT.h"

bool MyAnalysis::trigger(TString data,TString dataset,string year){

  bool triggerPass=false;
  bool triggerPassEE = false;
  bool triggerPassEMu = false;
  bool triggerPassMuMu = false;
  bool triggerPassE = false;
  bool triggerPassMu = false;
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
  return triggerPass;  

}
