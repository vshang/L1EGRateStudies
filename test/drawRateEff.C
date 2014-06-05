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
#include "THStack.h"

void setLegStyle(TLegend * leg) {
   leg->SetBorderSize(0);
   leg->SetLineColor(1);
   leg->SetLineStyle(1);
   leg->SetLineWidth(.3);
   leg->SetFillColor(0);
   leg->SetFillStyle(0);
}

void drawNewOld(std::vector<TH1F*> newHists, std::vector<TH1F*> oldHists, TCanvas * c, double ymax, std::pair<double, double> xrange = {0., 0.}) {
   c->Clear();
   TMultiGraph mg("mg", c->GetTitle());

   std::vector<TGraphErrors*> oldGraphs;
   std::vector<int> colors = {kRed, kGreen, kBlue};
   auto color = begin(colors);
   int style = 20;
   for(auto& oldHist : oldHists)
   {
      oldGraphs.push_back(new TGraphErrors((TH1 *) oldHist));
      oldGraphs.back()->SetLineColor(*color);
      oldGraphs.back()->SetMarkerColor(*color++);
      oldGraphs.back()->SetMarkerStyle(style++);
      oldGraphs.back()->SetMarkerSize(0.5);
      mg.Add(oldGraphs.back());
   }

   for ( auto newHist : newHists ) {
      auto g = new TGraphErrors((TH1 *) newHist);
      g->SetLineColor(kBlack);
      g->SetMarkerColor(kBlack);
      g->SetMarkerStyle(25);
      g->SetMarkerSize(0.5);
      mg.Add(g);
      mg.Draw("aple");
      if ( c->GetLogy() == 0 ) // linear
         mg.SetMinimum(0.);
      else
         mg.SetMinimum(10.);
      if ( ymax != 0. )
         mg.SetMaximum(ymax);
      TLegend *leg = new TLegend(0.5,0.8,0.9,0.9);
      setLegStyle(leg);
      for (auto& oldGraph : oldGraphs) leg->AddEntry(oldGraph, oldGraph->GetTitle(),"lpe");
      leg->AddEntry(g, g->GetTitle(),"lpe");
      leg->Draw("same");
      mg.GetXaxis()->SetTitle(oldHists[0]->GetXaxis()->GetTitle());
      if ( xrange.first != 0. || xrange.second != 0 )
        mg.GetXaxis()->SetRangeUser(xrange.first, xrange.second);
      mg.GetYaxis()->SetTitle(oldHists[0]->GetYaxis()->GetTitle());

      c->Print(("plots/"+std::string(newHist->GetName())+".png").c_str());
      delete leg;
      mg.RecursiveRemove(g);
      delete g;
   }
}

void drawNewOldHist(std::vector<TH1F*> newHists, std::vector<TH1F*> oldHists, TCanvas * c, double ymax) {
   THStack hs("hs", c->GetTitle());
   std::vector<int> colors = {kRed, kGreen, kBlue};
   auto color = begin(colors);
   for(auto& oldHist : oldHists)
   {
      oldHist->SetLineColor(*color++);
      hs.Add(oldHist);
   }
   c->Clear();
   if ( c->GetLogy() == 0 ) // linear
      hs.SetMinimum(0.);
   if ( ymax != 0. )
      hs.SetMaximum(ymax);

   for ( auto newHist : newHists ) {
      newHist->SetLineColor(kBlack);
      hs.Add(newHist);

      hs.Draw("nostack");

      TLegend *leg = new TLegend(0.4,0.8,0.9,0.9);
      setLegStyle(leg);
      for(auto& oldHist : oldHists) leg->AddEntry(oldHist, oldHist->GetTitle(),"l");
      leg->AddEntry(newHist, newHist->GetTitle(),"l");
      leg->Draw("same");
      hs.GetXaxis()->SetTitle(oldHists[0]->GetXaxis()->GetTitle());
      hs.GetYaxis()->SetTitle(oldHists[0]->GetYaxis()->GetTitle());
      hs.GetYaxis()->SetTitleOffset(1.2);
                  
      c->Print(("plots/"+std::string(newHist->GetName())+".png").c_str());
      delete leg;
      hs.RecursiveRemove(newHist);
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
   TCanvas * c = new TCanvas("canvas", "Canvas", 800, 600);
	
   TFile * rates = new TFile("egTriggerRates.root");
   TFile * eff = new TFile("egTriggerEff.root");

   auto rateHistKeys = rootools::getKeysofClass(rates, "analyzer", "TH1F");
   auto newAlgRateHists = rootools::loadObjectsMatchingPattern<TH1F>(rateHistKeys, "*crystal*");
   auto oldAlgRateHist = (TH1F *) rates->Get("analyzer/oldEG_rate");
   oldAlgRateHist->SetTitle("Tower-level L2 Algorithm");
   auto dynAlgRateHist = (TH1F *) rates->Get("analyzer/dynEG_rate");
   dynAlgRateHist->SetTitle("Dynamic Algorithm");

   c->SetLogy(1);
   c->SetGridx(1);
   c->SetGridy(1);
   gStyle->SetGridStyle(2);
   gStyle->SetGridColor(kGray+1);
   c->SetTitle("EG Fake Rates (PU140, minBias)");
   drawNewOld(newAlgRateHists, {oldAlgRateHist}, c, 40000., {0., 50.});

   auto effHistKeys = rootools::getKeysofClass(eff, "analyzer", "TH1F");
   auto newAlgEtaEffHists = rootools::loadObjectsMatchingPattern<TH1F>(effHistKeys, "*crystal*_eta");
   auto newAlgPtEffHists = rootools::loadObjectsMatchingPattern<TH1F>(effHistKeys, "*crystal*_pt");
   auto newAlgDRHists = rootools::loadObjectsMatchingPattern<TH1F>(effHistKeys, "*crystal*_deltaR*");
   auto newAlgDEtaHists = rootools::loadObjectsMatchingPattern<TH1F>(effHistKeys, "*crystal*_deta*");
   auto newAlgDPhiHists = rootools::loadObjectsMatchingPattern<TH1F>(effHistKeys, "*crystal*_dphi*");
   auto oldAlgEtaHist = (TH1F *) eff->Get("analyzer/oldEG_efficiency_eta");
   oldAlgEtaHist->SetTitle("Tower-level L2 Algorithm");
   oldAlgEtaHist->GetXaxis()->SetTitle("Offline reco. #eta");
   auto oldAlgPtHist = (TH1F *) eff->Get("analyzer/oldEG_efficiency_pt");
   oldAlgPtHist->SetTitle("Tower-level L2 Algorithm");
   oldAlgPtHist->GetXaxis()->SetTitle("Offline reco. pT (GeV)");
   auto oldAlgDRHist = (TH1F *) eff->Get("analyzer/oldEG_deltaR");
   oldAlgDRHist->SetTitle("Tower-level L2 Algorithm");
   oldAlgDRHist->GetYaxis()->SetTitle("Counts");
   auto oldAlgDEtaHist = (TH1F *) eff->Get("analyzer/oldEG_deta");
   auto oldAlgDPhiHist = (TH1F *) eff->Get("analyzer/oldEG_dphi");
   auto dynAlgEtaHist = (TH1F *) eff->Get("analyzer/dynEG_efficiency_eta");
   auto dynAlgPtHist = (TH1F *) eff->Get("analyzer/dynEG_efficiency_pt");
   auto dynAlgDRHist = (TH1F *) eff->Get("analyzer/dynEG_deltaR");
   auto dynAlgDEtaHist = (TH1F *) eff->Get("analyzer/dynEG_deta");
   auto dynAlgDPhiHist = (TH1F *) eff->Get("analyzer/dynEG_dphi");
   c->SetLogy(0);
   c->SetTitle("EG Single Electron Efficiencies");
   drawNewOld(newAlgEtaEffHists, {oldAlgEtaHist}, c, 1.2, {-1.6, 1.6});
   drawNewOld(newAlgPtEffHists, {oldAlgPtHist}, c, 1.2, {0., 50.});
   c->SetGridx(0);
   c->SetGridy(0);
   c->SetTitle("#Delta R Distribution Comparison");
   drawNewOldHist(newAlgDRHists, {oldAlgDRHist}, c, 0.);
   c->SetTitle("d#eta Distribution Comparison");
   drawNewOldHist(newAlgDEtaHists, {oldAlgDEtaHist, dynAlgDEtaHist}, c, 0.);
   c->SetTitle("d#phi Distribution Comparison");
   drawNewOldHist(newAlgDPhiHists, {oldAlgDPhiHist, dynAlgDPhiHist}, c, 0.);

   c->Clear();
   c->SetCanvasSize(1200,600);
   c->Divide(2,1);
   auto recoGenPtHist = (TH2F *) eff->Get("analyzer/reco_gen_pt");
   recoGenPtHist->SetTitle("Crystal EG alg. momentum error");
   recoGenPtHist->GetYaxis()->SetTitle("Relative Error (reco-gen)/gen");
   auto oldAlgrecoGenPtHist = (TH2F *) eff->Get("analyzer/oldAlg_reco_gen_pt");
   oldAlgrecoGenPtHist->SetTitle("Tower EG alg. momentum error");
   oldAlgrecoGenPtHist->GetYaxis()->SetTitle("Relative Error (reco-gen)/gen");
   recoGenPtHist->SetMaximum(50);
   oldAlgrecoGenPtHist->SetMaximum(50);
   oldAlgrecoGenPtHist->SetLineColor(kRed);
   c->cd(1);
   recoGenPtHist->Draw("colz");
   recoGenPtHist->GetYaxis()->SetTitleOffset(1.4);
   c->cd(2);
   oldAlgrecoGenPtHist->Draw("colz");
   oldAlgrecoGenPtHist->GetYaxis()->SetTitleOffset(1.4);
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
