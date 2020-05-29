void plotN2Map(){
  // TString title = "ddtmap_smooth_gaus2";

  // TString file_path = "maps/"+title+".root";
  // TString hist_path = "N2_v_pT_v_rhoddt_map_smooth_0p05_maps_cleaner";
  // TString out_file_path = "maps/"+title+".pdf";

  TString title = "CristinasMap";

  TString file_path = "/afs/desy.de/user/a/albrechs/xxl/af-cms/UHH2/10_2/CMSSW_10_2_10/src/UHH2/JetMass/Histograms/OutputAK82017v13.root";
  TString hist_path = "Rho2D";
  TString out_file_path = title+".pdf";

  
  gStyle->SetPadTickY(1);
  gStyle->SetPadTickX(1);
  gStyle->SetLegendBorderSize(0);

  gROOT->SetBatch(true);
  gStyle->SetOptStat(0);
  gStyle->SetOptFit(0);
  // gStyle->SetOptTitle(0);
  // gStyle->SetTextFont(43);
  //
  gStyle->SetTitleOffset(0.86,"X");
  gStyle->SetTitleOffset(1.6,"Y");

  // gStyle->SetPadLeftMargin(0.1);
  gStyle->SetPadLeftMargin(0.14);
  gStyle->SetPadBottomMargin(0.12);
  gStyle->SetPadTopMargin(0.08);
  gStyle->SetPadRightMargin(0.16);

  gStyle->SetMarkerSize(0.5);
  gStyle->SetHistLineWidth(1);
  gStyle->SetTitleSize(0.05, "XYZ");
  gStyle->SetLabelSize(0.04, "XYZ");
  gStyle->SetNdivisions(506, "XYZ");
  gStyle->SetLegendBorderSize(0);
  
  
  TFile *f = new TFile(file_path);
  TH2D * hist = (TH2D*)f->Get(hist_path);
  
  hist->GetXaxis()->SetTitle("#rho");
  hist->GetYaxis()->SetTitle("p_{T} [GeV]");
  // hist->GetZaxis()->SetTitle("N2^{DDT} 5/% quantile");
  hist->GetZaxis()->SetTitle("DeepBoosted ZHbbvsQCD 5/% quantile");

  // hist->GetXaxis()->SetRangeUser(-6.0,-2.1);
  // hist->GetYaxis()->SetRangeUser(200,1200);
  hist->GetZaxis()->SetRangeUser(0.12,0.3);
  // hist->GetZaxis()->SetRangeUser(0,1.);

  gStyle->SetNumberContours(25);
  
  double Font=43;
  double TitleSize=24.0;
  double TitleOffset=1.3;
  double LabelSize=18.0;
  hist->GetYaxis()->SetTitleFont(Font);
  hist->GetYaxis()->SetTitleSize(TitleSize);
  hist->GetYaxis()->SetTitleOffset(TitleOffset);
  hist->GetYaxis()->SetLabelFont(Font);
  hist->GetYaxis()->SetLabelSize(LabelSize);

  hist->GetXaxis()->SetTitleFont(Font);
  hist->GetXaxis()->SetTitleSize(TitleSize);
  hist->GetXaxis()->SetTitleOffset(TitleOffset);
  hist->GetXaxis()->SetLabelFont(Font);
  hist->GetXaxis()->SetLabelSize(LabelSize);

  hist->GetZaxis()->SetTitleFont(Font);
  hist->GetZaxis()->SetTitleSize(TitleSize);
  hist->GetZaxis()->SetTitleOffset(TitleOffset);
  hist->GetZaxis()->SetLabelFont(Font);
  hist->GetZaxis()->SetLabelSize(LabelSize);

  hist->GetZaxis()->SetNdivisions(510);

  hist->SetTitle(title);
  hist->SetTitleFont(43);
  hist->SetTitleSize(20.0);
	
  TCanvas * c1 = new TCanvas("c1","c1",700,600);
  c1->cd();
  hist->Draw("colz");
  c1->SaveAs(out_file_path);
  delete c1;

}
