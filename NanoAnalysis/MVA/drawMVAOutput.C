void drawMVAOutput() {
    gSystem->Load("libTMVAGui");

    TString fname = "tmp_TMVAClassification_TC_3lonZ/TMVAOutput_TC_3lonZ.root";

    // Comparison
    TMVA::mvas("dataset", fname, TMVA::kCompareType);
    gPad->SaveAs("ctZ_MVA.pdf");

    // Input variables
    TMVA::variables("dataset", fname);
    gPad->SaveAs("ctZ_InputVar.pdf");

    // Correlation matrices
    TMVA::correlations("dataset", fname, "Signal");
    gPad->SaveAs("CorrelationMatrixS.pdf");

    TMVA::correlations("dataset", fname, "Background");
    gPad->SaveAs("CorrelationMatrixB.pdf");

    // ROC curve (2 is typically the method index, adjust if needed)
    TMVA::efficiencies("dataset", fname, 2);
    gPad->SaveAs("ROC.pdf");
}
