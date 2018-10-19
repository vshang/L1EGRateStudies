import ROOT
from array import array
from collections import OrderedDict


def get_quantile_map() :

    quantile_map = OrderedDict()

    quantile_list = [0,0.0605,0.1355,0.1975,0.2525,0.3065,0.3645,0.4305,0.5185,0.6745,1] # see get_quantiles.py
    for i in range(len(quantile_list)-1) :
        f_low = quantile_list[i]
        f_high = quantile_list[i+1]
        quantile_map['EM_frac_%s_to_%s' % (str(f_low).replace('.','p'), str(f_high).replace('.','p'))] = \
                [ f_low, f_high ]
    #for k, v in quantile_map.iteritems() :
    #    print k, v

    return quantile_map

    


def add_calibration( name_in, calib_in, quantile_map ) :
    f_in = ROOT.TFile( name_in, 'UPDATE')
    t = f_in.Get( 'analyzer/tree' )

    f_calib = ROOT.TFile( calib_in, 'r' )
    for k, v in quantile_map.iteritems() :
        v.append( f_calib.Get( k ) )
        print v

    # new calibrations
    calib = array('f', [ 0 ] )
    calibB = t.Branch('calib', calib, 'calib/F')

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
    quantile_map[ 'EM_frac_0p6745_to_1' ] = [quantile_map[ 'EM_frac_0p6745_to_1' ][0], 2.0, quantile_map[ 'EM_frac_0p6745_to_1' ][2] ]
    em_frac = (ecal_L1EG_jet_pt + ecal_pt) / jet_pt
    #print "EM Frac: ",em_frac
    if em_frac == 2 : return 1.0 # These are non-recoed jets
    for k, v in quantile_map.iteritems() :
        if em_frac >= v[0] and em_frac <= v[1] :
            return v[2].Eval( jet_pt )
    print "Shouldn't get here, em_frac ",em_frac
    return 1.0



#dZCut( 'qcd.root', 'new_calibrations.root')
quantile_map = get_quantile_map()
add_calibration( 'qcd2.root', 'new_calibrations.root', quantile_map )


