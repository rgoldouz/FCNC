#include "JigsawRecTZFCNC.h"

using namespace RestFrames;
using namespace std;

JigsawRecTZFCNC::JigsawRecTZFCNC(){
  LAB=new LabRecoFrame("LAB","LAB");
  TZ=new DecayRecoFrame("TZ","tZ");
  T=new DecayRecoFrame("T","t");
  W=new DecayRecoFrame("W","W");
  B=new VisibleRecoFrame("B","b");
  L=new VisibleRecoFrame("L","#it{l}");
  NU=new InvisibleRecoFrame("NU","#nu");
  Z=new DecayRecoFrame("Z","Z");
  Lp=new VisibleRecoFrame("Lp","#it{l}^{+}");
  Lm=new VisibleRecoFrame("Lm","#it{l}^{-}");

  LAB->SetChildFrame(*TZ);
  TZ->AddChildFrame(*T);
  TZ->AddChildFrame(*Z);
  T->AddChildFrame(*B);
  T->AddChildFrame(*W);
  W->AddChildFrame(*L);
  W->AddChildFrame(*NU);
  Z->AddChildFrame(*Lp);
  Z->AddChildFrame(*Lm);

  LAB->InitializeTree(); 
  INV = new InvisibleGroup("INV","Invisible System");
  INV->AddFrame(*NU);

  // set the invisible system mass to zero
  InvMass = new SetMassInvJigsaw("InvMass","M_{#nu} = 0");
  INV->AddJigsaw(*InvMass);

  // set the invisible system rapidity to that of visible
  InvRapidity = new SetRapidityInvJigsaw("InvRapidity", "Invisible system rapidity Jigsaw");
  INV->AddJigsaw(*InvRapidity);
//  InvRapidity->AddVisibleFrames(TZ->GetListVisibleFrames());
  InvRapidity->AddVisibleFrame(*L);
  InvRapidity->AddVisibleFrame(*B);  
  LAB->InitializeAnalysis(); 
   ////////////// Jigsaw rules set-up /////////////////
}

void JigsawRecTZFCNC::Analyze(TLorentzVector l, TLorentzVector lp, TLorentzVector lm, TLorentzVector b, TLorentzVector nu){
  LAB->ClearEvent();                                   // clear the reco tree

  L->SetLabFrameFourVector(l);     // Set 4-vector
  Lp->SetLabFrameFourVector(lp);   // Set 4-vector
  Lm->SetLabFrameFourVector(lm);   // Set 4-vector
  B->SetLabFrameFourVector(b);     // Set 4-vector
  INV->SetLabFrameFourVector(nu);     // Set 4-vector
  LAB->AnalyzeEvent();                                 //analyze the event
}


JigsawRecTZFCNC::~JigsawRecTZFCNC(){
  delete LAB; 
  delete TZ;
  delete T;
  delete W;
  delete B;
  delete L;
  delete NU;
  delete Z;
  delete Lp;
  delete Lm;
  delete INV;
  delete InvMass;
  delete InvRapidity;
}



