void plot_asimov(TString filename){
  gROOT->SetBatch(kTRUE);

  TFile *FitDiagnostics = new TFile(filename);


  RooDataSet * obs_toy = (RooDataSet*) FitDiagnostics->Get("toys/toy_asimov");
  
  RooRealVar * msd =  new RooRealVar("msd","msd",1.);
  msd->setRange(0.,500.);
  msd->setBins(50);  

  TH1 *asimov = obs_toy->createHistogram("asimov",*msd);

  TCanvas *c = new TCanvas("c","c",600,600);

  asimov->Draw("h");

  c->SaveAs("asimov.pdf");
  
  
}
