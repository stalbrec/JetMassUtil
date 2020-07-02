import ROOT

ROOT.gStyle.SetOptStat(0)
ROOT.gStyle.SetPadTickY(1)
ROOT.gStyle.SetPadTickX(1)
ROOT.gStyle.SetLegendBorderSize(0)
ROOT.gROOT.SetBatch(True)

def NormalisePerBin(hists):
    h_norm = []
    for h in hists:
        h_norm.append(h.Clone())
    Nbins = 0.
    for ibin in range(1,hists[0].GetXaxis().GetNbins()+1):
        binTotal = 0.
        for h in hists:
            binTotal += h.GetBinContent(ibin)
        for g in h_norm:
            oldContent = g.GetBinContent(ibin)
            if(binTotal == 0):
                g.SetBinContent(ibin, 0)
            else:
                g.SetBinContent(ibin, oldContent/binTotal)
                g.SetBinError(ibin, g.GetBinError(ibin)/binTotal)
    return h_norm

plot_path = "pf_cat_plots_data"
import os
if not os.path.isdir(plot_path):
    os.makedirs(plot_path)
    
f_mc  = ROOT.TFile("/afs/desy.de/user/a/albrechs/xxl/af-cms/UHH2/10_2/CMSSW_10_2_10/src/UHH2/JetMass/Output/WJetsTrees/scaleStudy/PF_flavours/PseudoData.root")
f_data  = ROOT.TFile("/afs/desy.de/user/a/albrechs/xxl/af-cms/UHH2/10_2/CMSSW_10_2_10/src/UHH2/JetMass/Output/WJetsTrees/scaleStudy/PF_flavours/Data.root")
# f  = ROOT.TFile("/afs/desy.de/user/a/albrechs/xxl/af-cms/UHH2/10_2/CMSSW_10_2_10/src/UHH2/JetMass/Output/WJetsTrees/scaleStudy/PF_flavours/Data.root")

hist_dirs = ["PFHists_200to500","PFHists_500to1000","PFHists_1000to2000","PFHists_2000to3000","PFHists_3000to4000","PFHists_4000to5000"]
hist_tex_pseudo = ["200 < p_{T} < 500 ~~ N=4*10^{9}","500 < p_{T} < 1000 ~~ N=4*10^{9}","1000 < p_{T} < 2000","2000 < p_{T} < 3000","3000 < p_{T} < 4000","4000 < p_{T} < 5000"]
hist_tex_data = ["200 < p_{T} < 500","500 < p_{T} < 1000","1000 < p_{T} < 2000","2000 < p_{T} < 3000","3000 < p_{T} < 4000","4000 < p_{T} < 5000"]

for hist_dir in hist_dirs:
    categories = ["other", "gamma", "neutralH", "chargedH"]
    h_eta = []
    h_pt = []
    h_eta_Eweight = []
    h_eta_data = []
    h_pt_data = []
    h_eta_Eweight_data = []
    for cat in categories:
            h_eta.append(f_mc.Get(hist_dir+"/eta_"+cat))
            h_pt.append(f_mc.Get(hist_dir+"/pt_"+cat))
            h_eta_Eweight.append(f_mc.Get(hist_dir+"/eta_Eweight_"+cat))
            h_eta_data.append(f_data.Get(hist_dir+"/eta_"+cat))
            h_pt_data.append(f_data.Get(hist_dir+"/pt_"+cat))
            h_eta_Eweight_data.append(f_data.Get(hist_dir+"/eta_Eweight_"+cat))

    N = sum([h.Integral() for h in h_eta_Eweight])
    h_eta_Eweight_norm = NormalisePerBin(h_eta_Eweight)
    h_eta_Eweight_norm_data = NormalisePerBin(h_eta_Eweight_data)

    s_eta = ROOT.THStack()
    s_eta_norm = ROOT.THStack()
    s_eta_norm_data = ROOT.THStack()
    s_pt = ROOT.THStack()
    col = [13, 798, ROOT.kAzure+7, ROOT.kRed-4]

    for i in range(len(categories)):
        h_eta[i].SetFillColor(col[i])
        s_eta.Add(h_eta[i])
        h_pt[i].SetFillColor(col[i])
        s_pt.Add(h_pt[i])
        h_eta_Eweight_norm[i].SetFillColor(col[i])
        s_eta_norm.Add(h_eta_Eweight_norm[i])
        h_eta_Eweight_norm_data[i].SetLineColor(col[i]+1)
        h_eta_Eweight_norm_data[i].SetMarkerColor(col[i]+1)
        h_eta_Eweight_norm_data[i].SetMarkerStyle(8)
        s_eta_norm_data.Add(h_eta_Eweight_norm_data[i],"P")

    c_pt = ROOT.TCanvas("c_pt","c_pt",600, 600)
    ROOT.gPad.SetLeftMargin(0.16)
    ROOT.gPad.SetBottomMargin(0.14)
    s_pt.Draw("HIST")
    s_pt.GetXaxis().SetTitle("p_{T}")
    s_pt.GetYaxis().SetTitle("PF particles")
    s_pt.GetYaxis().SetTitleOffset(1.6)
    s_pt.GetXaxis().SetTitleOffset(1.1)
    s_pt.GetYaxis().SetTitleSize(0.05)
    s_pt.GetXaxis().SetTitleSize(0.05)
    s_pt.GetYaxis().SetLabelSize(0.05)
    s_pt.GetXaxis().SetLabelSize(0.05)
    s_pt.GetYaxis().SetNdivisions(505)
    s_pt.GetXaxis().SetRangeUser(0, 20)
    s_pt.SetMaximum(s_pt.GetMaximum()*1.3)
    l_pt = ROOT.TLegend(0.64,0.65,0.86,0.85)
    l_pt.SetBorderSize(0)
    l_pt.SetFillStyle(0)
    for i in reversed(range(len(categories))):
        l_pt.AddEntry(h_pt[i], categories[i],"f")
    l_pt.SetTextSize(0.04)
    l_pt.Draw()
    c_pt.SaveAs(plot_path+"/PFcategories_pt_ptbin%s.pdf"%(hist_dir.split('_')[-1]))

    c_eta = ROOT.TCanvas("c_eta","c_eta",600, 600)
    ROOT.gPad.SetLeftMargin(0.16)
    ROOT.gPad.SetBottomMargin(0.14)
    s_eta.Draw("HIST")
    s_eta.GetXaxis().SetTitle("#eta")
    s_eta.GetYaxis().SetTitle("PF particles")
    s_eta.GetYaxis().SetTitleOffset(1.6)
    s_eta.GetXaxis().SetTitleOffset(1.1)
    s_eta.GetYaxis().SetTitleSize(0.05)
    s_eta.GetXaxis().SetTitleSize(0.05)
    s_eta.GetYaxis().SetLabelSize(0.05)
    s_eta.GetXaxis().SetLabelSize(0.05)
    s_eta.GetYaxis().SetNdivisions(505)
    s_eta.GetXaxis().SetRangeUser(-3, 3)
    s_eta.SetMaximum(s_eta.GetMaximum()*1.3)
    l_eta = ROOT.TLegend(0.64,0.65,0.86,0.85)
    l_eta.SetBorderSize(0)
    l_eta.SetFillStyle(0)
    for i in reversed(range(len(categories))):
        l_eta.AddEntry(h_eta[i], categories[i],"f")
    l_eta.Draw()
    c_eta.SaveAs(plot_path+"/PFcategories_eta_ptbin%s.pdf"%(hist_dir.split('_')[-1]))

    c_eta_norm = ROOT.TCanvas("c_eta_norm","c_eta_norm",600, 600)
    ROOT.gPad.SetLeftMargin(0.16)
    ROOT.gPad.SetBottomMargin(0.14)
    s_eta_norm.Draw("HIST")
    s_eta_norm.GetXaxis().SetTitle("#eta")
    s_eta_norm.GetYaxis().SetTitle("energy fraction")
    s_eta_norm.GetYaxis().SetTitleOffset(1.6)
    s_eta_norm.GetXaxis().SetTitleOffset(1.1)
    s_eta_norm.GetYaxis().SetTitleSize(0.05)
    s_eta_norm.GetXaxis().SetTitleSize(0.05)
    s_eta_norm.GetYaxis().SetLabelSize(0.05)
    s_eta_norm.GetXaxis().SetLabelSize(0.05)
    s_eta_norm.GetYaxis().SetNdivisions(505)
    s_eta_norm.GetXaxis().SetRangeUser(-3, 3)
    s_eta_norm.SetMaximum(s_eta_norm.GetMaximum())
    s_eta_norm_data.Draw("SAME")
    l_eta_norm = ROOT.TLegend(0.64,0.65,0.86,0.85)
    l_eta_norm.SetBorderSize(0)
    l_eta_norm.SetFillStyle(0)
    for i in reversed(range(len(categories))):
        l_eta_norm.AddEntry(h_eta_Eweight_norm[i], categories[i],"f")
    latex = ROOT.TLatex()
    latex.SetNDC(1)
    latex.SetTextSize(0.04)
    l_eta_norm.Draw()
    print(" %s GeV #leq p_{T} < %s GeV N=%.2e"%(hist_dir.split('_')[-1].split('to')[0],hist_dir.split('_')[-1].split('to')[1],N))
    latex.DrawLatex(0.20,0.95," %s GeV #leq p_{T} < %s GeV N=%.2e"%(hist_dir.split('_')[-1].split('to')[0],hist_dir.split('_')[-1].split('to')[1],N))
    c_eta_norm.SaveAs(plot_path+"/PFcategories_eta_norm_ptbin%s.pdf"%(hist_dir.split('_')[-1]))

