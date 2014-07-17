void createCDF(TH2F * hist, bool invert = false) {
    for(int i=0; i<=hist->GetNbinsX()+1; ++i) {
        double integral = hist->Integral(i, i, 0, hist->GetNbinsY()+1);
        if (integral == 0) continue;
        for(int j=0; j<=hist->GetNbinsY()+1; ++j) {
            hist->SetBinContent(i, j, hist->GetBinContent(i, j)/integral);
        }
        integral = 0;
        for(int j=1; j<=hist->GetNbinsY()+1; ++j) {
            integral += hist->GetBinContent(i, j);
            hist->SetBinContent(i, j, (invert)? 1-integral:integral);
        }
    }
}

void setLegStyle(TLegend * leg) {
   leg->SetBorderSize(0);
   leg->SetLineColor(1);
   leg->SetLineStyle(1);
   leg->SetLineWidth(.3);
   leg->SetFillColor(0);
   leg->SetFillStyle(0);
}

void cutStudy(){
    gStyle->SetOptStat(0);
    TFile *_file0 = TFile::Open("egTriggerEff.root");
    TFile *_file1 = TFile::Open("egTriggerRates.root");
    TTree * eff = (TTree*) _file0->Get("analyzer/crystal_tree");
    TTree * rate = (TTree*) _file1->Get("analyzer/crystal_tree");

    TH2F * hovere_hist_sig = new TH2F("hovere_hist_sig", "H/E scatter (signal);Cluster pT;H/E Value", 60, 0., 50., 80, 0., 5.);
    TH2F * hovere_hist_bg = new TH2F("hovere_hist_bg", "H/E scatter (background);Cluster pT;H/E Value", 60, 0., 50., 80, 0., 5.);
    eff->Draw("cluster_hovere:cluster_pt >> hovere_hist_sig", "", "goff");
    rate->Draw("cluster_hovere:cluster_pt >> hovere_hist_bg", "", "goff");
    TH2F * iso_hist_sig = new TH2F("iso_hist_sig", "Isolation scatter (signal);Cluster pT;Isolation Value", 60, 0., 50., 80, 0., 15.);
    TH2F * iso_hist_bg = new TH2F("iso_hist_bg", "Isolation scatter (background);Cluster pT;Isolation Value", 60, 0., 50., 80, 0., 15.);
    eff->Draw("cluster_iso:cluster_pt >> iso_hist_sig", "", "goff");
    rate->Draw("cluster_iso:cluster_pt >> iso_hist_bg", "", "goff");

    TCanvas * c = new TCanvas("canvas", "scatter canvas", 1200, 600);
    c->Divide(2,1);
    c->cd(1);
    hovere_hist_sig->DrawCopy("col");
    c->cd(2);
    hovere_hist_bg->DrawCopy("col");
    c->Print("plots/hovere_scatter.png");

    createCDF(hovere_hist_sig);
    createCDF(hovere_hist_bg, true);

    TF1 * cut = new TF1("cut", "[0]/x+[1]", 1e-3, 50);
    cut->SetParameters(14., 0.05);
    cut->SetLineColor(kBlack);
    TF1 * oldcut = new TF1("oldcut", "0.5+(35-x+(x-35)*(35<x))**2/350", 1e-3, 50);
    oldcut->SetLineColor(kGray-2);
    oldcut->SetLineStyle(kDashed);

    double contours[] = {0., 0.5, 1-exp(-1), 1-exp(-2), 1-exp(-3), 1-exp(-4)};
    TCanvas * c2 = new TCanvas("intcanvas", "integral canvas", 1200, 600);
    c2->Divide(2,1);
    c2->cd(1);
    hovere_hist_sig->SetContour(6, contours);
    hovere_hist_sig->Draw("colz");
    cut->Draw("lsame");
    oldcut->Draw("lsame");
    c2->cd(2);
    hovere_hist_bg->Draw("colz");
    cut->Draw("lsame");
    oldcut->Draw("lsame");
    c2->Print("plots/hovere_cdf.png");

    TCanvas * c3 = new TCanvas("isocanvas", "scatter canvas", 1200, 600);
    c3->Divide(2,1);
    c3->cd(1);
    iso_hist_sig->DrawCopy("col");
    c3->cd(2);
    iso_hist_bg->DrawCopy("col");
    c3->Print("plots/isolation_scatter.png");

    createCDF(iso_hist_sig);
    createCDF(iso_hist_bg, true);
    
    TF1 * isocut = new TF1("cut", "[0]/x+[1]", 1e-3, 50);
    isocut->SetParameters(40., 0.1);
    isocut->SetLineColor(kBlack);
    TF1 * oldisocut = new TF1("oldcut", "1.3+(35-x+(x-35)*(35<x))**2/306.25", 1e-3, 50);
    oldisocut->SetLineColor(kGray-2);
    oldisocut->SetLineStyle(kDashed);

    TCanvas * c4 = new TCanvas("isointcanvas", "integral canvas", 1200, 600);
    c4->Divide(2,1);
    c4->cd(1);
    iso_hist_sig->SetContour(6, contours);
    iso_hist_sig->Draw("colz");
    isocut->Draw("lsame");
    oldisocut->Draw("lsame");
    c4->cd(2);
    iso_hist_bg->Draw("colz");
    isocut->Draw("lsame");
    oldisocut->Draw("lsame");
    c4->Print("plots/isolation_cdf.png");

    TCanvas * c5 = new TCanvas("ptratio_canvas", "ptratio_canvas", 700, 600);
    TH1F * ptratio_rate = new TH1F("ptratio_rate", "Single electron signal", 50, 0, 0.2);
    rate->Draw("pt.5/(pt.1+pt.2) >> ptratio_rate", "cluster_pt > 10.", "goff");
    ptratio_rate->SetLineColor(kRed);
    ptratio_rate->Sumw2();
    ptratio_rate->Scale(1./ptratio_rate->Integral());
    TH1F * ptratio_eff = new TH1F("ptratio_eff", "Background", 50, 0, 0.2);
    eff->Draw("pt.5/(pt.1+pt.2) >> ptratio_eff", "cluster_pt > 10.", "goff");
    ptratio_eff->Sumw2();
    ptratio_eff->Scale(1./ptratio_eff->Integral());
    THStack * ptratio_stack = new THStack("ptratio_stack", "Pt ratio cut parameter;pt.5/(pt.1+pt.2);Fraction of Events");
    ptratio_stack->Add(ptratio_rate, "hist ex0");
    ptratio_stack->Add(ptratio_eff, "hist ex0");
    ptratio_stack->Draw("nostack");
    ptratio_stack->GetYaxis()->SetTitleOffset(1.3);
    setLegStyle(c5->BuildLegend());
    c5->Print("plots/pt5_over_pt1+2_clustergt10.png");
}
