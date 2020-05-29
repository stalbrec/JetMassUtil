from __future__ import print_function

import os, ROOT
ROOT.TH1.AddDirectory(False)
ROOT.gStyle.SetPadTickY(1)
ROOT.gStyle.SetPadTickX(1)

import cms_style
cms_style.cms_style()

import numpy as np

HistDir = "../../Histograms/"
if(not os.path.exists(HistDir)):
    os.makedirs(HistDir)
PlotDir = "../../Plots/"
if(not os.path.exists(PlotDir)):
    os.makedirs(PlotDir)


class MassScaleGrid:
    def __init__(self,name,config):
        self.ptbins = np.array(config['ptbins'])
        self.etabins = np.array(config['etabins'])
        self.pfflavours = np.array(config['pfflavours'])
        self.Npt = len(self.ptbins)-1
        self.Neta = len(self.etabins)-1
        self.Npfflavours = len(self.pfflavours)
        self.grid_name = name
        self.filename = HistDir+'grid_'+name+'.root'

        self.h_grid = ROOT.TH2F("grid", "x=pt, y=eta", self.Npt, self.ptbins, self.Neta, self.etabins)
        self.h_categories = ROOT.TH1F("categories", "categories", self.Npfflavours, 0, self.Npfflavours)
        for i in range(self.Npfflavours):
            self.h_categories.GetXaxis().SetBinLabel(i+1, self.pfflavours[i])

    def write_grid(self):
        grid_file = ROOT.TFile(self.filename,'recreate')
        grid_file.cd()
        self.h_grid.Write("grid")
        self.h_categories.Write("categories")
        grid_file.Close()

    def write_varied_grid(self,name,variation,effect,variation_scale=0.1):
        varied_grids = [self.h_grid.Clone('grid_fit'+cat) for cat in self.pfflavours]
        
        parnames = []
        pars = []
        for i in range(self.Npt):
            for j in range(self.Neta):
                for k in range(self.Npfflavours):
                    parameter_name = "massScale_"
                    parameter_name += "pt" + str(i)
                    parameter_name += "_eta" + str(j)
                    parameter_name += "_" + self.pfflavours[k]
                    central = 0.0;
                    
                    if( ( self.Npt == 1 or variation[0] is None or i in variation[0] ) and ( self.Neta == 1 or variation[1] is None or j in variation[1] ) and (variation[2]=='all' or self.pfflavours[k] in variation[2]) ):
                        central = effect
                    bincont = 1.0 + central*variation_scale
                    varied_grids[k].SetBinContent(i+1,j+1,bincont)
                    parnames.append(parameter_name)
                    pars.append(central)
        outputFile = ROOT.TFile(HistDir + "/grid_"+self.grid_name+'_'+name+".root","recreate")
        outputFile.cd()
        for grid in varied_grids:
            grid.Write("grid_fit_"+self.pfflavours[k])
        self.h_categories.Write("categories")
        
        g = ROOT.TGraph(len(pars))
        for i in range(len(pars)):
            g.SetPoint(i, i+0.5, pars[i])
        frame = ROOT.TH1F("frame", " ", len(parnames), 0, len(parnames))
        frame.GetYaxis().SetRangeUser(-2, 2)
        frame.GetYaxis().SetTitleOffset(0.3)
        frame.GetYaxis().SetTitle("#sigma")
        frame.GetYaxis().CenterTitle()
        
        for i in range(len(parnames)):
            frame.GetXaxis().SetBinLabel(i+1, parnames[i])
        c = ROOT.TCanvas("c", "c", 2000, 600)
        ROOT.gPad.SetBottomMargin(.2)
        ROOT.gPad.SetRightMargin(.08)
        ROOT.gPad.SetLeftMargin(.04)
        frame.SetFillColor(ROOT.kWhite)
        frame.Draw()
        g.SetMarkerColor(ROOT.kBlack)
        g.SetMarkerStyle(8)
        g.SetMarkerSize(1)
        g.Draw("P SAME")

        g.Write("params_graph")
        c.Write("params")
        c.SaveAs(PlotDir+'/Nuisance_Input_'+self.grid_name+'_'+name+'.pdf')
        outputFile.Close()
                    
        
if(__name__ == "__main__"):
    grids = {
        "oneScale":{
            "ptbins":[0.,100000.],
            "etabins":[0.,9.],
            "pfflavours":["all"]
        },
        "PF_flavours":{
            "ptbins":[0.,100000.],
            "etabins":[0.,9.],
            "pfflavours":["chargedH", "neutralH", "gamma", "other"]
        },
        "2ptbins":{
            "ptbins":[0.,10.,100000.],
            "etabins":[0.,9.],
            "pfflavours":["all"]
        },
        "2etabins":{
            "ptbins":[0.,100000.],
            "etabins":[0., 1.479, 9.],
            "pfflavours":["all"]
        },
        "PF_flavours_2ptbins":{
            "ptbins":[0.,10.,100000.],
            "etabins":[0., 9.],
            "pfflavours":["chargedH", "neutralH", "gamma", "other"]
        },
        "PF_flavours_2etabins":{
            "ptbins":[0.,100000.],
            "etabins":[0., 1.479, 9.],
            "pfflavours":["chargedH", "neutralH", "gamma", "other"]
        },
        "oldBinning":{
            "ptbins":[0,10.,50.],
            "etabins":[0.,0.522,1.305,5.191],
            "pfflavours":["chargedH", "neutralH", "gamma", "other"]            
        },
        "threePtbins":{
            "ptbins":[0,10.,50.,100.],
            "etabins":[0.,0.522,1.305,5.191],
            "pfflavours":["chargedH", "neutralH", "gamma", "other"]            
        }
    }

    for name,config in grids.items():
        this_grid = MassScaleGrid(name,config)
        this_grid.write_grid()
        this_grid.write_varied_grid("all1UP",(None,None,"all"),1.)
        this_grid.write_varied_grid("all1p5DOWN",(None,None,"all"),-1.5)
        this_grid.write_varied_grid("chH_pt02_eta0_1p5DOWN",([0,2],[0],["chargedH","other"]),-1.5)
        
