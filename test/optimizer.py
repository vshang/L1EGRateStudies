import ROOT
from ROOT import gStyle, gPad
import math
from drawRateEff import setLegStyle, drawCMSString
import CMS_lumi, tdrstyle
from trigHelpers import makeNewCutTrees
from array import array
gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch(True)

canvasSize = 800

date = 'v2'
newEffFileName = 'r2_phase2_singleElectron_%s.root' % (date)
newPhotonFileName = 'r2_phase2_singlePhoton_%s.root' % (date)
newRateFileName = 'r2_phase2_minBias_%s.root' % (date)

rateFile = ROOT.TFile( newRateFileName, 'r' )
effFile = ROOT.TFile( newEffFileName, 'r' )

#effFile = ROOT.TFile( 'egTriggerEff.root', 'r' )
#rateFile = ROOT.TFile( 'egTriggerRates.root', 'r' )
eTree = effFile.Get("analyzer/crystal_tree")
rTree = rateFile.Get("analyzer/crystal_tree")

def addText( xPos, yPos, cName ) :
    cutName = ROOT.TText(xPos, yPos, cName)
    cutName.SetTextSize(0.03)
    cutName.DrawTextNDC(xPos, yPos, cName )

def tryCut( etree, rtree, var, cut, preCut="", verbose=True ) :
    if verbose :
        print "\nVar:",var
        print "Cut: ",cut
        print "PreCut: ",preCut
    returnMap = {}
    for val in [0,10,20,30,40] :
        h1 = ROOT.TH1F('h1','h1',100,val,val+10)
        etree.Draw( var + ' >> h1', cut )
        eVal = h1.Integral()
        h1_2 = ROOT.TH1F('h1_2','h1_2',100,val,val+10)
        etree.Draw( var + ' >> h1_2', preCut )
        eVal2 = h1_2.Integral()
        h2 = ROOT.TH1F('h2','h2',100,val,val+10)
        rtree.Draw( var + ' >> h2', cut )
        rVal = h2.Integral()
        h2_2 = ROOT.TH1F('h2_2','h2_2',100,val,val+10)
        rtree.Draw( var + ' >> h2_2', preCut )
        rVal2 = h2_2.Integral()
        if verbose :
            print " - Range: %i - %i" % (val, val+10)
            print " - Cuts out: %8i / %8i = %8f" % ((eVal2-eVal),eVal2,((eVal2-eVal)/eVal2))
            print " - Cuts out: %8i / %8i = %8f" % ((rVal2-rVal),rVal2,((rVal2-rVal)/rVal2))
        binMap = {
            "sigI" : eVal2,
            "sigF" : eVal,
            "bkgI" : rVal2,
            "bkgF" : rVal,
        }
        returnMap[ val ] = binMap
        
        del h1,h1_2,h2,h2_2
    return returnMap


def makeRatePlot( rateFile, tree, name, cut='', rateLimit=50, var='cluster_pt' ) :
    c = ROOT.TCanvas('c','c',canvasSize,canvasSize)
    
    h1 = ROOT.TH1F('h1', name,int(rateLimit*.8),0,rateLimit)
    tree.Draw( var+' >> h1', cut)
    h2 = ROOT.TH1F('h2'+name, name,int(rateLimit*.8),0,rateLimit)
    h2.Sumw2()
    
    for i in range(1, h1.GetNbinsX()+1) :
        h2.SetBinContent( i, h1.Integral( i, rateLimit ) )
        #FIXME h2.SetBinError( i, math.sqrt(h2.GetBinContent( i )) )
    
    # Normalize to 30 MHz
    nEvents = rateFile.Get("analyzer/eventCount").GetBinContent(1)
    print "n events scanned %i,   events in tree %i" % (nEvents, tree.GetEntries())
    factor = 30000. / nEvents
    print "factor",factor
    #factor = 30000. / tree.GetEntries()
    h2.Scale( factor )
    print name,"Bin cont bin 1",h2.GetBinContent(1)
    h2.SetMarkerSize(0)
    h2.SetLineWidth(2)
    
    h2.Draw()
    h2.GetYaxis().SetTitle('Rate (kHz)')
    h2.GetXaxis().SetTitle('L1 EG E_{T}')
    c.SetLogy()
    del h1
    del c
    return h2

def plotRateHists( name, hists=[] ) :
    #colors = [ROOT.kBlack, ROOT.kRed, ROOT.kBlue, ROOT.kGreen, ROOT.kOrange+7, ROOT.kMagenta, ROOT.kCyan, ROOT.kYellow+1, ROOT.kGreen-2]
    colors = [1, 2, 3, 4, ROOT.kYellow+1, 6, 7, 8, 46]
    c = ROOT.TCanvas('c','c',canvasSize,canvasSize)
    c.SetLogy()
    c.SetGrid()
    if len(hists) > 5 : yStart = 0.60
    else : yStart = 0.78
    #leg = setLegStyle(0.53,yStart,0.95,0.92)
    leg = setLegStyle(0.4,.65,0.95,0.92)
    leg.SetFillStyle(1001)
    leg.SetFillColor(ROOT.kWhite)

    max_ = 0.
    min_ = 1000.
    for i, h in enumerate(hists) :
        if h.GetBinContent(1) > max_ : max_ = h.GetBinContent(1)
        if h.GetBinContent( h.GetXaxis().GetNbins() ) < min_ : min_ = h.GetBinContent( h.GetXaxis().GetNbins() )
        h.SetLineColor( colors[i] )
        h.SetLineWidth( 2 )
        h.Draw('SAME')
        leg.AddEntry(h, h.GetTitle(),"lpe")

    # Redraw RCT on top
    hists[0].Draw('SAME')
    print "max",max_
    print "min",min_
    hists[0].SetMaximum( max_ * 2. )
    #hists[0].SetMinimum( min_ * 2. )
    hists[0].SetMinimum( 1. )
    leg.Draw("same")
    cms = drawCMSString("CMS Simulation, Phase-II 90X, <PU>=200, Minimum-Bias")
    c.Update()

    c.Print('/afs/cern.ch/user/t/truggles/www/Phase-II/v2/plotsOpt/rates_'+name+'.png')    
    del c
    
def makeEffPlot( ntree, otree, name, cut='', preCut='', yLabel='Eff. (L1 / Gen)', effLimit=50 ) :
    binSize = 5
    c = ROOT.TCanvas('c','c',canvasSize,canvasSize)
    p = ROOT.TPad('p','p',0,0,1,1)
    p.Draw()
    
    if preCut == '' :
        neumCut = cut
    else : 
        neumCut = cut+"*"+preCut

    nBins = int(effLimit/binSize)
    nBins = 20
    denom = ROOT.TH1F('denom'+name, name, nBins,0,effLimit)
    otree.Draw('gen_pt >> denom'+name, preCut)
    neum = ROOT.TH1F('neum'+name, name, nBins,0,effLimit)
    ntree.Draw('gen_pt >> neum'+name, neumCut)
    graph = ROOT.TGraphAsymmErrors(neum, denom)
    graph.SetMarkerSize(0)
    graph.SetLineWidth(2)
    
    graph.Draw()
    graph.GetYaxis().SetTitle(yLabel)
    graph.GetXaxis().SetTitle('Gen P_{T}')
    #c.Print('plotsOpt/eff_'+name+'.png')    
    del denom, neum
    del c,p
    return graph

def plotEffHists( name, graphs=[], nCol = 1 ) :
    #colors = [ROOT.kBlack, ROOT.kRed, ROOT.kBlue, ROOT.kGreen, ROOT.kOrange+7, ROOT.kMagenta, ROOT.kCyan, ROOT.kYellow+1, ROOT.kGreen-2]
    #colors = [1, 2, 3, 4, 5, 6, 7, 8, 46]
    colors = [1, 2, 3, 4, ROOT.kYellow+1, 6, 7, 8, 46]
    c = ROOT.TCanvas('c','c',canvasSize,canvasSize)
    c.SetTitle( name )
    c.SetGrid()
    xStart = 0.4 if nCol < 3 else 0.25
    leg = setLegStyle(xStart,0.78,0.95,0.92)
    leg.SetNColumns(nCol)
    leg.SetFillStyle(1001)
    leg.SetFillColor(ROOT.kWhite)


    mg = ROOT.TMultiGraph("mg", c.GetTitle())
    for i, g in enumerate(graphs) :
        g.SetLineColor( colors[int(math.floor(i/float(nCol)))] )
        g.SetMarkerColor( colors[int(math.floor(i/float(nCol)))] )
        g.SetMarkerStyle(20)
        if i%nCol==0: g.SetLineStyle(2)
        elif nCol == 3 and i%nCol==1 : g.SetLineStyle(9)
        else: g.SetLineStyle(1)
        mg.Add( g )
        leg.AddEntry(g, g.GetTitle(),"lpe")

    mg.Draw("aplez")
    mg.GetXaxis().SetTitle("Gen P_{T}")
    mg.GetYaxis().SetTitle( graphs[0].GetYaxis().GetTitle() )
    mg.SetMaximum( 1.4 )
    leg.Draw("same")
    cms = drawCMSString("CMS Simulation, Phase-II 90X, <PU>=200, L1EG Crystal Algo.")

    # Add name of cut
    xPos = .2
    yPos = .735
    addText( xPos, yPos, "Phase-2 L1EG Cut: "+name.replace('_',' ') )

    c.Update()
    c.Print('/afs/cern.ch/user/t/truggles/www/Phase-II/v2/plotsOpt/effs_'+name.replace(' ','_')+'.png')    
    del c


def makeComparisons( Cut, name, trkDetails=False, changeDenom=["",""], var='cluster_pt', doPhoton=False ) :

    #date = 'v2'
    ##date = '20170503v1'
    #newEffFileName = '%s/%s_singleElectron_eff.root' % (date, date)
    #newPhotonFileName = '%s/%s_singlePhoton_eff.root' % (date, date)
    #newRateFileName = '%s/%s_minBias_rate.root' % (date, date)
    date = 'v2'
    newEffFileName = 'r2_phase2_singleElectron_%s.root' % (date)
    newPhotonFileName = 'r2_phase2_singlePhoton_%s.root' % (date)
    newRateFileName = 'r2_phase2_minBias_%s.root' % (date)
    
    rateFile = ROOT.TFile( newRateFileName, 'r' )
    effFile = ROOT.TFile( newEffFileName, 'r' )

    oldRateFile = ROOT.TFile(newRateFileName,'r')
    if trkDetails :
        oldRateTrackFile = ROOT.TFile('egTriggerRateTracks.root','r')
    oldRateTree = oldRateFile.Get('analyzer/crystal_tree')
    if doPhoton :
        oldPhoEffFile = ROOT.TFile('egTriggerPhoEff.root','r')
        oldPhoEffTree = oldPhoEffFile.Get('analyzer/crystal_tree')
        makeNewCutTrees( 'egTriggerPhoEff.root', 'effPhoTree.root', Cut )
        effPhoFile = ROOT.TFile( 'effPhoTree.root', 'r' )
        ePhoTree = effPhoFile.Get("events")
    oldEffFile = ROOT.TFile(newEffFileName,'r')
    oldEffTree = oldEffFile.Get('analyzer/crystal_tree')
    # With the porposed cut, make a new cut tree, then sort
    # to ensure that only 1 cluster per event
    makeNewCutTrees( newEffFileName, 'effTree.root', Cut )
    makeNewCutTrees( newRateFileName, 'rateTree.root', Cut )
    #makeNewCutTrees( 'egTriggerRates.root', 'rateTreeTracks.root', 'trackPt > 10' )
    effFile = ROOT.TFile( 'effTree.root', 'r' )
    eTree = effFile.Get("events")
    newRateFile = ROOT.TFile('rateTree.root','r')
    rTree = newRateFile.Get("events")
    #newRateFileTracks = ROOT.TFile('rateTreeTracks.root','r')
    #rTreeTracks = newRateFileTracks.Get("events")

    # Additional pt cuts
    pt16 = "*("+var+" > 16)"
    pt20 = "*("+var+" > 20)"
    pt30 = "*("+var+" > 30)"

    if trkDetails :
        trackIso2 = "((0.130534 + 0.0131326*cluster_pt) > (trackIsoConePtSum/trackPt))"
        rTracks10 = makeRatePlot( oldRateTrackFile, rTreeTracks, "tracks p_{T}>10 GeV", "trackPt>10" )
        rTracks15 = makeRatePlot( oldRateTrackFile, rTreeTracks, "tracks p_{T}>15 GeV", "trackPt>15" )
        rTracks10Iso = makeRatePlot( oldRateTrackFile, rTreeTracks, "Iso tracks p_{T}>10 GeV", "trackPt>10 && "+trackIso2 )
        rTracks15Iso = makeRatePlot( oldRateTrackFile, rTreeTracks, "Iso tracks p_{T}>15 GeV", "trackPt>15 && "+trackIso2 )
        rTracks10egIso = makeRatePlot( oldRateFile, oldRateTree, "Iso tracks p_{T}>10 GeV - EG Matched", "trackPt>10 &&"+trackIso2 )
        rTracks15egIso = makeRatePlot( oldRateFile, oldRateTree, "Iso tracks p_{T}>15 GeV - EG Matched", "trackPt>15 &&"+trackIso2 )
    if var != 'cluster_pt' :
        #r5adj = makeRatePlot( oldRateFile, rTree, name, Cut, 50, var )
        #r5_20adj = makeRatePlot( oldRateFile, rTree, name+" p_{T}>20", Cut+pt20, 50, var )
        #r5_30adj = makeRatePlot( oldRateFile, rTree, name+" p_{T}>30", Cut+pt30, 50, var )
        r5adj = makeRatePlot( oldRateFile, rTree, name+" ptAdj", Cut, 50, var )
        r5_20adj = makeRatePlot( oldRateFile, rTree, name+" p_{T}>20 ptAdj", Cut+pt20, 50, var )
        r5_30adj = makeRatePlot( oldRateFile, rTree, name+" p_{T}>30 ptAdj", Cut+pt30, 50, var )
    rTracks10eg = makeRatePlot( oldRateFile, oldRateTree, "tracks p_{T}>10 GeV - EG Matched", "trackPt>10" )
    rTracks15eg = makeRatePlot( oldRateFile, oldRateTree, "tracks p_{T}>15 GeV - EG Matched", "trackPt>15" )
    noCuts = makeRatePlot( oldRateFile, oldRateTree, "Raw Rate - No Cuts", "" )
    
    #xMax = 50 if not doPhoton else 75
    xMax = 60
    r5 = makeRatePlot( oldRateFile, rTree, name, Cut, xMax )
    r5_20 = makeRatePlot( oldRateFile, rTree, name+" p_{T}>20", Cut+pt20, xMax )
    r5_30 = makeRatePlot( oldRateFile, rTree, name+" p_{T}>30", Cut+pt30, xMax )
    #rTDR = oldRateFile.Get('analyzer/l1extraParticlesUCT:All_rate')
    #rTDR.SetTitle('Stage 1 Level 1 Trigger - 2015')
    if trkDetails and changeDenom == ["",""] :
        plotRateHists(  name+"_track_details", [noCuts, rTracks10, rTracks15, rTracks10eg, rTracks15eg] )
        plotRateHists(  name+"_track_details_iso", [noCuts, rTracks10, rTracks15, rTracks10eg, rTracks15eg, rTracks10Iso, rTracks15Iso, rTracks10egIso, rTracks15egIso] )
    if changeDenom == ["",""] and var == 'cluster_pt' : 
        #plotRateHists(  name+"_turnons_20_30", [rTDR, r5, r5_20, r5_30] )
        plotRateHists(  name+"_turnons_20_30", [r5, r5_20, r5_30] )
    #plotRateHists(  name+"_turnons16_20_30", [rTDR, noCuts, rTracks10eg, rTracks15eg, r5, r5_20, r5_30] )
    #plotRateHists(  name+"_turnons16_20_30", [rTDR, noCuts, rTracks10, rTracks15, rTracks10eg, rTracks15eg, r5, r5_20, r5_30] )
    if var != 'cluster_pt' : 
        plotRateHists(  name+"_turnons_20_30_ptAdjust", [rTDR, r5adj, r5_20adj, r5_30adj] )
        plotRateHists(  name+"_turnons_20_30", [rTDR, r5, r5_20, r5_30] )
        return

    preCut = ""
    yEffLabel = "Eff. (L1/ Gen)"
    saveName = name
    if changeDenom != ["",""] : 
        preCut = changeDenom[0]
        yEffLabel = changeDenom[1]
        saveName = name+"_modDenom"
    e5 = makeEffPlot( eTree, oldEffTree, "Phase-2 Electron: All", Cut, preCut, yEffLabel, xMax )
    e5_20 = makeEffPlot( eTree, oldEffTree, "Phase-2 Electron: p_{T}>20", Cut+pt20, preCut, yEffLabel, xMax )
    e5_30 = makeEffPlot( eTree, oldEffTree, "Phase-2 Electron: p_{T}>30", Cut+pt30, preCut, yEffLabel, xMax )
    if doPhoton :
        e5Pho = makeEffPlot( ePhoTree, oldPhoEffTree, "Phase-2 Photon: All", Cut, preCut, yEffLabel, xMax )
        e5_20Pho = makeEffPlot( ePhoTree, oldPhoEffTree, "Phase-2 Photon: p_{T}>20", Cut+pt20, preCut, yEffLabel, xMax )
        e5_30Pho = makeEffPlot( ePhoTree, oldPhoEffTree, "Phase-2 Photon: p_{T}>30", Cut+pt30, preCut, yEffLabel, xMax )
    #neum = oldEffFile.Get('analyzer/l1extraParticlesUCT:All_efficiency_pt')
    #neum20 = oldEffFile.Get('analyzer/l1extraParticlesUCT:All_threshold20_efficiency_gen_pt')
    #neum30 = oldEffFile.Get('analyzer/l1extraParticlesUCT:All_threshold30_efficiency_gen_pt')
    ###denom = oldEffFile.Get('analyzer/gen_pt')
    denom = ROOT.TH1F('denomX', 'denomX',int(xMax/5),0,xMax)
    oldEffTree.Draw('denom_pt >> denomX')

    #for h in [neum, neum20, neum30] :
    #    h.Rebin(5) 
    #nBins = denom.GetXaxis().GetNbins()
    #for bin in range( 0, nBins+2 ) :
    #    if denom.GetBinContent(bin) < neum.GetBinContent(bin) :
    #        denom.SetBinContent(bin, neum.GetBinContent(bin) ) # FIXME
    #        print " --- Bin: %i    Neum: %.2f    Denom %.2f" % (bin, neum.GetBinContent(bin), denom.GetBinContent(bin))



    #eTDRall = ROOT.TGraphAsymmErrors( neum, denom )
    #eTDR20 = ROOT.TGraphAsymmErrors( neum20, denom )
    #eTDR30 = ROOT.TGraphAsymmErrors( neum30, denom )
    #eTDRall.SetTitle('Stage 1: All')
    #eTDR20.SetTitle('Stage 1: p_{T}>20')
    #eTDR30.SetTitle('Stage 1: p_{T}>30')
    if doPhoton :
        graphs = [eTDRall, e5, e5Pho, eTDR20, e5_20, e5_20Pho, eTDR30, e5_30, e5_30Pho] 
        nLegendCol = 3
    else :
        #graphs = [eTDRall, e5, eTDR20, e5_20, eTDR30, e5_30] 
        graphs = [e5, e5_20, e5_30] 
        nLegendCol = 2
    for graph in graphs :
        graph.GetYaxis().SetTitle(yEffLabel)
    plotEffHists(  saveName, graphs, nLegendCol )


def findPercentage( cnt, tree, var, targetPercent=0.99, cut="", startNeg=True, xRange=[0.,0.] ) :
    # find the max and min val of var in tree
    if xRange[0] == 0 and xRange[1] == 0 :
        varMax = 0.
        varMin = 0.
        for row in tree :
            val = getattr( row, var )
            if val < varMin : varMin = val
            if val > varMax : varMax = val
        print "Variable: %s has values in the range %.2f - %.2f" % (var, varMin, varMax)
    else :
        print "Using user provided xRange %.2f - %.2f" % (xRange[0], xRange[1])
        varMax = xRange[1]
        varMin = xRange[0]

    h = ROOT.TH1F('h%i' % cnt, 'h', 1000, varMin, varMax)
    tree.Draw( var+" >> h%i" % cnt, cut )
    total = h.Integral()
    #print "Total: ",total
    runningTot = 0.
    targetVal = total * ( 1. - targetPercent)
    if startNeg :
        #print " - Summing from negative upwards"
        begin = 1
        end = h.GetNbinsX()+1
        intervals = 1
    if not startNeg :
        #print " - Summing from positive downwards"
        begin = h.GetNbinsX()+1
        end = 1
        intervals = -1
    
    for bin in range(begin, end, intervals ) :
        #print bin
        runningTot += h.GetBinContent( bin )
        if runningTot >= targetVal :
            ret = h.GetBinCenter( bin )
            print "Reached target percent : %.3f at val: %.3f" % (targetPercent, ret )
            return [ret,h]

    print "Error, not sure why we made it here..."
    

def findQuantity( h, position ) :
    # find the max and min val of var in tree
    # +1 on valUp just so we don't double count the target bin
    valUp = h.Integral( h.GetXaxis().FindBin(position)+1, h.GetNbinsX() +1 )
    valDown = h.Integral( 1, h.GetXaxis().FindBin(position) )
    total = h.Integral()
    #print "Postion",position
    return [valDown, valUp, total]

def checkVarInRange( cnt, eTree, rTree, var, cut, targetPercent=0.99, startNeg=False, xRange=[0.,0.]) :
    output = [var,]

    print "Electrons"
    cnt += 1
    e1 = findPercentage( cnt, eTree, var, targetPercent, cut, startNeg, xRange )
    print "Fakes"
    cnt += 1
    r1 = findPercentage( cnt, rTree, var, targetPercent, cut, startNeg, xRange )
    #return [ret,h]
    
    #findQuantity( h, position )
    info1 = findQuantity( e1[1], e1[0] )
    info2 = findQuantity( r1[1], e1[0] )
    output.append( e1[0] )
    #return [valDown, valUp, total]
    if startNeg :
        print "Sig is cut %.3f percent" % (info1[0]/info1[2])
        print "Bkg is cut %.3f percent" % (info2[0]/info2[2])
        output.append( info1[0]/info1[2] )
        output.append( info2[0]/info2[2] )
    if not startNeg :
        print "Sig is cut %.3f percent" % (info1[1]/info1[2])
        print "Bkg is cut %.3f percent" % (info2[1]/info2[2])
        output.append( info1[1]/info1[2] )
        output.append( info2[1]/info2[2] )
    output.append( cut )
    return output


def makeCutROC( name, eTree, rTree, var, rocAry, prevCut, baseCut='', text='') :

    # Get our total # of events for sig and bkg
    eTree.Draw( var, baseCut )
    hE = gPad.GetPrimitive( "htemp" )
    sigInit = hE.Integral()
    rTree.Draw( var, baseCut )
    hR = gPad.GetPrimitive( "htemp" )
    bkgInit = hR.Integral()
    print "Signal Integral Inital:",sigInit
    print "Bkg Integral Inital:",bkgInit

    # For storing our values as we check the cuts
    sigVals = array('d', [])
    bkgVals = array('d', [])
    paramVals = array('d', [])

    # Plot our distribution, and check yields as we 
    # integrate along it
    if baseCut != '' : prevCut += "*"+baseCut
    h1 = ROOT.TH1F('h1','h1',rocAry[0],rocAry[1],rocAry[2])
    eTree.Draw( var + ' >> h1', prevCut )
    h2 = ROOT.TH1F('h2','h2',rocAry[0],rocAry[1],rocAry[2])
    rTree.Draw( var + ' >> h2', prevCut )

    for b in range( 1, h1.GetNbinsX()+1 ) :
        paramVals.append( h1.GetXaxis().GetBinCenter( b ) )
        eInt = h1.Integral( 0, b )
        rInt = h2.Integral( 0, b )
        if b % 50 == 0 or (b < 100 and b % 5 == 0) :
            print "Bin: %i  Eff: %f    Rate: %f" % (b, eInt,rInt)
        sigVals.append( eInt / sigInit )
        bkgVals.append( 1. - rInt / bkgInit )
        if abs( sigVals[-1] - .9 ) < 0.001 :
            print "Cut: %f    Sig: %f    Bkg: %f" % (paramVals[-1], sigVals[-1], bkgVals[-1])
        if 'PtMatch' in name :
            if abs( sigVals[-1] - .9 ) < 0.01 :
                print "Cut: %f    Sig: %f    Bkg: %f" % (paramVals[-1], sigVals[-1], bkgVals[-1])
            if abs( sigVals[-1] - .95 ) < 0.01 :
                print "Cut: %f    Sig: %f    Bkg: %f" % (paramVals[-1], sigVals[-1], bkgVals[-1])


    c = ROOT.TCanvas('c','c',800,800)
    c.SetGrid()
    c.SetTitle( name )
    g = ROOT.TGraph(rocAry[0], sigVals, bkgVals)
    g.Draw()
    g.GetXaxis().SetTitle('Signal Efficiency')
    g.GetYaxis().SetTitle('Background Rejection')
    g.SetMarkerStyle(0)
    g.SetLineColor(2)
    g.SetLineWidth(2)
    g.SetMaximum( 1.05 )
    g.SetMinimum( 0.5 )
    if "BaselineCut" in name :
        g.SetMinimum( 0.0 )
    g.GetXaxis().SetLimits( 0.0, 1. )
    g.Draw()
    c.Update()

    if text :
        chan = ROOT.TLatex(.2, .80,"x")
        chan.SetTextSize(0.04)
        chan.DrawLatexNDC(.2, .2, text )

    c.Print('/afs/cern.ch/user/t/truggles/www/Phase-II/v2/plotsOpt/ROC_'+name+'.png')    


def makeCutROCPlus( name, eTree, rTree, var, rocAry, prevCut, baseCut='', text='') :

    # Mapping for renaming aspects depending on if dPhi or dEta is the 'leading' cut
    nameMap = {
        'abs(trackDeltaEta)' : ['abs(trackDeltaPhi)', 'phi', 'eta'],
        'abs(trackDeltaPhi)' : ['abs(trackDeltaEta)', 'eta', 'phi']}

    # Get our total # of events for sig and bkg
    eTree.Draw( var, baseCut )
    hE = gPad.GetPrimitive( "htemp" )
    sigInit = hE.Integral()
    rTree.Draw( var, baseCut )
    hR = gPad.GetPrimitive( "htemp" )
    bkgInit = hR.Integral()

    # Extra cuts to vary phi and eta simultaneously
    dXCuts = []
    for i in range( 1, 8 ) :
        dXCuts.append( i*.01 )
    dXCuts = [0.01, 0.02, 0.03, 0.04, 0.05, 0.08, 0.12, 0.2, 0.5]
    
    sigs = {}
    bkgs = {}
    graphs = {}
    for cut in dXCuts :
        # For storing our values as we check the cuts
        sigs[cut] = array('d', [])
        bkgs[cut] = array('d', [])

        # Plot our distribution, and check yields as we 
        # integrate along it
        if baseCut != '' : prevCut += "*"+baseCut
        addition = "*(%s<%f)" % (nameMap[var][0], cut)
        h1 = ROOT.TH1F('h1','h1',rocAry[0],rocAry[1],rocAry[2])
        eTree.Draw( var + ' >> h1', prevCut+addition )
        h2 = ROOT.TH1F('h2','h2',rocAry[0],rocAry[1],rocAry[2])
        rTree.Draw( var + ' >> h2', prevCut+addition )

        #for b in range( 1, h1.GetNbinsX()+1 ) :
        for b in range( 0, h1.GetNbinsX() ) :
            eInt = h1.Integral( 0, b )
            rInt = h2.Integral( 0, b )
            sigs[cut].append( eInt / sigInit )
            bkgs[cut].append( 1. - rInt / bkgInit )
        del h1, h2
    
        graphs[cut] = ROOT.TGraph(rocAry[0], sigs[cut], bkgs[cut])
        graphs[cut].SetTitle("d#%s < %.2f" % (nameMap[var][1], cut) )

    c = ROOT.TCanvas('c','c',800,800)
    c.SetGrid()
    c.SetTitle( name )

    leg = setLegStyle(0.2,0.3,0.47,0.6)
    leg.SetFillStyle(1001)
    leg.SetFillColor(ROOT.kWhite)

    # Set everything for the first one and draw it
    graphs[dXCuts[0]].Draw()
    graphs[dXCuts[0]].GetXaxis().SetTitle('Signal Efficiency')
    graphs[dXCuts[0]].GetYaxis().SetTitle('Background Rejection')
    #graphs[dXCuts[0]].SetMaximum( 0.95 )
    #graphs[dXCuts[0]].SetMinimum( 0.6 )
    #graphs[dXCuts[0]].GetXaxis().SetLimits( 0.3, 1. )
    #if 'Baseline' in name :
    graphs[dXCuts[0]].SetMaximum( 1.05 )
    graphs[dXCuts[0]].SetMinimum( 0.0 )
    graphs[dXCuts[0]].GetXaxis().SetLimits( 0.0, 1. )
    #graphs[dXCuts[0]].SetLineColor(ROOT.kRed-10)
    graphs[dXCuts[0]].SetLineColor(1)
    graphs[dXCuts[0]].SetLineWidth(2)
    graphs[dXCuts[0]].SetMarkerStyle(0)
    graphs[dXCuts[0]].Draw()
    leg.AddEntry(graphs[dXCuts[0]], graphs[dXCuts[0]].GetTitle(),"lpe")
    dXCuts.remove( dXCuts[0] )

    for i, cut in enumerate(dXCuts) :
        #graphs[cut].Draw('SAME')
        #if i < 5 :
        #    graphs[cut].SetLineColor(ROOT.kRed-10+2*(i+1) )
        #else :
        #    graphs[cut].SetLineColor(ROOT.kBlue-10+2*(i+1) )
        graphs[cut].SetLineColor(2+i)
        graphs[cut].SetLineWidth(2)
        graphs[cut].Draw('SAME')
        leg.AddEntry(graphs[cut], graphs[cut].GetTitle(),"lpe")
    leg.Draw()
    c.Update()


    if text :
        txt1 = ROOT.TLatex(.2, .80,"x")
        txt1.SetTextSize(0.04)
        txt1.DrawLatexNDC(.2, .15, text )
        if baseCut != '' and "Baseline" not in name : 
            txt2 = ROOT.TLatex(.2, .80,"x")
            txt2.SetTextSize(0.035)
            text2 = "All considered events passing: %s" % baseCut
            txt2.DrawLatexNDC(.2, .19, text2 )

    c.Print('/afs/cern.ch/user/t/truggles/www/Phase-II/v2/plotsOpt/ROCPlus_'+name+'.png')    


if __name__ == '__main__' :


    cnt = 0
    
    tdrstyle.setTDRStyle()
    c = ROOT.TCanvas('c','c',canvasSize,canvasSize)
    showerShapes = "(-0.921128 + 0.180511*TMath::Exp(-0.0400725*cluster_pt)>(-1)*(e2x5/e5x5))"
    showerShapesB = "(-0.998511 + -8.16648e-05*TMath::Exp(-0.210906*cluster_pt)>(-1)*(e2x5b/e5x5b))"
    showerShapesC = "((-0.98 >(-1)*(e2x5/e5x5) || cluster_pt >35 ))"
    IsolationB = "((0.42128 + -1.48187*TMath::Exp(-0.234355*cluster_pt))>cluster_isoGtr2)"
    IsolationC = "((0.472785 + -8.17373*TMath::Exp(-0.821266*cluster_pt))>cluster_iso)"
    ### These below are with ~99% efficiency at plateau
    Isolation = "((0.990748 + 5.64259*TMath::Exp(-0.0613952*cluster_pt))>cluster_iso)"
    Isolation1 = "((-15.2726 + 15.9463*TMath::Exp(-0.000282339*cluster_pt))>cluster_isoGtr1)"
    Isolation2 = "((0.42128 + -1.48187*TMath::Exp(-0.234355*cluster_pt))>cluster_isoGtr2)"
    Isolation500 = "((0.562669 + 2.01266*TMath::Exp(-0.0559235*cluster_pt))>cluster_isoGtr500)"
    IsolationX = "((0.617738 + 2.00979*TMath::Exp(-0.056631*cluster_pt))>((cluster_iso*corePt-ecalPUtoPt*0.496)/corePt))"
    IsolationLobe = "((0.658715 + 1.9467*TMath::Exp(-0.0415617*cluster_pt))>((cluster_iso*corePt-(corePt*.1 < lslPt ? ecalPUtoPt-lslPt : (corePt*.1 < uslPt ? ecalPUtoPt-uslPt : ecalPUtoPt ) )*0.496)/corePt))"
    ### Aiming for ~95% eff at plateau
    #Isolation = "((0.884288 + 5.24376*TMath::Exp(-0.0838355*cluster_pt))>cluster_iso)"
    #Isolation500 = "((0.369795 + 1.66704*TMath::Exp(-0.0738599*cluster_pt))>cluster_isoGtr500)"
    #Isolation1 = "((-8.98409 + 9.35278*TMath::Exp(-0.000348177*cluster_pt))>cluster_isoGtr1)"
    #Isolation2 = "((0.191302 + -0.351645*TMath::Exp(-0.116907*cluster_pt))>cluster_isoGtr2)"
    #IsolationX = "((0.409748 + 1.52035*TMath::Exp(-0.0661331*cluster_pt))>((cluster_iso*corePt-ecalPUtoPt*0.496)/corePt))"

    tkIsoMatched = "((0.106544 + 0.00316748*cluster_pt)>(trackIsoConePtSum/trackPt))"

    cut_none = ""
    cut_ss = showerShapes
    cut_ss_cIso = showerShapes+"*"+Isolation
    cut_ss_cIsoB = showerShapesB+"*"+IsolationB
    cut_ss_cIsoC = showerShapesC+"*"+IsolationC
    cut_ss_cIso1 = showerShapes+"*"+Isolation1
    cut_ss_cIso2 = showerShapes+"*"+Isolation2
    cut_ss_cIso500 = showerShapes+"*"+Isolation500
    cut_ss_cIsoX = showerShapes+"*"+IsolationX
    cut_ss_cIsoLobe = showerShapes+"*"+IsolationLobe
    #cut_ss_cIso1 = Isolation1
    #cut_ss_cIso2 = Isolation2
    #cut_ss_cIso500 = Isolation500
    #cut_ss_cIsoX = IsolationX
    cut_ss_cIso_tkNoM = cut_ss_cIso+"*(trackDeltaR>0.1)"
    cut_ss_cIso_tkM = cut_ss_cIso+"*(trackDeltaR<0.1)"
    cut_ss_cIso_tkM_tkIso = cut_ss_cIso_tkM+"*"+tkIsoMatched
    tkMatched = "(trackDeltaR<.1)"
    tkNoMatched = "(trackDeltaR>.1)"

    rocAry = [1000, 0.0, 1.]
    textR = "Scanning 0.0 < #DeltaR(Trk, L1EG) < 1.0"
    textPhi = "Scanning 0.0 < d#phi(Trk, L1EG) < 1.0"
    textEta = "Scanning 0.0 < d#eta(Trk, L1EG) < 1.0"
    rebase20 = "(cluster_pt>20)"
    rebase30 = "(cluster_pt>30)"
    rebaseAll = cut_ss_cIso

    # Below cuts are for 500 MeV energy recHit cut
    ss500 = "(-0.905265 + 0.0409635*TMath::Exp(-0.165703*cluster_pt)>(-1)*(e2x5/e5x5))"
    iso500 = "((0.983083 + 3.32699*TMath::Exp(-0.0840977*cluster_pt))>cluster_iso)"
    cut_ss_cIso500 = ss500+"*"+iso500
    ss502 = "(-0.912155 + -0.0362738*TMath::Exp(-0.0482866*cluster_pt)>(-1)*(e2x5/e5x5))"
    iso502 = "((0.836744 + 2.60678*TMath::Exp(-0.115636*cluster_pt))>cluster_iso)"
    cut_ss_cIso502 = ss502+"*"+iso502
    makeComparisons( cut_ss_cIso502, "e2x5OverE5x5 Iso", False, ["",""], 'cluster_pt' )
    # Very aggressive in lower pt region below
    ss5002 = "(-0.91957 + -0.0233851*TMath::Exp(-0.0305597*cluster_pt)>(-1)*(e2x5/e5x5))"
    iso5002 = "((0.602232 + 2.78939*TMath::Exp(-0.0985843*cluster_pt))>cluster_iso)"
    cut_ss_cIso5002 = ss5002+"*"+iso500
    #makeComparisons( cut_ss_cIso5002, "e2x5OverE5x5 Iso", False, ["",""], 'cluster_pt' )
    #makeCutROC( "testDRCuts_ss_cIso", eTree, rTree, "trackDeltaR", rocAry, cut_ss_cIso, cut_none, textR )
    #makeCutROC( "testDPhiCuts_ss_cIso", eTree, rTree, "abs(trackDeltaPhi)", rocAry, cut_ss_cIso, cut_none, textPhi )
    #makeCutROC( "testDEtaCuts_ss_cIso", eTree, rTree, "abs(trackDeltaEta)", rocAry, cut_ss_cIso, cut_none, textEta )
    #makeCutROC( "testDRCutsBase20_ss_cIso", eTree, rTree, "trackDeltaR", rocAry, cut_ss_cIso, rebase20, textR )
    #makeCutROC( "testDPhiCutsBase20_ss_cIso", eTree, rTree, "abs(trackDeltaPhi)", rocAry, cut_ss_cIso, rebase20, textPhi )
    #makeCutROC( "testDEtaCutsBase20_ss_cIso", eTree, rTree, "abs(trackDeltaEta)", rocAry, cut_ss_cIso, rebase20, textEta )
    #makeCutROC( "testDRCutsBase30_ss_cIso", eTree, rTree, "trackDeltaR", rocAry, cut_ss_cIso, rebase30, textR )
    #makeCutROC( "testDPhiCutsBase30_ss_cIso", eTree, rTree, "abs(trackDeltaPhi)", rocAry, cut_ss_cIso, rebase30, textPhi )
    #makeCutROC( "testDEtaCutsBase30_ss_cIso", eTree, rTree, "abs(trackDeltaEta)", rocAry, cut_ss_cIso, rebase30, textEta )
    #makeCutROC( "testDRCutsBaselineCuts_ss_cIso", eTree, rTree, "trackDeltaR", rocAry, cut_ss_cIso, rebaseAll, textR )
    #makeCutROC( "testDPhiCutsBaselineCuts_ss_cIso", eTree, rTree, "abs(trackDeltaPhi)", rocAry, cut_ss_cIso, rebaseAll, textPhi )
    #makeCutROC( "testDEtaCutsBaselineCuts_ss_cIso", eTree, rTree, "abs(trackDeltaEta)", rocAry, cut_ss_cIso, rebaseAll, textEta )
    #makeCutROC( "testDRCutsBaselineCuts", eTree, rTree, "trackDeltaR", rocAry, cut_none, cut_none, textR )

    ptRes = "(abs(((cluster_pt - trackPt) / cluster_pt )) < .5)"
    #makeCutROC( "testDRCutsBaselineCuts20_ss_cIso", eTree, rTree, "trackDeltaR", rocAry, cut_ss_cIso+"*"+rebase20, rebaseAll+"*"+rebase20, textR )
#XXX    makeCutROC( "testDRCutsBaselineCuts20PtMatch_ss_cIso", eTree, rTree, "trackDeltaR", rocAry, cut_ss_cIso+"*"+rebase20+"*"+ptRes, rebaseAll+"*"+rebase20+"*"+ptRes, textR )
#XXX    makeCutROC( "testDRCutsBaselineCuts20PtMatch_ss_cIsoC", eTree, rTree, "trackDeltaR", rocAry, cut_ss_cIsoC+"*"+rebase20+"*"+ptRes, rebaseAll+"*"+rebase20+"*"+ptRes, textR )
    #XXX makeCutROC( "testDRCutsBaselineCuts20PtMatch_ss_cIsoB", eTree, rTree, "trackDeltaR", rocAry, cut_ss_cIsoB+"*"+rebase20+"*"+ptRes, rebaseAll+"*"+rebase20+"*"+ptRes, textR )

    #makeCutROC( "testDRCutsBaselineCuts20_ss_cIso", eTree, rTree, "trackDeltaR", rocAry, cut_ss_cIso, rebaseAll+"*"+rebase20, textR )
    #makeCutROC( "testDEtaCutsBaselineCuts20_ss_cIso", eTree, rTree, "abs(trackDeltaEta)", rocAry, cut_ss_cIso, rebaseAll+"*"+rebase20, textEta )
    #makeCutROC( "testDPhiCutsBaselineCuts20_ss_cIso", eTree, rTree, "abs(trackDeltaPhi)", rocAry, cut_ss_cIso, rebaseAll+"*"+rebase20, textPhi )


    #makeCutROCPlus( "testDPhiCuts_ss_cIso", eTree, rTree, "abs(trackDeltaPhi)", rocAry, cut_ss_cIso, cut_none, textPhi )
    #makeCutROCPlus( "testDEtaCuts_ss_cIso", eTree, rTree, "abs(trackDeltaEta)", rocAry, cut_ss_cIso, cut_none, textEta )
    #makeCutROCPlus( "testDPhiCutsBase20_ss_cIso", eTree, rTree, "abs(trackDeltaPhi)", rocAry, cut_ss_cIso, rebase20, textPhi )
    #makeCutROCPlus( "testDEtaCutsBase20_ss_cIso", eTree, rTree, "abs(trackDeltaEta)", rocAry, cut_ss_cIso, rebase20, textEta )
    #makeCutROCPlus( "testDPhiCutsBase30_ss_cIso", eTree, rTree, "abs(trackDeltaPhi)", rocAry, cut_ss_cIso, rebase30, textPhi )
    #makeCutROCPlus( "testDEtaCutsBase30_ss_cIso", eTree, rTree, "abs(trackDeltaEta)", rocAry, cut_ss_cIso, rebase30, textEta )
#XXX    makeCutROCPlus( "testDPhiCutsBaseline20_ss_cIso", eTree, rTree, "abs(trackDeltaPhi)", rocAry, cut_ss_cIso+"*"+rebase20, rebaseAll+"*"+rebase20, textPhi )
#XXX    makeCutROCPlus( "testDEtaCutsBaseline20_ss_cIso", eTree, rTree, "abs(trackDeltaEta)", rocAry, cut_ss_cIso+"*"+rebase20, rebaseAll+"*"+rebase20, textEta )
#XXX    makeCutROCPlus( "testDPhiCutsBaseline20PtMatch_ss_cIso", eTree, rTree, "abs(trackDeltaPhi)", rocAry, cut_ss_cIso, rebaseAll+"*"+rebase20+"*"+ptRes, textPhi )
#XXX    makeCutROCPlus( "testDEtaCutsBaseline20PtMatch_ss_cIso", eTree, rTree, "abs(trackDeltaEta)", rocAry, cut_ss_cIso, rebaseAll+"*"+rebase20+"*"+ptRes, textEta )
    #makeCutROCPlus( "testDPhiCutsBaseline_ss_cIso", eTree, rTree, "abs(trackDeltaPhi)", rocAry, cut_ss_cIso, rebaseAll, textPhi )
    #makeCutROCPlus( "testDEtaCutsBaseline_ss_cIso", eTree, rTree, "abs(trackDeltaEta)", rocAry, cut_ss_cIso, rebaseAll, textEta )



    makeSet = False
    if makeSet :
   #     makeComparisons( "(1)", "No_Cuts", True )
   #     makeComparisons( "(passed>0)", "Passed", True )
   #     makeComparisons( cut_ss, "e2x5OverE5x5", False, ["",""], 'crystal_pt_to_RCT2015' )
   #     makeComparisons( cut_ss_cIso, "e2x5OverE5x5 Iso", False, ["",""], 'crystal_pt_to_RCT2015' )
        makeComparisons( cut_ss_cIso, "e2x5OverE5x5 Iso", False, ["",""], 'cluster_pt' )
        #XXX makeComparisons( cut_ss_cIsoB, "e2x5OverE5x5 Iso B", False, ["",""], 'cluster_pt' )
        makeComparisons( cut_ss_cIso1, "e2x5OverE5x5 Iso 1 GeV", False, ["",""], 'cluster_pt' )
        makeComparisons( cut_ss_cIso2, "e2x5OverE5x5 Iso 2 GeV", False, ["",""], 'cluster_pt' )
        makeComparisons( cut_ss_cIso500, "e2x5OverE5x5 Iso 500 MeV", False, ["",""], 'cluster_pt' )
        makeComparisons( cut_ss_cIsoX, "e2x5OverE5x5 Iso PU Corr", False, ["",""], 'cluster_pt' )
        makeComparisons( cut_ss_cIsoLobe, "e2x5OverE5x5 Iso PU Corr Brem Sub", False, ["",""], 'cluster_pt' )
   #     makeComparisons( cut_ss_cIso_tkM, "e2x5OverE5x5 Iso TkMatch", False, [tkMatched, "L1Tk Match #DeltaR<0.1, Eff. (L1/Gen)"] )
   #     makeComparisons( cut_ss_cIso_tkM, "e2x5OverE5x5 Iso TkMatch", False, ["",""], 'crystal_pt_to_RCT2015' )
   #     #tryCut( eTree, rTree, "cluster_pt", cutMatch, previousCut)
   #     makeComparisons( cut_ss_cIso_tkM_tkIso, "e2x5OverE5x5 Iso TkMatch TkIso", False, [tkMatched, "L1Tk Match #DeltaR<0.1, Eff. (L1/Gen)"] )
   #     makeComparisons( cut_ss_cIso_tkM_tkIso, "SLHC Level 1 EGamma Crystal Based Algo.", False, ["",""], 'crystal_pt_to_RCT2015'  )
#XXX        makeComparisons( cut_ss_cIso_tkM_tkIso, "SLHC Level 1 EGamma Crystal Based Algo.", False, ["",""], 'cluster_pt'  )

        #tryCut( eTree, rTree, "cluster_pt", cut_ss, cut_none)
        #tryCut( eTree, rTree, "cluster_pt", showerShapes2, "")
        #tryCut( eTree, rTree, "cluster_pt", "((e2x5/cluster_pt)>.9)", "")
        #makeComparisons( cut, "e2x5OverE5x5" )
        #makeComparisons( cut, "e2x5OverE3x5" )

        #tryCut( eTree, rTree, "cluster_pt", cut, previousCut)
        #makeComparisons( cut, "e2x5OverE5x5 Iso" )

        #trackIso = "((0.130534 + 0.0131326*cluster_pt) > (trackIsoConePtSum/trackPt))"
        #previousCut = cut
        #cut += "*"+trackIso
        #tryCut( eTree, rTree, "cluster_pt", cut, previousCut)
        #makeComparisons( cut, "e2x5OverE5x5 Iso TrkIso" )

        #ptRes = "( ((trackPt-cluster_pt)/trackPt)>-2. )"
        #previousCut = cut
        #cut += "*"+ptRes
        #tryCut( eTree, rTree, "cluster_pt", cut, previousCut)
        #makeComparisons( cut, "e2x5OverE5x5 Iso TrkIso PtRes" )

#tryCut( eTree, rTree, "cluster_pt", "trackDeltaR<0.1", "")

#makeComparisons( "(1)", "No_Cuts", True )
#tryCut( eTree, rTree, "cluster_pt", cut+"*(trackDeltaR<0.1)", cut)
""" consider matched tracks """
#tryCut( eTree, rTree, "cluster_pt", cutMatch, cut)
#tryCut( eTree, rTree, "cluster_pt", cut+"*( (cluster_pt*2>trackPt && cluster_pt*0.5<trackPt))", cut) # Check agreement between Pt's
#tryCut( eTree, rTree, "cluster_pt", cutMatch+"*(bremStrength > .8)", cutMatch)


## Need to include the non-matched tracks as well to get a TRUE RATE
#noTkMatched = "(trackDeltaR>.1)"
#cutMatchIsoPlusNonMatched = cut+"*( ("+tkMatched+"*"+tkIsoMatched+") || ("+noTkMatched+") )"
#
#makeComparisons( cutMatchIsoPlusNonMatched, "Isolated Matching Tks + Non-Isolated Tks", False )
#
#""" consider non-matched tracks """
#cutNoMatch = cut+"*"+noTkMatched
#makeComparisons( cutNoMatch, "e2x5OverE5x5 Iso noTkMatched modDenom", False, [noTkMatched, "L1Tk No Match #DeltaR>0.1, Eff. (L1/Gen)"] )
#makeComparisons( cutNoMatch, "e2x5OverE5x5 Iso noTkMatched", False )
##tryCut( eTree, rTree, "cluster_pt", cutNoMatch+"*(cluster_iso<2.)", cutNoMatch)
#
##tryCut( eTree, rTree, "cluster_pt", cutNoMatch+"*(bremStrength > .8)", cutNoMatch)
#




#trackIso = "((0.130534 + 0.0131326*cluster_pt) > (trackIsoConePtSum/trackPt))"
#ptRes = "( ((trackPt-cluster_pt)/trackPt)>-2. )"
#previousCut = cut
#cut += "*"+ptRes
#tryCut( eTree, rTree, "cluster_pt", cut, previousCut)
#makeComparisons( cut, "e2x5OverE5x5_Iso_TkMatched_TkIso_ptRes_modDenom", False, True )
#makeComparisons( cut, "e2x5OverE5x5_Iso_TkMatched_TkIso_ptRes", False, False )



#XXX #trackIso = "((0.0947627 + 0.0135767*cluster_pt) > (trackIsoConePtSum/trackPt))"
#XXX #hovere = "((0.40633 + 2.17848*TMath::Exp(-0.114384*cluster_pt))>cluster_hovere)"
#XXX prevcut = showerShapes+"*"+Isolation
#XXX #cut = showerShapes+"*"+Isolation+"*"+hovere
#XXX #tryCut( eTree, rTree, "cluster_pt", cut, prevcut)
#XXX #XXX makeComparisons( cut, "e2x5OverE5x5_Iso_HoE" )
#XXX hovere = "((0.426413 +2.62318 *TMath::Exp(-0.105685*cluster_pt))>cluster_hovere)"
#XXX prevcut = cut2 
#XXX cut2 += "*"+hovere
#XXX #XXX tryCut( eTree, rTree, "cluster_pt", cut2, prevcut)
#XXX #XXX makeComparisons( cut2, "e2x5OverE5x5_Iso_TrkIso_HoE" )
#XXX ###bremTkChi2 = "((-0.622523 + -0.171795*TMath::Exp(-0.097391*trackChi2))>(-1)*bremStrength)"
#XXX ###prevcut = cut2 
#XXX ###cut2 += "*"+bremTkChi2
#XXX ###tryCut( eTree, rTree, "cluster_pt", cut2, prevcut)
#XXX 
#XXX ptRes3 = "( ((trackPt-cluster_pt)/trackPt)>-3. )"
#XXX cut3 = prevcut+"*"+ptRes3
#XXX cut4 = prevcut+"*"+ptRes2
#XXX #tryCut( eTree, rTree, "cluster_pt", cut3, prevcut)
#XXX #tryCut( eTree, rTree, "cluster_pt", cut4, prevcut)
#XXX #tryCut( eTree, rTree, "cluster_pt", ptRes, "")
#XXX #makeComparisons( cut4, "e2x5OverE5x5_Iso_TrkIso_PtRes" )
#XXX bremVChi2 = "((-0.622523 + -0.171795*TMath::Exp(-0.097391*trackChi2))>(-1)*(bremStrength))"
#XXX #cut5 = prevcut+"*"+bremVChi2
#XXX #tryCut( eTree, rTree, "cluster_pt", cut5, prevcut)
#XXX deltaPosition = "((abs(trackDeltaPhi)<.3 && abs(trackDeltaEta)<.3 && trackDeltaR<.3) || cluster_pt>25)" 
#XXX cut5 = prevcut+"*"+deltaPosition
#XXX #tryCut( eTree, rTree, "cluster_pt", cut5, prevcut)
#XXX #cut5 += "*"+ptRes2
#XXX #makeComparisons( cut5, "e2x5OverE5x5_Iso_TrkIso_PtRes_dPos" )
#XXX bremStr = "((-0.645727 + -0.00170667*cluster_pt)>(-1)*bremStrength)" 
#XXX cut5 = prevcut+"*"+bremStr
#XXX #tryCut( eTree, rTree, "cluster_pt", cut5, prevcut)
#XXX bremStr2 = "((-0.697673 + -0.00130133*cluster_pt)>(-1)*bremStrength)" 
#XXX cut5 = prevcut+"*"+bremStr2
#XXX #tryCut( eTree, rTree, "cluster_pt", cut5, prevcut)



varMap = {
    # Var name and Start from below or above
    "cluster_iso" : (False,[0.,0.]),
    "cluster_hovere" : (False,[0.,0.]),
    "trackDeltaR" : (False,[0.,0.]),
    "((trackPt-cluster_pt)/trackPt)" : (True,[-10.0, 1.5]),
    "abs(trackDeltaEta)" : (False,[0.,2.]),
    "abs(trackDeltaPhi)" : (False,[0.,2.]),
    "(-1)*(bremStrength)" : (False,[-1.,0.]),
    }

#cut15 base
cut = "(((0.415233 + 1.51272 * TMath::Exp(-0.10266*cluster_pt)) > cluster_hovere) && ((1.08154 + 4.28457 *TMath::Exp(-0.0556304*cluster_pt)) > cluster_iso))"
cut += "*(( cluster_pt>25 || (trackDeltaR < 0.35)*(abs(trackDeltaPhi)<.3)*(abs(trackDeltaEta)<.3)*(((trackPt - cluster_pt)/trackPt)>-2)))"
cut += "*(cluster_pt > 25)"

targetPercent = 0.99




#results = []
#for var, param in varMap.iteritems() :
#    print "\n\n <<==== %s   sum from below? %s ====>> " % (var, str(param[0]))
#    results.append( checkVarInRange( cnt, eTree, rTree, var, cut, targetPercent, param[0], param[1]) )
#
#print "Using Cut: %s" % cut
#for result in results :
#    print "Variable: %40s   Cut Postion: %.2f   Removes %.3f Signal and %.3f background" % (result[0], result[1], result[2], result[3])





