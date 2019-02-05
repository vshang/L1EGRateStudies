import ROOT
from array import array
from ROOT import gStyle

ROOT.gROOT.SetBatch(True)
gStyle.SetOptStat(0)


def getTH2( tree, name, to_plot, cut, x_and_y_bins ) :
    #print cut
    h1 = ROOT.TH2F(name+'_h', name+'_h', x_and_y_bins[0], x_and_y_bins[1], x_and_y_bins[2], x_and_y_bins[3], x_and_y_bins[4], x_and_y_bins[5])
    tree.Draw( to_plot + ' >> ' + name+'_h', cut )
    h1.SetDirectory(0)
    return h1


def getTH2VarBin( tree, name, to_plot, cut, x_and_y_bins ) :
    #print cut
    h1 = ROOT.TH2F(name+'_h', name+'_h', len(x_and_y_bins[0])-1, x_and_y_bins[0], len(x_and_y_bins[1])-1, x_and_y_bins[1])
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


def drawPointsHists3(saveName, h1, h2, h3, title1, title2, title3, xaxis, yaxis, areaNorm=False, plotDir='.') :
    doFit = False
    c2 = ROOT.TCanvas('c2', 'c2', 1600, 600)
    c2.Divide(3)
    c2.cd(1)
    ROOT.gPad.SetRightMargin( ROOT.gPad.GetRightMargin() * 1.4 )
    h1.GetXaxis().SetTitle( xaxis )
    h1.GetYaxis().SetTitle( yaxis )
    h1.SetTitle( title1 )
    if areaNorm :
        h1.Scale( 1. / h1.Integral() )
        max_ = h1.GetMaximum() * 1.3
        h1.SetMaximum( max_ )
    h1.Draw("colz")
    ROOT.gPad.SetGrid()
    xVals1 = array('f', [])
    yVals1 = array('f', [])

    points = []
    min_ = 10
    #for i in range(min_, 300) : points.append( i )
    for i in range(min_, 400) : points.append( i )
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
    if areaNorm :
        h2.Scale( 1. / h2.Integral() )
        h2.SetMaximum( max_ )
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

    
    c2.cd(3)
    ROOT.gPad.SetRightMargin( ROOT.gPad.GetRightMargin() * 1.4 )
    h3.SetTitle( title3 )
    if areaNorm :
        h3.Scale( 1. / h3.Integral() )
        h3.SetMaximum( max_ )
    h3.Draw("colz")
    ROOT.gPad.SetGrid()
    h3.GetXaxis().SetTitle( xaxis )
    h3.GetYaxis().SetTitle( yaxis )
    xVals3 = array('f', [])
    yVals3 = array('f', [])
    for point in points :
        xVals3.append( point )
        yVals3.append( getAverage( h3, point ) )
    #print xVals3
    #print yVals3
    g3 = ROOT.TGraph(len(xVals3), xVals3, yVals3)
    g3.SetLineWidth(2)
    g3.Draw('SAME')
    if doFit :
        f3 = ROOT.TF1( 'f3', '([0] + [1]*TMath::Exp(-[2]*x))', mini, maxi)
        f3.SetParName( 0, "y rise" )
        f3.SetParName( 1, "scale" )
        f3.SetParName( 2, "decay" )
        f3.SetParameter( 0, .5 )
        f3.SetParameter( 1, 2.5 )
        f3.SetParameter( 2, .15 )
        fit3 = g3.Fit('f3', 'R S')

    # Just to show the resulting fit
    c2.Print(plotDir+"/"+saveName+".png")
    #c2.Print(plotDir+"/"+saveName+".C")
    c2.Print(plotDir+"/"+saveName+".pdf")



def drawPointsSingleHist(saveName, h1, title1, xaxis, yaxis, plotDir='.') :
    c2 = ROOT.TCanvas('c2', 'c2', 600, 600)
    ROOT.gPad.SetRightMargin( ROOT.gPad.GetRightMargin() * 1.4 )
    h1.GetXaxis().SetTitle( xaxis )
    h1.GetYaxis().SetTitle( yaxis )
    h1.SetTitle( title1 )
    h1.Draw("colz")
    ROOT.gPad.SetGrid()
    xVals1 = array('f', [])
    yVals1 = array('f', [])

    points = []
    min_ = 5
    # was originally using 10 GeV spacing for calibrations here
    # Switch to using the same binning as the TH2
    for i in range(min_, 505, 10) : points.append( i )
    #points = get_x_binning()
    for i in range(len(points)-1) :
        # if empty column, don't appent to points
        point = (points[i]+points[i+1])/2.
        avg = getAverage( h1, point )
        if avg == -999 : continue
        #print i, points[i], points[i+1], point, avg
        xVals1.append( point )
        yVals1.append( avg )
    #print xVals1
    #print yVals1
    g1 = ROOT.TGraph(len(xVals1), xVals1, yVals1)
    g1.SetLineWidth(2)
    g1.GetXaxis().SetTitle( xaxis )
    g1.GetYaxis().SetTitle( yaxis )
    #g1.SaveAs('stage-2_calib_%s.root' % saveName)
    g1.Draw('SAME')

    # Just to show the resulting fit
    c2.Print(plotDir+"/"+saveName+".png")
    #c2.Print(plotDir+"/"+saveName+".C")
    #c2.Print(plotDir+"/"+saveName+".pdf")

    return g1






def drawPointsHists(saveName, h1, h2, title1, title2, xaxis, yaxis, new=False, plotDir='.') :
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
    min_ = 5
    # was originally using 10 GeV spacing for calibrations here
    # Switch to using the same binning as the TH2
    #for i in range(min_, 505, 10) : points.append( i )
    points = get_x_binning()
    for i in range(len(points)-1) :
        # if empty column, don't appent to points
        point = (points[i]+points[i+1])/2.
        avg = getAverage( h1, point )
        if avg == -999 : continue
        #print i, points[i], points[i+1], point, avg
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
    #for point in points :
    for i in range(len(points)-1) :
        # if empty column, don't appent to points
        point = (points[i]+points[i+1])/2.
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
    c2.Print(plotDir+"/"+saveName+".png")
    #c2.Print(plotDir+"/"+saveName+".C")
    #c2.Print(plotDir+"/"+saveName+".pdf")

    if not doFit :
        return g2
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
        return 1.0
    avgTot = weightedTot/tot
    
    #print "Final average total: ",avgTot
    
    answer = h.GetYaxis().FindBin( avgTot )
    #print "Associated bin: ",answer
    return avgTot


# create a list with the output delinimations splitting the calo jets
# into nBins based on EM fraction
def get_quantile_em_fraction_list( fName, nBins=10 ) :
    f = ROOT.TFile( fName, 'r')
    t = f.Get('analyzer/tree')
    
    h = ROOT.TH1D('h','h',10000,0,1.1)
    t.Draw( '(ecal_L1EG_jet_pt + ecal_pt)/jet_pt >> h', 'jet_pt >= 0')

    # To keep track of total so we can compute relative fractions
    total = h.Integral()
    
    c = ROOT.TCanvas('cx','cx',600,400)
    h.Draw()
    #ROOT.gPad.SetLogy()
    #c.SaveAs('quant.png')

    rtn_list = []    
    cum = 0
    index = 1
    for b in range( h.GetXaxis().GetNbins() ) :
        cum += h.GetBinContent( b )
        #if b > 20 : break
        if cum * 10 > total :
            to_append = round(h.GetBinCenter(b), 3)
            if len(rtn_list) == 0 and to_append != 0.0 :
                # Store first bin but don't add two 0.0 if to_append == 0.0
                rtn_list.append( 0.0 )
            rtn_list.append( to_append )
            print index, b, h.GetBinCenter(b), cum
            cum = 0
            index += 1
    # Store final bin
    rtn_list.append( 1.0 )

    del c, h

    return rtn_list
        
def get_x_binning() :
    #xBinning = array('f', [0.,15,17.5,20,22.5,25,27.5,30, \
    # Worked xBinning = array('f', [0.,20,22.5,25,27.5,30, \
    xBinning = array('f', [0.,5.,7.5,10.,12.5,15.,17.5,20,22.5,25,27.5,30, \
        35,40,45,50,55,60,65,70,75,80,85,90,95,100,110,120,130,140,150,160,170,180,190,200,225,250,275,300, \
        325,400,500]) # x binning
    #xBinningAlt = array('f', [0.,30, \
    #    35,40,45,50,55,60,65,70,75,80,85,90,95,100,110,120,130,140,150,160,170,180,190,200,225,250,275,300, \
    #    325,400,500]) # x binning
    return xBinning


def make_em_fraction_calibrations( c, fName, cut, plotBase ) :

    ### Shifting EM fraction plots ###
    nBins = 10
    quantile_list = get_quantile_em_fraction_list( fName, nBins )
    print "Quantile List", quantile_list

    # Get same file again
    jetFile = ROOT.TFile( fName, 'r' )
    tree = jetFile.Get("analyzer/tree")

    f_out = ROOT.TFile('jet_em_calibrations.root','RECREATE')
    #x_and_y_bins = [100,0,500, 200,0,20]
    xBinning = get_x_binning()
    yBinning = array('f', [i*0.1 for i in range(201)])
    for i in range(len(quantile_list)-1) :
        for eta in [['0.0', '0.3'], ['0.3', '0.7'], ['0.7', '1.0'], ['1.0', '1.2'], ['1.2', '2.0']] :
            f_low = quantile_list[i]
            f_high = quantile_list[i+1]
            x_and_y_bins = [ xBinning, yBinning ]
            #if f_low > 0.0 and f_low < 0.1 and f_high > 0.0 and f_high < 0.1 :
            #    x_and_y_bins = [ xBinningAlt, yBinning ]
            frac_cut = cut+" && abs(jet_eta)>=%s && abs(jet_eta)<=%s && (((ecal_L1EG_jet_pt + ecal_pt)/jet_pt) >= %f && ((ecal_L1EG_jet_pt + ecal_pt)/jet_pt) < %f)" % (eta[0], eta[1], f_low, f_high)
            print frac_cut
            to_plot = '(hcal_pt)/genJet_pt:jet_pt'
            #h1 = getTH2( tree, 'qcd1', to_plot, frac_cut, x_and_y_bins )
            h1 = getTH2VarBin( tree, 'qcd1', to_plot, frac_cut, x_and_y_bins )
            to_plot = '(genJet_pt - (ecal_L1EG_jet_pt + ecal_pt))/(hcal_pt):jet_pt'
            #h2 = getTH2( tree, 'qcd3', to_plot, frac_cut, x_and_y_bins )
            h2 = getTH2VarBin( tree, 'qcd3', to_plot, frac_cut, x_and_y_bins )
            xaxis = "Jet P_{T} (GeV)"
            #yaxis = "Relative Error in P_{T} reco/gen"
            yaxis = "Gen Jet pT - (ECAL+L1EG) / [ HCAL ]"
            title1 = "L1CaloJets HCAL1 - EM %.2f to %.2f" % (f_low, f_high)
            #title2 = "L1CaloJets HCAL2 - EM %.2f to %.2f" % (f_low, f_high)
            title2 = "HCAL Calibration vs. Reco Jet P_{T}"
            c.SetTitle("jetPt_qcd_HCALfocus_EM_frac_%s_to_%s_absEta%s_to_%s_PU0" % (str(f_low).replace('.','p'), str(f_high).replace('.','p'), eta[0].replace('.','p'), eta[1].replace('.','p')))
            g = drawPointsHists(c.GetTitle(), h1, h2, title1, title2, xaxis, yaxis, False, plotBase)
            g.SetTitle('%i_EM_frac_%s_to_%s_absEta_%s_to_%s' % (i, str(f_low).replace('.','p'), str(f_high).replace('.','p'), eta[0].replace('.','p'), eta[1].replace('.','p') ) )
            g.SetName('%i_EM_frac_%s_to_%s_absEta_%s_to_%s' % (i, str(f_low).replace('.','p'), str(f_high).replace('.','p'), eta[0].replace('.','p'), eta[1].replace('.','p') ) )
            print g
            g.Write()
            #x = ROOT.Double(0.)
            #y = ROOT.Double(0.)
            #for p in range( g.GetN() ) :
            #    g.GetPoint(p, x, y)
            #    print p, x, y
    f_out.Close()


if __name__ == '__main__' :

    import os

    base2 = '/data/truggles/l1CaloJets_20190128v2/'
    base3 = '/data/truggles/l1CaloJets_20190128v3/'
    jetsF200 = 'ttbar_PU200.root'
    jetsF0 = 'ttbar_PU0.root'

    date = '20190128_v2_v_v3'
    plotDir = '/afs/cern.ch/user/t/truggles/www/Phase-II/'+date+'v2'
    if not os.path.exists( plotDir ) : os.makedirs( plotDir )
    plotBase = plotDir

    jetFile0v2 = ROOT.TFile( base2+jetsF0, 'r' )
    jetFile200v2 = ROOT.TFile( base2+jetsF200, 'r' )
    jetFile0v3 = ROOT.TFile( base3+jetsF0, 'r' )
    jetFile200v3 = ROOT.TFile( base3+jetsF200, 'r' )


    tree2 = jetFile0v2.Get("analyzer/tree")
    tree2002 = jetFile200v2.Get("analyzer/tree")
    tree3 = jetFile0v3.Get("analyzer/tree")
    tree2003 = jetFile200v3.Get("analyzer/tree")
    c = ROOT.TCanvas('c', 'c', 800, 700)
    ''' Track to cluster reco resolution '''
    c.SetCanvasSize(1500,600)
    c.Divide(3)

    #cut = "abs(genJet_eta)<1.1"
    cut = "abs(genJet_eta)<5"
    x_and_y_bins = [30,0,300, 60,0,3]
    x_and_y_bins = [30,0,300, 120,0,6]

    make_calibrations = False
    ### Between these two you need to run add_calibrations.py to add 'calib' to TTree
    plot_calibrated_results = False

    """ Make new calibration root file """
    if make_calibrations :
        make_em_fraction_calibrations( c, base+jetsF0, cut, plotDir )

    eta_ranges = {
    'all' : '(abs(genJet_eta)<10)',
    'golden' : '(abs(genJet_eta)<1.2)',
    'barrel' : '(abs(genJet_eta)<1.5)',
    'barrel_transition' : '(abs(genJet_eta)<1.8 && abs(genJet_eta)>1.2)',
    'hgcal' : '(abs(genJet_eta)<3 && abs(genJet_eta)>1.5)',
    'hf' : '(abs(genJet_eta)>3)',
    }
    for k, cut in eta_ranges.iteritems() :
        to_plot = '(jet_pt)/genJet_pt:genJet_pt'
        h1 = getTH2( tree3, 'ttbar', to_plot, cut, x_and_y_bins )
        h2 = getTH2( tree2, 'ttbar', to_plot, cut, x_and_y_bins )
        xaxis = "Gen Jet P_{T} (GeV)"
        yaxis = "Relative Error in P_{T} reco/gen"
        title1 = "ttbar PU Uncorrected"
        title2 = "ttbar PU Corrected"
        c.SetTitle("genJetPt_ttbar_PU0_"+k)
        drawPointsHists(c.GetTitle(), h1, h2, title1, title2, xaxis, yaxis, False, plotDir)

        h1 = getTH2( tree2003, 'ttbar', to_plot, cut, x_and_y_bins )
        h2 = getTH2( tree2002, 'ttbar', to_plot, cut, x_and_y_bins )
        xaxis = "Gen Jet P_{T} (GeV)"
        yaxis = "Relative Error in P_{T} reco/gen"
        title1 = "ttbar PU Uncorrected"
        title2 = "ttbar PU Corrected"
        c.SetTitle("genJetPt_ttbar_PU200_"+k)
        drawPointsHists(c.GetTitle(), h1, h2, title1, title2, xaxis, yaxis, False, plotDir)

    #to_plot = '(ecal_L1EG_jet_pt + ecal_pt)/genJet_pt:genJet_pt'
    #h1 = getTH2( tree, 'qcd', to_plot, cut, x_and_y_bins )
    #to_plot = '(hcal_pt)/genJet_pt:genJet_pt'
    #h2 = getTH2( tree, 'stage-2', to_plot, cut, x_and_y_bins )
    #xaxis = "Gen Jet P_{T} (GeV)"
    #yaxis = "Relative Error in P_{T} reco/gen"
    #title1 = "ECAL Total Reco p_{T}"
    #title2 = "HCAL Reco p_{T}"
    #c.SetTitle("genJetPt_Ecal_vs_Hcal_PU0")
    #drawPointsHists(c.GetTitle(), h1, h2, title1, title2, xaxis, yaxis)

    #to_plot = '(ecal_L1EG_jet_pt)/genJet_pt:genJet_pt'
    #h1 = getTH2( tree, 'qcd', to_plot, cut, x_and_y_bins )
    #to_plot = '(ecal_pt)/genJet_pt:genJet_pt'
    #h2 = getTH2( tree, 'stage-2', to_plot, cut, x_and_y_bins )
    #xaxis = "Gen Jet P_{T} (GeV)"
    #yaxis = "Relative Error in P_{T} reco/gen"
    #title1 = "ECAL L1EG Reco p_{T}"
    #title2 = "ECAL Uncl. Reco p_{T}"
    #c.SetTitle("genJetPt_Ecal_PU0")
    #drawPointsHists(c.GetTitle(), h1, h2, title1, title2, xaxis, yaxis)

    #to_plot = '(jet_pt)/genJet_pt:genJet_pt'
    #h1 = getTH2( tree, 'qcd1', to_plot, cut, x_and_y_bins )
    #to_plot = '(ecal_L1EG_jet_pt + ecal_pt + hcal_pt )/genJet_pt:genJet_pt'
    #h2 = getTH2( tree, 'qcd2', to_plot, cut, x_and_y_bins )
    #to_plot = '(ecal_L1EG_jet_pt + ecal_pt + (hcal_pt*calib) )/genJet_pt:genJet_pt'
    #h3 = getTH2( tree, 'qcd3', to_plot, cut, x_and_y_bins )
    #xaxis = "Gen Jet P_{T} (GeV)"
    #yaxis = "Relative Error in P_{T} reco/gen"
    #title1 = "Jet Reco p_{T}"
    #title2 = "ECAL+HCAL+L1EG Reco p_{T}"
    #title3 = "ECAL+(HCAL*calib)+L1EG Reco p_{T}"
    #c.SetTitle("genJetPt_Subdivided_PU0")
    #drawPointsHists3(c.GetTitle(), h1, h2, h3, title1, title2, title3, xaxis, yaxis, plotDir)

    x_and_y_bins = [28,20,300, 60,0,3]
    """ Resulting Calibrations """
    if plot_calibrated_results :
        to_plot = '(jet_pt)/genJet_pt:genJet_pt'
        h1 = getTH2( tree, 'qcd1', to_plot, cut, x_and_y_bins )
        to_plot = '(ecal_L1EG_jet_pt + ecal_pt + (hcal_pt*calib) )/genJet_pt:genJet_pt'
        h2 = getTH2( tree, 'qcd2', to_plot, cut, x_and_y_bins )
        to_plot = '(stage2jet_pt)/genJet_pt:genJet_pt'
        h3 = getTH2( tree, 's2', to_plot, cut, x_and_y_bins )
        xaxis = "Gen Jet P_{T} (GeV)"
        yaxis = "Relative Error in P_{T} reco/gen"
        title1 = "Phase-II before HCAL calibrations"
        title2 = "Phase-II with HCAL calibrations"
        title3 = "Phase-I with calibrations"
        c.SetTitle("genJetPt_Calibrated_vs_Stage-2_PU0")
        areaNorm = True
        drawPointsHists3(c.GetTitle(), h1, h2, h3, title1, title2, title3, xaxis, yaxis, areaNorm, plotDir)



    #### PU 0, No ECAL Energy ###
    #cut = "abs(genJet_eta)<1.1 && ecal_pt == 0"
    #to_plot = '(jet_pt)/genJet_pt:genJet_pt'
    #h1 = getTH2( tree, 'qcd', to_plot, cut, x_and_y_bins )
    #to_plot = '(stage2jet_pt)/genJet_pt:genJet_pt'
    #h2 = getTH2( tree, 'stage-2', to_plot, cut, x_and_y_bins )
    #xaxis = "Gen Jet P_{T} (GeV)"
    #yaxis = "Relative Error in P_{T} reco/gen"
    #title1 = "Phase-2 Jets"
    #title2 = "Stage-2 Jets"
    #c.SetTitle("genJetPt_qcd_stage-2_PU0_EcalZero")
    #drawPointsHists(c.GetTitle(), h1, h2, title1, title2, xaxis, yaxis)

    #cut = "abs(genJet_eta)<1.1"
    #to_plot = '(ecal_L1EG_jet_pt)/genJet_pt:genJet_pt'
    #h1 = getTH2( tree, 'qcd', to_plot, cut, x_and_y_bins )
    #cut = "abs(genJet_eta)<1.1 && ecal_L1EG_jet_pt > 0"
    #to_plot = '(ecal_L1EG_jet_pt)/genJet_pt:genJet_pt'
    #h2 = getTH2( tree, 'stage-2', to_plot, cut, x_and_y_bins )
    #xaxis = "Gen Jet P_{T} (GeV)"
    #yaxis = "Relative Error in P_{T} reco/gen"
    #title1 = "ECAL Reco p_{T} All"
    #title2 = "ECAL Reco p_{T} ECAL Energy > 0"
    #c.SetTitle("genJetPt_Ecal_comp_PU0")
    #drawPointsHists(c.GetTitle(), h1, h2, title1, title2, xaxis, yaxis)


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
    #drawPointsHists(c.GetTitle(), h1, h2, title1, title2, xaxis, yaxis)

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
    #drawPointsHists(c.GetTitle(), h1, h2, title1, title2, xaxis, yaxis)





