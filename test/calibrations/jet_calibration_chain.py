import ROOT
import os
from array import array
from collections import OrderedDict
from caloJetPtCalibrations import getTH2, getTH2VarBin, \
    drawPointsHists, drawPointsHists3, make_em_fraction_calibrations, \
    get_x_binning

def prepare_calibration_py_cfg( quantile_map ) :
    o_file = open('L1CaloJetCalibrations_cfi.py', 'w')
    o_file.write( "import FWCore.ParameterSet.Config as cms\n\n" )
    # Already add zero for EM frac, will add upper val for each loop
    for k, v in quantile_map.iteritems() :
        print k, v

    # EM fraction
    o_file.write( "\temFractionBins = cms.vdouble([ 0.00" )
    em_frac_list = [0.0,]
    for k, v in quantile_map.iteritems() :
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
    o_file.write( "\tabsEtaBins = cms.vdouble([ 0.00" )
    abs_eta_list = [0.0,]
    for k, v in quantile_map.iteritems() :
        # continue if not increasing value
        if v[3] <= abs_eta_list[-1] : continue
        abs_eta_list.append( v[3] )
        o_file.write( ",%.2f" % v[3] )
    o_file.write( "]),\n" )
    print abs_eta_list

    # Pt binning
    o_file.write( "\tjetPtBins = cms.vdouble([ 0.0" )
    pt_binning = []
    pt_binning_array = get_x_binning()
    for val in pt_binning_array :
        if val == 0.0 : continue # skip to keep commans easy
        pt_binning.append( val )
        o_file.write( ",%.1f" % val )
    o_file.write( "]),\n" )
    print pt_binning
        
    # Now huge loop of values for each bin
    o_file.write( "\tjetCalibrations = cms.vdouble([\n" )
    x = ROOT.Double(0.)
    y = ROOT.Double(0.)
    cnt = 1
    for k, v in quantile_map.iteritems() :
        val_string = ''
        for point in range( v[-1].GetN() ) :
            v[-1].GetPoint( point, x, y )
            #print x, y
            val_string += "%.3f, " % y

        val_string = val_string.strip(' ')
        # No comma at end if final one
        if cnt == len( quantile_map.keys() ) :
            val_string = val_string.strip(',')
        o_file.write( "\t\t%s\n" % val_string )
        #print val_string
        cnt += 1
    o_file.write( "])\n" )
            
    
    o_file.close()

def get_quantile_map( calib_fName ) :

    # Open calibration root file and get thresholds from TGraphs
    f = ROOT.TFile( calib_fName, 'r' )

    keys = []
    allKeys = f.GetListOfKeys()

    for k in allKeys :
        if k.GetClassName() == 'TGraph' :
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
    f_in = ROOT.TFile( name_in, 'UPDATE')
    t = f_in.Get( 'analyzer/tree' )

    # new calibrations
    calib = array('f', [ 0 ] )
    calibB = t.Branch('calibX', calib, 'calibX/F')
    calibPt = array('f', [ 0 ] )
    calibPtB = t.Branch('calibPtX', calibPt, 'calibPtX/F')

    cnt = 0
    for row in t :
        cnt += 1
        if cnt % 10000 == 0 : print cnt

        ecal_L1EG_jet_pt = row.ecal_L1EG_jet_pt
        ecal_pt = row.ecal_pt
        hcal_pt = row.hcal_pt
        jet_pt = row.jet_pt
        abs_jet_eta = abs(row.jet_eta)
        val = calibrate( quantile_map, abs_jet_eta, ecal_L1EG_jet_pt, ecal_pt, jet_pt )
        calib[0] = val
        calibPt[0] = ecal_L1EG_jet_pt + ecal_pt + (val * hcal_pt)

        calibB.Fill()
        calibPtB.Fill()
    d = f_in.Get('analyzer')
    d.cd()
    t.Write('', ROOT.TObject.kOverwrite)
    f_in.Close()

def calibrate( quantile_map, abs_jet_eta, ecal_L1EG_jet_pt, ecal_pt, jet_pt ) :
    em_frac = (ecal_L1EG_jet_pt + ecal_pt) / jet_pt
    #print "EM Frac: ",em_frac
    if em_frac == 2 : return 1.0 # These are non-recoed jets
    if em_frac > 1.0 : em_frac = 1.0 # These are some corner case problems which will be fixed and only range up to 1.05
    for k, v in quantile_map.iteritems() :
        if em_frac >= v[0] and em_frac <= v[1] :
            if abs_jet_eta >= v[2] and abs_jet_eta <= v[3] :
                #return v[2].Eval( jet_pt )
                if jet_pt > 500 : # Straight line extension
                    rtn = v[-1].Eval( 500 )
                else :
                    rtn = v[-1].Eval( jet_pt )

                # Ensure not returning a negative value because of
                # unpopulated low pT bins
                while (rtn < 0) :
                    jet_pt += 2
                    rtn = v[-1].Eval( jet_pt )
                    if jet_pt > 500 : break
                assert(rtn >= 0), "The calibration result is less than zero for range name %s for \
                        EM fraction %.2f and Jet pT %.2f, resulting calibration %.2f" % (k, em_frac, jet_pt, rtn)

                return rtn
    print "Shouldn't get here, em_frac ",em_frac
    return 1.0

if '__main__' in __name__ :

    base = '/data/truggles/l1CaloJets_20181027/'

    #for shape in ['7x7', '9x9', 'circL', 'circT'] :
    #for shape in ['7x7',] :
    for shape in [

        # SHape Tests
        #'qcd200_20180927_7x7',
        #'qcd200_20180927_9x9',
        #'qcd200_20180927_circL',
        #'qcd200_20180927_circT',
        #'qcd_20180927_7x7',
        #'qcd_20180927_9x9',
        #'qcd_20180927_circL',
        #'qcd_20180927_circT',

        # Threshold Tests
        #'0_PUTests_0GeV',
        #'0_PUTests_0p5GeV',
        #'0_PUTests_1GeV',
        #'0_PUTests_2GeV',
        #'200_PUTests_0GeV',
        #'200_PUTests_0p5GeV',
        #'200_PUTests_1GeV',
        #'200_PUTests_2GeV',

        # ET Test
        #'merged_QCD-PU200_OldP4Vec_0p5GeV',
        #'merged_minBias-PU200_OldP4Vec_0p5GeV',
        'merged_QCD-PU200_UsingET_0p5GeV',
        #'merged_minBias-PU200_UsingET_0p5GeV',
        #'merged_TTbar-PU200_UsingET_0p5GeV',
    ] :
        
        #jetsF0 = 'merged_QCD-PU%s.root' % shape
        #date = jetsF0.replace('merged_QCD-','').replace('.root','')
        jetsF0 = '%s.root' % shape
        date = jetsF0.replace('merged_','').replace('.root','')
        plotDir = '/afs/cern.ch/user/t/truggles/www/Phase-II/'+date+'_v5'
        if not os.path.exists( plotDir ) : os.makedirs( plotDir )

        jetFile = ROOT.TFile( base+jetsF0, 'r' )
        print jetFile
        tree = jetFile.Get("analyzer/tree")

        c = ROOT.TCanvas('c', 'c', 800, 700)
        ''' Track to cluster reco resolution '''
        c.SetCanvasSize(1500,600)
        c.Divide(3)


        """ Make new calibration root file """
        # Only make for QCD sample, for other samples, pick up the
        # results of QCD
        cut = "abs(genJet_eta)<1.1"
        #if 'QCD' in shape :
        #    make_em_fraction_calibrations( c, base+jetsF0, cut, plotDir )
        jetFile.Close()

        """ Add new calibrations to TTree """
        quantile_map = get_quantile_map( 'jet_em_calibrations.root' )
        prepare_calibration_py_cfg( quantile_map )
        #add_calibration( base+jetsF0, quantile_map )

        """ Plot Results """
        jetFile = ROOT.TFile( base+jetsF0, 'r' )
        tree = jetFile.Get("analyzer/tree")

        plot_calibrated_results = True
        plot_calibrated_results = False
        # Can't plot for minBias b/c no gen
        if 'minBias' in shape : 
            plot_calibrated_results = False
        x_and_y_bins = [28,20,300, 60,0,3]
        """ Resulting Calibrations """
        if plot_calibrated_results :
            to_plot = '(jet_pt)/genJet_pt:genJet_pt'
            h1 = getTH2( tree, 'qcd1', to_plot, cut, x_and_y_bins )
            to_plot = '(ecal_L1EG_jet_pt + ecal_pt + (hcal_pt*calibX) )/genJet_pt:genJet_pt'
            h2 = getTH2( tree, 'qcd2', to_plot, cut, x_and_y_bins )
            to_plot = '(stage2jet_pt)/genJet_pt:genJet_pt'
            h3 = getTH2( tree, 's2', to_plot, cut, x_and_y_bins )
            xaxis = "Gen Jet P_{T} (GeV)"
            yaxis = "Relative Error in P_{T} reco/gen"
            title1 = "Phase-II before HCAL calibrations"
            title2 = "Phase-II with HCAL calibrations"
            title3 = "Phase-I with calibrations"
            c.SetTitle("genJetPt_Calibrated_vs_Stage-2_PU0")
            areaNorm = True
            drawPointsHists3(c.GetTitle(), h1, h2, h3, title1, title2, title3, xaxis, yaxis, areaNorm, plotDir)


