#ifndef MY_Z_candidate
#define MY_Z_candidate

#include<cmath>
#include<string>
#include<iostream>
#include<vector>
#include<complex>
#include <TLorentzVector.h>

using namespace std;
//using namespace math;
class Z_candidate {
  
public:
  Z_candidate(UInt_t,UInt_t,float,float,float,float );
  virtual ~Z_candidate();
  float pt_;
  float eta_;
  float phi_;
  float mass_;
  UInt_t lep1_;
  UInt_t lep2_;

private:
  
};

#endif

