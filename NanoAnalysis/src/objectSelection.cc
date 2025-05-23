#include "MyAnalysis.h"
#include "Utils.h"

void MyAnalysis::objectSelection(TString data,string year){
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
  for (int n=0;n<sys.size();++n){
    nominalWeights[n] =1;
    sysUpWeights[n] =1;
    sysDownWeights[n] =1;
  }
  float eReco=1;
  float eID1=1;
  float eID2=1;
  float eID3=1;
  float eRecoUp=1;
  float eID1Up=1;
  float eID2Up=1;
  float eID3Up=1;
  float eRecoDown=1;
  float eID1Down=1;
  float eID2Down=1;
  float eID3Down=1;
  float muReco=1;
  float muID1=1;
  float muID2=1;
  float muID3=1;
  float muRecoUp=1;
  float muID1Up=1;
  float muID2Up=1;
  float muID3Up=1;
  float muRecoDown=1;
  float muID1Down=1;
  float muID2Down=1;
  float muID3Down=1;
  float BJetSF=1;
  float CJetSF=1;
  float LJetSF=1;
  float BJetSF_UpCorr=1;
  float CJetSF_UpCorr=1;
  float LJetSF_UpCorr=1;
  float BJetSF_UpUnCorr=1;
  float CJetSF_UpUnCorr=1;
  float LJetSF_UpUnCorr=1;
  float BJetSF_DownCorr=1;
  float CJetSF_DownCorr=1;
  float LJetSF_DownCorr=1;
  float BJetSF_DownUnCorr=1;
  float CJetSF_DownUnCorr=1;
  float LJetSF_DownUnCorr=1;
  float BJetEff=1;
  float CJetEff=1;
  float LJetEff=1;
  double P_bjet_mc=1;
  bool jetlepfail;
  double muPtSFRochester;
  selectedLeptons = new std::vector<lepton_candidate*>();
  selectedPLeptons = new std::vector<lepton_candidate*>();
  selectedFLeptons = new std::vector<lepton_candidate*>();
  selectedLooseLeptons = new std::vector<lepton_candidate*>();
  Z_P = new std::vector<Z_candidate*>();
  Z_FP = new std::vector<Z_candidate*>();
// electron
  for (int l=0;l<nElectron;l++){
    if(abs(Electron_eta[l]) > 2.4 || (abs(Electron_eta[l])> 1.4442 && (abs(Electron_eta[l])< 1.566))) continue;
    if(looseElectron(l) && Electron_pt[l]>7) selectedLooseLeptons->push_back(new lepton_candidate(Electron_pt[l],Electron_eta[l],Electron_phi[l],Electron_charge[l],l,1, Electron_pdgId[l]));
    if(looseElectron(l) && tightElectron(l) && Electron_pt[l] >10){
      selectedPLeptons->push_back(new lepton_candidate(Electron_pt[l],Electron_eta[l],Electron_phi[l],Electron_charge[l],l,1, Electron_pdgId[l]));
      if (data == "mc"  && Electron_pt[l]>10){
        if(Electron_pt[l]>20) {
          nominalWeights[getVecPos(sys,"eleRecoIdIso")] = nominalWeights[getVecPos(sys,"eleRecoIdIso")] * csetEleIdReco->evaluate({year, "sf", "RecoAbove20", Electron_eta[l],Electron_pt[l]});
          eReco = eReco * csetEleIdReco->evaluate({year, "sf", "RecoAbove20", Electron_eta[l],Electron_pt[l]});
          eRecoUp = eRecoUp* csetEleIdReco->evaluate({year, "sfup", "RecoAbove20", Electron_eta[l],Electron_pt[l]});
          eRecoDown = eRecoDown * csetEleIdReco->evaluate({year, "sfdown", "RecoAbove20", Electron_eta[l],Electron_pt[l]});        
        }
        if(Electron_pt[l]<20) {
          nominalWeights[getVecPos(sys,"eleRecoIdIso")] = nominalWeights[getVecPos(sys,"eleRecoIdIso")] * csetEleIdReco->evaluate({year, "sf", "RecoBelow20", Electron_eta[l],Electron_pt[l]});
          eReco = eReco * csetEleIdReco->evaluate({year, "sf", "RecoBelow20", Electron_eta[l],Electron_pt[l]});
          eRecoUp = eRecoUp* csetEleIdReco->evaluate({year, "sfup", "RecoBelow20", Electron_eta[l],Electron_pt[l]});
          eRecoDown = eRecoDown * csetEleIdReco->evaluate({year, "sfdown", "RecoBelow20", Electron_eta[l],Electron_pt[l]});
        }
        nominalWeights[getVecPos(sys,"eleRecoIdIso")] = nominalWeights[getVecPos(sys,"eleRecoIdIso")] * scale_factor(sf_eleLoose_H, abs(Electron_eta[l]),Electron_pt[l],"central",false, true);
        nominalWeights[getVecPos(sys,"eleRecoIdIso")] = nominalWeights[getVecPos(sys,"eleRecoIdIso")] * scale_factor(sf_eleIsoIp_H, abs(Electron_eta[l]),Electron_pt[l],"central",false, true);
        nominalWeights[getVecPos(sys,"eleRecoIdIso")] = nominalWeights[getVecPos(sys,"eleRecoIdIso")] * scale_factor(sf_eleLooseMVATight_H, abs(Electron_eta[l]),Electron_pt[l],"central",false, true);

        eID1=eID1* scale_factor(sf_eleLoose_H, abs(Electron_eta[l]),Electron_pt[l],"central",false, true);
        eID2=eID2* scale_factor(sf_eleIsoIp_H, abs(Electron_eta[l]),Electron_pt[l],"central",false, true);
        eID3=eID3* scale_factor(sf_eleLooseMVATight_H, abs(Electron_eta[l]),Electron_pt[l],"central",false, true);
        eID1Up=eID1Up*scale_factor(sf_eleLoose_H, abs(Electron_eta[l]),Electron_pt[l],"up",false, true);
        eID2Up=eID2Up*scale_factor(sf_eleIsoIp_H, abs(Electron_eta[l]),Electron_pt[l],"up",false, true);
        eID3Up=eID3Up* scale_factor(sf_eleLooseMVATight_H, abs(Electron_eta[l]),Electron_pt[l],"up",false, true);
        eID1Down=eID1Down*scale_factor(sf_eleLoose_H, abs(Electron_eta[l]),Electron_pt[l],"down",false, true);
        eID2Down=eID2Down*scale_factor(sf_eleIsoIp_H, abs(Electron_eta[l]),Electron_pt[l],"down",false, true);
        eID3Down=eID3Down* scale_factor(sf_eleLooseMVATight_H, abs(Electron_eta[l]),Electron_pt[l],"down",false, true);
      }
    }
    if(looseElectron(l) && fakeElectron(l) && !tightElectron(l) && conept_TTH(l,11)>10) selectedFLeptons->push_back(new lepton_candidate(Electron_pt[l],Electron_eta[l],Electron_phi[l],Electron_charge[l],l,1, Electron_pdgId[l]));
  }

  sysUpWeights[getVecPos(sys,"eleRecoIdIso")] = nominalWeights[getVecPos(sys,"eleRecoIdIso")] + sqrt(pow(eReco-eRecoUp,2)+pow(eID1-eID1Up,2)+pow(eID2-eID2Up,2)+pow(eID3-eID3Up,2));
  sysDownWeights[getVecPos(sys,"eleRecoIdIso")] = nominalWeights[getVecPos(sys,"eleRecoIdIso")] - sqrt(pow(eReco-eRecoDown,2)+pow(eID1-eID1Down,2)+pow(eID2-eID2Down,2)+pow(eID3-eID3Down,2));
// Muon selection
  for (int l=0;l<nMuon;l++){
    if(Muon_pt[l] > 7 && looseMuon(l)) selectedLooseLeptons->push_back(new lepton_candidate(Muon_pt[l],Muon_eta[l],Muon_phi[l],Muon_charge[l],l,10, Muon_pdgId[l]));
    muPtSFRochester=1;
    if(data == "data" && Muon_pt[l]>20 && abs(Muon_eta[l])<2.4) muPtSFRochester = rc.kScaleDT(Muon_charge[l], Muon_pt[l],Muon_eta[l],Muon_phi[l], 0, 0);
    if (data == "mc" && Muon_pt[l]>20 && abs(Muon_eta[l])<2.4){
      if (Muon_genPartIdx[l]>=0 && Muon_genPartIdx[l]<=nGenPart) muPtSFRochester = rc.kSpreadMC(Muon_charge[l], Muon_pt[l],Muon_eta[l],Muon_phi[l], GenPart_pt[Muon_genPartIdx[l]],0, 0);
      if (Muon_genPartIdx[l]<0) muPtSFRochester = rc.kSmearMC(Muon_charge[l], Muon_pt[l],Muon_eta[l],Muon_phi[l], Muon_nTrackerLayers[l] , gRandom->Rndm(),0, 0);
    }
    if(looseMuon(l) && tightMuon(l) && muPtSFRochester * Muon_pt[l] >10){
      selectedPLeptons->push_back(new lepton_candidate(muPtSFRochester*Muon_pt[l],Muon_eta[l],Muon_phi[l],Muon_charge[l],l,10, Muon_pdgId[l]));
      if (data == "mc" && muPtSFRochester *Muon_pt[l] > 15){
      nominalWeights[getVecPos(sys,"muRecoIdIso")] = nominalWeights[getVecPos(sys,"muRecoIdIso")] * csetMuReco->evaluate({year + "_UL", abs(Muon_eta[l]),  muPtSFRochester *Muon_pt[l], "sf"});
      nominalWeights[getVecPos(sys,"muRecoIdIso")] = nominalWeights[getVecPos(sys,"muRecoIdIso")] * csetMuLoose->evaluate({year + "_UL", abs(Muon_eta[l]),  muPtSFRochester *Muon_pt[l], "sf"});
      nominalWeights[getVecPos(sys,"muRecoIdIso")] = nominalWeights[getVecPos(sys,"muRecoIdIso")] * scale_factor(sf_muonIsoIp_H, abs(Muon_eta[l]),muPtSFRochester *Muon_pt[l],"central",false, true);
      nominalWeights[getVecPos(sys,"muRecoIdIso")] = nominalWeights[getVecPos(sys,"muRecoIdIso")] * scale_factor(sf_muonLooseMVATight_H, abs(Muon_eta[l]),muPtSFRochester *Muon_pt[l],"central",false, true);

      muReco=muReco* csetMuReco->evaluate({year + "_UL", abs(Muon_eta[l]),  muPtSFRochester *Muon_pt[l], "sf"});
      muID1=muID1* csetMuLoose->evaluate({year + "_UL", abs(Muon_eta[l]),  muPtSFRochester *Muon_pt[l], "sf"});
      muID2=muID2* scale_factor(sf_muonIsoIp_H, abs(Muon_eta[l]),muPtSFRochester *Muon_pt[l],"central",false, true);
      muID3=muID3*scale_factor(sf_muonLooseMVATight_H, abs(Muon_eta[l]),muPtSFRochester *Muon_pt[l],"central",false, true);

      muRecoUp=muRecoUp* csetMuReco->evaluate({year + "_UL", abs(Muon_eta[l]),  muPtSFRochester *Muon_pt[l], "systup"});
      muID1Up=muID1Up * csetMuLoose->evaluate({year + "_UL", abs(Muon_eta[l]),  muPtSFRochester *Muon_pt[l], "systup"});
      muID2Up=muID2Up* scale_factor(sf_muonIsoIp_H, abs(Muon_eta[l]),muPtSFRochester *Muon_pt[l],"up",false, true);
      muID3Up=muID3Up* scale_factor(sf_muonLooseMVATight_H, abs(Muon_eta[l]),muPtSFRochester *Muon_pt[l],"up",false, true);

      muRecoDown=muRecoDown * csetMuReco->evaluate({year + "_UL", abs(Muon_eta[l]),  muPtSFRochester *Muon_pt[l], "systdown"});
      muID1Down=muID1Down* csetMuLoose->evaluate({year + "_UL", abs(Muon_eta[l]),  muPtSFRochester *Muon_pt[l], "systdown"});
      muID2Down=muID2Down* scale_factor(sf_muonIsoIp_H, abs(Muon_eta[l]),muPtSFRochester *Muon_pt[l],"down",false, true);
      muID3Down=muID3Down* scale_factor(sf_muonLooseMVATight_H, abs(Muon_eta[l]),muPtSFRochester *Muon_pt[l],"down",false, true);	
      
      }
    }
    if(looseMuon(l) && fakeMuon(l) && !tightMuon(l) && conept_TTH(l,13)>10) selectedFLeptons->push_back(new lepton_candidate(Muon_pt[l],Muon_eta[l],Muon_phi[l],Muon_charge[l],l,10,Muon_pdgId[l]));
  }

  sysUpWeights[getVecPos(sys,"muRecoIdIso")] = nominalWeights[getVecPos(sys,"muRecoIdIso")] + sqrt(pow(muReco-muRecoUp,2)+pow(muID1-muID1Up,2)+pow(muID2-muID2Up,2)+pow(muID3-muID3Up,2));
  sysDownWeights[getVecPos(sys,"muRecoIdIso")] = nominalWeights[getVecPos(sys,"muRecoIdIso")] - sqrt(pow(muReco-muRecoDown,2)+pow(muID1-muID1Down,2)+pow(muID2-muID2Down,2)+pow(muID3-muID3Down,2));

    sort(selectedPLeptons->begin(), selectedPLeptons->end(), ComparePtLep);
    sort(selectedFLeptons->begin(), selectedFLeptons->end(), ComparePtLep);
    selectedLeptons->insert(selectedLeptons->end(), selectedPLeptons->begin(), selectedPLeptons->end());
    selectedLeptons->insert(selectedLeptons->end(), selectedFLeptons->begin(), selectedFLeptons->end());
    sort(selectedLeptons->begin(), selectedLeptons->end(), ComparePtLep);

    for (UInt_t i=0;i<selectedPLeptons->size();i++){
      for (UInt_t j=i+1;j<selectedPLeptons->size();j++){
        if(((*selectedPLeptons)[i]->lep_ + (*selectedPLeptons)[j]->lep_ == 2 || (*selectedPLeptons)[i]->lep_ + (*selectedPLeptons)[j]->lep_ == 20) &&
           (*selectedPLeptons)[i]->charge_ + (*selectedPLeptons)[j]->charge_ ==0 ){
             Z_P->push_back(new Z_candidate(i,j, ((*selectedPLeptons)[i]->p4_ + (*selectedPLeptons)[j]->p4_).Pt(), ((*selectedPLeptons)[i]->p4_ + (*selectedPLeptons)[j]->p4_).Eta(),((*selectedPLeptons)[i]->p4_ + (*selectedPLeptons)[j]->p4_).Phi(),((*selectedPLeptons)[i]->p4_ + (*selectedPLeptons)[j]->p4_).M() ));
        }
      }
    }

    for (UInt_t i=0;i<selectedLeptons->size();i++){
      for (UInt_t j=i+1;j<selectedLeptons->size();j++){
        if(((*selectedLeptons)[i]->lep_ + (*selectedLeptons)[j]->lep_ == 2 || (*selectedLeptons)[i]->lep_ + (*selectedLeptons)[j]->lep_ == 20) &&
           (*selectedLeptons)[i]->charge_ + (*selectedLeptons)[j]->charge_ ==0 ){
             Z_FP->push_back(new Z_candidate(i,j, ((*selectedLeptons)[i]->p4_ + (*selectedLeptons)[j]->p4_).Pt(), ((*selectedLeptons)[i]->p4_ + (*selectedLeptons)[j]->p4_).Eta(),((*selectedLeptons)[i]->p4_ + (*selectedLeptons)[j]->p4_).Phi(),((*selectedLeptons)[i]->p4_ + (*selectedLeptons)[j]->p4_).M() ));
        }
      }
    }



//jets
    selectedJets = new std::vector<jet_candidate*>();
    JECsysUp = new std::vector<std::vector<jet_candidate*>>(nsrc + 1);
    JECsysDown = new std::vector<std::vector<jet_candidate*>>(nsrc + 1);
    float cJER;
    float cJERUp;
    float cJERDown;
    float jesVar;
    float jer_sf;
    float jer_sfUp;
    float jer_sfDown;
    float sigma;
    float jet_resolution;
    std::random_device rd{}; 
    std::mt19937 gen{rd()}; 
    for (int l=0;l<nJet;l++){
      if(Jet_jetId[l]==0 || abs(Jet_eta[l]) >= 2.4) continue;
      if (jetVetoMaps_H->GetBinContent(jetVetoMaps_H->GetXaxis()->FindBin(Jet_eta[l]),jetVetoMaps_H->GetYaxis()->FindBin(Jet_phi[l]))>0) continue;
      cJER=1;cJERUp=1;cJERDown=1; 
      jetlepfail = false;
      for (int i=0;i<selectedLooseLeptons->size();i++){
        if(deltaR((*selectedLooseLeptons)[i]->eta_,(*selectedLooseLeptons)[i]->phi_,Jet_eta[l],Jet_phi[l]) < 0.4 ) jetlepfail=true;
      }
      if(jetlepfail) continue;
      if(data == "mc"){
        jer_sf=uncRes.getScaleFactor({{JME::Binning::JetEta, Jet_eta[l]}}, Variation::NOMINAL); 
        jer_sfUp=uncRes.getScaleFactor({{JME::Binning::JetEta, Jet_eta[l]}}, Variation::UP);
        jer_sfDown=uncRes.getScaleFactor({{JME::Binning::JetEta, Jet_eta[l]}}, Variation::DOWN);
        jet_resolution = resolution.getResolution({{JME::Binning::JetPt, Jet_pt[l]}, {JME::Binning::JetEta, Jet_eta[l]}, {JME::Binning::Rho, fixedGridRhoFastjetAll}});
        if(Jet_genJetIdx[l]>=0){
          cJER=1+(jer_sf-1)*((Jet_pt[l]-GenJet_pt[Jet_genJetIdx[l]])/Jet_pt[l]);
          cJERUp=1+(jer_sfUp-1)*((Jet_pt[l]-GenJet_pt[Jet_genJetIdx[l]])/Jet_pt[l]);
          cJERDown=1+(jer_sfDown-1)*((Jet_pt[l]-GenJet_pt[Jet_genJetIdx[l]])/Jet_pt[l]);
        }
        else{
          sigma = jet_resolution * std::sqrt(jer_sf * jer_sf - 1);
          std::normal_distribution<> d(0, sigma);
          cJER = 1. + d(gen);
          sigma = jet_resolution * std::sqrt(jer_sfUp * jer_sfUp - 1);
          std::normal_distribution<> e(0, sigma);
          cJERUp = 1. + e(gen);
          sigma = jet_resolution * std::sqrt(jer_sfDown * jer_sfDown - 1);
          std::normal_distribution<> f(0, sigma);
          cJERDown = 1. + f(gen);
        }
        if(Jet_puId[l]<1 && cJER*Jet_pt[l]<50) continue;
        if(cJER*Jet_pt[l]>30)  selectedJets->push_back(new jet_candidate(cJER*Jet_pt[l],Jet_eta[l],Jet_phi[l],Jet_mass[l],Jet_btagDeepFlavB[l], year,Jet_partonFlavour[l]));
        if (cJERUp*Jet_pt[l]>30) (*JECsysUp)[nsrc].push_back(new jet_candidate(cJERUp*Jet_pt[l],Jet_eta[l],Jet_phi[l],Jet_mass[l],Jet_btagDeepFlavB[l], year,Jet_partonFlavour[l]));
        if (cJERDown*Jet_pt[l]>30) (*JECsysDown)[nsrc].push_back(new jet_candidate(cJERDown*Jet_pt[l],Jet_eta[l],Jet_phi[l],Jet_mass[l],Jet_btagDeepFlavB[l], year,Jet_partonFlavour[l]));

        if(cJER*Jet_pt[l]>30 && cJER*Jet_pt[l] <50){
          nominalWeights[getVecPos(sys,"JetPuID")] = nominalWeights[getVecPos(sys,"JetPuID")] * csetJetPuID->evaluate({Jet_eta[l],cJER*Jet_pt[l],"nom","L"});
          sysUpWeights[getVecPos(sys,"JetPuID")] = sysUpWeights[getVecPos(sys,"JetPuID")] * csetJetPuID->evaluate({Jet_eta[l],cJER*Jet_pt[l],"up","L"});
          sysDownWeights[getVecPos(sys,"JetPuID")] = sysDownWeights[getVecPos(sys,"JetPuID")] * csetJetPuID->evaluate({Jet_eta[l],cJER*Jet_pt[l],"down","L"});
        }
        for (int n=0;n<nsrc;++n){
          vsrc[n]->setJetPt(Jet_pt[l]);
          vsrc[n]->setJetEta(Jet_eta[l]);
          jesVar = vsrc[n]->getUncertainty(true);
          if ((1+jesVar)*cJER*Jet_pt[l]>30)  (*JECsysUp)[n].push_back(new jet_candidate((1+jesVar)*cJER*Jet_pt[l],Jet_eta[l],Jet_phi[l],Jet_mass[l],Jet_btagDeepFlavB[l], year,Jet_partonFlavour[l]));
          if ((1-jesVar)*cJER*Jet_pt[l]>30)  (*JECsysDown)[n].push_back(new jet_candidate((1-jesVar)*cJER*Jet_pt[l],Jet_eta[l],Jet_phi[l],Jet_mass[l],Jet_btagDeepFlavB[l], year,Jet_partonFlavour[l]));
        }
      }
      if(data == "data" && Jet_pt[l] >30){
        if(Jet_puId[l]<1 && Jet_pt[l]<50) continue;
        selectedJets->push_back(new jet_candidate(Jet_pt[l],Jet_eta[l],Jet_phi[l],Jet_mass[l],Jet_btagDeepFlavB[l],year,0));
      }
    }
    

    sort(selectedJets->begin(), selectedJets->end(), ComparePtJet);

// Btag SF
    for (int l=0;l<selectedJets->size();l++){
      if(data == "data") continue;
      if((*selectedJets)[l]->pt_<30) continue;
      BJetSF=csetBcJetSF->evaluate({"central", "M", 5, abs((*selectedJets)[l]->eta_),(*selectedJets)[l]->pt_});
      CJetSF=csetBcJetSF->evaluate({"central", "M", 4, abs((*selectedJets)[l]->eta_),(*selectedJets)[l]->pt_});
      LJetSF=csetLightJetSF->evaluate({"central", "M", 0, abs((*selectedJets)[l]->eta_),(*selectedJets)[l]->pt_});
      BJetEff=scale_factor(btagEff_b_H, (*selectedJets)[l]->pt_, abs((*selectedJets)[l]->eta_),"central", true, false);
      CJetEff=scale_factor(btagEff_c_H, (*selectedJets)[l]->pt_, abs((*selectedJets)[l]->eta_),"central", true, false);
      LJetEff=scale_factor(btagEff_udsg_H, (*selectedJets)[l]->pt_, abs((*selectedJets)[l]->eta_),"central", true, false);
      BJetSF_UpCorr=csetBcJetSF->evaluate({"up_correlated", "M", 5, abs((*selectedJets)[l]->eta_),(*selectedJets)[l]->pt_});
      CJetSF_UpCorr=csetBcJetSF->evaluate({"up_correlated", "M", 4, abs((*selectedJets)[l]->eta_),(*selectedJets)[l]->pt_});
      LJetSF_UpCorr=csetLightJetSF->evaluate({"up_correlated", "M", 0, abs((*selectedJets)[l]->eta_),(*selectedJets)[l]->pt_});
      BJetSF_UpUnCorr=csetBcJetSF->evaluate({"up_uncorrelated", "M", 5, abs((*selectedJets)[l]->eta_),(*selectedJets)[l]->pt_});
      CJetSF_UpUnCorr=csetBcJetSF->evaluate({"up_uncorrelated", "M", 4, abs((*selectedJets)[l]->eta_),(*selectedJets)[l]->pt_});
      LJetSF_UpUnCorr=csetLightJetSF->evaluate({"up_uncorrelated", "M", 0, abs((*selectedJets)[l]->eta_),(*selectedJets)[l]->pt_});
      BJetSF_DownCorr=csetBcJetSF->evaluate({"down_correlated", "M", 5, abs((*selectedJets)[l]->eta_),(*selectedJets)[l]->pt_});
      CJetSF_DownCorr=csetBcJetSF->evaluate({"down_correlated", "M", 4, abs((*selectedJets)[l]->eta_),(*selectedJets)[l]->pt_});
      LJetSF_DownCorr=csetLightJetSF->evaluate({"down_correlated", "M", 0, abs((*selectedJets)[l]->eta_),(*selectedJets)[l]->pt_});
      BJetSF_DownUnCorr=csetBcJetSF->evaluate({"down_uncorrelated", "M", 5, abs((*selectedJets)[l]->eta_),(*selectedJets)[l]->pt_});
      CJetSF_DownUnCorr=csetBcJetSF->evaluate({"down_uncorrelated", "M", 4, abs((*selectedJets)[l]->eta_),(*selectedJets)[l]->pt_});
      LJetSF_DownUnCorr=csetLightJetSF->evaluate({"down_uncorrelated", "M", 0, abs((*selectedJets)[l]->eta_),(*selectedJets)[l]->pt_});
//b-quark
      if( abs((*selectedJets)[l]->flavor_) == 5){
        if( (*selectedJets)[l]->btag_ ) {
          P_bjet_mc = P_bjet_mc * BJetEff;
          nominalWeights[getVecPos(sys,"bcTagSfCorr")] = nominalWeights[getVecPos(sys,"bcTagSfCorr")] * BJetEff * BJetSF;
          sysUpWeights[getVecPos(sys,"bcTagSfCorr")] = sysUpWeights[getVecPos(sys,"bcTagSfCorr")] * BJetEff * BJetSF_UpCorr;
          sysDownWeights[getVecPos(sys,"bcTagSfCorr")] = sysDownWeights[getVecPos(sys,"bcTagSfCorr")] * BJetEff * BJetSF_DownCorr;
          nominalWeights[getVecPos(sys,"LTagSfCorr")] = nominalWeights[getVecPos(sys,"LTagSfCorr")] * BJetEff * BJetSF;
          sysUpWeights[getVecPos(sys,"LTagSfCorr")] = sysUpWeights[getVecPos(sys,"LTagSfCorr")] * BJetEff * BJetSF;
          sysDownWeights[getVecPos(sys,"LTagSfCorr")] = sysDownWeights[getVecPos(sys,"LTagSfCorr")] * BJetEff * BJetSF;

          nominalWeights[getVecPos(sys,"bcTagSfUnCorr")] = nominalWeights[getVecPos(sys,"bcTagSfUnCorr")] * BJetEff * BJetSF;
          sysUpWeights[getVecPos(sys,"bcTagSfUnCorr")] = sysUpWeights[getVecPos(sys,"bcTagSfUnCorr")] * BJetEff * BJetSF_UpUnCorr;
          sysDownWeights[getVecPos(sys,"bcTagSfUnCorr")] = sysDownWeights[getVecPos(sys,"bcTagSfUnCorr")] * BJetEff * BJetSF_DownUnCorr;
          nominalWeights[getVecPos(sys,"LTagSfUnCorr")] = nominalWeights[getVecPos(sys,"LTagSfUnCorr")] * BJetEff * BJetSF;
          sysUpWeights[getVecPos(sys,"LTagSfUnCorr")] = sysUpWeights[getVecPos(sys,"LTagSfUnCorr")] * BJetEff * BJetSF;
          sysDownWeights[getVecPos(sys,"LTagSfUnCorr")] = sysDownWeights[getVecPos(sys,"LTagSfUnCorr")] * BJetEff * BJetSF;
        }
        if( !(*selectedJets)[l]->btag_ ) {
          P_bjet_mc = P_bjet_mc * (1 - BJetEff);
          nominalWeights[getVecPos(sys,"bcTagSfCorr")] = nominalWeights[getVecPos(sys,"bcTagSfCorr")]* (1- (BJetEff * BJetSF));
          sysUpWeights[getVecPos(sys,"bcTagSfCorr")] = sysUpWeights[getVecPos(sys,"bcTagSfCorr")]* (1- (BJetEff * BJetSF_UpCorr));
          sysDownWeights[getVecPos(sys,"bcTagSfCorr")] = sysDownWeights[getVecPos(sys,"bcTagSfCorr")]* (1- (BJetEff * BJetSF_DownCorr));
          nominalWeights[getVecPos(sys,"LTagSfCorr")] = nominalWeights[getVecPos(sys,"LTagSfCorr")]* (1- (BJetEff * BJetSF));
          sysUpWeights[getVecPos(sys,"LTagSfCorr")] = sysUpWeights[getVecPos(sys,"LTagSfCorr")]* (1- (BJetEff * BJetSF));
          sysDownWeights[getVecPos(sys,"LTagSfCorr")] = sysDownWeights[getVecPos(sys,"LTagSfCorr")]* (1- (BJetEff * BJetSF));

          nominalWeights[getVecPos(sys,"bcTagSfUnCorr")] = nominalWeights[getVecPos(sys,"bcTagSfUnCorr")]* (1- (BJetEff * BJetSF));
          sysUpWeights[getVecPos(sys,"bcTagSfUnCorr")] = sysUpWeights[getVecPos(sys,"bcTagSfUnCorr")]* (1- (BJetEff * BJetSF_UpUnCorr));
          sysDownWeights[getVecPos(sys,"bcTagSfUnCorr")] = sysDownWeights[getVecPos(sys,"bcTagSfUnCorr")]* (1- (BJetEff * BJetSF_DownUnCorr));
          nominalWeights[getVecPos(sys,"LTagSfUnCorr")] = nominalWeights[getVecPos(sys,"LTagSfUnCorr")]* (1- (BJetEff * BJetSF));
          sysUpWeights[getVecPos(sys,"LTagSfUnCorr")] = sysUpWeights[getVecPos(sys,"LTagSfUnCorr")]* (1- (BJetEff * BJetSF));
          sysDownWeights[getVecPos(sys,"LTagSfUnCorr")] = sysDownWeights[getVecPos(sys,"LTagSfUnCorr")]* (1- (BJetEff * BJetSF));
        }
      }
//c-quark
      if( abs((*selectedJets)[l]->flavor_) == 4){
        if( (*selectedJets)[l]->btag_) {
          P_bjet_mc = P_bjet_mc * CJetEff;
          nominalWeights[getVecPos(sys,"bcTagSfCorr")] = nominalWeights[getVecPos(sys,"bcTagSfCorr")] * CJetEff * CJetSF;
          sysUpWeights[getVecPos(sys,"bcTagSfCorr")] = sysUpWeights[getVecPos(sys,"bcTagSfCorr")] * CJetEff * CJetSF_UpCorr;
          sysDownWeights[getVecPos(sys,"bcTagSfCorr")] = sysDownWeights[getVecPos(sys,"bcTagSfCorr")] * CJetEff * CJetSF_DownCorr;
          nominalWeights[getVecPos(sys,"LTagSfCorr")] = nominalWeights[getVecPos(sys,"LTagSfCorr")] * CJetEff * CJetSF;
          sysUpWeights[getVecPos(sys,"LTagSfCorr")] = sysUpWeights[getVecPos(sys,"LTagSfCorr")] * CJetEff * CJetSF;
          sysDownWeights[getVecPos(sys,"LTagSfCorr")] = sysDownWeights[getVecPos(sys,"LTagSfCorr")] * CJetEff * CJetSF;

          nominalWeights[getVecPos(sys,"bcTagSfUnCorr")] = nominalWeights[getVecPos(sys,"bcTagSfUnCorr")] * CJetEff * CJetSF;
          sysUpWeights[getVecPos(sys,"bcTagSfUnCorr")] = sysUpWeights[getVecPos(sys,"bcTagSfUnCorr")] * CJetEff * CJetSF_UpUnCorr;
          sysDownWeights[getVecPos(sys,"bcTagSfUnCorr")] = sysDownWeights[getVecPos(sys,"bcTagSfUnCorr")] * CJetEff * CJetSF_DownUnCorr;
          nominalWeights[getVecPos(sys,"LTagSfUnCorr")] = nominalWeights[getVecPos(sys,"LTagSfUnCorr")] * CJetEff * CJetSF;
          sysUpWeights[getVecPos(sys,"LTagSfUnCorr")] = sysUpWeights[getVecPos(sys,"LTagSfUnCorr")] * CJetEff * CJetSF;
          sysDownWeights[getVecPos(sys,"LTagSfUnCorr")] = sysDownWeights[getVecPos(sys,"LTagSfUnCorr")] * CJetEff * CJetSF;
        }
        if( !(*selectedJets)[l]->btag_ ) {
          P_bjet_mc = P_bjet_mc * (1 - CJetEff);
          nominalWeights[getVecPos(sys,"bcTagSfCorr")] = nominalWeights[getVecPos(sys,"bcTagSfCorr")]* (1- (CJetEff * CJetSF));
          sysUpWeights[getVecPos(sys,"bcTagSfCorr")] = sysUpWeights[getVecPos(sys,"bcTagSfCorr")]* (1- (CJetEff * CJetSF_UpCorr));
          sysDownWeights[getVecPos(sys,"bcTagSfCorr")] = sysDownWeights[getVecPos(sys,"bcTagSfCorr")]* (1- (CJetEff * CJetSF_DownCorr));
          nominalWeights[getVecPos(sys,"LTagSfCorr")] = nominalWeights[getVecPos(sys,"LTagSfCorr")]* (1- (CJetEff * CJetSF));
          sysUpWeights[getVecPos(sys,"LTagSfCorr")] = sysUpWeights[getVecPos(sys,"LTagSfCorr")]* (1- (CJetEff * CJetSF));
          sysDownWeights[getVecPos(sys,"LTagSfCorr")] = sysDownWeights[getVecPos(sys,"LTagSfCorr")]* (1- (CJetEff * CJetSF));

          nominalWeights[getVecPos(sys,"bcTagSfUnCorr")] = nominalWeights[getVecPos(sys,"bcTagSfUnCorr")]* (1- (CJetEff * CJetSF));
          sysUpWeights[getVecPos(sys,"bcTagSfUnCorr")] = sysUpWeights[getVecPos(sys,"bcTagSfUnCorr")]* (1- (CJetEff * CJetSF_UpUnCorr));
          sysDownWeights[getVecPos(sys,"bcTagSfUnCorr")] = sysDownWeights[getVecPos(sys,"bcTagSfUnCorr")]* (1- (CJetEff * CJetSF_DownUnCorr));
          nominalWeights[getVecPos(sys,"LTagSfUnCorr")] = nominalWeights[getVecPos(sys,"LTagSfUnCorr")]* (1- (CJetEff * CJetSF));
          sysUpWeights[getVecPos(sys,"LTagSfUnCorr")] = sysUpWeights[getVecPos(sys,"LTagSfUnCorr")]* (1- (CJetEff * CJetSF));
          sysDownWeights[getVecPos(sys,"LTagSfUnCorr")] = sysDownWeights[getVecPos(sys,"LTagSfUnCorr")]* (1- (CJetEff * CJetSF));
        }
      }

//light-quark
      if( abs((*selectedJets)[l]->flavor_) != 4 && abs((*selectedJets)[l]->flavor_) != 5){
        if( (*selectedJets)[l]->btag_) {
          P_bjet_mc = P_bjet_mc * LJetEff;
          nominalWeights[getVecPos(sys,"bcTagSfCorr")] = nominalWeights[getVecPos(sys,"bcTagSfCorr")]* LJetEff * LJetSF;
          sysUpWeights[getVecPos(sys,"bcTagSfCorr")] = sysUpWeights[getVecPos(sys,"bcTagSfCorr")]* LJetEff * LJetSF;
          sysDownWeights[getVecPos(sys,"bcTagSfCorr")] = sysDownWeights[getVecPos(sys,"bcTagSfCorr")]* LJetEff * LJetSF;
          nominalWeights[getVecPos(sys,"LTagSfCorr")] = nominalWeights[getVecPos(sys,"LTagSfCorr")] * LJetEff * LJetSF;
          sysUpWeights[getVecPos(sys,"LTagSfCorr")] = sysUpWeights[getVecPos(sys,"LTagSfCorr")] * LJetEff * LJetSF_UpCorr;
          sysDownWeights[getVecPos(sys,"LTagSfCorr")] = sysDownWeights[getVecPos(sys,"LTagSfCorr")] * LJetEff * LJetSF_DownCorr;

          nominalWeights[getVecPos(sys,"bcTagSfUnCorr")] = nominalWeights[getVecPos(sys,"bcTagSfUnCorr")]* LJetEff * LJetSF;
          sysUpWeights[getVecPos(sys,"bcTagSfUnCorr")] = sysUpWeights[getVecPos(sys,"bcTagSfUnCorr")]* LJetEff * LJetSF;
          sysDownWeights[getVecPos(sys,"bcTagSfUnCorr")] = sysDownWeights[getVecPos(sys,"bcTagSfUnCorr")]* LJetEff * LJetSF;
          nominalWeights[getVecPos(sys,"LTagSfUnCorr")] = nominalWeights[getVecPos(sys,"LTagSfUnCorr")] * LJetEff * LJetSF;
          sysUpWeights[getVecPos(sys,"LTagSfUnCorr")] = sysUpWeights[getVecPos(sys,"LTagSfUnCorr")] * LJetEff * LJetSF_UpUnCorr;
          sysDownWeights[getVecPos(sys,"LTagSfUnCorr")] = sysDownWeights[getVecPos(sys,"LTagSfUnCorr")] * LJetEff * LJetSF_DownUnCorr;
        }
        if( !(*selectedJets)[l]->btag_ ) {
          P_bjet_mc = P_bjet_mc * (1 - LJetEff);
          nominalWeights[getVecPos(sys,"bcTagSfCorr")] = nominalWeights[getVecPos(sys,"bcTagSfCorr")]* (1- (LJetEff * LJetSF));
          sysUpWeights[getVecPos(sys,"bcTagSfCorr")] = sysUpWeights[getVecPos(sys,"bcTagSfCorr")]* (1- (LJetEff * LJetSF));
          sysDownWeights[getVecPos(sys,"bcTagSfCorr")] = sysDownWeights[getVecPos(sys,"bcTagSfCorr")]* (1- (LJetEff * LJetSF));
          nominalWeights[getVecPos(sys,"LTagSfCorr")] = nominalWeights[getVecPos(sys,"LTagSfCorr")]* (1- (LJetEff * LJetSF));
          sysUpWeights[getVecPos(sys,"LTagSfCorr")] = sysUpWeights[getVecPos(sys,"LTagSfCorr")]* (1- (LJetEff * LJetSF_UpCorr));
          sysDownWeights[getVecPos(sys,"LTagSfCorr")] = sysDownWeights[getVecPos(sys,"LTagSfCorr")]* (1- (LJetEff * LJetSF_DownCorr));

          nominalWeights[getVecPos(sys,"bcTagSfUnCorr")] = nominalWeights[getVecPos(sys,"bcTagSfUnCorr")]* (1- (LJetEff * LJetSF));
          sysUpWeights[getVecPos(sys,"bcTagSfUnCorr")] = sysUpWeights[getVecPos(sys,"bcTagSfUnCorr")]* (1- (LJetEff * LJetSF));
          sysDownWeights[getVecPos(sys,"bcTagSfUnCorr")] = sysDownWeights[getVecPos(sys,"bcTagSfUnCorr")]* (1- (LJetEff * LJetSF));
          nominalWeights[getVecPos(sys,"LTagSfUnCorr")] = nominalWeights[getVecPos(sys,"LTagSfUnCorr")]* (1- (LJetEff * LJetSF));
          sysUpWeights[getVecPos(sys,"LTagSfUnCorr")] = sysUpWeights[getVecPos(sys,"LTagSfUnCorr")]* (1- (LJetEff * LJetSF_UpUnCorr));
          sysDownWeights[getVecPos(sys,"LTagSfUnCorr")] = sysDownWeights[getVecPos(sys,"LTagSfUnCorr")]* (1- (LJetEff * LJetSF_DownUnCorr));
        }
      }
    }

    if (P_bjet_mc>0 && isfinite(nominalWeights[getVecPos(sys,"bcTagSfCorr")]) && isfinite(nominalWeights[getVecPos(sys,"LTagSfCorr")]) && isfinite(sysUpWeights[getVecPos(sys,"LTagSfCorr")]) && isfinite(sysDownWeights[getVecPos(sys,"LTagSfCorr")])){
      nominalWeights[getVecPos(sys,"bcTagSfCorr")] = nominalWeights[getVecPos(sys,"bcTagSfCorr")]/P_bjet_mc;
      sysUpWeights[getVecPos(sys,"bcTagSfCorr")] = sysUpWeights[getVecPos(sys,"bcTagSfCorr")]/P_bjet_mc;
      sysDownWeights[getVecPos(sys,"bcTagSfCorr")] = sysDownWeights[getVecPos(sys,"bcTagSfCorr")]/P_bjet_mc;
      nominalWeights[getVecPos(sys,"LTagSfCorr")] = nominalWeights[getVecPos(sys,"LTagSfCorr")]/P_bjet_mc;
      sysUpWeights[getVecPos(sys,"LTagSfCorr")] = sysUpWeights[getVecPos(sys,"LTagSfCorr")]/P_bjet_mc;
      sysDownWeights[getVecPos(sys,"LTagSfCorr")] = sysDownWeights[getVecPos(sys,"LTagSfCorr")]/P_bjet_mc;
  
      nominalWeights[getVecPos(sys,"bcTagSfUnCorr")] = nominalWeights[getVecPos(sys,"bcTagSfUnCorr")]/P_bjet_mc;
      sysUpWeights[getVecPos(sys,"bcTagSfUnCorr")] = sysUpWeights[getVecPos(sys,"bcTagSfUnCorr")]/P_bjet_mc;
      sysDownWeights[getVecPos(sys,"bcTagSfUnCorr")] = sysDownWeights[getVecPos(sys,"bcTagSfUnCorr")]/P_bjet_mc;
      nominalWeights[getVecPos(sys,"LTagSfUnCorr")] = nominalWeights[getVecPos(sys,"LTagSfUnCorr")]/P_bjet_mc;
      sysUpWeights[getVecPos(sys,"LTagSfUnCorr")] = sysUpWeights[getVecPos(sys,"LTagSfUnCorr")]/P_bjet_mc;
      sysDownWeights[getVecPos(sys,"LTagSfUnCorr")] = sysDownWeights[getVecPos(sys,"LTagSfUnCorr")]/P_bjet_mc;
    }
    else{
      cout<<"Warning: b-tagging eff or SF or infinit or b-jet prob in data is zero "<<endl;
      nominalWeights[getVecPos(sys,"bcTagSfCorr")] = 1;
      sysUpWeights[getVecPos(sys,"bcTagSfCorr")] = 1;
      sysDownWeights[getVecPos(sys,"bcTagSfCorr")] = 1;
      nominalWeights[getVecPos(sys,"LTagSfCorr")] = 1;
      sysUpWeights[getVecPos(sys,"LTagSfCorr")] = 1;
      sysDownWeights[getVecPos(sys,"LTagSfCorr")] = 1;

      nominalWeights[getVecPos(sys,"bcTagSfUnCorr")] = 1;
      sysUpWeights[getVecPos(sys,"bcTagSfUnCorr")] = 1;
      sysDownWeights[getVecPos(sys,"bcTagSfUnCorr")] = 1;
      nominalWeights[getVecPos(sys,"LTagSfUnCorr")] = 1;
      sysUpWeights[getVecPos(sys,"LTagSfUnCorr")] = 1;
      sysDownWeights[getVecPos(sys,"LTagSfUnCorr")] = 1;
    }      

//PU reweighting
    if (data == "mc" && year == "2016preVFP") {
      nominalWeights[getVecPos(sys,"pu")] = wPU.PU_2016preVFP(int(Pileup_nTrueInt),"nominal");
      sysUpWeights[getVecPos(sys,"pu")] = wPU.PU_2016preVFP(int(Pileup_nTrueInt),"up");
      sysDownWeights[getVecPos(sys,"pu")] = wPU.PU_2016preVFP(int(Pileup_nTrueInt),"down");
    }
    if (data == "mc" && year == "2016postVFP") {
      nominalWeights[getVecPos(sys,"pu")] = wPU.PU_2016postVFP(int(Pileup_nTrueInt),"nominal");
      sysUpWeights[getVecPos(sys,"pu")] = wPU.PU_2016postVFP(int(Pileup_nTrueInt),"up");
      sysDownWeights[getVecPos(sys,"pu")] = wPU.PU_2016postVFP(int(Pileup_nTrueInt),"down");
    }
    if (data == "mc" && year == "2017") {
      nominalWeights[getVecPos(sys,"pu")] = wPU.PU_2017(int(Pileup_nTrueInt),"nominal");
      sysUpWeights[getVecPos(sys,"pu")] = wPU.PU_2017(int(Pileup_nTrueInt),"up");
      sysDownWeights[getVecPos(sys,"pu")] = wPU.PU_2017(int(Pileup_nTrueInt),"down");
    }
    if (data == "mc" && year == "2018") {
      nominalWeights[getVecPos(sys,"pu")] = wPU.PU_2018(int(Pileup_nTrueInt),"nominal");
      sysUpWeights[getVecPos(sys,"pu")] = wPU.PU_2018(int(Pileup_nTrueInt),"up");
      sysDownWeights[getVecPos(sys,"pu")] = wPU.PU_2018(int(Pileup_nTrueInt),"down");
    }

    nominalWeights[getVecPos(sys,"prefiring")] = L1PreFiringWeight_Nom;
    sysUpWeights[getVecPos(sys,"prefiring")] = L1PreFiringWeight_Up;
    sysDownWeights[getVecPos(sys,"prefiring")] = L1PreFiringWeight_Dn;

}


void MyAnalysis::objectSelectionEnd(){
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

   for (int l=0;l<Z_P->size();l++){
   delete (*Z_P)[l];
   }
   Z_P->clear();
   Z_P->shrink_to_fit();
   delete Z_P;

   for (int l=0;l<Z_FP->size();l++){
   delete (*Z_FP)[l];
   }
   Z_FP->clear();
   Z_FP->shrink_to_fit();
   delete Z_FP;

//   cleanVec (selectedJetsJerUp);
//   cleanVec (selectedJetsJerDown);

   for (int l=0;l<JECsysUp->size();l++){
     for (int n=0;n<(*JECsysUp)[l].size();n++){
       delete (*JECsysUp)[l][n];
     }
   }
   for (int l=0;l<JECsysDown->size();l++){
     for (int n=0;n<(*JECsysDown)[l].size();n++){
       delete (*JECsysDown)[l][n];
     }
   }
   JECsysUp->clear();
   JECsysUp->shrink_to_fit();
   delete JECsysUp;
   JECsysDown->clear();
   JECsysDown->shrink_to_fit();
   delete JECsysDown;

}
///////////////////////////////////////////////////////////////////////////////////////////////////////////////

float MyAnalysis::conept_TTH(int l, int pdgid){
    if (abs(pdgid)==13){
      if(Muon_mediumId[l]>0 && Muon_mvaTTHUL[l] > 0.85) return Muon_pt[l];
      else return 0.90 * Muon_pt[l] * (1 + Muon_jetRelIso[l]);
    }
    else if (abs(pdgid)==11){
      if(Electron_mvaTTHUL[l] > 0.85) return Electron_pt[l];
      else return 0.90 * Electron_pt[l] * (1 + Electron_jetRelIso[l]);
    }
    else return 1000;
}

float MyAnalysis::jetBTagDeepFlav(int l){
  if(l<0) return -99;
  else return Jet_btagDeepFlavB[l];
}

bool MyAnalysis::ttH_idEmu_cuts_E3(int l){
    if (Electron_hoe[l]>=(0.10-0.00*(abs(Electron_eta[l]+Electron_deltaEtaSC[l])>1.479))) return false;
    if (Electron_eInvMinusPInv[l]<=-0.04) return false;
    if (Electron_sieie[l]>=(0.011+0.019*(abs(Electron_eta[l]+Electron_deltaEtaSC[l])>1.479))) return false;
    return true;
}

float MyAnalysis::smoothBFlav(float jetpt, float ptmin, float ptmax){
    double x = min(max(0.0, double (jetpt - ptmin))/(ptmax-ptmin), 1.0);
    return x*bTagCutWpL + (1-x)*bTagCutWpM;
}

bool MyAnalysis::looseMuon(int l){
  return (abs(Muon_eta[l]) < 2.4 && Muon_miniPFRelIso_all[l] < miniRelIso && Muon_sip3d[l] < sip3d && abs(Muon_dxy[l]) < dxy && abs(Muon_dz[l]) < dz && Muon_looseId[l]);
}


bool MyAnalysis::looseElectron(int l){
  return (abs(Electron_eta[l]) < 2.5 && Electron_miniPFRelIso_all[l] < miniRelIso && Electron_sip3d[l] < sip3d && abs(Electron_dxy[l]) < dxy && abs(Electron_dz[l]) < dz && Electron_lostHits[l]<=1 && Electron_mvaFall17V2noIso_WPL[l]);
}

bool MyAnalysis::fakeMuon(int l){
  return(jetBTagDeepFlav(Muon_jetIdx[l])<bTagCutWpM && (Muon_mvaTTHUL[l]>0.85 || (jetBTagDeepFlav(Muon_jetIdx[l]) < smoothBFlav(0.9*Muon_pt[l]*(1+Muon_jetRelIso[l]), 20, 45) && Muon_jetRelIso[l] < 0.50)));
}

bool MyAnalysis::fakeElectron(int l){
  return (jetBTagDeepFlav(Electron_jetIdx[l])<bTagCutWpM && ttH_idEmu_cuts_E3(l) && Electron_convVeto[l] && Electron_lostHits[l] == 0 && (Electron_mvaTTHUL[l]>0.90 || (Electron_mvaFall17V2noIso_WP90[l] && jetBTagDeepFlav(Electron_jetIdx[l]) < smoothBFlav(0.9*Electron_pt[l]*(1+Electron_jetRelIso[l]), 20, 45) && Electron_jetRelIso[l] < 1.0))); 
}

bool MyAnalysis::tightMuon(int l){
  return (Muon_mvaTTHUL[l]>0.85 && fakeMuon(l) && Muon_mediumId[l]>0);
}

bool MyAnalysis::tightElectron(int l){
  return (Electron_mvaTTHUL[l]>0.90 && fakeElectron(l));
}

bool MyAnalysis::tightCharge(int l, int pdgid){
  if(abs(pdgid) == 11){
    if (Electron_tightCharge[l]>=2) return true;
  }
  if(abs(pdgid) == 13){
    if (Muon_tightCharge[l]>=1) return true;
  }
  return false;
}

bool MyAnalysis::isMatched(int l, int pdgid, TString MC, bool ifChargedMatched){
  if (MC=="data") return true;
  if(abs(pdgid) == 11){
    if(!ifChargedMatched){
      if(Electron_genPartFlav[l]==1 || Electron_genPartFlav[l]==15) return true;
    }
    if(ifChargedMatched){
      if((Electron_genPartFlav[l]==1 || Electron_genPartFlav[l]==15) && (GenPart_pdgId[Electron_genPartIdx[l]]*Electron_pdgId[l]>0)) return true; 
    }
  }
  if(abs(pdgid) == 13){
    if(Muon_genPartFlav[l]==1 || Muon_genPartFlav[l]==15) return true;
  }
  return false;
}


