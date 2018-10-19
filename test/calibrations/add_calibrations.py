import ROOT
from array import array
from collections import OrderedDict


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

    


def add_calibration( name_in, calib_in, quantile_map ) :
    f_in = ROOT.TFile( name_in, 'UPDATE')
    t = f_in.Get( 'analyzer/tree' )

    #f_calib = ROOT.TFile( calib_in, 'r' )
    #for k, v in quantile_map.iteritems() :
    #    v.append( f_calib.Get( k ) )
    #    print v

    # new calibrations
    calib = array('f', [ 0 ] )
    calibB = t.Branch('calib6', calib, 'calib6/F')

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

    quantile_map = get_quantile_map( 'new_calibrations2.root' )
    add_calibration( 'qcd2.root', 'new_calibrations.root', quantile_map )


