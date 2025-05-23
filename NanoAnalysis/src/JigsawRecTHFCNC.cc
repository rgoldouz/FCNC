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
/*
#include "RestFrames/RestFrames.hh"

using namespace RestFrames;

int main() {
    // Set verbosity
    RestFrames::SetVerbosity(Verbosity::Silent);

    // Create frames
    LabRecoFrame LAB("LAB");
    DecayRecoFrame T1("T1");
    DecayRecoFrame T2("T2");

    DecayRecoFrame W1("W1");
    VisibleRecoFrame l1("l1");
    InvisibleRecoFrame nu1("nu1");
    VisibleRecoFrame b("b");

    VisibleRecoFrame u("u");
    DecayRecoFrame WH("WH");
    VisibleRecoFrame j1("j1");
    VisibleRecoFrame j2("j2");

    DecayRecoFrame W2("W2");
    VisibleRecoFrame l2("l2");
    InvisibleRecoFrame nu2("nu2");

    // Build frame tree
    LAB.SetChildFrames({T1, T2});

    T1.SetChildFrames({W1, b});
    W1.SetChildFrames({l1, nu1});

    T2.SetChildFrames({u, WH, W2});
    WH.SetChildFrames({j1, j2});
    W2.SetChildFrames({l2, nu2});

    // Construct the topology
    RecoFrameTree eventTree(LAB);
    eventTree.Initialize();

    // Define visible and invisible groups
    CombinatoricGroup visGroup("VisGroup", {l1, l2, b, u, j1, j2});
    InvisibleGroup invGroup("InvGroup", {nu1, nu2});

    // Create the jigsaw analysis
    JigsawAnalysis jigsaw("ttbar_uh_analysis", eventTree, visGroup, invGroup);

    // Add jigsaw rules if needed
    jigsaw.Initialize();

    // Input example 4-vectors (replace with real event data)
    TLorentzVector lv_l1(30, 0, 40, 50);
    TLorentzVector lv_l2(-20, -10, 25, 35);
    TLorentzVector lv_b(25, 15, -10, 35);
    TLorentzVector lv_u(40, 0, -20, 45);
    TLorentzVector lv_j1(30, 20, 0, 36);
    TLorentzVector lv_j2(-10, 15, 10, 22);
    TLorentzVector met(15, -10, 0, 0); // px, py, pz=0, E=0 for MET input

    // Set the visible 4-vectors
    visGroup.SetLabFrameFourVectors({lv_l1, lv_l2, lv_b, lv_u, lv_j1, lv_j2});

    // Set MET
    invGroup.SetLabFrameThreeVector((lv_nu1 + lv_nu2).Vect()); // Here use your MET vector

    // Analyze event
    if (!jigsaw.AnalyzeEvent()) {
        std::cerr << "Failed to analyze event." << std::endl;
        return 1;
    }

    // Example: access reconstructed top mass from T1
    double mT1 = T1.GetMass();
    std::cout << "Reconstructed top mass (T1): " << mT1 << " GeV" << std::endl;

    return 0;
}
*/

