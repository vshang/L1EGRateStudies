
import ROOT
import os
from array import array
from collections import OrderedDict
import L1Trigger.L1EGRateStudies.trigHelpers as trigHelpers
from caloJetPtCalibrationsGCT import getTH1, getTH2, getTH2VarBin, \
    drawPointsHists, drawPointsHists2, make_jet_calibrations, \
    get_x_binning, drawPointsSingleHist, make_tau_calibrations
import ctypes


def check_calibration_py_cfg( quantile_map ) :
    pt_binning_array = get_x_binning()
    alt_binning = array('f', [])
    for i in range( len(pt_binning_array) ) :
        if i == len(pt_binning_array) - 1 : continue # don't go over the top
        alt_binning.append( (pt_binning_array[i] + pt_binning_array[i+1] )/2. )
    print(pt_binning_arra)
    print(alt_binning)
    for k, v in quantile_map.items() :
        print(k, v)
        for b in alt_binning :
            print("%.3f " % v[-1].Eval( b ) ),
        print("\n")
    
    


def prepare_calibration_py_cfg( quantile_map, doTaus=False ) :
    if doTaus:
        fileName = 'L1CaloTauCalibrations_cfi.py'
    else:
        fileName = 'L1CaloJetCalibrations_cfi.py'
    o_file = open(fileName, 'w')
    o_file.write( "import FWCore.ParameterSet.Config as cms\n\n" )
    for k, v in quantile_map.items() :
        print(k, v)


    # Currently Pt binning is constant for all regions
    name_string = 'tau' if doTaus else 'jet'
    o_file.write( "\t%sPtBins = cms.vdouble([ 0.0" % name_string )
    pt_binning = []
    pt_binning_array = get_x_binning(name_string)
    for val in pt_binning_array :
        if val == 0.0 : continue # skip to keep commans easy
        pt_binning.append( val )
        o_file.write( ",%.1f" % val )
    o_file.write( "]),\n" )
    print(pt_binning)

    if not doTaus :
        prepare_calo_region_calibrations( 'Barrel', 0.0, 1.5, o_file, quantile_map )
        prepare_calo_region_calibrations( 'HGCal', 1.5, 3.0, o_file, quantile_map )
        prepare_calo_region_calibrations( 'HF', 3.0, 6.0, o_file, quantile_map )
    if doTaus :
        prepare_tau_calo_region_calibrations( 'Barrel', 0.0, 1.5, o_file, quantile_map )
        prepare_tau_calo_region_calibrations( 'HGCal', 1.5, 3.0, o_file, quantile_map )

    o_file.close()

def prepare_tau_calo_region_calibrations( calo_region_name, eta_min, eta_max, o_file, quantile_map ) :
    pt_binning_array = get_x_binning('tau')
    # Eta binning
    o_file.write( "\ttauAbsEtaBins%s = cms.vdouble([ %.2f" % (calo_region_name, eta_min) )
    abs_eta_list = [eta_min,]
    for k, v in quantile_map.items() :

        # Check this entry is in the correct eta range
        if v[0] < eta_min : continue
        if v[1] > eta_max : continue

        # continue if not increasing value
        if v[1] <= abs_eta_list[-1] : continue
        abs_eta_list.append( v[1] )
        o_file.write( ",%.2f" % v[1] )
    o_file.write( "]),\n" )
    print(abs_eta_list)

    # # L1EG binning
    # # EM fraction is unique for each L1EG scenario
    # o_file.write( "\ttauL1egInfo%s = cms.VPSet(\n" % calo_region_name )
    # l1eg_map = {
    #     '0L1EG' : 0,
    #     '1L1EG' : 1,
    #     'Gtr1L1EG' : 2,
    #     'All' : 0,
    # }
    # em_frac_map = OrderedDict()
    # for k, v in quantile_map.items() :

    #     # Check this entry is in the correct eta range
    #     if v[3] < eta_min : continue
    #     if v[4] > eta_max : continue

    #     # Check that this L1EG scenario has been added to map
    #     if v[0] not in em_frac_map.keys() :
    #         em_frac_map[ v[0] ] = [0.0,]

    #     # continue if not increasing value
    #     if v[2] <= em_frac_map[v[0]][-1] : continue
    #     if v[2] == 1.0 : # Need to go a little higher to catch rounding issues
    #         em_frac_map[v[0]].append( 1.05 )
    #     else :
    #         em_frac_map[v[0]].append( v[2] )
    # for k, v in em_frac_map.items() :
    #     print(k, v)
    #     float_to_str = [str(i) for i in v]
    #     to_print = ", ".join(float_to_str)
    #     o_file.write( "\t\tcms.PSet(\n" )
    #     o_file.write( "\t\t\tl1egCount = cms.double( %.1f ),\n" % l1eg_map[k] )
    #     o_file.write( "\t\t\tl1egEmFractions = cms.vdouble([ %s]),\n" % to_print )
    #     o_file.write( "\t\t),\n" )
    # o_file.write( "\t),\n" )

    # Now huge loop of values for each bin
    o_file.write( "\ttauCalibrations%s = cms.vdouble([\n" % calo_region_name )
    x = ctypes.c_double(0.)
    y = ctypes.c_double(0.)
    cnt = 1
    for k, v in quantile_map.items() :

        # Check this entry is in the correct eta range
        if v[0] < eta_min : continue
        if v[1] > eta_max : continue

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

def prepare_calo_region_calibrations( calo_region_name, eta_min, eta_max, o_file, quantile_map ) :
    pt_binning_array = get_x_binning()
    # # EM fraction
    # o_file.write( "\temFractionBins%s = cms.vdouble([ 0.00" % calo_region_name )
    # em_frac_list = [0.0,]
    # for k, v in quantile_map.items() :

    #     # Check this entry is in the correct eta range
    #     if v[2] < eta_min : continue
    #     if v[3] > eta_max : continue

    #     # continue if not increasing value
    #     if v[1] <= em_frac_list[-1] : continue
    #     em_frac_list.append( v[1] )
    #     if v[1] == 1.0 : # Need to go a little higher to catch rounding issues
    #         o_file.write( ",1.05" )
    #     else :
    #         o_file.write( ",%.2f" % v[1] )
    # o_file.write( "]),\n" )
    # print(em_frac_list)

    # Eta binning
    o_file.write( "\tabsEtaBins%s = cms.vdouble([ %.2f" % (calo_region_name, eta_min) )
    abs_eta_list = [eta_min,]
    for k, v in quantile_map.items() :

        # Check this entry is in the correct eta range
        if v[0] < eta_min : continue
        if v[1] > eta_max : continue

        # continue if not increasing value
        if v[1] <= abs_eta_list[-1] : continue
        abs_eta_list.append( v[1] )
        o_file.write( ",%.2f" % v[1] )
    o_file.write( "]),\n" )
    print(abs_eta_list)
        
    # Now huge loop of values for each bin
    o_file.write( "\tjetCalibrations%s = cms.vdouble([\n" % calo_region_name )
    x = ctypes.c_double(0.)
    y = ctypes.c_double(0.)
    cnt = 1
    for k, v in quantile_map.items() :

        # Check this entry is in the correct eta range
        if v[0] < eta_min : continue
        if v[1] > eta_max : continue

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
    print("Calibrating with file: %s" % calib_fName )
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

    if ('jet_em_calibrations' in calib_fName) :
        for key in keys :
            info = key.split('_')
            eta_low = float(info[2].replace('p','.'))
            eta_high = float(info[4].replace('p','.'))
            #quantile_map[ key ] = [ f_low, f_high, eta_low, eta_high, f.Get( key ) ]
            # FIXME - what happened to ROOT in 10_5_X?
            new_f1 = ROOT.TF1( key, '([0] + [1]*x + [2]*TMath::Exp(-[3]*x))')
            new_f1.SetParameter( 0, f.Get( key ).GetParameter( 0 ) )
            new_f1.SetParameter( 1, f.Get( key ).GetParameter( 1 ) )
            new_f1.SetParameter( 2, f.Get( key ).GetParameter( 2 ) )
            new_f1.SetParameter( 3, f.Get( key ).GetParameter( 3 ) )
            quantile_map[ key ] = [ eta_low, eta_high, new_f1 ]

    elif ('tau_pt_calibrations' in calib_fName) :
        for key in keys :
            info = key.split('_')
            eta_low = float(info[2].replace('p','.'))
            eta_high = float(info[4].replace('p','.'))
            #quantile_map[ key ] = [ f_low, f_high, eta_low, eta_high, f.Get( key ) ]
            # FIXME - what happened to ROOT in 10_5_X?
            new_f1 = ROOT.TF1( key, '([0] + [1]*TMath::Exp(-[2]*x))')
            new_f1.SetParameter( 0, f.Get( key ).GetParameter( 0 ) )
            new_f1.SetParameter( 1, f.Get( key ).GetParameter( 1 ) )
            new_f1.SetParameter( 2, f.Get( key ).GetParameter( 2 ) )
            quantile_map[ key ] = [ eta_low, eta_high, new_f1 ]

    else :
        print("File name %s does not match format of 'jet_em_calibrations_X' or 'tau_pt_calibrations_X'" % calib_fName)
        return
    #for k, v in quantile_map.items() :
    #    print k, v

    print("\n\n\nFIXME - what happened to ROOT in 10_5_X\nWhy are these errors here?\nThe code appears to work with my fix\n")

    return quantile_map

    

def add_jet_calibration( name_in, quantile_map ) :
    jet_pt_binning = get_x_binning(name_in)
    useBinnedPt = True
    print("Adding Phase-2 calibration branch to ttree. UseBinnedPt = %s" % useBinnedPt)
    f_in = ROOT.TFile( name_in, 'UPDATE')
    t = f_in.Get( 'analyzer/tree' )

    # new calibrations
    calib = array('f', [ 0 ] )
    calibB = t.Branch('calibHH', calib, 'calibHH/F')
    calibPt = array('f', [ 0 ] )
    calibPtB = t.Branch('calibPtHH', calibPt, 'calibPtHH/F')

    cnt = 0
    for row in t :
        cnt += 1
        if cnt % 10000 == 0 : print(cnt)

        jet_pt = row.jetEt
        abs_jet_eta = abs(row.jetEta)
        if jet_pt < 0 :
            val = -9.
            calib[0] = -9.
            calibPt[0] = -9.
        else :
            val = calibrate( quantile_map, abs_jet_eta, jet_pt, jet_pt_binning, useBinnedPt )
            calib[0] = val
            calibPt[0] = jet_pt * val

        calibB.Fill()
        calibPtB.Fill()
    d = f_in.Get('analyzer')
    d.cd()
    t.Write('', ROOT.TObject.kOverwrite)
    f_in.Close()


    

def add_tau_calibration( name_in, quantile_map ) :
    tau_pt_binning = get_x_binning('Tau')
    useBinnedPt = True
    print("Adding Phase-2 calibration branch to ttree. UseBinnedPt = %s" % useBinnedPt)
    f_in = ROOT.TFile( name_in, 'UPDATE')
    t = f_in.Get( 'analyzer/tree' )

    # new calibrations
    calib = array('f', [ 0 ] )
    calibB = t.Branch('calibHH', calib, 'calibHH/F')
    calibPt = array('f', [ 0 ] )
    calibPtB = t.Branch('calibPtHH', calibPt, 'calibPtHH/F')

    cnt = 0
    for row in t :
        cnt += 1
        if cnt % 10000 == 0 : print(cnt)

        tau_pt = row.tauEt
        abs_tau_eta = abs(row.jetEta)
        if tau_pt < 0 or abs_tau_eta > 3.0 :
            val = -9.
            calib[0] = -9.
            calibPt[0] = -9.
        else :
            val = calibrate_tau( quantile_map, abs_tau_eta, tau_pt, tau_pt_binning, useBinnedPt )
            calib[0] = val
            calibPt[0] = tau_pt * val

        calibB.Fill()
        calibPtB.Fill()
    d = f_in.Get('analyzer')
    d.cd()
    t.Write('', ROOT.TObject.kOverwrite)
    f_in.Close()


def add_stage2_calibration( name_in, stage2_calib_file, doTaus=False ) :
    print("Adding Stage-2 calibration branch to ttree, doTaus = %s, with file %s" % (doTaus, stage2_calib_file))
    f_in = ROOT.TFile( name_in, 'UPDATE')
    t = f_in.Get( 'analyzer/tree' )

    f_calib = ROOT.TFile( stage2_calib_file, 'READ')
    g_calib = f_calib.Get( 'Graph' )

    # new calibrations
    stage2_name = 'stage2jet_pt_calibration3'
    if doTaus :
        stage2_name = stage2_name.replace('jet', 'tau')
        
    stage2CalibPt = array('f', [ 0 ] )
    stage2CalibPtB = t.Branch(stage2_name, stage2CalibPt, stage2_name+'/F')

    cnt = 0
    for row in t :
        cnt += 1
        if cnt % 10000 == 0 : print(cnt)

        if not doTaus : # doJets
            pt = row.stage2jet_pt
            eval_pt = row.stage2jet_pt
            if eval_pt > 450 : eval_pt = 450
        else : # doTaus
            pt = row.stage2tau_pt
            eval_pt = row.stage2tau_pt
            if eval_pt > 200 : eval_pt = 200
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
            #print "jet_pt bin", index
            return ( jet_pt_binning[ index ] + jet_pt_binning[ index - 1 ] ) / 2.
        index += 1
        




def calibrate( quantile_map, abs_jet_eta, jet_pt, jet_pt_binning, useBins=False ) :

    for k, v in quantile_map.items() :
        if True:
            if abs_jet_eta >= v[0] and abs_jet_eta <= v[1] :
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
                if (rtn < 0) : print("The calibration result is less than zero for range name %s for \
                       Jet pT %.2f, resulting calibration %.2f" % (k, jet_pt, rtn))

                return rtn
    print("Shouldn't get here, em_frac ",em_frac)
    return 1.0



def calibrate_tau( quantile_map, abs_jet_eta, jet_pt, jet_pt_binning, useBins=False ) :

    for k, v in quantile_map.items() :

        if True: 
            if abs_jet_eta >= v[0] and abs_jet_eta <= v[1] :
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
                if (rtn < 0) : print("The calibration result is less than zero for range name %s for \
                        Jet pT %.2f, resulting calibration %.2f" % (k, jet_pt, rtn))

                return rtn
    print("Shouldn't get here, em_frac ",em_frac)
    return 1.0

if '__main__' in __name__ :

    # Commands
    # doJets = False
    # doTaus = True
    doJets = True
    doTaus = False

    make_calibrations = False
    apply_phase2_calibrations = False
    apply_stage2_calibrations = False
    prepare_calibration_cfg = False
    plot_calibrated_results = False

    # Uncomment to run!
    #make_calibrations = True
    apply_phase2_calibrations = True
    #apply_stage2_calibrations = True
    #prepare_calibration_cfg = True
    #plot_calibrated_results = True

    if doTaus:
        base = '/afs/hep.wisc.edu/home/vshang/public/Phase2L1CaloTaus/CMSSW_14_0_0_pre3/src/L1Trigger/L1EGRateStudies/test/crab/l1CaloTaus_r2_CMSSW_14_0_0_pre3/20240404/'
    else:
        base = '/afs/hep.wisc.edu/home/vshang/public/Phase2L1CaloTaus/CMSSW_14_0_0_pre3/src/L1Trigger/L1EGRateStudies/test/crab/l1CaloJets_r2_CMSSW_14_0_0_pre3/20240404/'

    shapes = [
        # R2
        #'output_round2_QCD_13_1X_nocalib3GeVmaxTT12jets',
        #'output_round2_VBFHiggsTauTau_13_1X_nocalib3GeVmaxTT12jets',
        #'output_round2_TTbar'
        #'output_round2_HiggsTauTau_Pallabi',
        'output_round2_minBias_13_1X_nocalib3GeVmaxTT12jets',
    ]

    for shape in shapes :
        
        #jetsF0 = 'merged_QCD-PU%s.root' % shape
        #date = jetsF0.replace('merged_QCD-','').replace('.root','')
        jetsF0 = '%s.root' % shape
        date = jetsF0.replace('merged_','').replace('.root','')
        date = base.split('/')[-2].replace('l1CaloJets_','')+shape
        plotDir = '/afs/hep.wisc.edu/home/vshang/public/Phase2L1CaloTaus/CMSSW_14_0_0_pre3/src/L1Trigger/L1EGRateStudies/test/crab'+date+'Vxy1'
        if not os.path.exists( plotDir ) : os.makedirs( plotDir )

        c = ROOT.TCanvas('c', '', 800, 700)
        ''' Track to cluster reco resolution '''
        c.SetCanvasSize(1500,600)
        c.Divide(3)


        """ Make new calibration root file """
        # Only make for QCD sample, for other samples, pick up the
        # results of QCD
        cut = "" # Do all Eta now
        if make_calibrations :
            jetFile = ROOT.TFile( base+jetsF0, 'r' )
            print(jetFile)
            tree = jetFile.Get("analyzer/tree")

            if ('qcd' in shape or 'QCD' in shape or True) and doJets :
                make_jet_calibrations( c, base+jetsF0, cut, plotDir )
            if 'Tau' in shape and doTaus :
                make_tau_calibrations( c, base+jetsF0, cut, plotDir )
            jetFile.Close()

        """ Add new calibrations to TTree """
        if apply_phase2_calibrations :
            version = shape.split('_')[-1]
            if doJets :
                version = 'nocalib3GeVmaxTT12jets'
                quantile_map = get_quantile_map( 'jet_em_calibrations_'+version+'.root' )
                add_jet_calibration( base+jetsF0, quantile_map )
            if doTaus :
                version = 'nocalib3GeVmaxTT12jets'
                quantile_map = get_quantile_map( 'tau_pt_calibrations_'+version+'.root ')
                add_tau_calibration( base+jetsF0, quantile_map )
        """ Prepare cfg calibration code snippet """
        if prepare_calibration_cfg :
            version = shape.split('_')[-1]
            ###version = 'v7'
            if doJets :
                version = 'nocalib3GeVmaxTT12jets'
                quantile_map = get_quantile_map( 'jet_em_calibrations_'+version+'.root' )
            if doTaus :
                version = 'nocalib3GeVmaxTT12jets'
                quantile_map = get_quantile_map( 'tau_pt_calibrations_'+version+'.root ')
            ####check_calibration_py_cfg( quantile_map )
            prepare_calibration_py_cfg( quantile_map, doTaus )
        """ Add Stage-2 Calibrations which do a good job up to 50 GeV """
        if apply_stage2_calibrations :
            if doJets :
                add_stage2_calibration( base+jetsF0, 'stage-2_jet_calib_stage2_genOverReco_by_reco.root' )
            if doTaus :
                add_stage2_calibration( base+jetsF0, 'stage-2_tau_calib_stage2_genOverReco_by_reco.root', doTaus )

        """ Plot Results """
        jetFile = ROOT.TFile( base+jetsF0, 'r' )
        tree = jetFile.Get("analyzer/tree")

        # Can't plot for minBias b/c no gen
        if 'minBias' in shape : 
            plot_calibrated_results = False
        x_and_y_bins = [28,20,300, 60,0,3]
        if 'Tau' in jetsF0 :
            x_and_y_bins = [20,0,100, 60,0,3]

        """ Resulting Calibrations:
            The eta ranges are cut slightly short of the transition regions
            to focus on the bulk of the region of interest. """
        if plot_calibrated_results :
            eta_ranges = {
            'all' : '(abs(genJet_eta)<10)',
            'barrel' : '(abs(genJet_eta)<1.4)',
            #'barrel_transition' : '(abs(genJet_eta)<1.8 && abs(genJet_eta)>1.2)',
            'hgcal' : '(abs(genJet_eta)<2.9 && abs(genJet_eta)>1.6)',
            'hf' : '(abs(genJet_eta)>3.1)',
            }
            for k, cut in eta_ranges.items() :
                if 'Tau' in jetsF0 and k == 'hf' : continue


                tau_pt = "tauEt"
                if 'Tau' in jetsF0 :
                    to_plot = tau_pt+'/genJet_pt:genJet_pt'
                    h1 = getTH2( tree, 'qcd1', to_plot, cut, x_and_y_bins )
                    to_plot = '( calibPtHH )/genJet_pt:genJet_pt'
                    h2 = getTH2( tree, 'qcd2', to_plot, cut, x_and_y_bins )
                    title1 = "Phase-2 GCTTau, raw "+k
                    title2 = "Phase-2 GCTTau, Calib "+k
                else :
                    to_plot = '(jetEt)/genJet_pt:genJet_pt'
                    h1 = getTH2( tree, 'qcd1', to_plot, cut, x_and_y_bins )
                    to_plot = '( calibPtHH )/genJet_pt:genJet_pt'
                    h2 = getTH2( tree, 'qcd2', to_plot, cut, x_and_y_bins )
                    title1 = "Phase-2 GCTJet, raw "+k
                    title2 = "Phase-2 GCTJet, Calib "+k
                xaxis = "Gen Jet P_{T} (GeV)"
                yaxis = "Relative Error in P_{T} reco/gen"
                if 'Tau' in jetsF0:
                    c.SetTitle("genTauEt_"+k)
                else:
                    c.SetTitle("genJetEt_"+k)
                areaNorm = True
                #areaNorm = False
                drawPointsHists2(c.GetTitle(), h1, h2, title1, title2, xaxis, yaxis, areaNorm, plotDir)
