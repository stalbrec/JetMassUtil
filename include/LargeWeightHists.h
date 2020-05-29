#pragma once

#include "UHH2/core/include/Hists.h"
#include <TString.h>


using namespace std;

class LargeWeightHists: public uhh2::Hists {
public:
  LargeWeightHists(uhh2::Context & ctx, const std::string & dirname);

  virtual void fill(const uhh2::Event & ev) override;
  virtual ~LargeWeightHists();

private:
	bool isMC;
};
