import ROOT
from trigHelpers import make_efficiency_graph, make_rate_hist, setLegStyle, checkDir
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

doEff = True
#doEff = False
doRate = True
doRate = False

c = ROOT.TCanvas('c', 'c', 600, 600)
p = ROOT.TPad('p','p', 0, 0, 1, 1)
p.Draw()
p.cd()


if doEff :
    fName = 'merged_QCD-PU200_OldP4Vec_0p5GeV'
    fName = 'merged_QCD-PU200_UsingET_0p5GeV'
    #fName = 'merged_TTbar-PU200_UsingET_0p5GeV'
    base = '/data/truggles/l1CaloJets_20181027/'
    universalSaveDir = "/afs/cern.ch/user/t/truggles/www/Phase-II/efficiencies/"
    checkDir( universalSaveDir )

    f = ROOT.TFile( base+fName+'.root', 'r' )
    t = f.Get('analyzer/tree')
    
    gP2 = make_efficiency_graph( t, 'abs(genJet_eta)<1.1', 'calibPtX > 100', 'genJet_pt', [60, 0, 300] )
    gS2 = make_efficiency_graph( t, 'abs(genJet_eta)<1.1', '(stage2jet_pt / 1.2) > 100', 'genJet_pt', [60, 0, 300] )
    
    gP2.SetLineColor(ROOT.kRed)
    gP2.SetLineWidth(2)
    gS2.SetLineColor(ROOT.kBlack)
    gS2.SetLineWidth(2)
    
    mg = ROOT.TMultiGraph("mg", "L1 Jet Efficiency")
    mg.Add( gP2 )
    mg.Add( gS2 )
    mg.Draw("aplez")
    mg.GetXaxis().SetTitle("Gen Jet p_{T}")
    mg.GetYaxis().SetTitle("L1 Algo. Efficiency w.r.t. Gen")
    p.SetGrid()
    
    
    leg = setLegStyle(0.5,0.3,0.9,0.7)
    leg.AddEntry(gS2, "Phase-I Jet Algo.","lpe")
    leg.AddEntry(gP2, "Phase-II Jet Algo.","lpe")
    leg.Draw("same")
    c.Update()
    
    
    c.SaveAs( universalSaveDir + fName + '_eff.png' )

""" MAKE RATES """
if doRate :
    fName = 'merged_minBias-PU200_PUTests_0p5GeV'
    base = '/data/truggles/l1CaloJets_20181024/'
    universalSaveDir = "/afs/cern.ch/user/t/truggles/www/Phase-II/rates/"
    checkDir( universalSaveDir )

    f = ROOT.TFile( base+fName+'.root', 'r' )
    print f
    t = f.Get('analyzer/tree')

    nEvents = f.Get('analyzer/nEvents').Integral()
    eta_threshold = 1.1
    x_info = [56, 20, 300]
    
    hP2 = make_rate_hist( nEvents, t, 'calibPtX', 1.0, 'jet_eta', eta_threshold, x_info ) 
    hP2.SaveAs( fName+'_Phase-2.root' )
    hS2 = make_rate_hist( nEvents, t, 'stage2jet_pt', 1./1.2, 'stage2jet_eta', eta_threshold, x_info )
    hS2.SaveAs( fName+'_Stage-2.root' )
    del hP2, hS2
    
    f1 = ROOT.TFile( fName+'_Phase-2.root', 'r')
    hP2 = f1.Get('cumul')
    f2 = ROOT.TFile( fName+'_Stage-2.root', 'r')
    hS2 = f2.Get('cumul')
    
    hP2.SetLineColor(ROOT.kRed)
    hP2.SetLineWidth(2)
    hS2.SetLineColor(ROOT.kBlack)
    hS2.SetLineWidth(2)
    
    #hP2.GetXaxis().SetRangeUser(20, 200)
    #hS2.GetXaxis().SetRangeUser(20, 200)
    
    hP2.SetTitle("L1 Algo. Rates")
    hP2.GetXaxis().SetTitle("Reco Jet p_{T}")
    hP2.GetYaxis().SetTitle("L1 Algo. Rate (kHz)")
    hP2.Draw()
    hS2.Draw('SAME')
    
    
    p.SetGrid()
    p.SetLogy()
    p.SetLeftMargin( .13 )
    p.SetBottomMargin( .1 )
    
    
    leg = setLegStyle(0.5,0.55,0.9,0.85)
    leg.AddEntry(hS2, "Phase-I Jet Algo.","lpe")
    leg.AddEntry(hP2, "Phase-II Jet Algo.","lpe")
    leg.Draw("same")
    c.Update()
    
    
    c.SaveAs( universalSaveDir + fName +  '_rate.png' )



