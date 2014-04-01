// This macro is to be run using `root -q -b drawRateEff.C+`
// Note: the ./plots/ directory must exist!

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

void drawNewOld(std::vector<TH1F*> newHists, TH1F * oldHist, TCanvas * c, double ymax) {
   oldHist->SetLineColor(kRed);
   if ( ymax != 0. )
      oldHist->SetMaximum(ymax);
   std::string oldTitle = oldHist->GetTitle();
   oldHist->SetTitle("EG Rates");
   for ( auto newHist : newHists ) {
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
   // Fix our title mangling
   oldHist->SetTitle(oldTitle.c_str());
}

void drawSame(std::vector<TH1F*> hists, TCanvas * c, double ymax, std::string name) {
   std::vector<int> colors { kRed, kGreen, kBlue, kBlack, kGray };
   hists[0]->SetMaximum(ymax);
   std::string h0t = hists[0]->GetTitle();
   hists[0]->SetTitle("EG Rates");
   TLegend *leg = new TLegend(0.5,0.7,0.9,0.9);
   setLegStyle(leg);
   hists[0]->SetLineColor(colors[0]);
   hists[0]->Draw();
   leg->AddEntry(hists[0], h0t.c_str(), "l");
   auto col = begin(colors);
   for (auto hist=begin(hists)+1; hist!=end(hists); hist++) {
      (*hist)->SetLineColor(*++col);
      (*hist)->Draw("same");
      leg->AddEntry(*hist, (*hist)->GetTitle(), "l");
   }
   leg->Draw("same");

   c->Print(("plots/"+name).c_str());
   c->Clear();
   delete leg;
}

void drawRateEff() {
   gStyle->SetOptStat(0);
   TCanvas * c = new TCanvas();
	
   TFile * rates = new TFile("egTriggerRates.root");
	TFile * eff = new TFile("egTriggerEff.root");

   auto rateHistKeys = rootools::getKeysofClass(rates, "analyzer", "TH1F");
   auto newAlgRateHists = rootools::loadObjectsMatchingPattern<TH1F>(rateHistKeys, "crystalEG*");
   auto oldAlgRateHist = (TH1F *) rates->Get("analyzer/oldEG_rate");
   oldAlgRateHist->SetTitle("Old L2 Algorithm");

   c->SetLogy(1);
   //c->SetGridx(1);
   //c->SetGridy(1);
   drawNewOld(newAlgRateHists, oldAlgRateHist, c, 40000.);
   // Draw several cuts on same plot (the four corners in search space)
   std::vector<TH1F*> selectedHists{oldAlgRateHist, newAlgRateHists[0], newAlgRateHists[3], newAlgRateHists[12], newAlgRateHists[15]};
   drawSame(selectedHists, c, 40000., "crystalEG_rate_variouscuts.png");

   auto effHistKeys = rootools::getKeysofClass(eff, "analyzer", "TH1F");
   auto newAlgEtaEffHists = rootools::loadObjectsMatchingPattern<TH1F>(effHistKeys, "crystalEG*_eta");
   auto newAlgPtEffHists = rootools::loadObjectsMatchingPattern<TH1F>(effHistKeys, "crystalEG*_pt");
   auto newAlgDRHists = rootools::loadObjectsMatchingPattern<TH1F>(effHistKeys, "crystalEG_deltaR*");
   auto oldAlgEtaHist = (TH1F *) eff->Get("analyzer/oldEG_efficiency_eta");
   auto oldAlgPtHist = (TH1F *) eff->Get("analyzer/oldEG_efficiency_pt");
   auto oldAlgDRHist = (TH1F *) eff->Get("analyzer/oldEG_deltaR");
   c->SetLogy(0);
   drawNewOld(newAlgEtaEffHists, oldAlgEtaHist, c, 1.2);
   drawNewOld(newAlgPtEffHists, oldAlgPtHist, c, 1.2);
   drawNewOld(newAlgDRHists, oldAlgDRHist, c, 0.);

   std::vector<TH1F*> selectedEtaEffHists{oldAlgEtaHist, newAlgEtaEffHists[0], newAlgEtaEffHists[3], newAlgEtaEffHists[12], newAlgEtaEffHists[15]};
   drawSame(selectedEtaEffHists, c, 1.2, "crystalEG_efficiency_variouscuts_eta.png");
   std::vector<TH1F*> selectedPtEffHists{oldAlgPtHist, newAlgPtEffHists[0], newAlgPtEffHists[3], newAlgPtEffHists[12], newAlgPtEffHists[15]};
   drawSame(selectedPtEffHists, c, 1.2, "crystalEG_efficiency_variouscuts_pt.png");
}
