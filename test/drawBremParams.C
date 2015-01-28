#include <iostream>
#include <vector>
#include <iomanip>

#include "TCanvas.h"
#include "TH1F.h"
#include "TH2F.h"
#include "TFile.h"
#include "TLatex.h"
#include "TLegend.h"
#include "TStyle.h"
#include "TTree.h"

void drawBremParams () {
    TFile *_file0 = TFile::Open("egTriggerEff.root");
    TTree * tree = (TTree*) _file0->Get("analyzer/crystal_tree");
    TFile *_file1 = TFile::Open("egTriggerRates.root");
    TTree * rate_tree = (TTree*) _file1->Get("analyzer/crystal_tree");
    
    TCanvas * c = new TCanvas();
    tree->Draw("crystalCount : corePt/gen_pt", "cluster_pt>5", "colz");
    c->Print("plots/crystalCount_vs_ptloss.png");
    tree->Draw("bremStrength : corePt/gen_pt", "cluster_pt>5", "colz");
    c->Print("plots/bremStrength_vs_ptloss_full.png");
    tree->Draw("bremStrength : E_core/E_gen", "cluster_pt>5", "colz");
    c->Print("plots/bremStrength_vs_Eloss_full.png");
    tree->Draw("bremStrength : corePt/gen_pt", "cluster_pt>5 && bremStrength < 0.95", "colz");
    c->Print("plots/bremStrength_vs_ptloss.png");
    tree->Draw("bremStrength : E_core/E_gen", "cluster_pt>5 && bremStrength < 0.95", "colz");
    c->Print("plots/bremStrength_vs_Eloss.png");

    tree->Draw("phiStripContiguous0 : corePt/gen_pt", "cluster_pt>5", "colz");
    c->Print("plots/phiStripContiguous0_vs_ptloss.png");
    tree->Draw("phiStripOneHole0 : corePt/gen_pt", "cluster_pt>5", "colz");
    c->Print("plots/phiStripOneHole0_vs_ptloss.png");
    tree->Draw("phiStripContiguous3p : corePt/gen_pt", "cluster_pt>5", "colz");
    c->Print("plots/phiStripContiguous3p_vs_ptloss.png");
    tree->Draw("phiStripOneHole3p : corePt/gen_pt", "cluster_pt>5", "colz");
    c->Print("plots/phiStripOneHole3p_vs_ptloss.png");

    TH1F * htemp = new TH1F("htemp", "htemp", 1, 0, 1000);
    tree->Draw("cluster_pt >> htemp", "passed && cluster_pt > 15");
    float electronTotal = htemp->Integral();
    rate_tree->Draw("cluster_pt >> htemp", "passed && cluster_pt > 15");
    float fakeTotal = htemp->Integral();

    std::vector<float> thresholds({0.9, 0.8, 0.7, 0.6});
    for(auto& threshold : thresholds)
    {
        tree->Draw("cluster_pt >> htemp", ("passed && cluster_pt > 15 && bremStrength < "+std::to_string(threshold)).c_str());
        float electronPass = htemp->Integral();
        rate_tree->Draw("cluster_pt >> htemp", ("passed && cluster_pt > 15 && bremStrength < "+std::to_string(threshold)).c_str());
        float fakePass = htemp->Integral();
        std::cout << threshold << " & " << std::setprecision(3) << electronPass*100./electronTotal << " & " << fakePass*100./fakeTotal << " \\\\" << std::endl;
    }
}
