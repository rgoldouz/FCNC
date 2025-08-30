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

int TMVAClassification_TU_2lss()
{
    // Initialize TMVA
    TMVA::Tools::Instance();
    TFile* outputFile = TFile::Open("TMVAOutput_TU_2lss.root", "RECREATE");
    TMVA::Factory* factory = new TMVA::Factory("TMVAClassification_TU_2lss", outputFile,
                                           "!V:!Silent:Color:DrawProgressBar:AnalysisType=Classification");
    TMVA::DataLoader* dataloader = new TMVA::DataLoader("dataset");

    // Load the input ROOT file and retrieve the tree
    TFile* inputB1 = TFile::Open( "/users/rgoldouz/FCNC/NanoAnalysis/MVA/2017_totalBG.root" );
    TFile* inputS1 = TFile::Open( "/users/rgoldouz/FCNC/NanoAnalysis/MVA/2017_FCNCTU.root" );

    TTree *background1     = (TTree*)inputB1->Get("FCNC");
    TTree *signalTree1     = (TTree*)inputS1->Get("FCNC");

    // Define input variables
    dataloader->AddVariable( "lep1Pt",                "lep1Pt", "GeV", 'F' );
    dataloader->AddVariable( "lep2Pt",                "lep2Pt", "GeV", 'F' );
    dataloader->AddVariable( "jet1Pt",                "jet1Pt", "GeV", 'F' );
    dataloader->AddVariable( "bJetPt",                "bJetPt", "GeV", 'F' );
    dataloader->AddVariable( "llM",                "llM", "GeV", 'F' );
    dataloader->AddVariable( "llPt",                "llPt", "GeV", 'F' );
    dataloader->AddVariable( "llDr",                "llDr", "", 'F' );
    dataloader->AddVariable( "llDphi",                "llDphi", "", 'F' );
    dataloader->AddVariable( "tH_topMass", "tH_topMass", "GeV", 'F' );
    dataloader->AddVariable( "tH_HMass", "tH_HMass_", "GeV", 'F' );
    dataloader->AddVariable( "tH_WtopMass", "tH_WtopMass", "GeV", 'F' );
    dataloader->AddVariable( "tH_W1HMass", "tH_W1HMass_", "GeV", 'F' );
    dataloader->AddVariable( "tH_W2HMass", "tH_W2HMass", "GeV", 'F' );
    dataloader->AddVariable( "tH_HPt", "tH_HPt", "GeV", 'F' );
    dataloader->AddVariable( "tH_HEta", "tH_HEta", "", 'F' );
    dataloader->AddVariable( "tH_topPt", "tH_topPt", "GeV", 'F' );
    dataloader->AddVariable( "tH_topEta", "tH_topEta", "", 'F' );
    dataloader->AddVariable( "tH_drWtopB", "tH_drWtopB", "GeV", 'F' );
    dataloader->AddVariable( "tH_drW1HW2H", "tH_drW1HW2H", "GeV", 'F' );
    dataloader->AddVariable( "nJets","nJets","",'I' );
    // Add more variables as needed

    // Clone the tree for each signal class and assign corresponding weights

    TFile* tmpFile = TFile::Open("tmp.root", "RECREATE");

    TTree* filteredBkgTree = background1->CopyTree("(ch==0) && weightSM>0");
    tmpFile->cd();
    filteredBkgTree->SetName("Background");
    filteredBkgTree->Write();

    TTree* filteredBkgTreeFake = background1->CopyTree("(chFA==0) && weightSMfake>0");
    tmpFile->cd();
    filteredBkgTreeFake->SetName("BackgroundFake");
    filteredBkgTreeFake->Write();

    TTree* filteredSigTree = signalTree1->CopyTree("(ch==0) && weightctp>0.001");
    tmpFile->cd();
    filteredSigTree->SetName("Signal");
    filteredSigTree->Write();

    dataloader->AddTree(filteredSigTree, "Signal", 1.0,"ch==0");
    dataloader->SetWeightExpression("weightctp", "Signal");
    // Add background tree (assuming it's separate)
    dataloader->AddTree(filteredBkgTree, "Background", 1.0,"ch==0");
    dataloader->SetWeightExpression("weightSM", "Background");
    dataloader->AddTree(filteredBkgTreeFake, "Background", 1.0,"chFA==0");
    dataloader->SetWeightExpression("weightSMfake", "Background");

    // Prepare training and testing trees
    dataloader->PrepareTrainingAndTestTree("","",
    "SplitMode=Random:NormMode=NumEvents:!V");

    // Book a multiclass BDT method
    factory->BookMethod(dataloader, TMVA::Types::kBDT, "BDT",
    "!H:!V:BoostType=Grad:Shrinkage=0.05:NTrees=500:MaxDepth=3:nCuts=10:UseBaggedBoost:BaggedSampleFraction=0.8:SeparationType=GiniIndex");

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

 
