import ROOT
import trigHelpers

version = 'v9'

def normalizeHists() :
    #eff = ROOT.TFile("r2_phase2_singleElectron_%s.root" % version, "UPDATE")
    #pho = ROOT.TFile("r2_phase2_singlePhoton_%s.root" % version, "UPDATE")
    #piZero = ROOT.TFile("r2_phase2_singlePiZero_%s.root" % version, "UPDATE")
    #rates = ROOT.TFile("r2_phase2_minBias_%s.root" % version, "UPDATE")
    effFiles = []
        'r2_phase2_singleElectron_top20.root',
        'r2_phase2_singleElectron_20170717noSkimRecoPerCard36v2.root',
        'r2_phase2_singleElectron_20170716top05.root',
        'r2_phase2_singleElectron_20170716top10.root',
        'r2_phase2_singleElectron_20170716top20.root',
        'r2_phase2_singleElectron_20170612v1.root',]
    rateFiles = [
        'r2_phase2_minBias_20170716top10.root',
        'r2_phase2_minBias_20170716top05.root',
        'r2_phase2_minBias_20170716top20.root',
        'r2_phase2_minBias_20170717noSkimRecoPerCard36v2.root',
        'r2_phase2_minBias_20170612v1.root']

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
                #dir_.Delete("eventCount*")
                file.Write("", ROOT.TObject.kOverwrite)
            file.Close()



if __name__ == '__main__' :
    normalizeHists()


