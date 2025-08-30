#include "../include/MyAnalysis.h"
int main(){
    TChain* ch    = new TChain("Events") ;

//    ch ->Add("/cms/cephfs/data/store/user/rgoldouz/FullProduction/FCNC_DAS/Skim_v2/mc/UL17_TUToFCNCToTLLProduction/output_2*");
//    ch ->Add("/cms/cephfs/data/store/user/rgoldouz/FullProduction/AnalysisTOPFCNC/Analysis_UL17_ZZTo4L/ANoutput_39.root");
//    ch ->Add("/cms/cephfs/data/store/user/awightma/skims/mc/new-lepMVA-v2/central_bkgd_p7/TWZToLL/v1/UL17_TWZToLL_tlept_Wlept/output_147.root");
//    ch ->Add("/cms/cephfs/data/store/user/awightma/skims/mc/new-lepMVA-v2/central_bkgd_p1/FullRun2/v2/UL17_ZZTo4L/output_3950.root");
//    ch ->Add("/cms/cephfs/data/store/user/awightma/skims/mc/new-lepMVA-v2/central_sgnl/FullRun2/v1/UL17_TTWJetsToLNu/output_1*");
//    ch ->Add("/cms/cephfs/data/store/user/rgoldouz/FullProduction/FCNC_DAS/Skim_v2/mc/UL17_TUToFCNCToUHDecay/output_69.root");
//    ch ->Add("/cms/cephfs/data/store/user/rgoldouz/FullProduction/FCNC_DAS/Skim_v2/mc/UL17_TCToFCNCToCHDecay/output_44.root");
//    ch ->Add("/cms/cephfs/data/store/user/rgoldouz/FullProduction/FCNC_DAS/Skim_v2/mc/UL17_TUToFCNCToULLDecay/output_90.root");
//    ch ->Add("/cms/cephfs/data/store/user/awightma/skims/mc/new-lepMVA-v2/central_sgnl/FullRun2/v1/UL17_TTZToLLNuNu_M_10/output_291.root");
//    ch ->Add("/cms/cephfs/data/store/user/awightma/skims/mc/new-lepMVA-v2/central_bkgd_p1/FullRun2/v2/UL17_DY50/output_1847.root");
//    ch ->Add("/cms/cephfs/data/store/user/awightma/skims/mc/new-lepMVA-v2/central_sgnl/FullRun2/v1/UL18_tttt/output_278.root");
//    ch ->Add("/cms/cephfs/data/store/user/awightma/skims/mc/new-lepMVA-v2/central_sgnl/FullRun2/v1/UL16_TTWJetsToLNu/output_566.root");
    ch ->Add("/cms/cephfs/data/store/user/rgoldouz/FullProduction/FCNC_DAS/Skim_v2/mc/UL18_TUToFCNCToTLLProduction/output_196.root");
//    ch ->Add("/cms/cephfs/data/store/user/awightma/skims/data/NAOD_ULv9_new-lepMVA-v2/FullRun2/v3/SingleMuon_D_UL2018/output_4998.root");
//    ch ->Add("/cms/cephfs/data/store/user/awightma/skims/data/NAOD_ULv9_new-lepMVA-v2/FullRun2/v3/SingleMuon_D_UL2017/output_1729.root");
//    ch ->Add("/cms/cephfs/data/store/user/awightma/skims/mc/new-lepMVA-v2/central_bkgd_p1/2016APV/v1/UL16APV_tbarW/output_536.root");
//    ch ->Add("/cms/cephfs/data/store/user/awightma/skims/data/NAOD_ULv9_new-lepMVA-v2/2016APV/v1/SingleMuon_E_HIPM_UL2016/output_740.root");
//    ch ->Add("/cms/cephfs/data/store/user/awightma/skims/data/NAOD_ULv9_new-lepMVA-v2/2016APV_eraB/v1/DoubleEG_B_ver2_HIPM_UL2016/output_322.root");
//    ch ->Add("/cms/cephfs/data/store/user/awightma/skims/mc/new-lepMVA-v2/central_bkgd_p1/FullRun2/v2/UL18_DY50/output_1380.root");
//        ch ->Add("/cms/cephfs/data/store/user/awightma/skims/mc/new-lepMVA-v2/central_bkgd_p1/FullRun2/v2/UL16_ZZTo4L/output_3749.root");
//    ch ->Add("/cms/cephfs/data/store/user/awightma/skims/mc/new-lepMVA-v2/central_bkgd_p1/FullRun2/v2/UL17_ZZTo4L/output_3955.root");
    MyAnalysis * t1 = new MyAnalysis(ch);

//      t1->Analyze("UL17_TTTo2L2Nu", "mc" , "none" , "2016postVFP" , "none" , 10 , 41.48 , 300000 , 0 , 1 , 0, t1);
    t1->Analyze("UL17_TUToFCNCToULLDecay", "mc" , "none" , "2018" , "none" , 10 , 41.48 , 300000 , 1 , 1 , 0, t1);
//    t1->Analyze("UL16_data", "data","SingleMuon", "2018", "none", 10 , 41.48 , 300000 , 0 , 1 , 0, t1);
 
delete t1;
}
