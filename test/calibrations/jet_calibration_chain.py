import ROOT
import os
from array import array
from collections import OrderedDict
import L1Trigger.L1EGRateStudies.trigHelpers as trigHelpers
from caloJetPtCalibrations import getTH1, getTH2, getTH2VarBin, \
    drawPointsHists, drawPointsHists3, make_em_fraction_calibrations, \
    get_x_binning, drawPointsSingleHist


def check_calibration_py_cfg( quantile_map ) :
    pt_binning_array = get_x_binning()
    alt_binning = array('f', [])
    for i in range( len(pt_binning_array) ) :
        if i == len(pt_binning_array) - 1 : continue # don't go over the top
        alt_binning.append( (pt_binning_array[i] + pt_binning_array[i+1] )/2. )
    print pt_binning_array
    print alt_binning
    for k, v in quantile_map.iteritems() :
        print k, v
        for b in alt_binning :
            print ("%.3f " % v[-1].Eval( b ) ),
        print "\n"
    
    


def prepare_calibration_py_cfg( quantile_map ) :
    o_file = open('L1CaloJetCalibrations_cfi.py', 'w')
    o_file.write( "import FWCore.ParameterSet.Config as cms\n\n" )
    # Already add zero for EM frac, will add upper val for each loop
    for k, v in quantile_map.iteritems() :
        print k, v

    # Currently Pt binning is constant for all regions
    o_file.write( "\tjetPtBins = cms.vdouble([ 0.0" )
    pt_binning = []
    pt_binning_array = get_x_binning()
    for val in pt_binning_array :
        if val == 0.0 : continue # skip to keep commans easy
        pt_binning.append( val )
        o_file.write( ",%.1f" % val )
    o_file.write( "]),\n" )
    print pt_binning

    prepare_calo_region_calibrations( 'Barrel', 0.0, 1.5, o_file, quantile_map )
    prepare_calo_region_calibrations( 'HGCal', 1.5, 3.0, o_file, quantile_map )
    prepare_calo_region_calibrations( 'HF', 3.0, 6.0, o_file, quantile_map )

    o_file.close()

def prepare_calo_region_calibrations( calo_region_name, eta_min, eta_max, o_file, quantile_map ) :
    pt_binning_array = get_x_binning()
    # EM fraction
    o_file.write( "\temFractionBins%s = cms.vdouble([ 0.00" % calo_region_name )
    em_frac_list = [0.0,]
    for k, v in quantile_map.iteritems() :

        # Check this entry is in the correct eta range
        if v[2] < eta_min : continue
        if v[3] > eta_max : continue

        # continue if not increasing value
        if v[1] <= em_frac_list[-1] : continue
        em_frac_list.append( v[1] )
        if v[1] == 1.0 : # Need to go a little higher to catch rounding issues
            o_file.write( ",1.05" )
        else :
            o_file.write( ",%.2f" % v[1] )
    o_file.write( "]),\n" )
    print em_frac_list

    # Eta binning
    o_file.write( "\tabsEtaBins%s = cms.vdouble([ %.2f" % (calo_region_name, eta_min) )
    abs_eta_list = [eta_min,]
    for k, v in quantile_map.iteritems() :

        # Check this entry is in the correct eta range
        if v[2] < eta_min : continue
        if v[3] > eta_max : continue

        # continue if not increasing value
        if v[3] <= abs_eta_list[-1] : continue
        abs_eta_list.append( v[3] )
        o_file.write( ",%.2f" % v[3] )
    o_file.write( "]),\n" )
    print abs_eta_list
        
    # Now huge loop of values for each bin
    o_file.write( "\tjetCalibrations%s = cms.vdouble([\n" % calo_region_name )
    x = ROOT.Double(0.)
    y = ROOT.Double(0.)
    cnt = 1
    for k, v in quantile_map.iteritems() :

        # Check this entry is in the correct eta range
        if v[2] < eta_min : continue
        if v[3] > eta_max : continue

        val_string = ''
        # Use this version when grabbing the value from the fit TF1
        for i in range( len(pt_binning_array) ) :
            if i == len(pt_binning_array) - 1 : continue # don't go over the top
            val_string += "%.3f, " % v[-1].Eval( (pt_binning_array[i] + pt_binning_array[i+1] )/2. )
        # Use this version when grabbing the value from the raw TGraph
        #for point in range( v[-1].GetN() ) :
        #    v[-1].GetPoint( point, x, y )
        #    #print x, y
        #    val_string += "%.3f, " % y

        val_string = val_string.strip(' ')
        # No comma at end if final one
        if cnt == len( quantile_map.keys() ) :
            val_string = val_string.strip(',')
        o_file.write( "\t\t%s\n" % val_string )
        #print val_string
        cnt += 1
    o_file.write( "\t]),\n" )

def get_quantile_map( calib_fName ) :

    # Open calibration root file and get thresholds from TGraphs
    print ("Calibrating with file: %s" % calib_fName )
    f = ROOT.TFile( calib_fName, 'r' )

    keys = []
    allKeys = f.GetListOfKeys()

    for k in allKeys :
        # Switched to using TF1 fit to the TGraph
        #if k.GetClassName() == 'TGraph' :
        if k.GetClassName() == 'TF1' :
            keys.append( k.GetName() )
    
    
    # Dict to store TGraph name as key and lower and upper thresholds as value
    quantile_map = OrderedDict()

    for key in keys :
        info = key.split('_')
        f_low = float(info[3].replace('p','.'))
        f_high = float(info[5].replace('p','.'))
        eta_low = float(info[7].replace('p','.'))
        eta_high = float(info[9].replace('p','.'))
        quantile_map[ key ] = [ f_low, f_high, eta_low, eta_high, f.Get( key ) ]
    #for k, v in quantile_map.iteritems() :
    #    print k, v

    return quantile_map

    


def add_calibration( name_in, quantile_map ) :
    jet_pt_binning = get_x_binning()
    useBinnedPt = True
    print "Adding Phase-2 calibration branch to ttree. UseBinnedPt = %s" % useBinnedPt
    f_in = ROOT.TFile( name_in, 'UPDATE')
    t = f_in.Get( 'analyzer/tree' )

    # new calibrations
    calib = array('f', [ 0 ] )
    calibB = t.Branch('calibAA', calib, 'calibAA/F')
    calibPt = array('f', [ 0 ] )
    calibPtB = t.Branch('calibPtAA', calibPt, 'calibPtAA/F')

    cnt = 0
    for row in t :
        cnt += 1
        if cnt % 10000 == 0 : print cnt

        ecal_L1EG_jet_pt = row.ecal_L1EG_jet_pt
        ecal_pt = row.ecal_pt
        hcal_pt = row.hcal_pt
        jet_pt = row.jet_pt
        abs_jet_eta = abs(row.jet_eta)
        if jet_pt < 0 :
            val = -9.
            calib[0] = -9.
            calibPt[0] = -9.
        else :
            val = calibrate( quantile_map, abs_jet_eta, ecal_L1EG_jet_pt, ecal_pt, jet_pt, jet_pt_binning, useBinnedPt )
            calib[0] = val
            calibPt[0] = ecal_L1EG_jet_pt + ecal_pt + (val * hcal_pt)

        calibB.Fill()
        calibPtB.Fill()
    d = f_in.Get('analyzer')
    d.cd()
    t.Write('', ROOT.TObject.kOverwrite)
    f_in.Close()


def add_stage2_calibration( name_in, stage2_calib_file ) :
    print "Adding Stage-2 calibration branch to ttree"
    f_in = ROOT.TFile( name_in, 'UPDATE')
    t = f_in.Get( 'analyzer/tree' )

    f_calib = ROOT.TFile( stage2_calib_file, 'READ')
    g_calib = f_calib.Get( 'Graph' )

    # new calibrations
    stage2CalibPt = array('f', [ 0 ] )
    stage2CalibPtB = t.Branch('stage2jet_pt_calibration3', stage2CalibPt, 'stage2jet_pt_calibration3/F')

    cnt = 0
    for row in t :
        cnt += 1
        if cnt % 10000 == 0 : print cnt

        pt = row.stage2jet_pt
        eval_pt = row.stage2jet_pt
        if eval_pt > 450 : eval_pt = 450
        stage2CalibPt[0] = pt * g_calib.Eval( eval_pt )

        stage2CalibPtB.Fill()
    d = f_in.Get('analyzer')
    d.cd()
    t.Write('', ROOT.TObject.kOverwrite)
    f_in.Close()



# This is to simulate FW LUTs
def find_binned_pt( jet_pt, jet_pt_binning ) :
    prev = 0.
    current = 0.
    index = 0

    # Don't go over the top
    if jet_pt >= jet_pt_binning[-1] :
        return ( jet_pt_binning[ -1 ] + jet_pt_binning[ -2 ] ) / 2.
        
    while True :
        # return bin center
        if jet_pt < jet_pt_binning[ index ] :
            print "jet_pt bin", index
            return ( jet_pt_binning[ index ] + jet_pt_binning[ index - 1 ] ) / 2.
        index += 1
        




def calibrate( quantile_map, abs_jet_eta, ecal_L1EG_jet_pt, ecal_pt, jet_pt, jet_pt_binning, useBins=False ) :
    em_frac = (ecal_L1EG_jet_pt + ecal_pt) / jet_pt
    #print "EM Frac: ",em_frac
    if em_frac == 2 : return 1.0 # These are non-recoed jets
    if em_frac > 1.0 : em_frac = 1.0 # These are some corner case problems which will be fixed and only range up to 1.05
    for k, v in quantile_map.iteritems() :
        if em_frac >= v[0] and em_frac <= v[1] :
            if abs_jet_eta >= v[2] and abs_jet_eta <= v[3] :
                #return v[2].Eval( jet_pt )
                tmp_pt = jet_pt
                if jet_pt > 500 : tmp_pt = 500 # Straight line extension
                if not useBins :
                    rtn = v[-1].Eval( tmp_pt )
                # This is to simulate FW LUTs
                if useBins :
                    binned_pt_val = find_binned_pt( tmp_pt, jet_pt_binning )
                    rtn = v[-1].Eval( binned_pt_val )

                # Ensure not returning a negative value because of
                # unpopulated low pT bins
                while (rtn < 0) :
                    jet_pt += 2
                    rtn = v[-1].Eval( jet_pt )
                    if jet_pt > 500 : break
                #assert(rtn >= 0), "The calibration result is less than zero for range name %s for \
                if (rtn < 0) : print "The calibration result is less than zero for range name %s for \
                        EM fraction %.2f and Jet pT %.2f, resulting calibration %.2f" % (k, em_frac, jet_pt, rtn)

                return rtn
    print "Shouldn't get here, em_frac ",em_frac
    return 1.0

if '__main__' in __name__ :

    base= '/data/truggles/l1CaloJets_20190210v7/'
    #base= '/data/truggles/l1CaloJets_20190206/'
    base= '/data/truggles/l1CaloJets_20190219v3/'
    base= '/data/truggles/l1CaloJets_20190301/'
    #base= '/data/truggles/l1CaloJets_20190304v1/'
    #base= '/data/truggles/l1CaloJets_20190305v2/'
    base= '/data/truggles/l1CaloJets_20190306v1TestJets/'
    base= '/data/truggles/l1CaloJets_20190306v1TestTaus/'
    base= '/data/truggles/l1CaloJets_20190306v2TestTaus/'

    for shape in [
        #'ttbar_PU200', # testing
        #'tau_PU200',
        #'tau_PU0',
        #'minBias_PU200',
        #'vbfhtt_v1',
        #'output_round2_eff_hists_qcd_v1',
        'ggHTauTau_PU0',
        'ggHTauTau_PU200',
    ] :
        
        #jetsF0 = 'merged_QCD-PU%s.root' % shape
        #date = jetsF0.replace('merged_QCD-','').replace('.root','')
        jetsF0 = '%s.root' % shape
        date = jetsF0.replace('merged_','').replace('.root','')
        date = base.split('/')[-2].replace('l1CaloJets__','')+shape
        plotDir = '/afs/cern.ch/user/t/truggles/www/Phase-II/20190306/'+date+''
        if not os.path.exists( plotDir ) : os.makedirs( plotDir )

        jetFile = ROOT.TFile( base+jetsF0, 'r' )
        print jetFile
        tree = jetFile.Get("analyzer/tree")

        c = ROOT.TCanvas('c', '', 800, 700)
        ''' Track to cluster reco resolution '''
        c.SetCanvasSize(1500,600)
        c.Divide(3)


        """ Make new calibration root file """
        # Only make for QCD sample, for other samples, pick up the
        # results of QCD
        cut = "" # Do all Eta now
        #if 'ttbar' in shape :
        #    make_em_fraction_calibrations( c, base+jetsF0, cut, plotDir )
        jetFile.Close()

        """ Add new calibrations to TTree """
        #version = shape.split('_')[-1]
        version = 'v7'
        #quantile_map = get_quantile_map( 'jet_em_calibrations_'+version+'.root' )
        ##prepare_calibration_py_cfg( quantile_map )
        ####check_calibration_py_cfg( quantile_map )
        ##FIXME add_calibration( base+jetsF0, quantile_map )
        #add_calibration( '../../../_jetOutputFileName0GeV3.root', quantile_map )
        """ Add Stage-2 Calibrations which do a good job up to 50 GeV """
        #add_stage2_calibration( base+jetsF0, 'stage-2_calib_stage2_genOverReco_by_reco.root' )

        """ Plot Results """
        jetFile = ROOT.TFile( base+jetsF0, 'r' )
        tree = jetFile.Get("analyzer/tree")

        plot_calibrated_results = True
        #plot_calibrated_results = False
        # Can't plot for minBias b/c no gen
        #if 'minBias' in shape : 
        #    plot_calibrated_results = False
        x_and_y_bins = [28,20,300, 60,0,3]
        if 'Tau' in jetsF0 :
            x_and_y_bins = [20,0,100, 60,0,3]
        #x_and_y_bins = [120,0,400, 300,0,15]
        """ Resulting Calibrations """
        if plot_calibrated_results :
            eta_ranges = {
            'all' : '(abs(genJet_eta)<10)',
            #'golden' : '(abs(genJet_eta)<1.2)',
            'barrel' : '(abs(genJet_eta)<1.4)',
            #'barrel_transition' : '(abs(genJet_eta)<1.8 && abs(genJet_eta)>1.2)',
            'hgcal' : '(abs(genJet_eta)<2.9 && abs(genJet_eta)>1.6)',
            'hf' : '(abs(genJet_eta)>3.1)',
            }
            for k, cut in eta_ranges.iteritems() :
                if 'Tau' in jetsF0 and k == 'hf' : continue

                #to_plot = '(jet_pt)/genJet_pt:genJet_pt'
                #h1 = getTH2( tree, 'qcd1', to_plot, cut, x_and_y_bins )
                ##to_plot = '(ecal_L1EG_jet_pt + ecal_pt + (hcal_pt_calibration) )/genJet_pt:genJet_pt' # For EDProducer check
                #to_plot = '( calibPtAA )/genJet_pt:genJet_pt'
                #h2 = getTH2( tree, 'qcd2', to_plot, cut, x_and_y_bins )
                ##to_plot = '(stage2jet_pt)/genJet_pt:genJet_pt'
                #to_plot = '(stage2jet_pt_calibration3)/genJet_pt:genJet_pt'
                #h3 = getTH2( tree, 's2', to_plot, cut, x_and_y_bins )
                #xaxis = "Gen Jet P_{T} (GeV)"
                #yaxis = "Relative Error in P_{T} reco/gen"
                #title1 = "Phase-II before HCAL calibrations"
                #title2 = "Phase-II with HCAL calibrations"
                #title3 = "Phase-I with calibrations"
                #c.SetTitle("genJetPt_Calibrated_vs_Stage-2_PU200_"+k)
                #areaNorm = True
                #drawPointsHists3(c.GetTitle(), h1, h2, h3, title1, title2, title3, xaxis, yaxis, areaNorm, plotDir)



                #to_plot = '(jet_pt)/genJet_pt:genJet_pt'
                #h1 = getTH2( tree, 'qcd1', to_plot, cut, x_and_y_bins )
                ##to_plot = '(ecal_L1EG_jet_pt + ecal_pt + (hcal_pt_calibration) )/genJet_pt:genJet_pt' # For EDProducer check
                #to_plot = '( calibPtAA )/genJet_pt:genJet_pt'
                #h2 = getTH2( tree, 'qcd2', to_plot, cut, x_and_y_bins )
                ##to_plot = '(stage2jet_pt)/genJet_pt:genJet_pt'
                #xaxis = "Gen Jet P_{T} (GeV)"
                #yaxis = "Relative Error in P_{T} reco/gen"
                #title1 = "Phase-II before HCAL calibrations"
                #title2 = "Phase-II with HCAL calibrations"
                #c.SetTitle("genJetPt_Calibration_"+k)
                #areaNorm = True
                #drawPointsHists(c.GetTitle(), h1, h2, title1, title2, xaxis, yaxis, areaNorm, plotDir)

                #to_plot = '(jet_pt)/genJet_pt:genJet_pt'
                #h1 = getTH2( tree, 'qcd1', to_plot, cut, x_and_y_bins )
                ##to_plot = '(ecal_L1EG_jet_pt + ecal_pt + (hcal_pt_calibration) )/genJet_pt:genJet_pt' # For EDProducer check
                #to_plot = '( calibPtBB )/genJet_pt:genJet_pt'
                #h2 = getTH2( tree, 'qcd2', to_plot, cut, x_and_y_bins )
                ##to_plot = '(stage2jet_pt)/genJet_pt:genJet_pt'
                #xaxis = "Gen Jet P_{T} (GeV)"
                #yaxis = "Relative Error in P_{T} reco/gen"
                #title1 = "Phase-II before HCAL calibrations"
                #title2 = "Phase-II with HCAL fit calibrations"
                #c.SetTitle("genJetPt_Calibration_fit_"+k)
                #areaNorm = True
                #drawPointsHists(c.GetTitle(), h1, h2, title1, title2, xaxis, yaxis, areaNorm, plotDir)

                #to_plot = '(jet_pt)/genJet_pt:genJet_pt'
                #h1 = getTH2( tree, 'qcd1', to_plot, cut, x_and_y_bins )
                ##to_plot = '(ecal_L1EG_jet_pt + ecal_pt + (hcal_pt_calibration) )/genJet_pt:genJet_pt' # For EDProducer check
                #to_plot = '( calibPtCC )/genJet_pt:genJet_pt'
                #h2 = getTH2( tree, 'qcd2', to_plot, cut, x_and_y_bins )
                ##to_plot = '(stage2jet_pt)/genJet_pt:genJet_pt'
                #xaxis = "Gen Jet P_{T} (GeV)"
                #yaxis = "Relative Error in P_{T} reco/gen"
                #title1 = "Phase-II before HCAL calibrations"
                #title2 = "Phase-II with HCAL fitBinned calibrations"
                #c.SetTitle("genJetPt_Calibration_fitBinned_"+k)
                #areaNorm = True
                #drawPointsHists(c.GetTitle(), h1, h2, title1, title2, xaxis, yaxis, areaNorm, plotDir)

                #to_plot = '(jet_pt_calibration)/genJet_pt:genJet_pt'
                #h1 = getTH2( tree, 'qcd1', to_plot, cut, x_and_y_bins )
                #to_plot = '(stage2jet_pt_calib)/genJet_pt:genJet_pt'
                #h2 = getTH2( tree, 'qcd2', to_plot, cut, x_and_y_bins )
                #xaxis = "Gen Jet P_{T} (GeV)"
                #yaxis = "Relative Error in P_{T} reco/gen"
                #title1 = "Phase-II "+k
                #title2 = "Phase-I "+k
                #c.SetTitle("genJetPt_comparisons_"+k)
                #areaNorm = True
                #drawPointsHists(c.GetTitle(), h1, h2, title1, title2, xaxis, yaxis, areaNorm, plotDir)


                to_plot = '(jet_pt)/genJet_pt:genJet_pt'
                h1 = getTH2( tree, 'qcd1', to_plot, cut, x_and_y_bins )
                to_plot = '(jet_pt_calibration)/genJet_pt:genJet_pt'
                h2 = getTH2( tree, 'qcd2', to_plot, cut, x_and_y_bins )
                if 'Tau' in jetsF0 :
                    to_plot = '(stage2tau_pt)/genJet_pt:genJet_pt'
                    h3 = getTH2( tree, 's2', to_plot, cut, x_and_y_bins )
                    title3 = "Phase-I CaloTau"
                else :
                    to_plot = '(stage2jet_pt)/genJet_pt:genJet_pt'
                    h3 = getTH2( tree, 's2', to_plot, cut, x_and_y_bins )
                    title3 = "Phase-I CaloJet"
                xaxis = "Gen Jet P_{T} (GeV)"
                yaxis = "Relative Error in P_{T} reco/gen"
                title1 = "Phase-II CaloTau, raw"
                title2 = "Phase-II CaloTau, EM Frac Calib"
                c.SetTitle("genJetPt_Tau_"+k)
                areaNorm = True
                drawPointsHists3(c.GetTitle(), h1, h2, h3, title1, title2, title3, xaxis, yaxis, areaNorm, plotDir)


            c.SetCanvasSize(600,600)
            c.Divide(1)

            # PU Zero
            # Rate file
            #jetFileX = ROOT.TFile( base+'ttbar_PU0_v1.root', 'r' )
            jetFileX = ROOT.TFile( base+jetsF0.replace('v1','v2'), 'r' )
            print jetFileX
            treeX = jetFileX.Get("analyzer/tree")

            ## Pt resolution
            #x_bins = [100, -1, 1]
            #for k, cut in eta_ranges.iteritems() :
            #    pt_res_hists = []
            #    #for pt in [20, 50, 100, 200] :
            #    for pt in [ 50, 100, 200] :
            #        pt_min = pt-10
            #        pt_max = pt+10
            #        if pt == 20 :
            #            pt_min = pt
            #            pt_max = pt+10
            #        if pt == 200 :
            #            pt_min = pt-20
            #            pt_max = pt+20
        
            #        cutX = '( calibPtAA > %i && calibPtAA < %i )' % (pt_min, pt_max )
            #        cutX += '*'+cut.replace('genJet_eta', 'jet_eta')
            #        to_plot = '( calibPtAA - genJet_pt )/genJet_pt'
            #        pt_res_hists.append( getTH1( treeX, 'ttbar PU 200, pt  [%i,%i]' % (pt_min,pt_max), to_plot, cutX, x_bins ) )
            #        pt_res_hists[-1].GetXaxis().SetTitle('p_{T} Resolution (reco-gen)/gen')
            #    c.SetName( 'jet_pt_calib_resolution_'+k )
            #    trigHelpers.drawDRHists( pt_res_hists, c, -1, plotDir, True ) # True is doFit

            ## Normalizations
            #norm_200_gen = jetFile.Get('analyzer/nEvents').Integral()
            #norm_200_all = jetFileX.Get('analyzer/nEvents').Integral()
            #x_bins = [110, -5.5, 5.5]
            #c.SetLogy(1) 
            #for pt in [20, 30, 40, 50] :
            #    cut = '( calibPtAA > %i )' % pt
            #    to_plot = '( jet_eta )'
            #    hx = getTH1( tree, 'minBias PU 200 no PU sub., pt > %i' % pt, to_plot, cut, x_bins )
            #    hx.Scale( 1. / norm_200_gen )
            #    cut = '( calibPtAA > %i )' % pt
            #    hy = getTH1( treeX, 'minBias PU 200 PU sub., pt > %i' % pt, to_plot, cut, x_bins )
            #    hy.Scale( 1. / norm_200_all )
            #    c.SetName( 'jet_eta_calib_pt_gtr'+str(pt) )
            #    hx.GetXaxis().SetTitle('Reco Jet #eta')
            #    trigHelpers.drawDRHists( [hx, hy], c, 50, plotDir, False, True ) # noFit, skip rescaling

            #to_plot = '( calibPtAA )'
            #x_bins = [40, 0, 200]
            #for k, cut in eta_ranges.iteritems() :
            #    cutX = cut.replace('genJet_eta', 'jet_eta')
            #    hx = getTH1( tree, 'minBias PU 200 no PU sub. '+k, to_plot, cutX, x_bins )
            #    hx.Scale( 1. / norm_200_gen )
            #    hy = getTH1( treeX, 'minBias PU 200 PU sub. '+k, '( calibPtAA )', cutX, x_bins )
            #    hy.Scale( 1. / norm_200_all )
            #    c.SaveAs( plotDir+'/jet_pt_calib_'+k+'.png' )
            #    c.SetName( 'jet_pt_calib_'+k )
            #    hx.GetXaxis().SetTitle('Reco Jet p_{T} (GeV)')
            #    trigHelpers.drawDRHists( [hx, hy], c, 50, plotDir, False, True ) # noFit, skip rescaling

            #jetFileX.Close()
            #jetFileX = ROOT.TFile( base+'minBias_PU200_v2.root', 'r' )
            #print jetFileX
            #treeX = jetFileX.Get("analyzer/tree")
            ## To check potential PU Jet ID vars
            #to_check = ['ecal_nL1EGs', '(hcal_3x3*calibAA + ecal_dR0p15)', '(max(max(max(hcal_2x2_1, hcal_2x2_2), hcal_2x2_3), hcal_2x2_4)*calibAA + ecal_dR0p1)', 'hcal_nHits', 'ecal_nHits', 'seed_pt', '(hcal_nHits+ecal_nHits+ecal_nL1EGs)']
            #to_check = ['(ecal_L1EG_jet_pt + ecal_pt)', '(hcal_pt*calibAA)']
            #c.SetCanvasSize(900,600)
            #c.Divide(2)
            #x_and_y_bins = [20,20,60, 30,0,0.75]
            #x_and_y_bins = [20,20,100, 30,0,1.1]
            #cut = '(abs(jet_eta)<1.4 && jet_pt > 20.)'
            #for var in to_check :
            #    x_and_y_bins_here = list(x_and_y_bins)
            #    set_title = var
            #    if '(hcal_nHits+ecal_nHits+ecal_nL1EGs)' == var : set_title = 'hcal_plus_ecal_plus_L1EG_nHits'
            #    elif 'hcal_3x3' in var : set_title = 'towers3x3'
            #    elif 'hcal_2x2' in var : set_title = 'towers2x2'

            #    if 'seed_pt' == var : x_and_y_bins_here[-1] = 0.75
            #    if 'hcal_2x2' in var : x_and_y_bins_here[-1] = 1
            #    if 'hcal_3x3' in var : x_and_y_bins_here[-1] = 2
            #    to_plot = var+'/calibPtAA:calibPtAA'
            #    h1 = getTH2( treeX, 'ttbar all', to_plot, cut, x_and_y_bins_here )
            #    h2 = getTH2( tree, 'ttbar gen', to_plot, cut, x_and_y_bins_here )
            #    xaxis = "Jet P_{T} (GeV)"
            #    yaxis = var+"/reco p_{T}"
            #    title1 = "MinBias Jets"
            #    title2 = "ttbar Gen Jets"
            #    c.SetTitle("pu_ID_checks_"+set_title)
            #    areaNorm = True
            #    drawPointsHists(c.GetTitle(), h1, h2, title1, title2, xaxis, yaxis, areaNorm, plotDir)

        #x_and_y_bins = [120,0,500, 300,0,15]
        #to_plot = '(stage2jet_pt)/genJet_pt:genJet_pt'
        #xaxis = "Gen Jet P_{T} (GeV)"
        #yaxis = "Relative Error in P_{T} reco/gen"
        #title1 = "Phase-I Out-of-box"
        #c.SetTitle("stage2_recoOverGen_by_gen")

        #x_and_y_bins = [120,0,500, 300,0,5]
        #to_plot = 'genJet_pt/stage2jet_pt:stage2jet_pt'
        #xaxis = "Stage-2 Jet P_{T} (GeV)"
        #yaxis = "Relative Error in P_{T}  gen/reco"
        #title1 = "Phase-I Out-of-box"
        #c.SetTitle("stage2_genOverReco_by_reco")

        #x_and_y_bins = [120,0,500, 300,0,15]
        #to_plot = '(stage2jet_pt_calibration3)/genJet_pt:genJet_pt'
        #xaxis = "Gen Jet P_{T} (GeV)"
        #yaxis = "Relative Error in P_{T} reco calib/gen"
        #title1 = "Phase-I Calibration 1"
        #c.SetTitle("stage2_recoCalib1OverGen_by_gen")

        #x_and_y_bins = [120,0,500, 300,0,5]
        #to_plot = 'genJet_pt/stage2jet_pt_calibration3:stage2jet_pt_calibration3'
        #xaxis = "Stage-2 Calib1 Jet P_{T} (GeV)"
        #yaxis = "Relative Error in P_{T}  gen/reco calib1"
        #title1 = "Phase-I Calibration 1"
        #c.SetTitle("stage2_genOverRecoCalib1_by_recoCalib1")

        #h1 = getTH2( tree, 's2', to_plot, cut, x_and_y_bins )
        #drawPointsSingleHist(c.GetTitle(), h1, title1, xaxis, yaxis, plotDir)




