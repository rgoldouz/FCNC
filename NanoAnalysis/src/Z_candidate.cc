#include "Z_candidate.h"

Z_candidate::Z_candidate(UInt_t lep1_in, UInt_t lep2_in, float pt_in, float eta_in, float phi_in, float mass_in){
  pt_ = pt_in;
  eta_ = eta_in;
  phi_ = phi_in;
  mass_ = mass_in;
  lep1_ = lep1_in;
  lep2_ = lep2_in;
}

Z_candidate::~Z_candidate(){}


