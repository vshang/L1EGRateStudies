// This macro is to be run using `root -q -b drawRateEff.C+`
// Note: the ./plots/ directory must exist!

// rootools can be found in ~nsmith/src/rootools
// It's just a small collection of useful utilities
#include "rootools.h"

#include <memory>
#include "TCanvas.h"
#include "TH1F.h"
#include "TLegend.h"
#include "TStyle.h"
#include "TGraph.h"
#include "TMultiGraph.h"

void setLegStyle(TLegend * leg) {
   leg->SetBorderSize(0);
   leg->SetLineColor(1);
   leg->SetLineStyle(1);
   leg->SetLineWidth(.3);
   leg->SetFillColor(0);
   leg->SetFillStyle(0);
}

void drawNewOld(std::vector<TH1F*> newHists, TH1F * oldHist, TCanvas * c, double ymax) {
   c->Clear();
   TGraph * oldGraph = new TGraph((TH1 *) oldHist);
   oldGraph->SetLineColor(kRed);
   oldGraph->SetMarkerColor(kRed);
   oldGraph->SetMarkerStyle(20);
   std::string oldTitle = oldHist->GetTitle();

   TMultiGraph mg("mg", "EG Rates");
   mg.Add(oldGraph);
   for ( auto newHist : newHists ) {
      auto g = new TGraph((TH1 *) newHist);
      g->SetMarkerStyle(21);
      mg.Add(g);
      mg.Draw("apl");
      if ( c->GetLogy() == 0 ) // linear
         mg.SetMinimum(0.);
      if ( ymax != 0. )
         mg.SetMaximum(ymax);
      TLegend *leg = new TLegend(0.5,0.8,0.9,0.9);
      setLegStyle(leg);
      leg->AddEntry(oldGraph, "Old L2 Algorithm","lp");
      leg->AddEntry(newHist, newHist->GetTitle(),"lp");
      leg->Draw("same");
      mg.GetXaxis()->SetTitle(oldHist->GetXaxis()->GetTitle());
      mg.GetYaxis()->SetTitle(oldHist->GetYaxis()->GetTitle());

      c->Print(("plots/"+std::string(newHist->GetName())+".png").c_str());
      delete leg;
      mg.RecursiveRemove(g);
      delete g;
   }
}

void drawSame(std::vector<TH1F*> hists, TCanvas * c, double ymax, std::string name) {
   std::vector<int> colors { kRed, kGreen, kBlue, kBlack, kGray };
   if ( ymax != 0. )
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
   rootools::drawMulti(selectedHists, c, "EG Fake Rates", "plots/crystalEG_rate_variouscuts.png", {0.5, 0.7, 0.9, 0.9});

   auto effHistKeys = rootools::getKeysofClass(eff, "analyzer", "TH1F");
   auto newAlgEtaEffHists = rootools::loadObjectsMatchingPattern<TH1F>(effHistKeys, "crystalEG*_eta");
   auto newAlgPtEffHists = rootools::loadObjectsMatchingPattern<TH1F>(effHistKeys, "crystalEG*_pt");
   auto newAlgDRHists = rootools::loadObjectsMatchingPattern<TH1F>(effHistKeys, "crystalEG_deltaR*");
   auto oldAlgEtaHist = (TH1F *) eff->Get("analyzer/oldEG_efficiency_eta");
   auto oldAlgPtHist = (TH1F *) eff->Get("analyzer/oldEG_efficiency_pt");
   auto oldAlgDRHist = (TH1F *) eff->Get("analyzer/oldEG_deltaR");
   c->SetLogy(0);
   drawNewOld(newAlgEtaEffHists, oldAlgEtaHist, c, 1.2);
   rootools::drawMulti({oldAlgEtaHist, newAlgEtaEffHists[10]}, c, "EG efficiencies", "plots/crystalEG_efficiency_tgraph_eta.png", {.5,.7,.9,.9});
   drawNewOld(newAlgPtEffHists, oldAlgPtHist, c, 1.2);
   drawNewOld(newAlgDRHists, oldAlgDRHist, c, 80.);

   std::vector<TH1F*> selectedEtaEffHists{oldAlgEtaHist, newAlgEtaEffHists[0], newAlgEtaEffHists[3], newAlgEtaEffHists[12], newAlgEtaEffHists[15]};
   rootools::drawMulti(selectedEtaEffHists, c, "EG Efficiencies", "plots/crystalEG_efficiency_variouscuts_eta.png", {0.5, 0.7, 0.9, 0.9});
   std::vector<TH1F*> selectedPtEffHists{oldAlgPtHist, newAlgPtEffHists[0], newAlgPtEffHists[3], newAlgPtEffHists[12], newAlgPtEffHists[15]};
   rootools::drawMulti(selectedPtEffHists, c, "EG Efficiencies", "plots/crystalEG_efficiency_variouscuts_pt.png", {0.5, 0.7, 0.9, 0.9});
   std::vector<TH1F*> selectedDRHists{oldAlgDRHist, newAlgDRHists[0], newAlgDRHists[3], newAlgDRHists[12], newAlgDRHists[15]};
   rootools::drawMulti(selectedDRHists, c, "EG single-electron reconstruction", "plots/crystalEG_deltaR_variouscuts.png", {0.5, 0.7, 0.9, 0.9});

   auto recoGenPtHist = (TH1F *) eff->Get("analyzer/reco_gen_pt");
   recoGenPtHist->Draw();
   c->Print("plots/reco_gen_pt.png");

   c->Clear();
   c->SetCanvasSize(1000,500);
   c->Divide(2,1);
   auto hovereHist = (TH1F *) eff->Get("analyzer/hovere");
   auto hovereHistFake = (TH1F *) rates->Get("analyzer/hovere");
   hovereHistFake->SetLineColor(kRed);
   c->cd(1);
   hovereHist->Draw();
   hovereHistFake->Draw("same");
   auto ecalIsoHist = (TH1F *) eff->Get("analyzer/ecalIso");
   auto ecalIsoHistFake = (TH1F *) rates->Get("analyzer/ecalIso");
   ecalIsoHistFake->SetLineColor(kRed);
   c->cd(2);
   ecalIsoHist->Draw();
   ecalIsoHistFake->Draw("same");
   TLegend * l = new TLegend(0.5,0.8,0.9,0.9);
   setLegStyle(l);
   l->AddEntry(ecalIsoHist, "True electron distribution", "l");
   l->AddEntry(ecalIsoHistFake, "Background distribution", "l");
   l->Draw("same");
   c->Print("plots/crystalEG_hovere_isolation_distributions.png");
}
