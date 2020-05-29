#include "../include/CentralInclude.h"


using namespace std;
using namespace RooFit;

void SetPlotStyle();
// TH1F* GetRatio(TH1F* num, TH1F* den);
void PlotHist(TH1F* h_pass, TH1F* h_fail, TString name);

int main(int argc, char* argv[]){

  TString filename;

  if(argc != 2){
    cout << "specify file!" << endl;
    return 1;
  }
  else filename = argv[1];
  TFile* file = new TFile(filename);

  std::vector<TString> ptBins={"500To550","550To600","600To675","675To800","800To1200"};

  for(TString ptBin : ptBins){
    TString histDir = "JetMass_N2DDT_pt";
    std::cout << "ptbin:" << ptBin << std::endl;
    TH1F* h_pass=(TH1F*) file->Get(histDir+ptBin+"_pass/Rho_central");
    TH1F* h_fail=(TH1F*) file->Get(histDir+ptBin+"_fail/Rho_central");
    std::cout << "ptbin:" << ptBin << std::endl;
    TH1F* h_Rpf =(TH1F*) h_pass->Clone();
    h_fail->Add(h_pass);
    h_Rpf->Divide(h_fail);
    SetPlotStyle();

    TCanvas *c = new TCanvas("c", "c", 600, 600);
    gPad->SetLeftMargin(0.16);
    gPad->SetBottomMargin(0.14);
    h_Rpf->SetTitle(" ");
    h_Rpf->GetXaxis()->SetTitle("#rho");
    h_Rpf->GetYaxis()->SetTitle("R_{p/f}");
    // h_Rpf->GetYaxis()->SetTitleOffset(1.6);
    // h_Rpf->GetXaxis()->SetTitleOffset(1.1);
    // h_Rpf->GetYaxis()->SetTitleSize(0.05);
    // h_Rpf->GetXaxis()->SetTitleSize(0.05);
    // h_Rpf->GetYaxis()->SetLabelSize(0.05);
    // h_Rpf->GetXaxis()->SetLabelSize(0.05);
    // h_Rpf->GetXaxis()->SetNdivisions(505);
    // h_Rpf->GetYaxis()->SetNdivisions(505);
    // h_Rpf->SetFillColor();
    // h_Rpf->SetLineColor();
    h_Rpf->Draw("P");
    gPad->RedrawAxis();
    c->SaveAs(histDir+ptBin+"_Rpf"+".pdf");
    delete c;
  }
  return 0;
}

void SetPlotStyle(){
  gStyle->SetOptStat(kFALSE);
  gStyle->SetPadTickY(1);
  gStyle->SetPadTickX(1);
  gStyle->SetLegendBorderSize(0);
  return;
}
