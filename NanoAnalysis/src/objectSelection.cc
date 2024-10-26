#include "objectSelection.h"

objectSelection::objectSelection(MyAnalysis *evt, TString year){
  eI = evt;
  if (year == "2016preVFP"){
    bTagCutWpL=0.0508;
    bTagCutWpM=0.2598;
  }
  else if (year == "2016postVFP"){
    bTagCutWpL=0.0480;
    bTagCutWpM=0.2489;
  }
  else if (year == "2017"){
    bTagCutWpL=0.0532;
    bTagCutWpM=0.3040;
  }
  else if (year == "2018"){
    bTagCutWpL=0.0490;
    bTagCutWpM=0.2783;
  }
  else cout<<"Error: year name is not consistant"<<endl;
}

float objectSelection::conept_TTH(int l, int pdgid){
    if (abs(pdgid)==13){
      if(eI->Muon_mediumId[l]>0 && eI->Muon_mvaTTHUL[l] > 0.85) return eI->Muon_pt[l];
      else return 0.90 * eI->Muon_pt[l] * (1 + eI->Muon_jetRelIso[l]);
    }
    if (abs(pdgid)==11){
      if(eI->Electron_mvaTTHUL[l] > 0.85) return eI->Electron_pt[l];
      else return 0.90 * eI->Electron_pt[l] * (1 + eI->Electron_jetRelIso[l]);
    }
}

float objectSelection::jetBTagDeepFlav(int l){
  if(l<0) return -99;
  else return eI->Jet_btagDeepFlavB[l];
}

bool objectSelection::ttH_idEmu_cuts_E3(int l){
    if (eI->Electron_hoe[l]>=(0.10-0.00*(abs(eI->Electron_eta[l]+eI->Electron_deltaEtaSC[l])>1.479))) return false;
    if (eI->Electron_eInvMinusPInv[l]<=-0.04) return false;
    if (eI->Electron_sieie[l]>=(0.011+0.019*(abs(eI->Electron_eta[l]+eI->Electron_deltaEtaSC[l])>1.479))) return false;
    return true;
}

float objectSelection::smoothBFlav(float jetpt, float ptmin, float ptmax){
    double x = min(max(0.0, double (jetpt - ptmin))/(ptmax-ptmin), 1.0);
    return x*bTagCutWpL + (1-x)*bTagCutWpM;
}

bool objectSelection::looseMuon(int l){
  return (abs(eI->Muon_eta[l]) < 2.4 && eI->Muon_miniPFRelIso_all[l] < miniRelIso && eI->Muon_sip3d[l] < sip3d && abs(eI->Muon_dxy[l]) < dxy && abs(eI->Muon_dz[l]) < dz && eI->Muon_looseId[l]);
}


bool objectSelection::looseElectron(int l){
  return (abs(eI->Electron_eta[l]) < 2.5 && eI->Electron_miniPFRelIso_all[l] < miniRelIso && eI->Electron_sip3d[l] < sip3d && abs(eI->Electron_dxy[l]) < dxy && abs(eI->Electron_dz[l]) < dz && eI->Electron_lostHits[l]<=1 && eI->Electron_mvaFall17V2noIso_WPL[l]);
}

bool objectSelection::fakeMuon(int l){
  return(jetBTagDeepFlav(eI->Muon_jetIdx[l])<bTagCutWpM && (eI->Muon_mvaTTHUL[l]>0.85 || (jetBTagDeepFlav(eI->Muon_jetIdx[l]) < smoothBFlav(0.9*eI->Muon_pt[l]*(1+eI->Muon_jetRelIso[l]), 20, 45) && eI->Muon_jetRelIso[l] < 0.50)));
}

bool objectSelection::fakeElectron(int l){
  return (jetBTagDeepFlav(eI->Electron_jetIdx[l])<bTagCutWpM && ttH_idEmu_cuts_E3(l) && eI->Electron_convVeto[l] && eI->Electron_lostHits[l] == 0 && (eI->Electron_mvaTTHUL[l]>0.90 || (eI->Electron_mvaFall17V2noIso_WP90[l] && jetBTagDeepFlav(eI->Electron_jetIdx[l]) < smoothBFlav(0.9*eI->Electron_pt[l]*(1+eI->Electron_jetRelIso[l]), 20, 45) && eI->Electron_jetRelIso[l] < 1.0))); 
}

bool objectSelection::tightMuon(int l){
  return (eI->Muon_mvaTTHUL[l]>0.85 && fakeMuon(l) && eI->Muon_mediumId[l]>0);
}

bool objectSelection::tightElectron(int l){
  return (eI->Electron_mvaTTHUL[l]>0.90 && fakeElectron(l));
}

bool objectSelection::tightCharge(int l, int pdgid){
  if(abs(pdgid) == 11){
    if (eI->Electron_tightCharge[l]>=2) return true;
  }
  if(abs(pdgid) == 13){
    if (eI->Muon_tightCharge[l]>=1) return true;
  }
  return false;
}

bool objectSelection::isMatched(int l, int pdgid, TString MC, bool ifChargedMatched){
  if (MC=="data") return true;
  if(abs(pdgid) == 11){
    if(!ifChargedMatched){
      if(eI->Electron_genPartFlav[l]==1 || eI->Electron_genPartFlav[l]==15) return true;
    }
    if(ifChargedMatched){
      if((eI->Electron_genPartFlav[l]==1 || eI->Electron_genPartFlav[l]==15) && (eI->GenPart_pdgId[eI->Electron_genPartIdx[l]]*eI->Electron_pdgId[l]>0)) return true; 
    }
  }
  if(abs(pdgid) == 13){
    if(eI->Muon_genPartFlav[l]==1 || eI->Muon_genPartFlav[l]==15) return true;
  }
  return false;
}

objectSelection::~objectSelection(){}
