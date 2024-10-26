#ifndef MY_objectSelection
#define MY_objectSelection

#pragma once
#include<cmath>
#include<string>
#include<iostream>
#include<vector>
#include<complex>
#include <TLorentzVector.h>
#include "MyAnalysis.h"

using namespace std;
//using namespace math;
class objectSelection{
  
public:
  objectSelection(MyAnalysis *evt, TString year);
  MyAnalysis *eI;
  virtual ~objectSelection();
  float bTagCutWpL;
  float bTagCutWpM;
  float jetBTagDeepFlav(int l);
  bool looseMuon(int l);
  bool looseElectron(int l);
  bool fakeMuon(int l);
  bool fakeElectron(int l);
  float smoothBFlav(float jetpt, float ptmin, float ptmax);
  bool ttH_idEmu_cuts_E3(int l);
  bool tightMuon(int l);
  bool tightElectron(int l);
  bool tightCharge(int l, int pdgid);
  bool isMatched(int l, int pdgid, TString MC, bool ifChargedMatched);
  float conept_TTH(int l, int pdgid);

private:
  double dxy =0.05;
  double dz =0.1;
  double miniRelIso=0.4 ;
  double sip3d=8;
  };

#endif

