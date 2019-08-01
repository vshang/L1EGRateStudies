import ROOT
import os
from array import array
from collections import OrderedDict
import L1Trigger.L1EGRateStudies.trigHelpers as trigHelpers
from caloJetPtCalibrations import getTH1, getTH2, getTH2VarBin, \
    drawPointsHists, drawPointsHists3, make_em_fraction_calibrations, \
    get_x_binning, drawPointsSingleHist, make_tau_calibrations


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
    
    


def prepare_calibration_py_cfg( quantile_map, doTaus=False ) :
    o_file = open('L1CaloJetCalibrations_cfi.py', 'w')
    o_file.write( "import FWCore.ParameterSet.Config as cms\n\n" )
    for k, v in quantile_map.iteritems() :
        print k, v


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
    print pt_binning

    if not doTaus :
        prepare_calo_region_calibrations( 'Barrel', 0.0, 1.5, o_file, quantile_map )
        prepare_calo_region_calibrations( 'HGCal', 1.5, 3.0, o_file, quantile_map )
        prepare_calo_region_calibrations( 'HF', 3.0, 6.0, o_file, quantile_map )
    if doTaus :
        prepare_tau_calo_region_calibrations( 'Barrel', 0.0, 1.5, o_file, quantile_map )
        prepare_tau_calo_region_calibrations( 'HGCal', 1.5, 3.0, o_file, quantile_map )

    o_file.close()

def prepare_tau_calo_region_calibrations( calo_region_name, eta_min, eta_max, o_file, quantile_map ) :
    pt_binning_array = get_x_binning('Tau')
    # Eta binning
    o_file.write( "\ttauAbsEtaBins%s = cms.vdouble([ %.2f" % (calo_region_name, eta_min) )
    abs_eta_list = [eta_min,]
    for k, v in quantile_map.iteritems() :

        # Check this entry is in the correct eta range
        if v[3] < eta_min : continue
        if v[4] > eta_max : continue

        # continue if not increasing value
        if v[4] <= abs_eta_list[-1] : continue
        abs_eta_list.append( v[4] )
        o_file.write( ",%.2f" % v[4] )
    o_file.write( "]),\n" )
    print abs_eta_list

    # L1EG binning
    # EM fraction is unique for each L1EG scenario
    o_file.write( "\ttauL1egInfo%s = cms.VPSet(\n" % calo_region_name )
    l1eg_map = {
        '0L1EG' : 0,
        '1L1EG' : 1,
        'Gtr1L1EG' : 2,
        'All' : 0,
    }
    em_frac_map = OrderedDict()
    for k, v in quantile_map.iteritems() :

        # Check this entry is in the correct eta range
        if v[3] < eta_min : continue
        if v[4] > eta_max : continue

        # Check that this L1EG scenario has been added to map
        if v[0] not in em_frac_map.keys() :
            em_frac_map[ v[0] ] = [0.0,]

        # continue if not increasing value
        if v[2] <= em_frac_map[v[0]][-1] : continue
        if v[2] == 1.0 : # Need to go a little higher to catch rounding issues
            em_frac_map[v[0]].append( 1.05 )
        else :
            em_frac_map[v[0]].append( v[2] )
    for k, v in em_frac_map.iteritems() :
        print k, v
        float_to_str = [str(i) for i in v]
        to_print = ", ".join(float_to_str)
        o_file.write( "\t\tcms.PSet(\n" )
        o_file.write( "\t\t\tl1egCount = cms.double( %.1f ),\n" % l1eg_map[k] )
        o_file.write( "\t\t\tl1egEmFractions = cms.vdouble([ %s]),\n" % to_print )
        o_file.write( "\t\t),\n" )
    o_file.write( "\t),\n" )

    # Now huge loop of values for each bin
    o_file.write( "\ttauCalibrations%s = cms.vdouble([\n" % calo_region_name )
    x = ROOT.Double(0.)
    y = ROOT.Double(0.)
    cnt = 1
    for k, v in quantile_map.iteritems() :

        # Check this entry is in the correct eta range
        if v[3] < eta_min : continue
        if v[4] > eta_max : continue

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

    if 'jet_em_calibrations' in calib_fName :
        for key in keys :
            info = key.split('_')
            f_low = float(info[3].replace('p','.'))
            f_high = float(info[5].replace('p','.'))
            eta_low = float(info[7].replace('p','.'))
            eta_high = float(info[9].replace('p','.'))
            #quantile_map[ key ] = [ f_low, f_high, eta_low, eta_high, f.Get( key ) ]
            # FIXME - what happened to ROOT in 10_5_X?
            new_f1 = ROOT.TF1( key, '([0] + [1]*x + [2]*TMath::Exp(-[3]*x))')
            new_f1.SetParameter( 0, f.Get( key ).GetParameter( 0 ) )
            new_f1.SetParameter( 1, f.Get( key ).GetParameter( 1 ) )
            new_f1.SetParameter( 2, f.Get( key ).GetParameter( 2 ) )
            new_f1.SetParameter( 3, f.Get( key ).GetParameter( 3 ) )
            quantile_map[ key ] = [ f_low, f_high, eta_low, eta_high, new_f1 ]

    elif 'tau_pt_calibrations' in calib_fName :
        for key in keys :
            info = key.split('_')
            l1eg = str(info[1].replace('p','.'))
            f_low = float(info[4].replace('p','.'))
            f_high = float(info[6].replace('p','.'))
            eta_low = float(info[8].replace('p','.'))
            eta_high = float(info[10].replace('p','.'))
            #quantile_map[ key ] = [ f_low, f_high, eta_low, eta_high, f.Get( key ) ]
            # FIXME - what happened to ROOT in 10_5_X?
            new_f1 = ROOT.TF1( key, '([0] + [1]*TMath::Exp(-[2]*x))')
            new_f1.SetParameter( 0, f.Get( key ).GetParameter( 0 ) )
            new_f1.SetParameter( 1, f.Get( key ).GetParameter( 1 ) )
            new_f1.SetParameter( 2, f.Get( key ).GetParameter( 2 ) )
            quantile_map[ key ] = [ l1eg, f_low, f_high, eta_low, eta_high, new_f1 ]

    else :
        print "File name %s does not match format of 'jet_em_calibrations_X' or 'tau_pt_calibrations_X'" % calib_fName
        return
    #for k, v in quantile_map.iteritems() :
    #    print k, v

    print "\n\n\nFIXME - what happened to ROOT in 10_5_X\nWhy are these errors here?\nThe code appears to work with my fix\n"

    return quantile_map

    

def add_jet_calibration( name_in, quantile_map ) :
    jet_pt_binning = get_x_binning(name_in)
    useBinnedPt = True
    print "Adding Phase-2 calibration branch to ttree. UseBinnedPt = %s" % useBinnedPt
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
        if cnt % 10000 == 0 : print cnt

        l1eg_pt = row.l1eg_pt
        ecal_pt = row.ecal_pt
        hcal_pt = row.hcal_pt
        jet_pt = row.jet_pt
        abs_jet_eta = abs(row.jet_eta)
        if jet_pt < 0 :
            val = -9.
            calib[0] = -9.
            calibPt[0] = -9.
        else :
            val = calibrate( quantile_map, abs_jet_eta, l1eg_pt, ecal_pt, jet_pt, jet_pt_binning, useBinnedPt )
            calib[0] = val
            calibPt[0] = l1eg_pt + ecal_pt + (val * hcal_pt)

        calibB.Fill()
        calibPtB.Fill()
    d = f_in.Get('analyzer')
    d.cd()
    t.Write('', ROOT.TObject.kOverwrite)
    f_in.Close()


    

def add_tau_calibration( name_in, quantile_map ) :
    tau_pt_binning = get_x_binning('Tau')
    useBinnedPt = True
    print "Adding Phase-2 calibration branch to ttree. UseBinnedPt = %s" % useBinnedPt
    f_in = ROOT.TFile( name_in, 'UPDATE')
    t = f_in.Get( 'analyzer/tree' )

    # new calibrations
    calib = array('f', [ 0 ] )
    calibB = t.Branch('calibHH', calib, 'calibHH/F')
    calibPt = array('f', [ 0 ] )
    calibPtB = t.Branch('calibPtHH', calibPt, 'calibPtHH/F')
    calibIsoRegionPt = array('f', [ 0 ] )
    calibIsoRegionPtB = t.Branch('calibIsoRegionPtHH', calibIsoRegionPt, 'calibIsoRegionPtHH/F')
    isoTau = array('f', [ 0 ] )
    isoTauB = t.Branch('isoTauHH', isoTau, 'isoTauHH/F')

    for k, v in quantile_map.iteritems() :
        print k, v

    # Add isolation WP similar to Run-II IsoTau
    f1Barrel = ROOT.TF1( 'isoTauBarrel', '([0] + [1]*TMath::Exp(-[2]*x))')
    f1Barrel.SetParName( 0, "y rise" )
    f1Barrel.SetParName( 1, "scale" )
    f1Barrel.SetParName( 2, "decay" )
    f1Barrel.SetParameter( 0, 0.25 )
    f1Barrel.SetParameter( 1, 0.85 )
    f1Barrel.SetParameter( 2, 0.094 )
    
    f1HGCal = ROOT.TF1( 'isoTauHGCal', '([0] + [1]*TMath::Exp(-[2]*x))')
    f1HGCal.SetParName( 0, "y rise" )
    f1HGCal.SetParName( 1, "scale" )
    f1HGCal.SetParName( 2, "decay" )
    f1HGCal.SetParameter( 0, 0.34 )
    f1HGCal.SetParameter( 1, 0.35 )
    f1HGCal.SetParameter( 2, 0.051 )

    cnt = 0
    for row in t :
        cnt += 1
        if cnt % 10000 == 0 : print cnt

        size = '3x5'
        l1eg_pt = getattr( row, 'l1eg_'+size )
        ecal_pt = getattr( row, 'ecal_'+size )
        hcal_pt = getattr( row, 'hcal_'+size )
        tau_pt = l1eg_pt + ecal_pt + hcal_pt
        abs_tau_eta = abs(row.jet_eta)
        n_L1EGs = getattr( row, 'n_l1eg_HoverE_Less0p25' )
        if tau_pt < 0 or abs_tau_eta > 3.0 :
            val = -9.
            calib[0] = -9.
            calibPt[0] = -9.
            calibIsoRegionPt[0] = -9.
            isoTau[0] = -9.
        else :
            val = calibrate_tau( quantile_map, abs_tau_eta, n_L1EGs, l1eg_pt, ecal_pt, tau_pt, tau_pt_binning, useBinnedPt )
            calib[0] = val
            calibPt[0] = tau_pt * val

            l1eg_7x7 = getattr( row, 'l1eg_7x7' )
            ecal_7x7 = getattr( row, 'ecal_7x7' )
            hcal_7x7 = getattr( row, 'hcal_7x7' )
            tau_7x7 = l1eg_7x7 + ecal_7x7 + hcal_7x7
            calibIsoRegionPt[0] = tau_7x7 * val
            # Iso WP is split by barrel and endcap
            # And, remove iso for taus > 100 GeV pT
            abs_tau_eta = abs( getattr( row, 'jet_eta' ) )
            if calibPt[0] > 100 :
                isoTau[0] = 1.
            elif abs_tau_eta <= 1.5 :
                isoTau[0] = 1. if f1Barrel.Eval( calibPt[0] ) >= ((calibIsoRegionPt[0] - calibPt[0]) / calibPt[0]) else 0.
            elif abs_tau_eta <= 3.0 :
                isoTau[0] = 1. if f1HGCal.Eval( calibPt[0] ) >= ((calibIsoRegionPt[0] - calibPt[0]) / calibPt[0]) else 0.
            else : isoTau[0] = 0.

        calibB.Fill()
        calibPtB.Fill()
        calibIsoRegionPtB.Fill()
        isoTauB.Fill()
    d = f_in.Get('analyzer')
    d.cd()
    t.Write('', ROOT.TObject.kOverwrite)
    f_in.Close()


def add_stage2_calibration( name_in, stage2_calib_file, doTaus=False ) :
    print "Adding Stage-2 calibration branch to ttree, doTaus = %s, with file %s" % (doTaus, stage2_calib_file)
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
        if cnt % 10000 == 0 : print cnt

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
        




def calibrate( quantile_map, abs_jet_eta, l1eg_pt, ecal_pt, jet_pt, jet_pt_binning, useBins=False ) :
    em_frac = (l1eg_pt + ecal_pt) / jet_pt
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



def calibrate_tau( quantile_map, abs_jet_eta, n_L1EGs, l1eg_pt, ecal_pt, jet_pt, jet_pt_binning, useBins=False ) :
    em_frac = (l1eg_pt + ecal_pt) / jet_pt
    #print "EM Frac: ",em_frac
    if em_frac == 2 : return 1.0 # These are non-recoed jets
    if em_frac > 1.0 : em_frac = 1.0 # These are some corner case problems which will be fixed and only range up to 1.05

    for k, v in quantile_map.iteritems() :

        # Choose dict for correct nL1EGs
        if v[0] == '0L1EG' and not n_L1EGs == 0 : continue
        if v[0] == '1L1EG' and not n_L1EGs == 1 : continue
        if v[0] == 'Gtr1L1EG' and not n_L1EGs > 1 : continue
        # HGCal v[0] == 'All' and has no L1EG selection

        if em_frac >= v[1] and em_frac <= v[2] :
            if abs_jet_eta >= v[3] and abs_jet_eta <= v[4] :
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


    # Commands
    #doJets = False
    #doTaus = True
    doJets = True
    doTaus = False

    make_calibrations = False
    apply_phase2_calibrations = False
    apply_stage2_calibrations = False
    prepare_calibration_cfg = False
    plot_calibrated_results = False

    # Uncomment to run!
    #make_calibrations = True
    #apply_phase2_calibrations = True
    apply_stage2_calibrations = True
    #prepare_calibration_cfg = True
    #plot_calibrated_results = True

    base = '/data/vshang/l1CaloJets_20190723_r2/'
    #base = '/data/truggles/l1CaloJets_20190417_r2/' # For Jets

    shapes = [
        # R2
        #'output_round2_HiggsTauTauv1',
        #'output_round2_minBiasv1'
        'output_round2_QCDv1',
    ]

    for shape in shapes :
        
        #jetsF0 = 'merged_QCD-PU%s.root' % shape
        #date = jetsF0.replace('merged_QCD-','').replace('.root','')
        jetsF0 = '%s.root' % shape
        date = jetsF0.replace('merged_','').replace('.root','')
        date = base.split('/')[-2].replace('l1CaloJets_','')+shape
        plotDir = '/afs/cern.ch/user/v/vshang/public/Phase2L1CaloTaus/CMSSW_10_5_0_pre1/src/L1Trigger/L1EGRateStudies/test/crab/'+date+'Vxy1'
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
            print jetFile
            tree = jetFile.Get("analyzer/tree")

            if ('qcd' in shape or 'QCD' in shape) and doJets :
                make_em_fraction_calibrations( c, base+jetsF0, cut, plotDir )
            if 'Tau' in shape and doTaus :
                make_tau_calibrations( c, base+jetsF0, cut, plotDir )
            jetFile.Close()

        """ Add new calibrations to TTree """
        if apply_phase2_calibrations :
            version = shape.split('_')[-1]
            if doJets :
                quantile_map = get_quantile_map( 'jet_em_calibrations_'+version+'.root' )
                add_jet_calibration( base+jetsF0, quantile_map )
            if doTaus :
                version = 'HiggsTauTauv1'
                quantile_map = get_quantile_map( 'tau_pt_calibrations_'+version+'.root ')
                add_tau_calibration( base+jetsF0, quantile_map )
        """ Prepare cfg calibration code snippet """
        if prepare_calibration_cfg :
            version = shape.split('_')[-1]
            ###version = 'v7'
            if doJets :
                quantile_map = get_quantile_map( 'jet_em_calibrations_'+version+'.root' )
            if doTaus :
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
            for k, cut in eta_ranges.iteritems() :
                if 'Tau' in jetsF0 and k == 'hf' : continue


                tau_pt = "(ecal_3x5 + l1eg_3x5 + hcal_3x5)"
                if 'Tau' in jetsF0 :
                    to_plot = tau_pt+'/genJet_pt:genJet_pt'
                    h1 = getTH2( tree, 'qcd1', to_plot, cut, x_and_y_bins )
                    to_plot = '( calibPtHH )/genJet_pt:genJet_pt'
                    h2 = getTH2( tree, 'qcd2', to_plot, cut, x_and_y_bins )
                    #to_plot = '(stage2tau_pt)/genJet_pt:genJet_pt'
                    to_plot = '(stage2tau_pt_calibration3)/genJet_pt:genJet_pt'
                    h3 = getTH2( tree, 's2', to_plot, cut, x_and_y_bins )
                    title1 = "Phase-II CaloTau, raw "+k
                    title2 = "Phase-II CaloTau, Calib "+k
                    title3 = "Phase-I CaloTau, Calib "+k
                else :
                    to_plot = '(jet_pt)/genJet_pt:genJet_pt'
                    h1 = getTH2( tree, 'qcd1', to_plot, cut, x_and_y_bins )
                    #to_plot = '(jet_pt_calibration)/genJet_pt:genJet_pt'
                    to_plot = '( calibPtHH )/genJet_pt:genJet_pt'
                    h2 = getTH2( tree, 'qcd2', to_plot, cut, x_and_y_bins )
                    #to_plot = '(stage2jet_pt)/genJet_pt:genJet_pt'
                    to_plot = '(stage2jet_pt_calib)/genJet_pt:genJet_pt'
                    h3 = getTH2( tree, 's2', to_plot, cut, x_and_y_bins )
                    title1 = "Phase-II CaloJet, raw "+k
                    title2 = "Phase-II CaloJet, EM Frac Calib "+k
                    title3 = "Phase-I CaloJet "+k
                xaxis = "Gen Jet P_{T} (GeV)"
                yaxis = "Relative Error in P_{T} reco/gen"
                c.SetTitle("genJetPt_Tau_"+k)
                areaNorm = True
                #areaNorm = False
                drawPointsHists3(c.GetTitle(), h1, h2, h3, title1, title2, title3, xaxis, yaxis, areaNorm, plotDir)


