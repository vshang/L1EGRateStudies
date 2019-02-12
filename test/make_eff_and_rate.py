import ROOT
from L1Trigger.L1EGRateStudies.trigHelpers import make_efficiency_graph, make_rate_hist, setLegStyle, checkDir
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
    fName = 'ttbar_PU200_v2'
    base = '/data/truggles/l1CaloJets_20190210/'
    date = '20190210'
    universalSaveDir = '/afs/cern.ch/user/t/truggles/www/Phase-II/efficiencies/20190210_PU_calib_comp/'+date+'_V3'
    checkDir( universalSaveDir )

    f = ROOT.TFile( base+fName+'.root', 'r' )
    t = f.Get('analyzer/tree')
    

    # Threshold cuts for passing region
    pt_cut = 100
    pt_cut = 50
    #pt_cut = 150
    #pt_cut = 200
    #pt_cut = 400
    #pt_cut = 100
    #pt_cut = 0

    """ Pt Eff """
    # Use eta cuts to restrict when doing pT efficiencies
    denom_cut = 'abs(genJet_eta)<1.2'
    axis = [160, 0, 400]
    gP2 = make_efficiency_graph( t, denom_cut, 'calibPtAA > %i' % pt_cut, 'genJet_pt', axis )
    gS2 = make_efficiency_graph( t, denom_cut, '(stage2jet_pt_calibration3) > %i' % pt_cut, 'genJet_pt', axis )

    """ Eta Eff """
    # Use pt cuts to restrict included objects when doing eta efficiencies
    #denom_cut = '(genJet_pt > 50)'
    #axis = [100, -5, 5]
    #gP2 = make_efficiency_graph( t, denom_cut, 'calibPtAA > %i' % pt_cut, 'genJet_eta', axis )
    #gS2 = make_efficiency_graph( t, denom_cut, '(stage2jet_pt_calibration3) > %i' % pt_cut, 'genJet_eta', axis )
    
    gP2.SetMinimum( 0. )
    gP2.SetLineColor(ROOT.kRed)
    gP2.SetLineWidth(2)
    gS2.SetLineColor(ROOT.kBlack)
    gS2.SetLineWidth(2)
    
    mg = ROOT.TMultiGraph("mg", "L1 Jet Efficiency")
    mg.Add( gP2 )
    mg.Add( gS2 )
    mg.SetMinimum( 0. )
    mg.Draw("aplez")
    mg.GetXaxis().SetTitle("Gen Jet p_{T}")
    mg.GetYaxis().SetTitle("L1 Algo. Efficiency w.r.t. Gen")
    p.SetGrid()
    
    
    leg = setLegStyle(0.5,0.3,0.9,0.7)
    leg.AddEntry(gS2, "Phase-I Jet Algo.","lpe")
    leg.AddEntry(gP2, "Phase-II Jet Algo.","lpe")
    leg.Draw("same")
    c.Update()
    
    
    c.SaveAs( universalSaveDir + fName + '_Calib_er1p2_%i_eff.png' % pt_cut )

""" MAKE RATES """
if doRate :
    fName = 'merged_minBias-PU200_Calibrated_v5'
    base = '/data/truggles/l1CaloJets_20181101/'
    universalSaveDir = "/afs/cern.ch/user/t/truggles/www/Phase-II/rates/"
    checkDir( universalSaveDir )

    f = ROOT.TFile( base+fName+'.root', 'r' )
    print f
    t = f.Get('analyzer/tree')

    nEvents = f.Get('analyzer/nEvents').Integral()
    eta_threshold = 1.2
    x_info = [56, 20, 300]
    
    hP2 = make_rate_hist( nEvents, t, 'jet_pt_calibration', 1.0, 'jet_eta', eta_threshold, x_info ) 
    hP2.SaveAs( fName+'_Phase-2.root' )
    hS2 = make_rate_hist( nEvents, t, 'stage2jet_pt_calibration3', 1.0, 'stage2jet_eta', eta_threshold, x_info )
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
    
    
    c.SaveAs( universalSaveDir + fName +  '_Calib_er1p2_rate.png' )



