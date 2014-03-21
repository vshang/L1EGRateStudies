void drawRateEff() {
	TFile rates("egTriggerRates.root");
	TFile eff("egTriggerEff.root");

	TH1F * oldrate = (TH1F *) rates.Get("analyzer/Old stage-2 EG");
	TH1F * srate   = (TH1F *) rates.Get("analyzer/Crystal-level EG");
	TH1F * oldeff  = (TH1F *) eff.Get("analyzer/Old stage-2 EG");
	TH1F * seff    = (TH1F *) eff.Get("analyzer/Crystal-level EG");

   {
      TCanvas rate_canvas("crate","c1");
      gPad->SetLogy(1);
      gPad->SetGridx(1);
      gPad->SetGridy(1);
      gStyle->SetOptStat(0);
      oldrate->SetLineColor(kRed);
      oldrate->Draw();
      srate->Draw("same");
   //   oldrate->GetXaxis()->SetTitle("ET Threshold (GeV)");
   //   oldrate->GetYaxis()->SetTitle("Rate (kHz)");
      oldrate->SetTitle("EG rates (neutrino gun PU140 bx25)");
      TLegend *leg = new TLegend(0.65,0.75,0.9,0.9,NULL,"brNDC");
            leg->SetBorderSize(0);
            leg->SetLineColor(1);
            leg->SetLineStyle(1);
            leg->SetLineWidth(.3);
            leg->SetFillColor(0);
            leg->SetFillStyle(0);
            leg->SetTextFont(20);
      leg->AddEntry(oldrate,"stage-2 alg.","l");
      leg->AddEntry(srate,"crystal-level alg.","l");
      leg->Draw("same");

      rate_canvas.Print("EGRates.png");
   }
   {
      TCanvas canvas("ceff","c1");
      gPad->SetLogy(0);
      gPad->SetGridx(1);
      gPad->SetGridy(1);
      gStyle->SetOptStat(0);
      oldeff->SetLineColor(kRed);
      oldeff->Draw();
      seff->Draw("same");
   //   oldeff->GetXaxis()->SetTitle("ET Threshold (GeV)");
      oldeff->GetYaxis()->SetTitle("#epsilon");
      oldeff->SetTitle("EG Efficiencies (single-electron PU140 bx25)");
      TLegend *leg = new TLegend(0.65,0.75,0.9,0.9,NULL,"brNDC");
            leg->SetBorderSize(0);
            leg->SetLineColor(1);
            leg->SetLineStyle(1);
            leg->SetLineWidth(.3);
            leg->SetFillColor(0);
            leg->SetFillStyle(0);
            leg->SetTextFont(20);
      leg->AddEntry(oldeff,"stage-2 alg.","l");
      leg->AddEntry(seff,"crystal-level alg.","l");
      leg->Draw("same");

      canvas.Print("EGEfficiencies.png");
   }
}
