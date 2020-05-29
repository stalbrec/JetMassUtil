from __future__ import print_function
import os, ROOT
import numpy as np

HistDir = "../../Histograms/test/"
if(not os.path.exists(HistDir)):
    os.makedirs(HistDir)
PlotDir = "../../Plots/"


class MassScaleGrid:
    def __init__(self,name,config):
        self.ptbins = np.array(config['ptbins'])
        self.etabins = np.array(config['etabins'])
        self.pfflavours = np.array(config['pfflavours'])
        self.Npt = len(self.ptbins)-1
        self.Neta = len(self.etabins)-1
        self.Npfflavours = len(self.pfflavours)
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
        varied_grids = [self.h_grid.Clone('grid_fit'+cat for cat in self.pfflavours)]
        
        parnames = []
        pars = []
        for i in range(self.Npt):
            for j in range(self.Neta):
                for k in range(self.Npfflavours):
                    parameter_name = "massScale_"
                    parameter_name += "pt" + str(i)
                    parameter_name += "_eta" + str(j)
                    parameter_name += "_" + self.pfflavours[k]
                    double central = 0.0;
                    
                    if((i==variation[0] or variation[0]<0) and (j==variation[1] or variation[1]<0) and variation[2]==self.pfflavours[k]):
                        central = 1.+effect
                    bincont = 1.0 + central*variation_scale
                    varied_grids[k]->SetBinContent(i+1,j+1,bincont)
                    parnames.push_back(parameter_name)
                    pars.push_back(central)
        outputFile = ROOT.TFile(HistDir + "/grid_"+name+".root","recreate")
        outputFile->cd()
        for grid in varied_grids:
            grid.Write("grid_fit_"+self.pfflavours[k])
        self.h_categories->Write("categories")

        #ToDo: below is WIP
        #the rest just saves a plot at some points
        g = ROOT.TGraph(len(pars))
        for i in range(len(pars)):
            g.SetPoint(i, i+0.5, pars[i])
        frame = ROOT.TH1F("frame", " ", len(parnames), 0, len(parnames))
        frame.GetYaxis().SetRangeUser(-2, 2)
        for i in range(len(parnames)):
            frame.GetXaxis().SetBinLabel(i+1, parnames[i])
        c = ROOT.TCanvas("c", "c", 800, 600);
        ROOT.gPad.SetBottomMargin(.2);
        ROOT.gPad.SetRightMargin(.2);
        frame.SetFillColor(kWhite);
        frame.Draw();
        g.SetMarkerColor(kBlack);
        g->SetMarkerStyle(8);
        g->SetMarkerSize(1);
        g->Draw("P SAME");

        g->Write("params_graph");
        c->Write("params");
        outputFile->Close();
        cout << "Created ../Histograms/grid_"+var+".root" << endl;

        PlotInputParameters(g, parname, var);

                    
        
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
        }
    }

    for name,config in grids.items():
        this_grid = MassScaleGrid(name,config)
        this_grid.write_grid()
        this_grid.write_varied_grid(0.1,'up')
