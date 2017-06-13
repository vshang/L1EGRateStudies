import ROOT
import trigHelpers

version = 'v9'

def normalizeHists() :
    eff = ROOT.TFile("r2_phase2_singleElectron_%s.root" % version, "UPDATE")
    pho = ROOT.TFile("r2_phase2_singlePhoton_%s.root" % version, "UPDATE")
    piZero = ROOT.TFile("r2_phase2_singlePiZero_%s.root" % version, "UPDATE")
    rates = ROOT.TFile("r2_phase2_minBias_%s.root" % version, "UPDATE")

    # We need to renormalize everything since these files were parallel processed

    # Single Electron and Photon are idential 
    for file in [eff, pho, piZero, ] :
        effHistKeys = trigHelpers.getKeysOfClass(file, "analyzer", "TH1F")
        effPtDenom = file.Get("analyzer/gen_pt")
        effEtaDenom = file.Get("analyzer/gen_eta")
        effRecoPtDenom = file.Get("analyzer/reco_pt")
        if effPtDenom != None :
            print "Creating efficiency histograms"
            print "Eff hists in 2 categories 1) gen / gen and 2) reco / reco"
            print "Total event count: %f" % effPtDenom.Integral()
            print "Total offline reco event count: %f" % effRecoPtDenom.Integral()

           
            file.cd("analyzer") 
            effPtHists = trigHelpers.loadObjectsMatchingPattern( file, "analyzer", effHistKeys, "*_efficiency*pt" )
            for hist in effPtHists :
                #if "reco_" not in hist.GetName() :
                #    denom = effPtDenom.Clone()
                #if "reco_" in hist.GetName() :
                #    denom = effRecoPtDenom.Clone()
                denom = effPtDenom.Clone()
                print "    Dividing " + hist.GetName() + " by " + denom.GetName()
                graph = ROOT.TGraphAsymmErrors(hist, denom)
                graph.GetXaxis().SetTitle(hist.GetXaxis().GetTitle())
                graph.GetYaxis().SetTitle("Efficiency")
                graph.Write()


            effEtaHists = trigHelpers.loadObjectsMatchingPattern(file, "analyzer", effHistKeys, "*_efficiency*eta")
            effEtaDenom.Sumw2()
            for hist in effEtaHists :
                denom = effEtaDenom.Clone()
                print "    Dividing " + hist.GetName() + " by " + denom.GetName()
                graph = ROOT.TGraphAsymmErrors(hist, denom)
                graph.GetXaxis().SetTitle(hist.GetXaxis().GetTitle())
                graph.GetYaxis().SetTitle("Efficiency")
                graph.Write()

            dir_ = file.Get("analyzer")
            #dir_.Delete("gen_pt*")
            #dir_.Delete("gen_eta*")
            file.Write("", ROOT.TObject.kOverwrite)


    doRate = False
    if doRate :
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


