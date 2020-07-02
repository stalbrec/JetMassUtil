#!/usr/bin/env python
from __future__ import print_function
import os,argparse

def exec_bash(command='echo "hello world"',debug=False):
    print(command)
    if(not debug):
        os.system(command)
    return """%s\n"""%command


rMIN=-1.5
rMAX=1.5

class CombineWorkflows:
    def __init__(self):
        print('Nothing to do here. This class is just a wrapper for some worflow methods using combine')
        self.methods = [func for func in dir(CombineWorkflows) if callable(getattr(CombineWorkflows, func))]        
        self.methods.remove('__init__')
        
        
    def diagnostics(self,args,debug=True):
        command_string = """#FitDiagnostics Workflow\n"""
        command_string += exec_bash("combine -M FitDiagnostics {WORKSPACE} --redefineSignalPOIs {POI} --setParameterRange {POI}={MIN},{MAX}".format(WORKSPACE=args.workspace,POI=args.POI,MIN=rMIN,MAX=rMAX),debug)
        command_string += exec_bash("PostFitShapesFromWorkspace -w {WORKSPACE} -o {MODELDIR}fit_shapes.root --postfit --sampling -f {MODELDIR}fitDiagnostics.root:fit_s".format(WORKSPACE=args.workspace,MODELDIR=args.model_dir),debug)

        return command_string
            

    def scan(self,args,debug=True):
        command_string="""#Scanning Workflow"""
        NPOINTS=50
        YMAX=14
        YCUT=50
        POI=args.POI
        # POI=""
        # POI="r"
        fitPOI=""
        plotPOI=""
        RANGE="--rMin %.2f --rMax %.2f"%(rMIN,rMAX)
        
        # POI="massScale_pt0_eta0_all"
        if POI is not  "r":
            fitPOI="--redefineSignalPOIs %s"%POI
            plotPOI="--POI %s"%POI
            RANGE="--setParameterRanges %s=%.2f,%.2f"%(POI,rMIN,rMAX)

        from collections import OrderedDict 

        # freezeParams={
        #     'freezeWqqNorm':['WJets_normUnc',2],
        #     'freezeZqqNorm':['ZJets_normUnc',3]
        # }
        freezeParams=OrderedDict()

        freezeParams['QCD3_2']=['qcdparam_ptbin3_msdbin2',7]
        freezeParams['QCD2_2']=['qcdparam_ptbin2_msdbin2',6]
        freezeParams['QCD1_2']=['qcdparam_ptbin1_msdbin2',5]
        freezeParams['QCD0_2']=['qcdparam_ptbin0_msdbin2',4]
        freezeParams['QCD0_12']=['qcdparam_ptbin0_msdbin12',3]
        freezeParams['QCD1_14']=['qcdparam_ptbin1_msdbin14',2]
            
            
        OUTPUTNAME="50points_massScalePOI_freezeQCDParam_m10To10"
    

        snapshot_suffix =  "snapshot"
        if(not args.justplots):
            print("fitting nominal model to use as snapshot")
            command_string += exec_bash("combine -M MultiDimFit {WORKSPACE} -n .{SNAPSHOT} -m 0 --saveWorkspace {POI} {RANGE}".format(WORKSPACE=args.workspace,SNAPSHOT=snapshot_suffix,POI=fitPOI,RANGE=RANGE),debug)
    

        multi_dim_fit_scan = "combine -M MultiDimFit higgsCombine.{SNAPSHOT}.MultiDimFit.mH0.root -m 0 -n .{NAME} {RANGE} --algo grid --points {NPOINTS} --snapshotName MultiDimFit --skipInitialFit {POI} {FREEZE}"
        nominal_name = "AllFloating"
        if(not args.justplots):
            print("perfoming scan without freezed nuisances")
            command_string += exec_bash(multi_dim_fit_scan.format(SNAPSHOT=snapshot_suffix,NAME=nominal_name,RANGE=RANGE,NPOINTS=NPOINTS,POI=fitPOI,FREEZE=""),debug)

        others_string=""
        breakdown_string=""
        for name,freezeSetting in freezeParams.items(): 
            if(not args.justplots):
                print("perfoming scan param "+name+" freezed:")
                command_string += exec_bash(multi_dim_fit_scan.format(SNAPSHOT=snapshot_suffix,NAME=name,RANGE=RANGE,NPOINTS=NPOINTS,POI=fitPOI,FREEZE="--freezeParameters "+freezeSetting[0]),debug)
            others_string += "higgsCombine.{SUFFIX}.MultiDimFit.mH0.root:{NAME}:{COLOR} ".format(SUFFIX=name,NAME=freezeSetting[0],COLOR=freezeSetting[1])
            breakdown_string += name+","
        breakdown_string += "Rest"

        print("plotting results")

        plotting_command = "python ../plot1DScan.py higgsCombine.{NOMINAL}.MultiDimFit.mH0.root --others {OTHERS} -o {OUTPUTNAME} --breakdown {BREAKDOWN} --y-max {YMAX} --y-cut {YCUT} {POI}"
        command_string += exec_bash(plotting_command.format(NOMINAL=nominal_name,OTHERS=others_string,OUTPUTNAME=OUTPUTNAME,BREAKDOWN=breakdown_string,YMAX=YMAX,YCUT=YCUT,POI=plotPOI),debug)
        return command_string

    
    def impact(self,args,debug=True):
        command_string = """#Impact Workflow\n"""
        if(not args.justplots):
            command_string += exec_bash("combineTool.py -M Impacts -d {WORKSPACE} -m 0 --robustFit 1 --doInitialFit --redefineSignalPOIs {POI}".format(WORKSPACE=args.workspace,POI=args.POI),debug)
            command_string += exec_bash("combineTool.py -M Impacts -d {WORKSPACE} -m 0 --robustFit 1 --doFits --redefineSignalPOIs {POI} --parallel {NWORKERS}".format(WORKSPACE=args.workspace,POI=args.POI,NWORKERS=args.workers),debug)
            command_string += exec_bash("combineTool.py -M Impacts -d {WORKSPACE} -m 0 -o {OUTPUT} --redefineSignalPOIs {POI}".format(WORKSPACE=args.workspace,POI=args.POI,OUTPUT=args.workspace.replace('_combined','').replace('.root','_impacts.json')),debug)
            command_string += exec_bash("mkdir impact_fits;mv *paramFit* impact_fits")
        command_string += exec_bash("plotImpacts.py -i {NAME}_impacts.json -o {NAME}_impacts".format(NAME=args.workspace.replace('_combined','').replace('.root','')),debug)

        return command_string
        
        
if(__name__=='__main__'):
    parser = argparse.ArgumentParser()
    parser.add_argument('--justplots',action="store_true")
    parser.add_argument('--debug',action="store_true")
    parser.add_argument('--method',type=str,choices=globals()['CombineWorkflows']().methods,required=True)
    parser.add_argument('--POI',default="massScale_pt0_eta0_all")
    parser.add_argument('--workspace','-w',default = 'WJetsOneScale_combined.root')
    parser.add_argument('--workers','-n',default=5)
    args = parser.parse_args()

    if(not os.path.isfile(args.workspace)):
        raise IOError('Could not find workspace file')
    
    args.model_dir=os.path.abspath('/'.join(args.workspace.split('/')[:-1])+'/') if '/' in args.workspace else ''


    print('workspace',args.workspace)
    print('model_dir',args.model_dir)
    print('using method',args.method)
    method = getattr(globals()['CombineWorkflows'](),args.method)
    command_string = method(args,args.debug)

    if(args.debug):
        print()
        print()
        print(command_string)

    
    
    

    
