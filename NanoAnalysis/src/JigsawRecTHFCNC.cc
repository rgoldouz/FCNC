#include "JigsawRecTHFCNC.h"

using namespace RestFrames;
using namespace std;

JigsawRecTHFCNC::JigsawRecTHFCNC(){
  LAB=new LabRecoFrame("LAB","LAB");
  TH=new DecayRecoFrame("TH","tH");
  T=new DecayRecoFrame("T","t");
  WT=new DecayRecoFrame("WT","Wt");
  BT=new VisibleRecoFrame("BT","bt");
  LT=new VisibleRecoFrame("LT","#it{l}t");
  NUT=new InvisibleRecoFrame("NUT","#nu t");
  H=new DecayRecoFrame("H","H");
  W1H=new DecayRecoFrame("W1H","W1H");
  W2H=new DecayRecoFrame("W2H","W2H");
  L1H=new VisibleRecoFrame("L1H","#it{l}1h");
  NU1H=new InvisibleRecoFrame("NU1H","#nu 1h");
  U2H=new VisibleRecoFrame("U2H","u2h");
  D2H=new VisibleRecoFrame("D2H","d2h");


  LAB->SetChildFrame(*TH);
  TH->AddChildFrame(*T);
  TH->AddChildFrame(*H);
  T->AddChildFrame(*BT);
  T->AddChildFrame(*WT);
  WT->AddChildFrame(*LT);
  WT->AddChildFrame(*NUT);
  H->AddChildFrame(*W1H);
  H->AddChildFrame(*W2H);
  W1H->AddChildFrame(*L1H);
  W1H->AddChildFrame(*NU1H);
  W2H->AddChildFrame(*U2H);
  W2H->AddChildFrame(*D2H);

  LAB->InitializeTree(); 
  INV = new InvisibleGroup("INV","Invisible System");
  INV->AddFrame(*NUT);
  INV->AddFrame(*NU1H);

  NuNuM_2W = new SetMassInvJigsaw("NuNuM_2W", "M_{#nu#nu} ~ m_{#it{l}#it{l}}");
  INV->AddJigsaw(*NuNuM_2W);
  NuNuR_2W = new SetRapidityInvJigsaw("NuNuR_2W", "#eta_{#nu#nu} = #eta_{#it{l}#it{l}}");
  INV->AddJigsaw(*NuNuR_2W);
  NuNuR_2W->AddVisibleFrames(*LT+*L1H);
  MinMW_2W = new MinMassesSqInvJigsaw("MinMW_2W","min #Sigma M_{W}^{ 2}", 2);
  INV->AddJigsaw(*MinMW_2W);
  MinMW_2W->AddVisibleFrame(*LT, 0);   MinMW_2W->AddInvisibleFrame(*NUT, 0);
  MinMW_2W->AddVisibleFrame(*L1H, 1);   MinMW_2W->AddInvisibleFrame(*NU1H, 1);

  LAB->InitializeAnalysis(); 
   ////////////// Jigsaw rules set-up /////////////////
}

void JigsawRecTHFCNC::Analyze(TLorentzVector l1, TLorentzVector l2, TLorentzVector b, TLorentzVector j1,TLorentzVector j2, TLorentzVector nu){
  LAB->ClearEvent();                                   // clear the reco tree

  LT->SetLabFrameFourVector(l1);     // Set 4-vector
  L1H->SetLabFrameFourVector(l2);   // Set 4-vector
  BT->SetLabFrameFourVector(b);     // Set 4-vector
  INV->SetLabFrameFourVector(nu);     // Set 4-vector
  U2H->SetLabFrameFourVector(j1);     // Set 4-vector
  D2H->SetLabFrameFourVector(j2);     // Set 4-vector
  LAB->AnalyzeEvent();                                 //analyze the event
}


JigsawRecTHFCNC::~JigsawRecTHFCNC(){
  delete LAB; 
  delete TH;
  delete T;
  delete WT;
  delete BT;
  delete LT;
  delete NUT;
  delete H;
  delete W1H;
  delete W2H;
  delete NU1H;
  delete L1H;
  delete D2H;
  delete U2H;
  delete INV;
  delete NuNuM_2W;
  delete NuNuR_2W;
  delete MinMW_2W;
}



