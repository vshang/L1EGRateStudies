import ROOT
from array import array
from ROOT import gStyle

ROOT.gROOT.SetBatch(True)
gStyle.SetOptStat(0)

def drawPoints(c, tree1, var, cut, tree2, tree3, xaxis, xinfo, yaxis, yinfo, points, linear=False, doFit=True, includeLine=False, invert=False) :
    doLog = False
    doLog = True
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
    if doLog :
        ROOT.gPad.SetLogz()
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
            #f3 = ROOT.TF1( 'f3', '([0] + [1]*x)', 80, 100 )
            ##f3.SetParameter( 0, 0.1471537 ) # 85 GeV swap
            #f3.SetParameter( 0, 0.1962996 ) # 80 GeV swap
            #f3.SetParameter( 1, 0.0 )
            #f3.SetLineWidth( 4 )
            #f3.Draw('SAME')
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
    if doLog :
        ROOT.gPad.SetLogz()
    if includeLine : 
        g1.Draw('SAME')
    if doFit :
        f2.Draw('SAME')
        #if "clusterPtVClusterIso" == c.GetTitle() :
        #    f3.Draw('SAME')
    c.cd(3)
    h3 = ROOT.TH2F("h3", title3, xinfo[0], xinfo[1], xinfo[2], yinfo[0], yinfo[1], yinfo[2])
    tree3.Draw( var + " >> h3", cut )
    h3.GetXaxis().SetTitle( xaxis )
    h3.GetYaxis().SetTitle( yaxis )
    h3.Draw("colz")
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

    # plot local
    #plotDir = 'plotCuts'
    # plot web
    plotDir = '/afs/cern.ch/user/t/truggles/www/Phase-II/'+date
    c.Print(plotDir+"/"+c.GetTitle()+".png")
    c.Print(plotDir+"/"+c.GetTitle()+".C")
    c.Print(plotDir+"/"+c.GetTitle()+".pdf")

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
    c2.Print(plotDir+"/"+c.GetTitle()+".C")
    c2.Print(plotDir+"/"+c.GetTitle()+".pdf")

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
    cx.Print(plotDir+"/"+c.GetTitle()+"_fits.C")
    cx.Print(plotDir+"/"+c.GetTitle()+"_fits.pdf")

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

    singleE = 'singleE_july20v2.root'

    date = '20180720_calibCheckV2'

    effFile = ROOT.TFile( singleE, 'r' )

    crystal_tree = effFile.Get("analyzer/crystal_tree")
    c = ROOT.TCanvas('c', 'c', 800, 700)
    ''' Track to cluster reco resolution '''
    c.SetCanvasSize(1500,600)
    c.Divide(3)

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

    l1Crystal2DPtResHist4 = effFile.Get("analyzer/reco_gen_pt4")
    stage22DPtResHist3 = effFile.Get("analyzer/stage2_reco_gen_pt3")
    xaxis = "Reco P_{T} (GeV)"
    yaxis = "Relative Error in P_{T} gen/reco"
    title1 = "L1EG Crystal Algo"
    title2 = "Stage-2"
    c.SetTitle("genPtVPtResFit4")
    drawPointsHists(l1Crystal2DPtResHist4, stage22DPtResHist3, title1, title2, xaxis, yaxis, True)

    #l1Crystal2DPtAdjResHist = effFile.Get("analyzer/reco_gen_pt_adj")
    #yaxis = "Relative Error in P_{T} (reco-gen)/gen"
    #c.SetTitle("genPtVPtAdjResFit")
    #drawPointsHists(l1Crystal2DPtAdjResHist, stage22DPtResHist2, title1, title2, xaxis, yaxis)

    #l1Crystal2DPtAdjResHist = effFile.Get("analyzer/reco_gen_pt_adj3")
    #yaxis = "Relative Error in P_{T} gen/reco"
    #c.SetTitle("genPtVPtAdjResFit3")
    #drawPointsHists(l1Crystal2DPtAdjResHist, stage22DPtResHist3, title1, title2, xaxis, yaxis, True)

