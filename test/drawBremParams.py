import ROOT


def drawBremParams() :
    effFile = ROOT.TFile("egTriggerEff.root", "r")
    tree = effFile.Get("analyzer/crystal_tree")
    rateFile = ROOT.TFile("egTriggerRates.root", "r")
    rate_tree = rateFile.Get("analyzer/crystal_tree")
    
    c = ROOT.TCanvas()
    tree.Draw("crystalCount : corePt/gen_pt", "cluster_pt>5", "colz")
    c.Print("plots/crystalCount_vs_ptloss.png")
    tree.Draw("bremStrength : corePt/gen_pt", "cluster_pt>5", "colz")
    c.Print("plots/bremStrength_vs_ptloss_full.png")
    tree.Draw("bremStrength : E_core/E_gen", "cluster_pt>5", "colz")
    c.Print("plots/bremStrength_vs_Eloss_full.png")
    tree.Draw("bremStrength : corePt/gen_pt", "cluster_pt>5 && bremStrength < 0.95", "colz")
    c.Print("plots/bremStrength_vs_ptloss.png")
    tree.Draw("bremStrength : E_core/E_gen", "cluster_pt>5 && bremStrength < 0.95", "colz")
    c.Print("plots/bremStrength_vs_Eloss.png")

    tree.Draw("phiStripContiguous0 : corePt/gen_pt", "cluster_pt>5", "colz")
    c.Print("plots/phiStripContiguous0_vs_ptloss.png")
    tree.Draw("phiStripOneHole0 : corePt/gen_pt", "cluster_pt>5", "colz")
    c.Print("plots/phiStripOneHole0_vs_ptloss.png")
    tree.Draw("phiStripContiguous3p : corePt/gen_pt", "cluster_pt>5", "colz")
    c.Print("plots/phiStripContiguous3p_vs_ptloss.png")
    tree.Draw("phiStripOneHole3p : corePt/gen_pt", "cluster_pt>5", "colz")
    c.Print("plots/phiStripOneHole3p_vs_ptloss.png")

    htemp = ROOT.TH1F("htemp", "htemp", 1, 0, 1000)
    tree.Draw("cluster_pt >> htemp", "passed && cluster_pt > 15")
    electronTotal = htemp.Integral()
    rate_tree.Draw("cluster_pt >> htemp", "passed && cluster_pt > 15")
    fakeTotal = htemp.Integral()

    thresholds = [0.9, 0.8, 0.7, 0.6]
    print "\nThreshold : Rate : Fake"
    for threshold in thresholds :
        tree.Draw("cluster_pt >> htemp", ("passed && cluster_pt > 15 && bremStrength < "+str(threshold)))
        electronPass = htemp.Integral()
        rate_tree.Draw("cluster_pt >> htemp", ("passed && cluster_pt > 15 && bremStrength < "+str(threshold)))
        fakePass = htemp.Integral()
        print str(threshold) + " & " + str(round(electronPass*100./electronTotal,3)) + " & " + str(round(fakePass*100./fakeTotal,3)) + " \\\\"


if __name__ == '__main__' :
    drawBremParams()
