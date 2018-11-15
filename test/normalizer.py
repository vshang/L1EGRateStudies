import ROOT
import L1Trigger.L1EGRateStudies.trigHelpers as trigHelpers

version = 'v9'

def makeEffGraph( numerator, denom ) :
    print "    Dividing " + numerator.GetName() + " by " + denom.GetName()
    graph = ROOT.TGraphAsymmErrors(numerator, denom)
    graph.GetXaxis().SetTitle(numerator.GetXaxis().GetTitle())
    graph.GetYaxis().SetTitle("Efficiency")
    graph.Write()

def normalizeHists() :
    effFiles = [
        'r2_phase2_singleElectron_20170820_flatIsoExt_all3.root',
        ]
    rateFiles = [
        ]

    # We need to renormalize everything since these files were parallel processed

    # Single Electron and Photon are idential 
    for fName in effFiles :
        file = ROOT.TFile( fName,  "UPDATE")
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

            # Track matched test
            effPtTrkMtchDenom_0p3 = file.Get("analyzer/gen_pt_trk_match_0p3")
            effPtTrkMtchDenom_0p1 = file.Get("analyzer/gen_pt_trk_match_0p1")
            effPtTrkMtchDenom_0p05 = file.Get("analyzer/gen_pt_trk_match_0p05")
            trk_0p3 = file.Get("analyzer/dyncrystalEG_efficiency_track_gen_match_pt_0p3")
            trk_0p1 = file.Get("analyzer/dyncrystalEG_efficiency_track_gen_match_pt_0p1")
            trk_0p05 = file.Get("analyzer/dyncrystalEG_efficiency_track_gen_match_pt_0p05")
            if effPtTrkMtchDenom_0p3 != None :
                pairs = [[effPtTrkMtchDenom_0p3, trk_0p3], [effPtTrkMtchDenom_0p1, trk_0p1], [effPtTrkMtchDenom_0p05, trk_0p05]]
                for pair in pairs :
                    denom = pair[0].Clone()
                    numerator = pair[1].Clone()
                    # Efficiency with gen track match as baseline
                    makeEffGraph( numerator, denom )
                    # Initial track to gen matching eff
                    denom = effPtDenom.Clone()
                    numerator = pair[0].Clone()
                    makeEffGraph( numerator, denom )



            

            dir_ = file.Get("analyzer")
            file.Write("", ROOT.TObject.kOverwrite)
        file.Close()


    doRate = True
    if doRate :
        for fName in rateFiles :
            file = ROOT.TFile( fName,  "UPDATE")
            rateHistKeys = trigHelpers.getKeysOfClass(file, "analyzer", "TH1F")
            if file.Get("analyzer/eventCount") != None :
                print "Normalizing rate histograms to 30MHz"
                nEvents = file.Get("analyzer/eventCount").GetBinContent(1)
                print "Total event count:", nEvents
                rateHists = trigHelpers.loadObjectsMatchingPattern(file, "analyzer", rateHistKeys, "*_rate*")
                dir_ = file.Get("analyzer")
                dir_.cd()
                for hist in rateHists :
                    hist.Sumw2()
                    hist.Scale(30000./nEvents)
                file.Write("", ROOT.TObject.kOverwrite)
            file.Close()



if __name__ == '__main__' :
    normalizeHists()


