#pragma once
#ifndef MY_genLevelAnalysis
#define MY_genLevelAnalysis

#include<cmath>
#include<string>
#include<iostream>
#include<vector>
#include<complex>
#include <TLorentzVector.h>
#include "MyAnalysis.h"
#include "WCPoint.h"
#include "WCFit.h"
#include <map>


using namespace std;
//using namespace math;
class genLevelAnalysis{
  
public:
  genLevelAnalysis(MyAnalysis *evt);
  MyAnalysis *eI;
  virtual ~genLevelAnalysis();
  bool overlapRemoval(double Et_cut, double Eta_cut, double dR_cut, bool verbose);
  std::vector<double> minGenDr(int myInd, std::vector<int> ignorePID = std::vector<int>());
  void fillLHEHists(float weight, std::vector<string> wc_names);
  void fillGENHists(float weight, std::vector<string> wc_names);
  void writeGENHists();
  const std::map<TString, std::vector<float>> vars =
  {
    {"topPtLHE",                        {0,      25,   0,  500}},
    {"aTopPtLHE",                       {1,      25,   0,  500}},
    {"topEtaLHE",                       {2,      20,   -3,  3}},
    {"aTopEtaLHE",                      {3,      20,   -3,  3}},
    {"leadingLeptonPtMc",               {4,      20,   0,  400}},
    {"leadingLeptonEtaMc",              {5,      20,   -3,  3}},
    {"massLlNotFromTopMc",              {6,      40,   0,  400}},
    {"ZPtMc",                           {7,      20,   0,  400}},
    {"ZEtaMc",                          {8,      20,   -3,  3}},
    {"HPtMc",                           {9,      20,   0,  400}},
    {"HEtaMc",                          {10,      20,   -3,  3}},
    {"eventsAll",                       {11,      1,   0,  1}},
  };
  vector<TH1EFT*> GenHists;
  std::vector<string> wc_names_lst={};
private:
  };

#endif

