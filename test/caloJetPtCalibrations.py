import ROOT
from array import array
from ROOT import gStyle

ROOT.gROOT.SetBatch(True)
gStyle.SetOptStat(0)


def getTH2( tree, name, to_plot, cut, x_and_y_bins ) :
    print cut
    h1 = ROOT.TH2F(name+'_h', name+'_h', x_and_y_bins[0], x_and_y_bins[1], x_and_y_bins[2], x_and_y_bins[3], x_and_y_bins[4], x_and_y_bins[5])
    tree.Draw( to_plot + ' >> ' + name+'_h', cut )
    h1.SetDirectory(0)
    return h1


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

    c.Print(plotDir+"/"+c.GetTitle()+".png")
    c.Print(plotDir+"/"+c.GetTitle()+".C")
    c.Print(plotDir+"/"+c.GetTitle()+".pdf")

    del h1, h2, h3, g1


def drawPointsHists(h1, h2, title1, title2, xaxis, yaxis, new=False) :
    doFit = False
    c2 = ROOT.TCanvas('c2', 'c2', 1200, 600)
    c2.Divide(2)
    c2.cd(1)
    ROOT.gPad.SetRightMargin( ROOT.gPad.GetRightMargin() * 1.4 )
    h1.GetXaxis().SetTitle( xaxis )
    h1.GetYaxis().SetTitle( yaxis )
    h1.SetTitle( title1 )
    h1.Draw("colz")
    ROOT.gPad.SetGrid()
    xVals1 = array('f', [])
    yVals1 = array('f', [])

    points = []
    min_ = 20
    if c.GetTitle() == "genPtVPtResFit_s2Cor" : min_ = 5 
    for i in range(min_, 300) : points.append( i )
    for point in points :
        # if empty column, don't appent to points
        avg = getAverage( h1, point )
        if avg == -999 : continue
        xVals1.append( point )
        yVals1.append( avg )
    #print xVals1
    #print yVals1
    g1 = ROOT.TGraph(len(xVals1), xVals1, yVals1)
    g1.SetLineWidth(2)
    g1.Draw('SAME')
    if doFit :
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
    ROOT.gPad.SetRightMargin( ROOT.gPad.GetRightMargin() * 1.4 )
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
    g2.SetLineWidth(2)
    g2.Draw('SAME')
    if doFit :
        f2 = ROOT.TF1( 'f2', '([0] + [1]*TMath::Exp(-[2]*x))', mini, maxi)
        f2.SetParName( 0, "y rise" )
        f2.SetParName( 1, "scale" )
        f2.SetParName( 2, "decay" )
        f2.SetParameter( 0, .5 )
        f2.SetParameter( 1, 2.5 )
        f2.SetParameter( 2, .15 )
        fit2 = g2.Fit('f2', 'R S')

    # Just to show the resulting fit
    c2.Print(plotDir+"/"+c.GetTitle()+".png")
    c2.Print(plotDir+"/"+c.GetTitle()+".C")
    c2.Print(plotDir+"/"+c.GetTitle()+".pdf")

    if not doFit : return
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

    import os

    #base = '/data/truggles/p2/20180911_jets_v2/'
    #base2 = '/data/truggles/p2/20180913_jets/'
    base = '/data/truggles/phaseII_qcd_20180923_v1-condor_jets/'
    #jetsF0 = 'qcd_pu0.root'
    #jetsF0 = 'qcd_LOW_L1EG.root'
    #jetsF200 = 'qcd_pu200.root'
    jetsF0 = 'qcd.root'

    date = '20180923_calibCheckV1'
    plotDir = '/afs/cern.ch/user/t/truggles/www/Phase-II/'+date+''
    if not os.path.exists( plotDir ) : os.makedirs( plotDir )

    jetFile0 = ROOT.TFile( base+jetsF0, 'r' )
    #jetFile0 = ROOT.TFile( base2+jetsF0, 'r' )
    #jetFile200 = ROOT.TFile( base+jetsF200, 'r' )


    tree = jetFile0.Get("analyzer/tree")
    #tree200 = jetFile200.Get("analyzer/tree")
    c = ROOT.TCanvas('c', 'c', 800, 700)
    ''' Track to cluster reco resolution '''
    c.SetCanvasSize(1500,600)
    c.Divide(3)

    cut = "abs(genJet_eta)<1.1"
    x_and_y_bins = [90,25,300, 40,0,2]


    ### PU 0 ###
    to_plot = '(jet_pt)/genJet_pt:genJet_pt'
    h1 = getTH2( tree, 'qcd', to_plot, cut, x_and_y_bins )
    to_plot = '(stage2jet_pt)/genJet_pt:genJet_pt'
    h2 = getTH2( tree, 'stage-2', to_plot, cut, x_and_y_bins )
    xaxis = "Gen Jet P_{T} (GeV)"
    yaxis = "Relative Error in P_{T} reco/gen"
    title1 = "Phase-2 Jets"
    title2 = "Stage-2 Jets"
    c.SetTitle("genJetPt_qcd_stage-2_PU0")
    drawPointsHists(h1, h2, title1, title2, xaxis, yaxis)

    cut = "abs(genJet_eta)<1.1 && ecal_L1EG_jet_pt > 0"
    #cut = "abs(genJet_eta)<1.1"
    to_plot = '(ecal_L1EG_jet_pt)/genJet_pt:genJet_pt'
    h1 = getTH2( tree, 'qcd', to_plot, cut, x_and_y_bins )
    cut = "abs(genJet_eta)<1.1"
    to_plot = '(hcal_pt)/genJet_pt:genJet_pt'
    h2 = getTH2( tree, 'stage-2', to_plot, cut, x_and_y_bins )
    xaxis = "Gen Jet P_{T} (GeV)"
    yaxis = "Relative Error in P_{T} reco/gen"
    title1 = "ECAL Reco p_{T}"
    title2 = "HCAL Reco p_{T}"
    c.SetTitle("genJetPt_Ecal_vs_Hcal_PU0")
    drawPointsHists(h1, h2, title1, title2, xaxis, yaxis)


    ### PU 0, No ECAL Energy ###
    cut = "abs(genJet_eta)<1.1 && ecal_pt == 0"
    to_plot = '(jet_pt)/genJet_pt:genJet_pt'
    h1 = getTH2( tree, 'qcd', to_plot, cut, x_and_y_bins )
    to_plot = '(stage2jet_pt)/genJet_pt:genJet_pt'
    h2 = getTH2( tree, 'stage-2', to_plot, cut, x_and_y_bins )
    xaxis = "Gen Jet P_{T} (GeV)"
    yaxis = "Relative Error in P_{T} reco/gen"
    title1 = "Phase-2 Jets"
    title2 = "Stage-2 Jets"
    c.SetTitle("genJetPt_qcd_stage-2_PU0_EcalZero")
    drawPointsHists(h1, h2, title1, title2, xaxis, yaxis)

    cut = "abs(genJet_eta)<1.1"
    to_plot = '(ecal_L1EG_jet_pt)/genJet_pt:genJet_pt'
    h1 = getTH2( tree, 'qcd', to_plot, cut, x_and_y_bins )
    cut = "abs(genJet_eta)<1.1 && ecal_L1EG_jet_pt > 0"
    to_plot = '(ecal_L1EG_jet_pt)/genJet_pt:genJet_pt'
    h2 = getTH2( tree, 'stage-2', to_plot, cut, x_and_y_bins )
    xaxis = "Gen Jet P_{T} (GeV)"
    yaxis = "Relative Error in P_{T} reco/gen"
    title1 = "ECAL Reco p_{T} All"
    title2 = "ECAL Reco p_{T} ECAL Energy > 0"
    c.SetTitle("genJetPt_Ecal_comp_PU0")
    drawPointsHists(h1, h2, title1, title2, xaxis, yaxis)


    #### PU 200 ###
    #to_plot = '(jet_pt)/genJet_pt:genJet_pt'
    #h1 = getTH2( tree200, 'qcd', to_plot, cut, x_and_y_bins )
    #to_plot = '(stage2jet_pt)/genJet_pt:genJet_pt'
    #h2 = getTH2( tree200, 'stage-2', to_plot, cut, x_and_y_bins )
    #xaxis = "Gen Jet P_{T} (GeV)"
    #yaxis = "Relative Error in P_{T} reco/gen"
    #title1 = "Phase-2 Jets"
    #title2 = "Stage-2 Jets"
    #c.SetTitle("genJetPt_qcd_stage-2_PU200")
    #drawPointsHists(h1, h2, title1, title2, xaxis, yaxis)

    #cut = "abs(genJet_eta)<1.1 && ecal_pt > 0"
    ##cut = "abs(genJet_eta)<1.1"
    #to_plot = '(ecal_pt)/genJet_pt:genJet_pt'
    #h1 = getTH2( tree200, 'qcd', to_plot, cut, x_and_y_bins )
    #cut = "abs(genJet_eta)<1.1"
    #to_plot = '(hcal_pt)/genJet_pt:genJet_pt'
    #h2 = getTH2( tree200, 'stage-2', to_plot, cut, x_and_y_bins )
    #xaxis = "Gen Jet P_{T} (GeV)"
    #yaxis = "Relative Error in P_{T} reco/gen"
    #title1 = "ECAL Reco p_{T}"
    #title2 = "HCAL Reco p_{T}"
    #c.SetTitle("genJetPt_Ecal_vs_Hcal_PU200")
    #drawPointsHists(h1, h2, title1, title2, xaxis, yaxis)





