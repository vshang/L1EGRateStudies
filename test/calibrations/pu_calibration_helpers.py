import ROOT
import math
from L1Trigger.L1EGRateStudies.trigHelpers import setLegStyle
from array import array
import L1Trigger.L1EGRateStudies.trigHelpers as trigHelpers
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)


# Provide number of towers for the geometrical area for energy normalization
#def get_n_towers( sub_detector, eta_range ) :
#    sub_detector_map = {
#'ecal' : {
#    'er1to3' :
#    'er4to6' : 
#    'er7to9' : 
#    'er10to12' : 
#    'er13to15' : 
#    'er16to18' :
#}
#
#
#
#    }
    


def make_PU_SFs( c, base, name, calo ) :

    # Output function file
    f_out = ROOT.TFile( 'PU_SF_%s_functions.root' % calo, 'RECREATE' )
    trigHelpers.checkDir( saveDir+'SFs/' )

    h_max = 270
    n_bins = 27
    delta = h_max / n_bins

    f200 = ROOT.TFile( base+name, 'r' )
    #f140 = ROOT.TFile( base+name.replace('200','140'), 'r' )
    f0 = ROOT.TFile( base+name.replace('200','0'), 'r' )
    h = ROOT.TH2F( 'SF_hist', 'SF_hist;iEta Bin;nvtx', 6, 0, 6, 27, 0, h_max )
    #h = ROOT.TH2F( 'SF_hist', 'SF_hist;iEta Bins;nvtx', 6, 0, 6, 10, 150, 250 )
    #h = ROOT.TH2F( 'SF_hist', 'SF_hist;iEta Bins;nvtx', 6, 0, 6, 1, 0, 10 )
    t200 = f200.Get( 'analyzer/hit_tree' )
    #t140 = f140.Get( 'analyzer/hit_tree' )
    t0 = f0.Get( 'analyzer/hit_tree' )
    iEta_index = 0
    mini = 99
    for iEta in ['er1to3', 'er4to6', 'er7to9', 'er10to12', 'er13to15', 'er16to18'] :
        h1 = ROOT.TH1F( 'SF_hist_%s' % iEta, 'SF_hist;nvtx', 27, 0, h_max )
        x_vals = array('f', [])
        y_vals = array('f', [])
        for nvtx in range( 0, h_max+1, delta ) :
            nvtx_low = nvtx
            nvtx_high = nvtx+10
            cut = '(nvtx_init >= %i && nvtx_init < %i)' % (nvtx_low, nvtx_high)
            h_n_hits = ROOT.TH1F('hits','hits',1000,0,10000)
            h_ET_sum = ROOT.TH1F('et_sum','et_sum',1000,0,10000)
            # Use PU0 sample for lowest nvtx bin
            if nvtx == 0 :
                t0.Draw( 'i_%s_hits_%s >> hits' % (calo, iEta), cut )
                t0.Draw( 'f_%s_hits_%s >> et_sum' % (calo, iEta), cut )
            #elif nvtx >= 90 and nvtx < 160 : 
            #    t140.Draw( 'i_%s_hits_%s >> hits' % (calo, iEta), cut )
            #    t140.Draw( 'f_%s_hits_%s >> et_sum' % (calo, iEta), cut )
            else : 
                t200.Draw( 'i_%s_hits_%s >> hits' % (calo, iEta), cut )
                t200.Draw( 'f_%s_hits_%s >> et_sum' % (calo, iEta), cut )
            if h_n_hits.Integral() > 0. :
                #print iEta_index, nvtx+delta, h_ET_sum.GetMean() / h_n_hits.GetMean()
                #h.Fill( iEta_index, nvtx+delta, h_ET_sum.GetMean() / h_n_hits.GetMean() )
                #if h_ET_sum.GetMean() / h_n_hits.GetMean() < mini : mini = h_ET_sum.GetMean() / h_n_hits.GetMean()
                #h1.SetBinContent( h1.FindBin( nvtx+delta), h_ET_sum.GetMean() / h_n_hits.GetMean() )
                #h1.SetBinError( h1.FindBin( nvtx+delta), 1./math.sqrt(h_ET_sum.Integral()) )
                print iEta_index, nvtx+delta, h_ET_sum.GetMean()
                h.Fill( iEta_index, nvtx+delta, h_ET_sum.GetMean() )
                x_vals.append( nvtx+delta )
                y_vals.append( h_ET_sum.GetMean() )
                if h_ET_sum.GetMean() < mini : mini = h_ET_sum.GetMean()
                h1.SetBinContent( h1.FindBin( nvtx+delta), h_ET_sum.GetMean() )
                h1.SetBinError( h1.FindBin( nvtx+delta), 1./math.sqrt(h_ET_sum.Integral()) )
            del h_n_hits, h_ET_sum
        h.GetXaxis().SetBinLabel( iEta_index+1, iEta )
        iEta_index += 1
        # for some reason there is an event at nvtx 40
        #h1.SetBinContent( 5, 0 )
        #h1.SetBinError( 5, 0 )
        f = ROOT.TF1('f1','[0] + [1] * x', h1.GetXaxis().GetBinLowEdge(1), h1.GetXaxis().GetBinUpEdge( h1.GetNbinsX() ) )
        h1.Fit( f )
        f2 = ROOT.TF1('%s_%s' % (calo, iEta),'[0] + [1] * x', h1.GetXaxis().GetBinLowEdge(2), h1.GetXaxis().GetBinUpEdge( h1.GetNbinsX() ) )
        h1.Fit( f2, "R" )
        h1.SetLineWidth( 2 )
        f.SetLineWidth( 2 )
        f2.SetLineWidth( 2 )
        f2.SetLineColor( ROOT.kBlue )
        #h1.Draw()
        g1 = ROOT.TGraph( len(x_vals), x_vals, y_vals )
        g1.SetTitle( 'ET_sum_graph_%s_%s' % (calo, iEta) )
        g1.SetName( 'ET_sum_graph_%s_%s' % (calo, iEta) )
        g1.SetLineColor( ROOT.kBlack )
        g1.SetLineWidth( 2 )
        g1.GetYaxis().SetTitle( 'MinBias E_{T} Sum (GeV)' )
        g1.GetXaxis().SetTitle( 'Number of Simulated Vertices' )
        g1.Draw()
        f.Draw('l same')
        f2.Draw('l same')
        f_out.cd()
        g1.Write()
        #f2.Write()
        c.SaveAs( saveDir+'SFs/SFs_%s_%s.png' % (calo, iEta) )
        del h1, f
    f_out.Close()
    h.SetMinimum( h.GetMinimum() )
    h.GetZaxis().SetRangeUser( mini, h.GetMaximum() )
    h.Draw('colz')
    ROOT.gPad.SetRightMargin( .15 )
    c.SaveAs( saveDir+'SFs/SFs_%s.png' % calo )
    #c.SaveAs( saveDir+'SFs_PU200_%s.png' % calo )
    #c.SaveAs( saveDir+'SFs_PU0_%s.png' % calo )
    


def draw_comp_hist( base, names, var, x_and_y_bins ) :

    name_var = var.replace(':','_')
    hists = []
    cnt = 1
    for n in names :
        f = ROOT.TFile( base+n, 'r' )
        h = ROOT.TH2F( name_var, name_var, x_and_y_bins[0], x_and_y_bins[1], x_and_y_bins[2], x_and_y_bins[3], x_and_y_bins[4], x_and_y_bins[5] )
        t = f.Get( 'analyzer/hit_tree' )
        t.Draw( var+' >> '+name_var )
        #h.Scale ( 1. / h.Integral() )
        h.SetLineColor( cnt )
        h.SetMarkerColor( cnt )
        h.SetDirectory(0)
        h.GetXaxis().SetTitle( var.split(':')[1] )
        h.GetYaxis().SetTitle( var.split(':')[0] )
        h.SetName( f.GetName().replace('puTest/','').replace('.root','') )
        cnt += 1
        hists.append( h )
    return hists

def make_comp_hist( base, names, var, scan=[0,10], hist_max=-1 ) :

    hists = []
    cnt = 1
    for n in names :
        f = ROOT.TFile( base+n, 'r' )
        h = f.Get( 'analyzer/'+var )
        if h.Integral() > 0. :
        #    h.Scale ( 1. / h.Integral() )
            h.Scale ( 1. / f.Get( 'analyzer/NEvents' ).Integral() )
        h.SetLineColor( cnt )
        h.SetMarkerColor( cnt )
        h.SetDirectory(0)
        h.GetXaxis().SetTitle( var+' (GeV)' )
        h.GetYaxis().SetTitle( 'A.U.' )
        h.SetTitle( var )
        h.SetName( f.GetName().replace('puTest/','').replace('.root','') )
        if hist_max != -1 :
            h.GetXaxis().SetRangeUser( 0, hist_max )
        cnt += 1
        hists.append( h )
    return hists

def plot_fit_params( c, var, x_y_info, fit_params ) :
    c.Clear()
    leg = setLegStyle(0.2,0.5,0.45,0.87)
    n_map = {
        1 : 'minBias',
        2 : 'ttbar',
        3 : 'qcd',
    }
    funcs = []
    cnt = 1
    max_v = 0. 
    for fit_vals in fit_params :
        f = ROOT.TF1('f'+str(cnt),'[0] + [1] * x', fit_vals[2], fit_vals[3] )
        f.SetParameter(0, fit_vals[0] )
        f.SetParameter(1, fit_vals[1] )
        f.SetLineColor( cnt )
        #f.GetXaxis().SetTitle( var.split(':')[1] )
        #f.GetYaxis().SetTitle( var.split(':')[0] )
        if f.Eval( fit_vals[3] ) > max_v : max_v = f.Eval( fit_vals[3] )
        funcs.append( f )
        cnt += 1
    cnt = 1
    funcs[0].Draw('ec')
    #funcs[0].SetMaximum( max_v * 1.1 )
    # this version of SetRange is: (x_low, y_low, x_max, y_max)
    #    'nvtx_init:i_hf_hits_leq_threshold' : [60, 0, 1000, 100, 0, 300], # not so good...
    #funcs[0].SetRange( x_y_info[1], x_y_info[2], max_v, x_y_info[5] )
    funcs[0].SetRange( x_y_info[1], x_y_info[4], x_y_info[2], 300 )
    #funcs[0].GetYaxis().SetRangeUser( max_v, x_y_info[5] )
    #funcs[0].GetXaxis().SetRangeUser( x_y_info[1], x_y_info[2] )
    #funcs[0].Draw('ec')
    funcs[0].GetXaxis().SetTitle( var.split(':')[1] )
    funcs[0].GetYaxis().SetTitle( var.split(':')[0] )
    funcs[0].SetTitle( var.split(':')[1] )
    for f in funcs :
        f.Draw('ec same')
        leg.AddEntry(f, n_map[cnt],"l")
        cnt += 1
    leg.Draw()
    ROOT.gPad.SetLogy(0)
    ROOT.gPad.SetLogz(0)
    print var
    #c.SaveAs( saveDir+'fits_'+var.replace(':','_')+'.root' )
    c.SaveAs( saveDir+'fits_'+var.replace(':','_')+'.png' )
    f_out = ROOT.TFile( 'fits_'+var.replace(':','_')+'.root', 'RECREATE' )
    f_out.cd()
    cnt = 1
    for f in funcs :
        f.SetTitle( n_map[cnt]+var.replace(':','_') )
        f.SetName( n_map[cnt]+var.replace(':','_') )
        cnt += 1
        f.Write()
    f_out.Close()
    


def plot_hists( c, var, hists, set_logy=False, append='' ) :
    #for i in range( scan[0], scan[1]+1 ) :
    #    for h in hists :
    #        print "%20s   fraction >= %i: %f" % (h.GetName(), i, h.Integral( i, h.GetNbinsX() ) )
    colz = ''
    if 'TH2' in str(type(hists)) :
        hists.Draw('hist colz')
        ROOT.gPad.SetLeftMargin(.15)
        f = ROOT.TF1('f1_'+append,'[0] + [1] * x', hists.GetXaxis().GetBinLowEdge(1), hists.GetXaxis().GetBinUpEdge( hists.GetNbinsX() ) )
        hists.Fit( f )
        f.Draw('l same')
        ROOT.gPad.SetLogz()
    if 'list' in str(type(hists)) :
        maxi = 0.
        for h in hists :
            if h.GetMaximum() > maxi : maxi = h.GetMaximum()
            if var == 'ecal_hits_et' : h.Rebin( 4 ) 
            if var == 'hcal_hits_et' : h.Rebin( 4 )
            if var == 'l1eg_hits_et' : h.Rebin( 4 )
            if var == 'hgcalEM_hits_et' : h.Rebin( 1 ) 
            if var == 'hgcalHad_hits_et' : h.Rebin( 1 ) 
            if var == 'hf_hits_et' : h.Rebin( 8 ) 
        if 'hits_et' in var :
            hists[0].GetXaxis().SetRangeUser( 0, 10 )
        #hists[0].Draw('hist')
        hists[0].Draw('E0L')
        hists[0].SetMaximum( maxi * 10 )
        if 'hits_et' in var :
            ROOT.gPad.SetLogy()
        else :
            ROOT.gPad.SetLogy(0)
        ROOT.gPad.Update()
        leg = setLegStyle(0.5,0.5,0.95,0.87)
        marker = 20
        for h in hists :
            h.SetMarkerStyle( marker )
            marker += 1
            h.SetMarkerSize( 1 )
            h.SetLineWidth( 2 )
            #h.Draw('hist SAME')
            h.Draw('E0L SAME')
            leg.AddEntry(h, h.GetName().split('/')[-1],"lpe")
        leg.Draw()
    if set_logy :
        ROOT.gPad.SetLogy()
    else :
        ROOT.gPad.SetLogy(0)
    c.SaveAs( saveDir+append+'_'+var.replace(':','_')+'.png' )
    if 'TH2' in str(type(hists)) :
        #return
        return [hists.GetFunction('f1_'+append).GetParameter(0), hists.GetFunction('f1_'+append).GetParameter(1), \
            hists.GetXaxis().GetBinLowEdge(1), hists.GetXaxis().GetBinUpEdge( hists.GetNbinsX() )]
        
def to_add( hists ) :
    h1 = hists.pop(0).Clone()
    h1.SetDirectory(0)
    for h in hists :
        h1.Add( h )
    return h1


    
if '__main__' in __name__ :
    date = '20190123v8'
    saveDir = '/afs/cern.ch/user/t/truggles/www/Phase-II/puTest_'+date+'/'
    trigHelpers.checkDir( saveDir )
    base = '/data/truggles/l1CaloJets_'+date+'/'
    c = ROOT.TCanvas('c','c',800,800)
    names = [
        'minBias_PU0.root',
        'minBias_PU200.root',
        'ttbar_PU0.root',
        'ttbar_PU200.root',
        #'qcd_PU0.root',
        #'qcd_PU200.root'
        ]
    scan=[0,10]
    hist_max=10
    var_map = {
        'total_hits_et' : ([0, 50], 50),
        #'total_et_sum' : ([0, 3000], -1),
        'ecal_hits_et' : ([0, 10], 50),
        #'ecal_et_sum' : ([0, 3000], -1),
        'hcal_hits_et' : ([0, 50], 50),
        #'hcal_et_sum' : ([0, 3000], -1),
        'l1eg_hits_et' : ([0, 50], 50),
        #'l1eg_et_sum' : ([0, 3000], -1),
        'unc_hits_et' : ([0, 50], 50),
        #'unc_et_sum' : ([0, 3000], -1),
        'hgcalEM_hits_et' : ([0, 50], 50),
        'hgcalHad_hits_et' : ([0, 50], 50),
        'hf_hits_et' : ([0, 50], 50),
    }
    for k, v in var_map.iteritems() :
        hists = make_comp_hist( base,names,k,v[0],v[1] )
        plot_hists( c, k, hists, True )
    
    draw_map = {
        ##'i_total_hits:nvtx_init' : [100, 0, 300, 60, 0, 3000],
        ##'f_total_hits:nvtx_init' : [100, 0, 300, 60, 0, 6000],
        ##'i_total_hits_gtr_threshold:nvtx_init' : [100, 0, 300, 60, 0, 1500],
        ##'f_total_hits_gtr_threshold:nvtx_init' : [100, 0, 300, 60, 0, 6000],
        ##'i_total_hits_leq_threshold:nvtx_init' : [100, 0, 300, 60, 0, 1500],
        ##'f_total_hits_leq_threshold:nvtx_init' : [100, 0, 300, 60, 0, 1500],
        #'i_ecal_hits:nvtx_init' : [100, 0, 300, 60, 0, 800],
        #'f_ecal_hits:nvtx_init' : [100, 0, 300, 60, 0, 1000],
        #'i_ecal_hits_gtr_threshold:nvtx_init' : [100, 0, 300, 60, 0, 800],
        #'f_ecal_hits_gtr_threshold:nvtx_init' : [100, 0, 300, 60, 0, 200],
        #'i_ecal_hits_leq_threshold:nvtx_init' : [100, 0, 300, 60, 0, 800],
        #'f_ecal_hits_leq_threshold:nvtx_init' : [100, 0, 300, 60, 0, 1000],
        #'i_hcal_hits:nvtx_init' : [100, 0, 300, 60, 0, 800],
        #'f_hcal_hits:nvtx_init' : [100, 0, 300, 60, 0, 4000],
        #'i_hcal_hits_gtr_threshold:nvtx_init' : [100, 0, 300, 60, 0, 800],
        #'f_hcal_hits_gtr_threshold:nvtx_init' : [100, 0, 300, 60, 0, 4000],
        #'i_hcal_hits_leq_threshold:f_hcal_hits' : [60, 0, 4000, 60, 0, 800],
        #'i_hcal_hits_leq_threshold:nvtx_init' : [100, 0, 300, 60, 0, 800],
        #'f_hcal_hits_leq_threshold:nvtx_init' : [100, 0, 300, 60, 0, 1500],
        ##'i_l1eg_hits:nvtx_init' : [100, 0, 300, 60, 0, 100],
        ##'f_l1eg_hits:nvtx_init' : [100, 0, 300, 60, 0, 4000],
        ##'i_l1eg_hits_gtr_threshold:nvtx_init' : [100, 0, 300, 60, 0, 100],
        ##'f_l1eg_hits_gtr_threshold:nvtx_init' : [100, 0, 300, 60, 0, 1500],
        ##'i_l1eg_hits_leq_threshold:nvtx_init' : [100, 0, 300, 60, 0, 100],
        ##'f_l1eg_hits_leq_threshold:nvtx_init' : [100, 0, 300, 60, 0, 1500],
        'nvtx_init:i_ecal_hits_leq_threshold' : [60, 0, 600, 100, 0, 300], # good
        'nvtx_init:i_hcal_hits_leq_threshold' : [60, 0, 300, 100, 0, 300], # decent
        'nvtx_init:i_hgcalEM_hits_leq_threshold' : [60, 0, 1000, 100, 0, 300], # decent, needs zero PU for minB
        'nvtx_init:i_hgcalHad_hits_leq_threshold' : [60, 0, 1000, 100, 0, 300], # okay
        'nvtx_init:i_hf_hits_leq_threshold' : [60, 0, 1000, 100, 0, 300], # not so good...
        #'nvtx_init:f_hf_hits_leq_threshold' : [60, 0, 3000, 100, 0, 300],

        #'nvtx_init:i_ecal_hits_gtr_threshold' : [60, 0, 600, 100, 0, 300],
        #'nvtx_init:i_hcal_hits_gtr_threshold' : [60, 0, 300, 100, 0, 300],
        #'nvtx_init:i_hgcalEM_hits_gtr_threshold' : [60, 0, 3000, 100, 0, 300],
        #'nvtx_init:i_hgcalHad_hits_gtr_threshold' : [60, 0, 3000, 100, 0, 300],
        #'nvtx_init:i_hf_hits_gtr_threshold' : [60, 0, 1000, 100, 0, 300],
        #'nvtx_init:f_hf_hits_gtr_threshold' : [60, 0, 1000, 100, 0, 300],

        #'nvtx_init:f_hgcalHad_hits' : [60, 0, 2000, 100, 0, 300],
        #'nvtx_init:f_hgcalEM_hits' : [60, 0, 5000, 100, 0, 300],
        #'nvtx_init:f_hf_hits' : [60, 0, 10000, 100, 0, 300],
        #'nvtx_init:i_hgcalHad_hits' : [60, 0, 1000, 100, 0, 300],
        #'nvtx_init:i_hgcalEM_hits' : [60, 0, 1000, 100, 0, 300],
        #'nvtx_init:i_hf_hits' : [60, 0, 1000, 100, 0, 300],
    }

    namesMB = [
        'minBias_PU0.root',
        'minBias_PU200.root',
    ]
    namesTT = [
        'ttbar_PU0.root',
        'ttbar_PU200.root',
    ]
    namesQCD = [
        'qcd_PU0.root',
        'qcd_PU200.root'
    ]

    for k, v in draw_map.iteritems() :
        fits = []
        hists = draw_comp_hist( base,namesMB,k,v )
        h = to_add( hists )
        fits.append( plot_hists( c, k, h, False, namesMB[0].split('_')[0] ) )
        hists = draw_comp_hist( base,namesTT,k,v )
        h = to_add( hists )
        fits.append( plot_hists( c, k, h, False, namesTT[0].split('_')[0] ) )
        #hists = draw_comp_hist( base,namesQCD,k,v )
        #h = to_add( hists )
        #fits.append( plot_hists( c, k, h, False, namesQCD[0].split('_')[0] ) )

        plot_fit_params( c, k, v, fits )

    name = 'minBias_PU200.root'
    make_PU_SFs( c, base, name, 'ecal' )
    make_PU_SFs( c, base, name, 'hcal' )


