#include "../include/MyAnalysis.h"
int main(){
    TChain* ch    = new TChain("Events") ;
//    ch ->Add("/cms/cephfs/data/store/user/rgoldouz/FullProduction/FullR2/UL17/FullSimFCNC/postLHE_step/v1/UL17_tuFCNC_tllProduction_noH/NAOD-00000_402.root");
//    ch ->Add("/cms/cephfs/data/store/user/awightma/skims/mc/new-lepMVA-v2/central_bkgd_p3/TTbarPowheg_ZG/v1/UL17_TTTo2L2Nu/output_1368.root");
//    ch ->Add("/cms/cephfs/data/store/user/rgoldouz/FullProduction/FullR2/UL17/FullSimFCNC/postLHE_step/v1/UL17_tuFCNC_tllProduction_noH_skimmed/output_7.root");
//    ch ->Add("/cms/cephfs/data/store/user/rgoldouz/FullProduction/FullR2/UL17/FullSimFCNC/postLHE_step/v1/UL17_tuFCNC_tHProduction_skimmed/output_1*.root");
//    ch ->Add("/cms/cephfs/data/store/user/rgoldouz/FullProduction/FCNC_DAS/Skim_v1/UL17_TUToFCNCToTHProduction_skimmed/output_*.root");
//    ch ->Add("/cms/cephfs/data/store/user/awightma/skims/mc/new-lepMVA-v2/central_bkgd_p3/TTbarPowheg_ZG/v1/UL17_TTToSemiLeptonic/output_1676.root");
//    ch ->Add("/cms/cephfs/data/store/user/awightma/skims/mc/new-lepMVA-v2/central_sgnl/FullRun2/v1/UL17_TTWJetsToLNu/output_6.root");
    ch ->Add("/cms/cephfs/data/store/user/awightma/skims/data/NAOD_ULv9_new-lepMVA-v2/FullRun2/v3/MuonEG_B_UL2017/output_3259.root");
//    ch ->Add("/cms/cephfs/data/store/user/awightma/skims/mc/new-lepMVA-v2/central_bkgd_p1/FullRun2/v2/UL17_DY50/output_3831.root");
//    ch ->Add("/cms/cephfs/data/store/user/rgoldouz/FullProduction/nanoGen/NanoGen_tuFCNCrwgt_tllProduction_noH/nanoGen_418.root");
//   ch ->Add("/cms/cephfs/data/store/user/awightma/skims/data/NAOD_ULv9_new-lepMVA-v2/2016APV/v1/DoubleMuon_C_HIPM_UL2016/output_322.root");
    MyAnalysis * t1 = new MyAnalysis(ch);

//    t1->Loop("UL17_tuFCNC_tllProduction_noH", "mc","none", "2017", "none", 1, 41.48, 400000, 1, 400, 0,t1);
//    t1->Loop("UL17_tuFCNC_ullDecay_noH", "mc" , "none" , "2017" , "none" , 1 , 41.48 , 300000 , 1 , 300 , 0, t1);
//    t1->Loop("UL17_tuFCNC_tllProduction_noH", "mc" , "none" , "2017" , "none" , 1 , 41.48 , 300000 , 1 , 1 , 0, t1);
//    t1->Loop("UL17_ttw", "mc" , "none" , "2017" , "none" , 1 , 41.48 , 300000 , 1 , 1 , 0, t1);
//    t1->Loop("UL17_data", "data","MuonEG", "2017", "none", 1, 41.48, 400000, 0, 400, 0,t1); 
//    t1->Loop("data_UL16preVFP_C_DoubleMuon", "data", "DoubleMuon", "2016preVFP", "C", 1, 19.52, 1, 0, 1, 0,t1);
    t1->Loop("UL17_data", "data" , "DoubleMuon" , "2017" , "D" , 1 , 59.83 , 1 , 0 , 1 , 0, t1);
//    t1->Loop("UL17_DY50", "mc","none", "2017", "none", 6077.22, 41.48, 131552424, 0, 400, 0,t1);   
delete t1;
}
