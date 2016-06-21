import ROOT
import trigHelpers

def normalizeHists() :
    eff = ROOT.TFile("egTriggerEff.root", "UPDATE")
    rates = ROOT.TFile("egTriggerRates.root", "UPDATE")

    # We need to renormalize everything since these files were parallel processed
 
    effHistKeys = trigHelpers.getKeysOfClass(eff, "analyzer", "TH1F")
    effPtDenom = eff.Get("analyzer/gen_pt")
    effEtaDenom = eff.Get("analyzer/gen_eta")
    effRecoPtDenom = eff.Get("analyzer/reco_pt")
    if effPtDenom != None :
        print "Creating efficiency histograms"
	print "Eff hists in 2 categories 1) gen / gen and 2) reco / reco"
        print "Total event count: %f" % effPtDenom.Integral()
        print "Total offline reco event count: %f" % effRecoPtDenom.Integral()

       
        eff.cd("analyzer") 
        effPtHists = trigHelpers.loadObjectsMatchingPattern( eff, "analyzer", effHistKeys, "*_efficiency*pt" )
        for hist in effPtHists :
            if "reco_" not in hist.GetName() :
                denom = effPtDenom.Clone()
            if "reco_" in hist.GetName() :
                denom = effRecoPtDenom.Clone()
            print "    Dividing " + hist.GetName() + " by " + denom.GetName()
            graph = ROOT.TGraphAsymmErrors(hist, denom)
            graph.GetXaxis().SetTitle(hist.GetXaxis().GetTitle())
            graph.GetYaxis().SetTitle("Efficiency")
            graph.Write()


        effEtaHists = trigHelpers.loadObjectsMatchingPattern(eff, "analyzer", effHistKeys, "*_efficiency*eta")
        effEtaDenom.Sumw2()
        for hist in effEtaHists :
            graph = ROOT.TGraphAsymmErrors(hist, effEtaDenom)
            graph.GetXaxis().SetTitle(hist.GetXaxis().GetTitle())
            graph.GetYaxis().SetTitle("Efficiency")
            graph.Write()

        dir_ = eff.Get("analyzer")
        #dir_.Delete("gen_pt*")
        #dir_.Delete("gen_eta*")
        eff.Write("", ROOT.TObject.kOverwrite)


    rateHistKeys = trigHelpers.getKeysOfClass(rates, "analyzer", "TH1F")
    if rates.Get("analyzer/eventCount") != None :
        print "Normalizing rate histograms to 30MHz"
        nEvents = rates.Get("analyzer/eventCount").GetBinContent(1)
        print "Total event count:", nEvents
        rateHists = trigHelpers.loadObjectsMatchingPattern(rates, "analyzer", rateHistKeys, "*_rate*")
        dir_ = rates.Get("analyzer")
        dir_.cd()
        for hist in rateHists :
            hist.Sumw2()
            hist.Scale(30000./nEvents)
        #dir_.Delete("eventCount*")
        rates.Write("", ROOT.TObject.kOverwrite)



if __name__ == '__main__' :
    normalizeHists()


