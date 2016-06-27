import ROOT
from array import array
from ROOT import gStyle

gStyle.SetOptStat(0)

def drawPoints(c, tree1, var, cut, title1, tree2, title2, xaxis, xinfo, yaxis, yinfo, points, linear=False, doFit=True, includeLine=False) :
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
        yVals1.append( getPoint( h1, point[0], point[1] ) )
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
        f1.SetParName( 0, "y rise" )
        f1.SetParName( 1, "scale" )
        f1.SetParName( 2, "decay" )
        f1.SetParameter( 0, .5 )
        f1.SetParameter( 1, 2.5 )
        f1.SetParameter( 2, .15 )
        g1.Fit('f1', fitCode )
    if linear and doFit :
        f1 = ROOT.TF1( 'f1', '([0] + [1]*x)', mini, maxi)
        f1.SetParName( 0, "y intercept" )
        f1.SetParName( 1, "slope" )
        f1.SetParameter( 0, .0 )
        f1.SetParameter( 1, 1. )
        g1.Fit('f1', fitCode )
    if doFit :
        f2 = ROOT.TF1( 'f2', '([0] + [1]*TMath::Exp(-[2]*x))', mini, maxi)
        f2.SetParameter( 0, f1.GetParameter( 0 ) )
        f2.SetParameter( 1, f1.GetParameter( 1 ) )
        f2.SetParameter( 2, f1.GetParameter( 2 ) )
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
    c.Print("plotsTmp/"+c.GetTitle()+".pdf")
    del h1, h2, g1


def drawPointsHists(h1, h2, title1, title2, xaxis, yaxis) :
    c2 = ROOT.TCanvas('c2', 'c2', 1200, 600)
    c2.Divide(2)
    c2.cd(1)
    h1.GetXaxis().SetTitle( xaxis )
    h1.GetYaxis().SetTitle( yaxis )
    h1.Draw("colz")
    xVals1 = array('f', [])
    yVals1 = array('f', [])

    points = []
    for i in range(7, 50) : points.append( i )
    for point in points :
        xVals1.append( point )
        yVals1.append( getAverage( h1, point ) )
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
    h2.Draw("colz")
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
    c2.Print("plotsTmp/"+c.GetTitle()+".pdf")
    cx = ROOT.TCanvas('cx','cx',600,600)
    cx.SetGridx()
    cx.SetGridy()
    f3 = ROOT.TF1( 'f3', '(-([0] + [1]*TMath::Exp(-[2]*x))+([3] + [4]*TMath::Exp(-[5]*x)))', mini, maxi)
    f3.SetParameter( 0, f1.GetParameter( 0 ) )
    f3.SetParameter( 1, f1.GetParameter( 1 ) )
    f3.SetParameter( 2, f1.GetParameter( 2 ) )
    f3.SetParameter( 3, f2.GetParameter( 0 ) )
    f3.SetParameter( 4, f2.GetParameter( 1 ) )
    f3.SetParameter( 5, f2.GetParameter( 2 ) )
    for i in range( 0, 6 ) :
        print "Fit Param: %i = %f" % (i, f3.GetParameter( i ) )
    f3.Draw()
    g1.Draw('SAME')
    g2.Draw('SAME')
    
    cx.Print("plotsTmp/"+c.GetTitle()+"_fits.pdf")
    del c2, h1, h2, g1, g2, cx




def getPoint( h, xVal, percentage ) :
    val = 0.
    tot = 0.
    xBin = h.GetXaxis().FindBin( xVal )
    for i in range( 1, h.GetNbinsY() ) :
        tot += h.GetBinContent( xBin, i )
    targetVal = tot * percentage
    for i in range( 1, h.GetNbinsY() ) :
        val += h.GetBinContent( xBin, i )
        if val >= targetVal :
            yVal = h.GetYaxis().GetBinCenter(i)
            #print "Reached target of %.3f at ybin %i with yval %.2f" % (percentage, i, yVal )
            return yVal
    print "Error, not supposed to get here"



def getAverage( h, xVal ) :
    val = 0.
    weightedTot = 0.
    tot = 0.
    xBin = h.GetXaxis().FindBin( xVal )
    for i in range( 1, h.GetNbinsY() ) :
        weightedTot += h.GetBinContent( xBin, i )*h.GetYaxis().GetBinCenter( i )
        tot += h.GetBinContent( xBin, i )
        #print weightedTot
    avgTot = weightedTot/tot
    #print "Final average total: ",avgTot
    
    answer = h.GetYaxis().FindBin( avgTot )
    #print "Associated bin: ",answer
    return avgTot
    print "Error, not supposed to get here"



if __name__ == '__main__' :
    rateFile = ROOT.TFile( 'egTriggerRates.root', 'r' )
    effFile = ROOT.TFile( 'egTriggerEff.root', 'r' )
    crystal_tree = effFile.Get("analyzer/crystal_tree")
    rate_tree = rateFile.Get("analyzer/crystal_tree")
    c = ROOT.TCanvas('c', 'c', 800, 700)
    ''' Track to cluster reco resolution '''
    c.SetCanvasSize(1200,600)
    c.Divide(2)

    points = [ # pt, percentile # Used for cut11
        [  5,   .80 ],
        [ 7.5,  .85 ],
        [ 10,   .90 ],
        [ 12.5, .925 ],
        [ 15,   .95 ],
        [ 17.5, .96 ],
        [ 22.5, .96 ],
        [ 27.5, .97 ],
        [ 32.5, .985 ],
        [ 37.5, .99 ],
        [ 42.5, .995 ],
        [ 47.5, .995 ]]
#    points = [ # pt, percentile
#        #[  5,   .60 ],
#        #[ 10,   .80 ],
#        #[ 15,   .90 ],
#        #[ 22.5, .95 ],
#        #[ 27.5, .96 ],
#        #[ 32.5, .97 ],
#        [ 37.5, .995 ],
#        [ 42.5, .995 ],
#        [ 47.5, .995 ]]

    cut = ""

#    cut = "(((0.415233 + 1.51272 * TMath::Exp(-0.10266*cluster_pt)) > cluster_hovere) && ((1.08154 + 4.28457 *TMath::Exp(-0.0556304*cluster_pt)) > cluster_iso))"
#    cut += "*(( cluster_pt>25 || (trackDeltaR < 0.35)*(abs(trackDeltaPhi)<.3)*(abs(trackDeltaEta)<.3)*(((trackPt - cluster_pt)/trackPt)>-2)))"
#    cut += "*( (-0.474475 + cluster_pt*-0.00613679) < bremStrength )"
    #cut += "*(trackIsoConeTrackCount < 7)"
    #showerShape = "(-0.892035+ 0.240369*TMath::Exp(-0.0791789 * cluster_pt)>((-1)*e2x5/e5x5) )"
    #hovere = "(0.430149 +3.28952*TMath::Exp(-0.128499 * cluster_pt)>cluster_hovere )"
    #iso = "(1.22987+ 7.24192*TMath::Exp(-0.0760816 * cluster_pt)>cluster_iso )"
    #cut = iso+"*"+showerShape+"*"+hovere

    title1 = "L1EGamma Crystal (Electrons)"
    title2 = "L1EGamma Crystal (Fake)"

    recoGenPtHist = effFile.Get("analyzer/reco_gen_pt")
    tdrRecoGenPtHist = effFile.Get("analyzer/l1extraParticlesUCT:All_reco_gen_pt")
    xaxis = "Gen P_{T} (GeV)"
    yaxis = "Relative Error in P_{T} (reco-gen)/gen"
    c.SetTitle("genPtVPtResFit")
    drawPointsHists(recoGenPtHist, tdrRecoGenPtHist, title1, title2, xaxis, yaxis)

    c.SetTitle("genPtVPtResFit_CrystalsAdjusted")
    h1 = ROOT.TH2F('h1_', 'EG Relative Momentum Error', 50, 0, 50, 60, -.3, .3)
    crystal_tree.Draw('((crystal_pt_to_RCT2015 - gen_pt)/gen_pt):gen_pt >> h1_')
    drawPointsHists(h1, tdrRecoGenPtHist, title1, title2, xaxis, yaxis)
    del h1
#
#
#    """ Our different cuts """
#    showerShapes = "(-0.921128 + 0.180511*TMath::Exp(-0.0400725*cluster_pt)>(-1)*(e2x5/e5x5))"
#    Isolation = "((0.990748 + 5.64259*TMath::Exp(-0.0613952*cluster_pt))>cluster_iso)"
#    tkIsoMatched = "((0.106544 + 0.00316748*cluster_pt)>(trackIsoConePtSum/trackPt))"
#
#    cut_none = ""
#    cut_ss = showerShapes
#    cut_ss_cIso = showerShapes+"*"+Isolation
#    cut_ss_cIso_tkNoM = cut_ss_cIso+"*(trackDeltaR>0.1)"
#    cut_ss_cIso_tkM = cut_ss_cIso+"*(trackDeltaR<0.1)"
#    cut_ss_cIso_tkM_tkIso = cut_ss_cIso_tkM+"*"+tkIsoMatched
#
#
#
#    var = "(-e2x5/e5x5):cluster_pt"
#    xaxis = "Cluster P_{T} (GeV)"
#    yaxis = "Negative Energy 2x5/5x5"
#    xinfo = [20, 0., 50.]
#    yinfo = [100, -1.1, -0.4]
#    c.SetTitle("clusterPtVE2x5OverE5x5")
#    drawPoints(c, crystal_tree, var, cut_none, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo, points)
#
#    var = "(-e2x5/e3x5):cluster_pt"
#    xaxis = "Cluster P_{T} (GeV)"
#    yaxis = "Negative Energy 2x5/3x5"
#    xinfo = [20, 0., 50.]
#    yinfo = [100, -1.1, -0.4]
#    c.SetTitle("clusterPtVE2x5OverE3x5")
#    drawPoints(c, crystal_tree, var, cut_none, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo, points)
#
#    var = "(-pt2x5/pt5x5):cluster_pt"
#    xaxis = "Cluster P_{T} (GeV)"
#    yaxis = "Negative P_{T} 2x5/5x5"
#    xinfo = [20, 0., 50.]
#    yinfo = [100, -1.1, -0.4]
#    c.SetTitle("clusterPtVPt2x5OverPt5x5")
#    drawPoints(c, crystal_tree, var, cut_none, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo, points)
#
#    var = "(-pt2x5/pt3x5):cluster_pt"
#    xaxis = "Cluster P_{T} (GeV)"
#    yaxis = "Negative P_{T} 2x5/3x5"
#    xinfo = [20, 0., 50.]
#    yinfo = [100, -1.1, -0.4]
#    c.SetTitle("clusterPtVPt2x5OverPt3x5")
#    drawPoints(c, crystal_tree, var, cut_none, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo, points)
#
#    var = "cluster_iso:cluster_pt"
#    xaxis = "Cluster P_{T} (GeV)"
#    yaxis = "Cluster Iso"
#    xinfo = [20, 0., 50.]
#    yinfo = [250, 0., 10.]
#    c.SetTitle("clusterPtVClusterIso")
#    drawPoints(c, crystal_tree, var, cut_ss, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo, points)
#
#    # Used to check if poor dR match is likely due to a brem, or not
#    # Conclusion: we just didn't find the right track (or it didn't exist)
#    #for val in range( 0, 10 ) :
#    #    v = val*0.05
#    #    var = "bremStrength:((trackPt-cluster_pt)/cluster_pt)"
#    #    top = v + 0.05
#    #    bottom = v
#    #    yaxis = "Brem Strength"
#    #    xaxis = "%.2f < #DeltaR < %.2f Cut: P_{T} Res (L1Tk-L1EG)/L1EG" % (bottom, top)
#    #    yinfo = [60, 0., 1.1]
#    #    xinfo = [25, -1., 5.]
#    #    c.SetTitle("clusterPtResVBremStr_dRCuts_%i" % val)
#    #    cutNew = cut+"*( trackDeltaR > %f && trackDeltaR < %f)" % (bottom, top)
#    #    drawPoints(c, crystal_tree, var, cutNew, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo, points, True, False)
#
#    var = "trackDeltaR:cluster_pt"
#    xaxis = "Cluster P_{T} (GeV)"
#    yaxis = "Track #Delta R"
#    xinfo = [20, 0., 50.]
#    yinfo = [100, -.05, 1.]
#    c.SetTitle("clusterPtVDR_ss_cIso")
#    drawPoints(c, crystal_tree, var, cut_ss_cIso, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo, points, True, False)
#
#    var = "deltaR:cluster_pt"
#    xaxis = "Cluster P_{T} (GeV)"
#    yaxis = "#Delta R (Gen, L1EG)"
#    xinfo = [20, 0., 50.]
#    yinfo = [100, -.05, 1.]
#    c.SetTitle("clusterPtVDRgen_ss_cIso")
#    drawPoints(c, crystal_tree, var, cut_ss_cIso, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo, points, True, False)
#
#    var = "trackDeltaR:cluster_pt"
#    xaxis = "Cluster P_{T} (GeV)"
#    yaxis = "Track #Delta R"
#    xinfo = [20, 0., 50.]
#    yinfo = [100, -.05, 1.]
#    c.SetTitle("clusterPtVDR_ss_cIso_tkM")
#    drawPoints(c, crystal_tree, var, cut_ss_cIso_tkM, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo, points, True, False)
#
#    var = "deltaR:cluster_pt"
#    xaxis = "Cluster P_{T} (GeV)"
#    yaxis = "#Delta R (Gen, L1EG)"
#    xinfo = [20, 0., 50.]
#    yinfo = [100, -.05, 1.]
#    c.SetTitle("clusterPtVDRgen_ss_cIso_tkNoM")
#    drawPoints(c, crystal_tree, var, cut_ss_cIso_tkNoM, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo, points, True, False)
#
#    var = "deltaR:cluster_pt"
#    xaxis = "Cluster P_{T} (GeV)"
#    yaxis = "#Delta R (Gen, L1EG)"
#    xinfo = [20, 0., 50.]
#    yinfo = [100, -.05, 1.]
#    c.SetTitle("clusterPtVDRgen_ss_cIso_tkM")
#    drawPoints(c, crystal_tree, var, cut_ss_cIso_tkM, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo, points, True, False)
#
#    var = "TMath::Sqrt((trackEta-trackHighestPtEta)*(trackEta-trackHighestPtEta)+(trackPhi-trackHighestPtPhi)*(trackPhi-trackHighestPtPhi)):cluster_pt"
#    xaxis = "Cluster P_{T} (GeV)"
#    yaxis = "#Delta R (matched L1Tk, highest p_{T} L1Tk)"
#    xinfo = [20, 0., 50.]
#    yinfo = [100, -.05, 5.]
#    c.SetTitle("clusterPtVDRL1TkHighestPt_ss_cIso_tkM")
#    drawPoints(c, crystal_tree, var, cut_ss_cIso_tkM, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo, points, True, False)
#
#    var = "TMath::Sqrt((trackEta-trackHighestPtCutChi2Eta)*(trackEta-trackHighestPtCutChi2Eta)+(trackPhi-trackHighestPtCutChi2Phi)*(trackPhi-trackHighestPtCutChi2Phi)):cluster_pt"
#    xaxis = "Cluster P_{T} (GeV)"
#    yaxis = "#Delta R (matched L1Tk, highest p_{T} L1Tk Chi2<100)"
#    xinfo = [20, 0., 50.]
#    yinfo = [100, -.05, 5.]
#    c.SetTitle("clusterPtVDRL1TkHighestPtCutChi2_ss_cIso_tkM")
#    drawPoints(c, crystal_tree, var, cut_ss_cIso_tkM, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo, points, True, False)
#
#    points = [ # pt, percentile # Used for cut11
#        [  5,   .90 ],
#        [ 7.5,  .90 ],
#        [ 10,   .95 ],
#        [ 12.5, .95 ],
#        [ 15,   .98 ],
#        [ 17.5, .99 ],
#        [ 22.5, .99 ],
#        [ 27.5, .99 ],
#        [ 32.5, .99 ],
#        [ 37.5, .99 ],
#        [ 42.5, .995 ],
#        [ 47.5, .995 ]]
#
#    var = "trackIsoConePtSum/trackPt:cluster_pt"
#    xaxis = "Cluster P_{T} (GeV)"
#    yaxis = "Track Isolation"
#    xinfo = [10, 0., 50.]
#    yinfo = [120, -.1, 5.]
#    c.SetTitle("clusterPtVTrackIsolation_ss_cIso_tkM")
#    drawPoints(c, crystal_tree, var, cut_ss_cIso_tkM, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo, points, True)
#
#    var = "trackPt:cluster_pt"
#    xaxis = "Cluster P_{T} (GeV)"
#    yaxis = "Track P_{T} (GeV)"
#    xinfo = [50, 0., 50.]
#    yinfo = [52, 0., 52.]
#    c.SetTitle("clusterPtVTrackPt_ss_cIso")
#    drawPoints(c, crystal_tree, var, cut_ss_cIso, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo, points, True, False)
#
#    var = "trackPt:gen_pt"
#    xaxis = "Gen P_{T} (GeV)"
#    yaxis = "Track P_{T} (GeV)"
#    xinfo = [50, 0., 50.]
#    yinfo = [52, 0., 52.]
#    c.SetTitle("genPtVTrackPt_ss_cIso")
#    drawPoints(c, crystal_tree, var, cut_ss_cIso, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo, points, True, False)
#
#    var = "gen_pt:cluster_pt"
#    xaxis = "Cluster P_{T} (GeV)"
#    yaxis = "Gen P_{T} (GeV)"
#    xinfo = [50, 0., 50.]
#    yinfo = [52, 0., 52.]
#    c.SetTitle("clusterPtVGenPt_ss_cIso")
#    drawPoints(c, crystal_tree, var, cut_ss_cIso, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo, points, True, False)
#
#    var = "trackPt:gen_pt"
#    xaxis = "Gen P_{T} (GeV)"
#    yaxis = "Track P_{T} (GeV)"
#    xinfo = [50, 0., 50.]
#    yinfo = [52, 0., 52.]
#    c.SetTitle("genPtVTrackPt_ss_cIso_tkNoM")
#    drawPoints(c, crystal_tree, var, cut_ss_cIso_tkNoM, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo, points, True, False)
#
#    var = "trackPt:cluster_pt"
#    xaxis = "Cluster P_{T} (GeV)"
#    yaxis = "Track P_{T} (GeV)"
#    xinfo = [50, 0., 50.]
#    yinfo = [52, 0., 52.]
#    c.SetTitle("clusterPtVTrackPt_ss_cIso_tkNoM")
#    drawPoints(c, crystal_tree, var, cut_ss_cIso_tkNoM, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo, points, True, False)
#
#    var = "gen_pt:cluster_pt"
#    xaxis = "Cluster P_{T} (GeV)"
#    yaxis = "Gen P_{T} (GeV)"
#    xinfo = [50, 0., 50.]
#    yinfo = [52, 0., 52.]
#    c.SetTitle("clusterPtVGenPt_ss_cIso_tkNoM")
#    drawPoints(c, crystal_tree, var, cut_ss_cIso_tkNoM, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo, points, True, False)
#
#    var = "gen_pt:cluster_pt"
#    xaxis = "Cluster P_{T} (GeV)"
#    yaxis = "Gen P_{T} (GeV)"
#    xinfo = [50, 0., 50.]
#    yinfo = [52, 0., 52.]
#    c.SetTitle("clusterPtVGenPt_ss_cIso_tkM")
#    drawPoints(c, crystal_tree, var, cut_ss_cIso_tkM, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo, points, True, False)
#
#    var = "trackPt:gen_pt"
#    xaxis = "Gen P_{T} (GeV)"
#    yaxis = "Track P_{T} (GeV)"
#    xinfo = [50, 0., 50.]
#    yinfo = [52, 0., 52.]
#    c.SetTitle("genPtVTrackPt_ss_cIso_tkM")
#    drawPoints(c, crystal_tree, var, cut_ss_cIso_tkM, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo, points, True, False)
#
#    var = "trackPt:cluster_pt"
#    xaxis = "Cluster P_{T} (GeV)"
#    yaxis = "Track P_{T} (GeV)"
#    xinfo = [50, 0., 50.]
#    yinfo = [52, 0., 52.]
#    c.SetTitle("clusterPtVTrackPt_ss_cIso_tkM")
#    drawPoints(c, crystal_tree, var, cut_ss_cIso_tkM, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo, points, True, False)
#
#
#    """ Track Isolated """
#    var = "(-1)*((trackPt-cluster_pt)/trackPt):trackPt"
#    xaxis = "Track P_{T} (GeV)"
#    yaxis = "P_{T} Resoluciton (Trk-L1)/Trk"
#    xinfo = [20, 0., 50.]
#    yinfo = [500, -1., 20.]
#    c.SetTitle("trackPtVPtRes_ss_cIso_tkM_tkIso")
#    drawPoints(c, crystal_tree, var, cut_ss_cIso_tkM_tkIso, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo, points, True)
#
#    var = "(-1)*((trackPt-cluster_pt)/trackPt):cluster_pt"
#    xaxis = "Cluster P_{T} (GeV)"
#    yaxis = "P_{T} Resoluciton (Trk-L1)/Trk"
#    xinfo = [20, 0., 50.]
#    yinfo = [500, -1., 15.]
#    c.SetTitle("clusterPtVPtRes_ss_cIso_tkM_tkIso")
#    drawPoints(c, crystal_tree, var, cut_ss_cIso_tkM_tkIso, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo, points, True)
#
##    trackIso2 = "((0.130534 + 0.0131326*cluster_pt) > (trackIsoConePtSum/trackPt))"
##    cut += "*"+trackIso2
##    var = "cluster_hovere:cluster_pt"
##    xaxis = "Cluster P_{T} (GeV)"
##    yaxis = "Cluster H/E"
##    xinfo = [20, 0., 50.]
##    yinfo = [250, 0., 15.]
##    c.SetTitle("clusterPtVHoverE")
##    drawPoints(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo, points)
##    hovere_old = "((0.40633 + 2.17848*TMath::Exp(-0.114384*cluster_pt))>cluster_hovere)"
##    hovere = "((0.426413 +2.62318 *TMath::Exp(-0.105685*cluster_pt))>cluster_hovere)"
##    #cut += "*"+hovere
##
##
##
##    points = [ # pt, percentile # Used for cut11
##        [  5,    .975 ],
##        [  15,   .975 ],
##        [  25,   .975 ],
##        [  35,   .975 ],
##        [  45,   .975 ],
##        [  55,   .975 ],
##        [  65,   .975 ],
##        [  75,   .975 ],
##        [  85,   .975 ],
##        [  95,   .975 ]]
##
##    var = "(-1)*bremStrength:trackChi2"
##    xaxis = "Track Chi2"
##    yaxis = "Brem Strength"
##    xinfo = [10, 0., 100.]
##    yinfo = [250, 0., -1.1]
##    c.SetTitle("trackChi2VBremStr")
##    drawPoints(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo, points)
#
#    #var = "trackIsoConeTrackCount/trackPt:cluster_pt"
#    #xaxis = "Cluster P_{T} (GeV)"
#    #yaxis = "Iso Cone Track Count / Track P_{T}"
#    #xinfo = [20, 0., 50.]
#    #yinfo = [250, 0., 5.]
#    #c.SetTitle("clusterPtVIsoConeTrkCntOverTrkPt")
#    #drawPoints(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo, points)
#
#    #var = "abs(trackRInv):cluster_pt"
#    #xaxis = "Cluster P_{T} (GeV)"
#    #yaxis = "abs( Track RInv )"
#    #xinfo = [20, 0., 50.]
#    #yinfo = [250, 0., 0.007]
#    #c.SetTitle("clusterPtVTrackRInv")
#    #drawPoints(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo, points)
#
##    var = "abs(trackDeltaPhi):cluster_pt"
##    xaxis = "Cluster P_{T} (GeV)"
##    yaxis = "abs( #delta#phi )"
##    xinfo = [20, 0., 50.]
##    yinfo = [500, 0., 1.]
##    c.SetTitle("clusterPtVDPhi")
##    drawPoints(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo, points, True)
##
##    var = "abs(trackDeltaEta):cluster_pt"
##    xaxis = "Cluster P_{T} (GeV)"
##    yaxis = "abs( #delta#eta )"
##    xinfo = [20, 0., 50.]
##    yinfo = [500, 0., 1.]
##    c.SetTitle("clusterPtVDEta")
##    drawPoints(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo, points, True)
##
##    var = "trackDeltaR:cluster_pt"
##    xaxis = "Cluster P_{T} (GeV)"
##    yaxis = "Track #Delta R"
##    xinfo = [20, 0., 50.]
##    yinfo = [500, 0., 1.]
##    c.SetTitle("clusterPtVDR")
##    drawPoints(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo, points, True)
##
##    points = [ # pt, percentile # Used for cut11
##        [  5,    .95 ],
##        [  15,   .95 ],
##        [  25,   .95 ],
##        [  35,   .95 ],
##        [  45,   .95 ],
##        [  55,   .95 ],
##        [  65,   .95 ],
##        [  75,   .95 ],
##        [  85,   .95 ],
##        [  95,   .95 ]]
##    var = "((-1)*(bremStrength)):cluster_pt"
##    xaxis = "Cluster P_{T} (GeV)"
##    yaxis = "Brem Strength"
##    xinfo = [20, 0., 50.]
##    yinfo = [500, -1.1, 0.]
##    c.SetTitle("clusterPtVBremStr")
##    drawPoints(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo, points, True)
#
#    #var = "trackIsoConeTrackCount:cluster_pt"
#    #xaxis = "Cluster P_{T} (GeV)"
#    #yaxis = "Iso Cone Trk Count"
#    #xinfo = [50, 0., 50.]
#    #yinfo = [60, 0., 30.]
#    #c.SetTitle("clusterPtVIsoConeNumTrks")
#    #drawPoints(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo, points, True)
##
##    var = "(trackPt/trackIsoConePtSum):cluster_pt"
##    xaxis = "Cluster P_{T} (GeV)"
##    yaxis = "Track Pt / Iso Cone Pt Sum"
##    xinfo = [20, 0., 50.]
##    yinfo = [50, 0., 50.]
##    c.SetTitle("clusterPtVTrackPtOverSumPt")
##    drawPoints(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo, points, True)
##
#    #var = "trackPt:cluster_pt"
#    #xaxis = "Cluster P_{T} (GeV)"
#    #yaxis = "Track P_{T} (GeV)"
#    #xinfo = [50, 0., 50.]
#    #yinfo = [52, 0., 52.]
#    #c.SetTitle("clusterPtVTrackPt")
#    #drawPoints(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo, points, True, False)
##
##    var = "(-1)*trackPt:cluster_pt"
##    xaxis = "Cluster P_{T} (GeV)"
##    yaxis = "Track P_{T} (GeV)"
##    xinfo = [20, 0., 50.]
##    yinfo = [200, -150., 70.]
##    c.SetTitle("clusterPtVNegTrackPt")
##    drawPoints(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo, points, True)
#
#    #points = [ # pt, percentile # Used for cut11
#    #    [  5,   .9 ],
#    #    [ 7.5,  .9 ],
#    #    [ 10,   .9 ],
#    #    [ 12.5, .9 ],
#    #    [ 15,   .9 ],
#    #    [ 17.5, .9 ],
#    #    [ 22.5, .9 ],
#    #    [ 27.5, .9 ],
#    #    [ 32.5, .9 ],
#    #    [ 37.5, .9 ],
#    #    [ 42.5, .9 ],
#    #    [ 47.5, .9 ]]
#    #var = "abs(trackRInv):cluster_pt"
#    #xaxis = "Cluster P_{T} (GeV)"
#    #yaxis = "abs( Track RInv )"
#    #xinfo = [20, 0., 50.]
#    #yinfo = [250, 0., 0.007]
#    #c.SetTitle("clusterPtVTrackRInvSelectBad")
#    #drawPoints(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo, points)
#
#    c.Clear()
#
#
#
#
