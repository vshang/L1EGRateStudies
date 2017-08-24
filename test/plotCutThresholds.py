import ROOT
from array import array
from ROOT import gStyle

ROOT.gROOT.SetBatch(True)
gStyle.SetOptStat(0)

def drawPoints(c, tree1, var, cut, tree2, tree3, xaxis, xinfo, yaxis, yinfo, points, linear=False, doFit=True, includeLine=False, invert=False) :
    title1 = "L1EGamma Crystal (Electrons)"
    title2 = "L1EGamma Crystal (Photons)"
    title3 = "L1EGamma Crystal (Fake)"
    print cut
    c.cd(1)
    h1 = ROOT.TH2F("h1", title1, xinfo[0], xinfo[1], xinfo[2], yinfo[0], yinfo[1], yinfo[2])
    tree1.Draw( var + " >> h1", cut )
    h1.GetXaxis().SetTitle( xaxis )
    h1.GetYaxis().SetTitle( yaxis )
    h1.Draw("colz")
    xVals1 = array('f', [])
    yVals1 = array('f', [])
    for point in points :
        xVals1.append( point[0] )
        yVals1.append( getPoint( h1, point[0], point[1], invert ) )
    #print xVals1
    #print yVals1
    g1 = ROOT.TGraph(len(xVals1), xVals1, yVals1)
    mini = points[0][0]
    maxi = points[-1][0]

    # Allow option to show the jagged fitting line for optimization
    # And clean version for presentations
    fitCode = 'S 0'
    if includeLine : 
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
        f1 = ROOT.TF1( 'f1', '([0] + [1]*x)', mini, maxi)
        f1.SetLineWidth( 4 )
        f1.SetParName( 0, "y intercept" )
        f1.SetParName( 1, "slope" )
        f1.SetParameter( 0, .0 )
        f1.SetParameter( 1, 1. )
        g1.Fit('f1', fitCode )
    if doFit :
        if "clusterPtVClusterIso" == c.GetTitle() :
            if linear :
                f2 = ROOT.TF1( 'f2', '([0] + [1]*x)', xinfo[1], 80)
                f2.SetParameter( 0, f1.GetParameter( 0 ) )
                f2.SetParameter( 1, f1.GetParameter( 1 ) )
            else :
                f2 = ROOT.TF1( 'f2', '([0] + [1]*TMath::Exp(-[2]*x))', xinfo[1], xinfo[2])
                f2.SetParameter( 0, f1.GetParameter( 0 ) )
                f2.SetParameter( 1, f1.GetParameter( 1 ) )
                f2.SetParameter( 2, f1.GetParameter( 2 ) )
            f3 = ROOT.TF1( 'f3', '([0] + [1]*x)', 80, 100 )
            #f3.SetParameter( 0, 0.1471537 ) # 85 GeV swap
            f3.SetParameter( 0, 0.1962996 ) # 80 GeV swap
            f3.SetParameter( 1, 0.0 )
            f3.SetLineWidth( 4 )
            f3.Draw('SAME')
        elif "clusterPtVE2x2OverE2x5" == c.GetTitle() :
            f2 = ROOT.TF1( 'f2', '([0] + [1]*x)', xinfo[1], xinfo[2])
            #f2.SetParameter( 0, 0.95 )
            #f2.SetParameter( 1, 0.0 )
            f2.SetParameter( 0, 0.96 )
            f2.SetParameter( 1, -0.0003 )
        elif "clusterPtVTrackDeltaR" == c.GetTitle() :
            f2 = ROOT.TF1( 'f2', '([0] + [1]*x)', xinfo[1], xinfo[2])
            f2.SetParameter( 0, 0.05 )
            f2.SetParameter( 1, 0.0 )
            
        else :
            if linear :
                f2 = ROOT.TF1( 'f2', '([0] + [1]*x)', xinfo[1], xinfo[2])
                f2.SetParameter( 0, f1.GetParameter( 0 ) )
                f2.SetParameter( 1, f1.GetParameter( 1 ) )
            else :
                f2 = ROOT.TF1( 'f2', '([0] + [1]*TMath::Exp(-[2]*x))', xinfo[1], xinfo[2])
                f2.SetParameter( 0, f1.GetParameter( 0 ) )
                f2.SetParameter( 1, f1.GetParameter( 1 ) )
                f2.SetParameter( 2, f1.GetParameter( 2 ) )
        f2.SetLineWidth( 4 )
        f2.Draw('SAME')
    
    c.cd(2)
    h2 = ROOT.TH2F("h2", title2, xinfo[0], xinfo[1], xinfo[2], yinfo[0], yinfo[1], yinfo[2])
    tree2.Draw( var + " >> h2", cut )
    h2.GetXaxis().SetTitle( xaxis )
    h2.GetYaxis().SetTitle( yaxis )
    h2.Draw("colz")
    if includeLine : 
        g1.Draw('SAME')
    if doFit :
        f2.Draw('SAME')
        if "clusterPtVClusterIso" == c.GetTitle() :
            f3.Draw('SAME')
    c.cd(3)
    h3 = ROOT.TH2F("h3", title3, xinfo[0], xinfo[1], xinfo[2], yinfo[0], yinfo[1], yinfo[2])
    tree3.Draw( var + " >> h3", cut )
    h3.GetXaxis().SetTitle( xaxis )
    h3.GetYaxis().SetTitle( yaxis )
    h3.Draw("colz")
    #if c.GetTitle() == 'clusterPtVE2x2OverE2x5' :
    #    ROOT.gPad.SetLogz()
    if includeLine : 
        g1.Draw('SAME')
    if doFit :
        f2.Draw('SAME')
        if "clusterPtVClusterIso" == c.GetTitle() :
            f3.Draw('SAME')

    # plot local
    #plotDir = 'plotCuts'
    # plot web
    plotDir = '/afs/cern.ch/user/t/truggles/www/Phase-II/'+date
    c.Print(plotDir+"/"+c.GetTitle()+".png")
    #c.Print(plotDir+"/"+c.GetTitle()+".C")
    #c.Print(plotDir+"/"+c.GetTitle()+".pdf")

    del h1, h2, h3, g1


def drawPointsHists(h1, h2, title1, title2, xaxis, yaxis, new=False) :
    c2 = ROOT.TCanvas('c2', 'c2', 1200, 600)
    c2.Divide(2)
    c2.cd(1)
    h1.GetXaxis().SetTitle( xaxis )
    h1.GetYaxis().SetTitle( yaxis )
    h1.SetTitle( title1 )
    h1.Draw("colz")
    ROOT.gPad.SetGrid()
    xVals1 = array('f', [])
    yVals1 = array('f', [])

    points = []
    for i in range(10, 95) : points.append( i )
    for point in points :
        # if empty column, don't appent to points
        avg = getAverage( h1, point )
        if avg == -999 : continue
        xVals1.append( point )
        yVals1.append( avg )
    #print xVals1
    #print yVals1
    g1 = ROOT.TGraph(len(xVals1), xVals1, yVals1)
    g1.Draw('SAME')
    mini = points[0]
    maxi = points[-1]
    f1 = ROOT.TF1( 'f1', '([0] + [1]*TMath::Exp(-[2]*x))', mini, maxi)
    f1.SetParName( 0, "y rise" )
    f1.SetParName( 1, "scale" )
    f1.SetParName( 2, "decay" )
    f1.SetParameter( 0, .5 )
    f1.SetParameter( 1, 2.5 )
    f1.SetParameter( 2, .15 )
    fit1 = g1.Fit('f1', 'R S')
    
    c2.cd(2)
    h2.SetTitle( title2 )
    h2.Draw("colz")
    ROOT.gPad.SetGrid()
    h2.GetXaxis().SetTitle( xaxis )
    h2.GetYaxis().SetTitle( yaxis )
    xVals2 = array('f', [])
    yVals2 = array('f', [])
    for point in points :
        xVals2.append( point )
        yVals2.append( getAverage( h2, point ) )
    #print xVals2
    #print yVals2
    g2 = ROOT.TGraph(len(xVals2), xVals2, yVals2)
    g2.Draw('SAME')
    f2 = ROOT.TF1( 'f2', '([0] + [1]*TMath::Exp(-[2]*x))', mini, maxi)
    f2.SetParName( 0, "y rise" )
    f2.SetParName( 1, "scale" )
    f2.SetParName( 2, "decay" )
    f2.SetParameter( 0, .5 )
    f2.SetParameter( 1, 2.5 )
    f2.SetParameter( 2, .15 )
    fit2 = g2.Fit('f2', 'R S')

    # Just to show the resulting fit
    # plot local
    #plotDir = 'plotCuts'
    # plot web
    plotDir = '/afs/cern.ch/user/t/truggles/www/Phase-II/'+date
    c2.Print(plotDir+"/"+c.GetTitle()+".png")
    #c2.Print(plotDir+"/"+c.GetTitle()+".C")
    #c2.Print(plotDir+"/"+c.GetTitle()+".pdf")

    cx = ROOT.TCanvas('cx','cx',600,600)
    cx.SetGridx()
    cx.SetGridy()
    if new :
        f3 = ROOT.TF1( 'f3', '(([0] + [1]*TMath::Exp(-[2]*x))*(1./([3] + [4]*TMath::Exp(-[5]*x))))', mini, maxi)
    else :
        f3 = ROOT.TF1( 'f3', '(-([0] + [1]*TMath::Exp(-[2]*x))+([3] + [4]*TMath::Exp(-[5]*x)))', mini, maxi)
    f3.SetParameter( 0, f1.GetParameter( 0 ) )
    f3.SetParameter( 1, f1.GetParameter( 1 ) )
    f3.SetParameter( 2, f1.GetParameter( 2 ) )
    f3.SetParameter( 3, f2.GetParameter( 0 ) )
    f3.SetParameter( 4, f2.GetParameter( 1 ) )
    f3.SetParameter( 5, f2.GetParameter( 2 ) )

    f3.Draw()
    #g1.Draw('SAME')
    #g2.Draw('SAME')
    
    for i in range( 0, 6 ) :
        print "Fit Param: %i = %f" % (i, f3.GetParameter( i ) )
        fitVal = ROOT.TLatex()
        fitVal.SetTextSize(0.04)
        fitVal.DrawLatexNDC(.45, .80-(i*.1), "Fit Param: %i = %f" % (i, f3.GetParameter( i ) ) )

    # Just to show the resulting fit
    # plot local
    #plotDir = 'plotCuts'
    # plot web
    plotDir = '/afs/cern.ch/user/t/truggles/www/Phase-II/'+date
    cx.Print(plotDir+"/"+c.GetTitle()+"_fits.png")
    #cx.Print(plotDir+"/"+c.GetTitle()+"_fits.C")
    #cx.Print(plotDir+"/"+c.GetTitle()+"_fits.pdf")

    del c2, h1, h2, g1, g2, cx




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

    date = 'v9'

    singleE = 'r2_phase2_singleElectron_%s.root' % date
    singlePho = 'r2_phase2_singlePhoton_%s.root' % date
    minBias = 'r2_phase2_minBias_%s.root' % date

    date = '20170824cutStudy'

    rateFile = ROOT.TFile( minBias, 'r' )
    effFile = ROOT.TFile( singleE, 'r' )
    effPhoFile = ROOT.TFile( singlePho, 'r' )

    crystal_tree = effFile.Get("analyzer/crystal_tree")
    crystal_treePho = effPhoFile.Get("analyzer/crystal_tree")
    rate_tree = rateFile.Get("analyzer/crystal_tree")
    c = ROOT.TCanvas('c', 'c', 800, 700)
    ''' Track to cluster reco resolution '''
    c.SetCanvasSize(1500,600)
    c.Divide(3)

    points = [ # pt, percentile # Used for cut11
        #[  5,   .80 ],
        #[ 7.5,  .85 ],
        #[ 10,   .90 ],
        #[ 12.5, .925 ],
        #[ 15,   .95 ],
        [  5,   .96 ],
        [ 7.5,  .96 ],
        [ 10,   .96 ],
        [ 12.5, .96 ],
        [ 15,   .96 ],
        [ 17.5, .96 ],
        [ 22.5, .96 ],
        [ 27.5, .97 ],
        [ 32.5, .985 ],
        [ 37.5, .99 ],
        [ 42.5, .99 ],
        [ 50, .995 ],
        [ 60, .995 ],
        [ 70, .995 ],
        [ 80, .995 ],
        [ 90, .995 ],
        ]

    cut = ""


    l1Crystal2DPtResHist = effFile.Get("analyzer/reco_gen_pt")
    stage22DPtResHist = effFile.Get("analyzer/stage2_reco_gen_pt")
    xaxis = "Gen P_{T} (GeV)"
    yaxis = "Relative Error in P_{T} (reco-gen)/gen"
    title1 = "L1EG Crystal Algo"
    title2 = "Stage-2"
    c.SetTitle("genPtVPtResFit")
    drawPointsHists(l1Crystal2DPtResHist, stage22DPtResHist, title1, title2, xaxis, yaxis)

    l1Crystal2DPtResHist2 = effFile.Get("analyzer/reco_gen_pt2")
    stage22DPtResHist2 = effFile.Get("analyzer/stage2_reco_gen_pt2")
    xaxis = "Reco P_{T} (GeV)"
    yaxis = "Relative Error in P_{T} (reco-gen)/gen"
    title1 = "L1EG Crystal Algo"
    title2 = "Stage-2"
    c.SetTitle("genPtVPtResFit2")
    drawPointsHists(l1Crystal2DPtResHist2, stage22DPtResHist2, title1, title2, xaxis, yaxis)

    l1Crystal2DPtResHist3 = effFile.Get("analyzer/reco_gen_pt3")
    stage22DPtResHist3 = effFile.Get("analyzer/stage2_reco_gen_pt3")
    xaxis = "Reco P_{T} (GeV)"
    yaxis = "Relative Error in P_{T} gen/reco"
    title1 = "L1EG Crystal Algo"
    title2 = "Stage-2"
    c.SetTitle("genPtVPtResFit3")
    drawPointsHists(l1Crystal2DPtResHist3, stage22DPtResHist3, title1, title2, xaxis, yaxis, True)

    l1Crystal2DPtAdjResHist = effFile.Get("analyzer/reco_gen_pt_adj")
    yaxis = "Relative Error in P_{T} (reco-gen)/gen"
    c.SetTitle("genPtVPtAdjResFit")
    drawPointsHists(l1Crystal2DPtAdjResHist, stage22DPtResHist2, title1, title2, xaxis, yaxis)

    l1Crystal2DPtAdjResHist = effFile.Get("analyzer/reco_gen_pt_adj3")
    yaxis = "Relative Error in P_{T} gen/reco"
    c.SetTitle("genPtVPtAdjResFit3")
    drawPointsHists(l1Crystal2DPtAdjResHist, stage22DPtResHist3, title1, title2, xaxis, yaxis, True)

    #c.SetTitle("genPtVPtResFit_CrystalsAdjusted")
    #h1 = ROOT.TH2F('h1_', 'EG Relative Momentum Error', 50, 0, 50, 60, -.3, .3)
    #crystal_tree.Draw('((crystal_pt_to_RCT2015 - gen_pt)/gen_pt):gen_pt >> h1_')
    #drawPointsHists(h1, tdrRecoGenPtHist, title1, title2, xaxis, yaxis)
    #del h1

    ## Reco PT normalization
    #c.SetTitle("genPtVPtResFit_CrystalsCheck")
    #h1 = ROOT.TH2F('h1_', 'EG Relative Momentum Error', 50, 0, 50, 60, -.3, .3)
    #crystal_tree.Draw('((cluster_pt - gen_pt)/gen_pt):gen_pt >> h1_')
    #drawPointsHists(h1, tdrRecoGenPtHist, title1, title2, xaxis, yaxis)
    #del h1

    #c.SetTitle("genPtVPtResFit_CrystalsECAL_PU_Corr")
    #h1 = ROOT.TH2F('h1_', 'EG Relative Momentum Error', 50, 0, 50, 60, -.3, .3)
    #crystal_tree.Draw('(( (cluster_pt-ecalPUtoPt/97) - gen_pt)/gen_pt):gen_pt >> h1_')
    #drawPointsHists(h1, tdrRecoGenPtHist, title1, title2, xaxis, yaxis)
    #del h1

    #c.SetTitle("genPtVPtResFit_CrystalsCheck_1plusPUin3x5")
    #h1 = ROOT.TH2F('h1_', 'EG Relative Momentum Error', 50, 0, 50, 60, -.3, .3)
    #crystal_tree.Draw('((cluster_pt - gen_pt)/gen_pt):gen_pt >> h1_','trackPUTrackCnt3x5DiffZ==0')
    #drawPointsHists(h1, tdrRecoGenPtHist, title1, title2, xaxis, yaxis)
    #del h1


    ##################
    ### FROZEN 62X ###
    ##################
    from loadCuts import getCutMap
    cutMap = getCutMap()
    showerShapesF = "(-0.896501 + 0.181135*TMath::Exp(-0.0696926*cluster_pt)>(-1)*(e2x5/e5x5))"
    IsolationF = "((1.0614 + 5.65869*TMath::Exp(-0.0646173*cluster_pt))>cluster_iso)"
    cut_ss_cIsoF = showerShapesF+"*"+IsolationF

    #######################
    ### In Progress 90X ###
    #######################
    # when changing from 500 to 250 MeV, you need to change the points settings
    # to get a good fit.  Also change the fit function of clusterPtVClusterIso
    # set as linear for 500 MeV, exponential for 250 MeV
    energy = '500MeV'
    isoLinear = False # For 250 MeV
    isoLinear = True # for 500 MeV
    Isolation9 = cutMap['90x'+energy]['isolation']
    showerShapes9 = cutMap['90x'+energy]['showerShape']
    cut_none = ""
    cut_ss_cIso9 = showerShapes9+" && "+Isolation9
    cut_ss_cIso9_pt10 = cut_ss_cIso9+" && cluster_pt>10"
    
    points = [ # pt, percentile # Used for cut11
        [ 15,   .95 ],
        [ 17.5, .96 ],
        [ 22.5, .96 ],
        [ 27.5, .97 ],
        [ 32.5, .985 ],
        [ 37.5, .99 ],
        [ 42.5, .99 ],
        [ 50, .995 ],
        [ 60, .995 ],
        [ 70, .995 ],
        [ 80, .995 ],
        [ 90, .995 ],
        ]


    #var = "(-e2x5/e5x5):cluster_pt"
    var = "(e2x5/e5x5):cluster_pt"
    xaxis = "Cluster P_{T} (GeV)"
    yaxis = "Energy 2x5/5x5"
    xinfo = [25, 0., 100.]
    #yinfo = [100, -1.05, -0.7]
    yinfo = [100, 0.7, 1.05]
    c.SetTitle("clusterPtVE2x5OverE5x5")
    drawPoints(c, crystal_tree, var, cut_none, crystal_treePho, rate_tree, xaxis, xinfo, yaxis, yinfo, points, False, True, False, True)
    c.SetTitle("clusterPtVE2x5OverE5x5_fitLine")
    drawPoints(c, crystal_tree, var, cut_none, crystal_treePho, rate_tree, xaxis, xinfo, yaxis, yinfo, points, False, True, True, True) # Draw fit line


    # There is lots of discriminating power in Iso if we tighten it a bit at low Pt
    points = [ # pt, percentile # Used for cut11
        [ 2.5,   .85 ],
        [ 7.5,  .85 ],
        [ 10,   .90 ],
        [ 12.5, .90 ],
        [ 15,   .94 ],
        [ 17.5, .96 ],
        [ 22.5, .96 ],
        [ 27.5, .97 ],
        [ 32.5, .985 ],
        [ 37.5, .99 ],
        [ 42.5, .99 ],
        [ 50, .995 ],
        [ 60, .995 ],
        [ 70, .995 ],
        [ 80, .995 ],
        [ 90, .995 ],
        [ 97, 1. ],
        ]

    var = "cluster_iso:cluster_pt"
    xaxis = "Cluster P_{T} (GeV)"
    yaxis = "Cluster Iso"
    xinfo = [20, 0., 100.]
    yinfo = [100, 0., 5.]
    c.SetTitle("clusterPtVClusterIso")
    drawPoints(c, crystal_tree, var, showerShapes9, crystal_treePho, rate_tree, xaxis, xinfo, yaxis, yinfo, points, isoLinear, True, False)
    c.SetTitle("clusterPtVClusterIso_fitLine")
    drawPoints(c, crystal_tree, var, showerShapes9, crystal_treePho, rate_tree, xaxis, xinfo, yaxis, yinfo, points, isoLinear, True, True) # Draw fit line

    points = [ # pt, percentile # Used for cut11
        [  5,   .85 ],
        [ 7.5,  .85 ],
        [ 10,   .9 ],
        [ 12.5, .9 ],
        [ 15,   .9 ],
        [ 17.5, .9 ],
        [ 22.5, .9 ],
        [ 27.5, .9 ],
        [ 32.5, .9 ],
        [ 37.5, .9 ],
        [ 42.5, .9 ],
        [ 50, .9 ],
        [ 60, .9 ],
        [ 70, .9 ],
        [ 80, .9 ],
        [ 90, .9 ],
        ]
    var = "trackDeltaR:cluster_pt"
    xaxis = "Cluster P_{T} (GeV)"
    yaxis = "Trk #DeltaR"
    xinfo = [20, 0., 100.]
    yinfo = [25, 0., 1.]
    c.SetTitle("clusterPtVTrackDeltaR")
    drawPoints(c, crystal_tree, var, cut_ss_cIso9, crystal_treePho, rate_tree, xaxis, xinfo, yaxis, yinfo, points, False, True)
    c.SetTitle("clusterPtVTrackDeltaR_noFit")
    drawPoints(c, crystal_tree, var, cut_ss_cIso9, crystal_treePho, rate_tree, xaxis, xinfo, yaxis, yinfo, points, False, False)
    c.SetTitle("clusterPtVTrackDeltaR_fitLine")
    drawPoints(c, crystal_tree, var, cut_ss_cIso9, crystal_treePho, rate_tree, xaxis, xinfo, yaxis, yinfo, points, False, True, True)

    # Photon Cut
    var = "(e2x2/e2x5):cluster_pt"
    xaxis = "Cluster P_{T} (GeV)"
    yaxis = "Energy 2x2/2x5"
    xinfo = [25, 0., 100.]
    #yinfo = [100, -1.05, -0.7]
    yinfo = [35, 0.7, 1.05]
    c.SetTitle("clusterPtVE2x2OverE2x5")
    drawPoints(c, crystal_tree, var, cut_ss_cIso9, crystal_treePho, rate_tree, xaxis, xinfo, yaxis, yinfo, points, False, True, False, True)
    #c.SetTitle("clusterPtVE2x2OverE2x5_fitLine")
    #drawPoints(c, crystal_tree, var, cut_ss_cIso9, crystal_treePho, rate_tree, xaxis, xinfo, yaxis, yinfo, points, False, True, True, True)

    points = [ # pt, percentile # Used for cut11
        [ 15,   .95 ],
        [ 17.5, .96 ],
        [ 22.5, .96 ],
        [ 27.5, .97 ],
        [ 32.5, .985 ],
        [ 37.5, .99 ],
        [ 42.5, .99 ],
        [ 50, .995 ],
        [ 60, .995 ],
        [ 70, .995 ],
        [ 80, .995 ],
        [ 90, .995 ],
        ]
    # Check H/E
    var = "cluster_hovere:cluster_pt"
    xaxis = "Cluster P_{T} (GeV)"
    yaxis = "H/E"
    xinfo = [25, 0., 100.]
    yinfo = [50, 0., 5.]
    c.SetTitle("clusterPtVHoverE")
    drawPoints(c, crystal_tree, var, cut_ss_cIso9, crystal_treePho, rate_tree, xaxis, xinfo, yaxis, yinfo, points, False, True)
    c.SetTitle("clusterPtVHoverE_fitLine")
    drawPoints(c, crystal_tree, var, cut_ss_cIso9, crystal_treePho, rate_tree, xaxis, xinfo, yaxis, yinfo, points, False, True)
#def drawPoints(c, tree1, var, cut, tree2, tree3, xaxis, xinfo, yaxis, yinfo, points, linear=False, doFit=True, includeLine=False, invert=False) :

#
#    points = [
#        [  5,   .10 ],
#        [ 7.5,  .10 ],
#        [ 10,   .10 ],
#        [ 12.5, .10 ],
#        [ 15,   .10 ],
#        [ 17.5, .10 ],
#        [ 22.5, .10 ],
#        [ 27.5, .10 ],
#        [ 32.5, .10 ],
#        [ 37.5, .10 ],
#        [ 42.5, .10 ],
#        [ 47.5, .10 ]]
#    pointsLong = list(points)
#    pointsLong.append([ 55, .10 ])
#    pointsLong.append([ 65, .10 ])
#
#    doFit = False
#    var = "trackPt:cluster_pt"
#    xaxis = "Cluster P_{T} (GeV)"
#    yaxis = "Track P_{T} (GeV)"
#    xinfo = [35, 0., 80.]
#    yinfo = [55, 0, 55]
#    c.SetTitle("clusterPtVTrackPt")
#    drawPoints(c, crystal_tree, var, cut_ss_cIsoF, crystal_treePho, rate_tree, xaxis, xinfo, yaxis, yinfo, points, True, doFit, doFit)
#
#    cut_ss_cIsoF2 = cut_ss_cIsoF+"*(trackDeltaR<.1)"
#    c.SetTitle("clusterPtVTrackPt_trkDR")
#    drawPoints(c, crystal_tree, var, cut_ss_cIsoF2, crystal_treePho, rate_tree, xaxis, xinfo, yaxis, yinfo, points, True, doFit, doFit)
#    c.SetTitle("clusterPtVTrackPt_trkDR_trkPtKeep")
#    cut_ss_cIsoF3 = cut_ss_cIsoF+"*(trackDeltaR<.05 || trackPt < 6.)"
#    drawPoints(c, crystal_tree, var, cut_ss_cIsoF3, crystal_treePho, rate_tree, xaxis, xinfo, yaxis, yinfo, points, True, doFit, doFit)
#
#    var = "trackDeltaR:cluster_pt"
#    xaxis = "Cluster P_{T} (GeV)"
#    yaxis = "#Delta R (Track, L1 Cluster)"
#    xinfo = [20, 0., 50.]
#    yinfo = [50, 0., 0.5]
#    c.SetTitle("clusterPtVTrackDeltaR")
#    drawPoints(c, crystal_tree, var, cut_ss_cIsoF, crystal_treePho, rate_tree, xaxis, xinfo, yaxis, yinfo, points, True, doFit, doFit)
#
#    var = "-e2x2/e2x5:cluster_pt"
#    xaxis = "Cluster P_{T} (GeV)"
#    yaxis = "E2x2 / E2x5"
#    xinfo = [20, 0., 50.]
#    yinfo = [50, -1.1, -0.4]
#    c.SetTitle("clusterPtVE2x2OverE2x5")
#    drawPoints(c, crystal_tree, var, cut_ss_cIsoF, crystal_treePho, rate_tree, xaxis, xinfo, yaxis, yinfo, points, True, doFit, doFit)




