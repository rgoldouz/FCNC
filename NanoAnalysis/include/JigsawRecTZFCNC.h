#ifndef MY_JigsawRecTZFCNC_h
#define MYJigsawRecTZFCNC_h
#include <iostream>
#include <cstring>
#include "RestFrames/RestFrames.hh"

using namespace RestFrames;
using namespace std;
class JigsawRecTZFCNC {
  public:
    JigsawRecTZFCNC();
    virtual ~JigsawRecTZFCNC();
    void Analyze(TLorentzVector l, TLorentzVector lp, TLorentzVector lm, TLorentzVector b, TLorentzVector nu); 
  /////////////////////////////////////////////////////////////////////////////////////////
    //Reco Frames
    LabRecoFrame           *LAB;
    DecayRecoFrame         *TZ;
    DecayRecoFrame         *T;
    DecayRecoFrame         *W;
    VisibleRecoFrame       *B;
    VisibleRecoFrame       *L;
    InvisibleRecoFrame     *NU;
    DecayRecoFrame         *Z;
    VisibleRecoFrame       *Lp;
    VisibleRecoFrame       *Lm;
    InvisibleGroup         *INV;
    SetMassInvJigsaw       *InvMass;
    SetRapidityInvJigsaw   *InvRapidity;
};

#endif





