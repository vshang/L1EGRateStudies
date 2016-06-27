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



    # Add a variable to scale L1EG cluster pt to
    # RCT 2015 pt 
    print "Adding crystal_pt_to_RCT2015 to crystal_tree"
    from array import array
    effTree = eff.Get('analyzer/crystal_tree')
    rateTree = rates.Get('analyzer/crystal_tree')
    rateCorPt = array('f', [ 0 ] )
    rateCorPtB = rateTree.Branch('crystal_pt_to_RCT2015', rateCorPt, 'crystal_pt_to_RCT2015/F')
    effCorPt = array('f', [ 0 ] )
    effCorPtB = effTree.Branch('crystal_pt_to_RCT2015', effCorPt, 'crystal_pt_to_RCT2015/F')

    # For fit parameter values, run "drawPointsHists" in plotCutThresholds.py
    corFunc = ROOT.TF1('f1', '(-([0] + [1]*TMath::Exp(-[2]*x))+([3] + [4]*TMath::Exp(-[5]*x)))')
    corFunc.SetParameter( 0, -0.041252 )
    corFunc.SetParameter( 1, 0.252128 )
    corFunc.SetParameter( 2, 0.088619 )
    corFunc.SetParameter( 3, 0.113996 )
    corFunc.SetParameter( 4, -0.268292 )
    corFunc.SetParameter( 5, 0.072791 )

    cnt = 0
    for i in range(0, rateTree.GetEntries() ) :
        rateTree.GetEntry( i )
        cnt += 1
        if cnt % 1000 == 0 : print "Rates Tree: %i" % cnt
        pt = rateTree.cluster_pt
        rateCorPt[0] = pt + corFunc( pt )*pt
        rateCorPtB.Fill()
    rates.Write("", ROOT.TObject.kOverwrite)
    rates.Close() 

    cnt = 0
    for i in range(0, effTree.GetEntries() ) :
        effTree.GetEntry( i )
        cnt += 1
        if cnt % 1000 == 0 : print "Efficiency Tree: %i" % cnt
	pt = effTree.cluster_pt
        effCorPt[0] = pt + corFunc( pt )*pt
        effCorPtB.Fill()
    eff.Write("", ROOT.TObject.kOverwrite)
    eff.Close()




if __name__ == '__main__' :
    normalizeHists()


