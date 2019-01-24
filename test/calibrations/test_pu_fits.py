import ROOT
import L1Trigger.L1EGRateStudies.trigHelpers as trigHelpers
from L1Trigger.L1EGRateStudies.trigHelpers import setLegStyle
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)


if '__main__' in __name__ :
    date = '20190123v7'
    saveDir = '/afs/cern.ch/user/t/truggles/www/Phase-II/puTest_'+date+'_res/'
    trigHelpers.checkDir( saveDir )
    base = '/data/truggles/l1CaloJets_'+date+'/'
    names = [
        #'minBias_PU0.root',
        'minBias_PU200.root',
        #'ttbar_PU0.root',
        'ttbar_PU200.root',
    ]

    pu_fits = ROOT.TFile( 'fits_pu.root', 'READ' )

    fits = {
        'minBiasnvtx_init_i_ecal_hits_leq_threshold' : [],
        'minBiasnvtx_init_i_hcal_hits_leq_threshold' : [],
        'minBiasnvtx_init_i_hf_hits_leq_threshold' : [],
        'minBiasnvtx_init_i_hgcalEM_hits_leq_threshold' : [],
        'minBiasnvtx_init_i_hgcalHad_hits_leq_threshold' : [],
    }

    cnt = 1
    h_min = -.6
    h_max = .5
    nb = 100
    for k, v in fits.iteritems() :
        v.append( pu_fits.Get( k ) )
        v.append( ROOT.TH1F( k, k, nb, h_min, h_max ) )
        v[1].SetLineColor( cnt )
        v[1].SetLineWidth( 2 )
        cnt += 1


    h_avg = ROOT.TH1F( 'Nvtx Estimation Resolution', 'Nvtx Estimation Resolution;nvtx (reco-gen)/gen;A.U.', nb, h_min, h_max )
    h_avg.SetLineWidth( 3 )

    for name in names :
        f = ROOT.TFile( base+name, 'READ' )
        t = f.Get( 'analyzer/hit_tree' )
        cnt = 0
        for row in t :
            cnt += 1
            #if cnt > 10 : break
        
            nvtx = row.nvtx_init
            tot = 0.
            for k, v in fits.iteritems() :
                var_name = k.replace( 'minBiasnvtx_init_','' )
                var = getattr( row, var_name )
                # Get subdetector based estimate
                val = v[0].Eval( var )
                #print '\t%30s    nvtx estimate: %.1f' % (k, val) 
                # add for running avg

                # This is to remove the poor resolution HF from the avg to improve it
                #tot += val
                if not '_hf_' in k :
                    tot += val

                # fill resolution plot
                v[1].Fill( (val - nvtx) / nvtx )
            #print "Gen nvtx: %.1f    Estimated nvtx: %.1f" % (nvtx, tot/len(fits) )

            # This is to remove the poor resolution HF from the avg to improve it
            #h_avg.Fill( ( (tot/ (len(fits)) ) - nvtx) / nvtx )
            h_avg.Fill( ( (tot/ (len(fits)-1) ) - nvtx) / nvtx )

        c = ROOT.TCanvas('c','c',800,800)
        h_avg.Scale( 1. / h_avg.Integral() )
        maxi = h_avg.GetMaximum()
        h_avg.Draw()
        leg = setLegStyle(0.65,0.5,0.9,0.87)
        for k, v in fits.iteritems() :
            v[1].Scale( 1. / v[1].Integral() )
            v[1].Draw('SAME')
            if v[1].GetMaximum() > maxi : maxi = v[1].GetMaximum()
            leg.AddEntry(v[1], k.split('_i_')[-1].split('_hits_')[0],"l")
        leg.AddEntry(h_avg, "average", "l")
        leg.Draw("SAME")
        h_avg.SetMaximum( maxi * 1.1 )
        #c.SaveAs( saveDir+name.replace('.root','')+'res.png' )
        c.SaveAs( saveDir+name.replace('.root','')+'res2.png' )

        fit_min = -0.2
        fit_max = 0.2
        shape = ROOT.TF1("shape", "gaus(0)", fit_min, fit_max )
        h_avg.Fit(shape, "R")
        fitResult = h_avg.GetFunction("shape")
        fitResults = []
        i = 0.
        fitResults.append( ROOT.TLatex(.15, .7, "Gaussian Fit:" ))
        fitResults.append( ROOT.TLatex(.15, .66-i*.13, "mean(hist): "+format(h_avg.GetMean(1), '.2g')))
        fitResults.append( ROOT.TLatex(.15, .62-i*.13, "#mu(fit): "+format(fitResult.GetParameter(1), '.2g')))
        fitResults.append( ROOT.TLatex(.15, .58-i*.13, "#sigma: "+format(fitResult.GetParameter(2), '.2g')))
        fitResults.append( ROOT.TLatex(.15, .54-i*.13, "fit range:"))
        fitResults.append( ROOT.TLatex(.15, .50-i*.13, "  [%.2f, %.2f]" % (fit_min, fit_max)))
        res = fitResult.GetParameter(2) / h_avg.GetMean(1)
        #fitResults.append( ROOT.TLatex(.15, .48-i*.13, "#sigma/#mu: "+format( res, '.3g')))
        for i in range( len(fitResults) ) :
            fitResults[i].SetTextSize(0.045)
            fitResults[i].SetTextFont(42)
            fitResults[i].SetNDC()
            fitResults[i].Draw()
        #c.SaveAs( saveDir+name.replace('.root','')+'res_text.png' )
        c.SaveAs( saveDir+name.replace('.root','')+'res2_text.png' )


