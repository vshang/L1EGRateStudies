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

void drawCDFs(TCanvas * c, TTree * rate, TTree * eff, std::string variable, std::string var_cuts, std::string cut, double max) {
    std::string prefix(c->GetName());
    std::string var_name(c->GetTitle());
    TF1 * cutFunction = new TF1((prefix+"_cut").c_str(), cut.c_str(), ., 50.);
    c->Divide(2,1);

    c->cd(2);
    gPad->SetRightMargin(0.13);
    TH2F * rate_cdf = new TH2F((prefix+"_rate_cdf").c_str(), ("Background;Cluster pT;"+var_name).c_str(), 60, 0., 50., 50, 0., max);
    rate->Draw((variable+":cluster_pt >> "+prefix+"_rate_cdf").c_str(), var_cuts.c_str(), "goff");
    rate_cdf->GetYaxis()->SetTitleOffset(1.4);
    rate_cdf->Draw("colz");
    cutFunction->Draw("lsame");

    c->cd(1);
    gPad->SetRightMargin(0.13);
    TH2F * eff_cdf = new TH2F((prefix+"_eff_cdf").c_str(), ("Single Electron signal;Cluster pT;"+var_name).c_str(), 60, 0., 50., 50, 0., max);
    eff->Draw((variable+":cluster_pt >> "+prefix+"_eff_cdf").c_str(), var_cuts.c_str(), "goff");
    eff_cdf->GetYaxis()->SetTitleOffset(1.4);
    eff_cdf->Draw("colz");
    cutFunction->Draw("lsame");

    c->Print(("plots/"+std::string(c->GetName())+"_pdf.png").c_str());
    c->Clear();

    createCDF(rate_cdf, true);
    createCDF(eff_cdf);
    double contours[] = {0., 0.5, 1-exp(-1), 1-exp(-2), 1-exp(-3), 1-exp(-4)};
    eff_cdf->SetContour(6, contours);

    c->Divide(2,1);
    c->cd(1);
    gPad->SetRightMargin(0.13);
    eff_cdf->GetZaxis()->SetTitle("Cumulative event fraction (<cut)");
    eff_cdf->Draw("colz");
    cutFunction->Draw("lsame");
    c->cd(2);
    gPad->SetRightMargin(0.13);
    rate_cdf->GetZaxis()->SetTitle("Cumulative event fraction (>cut)");
    rate_cdf->Draw("colz");
    cutFunction->Draw("lsame");

    c->Print(("plots/"+std::string(c->GetName())+"_cdf.png").c_str());
    c->Clear();
}

void cutStudy(){
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

    TCanvas * c = new TCanvas("canvas", "canvas", 1200, 600);

    c->SetName("hovere");
    c->SetTitle("H/E Value");
    // endcap: "22./x+0."
    drawCDFs(c, rate, eff, "cluster_hovere", "", "14/x+.05", 5);

    c->SetName("isolation");
    c->SetTitle("Isolation Value");
    // endcap: "64/x+0.1"
    drawCDFs(c, rate, eff, "cluster_iso", "", "40/x+0.1", 15);

    c->SetName("ptratio");
    c->SetTitle("Pt Ratio Value");
    // endcap: "0.18*(1-x/70)*(x<40)+.18*3/7*(x>40)"
    drawCDFs(c, rate, eff, "pt.5/(pt.1+pt.2)", "", "0.18*(1-x/100)*(x<30)+.18*.7*(x>30)", 0.3);


}
