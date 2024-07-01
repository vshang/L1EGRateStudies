import ROOT
from collections import OrderedDict
from L1Trigger.L1EGRateStudies.trigHelpers import make_efficiency_graph, make_rate_hist, make_rate_hist2, setLegStyle, checkDir
import os
from L1Trigger.L1EGRateStudies.trigHelpers import drawCMSString

if not os.path.exists( 'eff_and_rate_roots_jets/' ) : os.makedirs( 'eff_and_rate_roots_jets/' )
if not os.path.exists( 'eff_and_rate_roots_taus/' ) : os.makedirs( 'eff_and_rate_roots_taus/' )
#if not os.path.exists( 'eff_and_rate_roots2/' ) : os.makedirs( 'eff_and_rate_roots2/' )

ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)

#Define CMS Colors (see https://cms-analysis.docs.cern.ch/guidelines/plotting/colors/)
ColorA = ROOT.TColor.GetColor("#5790fc")
ColorB = ROOT.TColor.GetColor("#f89c20")
ColorC = ROOT.TColor.GetColor("#e42536")
ColorD = ROOT.TColor.GetColor("#964a8b")
ColorE = ROOT.TColor.GetColor("#9c9ca1")
ColorF = ROOT.TColor.GetColor("#7a21dd")

#doTau = True
doTau = False

#doEff = True
doEff = False

doPtEff = True
#doPtEff = False

doRate = True
#doRate = False

#doRateFirstHalf = True
doRateFirstHalf = False
doRateSecondHalf = True
#doRateSecondHalf = False

c = ROOT.TCanvas('c', 'c', 900, 900)
p = ROOT.TPad('p','p', 0, 0, 1, 1)
p.Draw()
p.cd()

p2Obj = 'jetEt'
#p2Obj = 'calibPtHH'
s2Obj = 'stage2jet_pt_calib'
s2ObjEta = 'stage2jet_eta'
if doTau :
    p2Obj = 'tauEt'
    #p2Obj = 'calibPtHH'
    s2Obj = 'stage2tau_pt'
    #s2Obj = 'stage2tau_pt_calibration3'
    s2ObjEta = 'stage2tau_eta'

text = 'Jet' if not doTau else 'Tau'
dirName = 'jets' if not doTau else 'taus'
    

if doEff :
    if doTau:
        fName = 'output_round2_VBFHiggsTauTau_13_1X_calib3GeVmaxTT12jets'
    else:
        fName = 'output_round2_QCD_13_1X_calib3GeVmaxTT12jets'
    #fName = 'output_round2_HiggsTauTauCross'
    #fName = 'output_round2_HiggsTauTau_Pallabi'
    date = '20240404'
    if doTau:
        base = '/afs/hep.wisc.edu/home/vshang/public/Phase2L1CaloTaus/CMSSW_14_0_0_pre3/src/L1Trigger/L1EGRateStudies/test/crab/l1CaloTaus_r2_CMSSW_14_0_0_pre3/20240404/'
    else:
        base = '/afs/hep.wisc.edu/home/vshang/public/Phase2L1CaloTaus/CMSSW_14_0_0_pre3/src/L1Trigger/L1EGRateStudies/test/crab/l1CaloJets_r2_CMSSW_14_0_0_pre3/20240404/'
    universalSaveDir = "/afs/hep.wisc.edu/home/vshang/public/Phase2L1CaloTaus/CMSSW_14_0_0_pre3/src/L1Trigger/L1EGRateStudies/test/efficiencies/CMSSW_14_0_0_pre3/"+dirName+"/"+date+"/"+fName+"/"
    checkDir( universalSaveDir )

    f = ROOT.TFile( base+fName+'.root', 'r' )
    t = f.Get('analyzer/tree')
    

    # Threshold cuts for passing region
    if doTau:
        pt_cut = 32
        #pt_cut = 50
    else:
        if doPtEff:
            #pt_cut = 100
            pt_cut = 50
            #pt_cut = 30 #For comparison to Emyr's plots
        else:
            pt_cut = 80
            #pt_cut = 0

    """ Pt Eff """
    if doPtEff :
        # Use eta cuts to restrict when doing pT efficiencies
        # denom_cut = 'abs(genJet_eta)<1.5'# && abs(jetEta)<5.0'
        # denom_cut2 = 'abs(genJet_eta)>1.5 && abs(genJet_eta)<3.0'# && abs(jetEta)<5.0'
        #denom_cut2 = 'abs(genJet_eta)>2.8 && abs(genJet_eta)<5.0'
        denom_cut = 'abs(genJet_eta)<1.5'# && abs(jetEta)<5.0'
        denom_cut2 = 'abs(genJet_eta)>1.5 && abs(genJet_eta)<2.5'# && abs(jetEta)<5.0'
        #denom_cut3 = 'abs(genJet_eta)>3.5 && abs(genJet_eta)<5.0'# && abs(jetEta)<5.0'
        denom_cut_label = '|#eta^{GEN Jet}| < 1.5'
        denom_cut_label2 = '1.5 < |#eta^{GEN Jet}| < 2.5'
        #denom_cut_label3 = '3.5 < |#eta^{GEN Jet}| < 5.0'
        #axis = [160, 0, 400]
        #axis = [70, 0, 700] #L1 Trigger Menu Validation settings for Barrel and HF
        #axis = [45, 0, 900] #L1 Trigger Menu Validation settings for Endcap
        #axis = [25, 0, 150] #Custom for comparing to Emry's plots
        axis = [25, 0, 700] #TDR Style
        if doTau :
            #axis = [150, 0, 150]
            axis = [25, 0, 150] #TDR Style
            denom_cut_label = '|#eta^{GEN #tau}| < 1.5'
            denom_cut_label2 = '1.5 < |#eta^{GEN #tau}| < 2.5'
            #denom_cut_label = '2.8 < |#eta^{Gen tau}| < 5.0'

        gP2 = make_efficiency_graph( t, denom_cut, p2Obj+' > %i' % pt_cut, 'genJet_pt', axis )
        gP22 = make_efficiency_graph( t, denom_cut2, p2Obj+' > %i' % pt_cut, 'genJet_pt', axis )
        #gS2 = make_efficiency_graph( t, denom_cut3, p2Obj+' > %i' % pt_cut, 'genJet_pt', axis )
        #gP22 = make_efficiency_graph( t, denom_cut, p2Obj+' > %i && loose_iso_tau_wp > 0.5' % pt_cut, 'genJet_pt', axis )
        #gS2 = make_efficiency_graph( t, denom_cut, s2Obj+' > %i' % pt_cut, 'genJet_pt', axis )
        #gS22 = make_efficiency_graph( t, denom_cut, s2Obj+' > %i && stage2tau_isoBit > 0.5' % pt_cut, 'genJet_pt', axis )

    """ Eta Eff """
    if not doPtEff :
        # Use pt cuts to restrict included objects when doing eta efficiencies
        if doTau:
            denom_pt = 40
        else:
            denom_pt = 100
            #denom_pt = 40
        denom_cut = '(genJet_pt > %i)' % denom_pt
        #denom_cut = '(genJet_pt > %i && genJet_pt < 100)' % denom_pt
        denom_cut_label = 'p_{T}^{GEN Jet} > %i GeV' % denom_pt
        #denom_cut_label = '%i < p_{T}^{GenJet} < 100 GeV' % denom_pt
        if doTau:
            denom_cut_label = 'p_{T}^{GEN #tau} > %i GeV' % denom_pt
        #axis = [100, -5, 5]
        axis = [40, -2.5, 2.5] #TDR Style
        if doTau:
            #axis = [100, -3, 3]
            axis = [40, -2.5, 2.5] #TDR Style
        gP2 = make_efficiency_graph( t, denom_cut, p2Obj+' > %i' % pt_cut, 'genJet_eta', axis )
        #gP22 = make_efficiency_graph( t, denom_cut, p2Obj+' > %i && loose_iso_tau_wp > 0.5' % pt_cut, 'genJet_eta', axis )
        #gS2 = make_efficiency_graph( t, denom_cut, s2Obj+' > %i' % pt_cut, 'genJet_eta', axis )
        #gS22 = make_efficiency_graph( t, denom_cut, s2Obj+' > %i && stage2tau_isoBit > 0.5' % pt_cut, 'genJet_eta', axis )
    
    gP2.SetMinimum( 0. )
    gP2.SetLineColor(ColorA)
    gP2.SetLineWidth(2)
    gP2.SetMarkerSize(2)
    gP2.SetMarkerStyle(20)
    gP2.SetMarkerColor(ColorA)
    if doPtEff:
        gP22.SetLineColor(ColorB)
        gP22.SetLineWidth(2)
        gP22.SetMarkerSize(2)
        gP22.SetMarkerStyle(21)
        gP22.SetMarkerColor(ColorB)
        # if not doTau:
        #     gS2.SetLineColor(ColorC)
        #     gS2.SetLineWidth(2)
        #     gS2.SetMarkerSize(2)
        #     gS2.SetMarkerStyle(22)
        #     gS2.SetMarkerColor(ColorC)
        

    #mg = ROOT.TMultiGraph("mg", "L1 %s Efficiency" % text)
    mg = ROOT.TMultiGraph("mg", "")
    mg.Add( gP2 )
    if doPtEff:
        mg.Add( gP22 )
        # if not doTau:
        #     mg.Add( gS2 )
    mg.GetXaxis().SetTitleOffset(1.3)
    mg.SetMinimum( 0. )
    if doPtEff:
        mg.Draw("apez")
    else:
        mg.Draw("aplez")
    if doPtEff :
        if doTau :
            mg.GetXaxis().SetTitle("GEN #tau p_{T} (GeV)")
        else :
            mg.GetXaxis().SetTitle("GEN %s p_{T} (GeV)" % text)
    else :
        if doTau :
            mg.GetXaxis().SetTitle("GEN #tau #eta")
        else :
            mg.GetXaxis().SetTitle("GEN %s #eta" % text)
    mg.GetYaxis().SetTitle("L1 Efficiency")
    mg.SetMaximum(1.3)
    mg.GetXaxis().SetLimits(axis[1], axis[2])
    p.SetGrid()

    #cmsString = drawCMSString("#bf{CMS Simulation}  <PU>=200  ggH+qqH, H#rightarrow#tau#tau")
    title = ROOT.TLatex()
    title.SetTextSize(0.045)
    title.DrawLatexNDC(.1, .91, "CMS")
    title.SetTextSize(0.030)
    title.DrawLatexNDC(.2, .91, "Phase-2 Simulation Preliminary")
    title.SetTextSize(0.035)
    title.DrawLatexNDC(.68, .91, "14 TeV, 200 PU")
    
    txt = ROOT.TLatex()
    txt.SetTextSize(0.03)
    if doPtEff:
        if doTau:                                         
            txt.DrawLatexNDC(.15, .83, "p_{T}^{GCTTau} > %i GeV" % pt_cut)
        else:
            txt.DrawLatexNDC(.15, .83, "p_{T}^{GCTJet} > %i GeV" % pt_cut) 
    else:
        txt.DrawLatexNDC(.15, .83,  "%s" % denom_cut_label) 
        if doTau:
            txt.DrawLatexNDC(.15, .76, "p_{T}^{GCTTau} > %i GeV" % pt_cut)
        else:
            txt.DrawLatexNDC(.15, .76, "p_{T}^{GCTJet} > %i GeV" % pt_cut) #End of comment out
    #txt.DrawLatexNDC(.12, .69, "|#eta^{CaloJet}| < 5.0")
    
    #leg = setLegStyle(0.5,0.3,0.9,0.7)
    leg = setLegStyle(0.45,0.74,0.88,0.88)
    leg.SetFillStyle(0)
    if doPtEff:
        leg.AddEntry(gP2, "GCT%s, " % text + denom_cut_label,"lpe")
        leg.AddEntry(gP22, "GCT%s, " % text + denom_cut_label2,"lpe")
        # if not doTau:
        #     leg.AddEntry(gS2, "GCT%s, " % text + denom_cut_label3,"lpe")
    else:
        leg.AddEntry(gP2, "GCT%s" % text,"lpe") 
    #if doTau:
        #leg.AddEntry(gP22, "CaloIso%s" % text,"lpe")
    leg.Draw("same")
    c.Update()


    #Fit histograms
    if doPtEff:
        f1Barrel = ROOT.TF1('fitBarrel', '[0]+([1]/2)*TMath::Erf(sqrt(2)*(x-[2])/[3])', -100, 1000)
        f1Endcap = ROOT.TF1('fitEndcap', '[0]+([1]/2)*TMath::Erf(sqrt(2)*(x-[2])/[3])', -100, 1000)
        # f1Barrel.SetParameters(0.0, 1.0, 50, 10)
        # f1Endcap.SetParameters(0.0, 1.0, 50, 10)
        # gP2.Fit('fitBarrel')
        # gP22.Fit('fitEndcap')
        if doTau:
            f1Barrel.SetParameters(0.477162, 1.00565, 29.443, 27.4076)
            f1Endcap.SetParameters(0.346072, 1.212, 23.1072, 43.6978)
        else:
            f1Barrel.SetParameters(-84.135, 170.265, -318.996, 266.28)
            f1Endcap.SetParameters(-14.145, 30.2767, -136.23, 174.036)
        f1Barrel.SetLineColor(ColorA)
        f1Endcap.SetLineColor(ColorB)
        f1Barrel.SetLineWidth(3)
        f1Endcap.SetLineWidth(3)
        f1Barrel.Draw('same')
        f1Endcap.Draw('same')

    
    app = 'ptEff' if doPtEff else 'etaEff_ptDenom%i' % denom_pt
    #c.SaveAs( universalSaveDir + fName + '_Calib_ptThreshold%i_%s_include_S2Iso.png' % (pt_cut, app) )
    c.SaveAs( universalSaveDir + fName + '_'+p2Obj+'_ptThreshold%i_%s.pdf' % (pt_cut, app) )
    #c.SaveAs( universalSaveDir + fName + '_Calib_ptThreshold%i_%s_IsoTaus_NoS2.png' % (pt_cut, app) )
    #c.SaveAs( universalSaveDir + fName + '_Calib_ptThreshold%i_%s_HGCal.png' % (pt_cut, app) )
    #c.SaveAs( fName + '_'+p2Obj+'_ptThreshold%i_%s_noMatching.png' % (pt_cut, app) )
    #c.SaveAs(fName + '_'+p2Obj+'_ptThreshold%i_%s.png' % (pt_cut, app) )

""" MAKE RATES """
if doRate :

    fName = 'output_round2_minBias_13_1X_calib3GeVmaxTT12jets'
    #fName = 'output_round2_minBias1x3'
    date = '20240404'
    if doTau:
        base = '/afs/hep.wisc.edu/home/vshang/public/Phase2L1CaloTaus/CMSSW_14_0_0_pre3/src/L1Trigger/L1EGRateStudies/test/crab/l1CaloTaus_r2_CMSSW_14_0_0_pre3/20240404/'
    else:
        base = '/afs/hep.wisc.edu/home/vshang/public/Phase2L1CaloTaus/CMSSW_14_0_0_pre3/src/L1Trigger/L1EGRateStudies/test/crab/l1CaloJets_r2_CMSSW_14_0_0_pre3/20240404/'
    universalSaveDir = "/afs/hep.wisc.edu/home/vshang/public/Phase2L1CaloTaus/CMSSW_14_0_0_pre3/src/L1Trigger/L1EGRateStudies/test/rates/CMSSW_14_0_0_pre3/"+dirName+"/"+date+"/"+fName+"/"
    checkDir( universalSaveDir )



    f = ROOT.TFile( base+fName+'.root', 'r' )
    print(f)
    t = f.Get('analyzer/tree')

    # We used cuts to make a slimmed ttree for looping, so need to get nEvents from the
    # original file

    fEvents = ROOT.TFile( base+fName.replace('_withCuts','')+'.root', 'r' )
    print(fEvents)
    nEvents = fEvents.Get('analyzer/nEvents').Integral()
    #nEvents = f.Get('analyzer/nEvents').Integral()

    # Min and Max eta thresholds for barrel, HGCal, HF rates
    eta_thresholds = OrderedDict()
    if doTau :
        eta_thresholds['all']    = [0., 2.5, ColorD, 23]
        #eta_thresholds['runII']  = [0., 2.1, ROOT.kBlue]
        #eta_thresholds['runII']  = [0., 2.172, ROOT.kBlue]
    else :
        eta_thresholds['all']    = [0., 2.5, ColorD, 23]
        #eta_thresholds['all']    = [0., 6.0, ROOT.kBlack]
    #eta_thresholds['all']    = [0., 6.0, ROOT.kBlack]
    eta_thresholds['barrel'] = [0., 1.5, ColorA, 20]
    #eta_thresholds['barrel'] = [0., 1.4, ROOT.kRed]
    eta_thresholds['hgcal']  = [1.5, 2.5, ColorB, 21]
    # if not doTau :
    #     eta_thresholds['hf']     = [3.0, 5.0, ColorC, 22]

    #Victor's edit: redefined eta_thresholds to plot track matched and unmatched rates on same plot
    # eta_thresholds['trackMatched_barrel'] = [0., 1.5, ROOT.kRed]
    # eta_thresholds['notTrackMatched_barrel'] = [0., 1.5, ROOT.kRed]
    # eta_thresholds['trackMatched_runII']  = [0., 2.1, ROOT.kBlue]
    # eta_thresholds['notTrackMatched_runII']  = [0., 2.1, ROOT.kBlue]
    # eta_thresholds['trackMatched_all']    = [0., 2.8, ROOT.kBlack]
    # eta_thresholds['notTrackMatched_all']    = [0., 2.8, ROOT.kBlack]


    # nBins, min, max
    #x_info = [100, 0, 200]
    x_info = [40, 0, 200] #TDR Style
    
    """ This portion takes a long time, only do it if doRateFirstHalf is True """
    if doRateFirstHalf :
        for name, thresholds in eta_thresholds.items() :
            hP2 = make_rate_hist( nEvents, t, p2Obj, 1.0, 'jetEta', thresholds[0], thresholds[1], x_info ) 
            #hP2 = make_rate_hist2( nEvents, t, p2Obj, 1.0, 'jetEta', thresholds[0], thresholds[1], x_info ) #Uncomment to make double tau rate plot
            hP2.SaveAs( 'eff_and_rate_roots_'+dirName+'/'+fName+'_'+name+'_Phase-2.root' )
            #hP2.SaveAs( 'eff_and_rate_roots2/'+fName+'_'+name+'_Phase-2.root' )
            del hP2
            # if doTau:
            #     hP22 = make_rate_hist( nEvents, t, p2Obj, 1.0, 'jetEta', thresholds[0], thresholds[1], x_info, 'loose_iso_tau_wp' ) 
            #     #hP22 = make_rate_hist2( nEvents, t, p2Obj, 1.0, 'jetEta', thresholds[0], thresholds[1], x_info, 'loose_iso_tau_wp' ) #Uncomment to make double tau rate plot
            #     hP22.SaveAs( 'eff_and_rate_roots_'+dirName+'/'+fName+'_'+name+'_Phase-2_iso.root' )
            #     #hP22.SaveAs( 'eff_and_rate_roots2/'+fName+'_'+name+'_Phase-2_iso.root' )
            #     del hP22
            #     #hS2 = make_rate_hist( nEvents, t, s2Obj, 1.0, s2ObjEta, thresholds[0], thresholds[1], x_info )
            #     #hS2 = make_rate_hist2( nEvents, t, s2Obj, 1.0, s2ObjEta, thresholds[0], thresholds[1], x_info ) #Uncomment to make double tau rate plot
            #     #hS2.SaveAs( 'eff_and_rate_roots_'+dirName+'/'+fName+'_'+name+'_Stage-2.root' )
            #     #hS2.SaveAs( 'eff_and_rate_roots2/'+fName+'_'+name+'_Stage-2.root' )
            #     #del hS2
            #     #hS22 = make_rate_hist( nEvents, t, s2Obj, 1.0, s2ObjEta, thresholds[0], thresholds[1], x_info, 'stage2tau_isoBit' )
            #     #hS22.SaveAs( 'eff_and_rate_roots_'+dirName+'/'+fName+'_'+name+'_Stage-2_iso.root' )
            #     #del hS22

    if not doRateSecondHalf :
        print("Skip second half of rate code")
        assert(0)
    
    saveName = 'output_round2_minBias_13_1X_calib3GeVmaxTT12jets'
    #saveName = 'output_round2_minBias1x3'
    #x_info_rebin = [100, 0, 160]
    x_info_rebin = [40, 0, 160] #TDR Style

    plot_map = OrderedDict()
    if doTau:
        # plot_map['barrel'] = OrderedDict()
        # plot_map['barrel']['Phase-2'] = ['Tau', 0]
        # plot_map['barrel']['Stage-2'] = ['Tau', 2]
        # plot_map['nominal'] = OrderedDict()
        # plot_map['nominal']['Phase-2'] = ['Tau', 0]
        # plot_map['nominal']['Stage-2'] = ['Tau', 2]
        plot_map['phase2_All'] = OrderedDict()
        plot_map['phase2_All']['Phase-2'] = ['Tau', 0]
        # plot_map['phase2_All']['Phase-2_iso'] = ['IsoTau', 2]
        # plot_map['phase2_endcap'] = OrderedDict()
        # plot_map['phase2_endcap']['Phase-2'] = ['Tau', 0]
        # plot_map['phase2_endcap']['Phase-2_iso'] = ['IsoTau', 2]
    else:
        plot_map['phase2_All'] = OrderedDict()
        plot_map['phase2_All']['Phase-2'] = ['Jet', 0]

    #Victor's edit: changed plot_map to plot track matched + unmatched rates on same plot for barrel, runII, and all seperately
    # plot_map['barrel'] = OrderedDict()
    # plot_map['barrel']['Phase-2_matched'] = ['Tau', 0]
    # plot_map['barrel']['Phase-2'] = ['Tau', 2]
    # plot_map['runII'] = OrderedDict()
    # plot_map['runII']['Phase-2_matched'] = ['Tau', 0]
    # plot_map['runII']['Phase-2'] = ['Tau', 2]
    # plot_map['all'] = OrderedDict()
    # plot_map['all']['Phase-2_matched'] = ['Tau', 0]
    # plot_map['all']['Phase-2'] = ['Tau', 2]

    for plot, samples in plot_map.items() :
        rates = []
        for sample, info in samples.items() :
            cnt = 0
            for name, thresholds in eta_thresholds.items() :

                print(sample, info, name)
                if plot == 'barrel' and name != 'barrel' : continue
                # if plot == 'barrel' and sample == 'Phase-2_matched' and name != 'trackMatched_barrel' : continue
                # if plot == 'barrel' and sample == 'Phase-2' and name != 'notTrackMatched_barrel' : continue
                # if plot == 'runII' and sample == 'Phase-2_matched' and name!= 'trackMatched_runII' : continue
                # if plot == 'runII' and sample == 'Phase-2' and name!= 'notTrackMatched_runII' : continue
                # if plot == 'all' and sample == 'Phase-2_matched' and name!= 'trackMatched_all' : continue
                # if plot == 'all' and sample == 'Phase-2' and name!= 'notTrackMatched_all' : continue


                f1 = ROOT.TFile( 'eff_and_rate_roots_'+dirName+'/'+saveName+'_'+name+'_'+sample.replace('_matched','')+'.root', 'r')
                #f1 = ROOT.TFile( 'eff_and_rate_roots2/'+saveName+'_'+name+'_'+sample.replace('_matched','')+'.root', 'r') ##Uncomment to make double tau rate plot
                print(f1)
                rates.append( f1.Get('cumul') )
                rates[-1].SetDirectory( 0 )
                rates[-1].SetTitle( '%s %s, %s' % (sample.replace('_iso',''), info[0], name) )
                rates[-1].SetName( '%s %s, %s' % (sample.replace('_iso',''), info[0], name) )
                # rates[-1].SetTitle( '%s %s, %s' % (sample.replace('_matched',' Track matched'), info[0], name) )
                # rates[-1].SetName( '%s %s, %s' % (sample.replace('_matched',' Track matched'), info[0], name) )
                rates[-1].SetLineColor( thresholds[2]+info[1] )
                rates[-1].SetMarkerColor( thresholds[2]+info[1] )
                rates[-1].SetMarkerStyle( thresholds[3] )
                rates[-1].SetMarkerSize( 2 )
                rates[-1].SetLineWidth( 2 )
                if name == 'all' :
                    rates[-1].SetLineWidth( 4 )
                rates[-1].GetXaxis().SetRangeUser(x_info_rebin[1], x_info_rebin[2])
                cnt += 1
        
        print(rates[0])
        rates[0].GetXaxis().SetTitle("GCT%s p_{T} threshold (GeV)" % text )
        rates[0].GetYaxis().SetTitle("L1 Rate (kHz)")
        rates[0].SetMaximum( 40000 ) 
        rates[0].SetMinimum( 5 ) 
        rates[0].GetXaxis().SetTitleOffset(1.3)
        rates[0].Draw('hist e')

        #cmsString = drawCMSString("#bf{CMS Simulation}  <PU>=200  Minimum Bias")
        title = ROOT.TLatex()
        title.SetTextSize(0.045)
        title.DrawLatexNDC(.13, .91, "CMS")
        title.SetTextSize(0.030)
        title.DrawLatexNDC(.23, .91, "Phase-2 Simulation Preliminary")
        title.SetTextSize(0.035)
        title.DrawLatexNDC(.68, .91, "14 TeV, 200 PU")

        cnt = 0
        for rate in rates :
            cnt += 1
            if cnt == 1 : continue
            if 'Stage-2' in rate.GetTitle() and 'hgcal' in rate.GetTitle() : continue
            if 'Stage-2' in rate.GetTitle() and 'all' in rate.GetTitle() : continue
            if 'Stage-2' in rate.GetTitle() and 'runII' in rate.GetTitle() : continue
            rate.Draw('hist e SAME')
        
        
        p.SetGrid()
        p.SetLogy()
        p.SetLeftMargin( .13 )
        p.SetBottomMargin( .1 )
        
        
        leg = setLegStyle(0.53,0.61,0.86,0.88)
        leg.SetFillStyle(0)
        for rate in rates :
            if 'Stage-2' in rate.GetTitle() and 'hgcal' in rate.GetTitle() : continue
            if 'Stage-2' in rate.GetTitle() and 'all' in rate.GetTitle() : continue
            if 'Stage-2' in rate.GetTitle() and 'runII' in rate.GetTitle() : continue
            title = rate.GetTitle() if not rate.GetTitle() == "L1 Rates" else "Phase2, All"
            title = title.replace('barrel', '0 < |#eta| < 1.5')
            #title = title.replace('barrel', '0 < |#eta| < 1.4')
            title = title.replace('Stage-2', 'Phase-I')
            #title = title.replace('Phase-2 ', 'Calo')
            title = title.replace('Phase-2 ', 'GCT')
            #title = title.replace('runII', '0 < |#eta| < 2.1')
            title = title.replace('runII', '0 < |#eta| < 2.172')
            title = title.replace('all', '0 < |#eta| < 2.5')
            title = title.replace('hgcal', '1.5 < |#eta| < 2.5')
            title = title.replace('hf', '3.0 < |#eta| < 5.0')

            title = title.replace('notTrackMatched_', '')
            title = title.replace('trackMatched_', '')
            leg.AddEntry(rate, title,"lpe")
        leg.Draw("same")
        rates[0].SetTitle("")
        c.Update()
        
        
        #c.SaveAs( universalSaveDir + fName +  '_CalibPtHH_rate_'+plot+'.png' )
        #c.SaveAs( universalSaveDir + fName +  '_tauEt_rate_'+plot+'.png' )
        c.SaveAs( universalSaveDir + fName +  '_jetEt_rate_'+plot+'.png' )
        #c.SaveAs( universalSaveDir + saveName +  '_Calib_double_rate_'+plot+'.pdf' ) ##Uncomment when making double tau rate plot
        #c.SaveAs( fName + '_CalibPtHH_rate_'+plot+'.png' )
