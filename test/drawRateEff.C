// This macro is to be run using `root -q -b drawRateEff.C+`

// rootools can be found in ~nsmith/src/rootools
// It's just a small collection of useful utilities
#include "rootools.h"
#include "TCanvas.h"
#include "TH1F.h"
#include "TLegend.h"
#include "TStyle.h"

void setLegStyle(TLegend * leg) {
   leg->SetBorderSize(0);
   leg->SetLineColor(1);
   leg->SetLineStyle(1);
   leg->SetLineWidth(.3);
   leg->SetFillColor(0);
   leg->SetFillStyle(0);
}

void drawNewOld(std::vector<TH1F*> newHists, TH1F * oldHist, TCanvas * c) {
   for ( auto newHist : newHists ) {
      oldHist->SetLineColor(kRed);
      oldHist->Draw();
      newHist->Draw("same");
      TLegend *leg = new TLegend(0.4,0.8,0.9,0.9);
      setLegStyle(leg);
      leg->AddEntry(oldHist, "Old L2 Algorithm","l");
      leg->AddEntry(newHist, newHist->GetTitle(),"l");
      leg->Draw("same");

      c->Print(("plots/"+std::string(newHist->GetName())+".png").c_str());
      delete leg;
   }
}


void drawRateEff() {
   gStyle->SetOptStat(0);
   TCanvas * c = new TCanvas();
	
   TFile * rates = new TFile("egTriggerRates.root");
	TFile * eff = new TFile("egTriggerEff.root");

   auto rateHistKeys = rootools::getKeysofClass(rates, "analyzer", "TH1F");
   auto newAlgRateHists = rootools::loadObjectsMatchingPattern<TH1F>(rateHistKeys, "crystalEG*");
   auto oldAlgRateHist = (TH1F *) rates->Get("analyzer/oldEG_rate");

   c->SetLogy(1);
   c->SetGridx(1);
   c->SetGridy(1);
   drawNewOld(newAlgRateHists, oldAlgRateHist, c);

   auto effHistKeys = rootools::getKeysofClass(eff, "analyzer", "TH1F");
   auto newAlgEtaEffHists = rootools::loadObjectsMatchingPattern<TH1F>(effHistKeys, "crystalEG*_eta");
   auto newAlgPtEffHists = rootools::loadObjectsMatchingPattern<TH1F>(effHistKeys, "crystalEG*_pt");
   auto oldAlgEtaHist = (TH1F *) eff->Get("analyzer/oldEG_eff_eta");
   auto oldAlgPtHist = (TH1F *) eff->Get("analyzer/oldEG_eff_pt");
   c->SetLogy(0);
   drawNewOld(newAlgEtaEffHists, oldAlgEtaHist, c);
   drawNewOld(newAlgPtEffHists, oldAlgPtHist, c);
}
