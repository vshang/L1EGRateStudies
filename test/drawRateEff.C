// This macro is to be run using `root -q -b drawRateEff.C+`
// Note: the ./plots/ directory must exist!

// rootools can be found in ~nsmith/src/rootools
// It's just a small collection of useful utilities
#include "rootools.h"

#include <memory>
#include "TCanvas.h"
#include "TH1F.h"
#include "TH2F.h"
#include "TLegend.h"
#include "TStyle.h"
#include "TGraph.h"
#include "TGraphErrors.h"
#include "TMultiGraph.h"
#include "TPaveStats.h"

void setLegStyle(TLegend * leg) {
   leg->SetBorderSize(0);
   leg->SetLineColor(1);
   leg->SetLineStyle(1);
   leg->SetLineWidth(.3);
   leg->SetFillColor(0);
   leg->SetFillStyle(0);
}

void drawNewOld(std::vector<TH1F*> newHists, TH1F * oldHist, TCanvas * c, double ymax, double xmax = 0.) {
   c->Clear();
   auto oldGraph = new TGraph((TH1 *) oldHist);
   oldGraph->SetLineColor(kRed);
   oldGraph->SetMarkerColor(kRed);
   oldGraph->SetMarkerStyle(20);
   std::string oldTitle = oldHist->GetTitle();

   TMultiGraph mg("mg", c->GetTitle());
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

void drawNewOldHist(std::vector<TH1F*> newHists, TH1F * oldHist, TCanvas * c, double ymax) {
   oldHist->SetLineColor(kRed);
   std::string oldTitle = oldHist->GetTitle();
   oldHist->SetTitle(c->GetTitle());
   c->Clear();
   for ( auto newHist : newHists ) {
      std::string newTitle = newHist->GetTitle();
      newHist->SetTitle(c->GetTitle());
      if ( oldHist->GetMaximum() > newHist->GetMaximum() )
      {
         if ( c->GetLogy() == 0 ) // linear
            oldHist->SetMinimum(0.);
         if ( ymax != 0. )
            oldHist->SetMaximum(ymax);
         oldHist->Draw();
         newHist->Draw("same");
      }
      else
      {
         if ( c->GetLogy() == 0 ) // linear
            newHist->SetMinimum(0.);
         if ( ymax != 0. )
            newHist->SetMaximum(ymax);
         newHist->Draw();
         oldHist->Draw("same");
      }
      TLegend *leg = new TLegend(0.4,0.8,0.9,0.9);
      setLegStyle(leg);
      leg->AddEntry(oldHist, "Old L2 Algorithm","l");
      leg->AddEntry(newHist, newTitle.c_str(),"l");
      leg->Draw("same");
                  
      c->Print(("plots/"+std::string(newHist->GetName())+".png").c_str());
      delete leg;
      newHist->SetTitle(newTitle.c_str());
   }
   // Fix our title mangling
   oldHist->SetTitle(oldTitle.c_str());
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
   c->SetTitle("EG Fake Rates (PU140, minBias)");
   drawNewOld(newAlgRateHists, oldAlgRateHist, c, 40000.);
   // Draw several cuts on same plot (the four corners in search space)
   std::vector<TH1F*> selectedHists{oldAlgRateHist, newAlgRateHists[0], newAlgRateHists[3], newAlgRateHists[12], newAlgRateHists[15]};
   rootools::drawMulti(selectedHists, c, "EG Fake Rates", "plots/crystalEG_rate_variouscuts.png", {0.5, 0.7, 0.9, 0.9});

   auto effHistKeys = rootools::getKeysofClass(eff, "analyzer", "TH1F");
   auto newAlgEtaEffHists = rootools::loadObjectsMatchingPattern<TH1F>(effHistKeys, "crystalEG*_eta");
   auto newAlgPtEffHists = rootools::loadObjectsMatchingPattern<TH1F>(effHistKeys, "crystalEG*_pt");
   auto newAlgDRHists = rootools::loadObjectsMatchingPattern<TH1F>(effHistKeys, "crystalEG_deltaR*");
   auto newAlgDEtaHists = rootools::loadObjectsMatchingPattern<TH1F>(effHistKeys, "crystalEG_deta*");
   auto newAlgDPhiHists = rootools::loadObjectsMatchingPattern<TH1F>(effHistKeys, "crystalEG_dphi*");
   auto oldAlgEtaHist = (TH1F *) eff->Get("analyzer/oldEG_efficiency_eta");
   auto oldAlgPtHist = (TH1F *) eff->Get("analyzer/oldEG_efficiency_pt");
   auto oldAlgDRHist = (TH1F *) eff->Get("analyzer/oldEG_deltaR");
   auto oldAlgDEtaHist = (TH1F *) eff->Get("analyzer/oldEG_deta");
   auto oldAlgDPhiHist = (TH1F *) eff->Get("analyzer/oldEG_dphi");
   c->SetLogy(0);
   c->SetTitle("EG Single Electron Efficiencies");
   drawNewOld(newAlgEtaEffHists, oldAlgEtaHist, c, 1.2);
   rootools::drawMulti({oldAlgEtaHist, newAlgEtaEffHists[10]}, c, "EG efficiencies", "plots/crystalEG_efficiency_tgraph_eta.png", {.5,.7,.9,.9});
   for(auto hist : newAlgPtEffHists)
   {
      hist->GetXaxis()->SetRange(0, 10);
   }
   drawNewOld(newAlgPtEffHists, oldAlgPtHist, c, 1.2, 50.);
   c->SetTitle("#Delta R Distribution Comparison");
   drawNewOldHist(newAlgDRHists, oldAlgDRHist, c, 0.);
   c->SetTitle("d#eta Distribution Comparison");
   drawNewOldHist(newAlgDEtaHists, oldAlgDEtaHist, c, 0.);
   c->SetTitle("d#phi Distribution Comparison");
   drawNewOldHist(newAlgDPhiHists, oldAlgDPhiHist, c, 0.);

   std::vector<TH1F*> selectedEtaEffHists{oldAlgEtaHist, newAlgEtaEffHists[0], newAlgEtaEffHists[3], newAlgEtaEffHists[12], newAlgEtaEffHists[15]};
   rootools::drawMulti(selectedEtaEffHists, c, "EG Efficiencies", "plots/crystalEG_efficiency_variouscuts_eta.png", {0.5, 0.7, 0.9, 0.9});
   std::vector<TH1F*> selectedPtEffHists{oldAlgPtHist, newAlgPtEffHists[0], newAlgPtEffHists[3], newAlgPtEffHists[12], newAlgPtEffHists[15]};
   rootools::drawMulti(selectedPtEffHists, c, "EG Efficiencies", "plots/crystalEG_efficiency_variouscuts_pt.png", {0.5, 0.7, 0.9, 0.9});
   std::vector<TH1F*> selectedDRHists{oldAlgDRHist, newAlgDRHists[0], newAlgDRHists[3], newAlgDRHists[12], newAlgDRHists[15]};
   rootools::drawMulti(selectedDRHists, c, "EG single-electron reconstruction", "plots/crystalEG_deltaR_variouscuts.png", {0.5, 0.7, 0.9, 0.9});

   c->Clear();
   c->SetCanvasSize(1000,500);
   c->Divide(2,1);
   auto recoGenPtHist = (TH2F *) eff->Get("analyzer/reco_gen_pt");
   auto oldAlgrecoGenPtHist = (TH2F *) eff->Get("analyzer/oldAlg_reco_gen_pt");
   recoGenPtHist->SetMaximum(50);
   oldAlgrecoGenPtHist->SetMaximum(50);
   oldAlgrecoGenPtHist->SetLineColor(kRed);
   c->cd(1);
   recoGenPtHist->Draw("colz");
   c->cd(2);
   oldAlgrecoGenPtHist->Draw("colz");
   c->Print("plots/reco_gen_pt.png");

   auto hovereHistSum = new TH1F("hovere_sum", "EG H/E distribution (full pT range)", 30, 0., 4.);
   auto hovereHistFakeSum = new TH1F("hoverefake_sum", "EG H/E distribution (full pT range)", 30, 0., 4.);
   auto ecalIsoHistSum = new TH1F("iso_sum", "EG ECal Isolation distribution (full pT range)", 30, 0., 4.);
   auto ecalIsoHistFakeSum = new TH1F("isofake_sum", "EG ECal Isolation distribution (full pT range)", 30, 0., 4.);
   std::vector<std::string> pts {"lowpt", "medpt", "highpt"};
   for(auto pt : pts)
   {
      auto hovereHist = (TH1F *) eff->Get(("analyzer/hovere_"+pt).c_str());
      auto hovereHistFake = (TH1F *) rates->Get(("analyzer/hovere_"+pt).c_str());
      auto ecalIsoHist = (TH1F *) eff->Get(("analyzer/ecalIso_"+pt).c_str());
      auto ecalIsoHistFake = (TH1F *) rates->Get(("analyzer/ecalIso_"+pt).c_str());
      hovereHistSum->Add(hovereHist);
      hovereHistFakeSum->Add(hovereHistFake);
      ecalIsoHistSum->Add(ecalIsoHist);
      ecalIsoHistFakeSum->Add(ecalIsoHistFake);
      c->Clear();
      c->Divide(2,1);
      hovereHistFake->SetLineColor(kRed);
      c->cd(1);
      // Normalize
      hovereHist->Scale(1./hovereHist->Integral());
      hovereHistFake->Scale(1./hovereHistFake->Integral());
      hovereHist->GetYaxis()->SetTitle("");
      hovereHist->Draw();
      hovereHistFake->Draw("same");
      ecalIsoHistFake->SetLineColor(kRed);
      c->cd(2);
      ecalIsoHist->Scale(1./ecalIsoHist->Integral());
      ecalIsoHistFake->Scale(1./ecalIsoHistFake->Integral());
      ecalIsoHist->GetYaxis()->SetTitle("");
      ecalIsoHist->Draw();
      ecalIsoHistFake->Draw("same");
      TLegend * l = new TLegend(0.4,0.8,0.9,0.9);
      setLegStyle(l);
      l->AddEntry(ecalIsoHist, "True electron distribution (int-norm)", "l");
      l->AddEntry(ecalIsoHistFake, "Background distribution (int-norm)", "l");
      l->Draw("same");
      c->Print(("plots/crystalEG_hovere_isolation_distributions_"+pt+".png").c_str());
   }
   c->Clear();
   c->Divide(2,1);
   hovereHistFakeSum->SetLineColor(kRed);
   c->cd(1);
   if ( hovereHistSum->GetMaximum() > hovereHistFakeSum->GetMaximum() )
   {
      hovereHistSum->Draw();
      hovereHistFakeSum->Draw("same");
   }
   else
   {
      hovereHistFakeSum->Draw();
      hovereHistSum->Draw("same");
   }
   ecalIsoHistFakeSum->SetLineColor(kRed);
   c->cd(2);
   if ( ecalIsoHistSum->GetMaximum() > ecalIsoHistFakeSum->GetMaximum() )
   {
      ecalIsoHistSum->Draw();
      ecalIsoHistFakeSum->Draw("same");
   }
   else
   {
      ecalIsoHistFakeSum->Draw();
      ecalIsoHistSum->Draw("same");
   }
   TLegend * l = new TLegend(0.4,0.8,0.9,0.9);
   setLegStyle(l);
   l->AddEntry(ecalIsoHistSum, "True electron distribution", "l");
   l->AddEntry(ecalIsoHistFakeSum, "Background distribution", "l");
   l->Draw("same");
   c->Print("plots/crystalEG_hovere_isolation_distributions.png");

}
