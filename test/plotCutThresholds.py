import ROOT
from array import array
from ROOT import gStyle
import os

ROOT.gROOT.SetBatch(True)
gStyle.SetOptStat(0)

def drawPoints(c, tree1, tree2, var, cut, xaxis, xinfo, yaxis, yinfo, points, linear=False, doFit=True, includeLine=False, invert=False) :
    print tree1
    print tree2
    doLog = False
    doLog = True
    title1 = "L1CaloTaus, ggH"
    title2 = "L1CaloTaus, minBias"
    print cut
    c.cd(1)
    if type(xinfo) == type([]) :
        h1 = ROOT.TH2F("h1", title1, xinfo[0], xinfo[1], xinfo[2], yinfo[0], yinfo[1], yinfo[2])
        h2 = ROOT.TH2F("h2", title2, xinfo[0], xinfo[1], xinfo[2], yinfo[0], yinfo[1], yinfo[2])
    elif type(xinfo) == type(array('f', [])) :
        h1 = ROOT.TH2F("h1", title1, len(xinfo)-1, xinfo, len(yinfo)-1, yinfo)
        h2 = ROOT.TH2F("h2", title2, len(xinfo)-1, xinfo, len(yinfo)-1, yinfo)
    tree1.Draw( var + " >> h1", cut )
    h1.GetXaxis().SetTitle( xaxis )
    h1.GetYaxis().SetTitle( yaxis )
    h1.Draw("colz")
    if doLog :
        ROOT.gPad.SetLogz()
        if 'tauPtVsRelIso' in c.GetTitle() :
            ROOT.gPad.SetLogy()
    xVals1 = array('f', [])
    yVals1 = array('f', [])
    for point in points :
        xVals1.append( point[0] )
        yVals1.append( getPoint( h1, point[0], point[1], invert ) )
    #print xVals1
    #print yVals1
    g1 = ROOT.TGraph(len(xVals1), xVals1, yVals1)

    # Use this with do_stage_2_tau_calibration_plots to save the fit graph
    #f_out = ROOT.TFile('stage2taus_pt.root', 'RECREATE')
    #g1.Write()
    #f_out.Close()

    mini = points[0][0]
    maxi = points[-1][0]

    # Allow option to show the jagged fitting line for optimization
    # And clean version for presentations
    fitCode = 'S 0'
    if includeLine : 
        g1.SetLineWidth( 4 )
        g1.Draw('SAME')
        fitCode = 'S'

    if not linear and doFit :
        f1 = ROOT.TF1( 'f1', '([0] + [1]*TMath::Exp(-[2]*x))', mini, maxi)
        f1.SetLineWidth( 4 )
        f1.SetParName( 0, "y rise" )
        f1.SetParName( 1, "scale" )
        f1.SetParName( 2, "decay" )
        f1.SetParameter( 0, .5 )
        f1.SetParameter( 1, 2.5 )
        f1.SetParameter( 2, .15 )
        g1.Fit('f1', fitCode )
    if linear and doFit :
        #f1 = ROOT.TF1( 'f1', '([0] + [1]*x)', mini, maxi)
        f1 = ROOT.TF1( 'f1', '([0])', mini, maxi)
        f1.SetLineWidth( 4 )
        f1.SetParName( 0, "y intercept" )
        #f1.SetParName( 1, "slope" )
        f1.SetParameter( 0, .0 )
        #f1.SetParameter( 1, 1. )
        g1.Fit('f1', fitCode )
    if doFit :
        if linear :
            #f2 = ROOT.TF1( 'f2', '([0] + [1]*x)', xinfo[1], xinfo[2])
            f2 = ROOT.TF1( 'f2', '([0])', xinfo[1], xinfo[2])
            f2.SetParameter( 0, f1.GetParameter( 0 ) )
            #f2.SetParameter( 1, f1.GetParameter( 1 ) )
        else :
            f2 = ROOT.TF1( 'f2', '([0] + [1]*TMath::Exp(-[2]*x))', xinfo[1], xinfo[2])
            f2.SetParameter( 0, f1.GetParameter( 0 ) )
            f2.SetParameter( 1, f1.GetParameter( 1 ) )
            f2.SetParameter( 2, f1.GetParameter( 2 ) )
        f2.SetLineWidth( 4 )
        f2.Draw('SAME')
    
    c.cd(2)
    tree2.Draw( var + " >> h2", cut )
    h2.GetXaxis().SetTitle( xaxis )
    h2.GetYaxis().SetTitle( yaxis )
    h2.Draw("colz")
    if doLog :
        ROOT.gPad.SetLogz()
        if 'tauPtVsRelIso' in c.GetTitle() :
            ROOT.gPad.SetLogy()
    if includeLine : 
        g1.Draw('SAME')
    if doFit :
        f2.Draw('SAME')
        #if "clusterPtVClusterIso" == c.GetTitle() :
        #    f3.Draw('SAME')
    if doLog :
        ROOT.gPad.SetLogz()
    #if c.GetTitle() == 'clusterPtVE2x2OverE2x5' :
    #    ROOT.gPad.SetLogz()
    if includeLine : 
        g1.Draw('SAME')
    if doFit :
        f2.Draw('SAME')
        #if "clusterPtVClusterIso" == c.GetTitle() :
        #    f3.Draw('SAME')

    c.Print(universalSaveDir+c.GetTitle()+".png")
    #c.Print(plotDir+"/"+c.GetTitle()+".C")
    #c.Print(plotDir+"/"+c.GetTitle()+".pdf")

    del h1, h2, g1





def getPoint( h, xVal, percentage, invert ) :
    val = 0.
    tot = 0.
    xBin = h.GetXaxis().FindBin( xVal )
    for i in range( 1, h.GetNbinsY() ) :
        tot += h.GetBinContent( xBin, i )
    targetVal = tot * percentage
    if not invert :
        for i in range( 1, h.GetNbinsY() ) :
            val += h.GetBinContent( xBin, i )
            if val >= targetVal :
                yVal = h.GetYaxis().GetBinCenter(i)
                #print "Non-Inverted Reached target of %.3f at ybin %i with yval %.2f" % (percentage, i, yVal )
                return yVal
    if invert :
        for i in range( 1, h.GetNbinsY() ) :
            invBin = h.GetNbinsY()+1-i
            val += h.GetBinContent( xBin, invBin )
            if val >= targetVal :
                yVal = h.GetYaxis().GetBinCenter(invBin)
                #print "Inverted Reached target of %.3f at ybin %i with yval %.2f" % (percentage, i, yVal )
                return yVal
    print "\n\nError, not supposed to get here\nAre you accidently asking for inverted or non-inverted when it should be the opposite?\n"



def getAverage( h, xVal ) :
    #print h
    val = 0.
    weightedTot = 0.
    tot = 0.
    xBin = h.GetXaxis().FindBin( xVal )
    for i in range( 1, h.GetNbinsY() ) :
        weightedTot += h.GetBinContent( xBin, i )*h.GetYaxis().GetBinCenter( i )
        tot += h.GetBinContent( xBin, i )
        #print weightedTot
    # Catch for empty columns
    if tot == 0. :
        return -999
    avgTot = weightedTot/tot
    
    #print "Final average total: ",avgTot
    
    answer = h.GetYaxis().FindBin( avgTot )
    #print "Associated bin: ",answer
    return avgTot



if __name__ == '__main__' :

    #tdrstyle.setTDRStyle()
    gStyle.SetOptStat(0)
    
    ggH = 'output_round2_HiggsTauTauvL1EGsv2.root'
    minBias = 'output_round2_minBiasv2.root'
    version = ggH.replace('.root','')
    
    base = '/data/truggles/l1CaloJets_20190308_r2/'
    
    #universalSaveDir = "/afs/cern.ch/user/t/truggles/www/Phase-II/"+version+"_GenTauInHGCalV5/"
    universalSaveDir = "/afs/cern.ch/user/t/truggles/www/Phase-II/"+version+"_GenTauInBarrelV5/"
    if not os.path.exists( universalSaveDir ) : os.makedirs( universalSaveDir )
    
    ggHHTTFile = ROOT.TFile( base+ggH, 'r' )
    ggH_tree = ggHHTTFile.Get("analyzer/tree")
    rateFile = ROOT.TFile( base+minBias, 'r' )
    rate_tree = rateFile.Get("analyzer/tree")
    print ggH_tree
    print rate_tree



    c = ROOT.TCanvas('c', 'c', 800, 700)
    ''' Track to cluster reco resolution '''
    c.SetCanvasSize(1500,600)
    c.Divide(2)

    cut = "(abs(jet_eta)<1.2 && jet_pt > 0)"



    # For L1TkMatch WP
    points = [ # pt, percentile # Used for cut11
        #[ 2.5,    ],
        [ 7.5,  .50 ],
        [ 10,   .50 ],
        [ 12.5, .50 ],
        [ 15,   .50 ],
        [ 17.5, .50 ],
        [ 20.0, .50 ],
        [ 22.5, .50 ],
        [ 25.0, .50 ],
        [ 27.5, .50 ],
        [ 32.5, .50 ],
        [ 35.0, .50 ],
        [ 37.5, .50 ],
        [ 42.5, .50 ],
        [ 50, .50 ],
        [ 60, .50 ],
        #[ 70, .50 ],
        #[ 80, .50 ],
        #[ 90, .50 ],
        #[ 100, .50 ],
        #[ 110, .50 ],
        #[ 120, .50 ],
        #[ 130, .50 ],
        #[ 140, .50 ],
        #[ 145, .50 ],
        ]

    reco_dm_map = {
        '0_L1EG' : '(n_l1eg_HoverE_Less0p25 == 0)',
        '1_L1EG' : '(n_l1eg_HoverE_Less0p25 == 1)',
        '2plus_L1EG' : '(n_l1eg_HoverE_Less0p25 > 1)',
        'All' : '(1)',

    }
    gen_dm_map = {
        '1pr0piZero' : '(genTau_n_prongs == 1 && genTau_n_photons == 0)',
        '1prGtr0piZero' : '(genTau_n_prongs == 1 && genTau_n_photons > 0)',
        '3pr0piZero' : '(genTau_n_prongs == 3 && genTau_n_photons == 0)',
        '3prGtr0piZero' : '(genTau_n_prongs == 3 && genTau_n_photons > 0)',
    }
        

    tau_pt = "(ecal_3x5 + l1eg_3x5 + hcal_3x5)"
    tau_pt = "(calibPtGG)"
    #for reco_k, reco_v in reco_dm_map.iteritems() :
    #    for gen_k, gen_v in gen_dm_map.iteritems() :
    #        cutX = cut+'*'+reco_v+"*"+gen_v
    #        print cutX
    #        var = "(hcal_3x5 / (ecal_3x5 + l1eg_3x5)):"+tau_pt
    #        xaxis = "Tau 3x5 P_{T} (GeV)"
    #        yaxis = "H/E"
    #        xinfo = [30, 0., 150.]
    #        xinfo = [30, 0., 60.]
    #        yinfo = [100, 0., 5.]
    #        if reco_k == '0_L1EG' :
    #            yinfo = [100, 0., 20.]
    #        c.SetTitle("tauPtVsHoverE_"+gen_k+"_"+reco_k)
    #        isoLinear = False
    #        isoLinear = True
    #        doFit = True
    #        includeGraph = True
    #        drawPoints(c, ggH_tree, rate_tree, var, cutX, xaxis, xinfo, yaxis, yinfo, points, isoLinear, doFit, includeGraph)


    points = [ [i, .99] for i in range(20, 200, 2)]
    cut = "(jet_pt>0 && abs(jet_eta)<=3.0)"
    var = "(calibPtGG / ((jet_pt_calibrate) - calibPtGG)):calibPtGG"
    var = "(((ecal_7x7 + l1eg_7x7 + hcal_7x7)*calibGG - calibPtGG) / calibPtGG):calibPtGG"
    xaxis = "Tau 3x5 P_{T} Calibrated (GeV)"
    yaxis = "Rel. Iso."
    xinfo = [40, 0., 200.]
    xinfo = [36, 20., 200.]
    yinfo = [100, 0., 5.]
    c.SetTitle("tauPtVsRelIso99")
    isoLinear = False
    #isoLinear = True
    doFit = True
    includeGraph = True
    drawPoints(c, ggH_tree, rate_tree, var, cut, xaxis, xinfo, yaxis, yinfo, points, isoLinear, doFit, includeGraph)
    points = [ [i, .95] for i in range(20, 200, 2)]
    c.SetTitle("tauPtVsRelIso95")
    drawPoints(c, ggH_tree, rate_tree, var, cut, xaxis, xinfo, yaxis, yinfo, points, isoLinear, doFit, includeGraph)
    points = [ [i, .9] for i in range(20, 200, 2)]
    c.SetTitle("tauPtVsRelIso90")
    drawPoints(c, ggH_tree, rate_tree, var, cut, xaxis, xinfo, yaxis, yinfo, points, isoLinear, doFit, includeGraph)



    """ Make the Stage-2 Tau pT correction
        The Stage-2 reco pT above 250 needs incorporation of the fine grain
        bit perhapse.  Because of that we cut at 200 GeV for reco pT.
        If making the calibration, uncomment the code in drawPoints by the
        do_stage_2_tau_calibration_plots comment. """
    do_stage_2_tau_calibration_plots = False
    if do_stage_2_tau_calibration_plots :
        points = [ [i, .5] for i in range(10, 200, 2)]
        cut = "(stage2tau_pt > 0)"
        var = "genJet_pt/stage2tau_pt:stage2tau_pt"
        xaxis = "Stage-2 Tau p_{T} (GeV)"
        yaxis = "Gen Tau p_{T} / Stage-2 Tau p_{T}"
        xinfo = [75, 0., 300.]
        yinfo = [1000, 0., 4.]
        xinfo = array('f', [])
        for i in range( 0, 100, 2 ) : xinfo.append( i )
        for i in range( 100, 150, 5 ) : xinfo.append( i )
        for i in range( 150, 201, 25 ) : xinfo.append( i )
        yinfo = array('f', [])
        for i in range( 0, 1001 ) : yinfo.append( i*0.004 )
        c.SetTitle("tauPtVsStage2Pt")
        isoLinear = False
        doFit = False
        includeGraph = True
        drawPoints(c, ggH_tree, ggH_tree, var, cut, xaxis, xinfo, yaxis, yinfo, points, isoLinear, doFit, includeGraph)
        c.SetTitle("tauPtVsStage2PtCor")
        var = "genJet_pt/stage2tau_pt_calibration3:stage2tau_pt_calibration3"
        xaxis = "Stage-2 Tau p_{T} Calib. (GeV)"
        yaxis = "Gen Tau p_{T} / Stage-2 Tau p_{T} Calib."
        drawPoints(c, ggH_tree, ggH_tree, var, cut, xaxis, xinfo, yaxis, yinfo, points, isoLinear, doFit, includeGraph)




