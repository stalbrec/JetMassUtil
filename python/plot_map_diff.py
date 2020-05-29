from ROOT import gStyle, gROOT, TFile, TCanvas, TF1, TLatex
import os
import numpy as np
def plot_map(out_file_path, hist):
    map_name  = out_file_path if '/' not in out_file_path else out_file_path.split('/')[-1]
    map_name = map_name.replace('.pdf','')
    rho_min = -6.0
    rho_max = -2.6
    pt_min = 500.
    pt_max = 1200.
    # rho_min = -10
    # rho_max = 0
    # pt_min = 200
    # pt_max = 5000
    disc_min = 0.12
    disc_max = 0.3
    left_margin = 0.14
    right_margin = 0.16
    top_margin = 0.08
    bottom_margin = 0.12

    gStyle.SetPadTickY(1)
    gStyle.SetPadTickX(1)
    gStyle.SetLegendBorderSize(0)
    
    gROOT.SetBatch(True)
    gStyle.SetOptStat(0)
    gStyle.SetOptFit(0)
    gStyle.SetTitleOffset(0.86,"X")
    gStyle.SetTitleOffset(1.6,"Y")
    gStyle.SetPadLeftMargin(left_margin)
    gStyle.SetPadBottomMargin(bottom_margin)
    gStyle.SetPadTopMargin(top_margin)
    gStyle.SetPadRightMargin(right_margin)
    
    gStyle.SetMarkerSize(0.5)
    gStyle.SetHistLineWidth(1)
    gStyle.SetTitleSize(0.05, "XYZ")
    gStyle.SetLabelSize(0.04, "XYZ")
    gStyle.SetNdivisions(506, "XYZ")
    gStyle.SetNumberContours(25)
    gStyle.SetLegendBorderSize(0)
  
    hist.GetXaxis().SetTitle("#rho")
    hist.GetYaxis().SetTitle("p_{T} [GeV]")
    if('n2' in map_name.lower()):
        hist.GetZaxis().SetTitle("N2^{DDT} X% quantile")
    else:
        hist.GetZaxis().SetTitle("DeepBoosted WvsQCD X% quantile")
        disc_max=1
    hist.GetXaxis().SetRangeUser(rho_min, rho_max)
    hist.GetYaxis().SetRangeUser(pt_min, pt_max)
    # if(disc_max>hist.GetMaximum()):
    #     hist.GetZaxis().SetRangeUser(disc_min, disc_max)

    Font=43
    TitleSize=24.0
    TitleOffset=1.3
    LabelSize=18.0
    hist.GetYaxis().SetTitleFont(Font)
    hist.GetYaxis().SetTitleSize(TitleSize)
    hist.GetYaxis().SetTitleOffset(TitleOffset)
    hist.GetYaxis().SetLabelFont(Font)
    hist.GetYaxis().SetLabelSize(LabelSize)

    hist.GetXaxis().SetTitleFont(Font)
    hist.GetXaxis().SetTitleSize(TitleSize)
    hist.GetXaxis().SetTitleOffset(TitleOffset)
    hist.GetXaxis().SetLabelFont(Font)
    hist.GetXaxis().SetLabelSize(LabelSize)
    
    hist.GetZaxis().SetTitleFont(Font)
    hist.GetZaxis().SetTitleSize(TitleSize)
    hist.GetZaxis().SetTitleOffset(TitleOffset)
    hist.GetZaxis().SetLabelFont(Font)
    hist.GetZaxis().SetLabelSize(LabelSize)
    
    # hist.GetZaxis().SetNdivisions(20)
    
    hist.SetTitle(map_name.replace('_',' '))
    hist.SetTitleFont(43)
    hist.SetTitleSize(18.0)
	
    # isomasses = [20,55,80,120,200]
    # isomasses = [20,65,80,125,200]
    # isomasses = range(40,200,20)
    isomasses = [40,80,110,120,200]
    str_isomass = "%.2f*TMath::Exp(-x/2)"
    tf1_isomasses = []
    for i in range(len(isomasses)):
        msd = isomasses[i]
        new_isomass = TF1('isomass_%i'%int(msd),str_isomass%msd,rho_min,rho_max)
        # new_isomass.SetLineColor(920+i)
        new_isomass.SetLineColorAlpha(1,0.4)
        tf1_isomasses.append(new_isomass)


    c1 = TCanvas("c1","c1",700,600)
    c1.cd()
    hist.Draw("colz")
    latex_border = TLatex()
    latex_border.SetNDC(1)
    latex_border.SetTextColor(1)
    latex_border.SetTextFont(43)
    latex_border.SetTextSize(15.5)
    latex_border.SetTextAngle(297)
    latex = TLatex()
    latex.SetNDC(1)
    latex.SetTextColor(920)
    latex.SetTextFont(43)
    latex.SetTextSize(15)
    # latex.SetTextAngle(297)
    for i in range(len(isomasses)):
        x_pitch = (1-left_margin-right_margin)/(rho_max-rho_min)
        y_pitch = (1-bottom_margin-top_margin)/(pt_max-pt_min)
        msd = isomasses[i]
        pt=msd*np.exp(-rho_min/2)
        pt = 800 if pt > pt_max else pt
        angle = ((180/np.pi)*np.arctan(2*x_pitch/(pt*y_pitch)))+272
        latex.SetTextAngle(angle)
        latex_border.SetTextAngle(angle)
        tf1_isomass = tf1_isomasses[i]
        tf1_isomass.Draw('SAME')
        x_pos = left_margin+((2*np.log(msd/pt)-rho_min))*x_pitch+0.01
        y_pos = bottom_margin+(pt-pt_min)*y_pitch +0.01
        latex_border.DrawLatex(x_pos,y_pos,'m_{SD} = %.1f GeV'%msd)
        # latex.DrawLatex(x_pos,y_pos,'m_{SD} = %.1f GeV'%msd)
    c1.SaveAs(out_file_path+".pdf")
    c1.SaveAs(out_file_path+".png")
    c1.SaveAs(out_file_path+".C")
    del c1


if __name__ == "__main__":
    # f1 = TFile('maps/QCD_2017_smooth_gaus10p00sigma.root')
    # hist1 = f1.Get('N2_v_pT_v_rho_0p05_smooth_gaus10p00sigma_maps_cleaner')
    # f1 = TFile('maps_test/QCD_2017_smooth_gaus4p00sigma.root')
    # hist1 = f1.Get('N2_v_pT_v_rho_0p05_smooth_gaus4p00sigma_maps_cleaner')
    # f2 = TFile('maps_test/QCD_2017_NAK8Pt500_smooth_gaus4p00sigma.root')
    # hist2 = f2.Get('N2_v_pT_v_rho_0p05_smooth_gaus4p00sigma_maps_NAK8_Pt500')
    f1 = TFile('maps/QCD_2017.root')
    hist1 = f1.Get('N2_v_pT_v_rho_0p05_maps_cleaner')
    f2 = TFile('old_maps_withoutFallback/maps_test/QCD_2017.root')
    hist2 = f2.Get('N2_v_pT_v_rho_0p05_maps_cleaner')

    hist3 = hist1.Clone()
    hist3.Add(hist2,-1.)
    
    plot_map('N2_ddt_withMwithoutFallback',hist3)
