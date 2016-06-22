import ROOT
from array import array
from ROOT import gStyle

gStyle.SetOptStat(0)

def drawPoints(c, tree1, var, cut, title1, tree2, title2, xaxis, xinfo, yaxis, yinfo, points, linear=False, doFit=True) :
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
    if doFit :
        #g1.SetLineWidth(0)
        #g1.SetLineStyle(0)
        #g1.SetLineColor(ROOT.kViolet+5)
        g1.Draw('SAME')
    mini = points[0][0]
    maxi = points[-1][0]
    f2 = ROOT.TF1()
    if not linear and doFit :
        f1 = ROOT.TF1( 'f1', '([0] + [1]*TMath::Exp(-[2]*x))', mini, maxi)
        f1.SetParName( 0, "y rise" )
        f1.SetParName( 1, "scale" )
        f1.SetParName( 2, "decay" )
        f1.SetParameter( 0, .5 )
        f1.SetParameter( 1, 2.5 )
        f1.SetParameter( 2, .15 )
        rslt = g1.Fit('f1', 'S')
        rslt.Draw('SAME')
        #f2 = rslt.Clone()
        #print rslt.ls()
        #print f2.ls()
    if linear and doFit :
        f1 = ROOT.TF1( 'f1', '([0] + [1]*x)', mini, maxi)
        f1.SetParName( 0, "y intercept" )
        f1.SetParName( 1, "slope" )
        f1.SetParameter( 0, .0 )
        f1.SetParameter( 1, 1. )
        rslt = g1.Fit('f1', 'S')
        rslt.Draw('SAME')
        #f2 = rslt.Clone()
    
    c.cd(2)
    h2 = ROOT.TH2F("h2", title2, xinfo[0], xinfo[1], xinfo[2], yinfo[0], yinfo[1], yinfo[2])
    tree2.Draw( var + " >> h2", cut )
    h2.GetXaxis().SetTitle( xaxis )
    h2.GetYaxis().SetTitle( yaxis )
    h2.Draw("colz")
    #del g1
    if doFit :
        g1.Draw('SAME')
    c.Print("plotsTmp/"+c.GetTitle()+".pdf")
    del h1, h2, g1




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

    cut = ""
    var = "(-1)*(e2x5/e5x5):cluster_pt"
    xaxis = "Cluster P_{T} (GeV)"
    yaxis = "Energy 2x5/5x5"
    xinfo = [20, 0., 50.]
    yinfo = [250, 0., -1.]
    c.SetTitle("clusterPtVE2x5OverE5x5")
    drawPoints(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo, points)

    showerShapes = "(-0.921128 + 0.180511*TMath::Exp(-0.0400725*cluster_pt)>(-1)*(e2x5/e5x5))"
    cut += showerShapes
    var = "cluster_iso:cluster_pt"
    xaxis = "Cluster P_{T} (GeV)"
    yaxis = "Cluster Iso"
    xinfo = [20, 0., 50.]
    yinfo = [250, 0., 10.]
    c.SetTitle("clusterPtVClusterIso")
    drawPoints(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo, points)

    Isolation = "((0.990748 + 5.64259*TMath::Exp(-0.0613952*cluster_pt))>cluster_iso)"
    cut += "*"+Isolation

    var = "trackDeltaR:cluster_pt"
    xaxis = "Cluster P_{T} (GeV)"
    yaxis = "Track #Delta R"
    xinfo = [20, 0., 50.]
    yinfo = [100, -.05, 1.]
    c.SetTitle("clusterPtVDR_postE2x5overE5x5AndClusterIso")
    drawPoints(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo, points, True, False)

    points = [ # pt, percentile # Used for cut11
        [  5,   .90 ],
        [ 7.5,  .90 ],
        [ 10,   .95 ],
        [ 12.5, .95 ],
        [ 15,   .98 ],
        [ 17.5, .99 ],
        [ 22.5, .99 ],
        [ 27.5, .99 ],
        [ 32.5, .99 ],
        [ 37.5, .99 ],
        [ 42.5, .995 ],
        [ 47.5, .995 ]]

    var = "trackIsoConePtSum/trackPt:cluster_pt"
    xaxis = "Cluster P_{T} (GeV)"
    yaxis = "Track Isolation"
    xinfo = [10, 0., 50.]
    yinfo = [120, -.1, 5.]
    c.SetTitle("clusterPtVTrackIsolation")
    drawPoints(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo, points, True)

    var = "trackPt:cluster_pt"
    xaxis = "Cluster P_{T} (GeV)"
    yaxis = "Track P_{T} (GeV)"
    xinfo = [50, 0., 50.]
    yinfo = [52, 0., 52.]
    c.SetTitle("clusterPtVTrackPt")
    drawPoints(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo, points, True, False)

    var = "trackPt:cluster_pt"
    xaxis = "Cluster P_{T} (GeV)"
    yaxis = "Track P_{T} (GeV)"
    xinfo = [50, 0., 50.]
    yinfo = [52, 0., 52.]
    c.SetTitle("clusterPtVTrackPt_nonMatchedTracks")
    drawPoints(c, crystal_tree, var, cut+"*(trackDeltaR>.1)", title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo, points, True, False)

    trkMatch = "((trackDeltaR<.1))"
    cut += "*"+trkMatch
    var = "trackIsoConePtSum/trackPt:cluster_pt"
    xaxis = "Cluster P_{T} (GeV)"
    yaxis = "Track Isolation"
    xinfo = [10, 0., 50.]
    yinfo = [120, -.1, 5.]
    c.SetTitle("clusterPtVTrackIsolation_matchedTracks")
    drawPoints(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo, points, True)

    var = "trackPt:cluster_pt"
    xaxis = "Cluster P_{T} (GeV)"
    yaxis = "Track P_{T} (GeV)"
    xinfo = [50, 0., 50.]
    yinfo = [52, 0., 52.]
    c.SetTitle("clusterPtVTrackPt_matchedTracks")
    drawPoints(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo, points, True, False)

#    trackIso2 = "((0.130534 + 0.0131326*cluster_pt) > (trackIsoConePtSum/trackPt))"
#    cut += "*"+trackIso2
#    var = "cluster_hovere:cluster_pt"
#    xaxis = "Cluster P_{T} (GeV)"
#    yaxis = "Cluster H/E"
#    xinfo = [20, 0., 50.]
#    yinfo = [250, 0., 15.]
#    c.SetTitle("clusterPtVHoverE")
#    drawPoints(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo, points)
#    hovere_old = "((0.40633 + 2.17848*TMath::Exp(-0.114384*cluster_pt))>cluster_hovere)"
#    hovere = "((0.426413 +2.62318 *TMath::Exp(-0.105685*cluster_pt))>cluster_hovere)"
#    #cut += "*"+hovere
#
#
#
#    points = [ # pt, percentile # Used for cut11
#        [  5,    .975 ],
#        [  15,   .975 ],
#        [  25,   .975 ],
#        [  35,   .975 ],
#        [  45,   .975 ],
#        [  55,   .975 ],
#        [  65,   .975 ],
#        [  75,   .975 ],
#        [  85,   .975 ],
#        [  95,   .975 ]]
#
#    var = "(-1)*bremStrength:trackChi2"
#    xaxis = "Track Chi2"
#    yaxis = "Brem Strength"
#    xinfo = [10, 0., 100.]
#    yinfo = [250, 0., -1.1]
#    c.SetTitle("trackChi2VBremStr")
#    drawPoints(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo, points)

    #var = "trackIsoConeTrackCount/trackPt:cluster_pt"
    #xaxis = "Cluster P_{T} (GeV)"
    #yaxis = "Iso Cone Track Count / Track P_{T}"
    #xinfo = [20, 0., 50.]
    #yinfo = [250, 0., 5.]
    #c.SetTitle("clusterPtVIsoConeTrkCntOverTrkPt")
    #drawPoints(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo, points)

    #var = "abs(trackRInv):cluster_pt"
    #xaxis = "Cluster P_{T} (GeV)"
    #yaxis = "abs( Track RInv )"
    #xinfo = [20, 0., 50.]
    #yinfo = [250, 0., 0.007]
    #c.SetTitle("clusterPtVTrackRInv")
    #drawPoints(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo, points)

#    var = "abs(trackDeltaPhi):cluster_pt"
#    xaxis = "Cluster P_{T} (GeV)"
#    yaxis = "abs( #delta#phi )"
#    xinfo = [20, 0., 50.]
#    yinfo = [500, 0., 1.]
#    c.SetTitle("clusterPtVDPhi")
#    drawPoints(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo, points, True)
#
#    var = "(-1)*((trackPt-cluster_pt)/trackPt):trackPt"
#    xaxis = "Track P_{T} (GeV)"
#    yaxis = "Pt Res"
#    xinfo = [20, 0., 50.]
#    yinfo = [500, -1., 35.]
#    c.SetTitle("trackPtVPtRes")
#    drawPoints(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo, points, True)
#
#    var = "(-1)*((trackPt-cluster_pt)/trackPt):cluster_pt"
#    xaxis = "Cluster P_{T} (GeV)"
#    yaxis = "Pt Res"
#    xinfo = [20, 0., 50.]
#    yinfo = [500, -1., 35.]
#    c.SetTitle("clusterPtVPtRes")
#    drawPoints(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo, points, True)
#
#    var = "abs(trackDeltaEta):cluster_pt"
#    xaxis = "Cluster P_{T} (GeV)"
#    yaxis = "abs( #delta#eta )"
#    xinfo = [20, 0., 50.]
#    yinfo = [500, 0., 1.]
#    c.SetTitle("clusterPtVDEta")
#    drawPoints(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo, points, True)
#
#    var = "trackDeltaR:cluster_pt"
#    xaxis = "Cluster P_{T} (GeV)"
#    yaxis = "Track #Delta R"
#    xinfo = [20, 0., 50.]
#    yinfo = [500, 0., 1.]
#    c.SetTitle("clusterPtVDR")
#    drawPoints(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo, points, True)
#
#    points = [ # pt, percentile # Used for cut11
#        [  5,    .95 ],
#        [  15,   .95 ],
#        [  25,   .95 ],
#        [  35,   .95 ],
#        [  45,   .95 ],
#        [  55,   .95 ],
#        [  65,   .95 ],
#        [  75,   .95 ],
#        [  85,   .95 ],
#        [  95,   .95 ]]
#    var = "((-1)*(bremStrength)):cluster_pt"
#    xaxis = "Cluster P_{T} (GeV)"
#    yaxis = "Brem Strength"
#    xinfo = [20, 0., 50.]
#    yinfo = [500, -1.1, 0.]
#    c.SetTitle("clusterPtVBremStr")
#    drawPoints(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo, points, True)

    #var = "trackIsoConeTrackCount:cluster_pt"
    #xaxis = "Cluster P_{T} (GeV)"
    #yaxis = "Iso Cone Trk Count"
    #xinfo = [50, 0., 50.]
    #yinfo = [60, 0., 30.]
    #c.SetTitle("clusterPtVIsoConeNumTrks")
    #drawPoints(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo, points, True)
#
#    var = "(trackPt/trackIsoConePtSum):cluster_pt"
#    xaxis = "Cluster P_{T} (GeV)"
#    yaxis = "Track Pt / Iso Cone Pt Sum"
#    xinfo = [20, 0., 50.]
#    yinfo = [50, 0., 50.]
#    c.SetTitle("clusterPtVTrackPtOverSumPt")
#    drawPoints(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo, points, True)
#
    #var = "trackPt:cluster_pt"
    #xaxis = "Cluster P_{T} (GeV)"
    #yaxis = "Track P_{T} (GeV)"
    #xinfo = [50, 0., 50.]
    #yinfo = [52, 0., 52.]
    #c.SetTitle("clusterPtVTrackPt")
    #drawPoints(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo, points, True, False)
#
#    var = "(-1)*trackPt:cluster_pt"
#    xaxis = "Cluster P_{T} (GeV)"
#    yaxis = "Track P_{T} (GeV)"
#    xinfo = [20, 0., 50.]
#    yinfo = [200, -150., 70.]
#    c.SetTitle("clusterPtVNegTrackPt")
#    drawPoints(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo, points, True)

    #points = [ # pt, percentile # Used for cut11
    #    [  5,   .9 ],
    #    [ 7.5,  .9 ],
    #    [ 10,   .9 ],
    #    [ 12.5, .9 ],
    #    [ 15,   .9 ],
    #    [ 17.5, .9 ],
    #    [ 22.5, .9 ],
    #    [ 27.5, .9 ],
    #    [ 32.5, .9 ],
    #    [ 37.5, .9 ],
    #    [ 42.5, .9 ],
    #    [ 47.5, .9 ]]
    #var = "abs(trackRInv):cluster_pt"
    #xaxis = "Cluster P_{T} (GeV)"
    #yaxis = "abs( Track RInv )"
    #xinfo = [20, 0., 50.]
    #yinfo = [250, 0., 0.007]
    #c.SetTitle("clusterPtVTrackRInvSelectBad")
    #drawPoints(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo, points)

    c.Clear()




