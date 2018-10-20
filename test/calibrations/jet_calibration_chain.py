import ROOT
import os
from array import array
from collections import OrderedDict
from caloJetPtCalibrations import getTH2, getTH2VarBin, \
    drawPointsHists, drawPointsHists3, make_em_fraction_calibrations


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
        quantile_map[ key ] = [ f_low, f_high, f.Get( key ) ]
    for k, v in quantile_map.iteritems() :
        print k, v

    return quantile_map

    


def add_calibration( name_in, quantile_map ) :
    f_in = ROOT.TFile( name_in, 'UPDATE')
    t = f_in.Get( 'analyzer/tree' )

    # new calibrations
    calib = array('f', [ 0 ] )
    calibB = t.Branch('calibX', calib, 'calibX/F')

    cnt = 0
    for row in t :
        cnt += 1
        if cnt % 10000 == 0 : print cnt

        ecal_L1EG_jet_pt = row.ecal_L1EG_jet_pt
        ecal_pt = row.ecal_pt
        jet_pt = row.jet_pt
        val = calibrate( quantile_map, ecal_L1EG_jet_pt, ecal_pt, jet_pt )
        calib[0] = val

        calibB.Fill()
    d = f_in.Get('analyzer')
    d.cd()
    t.Write('', ROOT.TObject.kOverwrite)
    f_in.Close()

def calibrate( quantile_map, ecal_L1EG_jet_pt, ecal_pt, jet_pt ) :
    em_frac = (ecal_L1EG_jet_pt + ecal_pt) / jet_pt
    #print "EM Frac: ",em_frac
    if em_frac == 2 : return 1.0 # These are non-recoed jets
    if em_frac > 1.0 : em_frac = 1.0 # These are some corner case problems which will be fixed and only range up to 1.05
    for k, v in quantile_map.iteritems() :
        if em_frac >= v[0] and em_frac <= v[1] :
            #return v[2].Eval( jet_pt )
            if jet_pt > 500 : # Straight line extension
                rtn = v[2].Eval( 500 )
            else :
                rtn = v[2].Eval( jet_pt )
            assert(rtn >= 0), "The calibration result is less than zero for range name %s for \
                    EM fraction %.2f and Jet pT %.2f, resulting calibration %.2f" % (k, em_frac, jet_pt, rtn)
            return rtn
    print "Shouldn't get here, em_frac ",em_frac
    return 1.0

if '__main__' in __name__ :

    base = '/data/truggles/phaseII_qcd_20180925_v1-condor_jets/'
    base = ''
    jetsF0 = 'qcd3.root'
    base = '/data/truggles/p2/20180927_QCD_diff_jet_shapes_calib/'

    #for shape in ['7x7', '9x9', 'circL', 'circT'] :
    for shape in ['7x7',] :
        
        jetsF0 = 'qcd_20180927_%s.root' % shape
        date = '20180926_calibCheckV2_visuals7'
        date = jetsF0.replace('qcd_','').replace('.root','')
        plotDir = '/afs/cern.ch/user/t/truggles/www/Phase-II/'+date+''
        if not os.path.exists( plotDir ) : os.makedirs( plotDir )

        jetFile = ROOT.TFile( base+jetsF0, 'r' )
        tree = jetFile.Get("analyzer/tree")

        c = ROOT.TCanvas('c', 'c', 800, 700)
        ''' Track to cluster reco resolution '''
        c.SetCanvasSize(1500,600)
        c.Divide(3)


        """ Make new calibration root file """
        cut = "abs(genJet_eta)<1.1"
        make_em_fraction_calibrations( c, base+jetsF0, cut, plotDir )
        jetFile.Close()

        """ Add new calibrations to TTree """
        quantile_map = get_quantile_map( 'jet_em_calibrations.root' )
        add_calibration( base+jetsF0, quantile_map )

        """ Plot Results """
        jetFile = ROOT.TFile( base+jetsF0, 'r' )
        tree = jetFile.Get("analyzer/tree")

        plot_calibrated_results = True
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


