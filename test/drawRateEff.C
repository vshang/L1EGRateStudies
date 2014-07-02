// This macro is to be run using `root -q -b drawRateEff.C+`
// Note: the ./plots/ directory must exist!

// rootools can be found in ~nsmith/src/rootools
// It's just a small collection of useful utilities
#include "rootools.h"

#include <memory>
#include "TBox.h"
#include "TCanvas.h"
#include "TH1F.h"
#include "TH2F.h"
#include "TLatex.h"
#include "TLegend.h"
#include "TStyle.h"
#include "TGraph.h"
#include "TGraphErrors.h"
#include "TGraphAsymmErrors.h"
#include "TMultiGraph.h"
#include "TPaletteAxis.h"
#include "TPaveStats.h"
#include "TTree.h"
#include "THStack.h"
#include "TF1.h"
#include "TF2.h"

void setLegStyle(TLegend * leg) {
   leg->SetBorderSize(0);
   leg->SetLineColor(1);
   leg->SetLineStyle(1);
   leg->SetLineWidth(.3);
   leg->SetFillColor(0);
   leg->SetFillStyle(0);
}

void drawNewOld(std::vector<TH1F*> newHists, std::vector<TH1F*> oldHists, TCanvas * c, double ymax, std::pair<double, double> xrange = {0., 0.}, bool fit = false) {
   c->Clear();
   TMultiGraph mg("mg", c->GetTitle());

   std::vector<TGraphErrors*> oldGraphs;
   std::vector<int> colors = {kRed, kGreen, kBlue, kOrange, kGray};
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
      if ( fit )
         mg.Draw("apez");
      else
         mg.Draw("aplez");

      if ( c->GetLogy() == 0 ) // linear
         mg.SetMinimum(0.);
      else
         mg.SetMinimum(10.);

      if ( ymax != 0. )
         mg.SetMaximum(ymax);

      if ( fit && xrange.second != xrange.first )
      {
         TF1 shape("shape", "[0]/2*(1+TMath::Erf((x-[1])/([2]*sqrt(x))))", xrange.first, xrange.second);
         shape.SetParameters(1., 10., 2.);
         g->Fit(&shape);
         g->GetFunction("shape")->SetLineColor(g->GetLineColor());
         g->GetFunction("shape")->SetLineWidth(g->GetLineWidth()*2);
         for(auto& graph : oldGraphs)
         {
            graph->Fit(&shape);
            graph->GetFunction("shape")->SetLineColor(graph->GetLineColor());
            graph->GetFunction("shape")->SetLineWidth(graph->GetLineWidth()*2);
         }
      }

      TLegend *leg = new TLegend(0.5,0.76,0.9,0.9);
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

void draw(std::vector<TGraphAsymmErrors*> graphs, TCanvas * c, double ymax, std::pair<double, double> xrange = {0., 0.}, bool fit = false) {
   c->Clear();
   TMultiGraph mg("mg", c->GetTitle());

   std::vector<int> colors = {kBlack, kRed, kGreen, kBlue, kOrange, kGray};
   auto color = begin(colors);
   int style = 20;
   for(auto& graph : graphs)
   {
      graph->SetLineColor(*color);
      graph->SetMarkerColor(*color++);
      graph->SetMarkerStyle(style++);
      graph->SetMarkerSize(0.5);
      mg.Add(graph);
   }
   if ( fit )
      mg.Draw("apez");
   else
      mg.Draw("aplez");

   if ( c->GetLogy() == 0 ) // linear
      mg.SetMinimum(0.);
   else
      mg.SetMinimum(10.);

   if ( ymax != 0. )
      mg.SetMaximum(ymax);

   if ( fit && xrange.second != xrange.first )
   {
      for(auto& graph : graphs)
      {
         TF1 shape("shape", "[0]/2*(1+TMath::Erf((x-[1])/([2]*sqrt(x))))", xrange.first, xrange.second);
         shape.SetParameters(1., 15., 3.);
         // Somehow, step size increases each time, have to find a way to control it...
         graph->Fit(&shape);
         graph->GetFunction("shape")->SetLineColor(graph->GetLineColor());
         graph->GetFunction("shape")->SetLineWidth(graph->GetLineWidth()*2);
      }
   }

   TLegend *leg = new TLegend(0.5,0.76,0.9,0.9);
   setLegStyle(leg);
   for (auto& graph: graphs) leg->AddEntry(graph, graph->GetTitle(),"lpe");
   leg->Draw("same");
   mg.GetXaxis()->SetTitle(graphs[0]->GetXaxis()->GetTitle());
   if ( xrange.first != 0. || xrange.second != 0 )
     mg.GetXaxis()->SetRangeUser(xrange.first, xrange.second);
   mg.GetYaxis()->SetTitle(graphs[0]->GetYaxis()->GetTitle());

   // Get rid of divide_... stuff
   std::string name(graphs[0]->GetName());
   name = name.substr(7, name.find("_by")-7);
   c->Print(("plots/"+name+".png").c_str());
   delete leg;
   for(auto& graph : graphs)
   {
      mg.RecursiveRemove(graph);
   }
}

void draw2DdeltaRHist(TH2F* hist, TCanvas * c) {
   c->Clear();
   c->cd();
   gStyle->SetOptTitle(0);
   double margin = 0.07;
   double histpad_size = 0.7;
   auto hist_pad = new TPad((c->GetName()+std::string("_hist")).c_str(), "subpad", margin, margin, histpad_size+margin, histpad_size+margin, c->GetFillColor());
   hist_pad->SetMargin(0., 0., 0., 0.);
   hist_pad->Draw();
   auto xprojection_pad = new TPad((c->GetName()+std::string("_xprojection")).c_str(), "subpad", margin, histpad_size+margin, histpad_size+margin, 1-margin, c->GetFillColor());
   xprojection_pad->SetMargin(0., 0., 0., 0.);
   xprojection_pad->Draw();
   auto yprojection_pad = new TPad((c->GetName()+std::string("_yprojection")).c_str(), "subpad", histpad_size+margin, margin, 1-margin, histpad_size+margin, c->GetFillColor());
   yprojection_pad->SetMargin(0., 0., 0., 0.);
   yprojection_pad->Draw();

   hist->Sumw2();
   hist->Scale(1./hist->Integral());
   auto xprojection_hist = hist->ProjectionX(hist->GetName(), 1, hist->GetNbinsY(), "e");
   auto xprojection = new TGraphErrors(xprojection_hist);
   xprojection->SetLineColor(kBlack);
   xprojection->SetMarkerColor(kBlack);
   auto yprojection_hist = hist->ProjectionY(hist->GetName(), 1, hist->GetNbinsX(), "e");
   auto yprojection = new TGraphErrors(yprojection_hist->GetXaxis()->GetNbins());
   yprojection->SetName((yprojection_hist->GetName()+std::string("_graph")).c_str());
   TAxis * yproj_xaxis = yprojection_hist->GetXaxis();
   for(int i=0; i<yprojection_hist->GetXaxis()->GetNbins(); i++)
   {
      double bin = yproj_xaxis->GetBinCenter(i+1);
      double width = yprojection_hist->GetBinWidth(i+1)*gStyle->GetErrorX();
      double count = yprojection_hist->GetBinContent(i+1);
      double err = yprojection_hist->GetBinError(i+1);
      yprojection->SetPoint(i, count, bin);
      yprojection->SetPointError(i, err, width);
   }

   // Draw 2D hist
   hist_pad->cd();
   hist->Draw("col");
   hist->GetYaxis()->SetTitleOffset(1.4);
   
   // Fit hist
   TF2 shape("2dshape", "[0]*exp(-[2]*(x[0]-[1])**2-[4]*(x[1]-[3])**2-2*[5]*(x[0]-[1])*(x[1]-[3]))", -0.05, 0.05, -0.05, 0.05);
   shape.SetParameters(0.003, 0., 3.769e4, 0., 4.215e4, -1.763e4);
   hist->Fit(&shape, "n");
   const double max = shape.GetParameter(0);
   const double contours[3] {max*exp(-4.5), max*exp(-2), max*exp(-0.5)};
   shape.SetContour(3, contours);
   shape.SetNpx(100);
   shape.SetNpy(100);
   shape.SetLineWidth(2);
   shape.SetLineColor(kRed);
   shape.Draw("cont3 same");
   
   // One crystal box
   TBox crystalBox(-0.0173/2, -0.0173/2, 0.0173/2, 0.0173/2);
   crystalBox.SetLineStyle(3);
   crystalBox.SetLineColor(kGray);
   crystalBox.SetLineWidth(2);
   crystalBox.SetFillStyle(0);
   crystalBox.Draw();

   // Draw x projection
   xprojection_pad->cd();
   xprojection->Draw("apez");
   xprojection->GetYaxis()->SetNdivisions(0);
   xprojection->GetXaxis()->SetRangeUser(hist->GetXaxis()->GetBinLowEdge(1), hist->GetXaxis()->GetBinUpEdge(hist->GetXaxis()->GetNbins()));
   xprojection->GetXaxis()->SetLabelSize(0.);
   xprojection->GetYaxis()->SetRangeUser(0., 0.2);
   TF1 shapeprojX("shapeprojX", "[0]*sqrt(([2]*[4]-[5]**2)/(TMath::Pi()*[2]))*exp(([5]**2-[2]*[4])*(x-[3])**2/[2])", -0.05, 0.05);
   shapeprojX.SetParameters(shape.GetParameters());
   shapeprojX.SetParameter(0, shape.GetParameter(0)/20);
   shapeprojX.SetLineWidth(2);
   shapeprojX.SetNpx(100);
   shapeprojX.SetLineColor(kRed);
   shapeprojX.Draw("same");

   // Draw y projection
   yprojection_pad->cd();
   yprojection->Draw("apez");
   yprojection->GetXaxis()->SetNdivisions(0);
   yprojection->GetXaxis()->SetRangeUser(0., 0.2);
   yprojection->GetYaxis()->SetRangeUser(hist->GetYaxis()->GetBinLowEdge(1), hist->GetYaxis()->GetBinUpEdge(hist->GetYaxis()->GetNbins()));
   yprojection->GetYaxis()->SetLabelSize(0.);
   TF1 shapeprojY("shapeprojY", "[0]*sqrt(([2]*[4]-[5]**2)/(TMath::Pi()*[4]))*exp(([5]**2-[2]*[4])*(x-[1])**2/[4])", -0.05, 0.05);
   shapeprojY.SetParameters(shape.GetParameters());
   shapeprojY.SetParameter(0, shape.GetParameter(0)/20);
   double shapeprojYpos[101], shapeprojYval[101];
   for(int i=0; i<101; ++i) {
      shapeprojYpos[i] = 1e-3*i-0.05;
      shapeprojYval[i] = shapeprojY.Eval(shapeprojYpos[i]);
   }
   TGraph shapeprojYLine(101, shapeprojYval, shapeprojYpos);
   shapeprojYLine.SetLineColor(kRed);
   shapeprojYLine.SetLineWidth(2);
   shapeprojYLine.Draw("l");

   // Draw Title
   c->cd();
   auto title = new TLatex(margin, 1-margin+0.01, "Crystal-level EG Trigger #DeltaR Distribution");
   title->SetTextSize(0.04);
   title->SetNDC();
   title->Draw();

   // Stats
   TLatex *stats[5];
   stats[0] = new TLatex(histpad_size+margin+0.01, histpad_size+margin+0.13, ("#mu_#eta = "+to_string(shape.GetParameter(1))).c_str());
   stats[1] = new TLatex(histpad_size+margin+0.01, histpad_size+margin+0.1, ("#mu_#phi = "+to_string(shape.GetParameter(3))).c_str());
   stats[2] = new TLatex(histpad_size+margin+0.01, histpad_size+margin+0.07, ("#sigma_#eta#eta = "+to_string(sqrt(0.5/shape.GetParameter(2)))).c_str());
   stats[3] = new TLatex(histpad_size+margin+0.01, histpad_size+margin+0.04, ("#sigma_#phi#phi = "+to_string(sqrt(0.5/shape.GetParameter(4)))).c_str());
   stats[4] = new TLatex(histpad_size+margin+0.01, histpad_size+margin+0.01, ("#sigma_#eta#phi = "+to_string(sqrt(-0.5/shape.GetParameter(5)))).c_str());
   for(int i=0; i<5; ++i) {
      stats[i]->SetTextSize(0.024);
      stats[i]->SetNDC();
      stats[i]->Draw();
   }

   // Draw palette
   // (not working)
   gPad->Update();
   auto palette = new TPaletteAxis(1-margin+0.01, margin, 1-0.01, histpad_size+margin, hist);
   palette->Draw();
   gPad->Modified();
   gPad->Update();

   c->Print(("plots/"+std::string(hist->GetName())+".png").c_str());
   delete yprojection;
   
   gStyle->SetOptTitle(1);
}

void drawNewOldHist(std::vector<TH1F*> newHists, std::vector<TH1F*> oldHists, TCanvas * c, double ymax) {
   THStack hs("hs", c->GetTitle());
   std::vector<int> colors = {kRed, kGreen, kBlue, kOrange, kGray};
   auto color = begin(colors);
   for(auto& oldHist : oldHists)
   {
      oldHist->Sumw2();
      oldHist->Scale(1./oldHist->Integral());
      oldHist->SetLineColor(*color++);
      hs.Add(oldHist, "hist ex0");
   }
   c->Clear();
   if ( c->GetLogy() == 0 ) // linear
      hs.SetMinimum(0.);
   if ( ymax != 0. )
      hs.SetMaximum(ymax);

   for ( auto newHist : newHists ) {
      newHist->Sumw2();
      newHist->Scale(1./newHist->Integral());
      newHist->SetLineColor(kBlack);
      hs.Add(newHist, "hist ex0");

      hs.Draw("nostack");

      TLegend *leg = new TLegend(0.5,0.76,0.9,0.9);
      setLegStyle(leg);
      for(auto& oldHist : oldHists) leg->AddEntry(oldHist, oldHist->GetTitle(),"l");
      leg->AddEntry(newHist, newHist->GetTitle(),"l");
      leg->Draw("same");
      hs.GetXaxis()->SetTitle(oldHists[0]->GetXaxis()->GetTitle());
      hs.GetYaxis()->SetTitle(oldHists[0]->GetYaxis()->GetTitle());
      hs.GetYaxis()->SetTitleOffset(1.2);
      hs.GetYaxis()->SetTitle("Fraction of Events");
                  
      c->Print(("plots/"+std::string(newHist->GetName())+".png").c_str());
      delete leg;
      hs.RecursiveRemove(newHist);
   }
}

void drawRateEff() {
   gStyle->SetOptStat(0);
   TCanvas * c = new TCanvas("canvas", "Canvas", 800, 600);
	
   TFile * rates = new TFile("egTriggerRates.root");
   TFile * eff = new TFile("egTriggerEff.root");

   auto rateHistKeys = rootools::getKeysofClass(rates, "analyzer", "TH1F");
   auto newAlgRateHists = rootools::loadObjectsMatchingPattern<TH1F>(rateHistKeys, "*crystal*");
   auto oldAlgRateHist = (TH1F *) rates->Get("analyzer/SLHCL1ExtraParticles:EGamma_rate");
   oldAlgRateHist->SetTitle("Original L2 Algorithm");
   auto dynAlgRateHist = (TH1F *) rates->Get("analyzer/SLHCL1ExtraParticlesNewClustering:EGamma_rate");
   dynAlgRateHist->SetTitle("LLR L2 Algorithm");
   auto run1AlgRateHist = (TH1F *) rates->Get("analyzer/l1extraParticles:All_rate");
   run1AlgRateHist->SetTitle("Run 1 Algorithm");
   auto crystalAlgRateHist = (TH1F *) rates->Get("analyzer/L1EGammaCrystalsProducer:EGammaCrystal_rate");
   crystalAlgRateHist->SetTitle("Crystal-level Algorithm (producer)");

   c->SetLogy(1);
   c->SetGridx(1);
   c->SetGridy(1);
   gStyle->SetGridStyle(2);
   gStyle->SetGridColor(kGray+1);
   c->SetTitle("EG Fake Rates (PU140, minBias)");
   drawNewOld(newAlgRateHists, {oldAlgRateHist, dynAlgRateHist, run1AlgRateHist}, c, 40000., {0., 50.});

   auto effHistKeys = rootools::getKeysofClass(eff, "analyzer", "TGraphAsymmErrors");
   auto deltaHistKeys = rootools::getKeysofClass(eff, "analyzer", "TH1F");
   auto newAlgEtaEffHists = rootools::loadObjectsMatchingPattern<TGraphAsymmErrors>(effHistKeys, "*crystal*_eta_by_gen_eta");
   auto newAlgPtEffHists = rootools::loadObjectsMatchingPattern<TGraphAsymmErrors>(effHistKeys, "divide_dyncrystal*_pt_by_gen_pt");
   auto newAlgRecoPtEffHists = rootools::loadObjectsMatchingPattern<TGraphAsymmErrors>(effHistKeys, "divide_dyncrystalEG_threshold*");
   auto newAlgDRHists = rootools::loadObjectsMatchingPattern<TH1F>(deltaHistKeys, "*crystal*_deltaR*");
   auto newAlgDEtaHists = rootools::loadObjectsMatchingPattern<TH1F>(deltaHistKeys, "*crystal*_deta*");
   auto newAlgDPhiHists = rootools::loadObjectsMatchingPattern<TH1F>(deltaHistKeys, "*crystal*_dphi*");

   auto oldAlgEtaHist = (TGraphAsymmErrors *) eff->Get("analyzer/divide_SLHCL1ExtraParticles:EGamma_efficiency_eta_by_gen_eta");
   oldAlgEtaHist->SetTitle("Original L2 Algorithm");
   auto oldAlgPtHist = (TGraphAsymmErrors *) eff->Get("analyzer/divide_SLHCL1ExtraParticles:EGamma_efficiency_pt_by_gen_pt");
   oldAlgPtHist->SetTitle("Original L2 Algorithm");
   auto oldAlgRecoPtHists = rootools::loadObjectsMatchingPattern<TGraphAsymmErrors>(effHistKeys, "divide_SLHCL1ExtraParticles:EGamma_threshold*");
   for(auto& hist : oldAlgRecoPtHists) hist->SetTitle("Original L2 Algorithm");
   auto oldAlgDRHist = (TH1F *) eff->Get("analyzer/SLHCL1ExtraParticles:EGamma_deltaR");
   oldAlgDRHist->SetTitle("Original L2 Algorithm");
   oldAlgDRHist->GetYaxis()->SetTitle("Counts");
   auto oldAlgDEtaHist = (TH1F *) eff->Get("analyzer/SLHCL1ExtraParticles:EGamma_deta");
   oldAlgDEtaHist->SetTitle("Original L2 Algorithm");
   auto oldAlgDPhiHist = (TH1F *) eff->Get("analyzer/SLHCL1ExtraParticles:EGamma_dphi");
   oldAlgDPhiHist->SetTitle("Original L2 Algorithm");

   auto dynAlgEtaHist = (TGraphAsymmErrors *) eff->Get("analyzer/divide_SLHCL1ExtraParticlesNewClustering:EGamma_efficiency_eta_by_gen_eta");
   dynAlgEtaHist->SetTitle("LLR L2 Algorithm");
   auto dynAlgPtHist = (TGraphAsymmErrors *) eff->Get("analyzer/divide_SLHCL1ExtraParticlesNewClustering:EGamma_efficiency_pt_by_gen_pt");
   dynAlgPtHist->SetTitle("LLR L2 Algorithm");
   auto dynAlgDRHist = (TH1F *) eff->Get("analyzer/SLHCL1ExtraParticlesNewClustering:EGamma_deltaR");
   dynAlgDRHist->SetTitle("LLR L2 Algorithm");
   auto dynAlgDEtaHist = (TH1F *) eff->Get("analyzer/SLHCL1ExtraParticlesNewClustering:EGamma_deta");
   dynAlgDEtaHist->SetTitle("LLR L2 Algorithm");
   auto dynAlgDPhiHist = (TH1F *) eff->Get("analyzer/SLHCL1ExtraParticlesNewClustering:EGamma_dphi");
   dynAlgDPhiHist->SetTitle("LLR L2 Algorithm");

   auto run1AlgPtHist = (TGraphAsymmErrors *) eff->Get("analyzer/divide_l1extraParticles:All_efficiency_pt_by_gen_pt");
   run1AlgPtHist->SetTitle("Run 1 Algorithm");
   auto run1AlgDRHist = (TH1F *) eff->Get("analyzer/l1extraParticles:All_deltaR");
   run1AlgDRHist->SetTitle("Run 1 Algorithm");

   auto crystalAlgPtHist = (TGraphAsymmErrors *) eff->Get("analyzer/divide_L1EGammaCrystalsProducer:EGammaCrystal_efficiency_pt_by_gen_pt");
   crystalAlgPtHist->SetTitle("Crystal-level Algorithm (producer)");

   // Use crystal tree to adjust turn-on plot for incorrect offline pt reconstruction
   auto crystal_tree = (TTree *) eff->Get("analyzer/crystal_tree");
   auto newAlgTurnOnNumerator = new TH1F("newAlgTurnOnNumerator", "Crystal (pT corrected)", 60, 0., 50.);
   auto newAlgTurnOnDenom = new TH1F("newAlgTurnOnDenom", "Dynamic Crystal Trigger", 60, 0., 50.);
   auto offlineRecoHist = new TH2F("offlineRecoHist", "Offline reco to gen. comparison;Gen. pT (GeV);(reco-gen)/gen;Counts", 60, 0., 50., 60, -0.5, 0.5);
   crystal_tree->Draw("(reco_pt-gen_pt)/gen_pt:gen_pt >> offlineRecoHist", "reco_pt>0", "colz");
   auto offlineRecoHistProjection = offlineRecoHist->ProjectionY("offlineRecoHistProjection", 0, -1, "e");
   c->SetLogy(0);
   offlineRecoHist->Draw("colz");
   c->Print("plots/offlineReco_vs_gen.png");
   c->Clear();
   offlineRecoHistProjection->Draw("hist ex0");
   TF1 gaus("gaus", "gaus", -.5, .5);
   gaus.SetParameters(1.3e3, 0.1, 0.1);
   offlineRecoHistProjection->Fit(&gaus, "", "", 0., 0.2);
   TLatex fitmu(-0.4, 1200., ("#mu = "+std::to_string(gaus.GetParameter(1))).c_str());
   fitmu.Draw();
   c->Print("plots/offlineReco_vs_gen_projection.png");
   crystal_tree->Draw("reco_pt >> newAlgTurnOnDenom", "reco_pt > 0.");
   crystal_tree->Draw("reco_pt >> newAlgTurnOnNumerator", "reco_pt > 0. && passed && cluster_pt > 15./1.109");
   auto newAlgCorrectedRecoPtHist15 = new TGraphAsymmErrors(newAlgTurnOnNumerator, newAlgTurnOnDenom);
   crystal_tree->Draw("reco_pt >> newAlgTurnOnNumerator", "reco_pt > 0. && passed && cluster_pt > 30./1.109");
   auto newAlgCorrectedRecoPtHist30 = new TGraphAsymmErrors(newAlgTurnOnNumerator, newAlgTurnOnDenom);

   c->SetTitle("EG Single Electron Efficiencies");
   for(auto& hist : newAlgEtaEffHists)
      draw({hist, oldAlgEtaHist, dynAlgEtaHist}, c, 1.2, {-1.6, 1.6});
   for(auto& hist : newAlgPtEffHists)
      draw({hist, oldAlgPtHist, dynAlgPtHist, run1AlgPtHist}, c, 1.2, {0., 50.}, true);
   std::cout << "new hists size: " << newAlgRecoPtEffHists.size() << ", old hists size: " << oldAlgRecoPtHists.size() << std::endl;
   c->SetTitle("EG Single Electron Turn-On Efficiencies, 15GeV Threshold");
   draw({newAlgRecoPtEffHists[0], newAlgCorrectedRecoPtHist15, oldAlgRecoPtHists[0]}, c, 1.2, {0., 50.}, true);
   c->SetTitle("EG Single Electron Turn-On Efficiencies, 30GeV Threshold");
   draw({newAlgRecoPtEffHists[1], newAlgCorrectedRecoPtHist30, oldAlgRecoPtHists[1]}, c, 1.2, {0., 50.}, true);
   c->SetGridx(0);
   c->SetGridy(0);
   c->SetTitle("#Delta R Distribution Comparison");
   drawNewOldHist(newAlgDRHists, {oldAlgDRHist, dynAlgDRHist, run1AlgDRHist}, c, 0.);
   c->SetTitle("d#eta Distribution Comparison");
   drawNewOldHist(newAlgDEtaHists, {oldAlgDEtaHist, dynAlgDEtaHist}, c, 0.);
   c->SetTitle("d#phi Distribution Comparison");
   drawNewOldHist(newAlgDPhiHists, {oldAlgDPhiHist, dynAlgDPhiHist}, c, 0.);

   c->Clear();
   auto bremHist = (TH2F *) eff->Get("analyzer/brem_dphi_hist");
   bremHist->Draw("colz");
   c->Print("plots/brem_dphi_hist.png");
   auto bremHistProj = bremHist->ProjectionY("brem_dphi_hist_py", 1, 4);
   bremHistProj->Draw();
   c->Print("plots/brem_dphi_hist_py.png");

   auto dynCrystal2DdeltaRHist = (TH2F *) eff->Get("analyzer/dyncrystalEG_2DdeltaR_hist");
   c->SetCanvasSize(800, 700);
   c->SetTitle("#Delta R Distribution Fit");
   draw2DdeltaRHist(dynCrystal2DdeltaRHist, c);

   c->Clear();
   c->SetCanvasSize(1200,600);
   c->Divide(2,1);
   auto recoGenPtHist = (TH2F *) eff->Get("analyzer/reco_gen_pt");
   recoGenPtHist->SetTitle("Crystal EG alg. momentum error");
   recoGenPtHist->GetYaxis()->SetTitle("Relative Error (reco-gen)/gen");
   auto oldAlgrecoGenPtHist = (TH2F *) eff->Get("analyzer/SLHCL1ExtraParticles:EGamma_reco_gen_pt");
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
