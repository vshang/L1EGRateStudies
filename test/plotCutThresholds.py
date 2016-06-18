import ROOT
from array import array

def drawPoints(c, tree1, var, cut, title1, tree2, title2, xaxis, xinfo, yaxis, yinfo, points, linear=False) :
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
    g1.Draw('SAME')
    mini = points[0][0]
    maxi = points[-1][0]
    if not linear :
        f1 = ROOT.TF1( 'f1', '([0] + [1]*TMath::Exp(-[2]*x))', mini, maxi)
        f1.SetParName( 0, "y rise" )
        f1.SetParName( 1, "scale" )
        f1.SetParName( 2, "decay" )
        f1.SetParameter( 0, .5 )
        f1.SetParameter( 1, 2.5 )
        f1.SetParameter( 2, .15 )
        rslt = g1.Fit('f1')
    if linear :
        f1 = ROOT.TF1( 'f1', '([0] + [1]*x)', mini, maxi)
        f1.SetParName( 0, "y intercept" )
        f1.SetParName( 1, "slope" )
        f1.SetParameter( 0, .0 )
        f1.SetParameter( 1, 1. )
        rslt = g1.Fit('f1')
    
    c.cd(2)
    h2 = ROOT.TH2F("h2", title2, xinfo[0], xinfo[1], xinfo[2], yinfo[0], yinfo[1], yinfo[2])
    tree2.Draw( var + " >> h2", cut )
    h2.GetXaxis().SetTitle( xaxis )
    h2.GetYaxis().SetTitle( yaxis )
    h2.Draw("colz")
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
        [  5,   .85 ],
        [ 7.5,  .85 ],
        [ 10,   .875 ],
        [ 12.5, .90 ],
        [ 15,   .925 ],
        [ 17.5, .95 ],
        [ 22.5, .97 ],
        [ 27.5, .98 ],
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

    var = "cluster_pt:trackDeltaEta"
    title1 = "L1EGamma Crystal (Electrons)"
    title2 = "L1EGamma Crystal (Fake)"
    var = "cluster_hovere:cluster_pt"
    xaxis = "Cluster P_{T} (GeV)"
    yaxis = "Cluster H/E"
    xinfo = [20, 0., 50.]
    yinfo = [250, 0., 15.]
    c.SetTitle("clusterPtVHoverE")
    drawPoints(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo, points)

    var = "cluster_iso:cluster_pt"
    xaxis = "Cluster P_{T} (GeV)"
    yaxis = "Cluster Iso (GeV)"
    xinfo = [20, 0., 50.]
    yinfo = [250, 0., 10.]
    c.SetTitle("clusterPtVClusterIso")
    drawPoints(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo, points)

    var = "(-1)*(e2x5/e5x5):cluster_pt"
    xaxis = "Cluster P_{T} (GeV)"
    yaxis = "Energy 2x5/5x5"
    xinfo = [20, 0., 50.]
    yinfo = [250, 0., -1.]
    c.SetTitle("clusterPtVE2x5OverE5x5")
    drawPoints(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo, points)

#    points = [ # pt, percentile
#        [  5,   .95],
#        [ 10,   .95],
#        [ 15,   .95],
#        [ 22.5, .95],
#        [ 27.5, .98],
#        [ 32.5, .98],
#        [ 37.5, .98 ],
#        [ 42.5, .98 ],
#        [ 47.5, .98 ]]
#
#    var = "abs(trackDeltaPhi):cluster_pt"
#    xaxis = "Cluster P_{T} (GeV)"
#    yaxis = "abs( #delta#phi )"
#    xinfo = [20, 0., 50.]
#    yinfo = [500, 0., 1.]
#    c.SetTitle("clusterPtVDPhi")
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
#    var = "((-1)*(bremStrength)):cluster_pt"
#    xaxis = "Cluster P_{T} (GeV)"
#    yaxis = "Brem Strength"
#    xinfo = [20, 0., 50.]
#    yinfo = [500, -1.1, 0.]
#    c.SetTitle("clusterPtVBremStr")
#    drawPoints(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo, points, True)
#
#    var = "trackIsoConeTrackCount:cluster_pt"
#    xaxis = "Cluster P_{T} (GeV)"
#    yaxis = "Iso Cone Trk Count"
#    xinfo = [20, 0., 50.]
#    yinfo = [30, 0., 30.]
#    c.SetTitle("clusterPtVIsoConeNumTrks")
#    drawPoints(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo, points, True)
#
#    var = "(trackPt/trackIsoConePtSum):cluster_pt"
#    xaxis = "Cluster P_{T} (GeV)"
#    yaxis = "Track Pt / Iso Cone Pt Sum"
#    xinfo = [20, 0., 50.]
#    yinfo = [50, 0., 50.]
#    c.SetTitle("clusterPtVTrackPtOverSumPt")
#    drawPoints(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo, points, True)
#
#    cut = ""
#    points = [ # pt, percentile
#        [  5,   .97],
#        [ 10,   .97],
#        [ 15,   .97],
#        [ 22.5, .98],
#        [ 27.5, .99],
#        [ 32.5, .99],
#        [ 37.5, .995 ],
#        [ 42.5, .995 ],
#        [ 47.5, .995 ]]
#    var = "trackPt:cluster_pt"
#    xaxis = "Cluster P_{T} (GeV)"
#    yaxis = "Track P_{T} (GeV)"
#    xinfo = [20, 0., 50.]
#    yinfo = [100, 0., 100.]
#    c.SetTitle("clusterPtVTrackPt")
#    drawPoints(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo, points, True)
#
#    points = [ # pt, percentile
#        #[  5,   .95],
#        #[ 10,   .95],
#        #[ 15,   .95],
#        #[ 22.5, .95],
#        [ 27.5, .95],
#        [ 32.5, .95],
#        [ 37.5, .95 ],
#        [ 42.5, .95 ],
#        [ 47.5, .95 ]]
#    var = "(-1)*trackPt:cluster_pt"
#    xaxis = "Cluster P_{T} (GeV)"
#    yaxis = "Track P_{T} (GeV)"
#    xinfo = [20, 0., 50.]
#    yinfo = [200, -150., 70.]
#    c.SetTitle("clusterPtVNegTrackPt")
#    drawPoints(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo, points, True)
#
#
#    c.Clear()
#
#
#
#
