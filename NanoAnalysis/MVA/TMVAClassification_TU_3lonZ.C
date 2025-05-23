/// \ingroup tutorial_tmva
 /// \notebook -nodraw
 /// This macro provides examples for the training and testing of the
 /// TMVA classifiers.
 ///
 /// As input data is used a toy-MC sample consisting of four Gaussian-distributed
 /// and linearly correlated input variables.
 /// The methods to be used can be switched on and off by means of booleans, or
 /// via the prompt command, for example:
 ///
 ///     root -l ./TMVAClassification.CUndefined control sequence \"
 ///
 /// (note that the backslashes are mandatory)
 /// If no method given, a default set of classifiers is used.
 /// The output file "TMVA.root" can be analysed with the use of dedicated
 /// macros (simply say: root -l <macro.C>), which can be conveniently
 /// invoked through a GUI that will appear at the end of the run of this macro.
 /// Launch the GUI via the command:
 ///
 ///     root -l ./TMVAGui.C
 ///
 /// You can also compile and run the example with the following commands
 ///
 ///     make
 ///     ./TMVAClassification <Methods>
 ///
 /// where: `<Methods> = "method1 method2"` are the TMVA classifier names
 /// example:
 ///
 ///     ./TMVAClassification Fisher LikelihoodPCA BDT
 ///
 /// If no method given, a default set is of classifiers is used
 ///
 /// - Project   : TMVA - a ROOT-integrated toolkit for multivariate data analysis
 /// - Package   : TMVA
 /// - Root Macro: TMVAClassification
 ///
 /// \macro_output
 /// \macro_code
 /// \author Andreas Hoecker
 
 
 #include <cstdlib>
 #include <iostream>
 #include <map>
 #include <string>
 
 #include "TChain.h"
 #include "TFile.h"
 #include "TTree.h"
 #include "TString.h"
 #include "TObjString.h"
 #include "TSystem.h"
 #include "TROOT.h"
 
 #include "TMVA/Factory.h"
 #include "TMVA/DataLoader.h"
 #include "TMVA/Tools.h"
 #include "TMVA/TMVAGui.h"

int TMVAClassification_TU_3lonZ()
{
    // Initialize TMVA
    TMVA::Tools::Instance();
    TFile* outputFile = TFile::Open("TMVAOutput_TU_3lonZ.root", "RECREATE");
    TMVA::Factory* factory = new TMVA::Factory("TMVAMulticlass_TU_3lonZ", outputFile,
                                           "!V:!Silent:Color:DrawProgressBar:AnalysisType=Multiclass");
    TMVA::DataLoader* dataloader = new TMVA::DataLoader("dataset");

    // Load the input ROOT file and retrieve the tree
    TFile* inputB1 = TFile::Open( "/afs/crc.nd.edu/user/r/rgoldouz/FCNC/NanoAnalysis/MVA/2017_totalBG.root" );
    TFile* inputS1 = TFile::Open( "/afs/crc.nd.edu/user/r/rgoldouz/FCNC/NanoAnalysis/MVA/2017_FCNCTU.root" );

    TTree *background1     = (TTree*)inputB1->Get("FCNC");
    TTree *signalTree1     = (TTree*)inputS1->Get("FCNC");

    // Define input variables
    dataloader->AddVariable( "lep1Pt",                "lep1Pt", "GeV", 'F' );
    dataloader->AddVariable( "lep2Pt",                "lep2Pt", "GeV", 'F' );
    dataloader->AddVariable( "lep3Pt",                "lep3Pt", "GeV", 'F' );
    dataloader->AddVariable( "jet1Pt",                "jet1Pt", "GeV", 'F' );
    dataloader->AddVariable( "bJetPt",                "bJetPt", "GeV", 'F' );
    dataloader->AddVariable( "llDr",                "llDr", "", 'F' );
    dataloader->AddVariable( "llDphi",                "llDphi", "", 'F' );
    dataloader->AddVariable( "tZ_topMass", "tZ_topMass", "GeV", 'F' );
    dataloader->AddVariable( "tZ_WtopMass", "tZ_WtopMass", "GeV", 'F' );
    dataloader->AddVariable( "tZ_ZPt", "tZ_ZPt", "GeV", 'F' );
    dataloader->AddVariable( "tZ_ZEta", "tZ_ZEta", "", 'F' );
    dataloader->AddVariable( "tZ_topPt", "tZ_topPt", "GeV", 'F' );
    dataloader->AddVariable( "tZ_topEta", "tZ_topEta", "", 'F' );
    dataloader->AddVariable( "nJets","nJets","",'I' );

    // Add more variables as needed

    // Clone the tree for each signal class and assign corresponding weights
    const int numClasses = 3;
    TString classNames[numClasses] = {"ctZ","cpt","cpQM"};
    TString weightBranches[numClasses] = {"weightctZ","weightcpt","weightcpQM"};
    TCut cuts[numClasses] = {"(ch==5) && weightctZ>0.001", "(ch==5) && weightcpt>0.001","(ch==5) && weightcpQM>0.001"};

    TFile* tmpFile = TFile::Open("tmp.root", "RECREATE");

    for (int i = 0; i < numClasses; ++i) {
        TTree* sigTree = signalTree1->CloneTree(-1, "fast");
//    If you need to apply a cut, you can apply event preselection via that 4th TCut parameter like:    dataloader->AddTree(sigTree, classNames[i],"pt > 30");
        dataloader->AddTree(sigTree, classNames[i], 1.0,cuts[i]);
        dataloader->SetWeightExpression(weightBranches[i], classNames[i]);
    }

    // Add background tree (assuming it's separate)
    dataloader->AddTree(background1, "Background", 1.0,"(ch==5) && weightSM>0");
//    dataloader->SetWeightExpression("weight_bg", "Background");

    // Prepare training and testing trees
    dataloader->PrepareTrainingAndTestTree("","",
    "SplitMode=Random:NormMode=NumEvents:!V");

    // Book a multiclass BDT method
factory->BookMethod(dataloader, TMVA::Types::kBDT, "BDT",
    "!H:!V:BoostType=Grad:Shrinkage=0.1:NTrees=200:MaxDepth=3:nCuts=20:UseBaggedBoost:BaggedSampleFraction=0.6:SeparationType=GiniIndex");
   // factory->BookMethod(dataloader, TMVA::Types::kBDT, "BDT",
  //   "!H:!V:NTrees=300:BoostType=Grad:SeparationType=GiniIndex:nCuts=20:MaxDepth=3");

    // Train, test, and evaluate the MVA methods
    factory->TrainAllMethods();
    factory->TestAllMethods();
    factory->EvaluateAllMethods();

    // Clean up
    outputFile->Close();
    delete factory;
    delete dataloader;

    return 0;
}

 
