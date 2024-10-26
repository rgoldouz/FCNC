#ifndef MY_JigsawRecTHFCNC_h
#define MYJigsawRecTHFCNC_h
#include <iostream>
#include <cstring>
#include "RestFrames/RestFrames.hh"

using namespace RestFrames;
using namespace std;
class JigsawRecTHFCNC {
  public:
    JigsawRecTHFCNC();
    virtual ~JigsawRecTHFCNC();
    void Analyze(TLorentzVector l1, TLorentzVector l2, TLorentzVector b, TLorentzVector j1,TLorentzVector j2, TLorentzVector nu); 
  /////////////////////////////////////////////////////////////////////////////////////////
    //Reco Frames
    LabRecoFrame           *LAB;
    DecayRecoFrame         *TH;
    DecayRecoFrame         *T;
    DecayRecoFrame         *WT;
    VisibleRecoFrame       *BT;
    VisibleRecoFrame       *LT;
    InvisibleRecoFrame     *NUT;
    DecayRecoFrame         *H;
    DecayRecoFrame         *W1H;
    DecayRecoFrame         *W2H;
    VisibleRecoFrame       *L1H;
    InvisibleRecoFrame     *NU1H;
    VisibleRecoFrame       *U2H;
    VisibleRecoFrame       *D2H;
    InvisibleGroup         *INV;
    SetMassInvJigsaw *NuNuM_2W;
    SetRapidityInvJigsaw *NuNuR_2W;
    MinMassesSqInvJigsaw *MinMW_2W;
};

#endif





