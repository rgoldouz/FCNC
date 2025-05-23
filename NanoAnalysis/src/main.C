#include "../include/MyAnalysis.h"
int main(){
    TChain* ch    = new TChain("Events") ;

//    ch ->Add("/cms/cephfs/data/store/user/rgoldouz/FullProduction/FCNC_DAS/Skim_v2/mc/UL17_TUToFCNCToTLLProduction/output_*");
//    ch ->Add("/cms/cephfs/data/store/user/rgoldouz/FullProduction/AnalysisTOPFCNC/Analysis_UL17_ZZTo4L/ANoutput_39.root");
//    ch ->Add("/cms/cephfs/data/store/user/awightma/skims/mc/new-lepMVA-v2/central_bkgd_p7/TWZToLL/v1/UL17_TWZToLL_tlept_Wlept/output_147.root");
//    ch ->Add("/cms/cephfs/data/store/user/awightma/skims/mc/new-lepMVA-v2/central_sgnl/FullRun2/v1/UL17_TTWJetsToLNu/output_1*");
//    ch ->Add("/cms/cephfs/data/store/user/rgoldouz/FullProduction/FCNC_DAS/Skim_v2/mc/UL17_TUToFCNCToUHDecay/output_69.root");
//    ch ->Add("/cms/cephfs/data/store/user/rgoldouz/FullProduction/FCNC_DAS/Skim_v2/mc/UL17_TCToFCNCToCHDecay/output_44.root");
//    ch ->Add("/cms/cephfs/data/store/user/rgoldouz/FullProduction/FCNC_DAS/Skim_v2/mc/UL17_TUToFCNCToULLDecay/output_*");
    ch ->Add("/cms/cephfs/data/store/user/awightma/skims/mc/new-lepMVA-v2/central_bkgd_p1/FullRun2/v2/UL17_ZZTo4L/output_3955.root");
    MyAnalysis * t1 = new MyAnalysis(ch);

    t1->Loop("UL17_ttW", "mc" , "none" , "2017" , "none" , 10 , 41.48 , 300000 , 0 , 1 , 0, t1);
//    t1->Loop("UL17_FCNCTTWJetsToLNu", "mc" , "none" , "2017" , "none" , 10 , 41.48 , 300000 , 1 , 1 , 0, t1);
//    t1->Loop("UL17_data", "data","MuonEG", "2017", "none", 1, 41.48, 400000, 0, 400, 0,t1); 
delete t1;
}
