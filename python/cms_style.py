import ROOT
ROOT.gROOT.SetBatch(True)

color_list = [857,629,797,414,434,885,905,805,394,835,862,595,880,615,627,803,402,927]

colors = {
    'QCD':867,
    'WUnmatched':419,
    'WMatched':413,
    'ZUnmatched':797,
    'ZMatched':800,
    'SingleTop':800,
    'TTbar':810,
    'WJets':413,
    'other':867
}

def cms_style():
    ROOT.gROOT.SetStyle("Plain")
    ROOT.gStyle.SetMarkerSize(2.5)

    cmsStyle = ROOT.TStyle("CMS","CMS approved plots style")

    cmsStyle.SetLegendBorderSize(0)

    cmsStyle.SetFrameBorderMode(0)
    cmsStyle.SetCanvasBorderMode(0)
    cmsStyle.SetPadBorderMode(0)
    cmsStyle.SetPadColor(0)
    cmsStyle.SetCanvasColor(0)
    cmsStyle.SetTitleColor(1)
    cmsStyle.SetStatColor(0)
    cmsStyle.SetFrameFillColor(0)
    
    cmsStyle.SetPaperSize(20,26)
    cmsStyle.SetPadTopMargin(0.055)
    cmsStyle.SetPadRightMargin(0.055)
    cmsStyle.SetPadBottomMargin(0.15)
    cmsStyle.SetPadLeftMargin(0.15)
    
    # cmsStyle.SetTextFont(132)
    cmsStyle.SetTextFont(42)
    cmsStyle.SetTextSize(0.08)
    cmsStyle.SetLabelFont(42,"x")
    cmsStyle.SetLabelFont(42,"y")
    cmsStyle.SetTitleOffset(1.15,"x")
    cmsStyle.SetTitleOffset(1.15,"y")
    cmsStyle.SetLabelFont(42,"z")
    cmsStyle.SetLabelSize(0.04,"x")
    cmsStyle.SetTitleSize(0.05,"x")
    cmsStyle.SetNdivisions(506, "x")
    cmsStyle.SetLabelSize(0.04,"y")
    cmsStyle.SetTitleSize(0.05,"y")
    cmsStyle.SetNdivisions(506, "y")
    cmsStyle.SetLabelSize(0.05,"z")
    cmsStyle.SetTitleSize(0.06,"z")
    cmsStyle.SetNdivisions(506, "z")

    cmsStyle.SetMarkerStyle(8)
    cmsStyle.SetHistLineWidth(2)
    cmsStyle.SetLineStyleString(2,"[12 12]")
    
    cmsStyle.SetOptTitle(0)
    cmsStyle.SetOptStat(0)
    cmsStyle.SetOptFit(0)
    
    cmsStyle.SetPalette(1)
    cmsStyle.SetOptTitle(0)
    
    ROOT.gROOT.SetStyle("Plain")
    ROOT.gROOT.SetStyle("CMS")



obs_draw_option = 'PE1'
draw_option = 'H'

ratio_plot = True
xLabelSize=18.
yLabelSize=18.
xTitleSize=20.
yTitleSize=22.
xTitleOffset=2.8
yTitleOffset=1.5

logX=False
logY=False

yplot=0.7
yratio=0.3
ymax=1.0
xmax=1.0
xmin=0.0

def setup_hist(hist):
    hist.GetYaxis().SetTitleFont(43)
    hist.GetYaxis().SetTitleSize(yTitleSize)
    hist.GetYaxis().SetTitleOffset(yTitleOffset)
    hist.GetYaxis().SetLabelFont(43)
    hist.GetYaxis().SetLabelSize(yLabelSize)
    if(ratio_plot):
        hist.GetXaxis().SetTitleSize(0.0)
        hist.GetXaxis().SetLabelSize(0.0)
    else:
        # hist.GetXaxis().SetTitle(xTitle)
        hist.GetXaxis().SetTitleFont(43)
        hist.GetXaxis().SetTitleSize(xTitleSize)
        hist.GetXaxis().SetTitleOffset(xTitleOffset)
        hist.GetXaxis().SetLabelFont(43)
        hist.GetXaxis().SetLabelSize(xLabelSize)

    # if(YRangeUser):
    #     hist.GetYaxis().SetRangeUser(y_range[0],y_range[1])
    # if(XRangeUser):
    #     hist.GetXaxis().SetRangeUser(x_range[0],x_range[1])
                
def setup_ratio_hist(ratioHist):
  ratioHist.GetYaxis().CenterTitle()
  ratioHist.GetYaxis().SetTitleFont(43)
  ratioHist.GetYaxis().SetTitleSize(yTitleSize)
  ratioHist.GetYaxis().SetTitleOffset(yTitleOffset)
  ratioHist.GetYaxis().SetLabelFont(43)
  ratioHist.GetYaxis().SetLabelSize(yLabelSize)
  ratioHist.GetYaxis().SetNdivisions(506)

  # ratioHist.GetXaxis().SetTitle("m_{SD} [GeV]")
  ratioHist.GetXaxis().SetTitleFont(43)
  ratioHist.GetXaxis().SetTitleSize(xTitleSize)
  ratioHist.GetXaxis().SetTitleOffset(xTitleOffset)
  ratioHist.GetXaxis().SetLabelFont(43)
  ratioHist.GetXaxis().SetLabelSize(xLabelSize)
  ratioHist.GetXaxis().SetTickLength(0.08)
  ratioHist.GetXaxis().SetNdivisions(506)

def setup_pads(c):
    if(ratio_plot):
        plotpad = ROOT.TPad("plotpad","Plot",xmin,ymax-yplot,xmax,ymax)
        ratiopad = ROOT.TPad("ratiopad","Ratio",xmin,ymax-yplot-yratio,xmax,ymax-yplot)
    else:
        plotpad = ROOT.TPad("plotpad","Plot",xmin,ymax-yplot-yratio,xmax,ymax)
        ratiopad = None

    plotpad.SetTopMargin(0.08)
    plotpad.SetLeftMargin(0.14)
    plotpad.SetRightMargin(0.05)
    plotpad.SetTicks()
    plotpad.Draw()
    
    if(ratio_plot):
        plotpad.SetBottomMargin(0.016)
        ratiopad.SetTopMargin(0.016)
        ratiopad.SetBottomMargin(0.35)
        ratiopad.SetLeftMargin(0.14)
        ratiopad.SetRightMargin(0.05)
        ratiopad.SetTicks()
        ratiopad.Draw()
    else:
        plotpad.SetBottomMargin(0.1)
        
    if(logY):
        plotpad.SetLogy()
        c.SetLogy()
    if(logX):
        plotpad.SetLogx()
        if(ratio_plot):
            ratiopad.SetLogx()
        c.SetLogx()
    return plotpad,ratiopad
