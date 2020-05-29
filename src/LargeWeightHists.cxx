#include "UHH2/JetMass/include/LargeWeightHists.h"
#include "UHH2/core/include/Event.h"
#include "UHH2/common/include/PartonHT.h"
#include "UHH2/common/include/Utils.h"

#include "TH1F.h"
#include <iostream>

using namespace std;
using namespace uhh2;

LargeWeightHists::LargeWeightHists(Context & ctx, const string & dirname): Hists(ctx, dirname){
  auto dataset_type = ctx.get("dataset_type");
  isMC = dataset_type == "MC";
  auto version = ctx.get("dataset_version");
  book<TH1F>("recoJetGenHTRatio","recoJetGenHTRatio",100,0,10);
  book<TH1F>("genJetGenHTRatioMax","genJetGenHTRatioMax",100,0,10);

  book<TH1F>("recoJetQScaleRatioMax","recoJetQScaleRatioMax",100,0,10);

  book<TH1F>("PUpTHatGenHTRatioMax","PUpTHatGenHTRatioMax",100,0,10);

  book<TH1F>("recoJetpTHatRatioMax","recoJetpTHatRatioMax",100,0,10);
  book<TH1F>("genJetpTHatRatioMax","genJetpTHatRatioMax",100,0,10);

}

void LargeWeightHists::fill(const Event & event){
  auto weight = event.weight;
  assert(event.genparticles);
  float genHT = PartonHT::calculate(*event.genparticles);
  auto recoJets = *event.jets;
  sort_by_pt(recoJets);
  bool hasRecoJets = recoJets.size() > 0;
  float recoJetPt = (hasRecoJets) ? recoJets[0].pt() : 0.;
  auto genJets = *event.genjets;
  sort_by_pt(genJets);
  bool hasGenJets = genJets.size() > 0;
  float genJetPt = (hasGenJets) ? genJets[0].pt() : 0.;
  // Check ratio of jet pT / gen HT

  if ((genHT > 0) && hasRecoJets) hist("recoJetGenHTRatio")->Fill(recoJetPt / genHT, weight);
  if ((genHT > 0) && hasGenJets) hist("genJetGenHTRatioMax")->Fill(genJetPt / genHT, weight);


  // Check ratio of jet pT / Q scale
  float qScale = event.genInfo->qScale();
  if ((qScale > 0) && hasRecoJets) hist("recoJetQScaleRatioMax")->Fill(recoJetPt / qScale,weight);


  // Check ratio of pileup maximum pTHat / gen HT (i.e. is the scale of PU > hard event?)
  float PU_pThat = event.genInfo->PU_pT_hat_max();
  if ((genHT > 0))hist("PUpTHatGenHTRatioMax")->Fill(PU_pThat / genHT,weight);
  // Check event weight is sensible based on pthat - but isn't always available
  // e.g. exists for Pythia pT-binned, but not HT-binned


  if (event.genInfo->binningValues().size() > 0) {
      double ptHat = event.genInfo->binningValues().at(0); // yes this is correct. no idea why
      if ((ptHat > 0) && hasRecoJets)hist("recoJetpTHatRatioMax")->Fill( recoJetPt / ptHat, weight);
      if ((ptHat > 0) && hasGenJets)hist("genJetpTHatRatioMax")->Fill(genJetPt / ptHat, weight);
  }

}

LargeWeightHists::~LargeWeightHists(){}
