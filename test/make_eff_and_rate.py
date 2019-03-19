import ROOT
from collections import OrderedDict
from L1Trigger.L1EGRateStudies.trigHelpers import make_efficiency_graph, make_rate_hist, setLegStyle, checkDir
import os

if not os.path.exists( 'eff_and_rate_roots/' ) : os.makedirs( 'eff_and_rate_roots/' )

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

doTau = True
#doTau = False

doEff = True
#doEff = False

doPtEff = True
#doPtEff = False

doRate = True
doRate = False

c = ROOT.TCanvas('c', 'c', 900, 900)
p = ROOT.TPad('p','p', 0, 0, 1, 1)
p.Draw()
p.cd()


if doEff :
    fName = 'output_round2_QCDMar14v1'
    fName = 'output_round2_TTbarMar14v1'
    fName = 'output_round2_HiggsTauTauvL1EGsv2'
    date = '20190308'
    base = '/data/truggles/l1CaloJets_'+date+'_r2/'
    universalSaveDir = "/afs/cern.ch/user/t/truggles/www/Phase-II/efficiencies/"+date+"/"+fName+"/"
    checkDir( universalSaveDir )
    checkDir( universalSaveDir )

    f = ROOT.TFile( base+fName+'.root', 'r' )
    t = f.Get('analyzer/tree')
    

    # Threshold cuts for passing region
    pt_cut = 100
    #pt_cut = 40
    #pt_cut = 20
    pt_cut = 32
    #pt_cut = 80
    #pt_cut = 150
    #pt_cut = 200
    #pt_cut = 400
    #pt_cut = 100
    #pt_cut = 0

    p2Obj = 'jet_pt_calibration'
    s2Obj = 'stage2jet_pt'
    #s2Obj = 'stage2jet_pt_calibration3'
    if doTau :
        p2Obj = 'calibPtGG'
        #s2Obj = 'stage2tau_pt'
        s2Obj = 'stage2tau_pt_calibration3'
    
    """ Pt Eff """
    if doPtEff :
        # Use eta cuts to restrict when doing pT efficiencies
        denom_cut = 'abs(genJet_eta)<1.4'
        axis = [160, 0, 400]
        if doTau :
            axis = [150, 0, 150]
            #axis = [40, 0, 200]

        gP2 = make_efficiency_graph( t, denom_cut, p2Obj+' > %i' % pt_cut, 'genJet_pt', axis )
        gP22 = make_efficiency_graph( t, denom_cut, p2Obj+' > %i && isoTauHH > 0.5' % pt_cut, 'genJet_pt', axis )
        gS2 = make_efficiency_graph( t, denom_cut, s2Obj+' > %i' % pt_cut, 'genJet_pt', axis )
        gS22 = make_efficiency_graph( t, denom_cut, s2Obj+' > %i && stage2tau_isoBit > 0.5' % pt_cut, 'genJet_pt', axis )

    """ Eta Eff """
    if not doPtEff :
        # Use pt cuts to restrict included objects when doing eta efficiencies
        denom_pt = 40
        denom_cut = '(genJet_pt > %i)' % denom_pt
        axis = [100, -5, 5]
        gP2 = make_efficiency_graph( t, denom_cut, p2Obj+' > %i' % pt_cut, 'genJet_eta', axis )
        gP22 = make_efficiency_graph( t, denom_cut, p2Obj+' > %i && isoTauHH > 0.5' % pt_cut, 'genJet_eta', axis )
        gS2 = make_efficiency_graph( t, denom_cut, s2Obj+' > %i' % pt_cut, 'genJet_eta', axis )
        gS22 = make_efficiency_graph( t, denom_cut, s2Obj+' > %i && stage2tau_isoBit > 0.5' % pt_cut, 'genJet_eta', axis )
    
    gP2.SetMinimum( 0. )
    gP2.SetLineColor(ROOT.kRed)
    gP2.SetLineWidth(2)
    gP22.SetLineColor(ROOT.kGreen+3)
    gP22.SetLineWidth(2)
    gS2.SetLineColor(ROOT.kBlack)
    gS2.SetLineWidth(2)
    gS22.SetLineColor(ROOT.kBlue)
    gS22.SetLineWidth(2)
    
    text = 'Jet' if not doTau else 'Tau'

    mg = ROOT.TMultiGraph("mg", "L1 %s Efficiency" % text)
    mg.Add( gP2 )
    mg.Add( gP22 )
    mg.Add( gS2 )
    mg.Add( gS22 )
    mg.SetMinimum( 0. )
    mg.Draw("aplez")
    mg.GetXaxis().SetTitle("Gen %s p_{T}" % text)
    mg.GetYaxis().SetTitle("L1 Algo. Efficiency w.r.t. Gen")
    mg.SetMaximum(1.3)
    p.SetGrid()
    
    txt = ROOT.TLatex()
    txt.SetTextSize(0.035)
    txt.DrawLatexNDC(.12, .85,  "Baseline:")
    txt.DrawLatexNDC(.12, .81,  "   %s" % denom_cut)
    txt.DrawLatexNDC(.12, .76, "Passing: (Reco p_{T} > %i)" % pt_cut)
    
    #leg = setLegStyle(0.5,0.3,0.9,0.7)
    leg = setLegStyle(0.5,0.72,0.9,0.88)
    leg.AddEntry(gS2, "Phase-I %s" % text,"lpe")
    leg.AddEntry(gS22, "Phase-I Iso %s" % text,"lpe")
    leg.AddEntry(gP2, "Phase-II %s" % text,"lpe")
    leg.AddEntry(gP22, "Phase-II Iso %s" % text,"lpe")
    leg.Draw("same")
    c.Update()
    
    
    app = 'ptEff' if doPtEff else 'etaEff_ptDenom%i' % denom_pt
    c.SaveAs( universalSaveDir + fName + '_Calib_ptThreshold%i_%s.png' % (pt_cut, app) )

""" MAKE RATES """
if doRate :
    fName = 'minBias_PU200_withCuts_v7'
    date = '20190210v7'
    base = '/data/truggles/l1CaloJets_%s/' % date
    universalSaveDir = "/afs/cern.ch/user/t/truggles/www/Phase-II/rates/"+date+"/"+fName+"/"
    # Stage-2
    fName = 'minBias_PU200_v8'
    date = '20190210v8'
    base = '/data/truggles/l1CaloJets_%s/' % date
    #fName = 'merged_minBias-PU200_Calibrated_withCuts_v5'
    #base = '/data/truggles/l1CaloJets_20181101/'
    universalSaveDir = "/afs/cern.ch/user/t/truggles/www/Phase-II/rates/"
    checkDir( universalSaveDir )

    f = ROOT.TFile( base+fName+'.root', 'r' )
    print f
    t = f.Get('analyzer/tree')

    # We used cuts to make a slimmed ttree for looping, so need to get nEvents from the
    # original file

    #fEvents = ROOT.TFile( base+fName.replace('_withCuts','')+'.root', 'r' )
    #print fEvents
    #nEvents = fEvents.Get('analyzer/nEvents').Integral()
    nEvents = f.Get('analyzer/nEvents').Integral()

    # Min and Max eta thresholds for barrel, HGCal, HF rates
    eta_thresholds = OrderedDict()
    eta_thresholds['all']    = [0., 6.0]
    eta_thresholds['barrel'] = [0., 1.5]
    eta_thresholds['hgcal']  = [1.5, 3.0]
    eta_thresholds['hf']     = [3.0, 6.0]

    # nBins, min, max
    x_info = [54, 30, 300]
    
    #for name, thresholds in eta_thresholds.iteritems() :
    #    #hP2 = make_rate_hist( nEvents, t, 'jet_pt_calibration', 1.0, 'jet_eta', thresholds[0], thresholds[1], x_info ) 
    #    #hP2.SaveAs( 'eff_and_rate_roots/'+fName+'_'+name+'_Phase-2.root' )
    #    #del hP2
    #    hS2 = make_rate_hist( nEvents, t, 'stage2jet_pt_calibration3', 1.0, 'stage2jet_eta', thresholds[0], thresholds[1], x_info )
    #    hS2.SaveAs( 'eff_and_rate_roots/'+fName+'_'+name+'_Stage-2.root' )
    #    del hS2

    #assert(0)

    
    rates = []
    colors = [ROOT.kBlack, ROOT.kRed, ROOT.kBlue, ROOT.kGreen, ROOT.kOrange, ROOT.kGray+2]
    cnt = 0
    p2name = 'minBias_PU200_withCuts_v7'
    s2name = 'minBias_PU200_v8'
    for name, thresholds in eta_thresholds.iteritems() :
        f1 = ROOT.TFile( 'eff_and_rate_roots/'+p2name+'_'+name+'_Phase-2.root', 'r')
        print f1
        rates.append( f1.Get('cumul') )
        rates[-1].SetDirectory( 0 )
        rates[-1].SetTitle( 'Phase2 - %s' % name )
        rates[-1].SetName( 'Phase2 - %s' %name )
        rates[-1].SetLineColor( colors[cnt] )
        rates[-1].SetMarkerColor( colors[cnt] )
        rates[-1].SetLineWidth( 2 )
        if name == 'all' :
            rates[-1].SetLineWidth( 4 )
        rates[-1].GetXaxis().SetRangeUser(x_info[1], x_info[2])
        cnt += 1
    cnt = 0
    for name, thresholds in eta_thresholds.iteritems() :
        f1 = ROOT.TFile( 'eff_and_rate_roots/'+s2name+'_'+name+'_Stage-2.root', 'r')
        print f1
        rates.append( f1.Get('cumul') )
        rates[-1].SetDirectory( 0 )
        rates[-1].SetTitle( 'Stage2 - %s' % name )
        rates[-1].SetName( 'Stage2 - %s' % name )
        rates[-1].SetLineColor( colors[cnt]+2 )
        rates[-1].SetMarkerColor( colors[cnt]+2 )
        rates[-1].SetLineWidth( 2 )
        rates[-1].GetXaxis().SetRangeUser(x_info[1], x_info[2])
        cnt += 1
    
    print rates[0]
    rates[0].SetTitle("L1 Algo. Rates")
    rates[0].GetXaxis().SetTitle("Reco Jet p_{T}")
    rates[0].GetYaxis().SetTitle("L1 Algo. Rate (kHz)")
    rates[0].Draw()
    cnt = 0
    for rate in rates :
        cnt += 1
        if cnt == 1 : continue
        if rate.GetTitle() == 'Stage2 - hgcal' : continue
        if rate.GetTitle() == 'Stage2 - all' : continue
        rate.Draw('SAME')
    
    
    p.SetGrid()
    p.SetLogy()
    p.SetLeftMargin( .13 )
    p.SetBottomMargin( .1 )
    
    
    leg = setLegStyle(0.5,0.55,0.9,0.85)
    for rate in rates :
        if rate.GetTitle() == 'Stage2 - hgcal' : continue
        if rate.GetTitle() == 'Stage2 - all' : continue
        title = rate.GetTitle() if not rate.GetTitle() == "L1 Algo. Rates" else "Phase2 - All"
        leg.AddEntry(rate, title,"lpe")
    leg.Draw("same")
    c.Update()
    
    
    c.SaveAs( universalSaveDir + fName +  '_Calib_rate.png' )



