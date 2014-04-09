// This macro is to be run using `root -q -b drawHeatmaps.C+`
// Note: the ./plots/ directory must exist!

// rootools can be found in ~nsmith/src/rootools
// It's just a small collection of useful utilities
#include "rootools.h"

#include <memory>
#include "TCanvas.h"
#include "TH2F.h"
#include "TStyle.h"


void drawHeatmaps() {
   gStyle->SetOptStat(0);
   TCanvas * c = new TCanvas();
	
   TFile * heatmapfile = new TFile("electronHeatmap.root");

   auto keys = rootools::getKeysofClass(heatmapfile, "analyzer", "TH2F");
   auto heatmaps = rootools::loadObjectsMatchingPattern<TH2F>(keys, "heatmap*");

   for(auto heatmap : heatmaps) {
      c->Clear();
      heatmap->Draw("colz");
      c->Print((std::string("plots/")+heatmap->GetName()+".png").c_str());
   }
}
