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

int TMVAClassification_TU_3loffZ()
{
    // Initialize TMVA
    TMVA::gConfig().SetSilent(false);  // Enable messages
    TMVA::Tools::Instance();
    TFile* outputFile = TFile::Open("TMVAOutput_TU_3loffZ.root", "RECREATE");
    TMVA::Factory* factory = new TMVA::Factory("TMVAMulticlass_TU_3loffZ", outputFile,
                                           "!V:!Silent:Color:DrawProgressBar:AnalysisType=Multiclass");
    TMVA::DataLoader* dataloader = new TMVA::DataLoader("dataset");

    // Load the input ROOT file and retrieve the tree
    TFile* inputB1 = TFile::Open( "/users/rgoldouz/FCNC/NanoAnalysis/MVA/2017_totalBG.root" );
    TFile* inputS1 = TFile::Open( "/users/rgoldouz/FCNC/NanoAnalysis/MVA/2017_FCNCTU.root" );

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
    dataloader->AddVariable( "tZ_ZMass", "tZ_ZMass", "GeV", 'F' );
    dataloader->AddVariable( "tZ_WtopMass", "tZ_WtopMass", "GeV", 'F' );
    dataloader->AddVariable( "tZ_ZPt", "tZ_ZPt", "GeV", 'F' );
    dataloader->AddVariable( "tZ_ZEta", "tZ_ZEta", "", 'F' );
    dataloader->AddVariable( "tZ_topPt", "tZ_topPt", "GeV", 'F' );
    dataloader->AddVariable( "tZ_topEta", "tZ_topEta", "", 'F' );
    dataloader->AddVariable( "nJets","nJets","",'I' );

    // Create the file to store filtered trees
    TFile* tmpFile = new TFile("tmp.root", "RECREATE");
    
    const int numClasses = 3;
    TString classNames[numClasses] = {"ctlS","ctlT","ctlV"};
    TCut cuts[numClasses] = {
        "(ch==6)  && weightctlS>0.00001",
        "(ch==6) && weightctlT>0.0001",
        "(ch==6) && (weightcte>0.00001 || weightctl>0.00001 || weightcQe>0.00001 || weightcQlM>0.00001)"
    };
    
    for (int i = 0; i < numClasses; ++i) {
        // Apply the cut and clone the tree into the tmpFile
        tmpFile->cd(); // Ensure we're writing to the tmpFile
        TTree* filteredSigTree = signalTree1->CopyTree(cuts[i]);
        filteredSigTree->SetName(classNames[i]); // Optionally rename for clarity
        filteredSigTree->Write(); // Write the tree to tmpFile
    
        dataloader->AddTree(filteredSigTree, classNames[i], 1.0, "ch==6");
    }
    
    // Add background tree
    TTree* filteredBkgTree = background1->CopyTree("(ch==6) && weightSM>0");
    tmpFile->cd();
    filteredBkgTree->SetName("Background");
    filteredBkgTree->Write();
    
    dataloader->AddTree(filteredBkgTree, "Background", 1.0, "ch==6");
    // Set weights after adding trees
    dataloader->SetWeightExpression("weightSM", "Background");
    dataloader->SetWeightExpression("weightctlS", "ctlS");
    dataloader->SetWeightExpression("weightctlT", "ctlT");
    dataloader->SetWeightExpression("weightcte + weightctl + weightcQe + weightcQlM", "ctlV");    
    // Prepare training and testing
    dataloader->PrepareTrainingAndTestTree("","SplitMode=Random:NormMode=NumEvents:V");

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

 
