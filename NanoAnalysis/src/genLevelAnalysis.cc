#include "genLevelAnalysis.h"
#include "Utils.h"


genLevelAnalysis::genLevelAnalysis(MyAnalysis *evt){
  eI = evt;
  GenHists.resize(vars.size());
  std::stringstream name;
  TH1EFT *h_test;
  for( auto it = vars.cbegin() ; it != vars.cend() ; ++it ){
    name<<it->first;
    h_test = new TH1EFT((name.str()).c_str(),(name.str()).c_str(),it->second.at(1), it->second.at(2), it->second.at(3));
    h_test->StatOverflows(kTRUE);
    h_test->Sumw2(kTRUE);
    GenHists[it->second.at(0)]=h_test;
    name.str("");
  }
}
std::vector<double> genLevelAnalysis::minGenDr(int myInd, std::vector<int> ignorePID){
    double myEta = eI->GenPart_eta[myInd];
    double myPhi = eI->GenPart_phi[myInd];
    int myPID = eI->GenPart_pdgId[myInd];

    double mindr = 999.0;
    double dr;
    int bestInd = -1;
    for( int oind = 0; oind < eI->nGenPart; oind++){
        if(oind == myInd) continue;
        if(eI->GenPart_status[oind] != 1) continue; // check if it's final state
        if(eI->GenPart_pt[oind] < 5)  continue;
        if(abs(eI->GenPart_pt[oind] - eI->GenPart_pt[myInd]) < 0.01 && (eI->GenPart_pdgId[oind] == eI->GenPart_pdgId[myInd]) && abs(eI->GenPart_eta[oind] - eI->GenPart_eta[myInd]) < 0.01)  continue; // skip if same particle
        int opid = abs(eI->GenPart_pdgId[oind]);
        if(opid == 12 || opid == 14 || opid == 16) continue;
        if(std::find(ignorePID.begin(),ignorePID.end(),opid) != ignorePID.end()) continue;
        dr = dR(myEta, myPhi, eI->GenPart_eta[oind], eI->GenPart_phi[oind]);
        if( mindr > dr ) {
            int genParentIdx = eI->GenPart_genPartIdxMother[oind];
            bool isDecay = false;
            while (genParentIdx>=myInd){
                if (genParentIdx==myInd) isDecay = true;
                genParentIdx = eI->GenPart_genPartIdxMother[genParentIdx];
            }
            if (isDecay) continue;

            mindr = dr;
            bestInd = oind;
        }
    }
    vector<double> v;
    v.push_back(mindr);
    v.push_back((double)bestInd);
    return v;
}

bool genLevelAnalysis::overlapRemoval(double Et_cut, double Eta_cut, double dR_cut, bool verbose){
    bool haveOverlap = false;
    vector<int> extraPIDIgnore={22};
    for(int mcInd=0; mcInd<eI->nGenPart; ++mcInd){
        if(eI->GenPart_pdgId[mcInd]==22){

            bool parentagePass=false;
            vector<double> minDR_Result = {-1.,0.};
            bool Overlaps = false;
            int maxPDGID = 0;
            if (eI->GenPart_pt[mcInd] >= Et_cut &&
                fabs(eI->GenPart_eta[mcInd]) <= Eta_cut){

                Int_t parentIdx = mcInd;
                int motherPDGID = 0;
                bool fromTopDecay = false;
                while (parentIdx != -1){
                    motherPDGID = std::abs(eI->GenPart_pdgId[parentIdx]);
                    maxPDGID = std::max(maxPDGID,motherPDGID);
                    parentIdx = eI->GenPart_genPartIdxMother[parentIdx];
                }

                bool parentagePass = maxPDGID < 37;
                if (parentagePass) {
                    minDR_Result= minGenDr(mcInd, extraPIDIgnore);
                    if(minDR_Result.at(0) > dR_cut) {
                        haveOverlap = true;
                        Overlaps = true;
                    }
                }
            }
            if (verbose){
                cout << " gen particle idx="<<mcInd << " pdgID="<<eI->GenPart_pdgId[mcInd] << " status="<<eI->GenPart_status[mcInd] << " pt="<<eI->GenPart_pt[mcInd] << " eta=" << eI->GenPart_eta[mcInd] << " parentage=" << (maxPDGID < 37) << " maxPDGID=" << maxPDGID << " minDR="<<minDR_Result.at(0) << " closestInd="<<minDR_Result.at(1) << " closestPDGID="<<eI->GenPart_pdgId[(int)minDR_Result.at(1)]<<" OVERLAPS="<<Overlaps<<endl;
            }
        }
    }
    return haveOverlap;
}

void genLevelAnalysis::fillGENHists(float weight, std::vector<string> wc_names){
  WCFit *eft_fit;
  if (wc_names.size()>0) eft_fit = new WCFit(wc_names.size(), wc_names, eI->nEFTfitCoefficients, eI->EFTfitCoefficients, weight);
  else eft_fit = new WCFit(wc_names.size(), wc_names,1, &weight, 1.0);
  
  TLorentzVector *top, *aTop, *Z, *H;
  std::vector<lepton_candidate*> *selectedLeptons;
  float massCandidate;
  top = new TLorentzVector();
  aTop = new TLorentzVector();
  Z = new TLorentzVector();
  H = new TLorentzVector();
  selectedLeptons = new std::vector<lepton_candidate*>();
  for (int l=0;l<eI->nGenPart;l++){
    if(eI->GenPart_pdgId[l]==6 && (eI->GenPart_statusFlags[l] & (1<<12)) == (1<<12)) top->SetPtEtaPhiM(eI->GenPart_pt[l],eI->GenPart_eta[l],eI->GenPart_phi[l],eI->GenPart_mass[l]);
    if(eI->GenPart_pdgId[l]==-6 && (eI->GenPart_statusFlags[l] & (1<<12)) == (1<<12)) aTop->SetPtEtaPhiM(eI->GenPart_pt[l],eI->GenPart_eta[l],eI->GenPart_phi[l],eI->GenPart_mass[l]);
    if(abs(eI->GenPart_pdgId[l])==25 && (eI->GenPart_statusFlags[l] & (1<<12)) == (1<<12)) H->SetPtEtaPhiM(eI->GenPart_pt[l],eI->GenPart_eta[l],eI->GenPart_phi[l],eI->GenPart_mass[l]);
    if(abs(eI->GenPart_pdgId[l])==23 && (eI->GenPart_statusFlags[l] & (1<<12)) == (1<<12)) Z->SetPtEtaPhiM(eI->GenPart_pt[l],eI->GenPart_eta[l],eI->GenPart_phi[l],eI->GenPart_mass[l]);
    if((abs(eI->GenPart_pdgId[l])==11 || abs(eI->GenPart_pdgId[l])==13 || abs(eI->GenPart_pdgId[l])==15) &&  (eI->GenPart_statusFlags[l] & (1<<13)) == (1<<13)){
      if(eI->GenPart_pt[l]>10 && abs(eI->GenPart_eta[l])<2.5) {
        int x=eI->GenPart_pdgId[l];
        if(abs(x) ==11) selectedLeptons->push_back(new lepton_candidate(eI->GenPart_pt[l],eI->GenPart_eta[l],eI->GenPart_phi[l],eI->GenPart_pdgId[l],l,1, eI->GenPart_pdgId[l]));
        if(abs(x) ==13) selectedLeptons->push_back(new lepton_candidate(eI->GenPart_pt[l],eI->GenPart_eta[l],eI->GenPart_phi[l],eI->GenPart_pdgId[l],l,10, eI->GenPart_pdgId[l]));
        if(abs(x) ==15) selectedLeptons->push_back(new lepton_candidate(eI->GenPart_pt[l],eI->GenPart_eta[l],eI->GenPart_phi[l],eI->GenPart_pdgId[l],l,100, eI->GenPart_pdgId[l]));
      }
    }
  }
  sort(selectedLeptons->begin(),selectedLeptons->end(), ComparePtLep);
  if(selectedLeptons->size()>1){
    massCandidate=-1;
    for (int i=0;i<selectedLeptons->size();i++){
      for (int j=i+1;j<selectedLeptons->size();j++){
        if(selectedLeptons->at(i)->lep_ == selectedLeptons->at(j)->lep_ &&
           selectedLeptons->at(i)->charge_ != selectedLeptons->at(j)->charge_ &&
          (selectedLeptons->at(i)->p4_ + selectedLeptons->at(j)->p4_).M()>massCandidate) massCandidate=(selectedLeptons->at(i)->p4_ + selectedLeptons->at(j)->p4_).M();
      }
    }
  }
  GenHists[vInd(vars,"eventsAll")]->Fill(0.5,weight,*eft_fit);
  if(top->Pt()>0) GenHists[vInd(vars,"topPtLHE")]->Fill(top->Pt(),weight,*eft_fit);
  if(top->Pt()>0) GenHists[vInd(vars,"topEtaLHE")]->Fill(top->Eta(),weight,*eft_fit);
  if(aTop->Pt()>0) GenHists[vInd(vars,"aTopPtLHE")]->Fill(aTop->Pt(),weight,*eft_fit);
  if(aTop->Pt()>0) GenHists[vInd(vars,"aTopEtaLHE")]->Fill(aTop->Eta(),weight,*eft_fit);
  if(selectedLeptons->size()>0) GenHists[vInd(vars,"leadingLeptonPtMc")]->Fill((*selectedLeptons)[0]->pt_,weight,*eft_fit);
  if(selectedLeptons->size()>0) GenHists[vInd(vars,"leadingLeptonEtaMc")]->Fill((*selectedLeptons)[0]->eta_,weight,*eft_fit);
  if(massCandidate>0) GenHists[vInd(vars,"massLlNotFromTopMc")]->Fill(massCandidate,weight,*eft_fit);
  if(Z->Pt()>0) GenHists[vInd(vars,"ZPtMc")]->Fill(Z->Pt(),weight,*eft_fit);
  if(Z->Pt()>0) GenHists[vInd(vars,"ZEtaMc")]->Fill(Z->Eta(),weight,*eft_fit);
  if(H->Pt()>0) GenHists[vInd(vars,"HPtMc")]->Fill(H->Pt(),weight,*eft_fit);
  if(H->Pt()>0) GenHists[vInd(vars,"HEtaMc")]->Fill(H->Eta(),weight,*eft_fit);
  delete top;
  delete aTop;
  delete Z;
  delete H;
  for (int l=0;l<selectedLeptons->size();l++){
    delete (*selectedLeptons)[l];
  }
  selectedLeptons->clear();
  selectedLeptons->shrink_to_fit();
  delete eft_fit;
}

void genLevelAnalysis::writeGENHists(){
//  cout<<"The following Gen level distributions are written on the output file"<<endl;
  for (int i=0;i<GenHists.size();++i){
//    cout<<i<<":"<<GenHists[i]->GetName()<<endl;
    GenHists[i]->Write("",TObject::kOverwrite);
  }
}

genLevelAnalysis::~genLevelAnalysis(){
  for (int n=0;n<GenHists.size();++n){
    delete GenHists[n];
  }
  GenHists.clear();
  GenHists.shrink_to_fit();
}
