#include "MyAnalysis.h"
#include "TH1EFT.h"

   double binsPtH[]={0, 10, 20, 30, 50, 80, 120, 170, 250, 350, 500,750,1000};
   double binsPtM[]={0, 10, 20, 30, 50, 80, 110, 150, 200, 250, 300, 400, 500};
   double binsPtL[]={0, 10, 20, 30, 50, 80, 110, 150, 200, 250, 300};
   double binsEta[]={-5,-4,-3,-2.75,-2.5,-2.25,-2,-1.75,-1.5,-1.25,-1,-0.75,-0.5,-0.25,0,0.25,0.5,0.75,1,1.25,1.5,1.75,2,2.25,2.5,2.75,3,4,5};
   double binsPhi[]={-4,-3,-2,-1,0,1,2,3,4};
   double binsMVA[]={0,0.1,0.2,0.3,0.4,0.5,0.6,0.7,0.8,0.9,1,1.1,1.2,1.3,1.4,1.5,1.6,1.7,1.8,1.9,2,2.5,3,3.5,4,4.5,5,10,15,20,25,30,35,40,45,50};
   double binsDr[]={0,0.5,1,1.5,2,2.5,3,3.5,4,4.5,5,5.5,6,6.5,7};
   double binsMz[]={70.0, 71.0256, 72.0513, 73.0769, 74.1026, 75.1282, 76.1538, 77.1795, 78.2051, 79.2308,80.2564, 81.2821, 82.3077, 83.3333, 84.3590, 85.3846, 86.4103, 87.4359, 88.4615, 89.4872,90.5128, 91.5385, 92.5641, 93.5897, 94.6154, 95.6410, 96.6667, 97.6923, 98.7179, 99.7436,100.7692, 101.7949, 102.8205, 103.8462, 104.8718, 105.8974, 106.9231, 107.9487, 108.9744, 110.0};
   double binsnJets[]={0,1,2,3,4,5,6,7,8};
   double binsnVtx[]={0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15,16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60};

   const std::map<TString, std::tuple<int, int, const double*>> MyAnalysis::vars =
   {
    {"lep1Pt",                         {0,       sizeof(binsPtH)/sizeof(double) - 1, binsPtH}},
    {"lep1Eta",                        {1,       sizeof(binsEta)/sizeof(double) - 1, binsEta}},
    {"lep1Phi",                        {2,       sizeof(binsPhi)/sizeof(double) - 1, binsPhi}},
    {"lep2Pt",                         {3,       sizeof(binsPtM)/sizeof(double) - 1, binsPtM}},
    {"lep2Eta",                        {4,       sizeof(binsEta)/sizeof(double) - 1, binsEta}},
    {"lep2Phi",                        {5,       sizeof(binsPhi)/sizeof(double) - 1, binsPhi}},
    {"llM",                            {6,       sizeof(binsPtM)/sizeof(double) - 1, binsPtM }},
    {"llPt",                           {7,       sizeof(binsPtM)/sizeof(double) - 1, binsPtM }},
    {"llDr",                           {8,       sizeof(binsDr)/sizeof(double) - 1, binsDr}},
    {"llDphi",                         {9,       sizeof(binsDr)/sizeof(double) - 1, binsDr}},
    {"jet1Pt",                         {10,      sizeof(binsPtL)/sizeof(double) - 1, binsPtL }},
    {"jet1Eta",                        {11,      sizeof(binsEta)/sizeof(double) - 1, binsEta}},
    {"jet1Phi",                        {12,      sizeof(binsPhi)/sizeof(double) - 1, binsPhi}},
    {"njet",                           {13,      sizeof(binsnJets)/sizeof(double) - 1, binsnJets}},
    {"nbjet",                          {14,      sizeof(binsnJets)/sizeof(double) - 1, binsnJets}},
    {"Met",                            {15,      sizeof(binsPtL)/sizeof(double) - 1, binsPtL }},
    {"MetPhi",                         {16,      sizeof(binsPhi)/sizeof(double) - 1, binsPhi}},
    {"nVtx",                           {17,      sizeof(binsnVtx)/sizeof(double) - 1, binsnVtx}},
    {"llMZw",                          {18,      sizeof(binsMz)/sizeof(double) - 1, binsMz}},
    {"MVATU",                          {19,      sizeof(binsMVA)/sizeof(double) - 1, binsMVA}},
    {"MVATC",                          {20,      sizeof(binsMVA)/sizeof(double) - 1, binsMVA}},
    {"lep3Pt",                         {21,      sizeof(binsPtL)/sizeof(double) - 1, binsPtL}},
    {"lep3Eta",                        {22,      sizeof(binsEta)/sizeof(double) - 1, binsEta}},
    {"bJetPt",                         {23,      sizeof(binsPtL)/sizeof(double) - 1, binsPtL }},
    {"bJetEta",                        {24,      sizeof(binsEta)/sizeof(double) - 1, binsEta}},
    {"tH_topMass",                     {25,      sizeof(binsPtH)/sizeof(double) - 1, binsPtH}},
    {"tH_HMass",                       {26,      sizeof(binsPtH)/sizeof(double) - 1, binsPtH}},
    {"tH_WtopMass",                    {27,      sizeof(binsPtH)/sizeof(double) - 1, binsPtH}},
    {"tH_W1HMass",                     {28,      sizeof(binsPtH)/sizeof(double) - 1, binsPtH}},
    {"tH_W2HMass",                     {29,      sizeof(binsPtH)/sizeof(double) - 1, binsPtH}},
    {"tH_HPt",                         {30,      sizeof(binsPtH)/sizeof(double) - 1, binsPtH}},
    {"tH_HEta",                        {31,      sizeof(binsEta)/sizeof(double) - 1, binsEta}},
    {"tH_topPt",                       {32,      sizeof(binsPtH)/sizeof(double) - 1, binsPtH}},
    {"tH_topEta",                      {33,      sizeof(binsEta)/sizeof(double) - 1, binsEta}},
    {"tH_drWtopB",                     {34,      sizeof(binsDr)/sizeof(double) - 1, binsDr}},
    {"tH_drW1HW2H",                    {35,      sizeof(binsDr)/sizeof(double) - 1, binsDr}},
    {"tZ_topMass",                     {36,      sizeof(binsPtH)/sizeof(double) - 1, binsPtH}},
    {"tZ_ZMass",                       {37,      sizeof(binsPtH)/sizeof(double) - 1, binsPtH}},
    {"tZ_WtopMass",                    {38,      sizeof(binsPtH)/sizeof(double) - 1, binsPtH}},
    {"tZ_ZPt",                         {39,      sizeof(binsPtH)/sizeof(double) - 1, binsPtH}},
    {"tZ_ZEta",                        {40,      sizeof(binsEta)/sizeof(double) - 1, binsEta}},
    {"tZ_topPt",                       {41,      sizeof(binsPtH)/sizeof(double) - 1, binsPtH}},
    {"tZ_topEta",                      {42,      sizeof(binsEta)/sizeof(double) - 1, binsEta}},
   };

      const std::map<TString, std::tuple<int, int, const double*>> MyAnalysis::varsFA =
   {
    {"lep1Pt",                         {0,       sizeof(binsPtH)/sizeof(double) - 1, binsPtH}},
    {"lep1Eta",                        {1,       sizeof(binsEta)/sizeof(double) - 1, binsEta}},
    {"lep1Phi",                        {2,       sizeof(binsPhi)/sizeof(double) - 1, binsPhi}},
    {"lep2Pt",                         {3,       sizeof(binsPtM)/sizeof(double) - 1, binsPtM}},
    {"lep2Eta",                        {4,       sizeof(binsEta)/sizeof(double) - 1, binsEta}},
    {"lep2Phi",                        {5,       sizeof(binsPhi)/sizeof(double) - 1, binsPhi}},
    {"llM",                            {6,       sizeof(binsPtM)/sizeof(double) - 1, binsPtM }},
    {"llPt",                           {7,       sizeof(binsPtM)/sizeof(double) - 1, binsPtM }},
    {"llDr",                           {8,       sizeof(binsDr)/sizeof(double) - 1, binsDr}},
    {"llDphi",                         {9,       sizeof(binsDr)/sizeof(double) - 1, binsDr}},
    {"jet1Pt",                         {10,      sizeof(binsPtL)/sizeof(double) - 1, binsPtL }},
    {"jet1Eta",                        {11,      sizeof(binsEta)/sizeof(double) - 1, binsEta}},
    {"jet1Phi",                        {12,      sizeof(binsPhi)/sizeof(double) - 1, binsPhi}},
    {"njet",                           {13,      sizeof(binsnJets)/sizeof(double) - 1, binsnJets}},
    {"nbjet",                          {14,      sizeof(binsnJets)/sizeof(double) - 1, binsnJets}},
    {"Met",                            {15,      sizeof(binsPtL)/sizeof(double) - 1, binsPtL }},
    {"MetPhi",                         {16,      sizeof(binsPhi)/sizeof(double) - 1, binsPhi}},
    {"nVtx",                           {17,      sizeof(binsnVtx)/sizeof(double) - 1, binsnVtx}},
    {"llMZw",                          {18,      sizeof(binsMz)/sizeof(double) - 1, binsMz}},
    {"MVATU",                          {19,      sizeof(binsMVA)/sizeof(double) - 1, binsMVA}},
    {"MVATC",                          {20,      sizeof(binsMVA)/sizeof(double) - 1, binsMVA}},
    {"lep3Pt",                         {21,      sizeof(binsPtL)/sizeof(double) - 1, binsPtL}},
    {"lep3Eta",                        {22,      sizeof(binsEta)/sizeof(double) - 1, binsEta}},
    {"bJetPt",                         {23,      sizeof(binsPtL)/sizeof(double) - 1, binsPtL }},
    {"bJetEta",                        {24,      sizeof(binsEta)/sizeof(double) - 1, binsEta}},
    {"tH_topMass",                     {25,      sizeof(binsPtH)/sizeof(double) - 1, binsPtH}},
    {"tH_HMass",                       {26,      sizeof(binsPtH)/sizeof(double) - 1, binsPtH}},
    {"tH_WtopMass",                    {27,      sizeof(binsPtH)/sizeof(double) - 1, binsPtH}},
    {"tH_W1HMass",                     {28,      sizeof(binsPtH)/sizeof(double) - 1, binsPtH}},
    {"tH_W2HMass",                     {29,      sizeof(binsPtH)/sizeof(double) - 1, binsPtH}},
    {"tH_HPt",                         {30,      sizeof(binsPtH)/sizeof(double) - 1, binsPtH}},
    {"tH_HEta",                        {31,      sizeof(binsEta)/sizeof(double) - 1, binsEta}},
    {"tH_topPt",                       {32,      sizeof(binsPtH)/sizeof(double) - 1, binsPtH}},
    {"tH_topEta",                      {33,      sizeof(binsEta)/sizeof(double) - 1, binsEta}},
    {"tH_drWtopB",                     {34,      sizeof(binsDr)/sizeof(double) - 1, binsDr}},
    {"tH_drW1HW2H",                    {35,      sizeof(binsDr)/sizeof(double) - 1, binsDr}},
    {"tZ_topMass",                     {36,      sizeof(binsPtH)/sizeof(double) - 1, binsPtH}},
    {"tZ_ZMass",                       {37,      sizeof(binsPtH)/sizeof(double) - 1, binsPtH}},
    {"tZ_WtopMass",                    {38,      sizeof(binsPtH)/sizeof(double) - 1, binsPtH}},
    {"tZ_ZPt",                         {39,      sizeof(binsPtH)/sizeof(double) - 1, binsPtH}},
    {"tZ_ZEta",                        {40,      sizeof(binsEta)/sizeof(double) - 1, binsEta}},
    {"tZ_topPt",                       {41,      sizeof(binsPtH)/sizeof(double) - 1, binsPtH}},
    {"tZ_topEta",                      {42,      sizeof(binsEta)/sizeof(double) - 1, binsEta}},
   };

   const std::map<TString, std::tuple<int, int, const double*>> MyAnalysis::varsFullSys =
   {
    {"MVATU",                          {0,      sizeof(binsMVA)/sizeof(double) - 1, binsMVA}},
    {"MVATC",                          {1,      sizeof(binsMVA)/sizeof(double) - 1, binsMVA}},
   };

void MyAnalysis::initiateHists(TString data,string year, bool ifSys){
  cout<<"Start initiating"<<endl;
  //Hists is used to save nominal histograms in signal regions
  Hists.resize(channels.size());
  for (int i=0;i<channels.size();++i){
    Hists[i].resize(regions.size());
    for (int k=0;k<regions.size();++k){
      Hists[i][k].resize(vars.size());
    }
  }
  std::stringstream name;
  for (int i=0;i<channels.size();++i){
    for (int k=0;k<regions.size();++k){
      for( auto it = vars.cbegin() ; it != vars.cend() ; ++it ){
        name<<channels[i]<<"_"<<regions[k]<<"_"<<it->first;
        h_test = new TH1EFT((name.str()).c_str(),(name.str()).c_str(),std::get<1>(it->second), std::get<2>(it->second));
        h_test->SetDirectory(0);
        h_test->StatOverflows(kTRUE);
        h_test->Sumw2(kTRUE);
        Hists[i][k][std::get<0>(it->second)] = h_test;
        name.str("");
      }
    }
  }
  //HistsFA is used to save nominal histograms in fake control regions
  HistsFA.resize(channelsFA.size());
  for (int i=0;i<channelsFA.size();++i){
    HistsFA[i].resize(regions.size());
    for (int k=0;k<regions.size();++k){
      HistsFA[i][k].resize(varsFA.size());
    }
  }
  for (int i=0;i<channelsFA.size();++i){
    for (int k=0;k<regions.size();++k){
      for( auto it = varsFA.cbegin() ; it != varsFA.cend() ; ++it ){
        name<<channelsFA[i]<<"_"<<regions[k]<<"_"<<it->first;
        h_test = new TH1EFT((name.str()).c_str(),(name.str()).c_str(),std::get<1>(it->second), std::get<2>(it->second));
        h_test->SetDirectory(0);
        h_test->StatOverflows(kTRUE);
        h_test->Sumw2(kTRUE);
        HistsFA[i][k][std::get<0>(it->second)] = h_test;
        name.str("");
      }
    }
  }

  //HistsFAUp/Down is used to save systematic uncertainties related to the fake rate estimation	  
  HistsFAUp.resize(channelsFA.size());
  for (int i=0;i<channelsFA.size();++i){
    HistsFAUp[i].resize(regions.size());
    for (int k=0;k<regions.size();++k){
      HistsFAUp[i][k].resize(varsFullSys.size());
      for (int n=0;n<varsFullSys.size();++n){
        HistsFAUp[i][k][n].resize(sysFA.size());
      }
    }
  }
  HistsFADown.resize(channelsFA.size());
  for (int i=0;i<channelsFA.size();++i){
    HistsFADown[i].resize(regions.size());
    for (int k=0;k<regions.size();++k){
      HistsFADown[i][k].resize(varsFullSys.size());
      for (int n=0;n<varsFullSys.size();++n){
        HistsFADown[i][k][n].resize(sysFA.size());
      }
    }
  }
  for (int i=0;i<channelsFA.size();++i){
    for (int k=0;k<regions.size();++k){
      for( auto it = varsFullSys.cbegin() ; it != varsFullSys.cend() ; ++it ){
        for (int n=0;n<sysFA.size();++n){
          name<<channelsFA[i]<<"_"<<regions[k]<<"_"<<it->first<<"_"<<sysFA[n]<<"_Up";
          h_test = new TH1EFT((name.str()).c_str(),(name.str()).c_str(),std::get<1>(it->second), std::get<2>(it->second));
          h_test->SetDirectory(0);
          h_test->StatOverflows(kTRUE);
          HistsFAUp[i][k][std::get<0>(it->second)][n] = h_test;
          name.str("");
          name<<channelsFA[i]<<"_"<<regions[k]<<"_"<<it->first<<"_"<<sysFA[n]<<"_Down";
          h_test = new TH1EFT((name.str()).c_str(),(name.str()).c_str(),std::get<1>(it->second), std::get<2>(it->second));
          h_test->SetDirectory(0);
          h_test->StatOverflows(kTRUE);
          HistsFADown[i][k][std::get<0>(it->second)][n] = h_test;
          name.str("");
        }
      }
    }
  }

  if(data == "mc" && ifSys){
    //HistsSysCompactUp/Down is used to save TH1EFT histograms including systematics that change event weights. Each constant is used to save the weight of events in a new scenario. So instead of keeping n histogram for n systematic variation, we save one histogram with different weights. 
    HistsSysCompactUp.resize(channelsSys.size());
    for (int i=0;i<channelsSys.size();++i){
      HistsSysCompactUp[i].resize(regions.size());
      for (int k=0;k<regions.size();++k){
        HistsSysCompactUp[i][k].resize(vars.size());
      }
    }
    HistsSysCompactDown.resize(channelsSys.size());
    for (int i=0;i<channelsSys.size();++i){
      HistsSysCompactDown[i].resize(regions.size());
      for (int k=0;k<regions.size();++k){
        HistsSysCompactDown[i][k].resize(vars.size());
      }
    }
    for (int i=0;i<channelsSys.size();++i){
      for (int k=0;k<regions.size();++k){
        for( auto it = vars.cbegin() ; it != vars.cend() ; ++it ){
          name<<channelsSys[i]<<"_"<<regions[k]<<"_"<<it->first<<"_"<<"_Up";
          h_test = new TH1EFT((name.str()).c_str(),(name.str()).c_str(),std::get<1>(it->second), std::get<2>(it->second));
          h_test->SetDirectory(0);
          h_test->StatOverflows(kTRUE);
         // h_test->Sumw2(kTRUE);
          HistsSysCompactUp[i][k][std::get<0>(it->second)] = h_test;
          name.str("");
          name<<channelsSys[i]<<"_"<<regions[k]<<"_"<<it->first<<"_"<<"_Down";
          h_test = new TH1EFT((name.str()).c_str(),(name.str()).c_str(),std::get<1>(it->second), std::get<2>(it->second));
          h_test->SetDirectory(0);
          h_test->StatOverflows(kTRUE);
         // h_test->Sumw2(kTRUE);
          HistsSysCompactDown[i][k][std::get<0>(it->second)] = h_test;
          name.str("");
        }
      }
    }

    HistsSysUp.resize(channelsSys.size());
    for (int i=0;i<channelsSys.size();++i){
      HistsSysUp[i].resize(regions.size());
      for (int k=0;k<regions.size();++k){
        HistsSysUp[i][k].resize(varsFullSys.size());
        for (int n=0;n<varsFullSys.size();++n){
          HistsSysUp[i][k][n].resize(sys.size());
        }
      }
    }
    HistsSysDown.resize(channelsSys.size());
    for (int i=0;i<channelsSys.size();++i){
      HistsSysDown[i].resize(regions.size());
      for (int k=0;k<regions.size();++k){
        HistsSysDown[i][k].resize(varsFullSys.size());
        for (int n=0;n<varsFullSys.size();++n){
          HistsSysDown[i][k][n].resize(sys.size());
        }
      }
    }
    for (int i=0;i<channelsSys.size();++i){
      for (int k=0;k<regions.size();++k){
        for( auto it = varsFullSys.cbegin() ; it != varsFullSys.cend() ; ++it ){
          for (int n=0;n<sys.size();++n){
            name<<channelsSys[i]<<"_"<<regions[k]<<"_"<<it->first<<"_"<<sys[n]<<"_Up";
            h_test = new TH1EFT((name.str()).c_str(),(name.str()).c_str(),std::get<1>(it->second), std::get<2>(it->second));
            h_test->SetDirectory(0);
            h_test->StatOverflows(kTRUE);
           // h_test->Sumw2(kTRUE);
            HistsSysUp[i][k][std::get<0>(it->second)][n] = h_test;
            name.str("");
            name<<channelsSys[i]<<"_"<<regions[k]<<"_"<<it->first<<"_"<<sys[n]<<"_Down";
            h_test = new TH1EFT((name.str()).c_str(),(name.str()).c_str(),std::get<1>(it->second), std::get<2>(it->second));
            h_test->SetDirectory(0);
            h_test->StatOverflows(kTRUE);
           // h_test->Sumw2(kTRUE);
            HistsSysDown[i][k][std::get<0>(it->second)][n] = h_test;
            name.str("");
          }
        }
      }
    }

    HistsNormalSysUp.resize(channelsSys.size());
    for (int i=0;i<channelsSys.size();++i){
      HistsNormalSysUp[i].resize(regions.size());
      for (int k=0;k<regions.size();++k){
        HistsNormalSysUp[i][k].resize(vars.size());
        for (int n=0;n<vars.size();++n){
          HistsNormalSysUp[i][k][n].resize(sysNormal.size());
        }
      }
    }
    HistsNormalSysDown.resize(channelsSys.size());
    for (int i=0;i<channelsSys.size();++i){
      HistsNormalSysDown[i].resize(regions.size());
      for (int k=0;k<regions.size();++k){
        HistsNormalSysDown[i][k].resize(vars.size());
        for (int n=0;n<vars.size();++n){
          HistsNormalSysDown[i][k][n].resize(sysNormal.size());
        }
      }
    }

    for (int i=0;i<channelsSys.size();++i){
      for (int k=0;k<regions.size();++k){
        for( auto it = vars.cbegin() ; it != vars.cend() ; ++it ){
          for (int n=0;n<sysNormal.size();++n){
            name<<channelsSys[i]<<"_"<<regions[k]<<"_"<<it->first<<"_"<<sysNormal[n]<<"__Up";
            h_testNormal = new TH1F((name.str()).c_str(),(name.str()).c_str(),std::get<1>(it->second), std::get<2>(it->second));
            h_testNormal->SetDirectory(0);
            h_testNormal->StatOverflows(kTRUE);
           // h_test->Sumw2(kTRUE);
            HistsNormalSysUp[i][k][std::get<0>(it->second)][n] = h_testNormal;
            name.str("");
            name<<channelsSys[i]<<"_"<<regions[k]<<"_"<<it->first<<"_"<<sysNormal[n]<<"__Down";
            h_testNormal = new TH1F((name.str()).c_str(),(name.str()).c_str(),std::get<1>(it->second), std::get<2>(it->second));
            h_testNormal->SetDirectory(0);
            h_testNormal->StatOverflows(kTRUE);
           // h_test->Sumw2(kTRUE);
            HistsNormalSysDown[i][k][std::get<0>(it->second)][n] = h_testNormal;
            name.str("");
          }
        }
      }
    }

    HistsTh.resize(channelsSys.size());
    for (int i=0;i<channelsSys.size();++i){
      HistsTh[i].resize(regions.size());
      for (int k=0;k<regions.size();++k){
        HistsTh[i][k].resize(varsFullSys.size());
      }
    }
    for (int i=0;i<channelsSys.size();++i){
      for (int k=0;k<regions.size();++k){
        for( auto it = varsFullSys.cbegin() ; it != varsFullSys.cend() ; ++it ){
          name<<channelsSys[i]<<"_"<<regions[k]<<"_"<<it->first<<"_Th";
          h_test = new TH1EFT((name.str()).c_str(),(name.str()).c_str(),std::get<1>(it->second), std::get<2>(it->second));
          h_test->SetDirectory(0);
          h_test->StatOverflows(kTRUE);
          HistsTh[i][k][std::get<0>(it->second)] = h_test;
          name.str("");
        }
      }
    }
  }
  cout<<"All histograms are initiated"<<endl;
  tree_out = new TTree("FCNC","Top FCNC analysis") ;
  tree_out->Branch("HT"      , &HT_ , "HT/F" ) ;
  tree_out->Branch("lep1Pt"      , &lep1Pt_ , "lep1Pt/F" ) ;
  tree_out->Branch("lep1Eta"      , &lep1Eta_ , "lep1Eta/F" ) ;
  tree_out->Branch("lep2Pt"      , &lep2Pt_ , "lep2Pt/F" ) ;
  tree_out->Branch("lep2Eta"      , &lep2Eta_ , "lep2Eta/F" ) ;
  tree_out->Branch("lep3Pt"      , &lep3Pt_ , "lep3Pt/F" ) ;
  tree_out->Branch("lep3Eta"      , &lep3Eta_ , "lep3Eta/F" ) ;
  tree_out->Branch("llM"      , &llM_ , "llM/F" ) ;
  tree_out->Branch("llPt"      , &llPt_ , "llPt/F" ) ;
  tree_out->Branch("llDr"      , &llDr_ , "llDr/F" ) ;
  tree_out->Branch("llDphi"      , &llDphi_ , "llDphi/F" ) ;
  tree_out->Branch("jet1Pt"      , &jet1Pt_ , "jet1Pt/F" ) ;
  tree_out->Branch("jet1Eta"      , &jet1Eta_ , "jet1Eta/F"  ) ;
  tree_out->Branch("bJetPt"      , &bJetPt_ , "bJetPt/F" ) ;
  tree_out->Branch("bJetEta"      , &bJetEta_ , "bJetEta/F"  ) ;
  tree_out->Branch("nJets"      , &nJets_ , "nJets/I"  ) ;
  tree_out->Branch("tH_topMass"      , &tH_topMass_ , "tH_topMass/F"  ) ;
  tree_out->Branch("tH_HMass"      , &tH_HMass_ , "tH_HMass/F"  ) ;
  tree_out->Branch("tH_WtopMass"      , &tH_WtopMass_ , "tH_WtopMass/F"  ) ;
  tree_out->Branch("tH_W1HMass"      , &tH_W1HMass_ , "tH_W1HMass/F"  ) ;
  tree_out->Branch("tH_W2HMass"      , &tH_W2HMass_ , "tH_W2HMass/F"  ) ;
  tree_out->Branch("tH_HPt"      , &tH_HPt_ , "tH_HPt/F"  ) ;
  tree_out->Branch("tH_HEta"      , &tH_HEta_ , "tH_HEta/F"  ) ;
  tree_out->Branch("tH_topPt"      , &tH_topPt_ , "tH_topPt/F"  ) ;
  tree_out->Branch("tH_topEta"      , &tH_topEta_ , "tH_topEta/F"  ) ;
  tree_out->Branch("tH_drWtopB"      , &tH_drWtopB_ , "tH_drWtopB/F"  ) ;
  tree_out->Branch("tH_drW1HW2H"      , &tH_drW1HW2H_ , "tH_drW1HW2H/F"  ) ;
  tree_out->Branch("tZ_topMass"      , &tZ_topMass_ , "tZ_topMass/F"  ) ;
  tree_out->Branch("tZ_ZMass"      , &tZ_ZMass_ , "tZ_ZMass/F"  ) ;
  tree_out->Branch("tZ_WtopMass"      , &tZ_WtopMass_ , "tZ_WtopMass/F"  ) ;
  tree_out->Branch("tZ_ZPt"      , &tZ_ZPt_ , "tZ_ZPt/F"  ) ;
  tree_out->Branch("tZ_ZEta"      , &tZ_ZEta_ , "tZ_ZEta/F"  ) ;
  tree_out->Branch("tZ_topPt"      , &tZ_topPt_ , "tZ_topPt/F"  ) ;
  tree_out->Branch("tZ_topEta"      , &tZ_topEta_ , "tZ_topEta/F"  ) ;

  tree_out->Branch("weightSM"      , &weightSM_ , "weightSM/F" ) ;
  tree_out->Branch("weightSMfake"      , &weightSMfake_ , "weightSMfake/F" ) ;
  tree_out->Branch("weightctp"      , &weightctp_ , "weightctp/F" ) ;
  tree_out->Branch("weightctlS"      , &weightctlS_ , "weightctlS/F" ) ;
  tree_out->Branch("weightcte"      , &weightcte_ , "weightcte/F" ) ;
  tree_out->Branch("weightctl"      , &weightctl_ , "weightctl/F" ) ;
  tree_out->Branch("weightctlT"      , &weightctlT_ , "weightctlT/F" ) ;
  tree_out->Branch("weightctZ"      , &weightctZ_ , "weightctZ/F" ) ;
  tree_out->Branch("weightcpt"      , &weightcpt_ , "weightcpt/F" ) ;
  tree_out->Branch("weightcpQM"      , &weightcpQM_ , "weightcpQM/F" ) ;
  tree_out->Branch("weightctA"      , &weightctA_ , "weightctA/F" ) ;
  tree_out->Branch("weightcQe"      , &weightcQe_ , "weightcQe/F" ) ;
  tree_out->Branch("weightctG"      , &weightctG_ , "weightctG/F" ) ;
  tree_out->Branch("weightcQlM"      , &weightcQlM_ , "weightcQlM/F" ) ;
  tree_out->Branch("ch"      , &ch_, "ch/I" ) ;
  tree_out->Branch("chFA"      , &chFA_, "chFA/I" ) ;
  tree_out->Branch("reg"      , &reg_, "reg/I" ) ;
  tree_out->Branch("MVATU"      , &MVATU_ , "MVATU/F" ) ;

  cout<<"Output tree is ready to be used"<<endl;
}

void MyAnalysis::inputs(TString data,string year){
  ROOT::DisableImplicitMT();
  const char* srcnames[nsrc] = {"FlavorQCD", "BBEC1", "Absolute", "RelativeBal", "RelativeSample_2016","Total"};
  string yearName;
  string yearNameS;
  yearName=year;
  if(year == "2016preVFP") yearName="2016APV";
  if(year == "2016postVFP") yearName="2016";
  yearNameS=year;
  if(year == "2016preVFP") yearNameS="2016apv";
  if(year == "2016postVFP") yearNameS="2016";
  if(data == "mc"){
    TFile *f_btagEff_Map = new TFile("/users/rgoldouz/FCNC/NanoAnalysis/input/btagEffs_TopEFT_2022_05_16.root");
    TH2F* htemp = (TH2F*)f_btagEff_Map->Get(("BtagSFB_DeepFlavM_" + yearNameS).c_str());
    btagEff_b_H = (TH2F*)htemp->Clone("btagEff_b_H_clone");  // Clone decouples from file
    btagEff_b_H->SetDirectory(0);  // Important: unbind from the file, especially in ROOT < 6.22
    htemp = (TH2F*)f_btagEff_Map->Get(("BtagSFC_DeepFlavM_" + yearNameS).c_str());
    btagEff_c_H = (TH2F*)htemp->Clone("btagEff_c_H_clone");  
    btagEff_c_H->SetDirectory(0);  
    htemp = (TH2F*)f_btagEff_Map->Get(("BtagSFL_DeepFlavM_" + yearNameS).c_str());
    btagEff_udsg_H = (TH2F*)htemp->Clone("btagEff_udsg_H_clone");  
    btagEff_udsg_H->SetDirectory(0);  
    f_btagEff_Map->Close();
    delete f_btagEff_Map;

    TFile *f_trigger = new TFile(("/users/rgoldouz/FCNC/NanoAnalysis/input/triggerScaleFactors_" + yearName + ".root").c_str());
    htemp = (TH2F*)f_trigger->Get("sf_2l_ee");
    sf_triggeree_H = (TH2F*)htemp->Clone("sf_triggeree_H_clone");
    sf_triggeree_H->SetDirectory(0);
    htemp = (TH2F*)f_trigger->Get("sf_2l_em");
    sf_triggeremu_H = (TH2F*)htemp->Clone("sf_triggeremu_H_clone");
    sf_triggeremu_H->SetDirectory(0);
    htemp = (TH2F*)f_trigger->Get("sf_2l_mm");
    sf_triggermumu_H = (TH2F*)htemp->Clone("sf_triggermumu_H_clone");
    sf_triggermumu_H->SetDirectory(0);
    f_trigger->Close();
    delete f_trigger;

    TFile *f_HighPtMuRecoSF = new TFile(("/users/rgoldouz/FCNC/NanoAnalysis/input/HighPtMuRecoSF_" + year + ".root").c_str());
    htemp = (TH2F*)f_HighPtMuRecoSF->Get("h2_HighPtMuRecoSF_pVsAbsEta");
    highPtMuRecoSF_pVsAbsEta_H = (TH2F*)htemp->Clone("highPtMuRecoSF_pVsAbsEta_H_clone");
    highPtMuRecoSF_pVsAbsEta_H->SetDirectory(0);
    f_HighPtMuRecoSF->Close();
    delete f_HighPtMuRecoSF;

    TFile *f_muonIsoIp = new TFile(("/users/rgoldouz/FCNC/NanoAnalysis/data/topCoffeaData/leptonSF/muon/egammaEffi" + yearName + "_iso_EGM2D.root").c_str());
    htemp = (TH2F*)f_muonIsoIp->Get("EGamma_SF2D");
    sf_muonIsoIp_H= (TH2F*)htemp->Clone("sf_muonIsoIp_H_clone");
    sf_muonIsoIp_H->SetDirectory(0);
    f_muonIsoIp->Close();
    delete f_muonIsoIp;

    TFile *f_muonLooseMVATight = new TFile(("/users/rgoldouz/FCNC/NanoAnalysis/data/topCoffeaData/leptonSF/muon/egammaEffi" + yearName + "_EGM2D.root").c_str());
    htemp = (TH2F*)f_muonLooseMVATight->Get("EGamma_SF2D");
    sf_muonLooseMVATight_H = (TH2F*)htemp->Clone("sf_muonLooseMVATight_H_clone");
    sf_muonLooseMVATight_H->SetDirectory(0);
    f_muonLooseMVATight->Close();
    delete f_muonLooseMVATight;

    TFile *f_eleLoose = new TFile(("/users/rgoldouz/FCNC/NanoAnalysis/data/topCoffeaData/leptonSF/elec/egammaEffi" + yearName + "_recoToloose_EGM2D.root").c_str());
    htemp = (TH2F*)f_eleLoose->Get("EGamma_SF2D");
    sf_eleLoose_H = (TH2F*)htemp->Clone("sf_eleLoose_H_clone");
    sf_eleLoose_H->SetDirectory(0);
    f_eleLoose->Close();
    delete f_eleLoose;

    TFile *f_eleIsoIp = new TFile(("/users/rgoldouz/FCNC/NanoAnalysis/data/topCoffeaData/leptonSF/elec/egammaEffi" + yearName + "_iso_EGM2D.root").c_str());
    htemp = (TH2F*)f_eleIsoIp->Get("EGamma_SF2D");
    sf_eleIsoIp_H = (TH2F*)htemp->Clone("sf_eleIsoIp_H_clone");
    sf_eleIsoIp_H->SetDirectory(0);
    f_eleIsoIp->Close();
    delete f_eleIsoIp;

    TFile *f_eleLooseMVATight = new TFile(("/users/rgoldouz/FCNC/NanoAnalysis/data/topCoffeaData/leptonSF/elecNEWmva/egammaEffi" + yearName + "_3l_EGM2D.root").c_str());
    htemp = (TH2F*)f_eleLooseMVATight->Get("EGamma_SF2D");
    sf_eleLooseMVATight_H = (TH2F*)htemp->Clone("sf_eleLooseMVATight_H_clone");
    sf_eleLooseMVATight_H->SetDirectory(0);
    f_eleLooseMVATight->Close();
    delete f_eleLooseMVATight;

    TFile *f_eleLooseMVATight2lss = new TFile(("/users/rgoldouz/FCNC/NanoAnalysis/data/topCoffeaData/leptonSF/elecNEWmva/egammaEffi" + yearName + "_2lss_EGM2D.root").c_str());
    htemp = (TH2F*)f_eleLooseMVATight2lss->Get("EGamma_SF2D");
    sf_eleLooseMVATight2lss_H =  (TH2F*)htemp->Clone("sf_eleLooseMVATight2lss_H_clone");
    sf_eleLooseMVATight2lss_H->SetDirectory(0);
    f_eleLooseMVATight2lss->Close();
    delete f_eleLooseMVATight2lss;
  }
  if(year == "2016preVFP"){
    JERFile1="/users/rgoldouz/FCNC/NanoAnalysis/input/JER/Summer20UL16APV_JRV3_MC/Summer20UL16APV_JRV3_MC_SF_AK4PFchs.txt";
    JERFile2="/users/rgoldouz/FCNC/NanoAnalysis/input/JER/Summer20UL16APV_JRV3_MC/Summer20UL16APV_JRV3_MC_PtResolution_AK4PFchs.txt";
    JECFile = "/users/rgoldouz/FCNC/NanoAnalysis/input/Summer19UL16APV_V7_MC/RegroupedV2_Summer19UL16APV_V7_MC_UncertaintySources_AK4PFchs.txt";
    rochesterFile = "/users/rgoldouz/FCNC/NanoAnalysis/input/RoccoR2016aUL.txt";
    eleSF="/users/rgoldouz/FCNC/NanoAnalysis/data/POG/EGM/2016preVFP_UL/electron.json.gz";
    muSF= "/users/rgoldouz/FCNC/NanoAnalysis/data/POG/MUO/2016preVFP_UL/muon_Z.json.gz";
    bSF="/users/rgoldouz/FCNC/NanoAnalysis/data/POG/BTV/2016preVFP_UL/btagging.json.gz";
    jetSF="/users/rgoldouz/FCNC/NanoAnalysis/data/POG/JME/2016preVFP_UL/UL16preVFP_jmar.json.gz";
    TFile *Map2016preVFP = new TFile("/users/rgoldouz/FCNC/NanoAnalysis/input/hotjets-UL16.root");
    TH2F* htemp = (TH2F*)Map2016preVFP->Get("h2hot_ul16_plus_hbm2_hbp12_qie11");
    jetVetoMaps_H = (TH2F*)htemp->Clone("jetVetoMaps_H_clone");
    jetVetoMaps_H->SetDirectory(0);
    Map2016preVFP->Close();
    delete Map2016preVFP;

    TFile *lepFR = new TFile("/users/rgoldouz/FCNC/NanoAnalysis/data/topCoffeaData/fromTTH/fakerate/fr_2016APV_2016_recorrected.root");
    htemp = (TH2F*)lepFR->Get("FR_mva085_mu_data_comb_recorrected");
    fr_mu_H = (TH2F*)htemp->Clone("fr_mu_H_clone");
    fr_mu_H->SetDirectory(0);
    htemp = (TH2F*)lepFR->Get("FR_mva085_mu_data_comb_recorrected_up");
    fr_mu_H_up = (TH2F*)htemp->Clone("FR_mva085_mu_data_comb_recorrected_up_clone");
    fr_mu_H_up->SetDirectory(0);
    htemp = (TH2F*)lepFR->Get("FR_mva085_mu_data_comb_recorrected_down");
    fr_mu_H_down = (TH2F*)htemp->Clone("FR_mva085_mu_data_comb_recorrected_down_clone");
    fr_mu_H_down->SetDirectory(0);
    htemp = (TH2F*)lepFR->Get("FR_mva085_mu_data_comb_recorrected_pt1");
    fr_mu_H_ptUp = (TH2F*)htemp->Clone("FR_mva085_mu_data_comb_recorrected_pt1_clone");
    fr_mu_H_ptUp->SetDirectory(0);
    htemp = (TH2F*)lepFR->Get("FR_mva085_mu_data_comb_recorrected_pt2");
    fr_mu_H_ptDown = (TH2F*)htemp->Clone("FR_mva085_mu_data_comb_recorrected_pt2_clone");
    fr_mu_H_ptDown->SetDirectory(0);
    htemp = (TH2F*)lepFR->Get("FR_mva085_mu_data_comb_recorrected_be1");
    fr_mu_H_etaUp = (TH2F*)htemp->Clone("FR_mva085_mu_data_comb_recorrected_be1_clone");
    fr_mu_H_etaUp->SetDirectory(0);
    htemp = (TH2F*)lepFR->Get("FR_mva085_mu_data_comb_recorrected_be2");
    fr_mu_H_etaDown = (TH2F*)htemp->Clone("FR_mva085_mu_data_comb_recorrected_be2_clone");
    fr_mu_H_etaDown->SetDirectory(0);

    htemp = (TH2F*)lepFR->Get("FR_mva090_el_data_comb_NC_recorrected");
    fr_ele_H = (TH2F*)htemp->Clone("fr_ele_H_clone");
    fr_ele_H->SetDirectory(0);
    htemp = (TH2F*)lepFR->Get("FR_mva090_el_data_comb_NC_recorrected_up");
    fr_ele_H_up = (TH2F*)htemp->Clone("FR_mva090_el_data_comb_NC_recorrected_up_clone");
    fr_ele_H_up->SetDirectory(0);
    htemp = (TH2F*)lepFR->Get("FR_mva090_el_data_comb_NC_recorrected_down");
    fr_ele_H_down = (TH2F*)htemp->Clone("FR_mva090_el_data_comb_NC_recorrected_down_clone");
    fr_ele_H_down->SetDirectory(0);
    htemp = (TH2F*)lepFR->Get("FR_mva090_el_data_comb_NC_recorrected_pt1");
    fr_ele_H_ptUp = (TH2F*)htemp->Clone("FR_mva090_el_data_comb_NC_recorrected_pt1_clone");
    fr_ele_H_ptUp->SetDirectory(0);
    htemp = (TH2F*)lepFR->Get("FR_mva090_el_data_comb_NC_recorrected_pt2");
    fr_ele_H_ptDown = (TH2F*)htemp->Clone("FR_mva090_el_data_comb_NC_recorrected_pt2_clone");
    fr_ele_H_ptDown->SetDirectory(0);
    htemp = (TH2F*)lepFR->Get("FR_mva090_el_data_comb_NC_recorrected_be1");
    fr_ele_H_etaUp = (TH2F*)htemp->Clone("FR_mva090_el_data_comb_NC_recorrected_be1_clone");
    fr_ele_H_etaUp->SetDirectory(0);
    htemp = (TH2F*)lepFR->Get("FR_mva090_el_data_comb_NC_recorrected_be2");
    fr_ele_H_etaDown = (TH2F*)htemp->Clone("FR_mva090_el_data_comb_NC_recorrected_be2_clone");
    fr_ele_H_etaDown->SetDirectory(0);
    lepFR->Close();
    delete lepFR;

    TFile *lepCF = new TFile("/users/rgoldouz/FCNC/NanoAnalysis/input/fliprates_frommc_UL16APV_recorrected.root");
    htemp = (TH2F*)lepCF->Get("chargeMisId");
    cf_ele_H = (TH2F*)htemp->Clone("cf_ele_H_clone");
    cf_ele_H->SetDirectory(0);
    lepCF->Close();
    delete lepCF;

    chargeFlipNorm=0.79;
    gLumiMask="/users/rgoldouz/FCNC/NanoAnalysis/input/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt";
    fRun=271036;
    lRun=284044;
  }

  if(year == "2016postVFP"){
    JERFile1="/users/rgoldouz/FCNC/NanoAnalysis/input/JER/Summer20UL16_JRV3_MC/Summer20UL16_JRV3_MC_SF_AK4PFchs.txt";
    JERFile2="/users/rgoldouz/FCNC/NanoAnalysis/input/JER/Summer20UL16_JRV3_MC/Summer20UL16_JRV3_MC_PtResolution_AK4PFchs.txt";
    JECFile = "/users/rgoldouz/FCNC/NanoAnalysis/input/Summer19UL16_V7_MC/RegroupedV2_Summer19UL16_V7_MC_UncertaintySources_AK4PFchs.txt";
    rochesterFile = "/users/rgoldouz/FCNC/NanoAnalysis/input/RoccoR2016bUL.txt";
    eleSF="/users/rgoldouz/FCNC/NanoAnalysis/data/POG/EGM/2016postVFP_UL/electron.json.gz";
    muSF= "/users/rgoldouz/FCNC/NanoAnalysis/data/POG/MUO/2016postVFP_UL/muon_Z.json.gz";
    bSF="/users/rgoldouz/FCNC/NanoAnalysis/data/POG/BTV/2016postVFP_UL/btagging.json.gz";
    jetSF="/users/rgoldouz/FCNC/NanoAnalysis/data/POG/JME/2016postVFP_UL/UL16postVFP_jmar.json.gz";
    TFile *Map2016postVFP = new TFile("/users/rgoldouz/FCNC/NanoAnalysis/input/hotjets-UL16.root");
    TH2F* htemp = (TH2F*)Map2016postVFP->Get("h2hot_ul16_plus_hbm2_hbp12_qie11");
    jetVetoMaps_H =  (TH2F*)htemp->Clone("jetVetoMaps_H_clone");
    jetVetoMaps_H->SetDirectory(0);
    Map2016postVFP->Close();
    delete Map2016postVFP;

    TFile *lepFR = new TFile("/users/rgoldouz/FCNC/NanoAnalysis/data/topCoffeaData/fromTTH/fakerate/fr_2016APV_2016_recorrected.root");
    htemp = (TH2F*)lepFR->Get("FR_mva085_mu_data_comb_recorrected");
    fr_mu_H = (TH2F*)htemp->Clone("fr_mu_H_clone");
    fr_mu_H->SetDirectory(0);
    htemp = (TH2F*)lepFR->Get("FR_mva085_mu_data_comb_recorrected_up");
    fr_mu_H_up = (TH2F*)htemp->Clone("FR_mva085_mu_data_comb_recorrected_up_clone");
    fr_mu_H_up->SetDirectory(0);
    htemp = (TH2F*)lepFR->Get("FR_mva085_mu_data_comb_recorrected_down");
    fr_mu_H_down = (TH2F*)htemp->Clone("FR_mva085_mu_data_comb_recorrected_down_clone");
    fr_mu_H_down->SetDirectory(0);
    htemp = (TH2F*)lepFR->Get("FR_mva085_mu_data_comb_recorrected_pt1");
    fr_mu_H_ptUp = (TH2F*)htemp->Clone("FR_mva085_mu_data_comb_recorrected_pt1_clone");
    fr_mu_H_ptUp->SetDirectory(0);
    htemp = (TH2F*)lepFR->Get("FR_mva085_mu_data_comb_recorrected_pt2");
    fr_mu_H_ptDown = (TH2F*)htemp->Clone("FR_mva085_mu_data_comb_recorrected_pt2_clone");
    fr_mu_H_ptDown->SetDirectory(0);
    htemp = (TH2F*)lepFR->Get("FR_mva085_mu_data_comb_recorrected_be1");
    fr_mu_H_etaUp = (TH2F*)htemp->Clone("FR_mva085_mu_data_comb_recorrected_be1_clone");
    fr_mu_H_etaUp->SetDirectory(0);
    htemp = (TH2F*)lepFR->Get("FR_mva085_mu_data_comb_recorrected_be2");
    fr_mu_H_etaDown = (TH2F*)htemp->Clone("FR_mva085_mu_data_comb_recorrected_be2_clone");
    fr_mu_H_etaDown->SetDirectory(0);

    htemp = (TH2F*)lepFR->Get("FR_mva090_el_data_comb_NC_recorrected");
    fr_ele_H = (TH2F*)htemp->Clone("fr_ele_H_clone");
    fr_ele_H->SetDirectory(0);
    htemp = (TH2F*)lepFR->Get("FR_mva090_el_data_comb_NC_recorrected_up");
    fr_ele_H_up = (TH2F*)htemp->Clone("FR_mva090_el_data_comb_NC_recorrected_up_clone");
    fr_ele_H_up->SetDirectory(0);
    htemp = (TH2F*)lepFR->Get("FR_mva090_el_data_comb_NC_recorrected_down");
    fr_ele_H_down = (TH2F*)htemp->Clone("FR_mva090_el_data_comb_NC_recorrected_down_clone");
    fr_ele_H_down->SetDirectory(0);
    htemp = (TH2F*)lepFR->Get("FR_mva090_el_data_comb_NC_recorrected_pt1");
    fr_ele_H_ptUp = (TH2F*)htemp->Clone("FR_mva090_el_data_comb_NC_recorrected_pt1_clone");
    fr_ele_H_ptUp->SetDirectory(0);
    htemp = (TH2F*)lepFR->Get("FR_mva090_el_data_comb_NC_recorrected_pt2");
    fr_ele_H_ptDown = (TH2F*)htemp->Clone("FR_mva090_el_data_comb_NC_recorrected_pt2_clone");
    fr_ele_H_ptDown->SetDirectory(0);
    htemp = (TH2F*)lepFR->Get("FR_mva090_el_data_comb_NC_recorrected_be1");
    fr_ele_H_etaUp = (TH2F*)htemp->Clone("FR_mva090_el_data_comb_NC_recorrected_be1_clone");
    fr_ele_H_etaUp->SetDirectory(0);
    htemp = (TH2F*)lepFR->Get("FR_mva090_el_data_comb_NC_recorrected_be2");
    fr_ele_H_etaDown = (TH2F*)htemp->Clone("FR_mva090_el_data_comb_NC_recorrected_be2_clone");
    fr_ele_H_etaDown->SetDirectory(0);
    lepFR->Close();
    delete lepFR;

    TFile *lepCF = new TFile("/users/rgoldouz/FCNC/NanoAnalysis/input/fliprates_frommc_UL16_recorrected.root");
    htemp = (TH2F*)lepCF->Get("chargeMisId");
    cf_ele_H = (TH2F*)htemp->Clone("cf_ele_H_clone");
    cf_ele_H->SetDirectory(0);
    lepCF->Close();
    delete lepCF;

    chargeFlipNorm=0.81;
    gLumiMask="/users/rgoldouz/FCNC/NanoAnalysis/input/Cert_271036-284044_13TeV_Legacy2016_Collisions16_JSON.txt";
    fRun=271036;
    lRun=284044;
  }

  if(year == "2017"){
    JERFile1="/users/rgoldouz/FCNC/NanoAnalysis/input/JER/Summer19UL17_JRV3_MC/Summer19UL17_JRV3_MC_SF_AK4PFchs.txt";
    JERFile2="/users/rgoldouz/FCNC/NanoAnalysis/input/JER/Summer19UL17_JRV3_MC/Summer19UL17_JRV3_MC_PtResolution_AK4PFchs.txt";
    srcnames[4] ="RelativeSample_2017"; 
    JECFile = "/users/rgoldouz/FCNC/NanoAnalysis/input/Summer19UL17_V5_MC/RegroupedV2_Summer19UL17_V5_MC_UncertaintySources_AK4PFchs.txt";
    rochesterFile = "/users/rgoldouz/FCNC/NanoAnalysis/input/RoccoR2017UL.txt";
    eleSF="/users/rgoldouz/FCNC/NanoAnalysis/data/POG/EGM/2017_UL/electron.json.gz";
    muSF= "/users/rgoldouz/FCNC/NanoAnalysis/data/POG/MUO/2017_UL/muon_Z.json.gz";
    bSF="/users/rgoldouz/FCNC/NanoAnalysis/data/POG/BTV/2017_UL/btagging.json.gz";
    jetSF="/users/rgoldouz/FCNC/NanoAnalysis/data/POG/JME/2017_UL/UL17_jmar.json.gz";
    TFile *Map2017 = new TFile("/users/rgoldouz/FCNC/NanoAnalysis/input/hotjets-UL17_v2.root");
    TH2F* htemp = (TH2F*)Map2017->Get("h2hot_ul17_plus_hep17_plus_hbpw89");    
    jetVetoMaps_H = (TH2F*)htemp->Clone("jetVetoMaps_H_clone");
    jetVetoMaps_H->SetDirectory(0);
    Map2017->Close();
    delete Map2017;

    TFile *lepFR = new TFile("/users/rgoldouz/FCNC/NanoAnalysis/data/topCoffeaData/fromTTH/fakerate/fr_2017_recorrected.root");
    htemp = (TH2F*)lepFR->Get("FR_mva085_mu_data_comb_recorrected");
    fr_mu_H = (TH2F*)htemp->Clone("fr_mu_H_clone");
    fr_mu_H->SetDirectory(0);
    htemp = (TH2F*)lepFR->Get("FR_mva085_mu_data_comb_recorrected_up");
    fr_mu_H_up = (TH2F*)htemp->Clone("FR_mva085_mu_data_comb_recorrected_up_clone");
    fr_mu_H_up->SetDirectory(0);
    htemp = (TH2F*)lepFR->Get("FR_mva085_mu_data_comb_recorrected_down");
    fr_mu_H_down = (TH2F*)htemp->Clone("FR_mva085_mu_data_comb_recorrected_down_clone");
    fr_mu_H_down->SetDirectory(0);
    htemp = (TH2F*)lepFR->Get("FR_mva085_mu_data_comb_recorrected_pt1");
    fr_mu_H_ptUp = (TH2F*)htemp->Clone("FR_mva085_mu_data_comb_recorrected_pt1_clone");
    fr_mu_H_ptUp->SetDirectory(0);
    htemp = (TH2F*)lepFR->Get("FR_mva085_mu_data_comb_recorrected_pt2");
    fr_mu_H_ptDown = (TH2F*)htemp->Clone("FR_mva085_mu_data_comb_recorrected_pt2_clone");
    fr_mu_H_ptDown->SetDirectory(0);
    htemp = (TH2F*)lepFR->Get("FR_mva085_mu_data_comb_recorrected_be1");
    fr_mu_H_etaUp = (TH2F*)htemp->Clone("FR_mva085_mu_data_comb_recorrected_be1_clone");
    fr_mu_H_etaUp->SetDirectory(0);    
    htemp = (TH2F*)lepFR->Get("FR_mva085_mu_data_comb_recorrected_be2");
    fr_mu_H_etaDown = (TH2F*)htemp->Clone("FR_mva085_mu_data_comb_recorrected_be2_clone");
    fr_mu_H_etaDown->SetDirectory(0);

    htemp = (TH2F*)lepFR->Get("FR_mva090_el_data_comb_NC_recorrected");
    fr_ele_H = (TH2F*)htemp->Clone("fr_ele_H_clone");
    fr_ele_H->SetDirectory(0);
    htemp = (TH2F*)lepFR->Get("FR_mva090_el_data_comb_NC_recorrected_up");
    fr_ele_H_up = (TH2F*)htemp->Clone("FR_mva090_el_data_comb_NC_recorrected_up_clone");
    fr_ele_H_up->SetDirectory(0);
    htemp = (TH2F*)lepFR->Get("FR_mva090_el_data_comb_NC_recorrected_down");
    fr_ele_H_down = (TH2F*)htemp->Clone("FR_mva090_el_data_comb_NC_recorrected_down_clone");
    fr_ele_H_down->SetDirectory(0);
    htemp = (TH2F*)lepFR->Get("FR_mva090_el_data_comb_NC_recorrected_pt1");
    fr_ele_H_ptUp = (TH2F*)htemp->Clone("FR_mva090_el_data_comb_NC_recorrected_pt1_clone");
    fr_ele_H_ptUp->SetDirectory(0);
    htemp = (TH2F*)lepFR->Get("FR_mva090_el_data_comb_NC_recorrected_pt2");
    fr_ele_H_ptDown = (TH2F*)htemp->Clone("FR_mva090_el_data_comb_NC_recorrected_pt2_clone");
    fr_ele_H_ptDown->SetDirectory(0);
    htemp = (TH2F*)lepFR->Get("FR_mva090_el_data_comb_NC_recorrected_be1");
    fr_ele_H_etaUp = (TH2F*)htemp->Clone("FR_mva090_el_data_comb_NC_recorrected_be1_clone");
    fr_ele_H_etaUp->SetDirectory(0);
    htemp = (TH2F*)lepFR->Get("FR_mva090_el_data_comb_NC_recorrected_be2");
    fr_ele_H_etaDown = (TH2F*)htemp->Clone("FR_mva090_el_data_comb_NC_recorrected_be2_clone");
    fr_ele_H_etaDown->SetDirectory(0);
    lepFR->Close();
    delete lepFR;

    TFile *lepCF = new TFile("/users/rgoldouz/FCNC/NanoAnalysis/input/fliprates_frommc_UL17_recorrected.root");
    htemp = (TH2F*)lepCF->Get("chargeMisId");
    cf_ele_H = (TH2F*)htemp->Clone("cf_ele_H_clone");
    cf_ele_H->SetDirectory(0);
    lepCF->Close();
    delete lepCF;

    gLumiMask="/users/rgoldouz/FCNC/NanoAnalysis/input/Cert_294927-306462_13TeV_UL2017_Collisions17_GoldenJSON.txt";
    chargeFlipNorm=1.22;
    fRun=294927;
    lRun=306462;
  }

  if(year == "2018"){
    JERFile1="/users/rgoldouz/FCNC/NanoAnalysis/input/JER/Summer19UL18_JRV2_MC/Summer19UL18_JRV2_MC_SF_AK4PFchs.txt";
    JERFile2="/users/rgoldouz/FCNC/NanoAnalysis/input/JER/Summer19UL18_JRV2_MC/Summer19UL18_JRV2_MC_PtResolution_AK4PFchs.txt";
    srcnames[4] ="RelativeSample_2018";
    JECFile = "/users/rgoldouz/FCNC/NanoAnalysis/input/Summer19UL18_V5_MC/RegroupedV2_Summer19UL18_V5_MC_UncertaintySources_AK4PFchs.txt";
    rochesterFile = "/users/rgoldouz/FCNC/NanoAnalysis/input/RoccoR2018UL.txt";
    eleSF="/users/rgoldouz/FCNC/NanoAnalysis/data/POG/EGM/2018_UL/electron.json.gz";
    muSF= "/users/rgoldouz/FCNC/NanoAnalysis/data/POG/MUO/2018_UL/muon_Z.json.gz";
    bSF="/users/rgoldouz/FCNC/NanoAnalysis/data/POG/BTV/2018_UL/btagging.json.gz";
    jetSF="/users/rgoldouz/FCNC/NanoAnalysis/data/POG/JME/2018_UL/UL18_jmar.json.gz";
    TFile *Map2018 = new TFile("/users/rgoldouz/FCNC/NanoAnalysis/input/hotjets-UL18.root");
    TH2F* htemp = (TH2F*)Map2018->Get("h2hot_ul18_plus_hem1516_and_hbp2m1");
    jetVetoMaps_H = (TH2F*)htemp->Clone("jetVetoMaps_H_clone");
    jetVetoMaps_H->SetDirectory(0);
    Map2018->Close();
    delete Map2018;

    TFile *lepFR = new TFile("/users/rgoldouz/FCNC/NanoAnalysis/data/topCoffeaData/fromTTH/fakerate/fr_2018_recorrected.root");
    htemp = (TH2F*)lepFR->Get("FR_mva085_mu_data_comb_recorrected");
    fr_mu_H = (TH2F*)htemp->Clone("fr_mu_H_clone");
    fr_mu_H->SetDirectory(0);
    htemp = (TH2F*)lepFR->Get("FR_mva085_mu_data_comb_recorrected_up");
    fr_mu_H_up = (TH2F*)htemp->Clone("FR_mva085_mu_data_comb_recorrected_up_clone");
    fr_mu_H_up->SetDirectory(0);
    htemp = (TH2F*)lepFR->Get("FR_mva085_mu_data_comb_recorrected_down");
    fr_mu_H_down = (TH2F*)htemp->Clone("FR_mva085_mu_data_comb_recorrected_down_clone");
    fr_mu_H_down->SetDirectory(0);
    htemp = (TH2F*)lepFR->Get("FR_mva085_mu_data_comb_recorrected_pt1");
    fr_mu_H_ptUp = (TH2F*)htemp->Clone("FR_mva085_mu_data_comb_recorrected_pt1_clone");
    fr_mu_H_ptUp->SetDirectory(0);
    htemp = (TH2F*)lepFR->Get("FR_mva085_mu_data_comb_recorrected_pt2");
    fr_mu_H_ptDown = (TH2F*)htemp->Clone("FR_mva085_mu_data_comb_recorrected_pt2_clone");
    fr_mu_H_ptDown->SetDirectory(0);
    htemp = (TH2F*)lepFR->Get("FR_mva085_mu_data_comb_recorrected_be1");
    fr_mu_H_etaUp = (TH2F*)htemp->Clone("FR_mva085_mu_data_comb_recorrected_be1_clone");
    fr_mu_H_etaUp->SetDirectory(0);
    htemp = (TH2F*)lepFR->Get("FR_mva085_mu_data_comb_recorrected_be2");
    fr_mu_H_etaDown = (TH2F*)htemp->Clone("FR_mva085_mu_data_comb_recorrected_be2_clone");
    fr_mu_H_etaDown->SetDirectory(0);

    htemp = (TH2F*)lepFR->Get("FR_mva090_el_data_comb_NC_recorrected");
    fr_ele_H = (TH2F*)htemp->Clone("fr_ele_H_clone");
    fr_ele_H->SetDirectory(0);
    htemp = (TH2F*)lepFR->Get("FR_mva090_el_data_comb_NC_recorrected_up");
    fr_ele_H_up = (TH2F*)htemp->Clone("FR_mva090_el_data_comb_NC_recorrected_up_clone");
    fr_ele_H_up->SetDirectory(0);
    htemp = (TH2F*)lepFR->Get("FR_mva090_el_data_comb_NC_recorrected_down");
    fr_ele_H_down = (TH2F*)htemp->Clone("FR_mva090_el_data_comb_NC_recorrected_down_clone");
    fr_ele_H_down->SetDirectory(0);
    htemp = (TH2F*)lepFR->Get("FR_mva090_el_data_comb_NC_recorrected_pt1");
    fr_ele_H_ptUp = (TH2F*)htemp->Clone("FR_mva090_el_data_comb_NC_recorrected_pt1_clone");
    fr_ele_H_ptUp->SetDirectory(0);
    htemp = (TH2F*)lepFR->Get("FR_mva090_el_data_comb_NC_recorrected_pt2");
    fr_ele_H_ptDown = (TH2F*)htemp->Clone("FR_mva090_el_data_comb_NC_recorrected_pt2_clone");
    fr_ele_H_ptDown->SetDirectory(0);
    htemp = (TH2F*)lepFR->Get("FR_mva090_el_data_comb_NC_recorrected_be1");
    fr_ele_H_etaUp = (TH2F*)htemp->Clone("FR_mva090_el_data_comb_NC_recorrected_be1_clone");
    fr_ele_H_etaUp->SetDirectory(0);
    htemp = (TH2F*)lepFR->Get("FR_mva090_el_data_comb_NC_recorrected_be2");
    fr_ele_H_etaDown = (TH2F*)htemp->Clone("FR_mva090_el_data_comb_NC_recorrected_be2_clone");
    fr_ele_H_etaDown->SetDirectory(0);
    lepFR->Close();
    delete lepFR;

    TFile *lepCF = new TFile("/users/rgoldouz/FCNC/NanoAnalysis/input/fliprates_frommc_UL18_recorrected.root");
    htemp = (TH2F*)lepCF->Get("chargeMisId");
    cf_ele_H =  (TH2F*)htemp->Clone("cf_ele_H_clone");
    cf_ele_H->SetDirectory(0);
    lepCF->Close();
    delete lepCF;
    gLumiMask="/users/rgoldouz/FCNC/NanoAnalysis/input/Cert_314472-325175_13TeV_Legacy2018_Collisions18_JSON.txt";
    chargeFlipNorm=1.12;
    fRun=314472;
    lRun=325175;
  }
  cout<<"Scale factor histograms are ready to be used"<<endl;

  csetFileEleSF = CorrectionSet::from_file(eleSF);
  csetEleIdReco = csetFileEleSF->at("UL-Electron-ID-SF");

  csetFileMuSF = CorrectionSet::from_file(muSF);
  csetMuReco = csetFileMuSF->at("NUM_TrackerMuons_DEN_genTracks");
  csetMuLoose = csetFileMuSF->at("NUM_LooseID_DEN_TrackerMuons");

  csetFilebSF = CorrectionSet::from_file(bSF);
  csetLightJetSF = csetFilebSF->at("deepJet_incl");
//  auto csetBcJetSF = csetFilebSF->at("deepCSV_mujets");
  csetBcJetSF = csetFilebSF->at("deepJet_comb");

  csetFileJetSF = CorrectionSet::from_file(jetSF);
  csetJetPuID = csetFileJetSF->at("PUJetID_eff");

  csetFilePDFScale = CorrectionSet::from_file("/users/rgoldouz/FCNC/NanoAnalysis/bin/lhe_weight_sums.json");
  csetPDF = csetFilePDFScale->at("pdf_weight_sums");
  csetScale = csetFilePDFScale->at("qcd_scale_weight_sums");

  nominalWeights.assign(sys.size(), 1);
  sysUpWeights.assign(sys.size(), 1);
  sysDownWeights.assign(sys.size(), 1);
  rc.init(rochesterFile);

  cout<<"Setting MVA"<<endl;
  TMVA::Tools::Instance();
  readerMVA3loffZ_TU = new TMVA::Reader( "!Color:!Silent" );
  readerMVA3loffZ_TU->AddVariable( "lep1Pt",       &MVA_lep1Pt    );
  readerMVA3loffZ_TU->AddVariable( "lep2Pt",       &MVA_lep2Pt    );
  readerMVA3loffZ_TU->AddVariable( "lep3Pt",       &MVA_lep3Pt    );
  readerMVA3loffZ_TU->AddVariable( "jet1Pt",       &MVA_jet1Pt    );
  readerMVA3loffZ_TU->AddVariable( "bJetPt",       &MVA_bJetPt    );
  readerMVA3loffZ_TU->AddVariable( "llDr",         &MVA_llDr    );
  readerMVA3loffZ_TU->AddVariable( "llDphi",       &MVA_llDphi    );
  readerMVA3loffZ_TU->AddVariable( "tZ_topMass",   &MVA_tZ_topMass    );
  readerMVA3loffZ_TU->AddVariable( "tZ_ZMass",     &MVA_tZ_ZMass    );
  readerMVA3loffZ_TU->AddVariable( "tZ_WtopMass",  &MVA_tZ_WtopMass    );
  readerMVA3loffZ_TU->AddVariable( "tZ_ZPt",       &MVA_tZ_ZPt    );
  readerMVA3loffZ_TU->AddVariable( "tZ_ZEta",      &MVA_tZ_ZEta    );
  readerMVA3loffZ_TU->AddVariable( "tZ_topPt",     &MVA_tZ_topPt    );
  readerMVA3loffZ_TU->AddVariable( "tZ_topEta",    &MVA_tZ_topEta    );
  readerMVA3loffZ_TU->AddVariable( "nJets",        &MVA_nJets    );
  readerMVA3loffZ_TU->BookMVA( "BDT::BDT", "/users/rgoldouz/FCNC/NanoAnalysis/MVA/tmp_TMVAClassification_TU_3loffZ/dataset/weights/TMVAMulticlass_TU_3loffZ_BDT.weights.xml");
  readerMVA3loffZ_TC = new TMVA::Reader( "!Color:!Silent" );
  readerMVA3loffZ_TC->AddVariable( "lep1Pt",       &MVA_lep1Pt    );
  readerMVA3loffZ_TC->AddVariable( "lep2Pt",       &MVA_lep2Pt    );
  readerMVA3loffZ_TC->AddVariable( "lep3Pt",       &MVA_lep3Pt    );
  readerMVA3loffZ_TC->AddVariable( "jet1Pt",       &MVA_jet1Pt    );
  readerMVA3loffZ_TC->AddVariable( "bJetPt",       &MVA_bJetPt    );
  readerMVA3loffZ_TC->AddVariable( "llDr",         &MVA_llDr    );
  readerMVA3loffZ_TC->AddVariable( "llDphi",       &MVA_llDphi    );
  readerMVA3loffZ_TC->AddVariable( "tZ_topMass",   &MVA_tZ_topMass    );
  readerMVA3loffZ_TC->AddVariable( "tZ_ZMass",     &MVA_tZ_ZMass    );
  readerMVA3loffZ_TC->AddVariable( "tZ_WtopMass",  &MVA_tZ_WtopMass    );
  readerMVA3loffZ_TC->AddVariable( "tZ_ZPt",       &MVA_tZ_ZPt    );
  readerMVA3loffZ_TC->AddVariable( "tZ_ZEta",      &MVA_tZ_ZEta    );
  readerMVA3loffZ_TC->AddVariable( "tZ_topPt",     &MVA_tZ_topPt    );
  readerMVA3loffZ_TC->AddVariable( "tZ_topEta",    &MVA_tZ_topEta    );
  readerMVA3loffZ_TC->AddVariable( "nJets",        &MVA_nJets    );
  readerMVA3loffZ_TC->BookMVA( "BDT::BDT", "/users/rgoldouz/FCNC/NanoAnalysis/MVA/tmp_TMVAClassification_TC_3loffZ/dataset/weights/TMVAMulticlass_TC_3loffZ_BDT.weights.xml");

  readerMVA3lonZ_TU = new TMVA::Reader( "!Color:!Silent" );
  readerMVA3lonZ_TU->AddVariable( "lep1Pt",       &MVA_lep1Pt    );
  readerMVA3lonZ_TU->AddVariable( "lep2Pt",       &MVA_lep2Pt    );
  readerMVA3lonZ_TU->AddVariable( "lep3Pt",       &MVA_lep3Pt    );
  readerMVA3lonZ_TU->AddVariable( "jet1Pt",       &MVA_jet1Pt    );
  readerMVA3lonZ_TU->AddVariable( "bJetPt",       &MVA_bJetPt    );
  readerMVA3lonZ_TU->AddVariable( "llDr",         &MVA_llDr    );
  readerMVA3lonZ_TU->AddVariable( "llDphi",       &MVA_llDphi    );
  readerMVA3lonZ_TU->AddVariable( "tZ_topMass",   &MVA_tZ_topMass    );
  readerMVA3lonZ_TU->AddVariable( "tZ_WtopMass",  &MVA_tZ_WtopMass    );
  readerMVA3lonZ_TU->AddVariable( "tZ_ZPt",       &MVA_tZ_ZPt    );
  readerMVA3lonZ_TU->AddVariable( "tZ_ZEta",      &MVA_tZ_ZEta    );
  readerMVA3lonZ_TU->AddVariable( "tZ_topPt",     &MVA_tZ_topPt    );
  readerMVA3lonZ_TU->AddVariable( "tZ_topEta",    &MVA_tZ_topEta    );
  readerMVA3lonZ_TU->AddVariable( "nJets",        &MVA_nJets    );
  readerMVA3lonZ_TU->BookMVA( "BDT::BDT", "/users/rgoldouz/FCNC/NanoAnalysis/MVA/tmp_TMVAClassification_TU_3lonZ/dataset/weights/TMVAMulticlass_TU_3lonZ_BDT.weights.xml");  
  readerMVA3lonZ_TC = new TMVA::Reader( "!Color:!Silent" );
  readerMVA3lonZ_TC->AddVariable( "lep1Pt",       &MVA_lep1Pt    );
  readerMVA3lonZ_TC->AddVariable( "lep2Pt",       &MVA_lep2Pt    );
  readerMVA3lonZ_TC->AddVariable( "lep3Pt",       &MVA_lep3Pt    );
  readerMVA3lonZ_TC->AddVariable( "jet1Pt",       &MVA_jet1Pt    );
  readerMVA3lonZ_TC->AddVariable( "bJetPt",       &MVA_bJetPt    );
  readerMVA3lonZ_TC->AddVariable( "llDr",         &MVA_llDr    );
  readerMVA3lonZ_TC->AddVariable( "llDphi",       &MVA_llDphi    );
  readerMVA3lonZ_TC->AddVariable( "tZ_topMass",   &MVA_tZ_topMass    );
  readerMVA3lonZ_TC->AddVariable( "tZ_WtopMass",  &MVA_tZ_WtopMass    );
  readerMVA3lonZ_TC->AddVariable( "tZ_ZPt",       &MVA_tZ_ZPt    );
  readerMVA3lonZ_TC->AddVariable( "tZ_ZEta",      &MVA_tZ_ZEta    );
  readerMVA3lonZ_TC->AddVariable( "tZ_topPt",     &MVA_tZ_topPt    );
  readerMVA3lonZ_TC->AddVariable( "tZ_topEta",    &MVA_tZ_topEta    );
  readerMVA3lonZ_TC->AddVariable( "nJets",        &MVA_nJets    );
  readerMVA3lonZ_TC->BookMVA( "BDT::BDT", "/users/rgoldouz/FCNC/NanoAnalysis/MVA/tmp_TMVAClassification_TC_3lonZ/dataset/weights/TMVAMulticlass_TC_3lonZ_BDT.weights.xml");

  readerMVA2lss_TU = new TMVA::Reader( "!Color:!Silent" );
  readerMVA2lss_TU->AddVariable( "lep1Pt",         &MVA_lep1Pt );
  readerMVA2lss_TU->AddVariable( "lep2Pt",         &MVA_lep2Pt );
  readerMVA2lss_TU->AddVariable( "jet1Pt",         &MVA_jet1Pt );
  readerMVA2lss_TU->AddVariable( "bJetPt",         &MVA_bJetPt );
  readerMVA2lss_TU->AddVariable( "llM",            &MVA_llM ); 
  readerMVA2lss_TU->AddVariable( "llPt",           &MVA_llPt );
  readerMVA2lss_TU->AddVariable( "llDr",           &MVA_llDr );
  readerMVA2lss_TU->AddVariable( "llDphi",         &MVA_llDphi );
  readerMVA2lss_TU->AddVariable( "tH_topMass",     &MVA_tH_topMass );
  readerMVA2lss_TU->AddVariable( "tH_HMass",       &MVA_tH_HMass );
  readerMVA2lss_TU->AddVariable( "tH_WtopMass",    &MVA_tH_WtopMass );
  readerMVA2lss_TU->AddVariable( "tH_W1HMass",     &MVA_tH_W1HMass );
  readerMVA2lss_TU->AddVariable( "tH_W2HMass",     &MVA_tH_W2HMass );
  readerMVA2lss_TU->AddVariable( "tH_HPt",         &MVA_tH_HPt );
  readerMVA2lss_TU->AddVariable( "tH_HEta",        &MVA_tH_HEta );
  readerMVA2lss_TU->AddVariable( "tH_topPt",       &MVA_tH_topPt );
  readerMVA2lss_TU->AddVariable( "tH_topEta",      &MVA_tH_topEta );
  readerMVA2lss_TU->AddVariable( "tH_drWtopB",     &MVA_tH_drWtopB );
  readerMVA2lss_TU->AddVariable( "tH_drW1HW2H",    &MVA_tH_drW1HW2H );
  readerMVA2lss_TU->AddVariable( "nJets",          &MVA_nJets );
  readerMVA2lss_TU->BookMVA( "BDT::BDT", "/users/rgoldouz/FCNC/NanoAnalysis/MVA/tmp_TMVAClassification_TU_2lss/dataset/weights/TMVAClassification_TU_2lss_BDT.weights.xml");

  readerMVA2lss_TC = new TMVA::Reader( "!Color:!Silent" );
  readerMVA2lss_TC->AddVariable( "lep1Pt",         &MVA_lep1Pt );
  readerMVA2lss_TC->AddVariable( "lep2Pt",         &MVA_lep2Pt );
  readerMVA2lss_TC->AddVariable( "jet1Pt",         &MVA_jet1Pt );
  readerMVA2lss_TC->AddVariable( "bJetPt",         &MVA_bJetPt );
  readerMVA2lss_TC->AddVariable( "llM",            &MVA_llM );
  readerMVA2lss_TC->AddVariable( "llPt",           &MVA_llPt );
  readerMVA2lss_TC->AddVariable( "llDr",           &MVA_llDr );
  readerMVA2lss_TC->AddVariable( "llDphi",         &MVA_llDphi );
  readerMVA2lss_TC->AddVariable( "tH_topMass",     &MVA_tH_topMass );
  readerMVA2lss_TC->AddVariable( "tH_HMass",       &MVA_tH_HMass );
  readerMVA2lss_TC->AddVariable( "tH_WtopMass",    &MVA_tH_WtopMass );
  readerMVA2lss_TC->AddVariable( "tH_W1HMass",     &MVA_tH_W1HMass );
  readerMVA2lss_TC->AddVariable( "tH_W2HMass",     &MVA_tH_W2HMass );
  readerMVA2lss_TC->AddVariable( "tH_HPt",         &MVA_tH_HPt );
  readerMVA2lss_TC->AddVariable( "tH_HEta",        &MVA_tH_HEta );
  readerMVA2lss_TC->AddVariable( "tH_topPt",       &MVA_tH_topPt );
  readerMVA2lss_TC->AddVariable( "tH_topEta",      &MVA_tH_topEta );
  readerMVA2lss_TC->AddVariable( "tH_drWtopB",     &MVA_tH_drWtopB );
  readerMVA2lss_TC->AddVariable( "tH_drW1HW2H",    &MVA_tH_drW1HW2H );
  readerMVA2lss_TC->AddVariable( "nJets",          &MVA_nJets );
  readerMVA2lss_TC->BookMVA( "BDT::BDT", "/users/rgoldouz/FCNC/NanoAnalysis/MVA/tmp_TMVAClassification_TC_2lss/dataset/weights/TMVAClassification_TC_2lss_BDT.weights.xml");

  vsrc.resize(nsrc);

  for (int isrc = 0; isrc < nsrc; isrc++) {
    JetCorrectorParameters *p = new JetCorrectorParameters(JECFile, srcnames[isrc]);
    JetCorrectionUncertainty *unc = new JetCorrectionUncertainty(*p);
    vsrc[isrc] = unc;
  }

  uncRes = JME::JetResolutionScaleFactor(JERFile1);
  resolution=JME::JetResolution(JERFile2);

}


void MyAnalysis::endHists(TString data,string year, bool ifSys){
  for (int i=0;i<channels.size();++i){
    for (int k=0;k<regions.size();++k){
      for (int l=0;l<vars.size();++l){
        Hists[i][k][l]  ->Write("",TObject::kOverwrite);
        delete Hists[i][k][l];
      }
    }
  }

  for (int i=0;i<channelsFA.size();++i){
    for (int k=0;k<regions.size();++k){
      for (int l=0;l<varsFA.size();++l){
        HistsFA[i][k][l]  ->Write("",TObject::kOverwrite);
        delete HistsFA[i][k][l];
      }
    }
  }

  for (int i=0;i<channelsFA.size();++i){
    for (int k=0;k<regions.size();++k){
      for (int l=0;l<varsFullSys.size();++l){
        for (int n=0;n<sysFA.size();++n){
          HistsFAUp[i][k][l][n]->Write("",TObject::kOverwrite);
          HistsFADown[i][k][l][n]->Write("",TObject::kOverwrite);
          delete HistsFAUp[i][k][l][n];
          delete HistsFADown[i][k][l][n];
        }
      }	  
    }
  }
  if (data == "mc" && ifSys){
    for (int i=0;i<channelsSys.size();++i){
      for (int k=0;k<regions.size();++k){
        for (int l=0;l<vars.size();++l){
          HistsSysCompactUp[i][k][l]->Write("",TObject::kOverwrite);
          delete HistsSysCompactUp[i][k][l];
          HistsSysCompactDown[i][k][l]->Write("",TObject::kOverwrite);
          delete HistsSysCompactDown[i][k][l];
          for (int n=0;n<sysNormal.size();++n){
            HistsNormalSysUp[i][k][l][n]->Write("",TObject::kOverwrite);
            HistsNormalSysDown[i][k][l][n]->Write("",TObject::kOverwrite);
            delete HistsNormalSysUp[i][k][l][n];
            delete HistsNormalSysDown[i][k][l][n];
          }
        }
      }
    }
    for (int i=0;i<channelsSys.size();++i){
      for (int k=0;k<regions.size();++k){
        for (int l=0;l<varsFullSys.size();++l){
	  HistsTh[i][k][l]->Write("",TObject::kOverwrite);
          delete HistsTh[i][k][l];
          for (int n=0;n<sys.size();++n){
            HistsSysUp[i][k][l][n]->Write("",TObject::kOverwrite);
            HistsSysDown[i][k][l][n]->Write("",TObject::kOverwrite);
            delete HistsSysUp[i][k][l][n];
            delete HistsSysDown[i][k][l][n];
          }
        }
      }
    }
  }
  tree_out->Write();
  delete tree_out;

  Hists.clear();
  Hists.shrink_to_fit();
  HistsFA.clear();
  HistsFA.shrink_to_fit();
//  cout<<"Hists cleaned"<<endl;
  if(ifSys){
    HistsSysUp.clear();
    HistsSysUp.shrink_to_fit();
//    cout<<"HistsSysUp cleaned"<<endl;
    HistsNormalSysUp.clear();
    HistsNormalSysUp.shrink_to_fit();
    HistsSysCompactUp.clear();
    HistsSysCompactUp.shrink_to_fit();
    HistsSysCompactDown.clear();
    HistsSysCompactDown.shrink_to_fit();
    HistsSysDown.clear();
    HistsSysDown.shrink_to_fit();
    HistsNormalSysDown.clear();
    HistsNormalSysDown.shrink_to_fit();
//    cout<<"HistsSysDown cleaned"<<endl;
    HistsTh.clear();
    HistsTh.shrink_to_fit();
//    cout<<"HistsSysUp cleaned"<<endl;

  }
}










