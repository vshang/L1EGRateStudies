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
    std::string cutstring = "!endcap";

    gStyle->SetOptStat(0);
    gStyle->SetTitleFont(42, "p");
    gStyle->SetTitleColor(1);
    gStyle->SetTitleTextColor(1);
    gStyle->SetTitleFillColor(10);
    gStyle->SetTitleFontSize(0.05);
    gStyle->SetTitleOffset(1.2, "XYZ");
    gStyle->SetTitleFont(42, "XYZ");
    gStyle->SetLabelFont(42, "XYZ");

    TFile *_file0 = TFile::Open("egTriggerEff.root");
    TFile *_file1 = TFile::Open("egTriggerRates.root");
    TTree * eff = (TTree*) _file0->Get("analyzer/crystal_tree");
    TTree * rate = (TTree*) _file1->Get("analyzer/crystal_tree");

    TH2F * hovere_hist_sig = new TH2F("hovere_hist_sig", "Single Electron Signal;Cluster pT;H/E Value", 60, 0., 50., 80, 0., 5.);
    TH2F * hovere_hist_bg = new TH2F("hovere_hist_bg", "Background;Cluster pT;H/E Value", 60, 0., 50., 80, 0., 5.);
    eff->Draw("cluster_hovere:cluster_pt >> hovere_hist_sig", (""+cutstring).c_str(), "goff");
    rate->Draw("cluster_hovere:cluster_pt >> hovere_hist_bg", (""+cutstring).c_str(), "goff");
    TH2F * iso_hist_sig = new TH2F("iso_hist_sig", "Single Electron Signal;Cluster pT;Isolation Value", 60, 0., 50., 80, 0., 15.);
    TH2F * iso_hist_bg = new TH2F("iso_hist_bg", "Background;Cluster pT;Isolation Value", 60, 0., 50., 80, 0., 15.);
    eff->Draw("cluster_iso:cluster_pt >> iso_hist_sig", (""+cutstring).c_str(), "goff");
    rate->Draw("cluster_iso:cluster_pt >> iso_hist_bg", (""+cutstring).c_str(), "goff");

    TCanvas * c = new TCanvas("canvas", "scatter canvas", 1200, 600);
    c->Divide(2,1);
    c->cd(1);
    hovere_hist_sig->DrawCopy("col");
    c->cd(2);
    hovere_hist_bg->DrawCopy("col");
    c->Print("plots/hovere_scatter.png");

    createCDF(hovere_hist_sig);
    createCDF(hovere_hist_bg, true);

    TF1 * hoecut = new TF1("hoecut", "[0]/x+[1]", 1e-3, 50);
    hoecut->SetParameters(14., 0.05);
    hoecut->SetLineColor(kBlack);
    TF1 * hoecut_endcap = new TF1("hoecut_endcap", "22./x+0.", 1e-3, 50);
    hoecut_endcap->SetLineColor(kGray-2);
    hoecut_endcap->SetLineStyle(kDashed);

    double contours[] = {0., 0.5, 1-exp(-1), 1-exp(-2), 1-exp(-3), 1-exp(-4)};
    TCanvas * c2 = new TCanvas("intcanvas", "integral canvas", 1200, 600);
    c2->Divide(2,1);
    c2->cd(1);
    gPad->SetRightMargin(0.13);
    hovere_hist_sig->SetContour(6, contours);
    hovere_hist_sig->GetZaxis()->SetTitle("Cumulative event fraction (<cut)");
    hovere_hist_sig->Draw("colz");
    hoecut->Draw("lsame");
    hoecut_endcap->Draw("lsame");
    c2->cd(2);
    gPad->SetRightMargin(0.13);
    hovere_hist_bg->GetZaxis()->SetTitle("Cumulative event fraction (>cut)");
    hovere_hist_bg->Draw("colz");
    hoecut->Draw("lsame");
    hoecut_endcap->Draw("lsame");
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
    
    TF1 * isocut = new TF1("isocut", "[0]/x+[1]", 1e-3, 50);
    isocut->SetParameters(40., 0.1);
    isocut->SetLineColor(kBlack);
    TF1 * isocut_endcap = new TF1("isocut_endcap", "64./x+0.1", 1e-3, 50);
    isocut_endcap->SetLineColor(kGray-2);
    isocut_endcap->SetLineStyle(kDashed);

    TCanvas * c4 = new TCanvas("isointcanvas", "integral canvas", 1200, 600);
    c4->Divide(2,1);
    c4->cd(1);
    gPad->SetRightMargin(0.13);
    iso_hist_sig->SetContour(6, contours);
    iso_hist_sig->GetZaxis()->SetTitle("Cumulative event fraction (<cut)");
    iso_hist_sig->Draw("colz");
    isocut->Draw("lsame");
    isocut_endcap->Draw("lsame");
    c4->cd(2);
    gPad->SetRightMargin(0.13);
    iso_hist_bg->GetZaxis()->SetTitle("Cumulative event fraction (>cut)");
    iso_hist_bg->Draw("colz");
    isocut->Draw("lsame");
    isocut_endcap->Draw("lsame");
    c4->Print("plots/isolation_cdf.png");

    TCanvas * c5 = new TCanvas("ptratio_canvas", "ptratio_canvas", 700, 600);
    TH1F * ptratio_rate = new TH1F("ptratio_rate", "Background", 50, 0, 0.2);
    rate->Draw("pt.5/(pt.1+pt.2) >> ptratio_rate", ("cluster_pt > 10. && "+cutstring).c_str(), "goff");
    ptratio_rate->SetLineColor(kRed);
    ptratio_rate->Sumw2();
    ptratio_rate->Scale(1./ptratio_rate->Integral());
    TH1F * ptratio_eff = new TH1F("ptratio_eff", "Single electron signal", 50, 0, 0.2);
    eff->Draw("pt.5/(pt.1+pt.2) >> ptratio_eff", ("cluster_pt > 10. && "+cutstring).c_str(), "goff");
    ptratio_eff->Sumw2();
    ptratio_eff->Scale(1./ptratio_eff->Integral());
    THStack * ptratio_stack = new THStack("ptratio_stack", "Pt ratio cut parameter;pt.5/(pt.1+pt.2);Fraction of Events");
    ptratio_stack->Add(ptratio_rate, "hist ex0");
    ptratio_stack->Add(ptratio_eff, "hist ex0");
    ptratio_stack->Draw("nostack");
    ptratio_stack->GetYaxis()->SetTitleOffset(1.3);
    setLegStyle(c5->BuildLegend());
    c5->Print("plots/pt5_over_pt1+2_clustergt10.png");

    TCanvas * c6 = new TCanvas("ptratio_2dcanvas", "ptratio_2dcanvas", 1200, 600);
    TF1 * ratiocut = new TF1("ratiocut", "0.18*(1-x/100)*(x<30)+.18*.7*(x>30)", 0., 50.);
    TF1 * ratiocut_endcap = new TF1("ratiocut_endcap", "0.18*(1-x/70)*(x<40)+.18*3/7*(x>40)", 0., 50.);
    ratiocut_endcap->SetLineColor(kGray-2);
    ratiocut_endcap->SetLineStyle(kDashed);
    c6->Divide(2,1);
    c6->cd(2);
    gPad->SetRightMargin(0.13);
    TH2F * ptratio2_rate = new TH2F("ptratio2_rate", "Background;Cluster pT;pt.5/(pt.1+pt.2)", 50, 0., 50., 50, 0., 0.3);
    rate->Draw("pt.5/(pt.1+pt.2) : cluster_pt >> ptratio2_rate", (""+cutstring).c_str(), "goff");
    createCDF(ptratio2_rate, true);
    ptratio2_rate->GetZaxis()->SetTitle("Cumulative event fraction (>cut)");
    ptratio2_rate->GetYaxis()->SetTitleOffset(1.4);
    ptratio2_rate->Draw("colz");
    ratiocut->Draw("lsame");
    ratiocut_endcap->Draw("lsame");
    c6->cd(1);
    gPad->SetRightMargin(0.13);
    TH2F * ptratio2_eff = new TH2F("ptratio2_eff", "Single electron signal;Cluster pT;pt.5/(pt.1+pt.2)", 50, 0., 50., 50, 0., 0.3);
    eff->Draw("pt.5/(pt.1+pt.2) : cluster_pt >> ptratio2_eff", (""+cutstring).c_str(), "goff");
    ptratio2_eff->SetContour(6, contours);
    createCDF(ptratio2_eff);
    ptratio2_eff->GetZaxis()->SetTitle("Cumulative event fraction (<cut)");
    ptratio2_eff->GetYaxis()->SetTitleOffset(1.4);
    ptratio2_eff->Draw("colz");
    ratiocut->Draw("lsame");
    ratiocut_endcap->Draw("lsame");
    c6->Print("plots/pt5_over_pt1+2_2d.png");
}
