import ROOT
from ROOT import gStyle, gPad
import math
from drawRateEff import setLegStyle, drawCMSString
import CMS_lumi, tdrstyle
from efficiencyTrees import makeNewCutTrees
gStyle.SetOptStat(0)

canvasSize = 800

effFile = ROOT.TFile( 'egTriggerEff.root', 'r' )
rateFile = ROOT.TFile( 'egTriggerRates.root', 'r' )
eTree = effFile.Get("analyzer/crystal_tree")
rTree = rateFile.Get("analyzer/crystal_tree")


def tryCut( etree, rtree, var, cut, preCut="" ) :
    print "Var:",var
    print "Cut: ",cut
    print "PreCut: ",preCut
    for val in [0,10,20,30,40] :
        print " - Range: %i - %i" % (val, val+10)
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
        print " - Cuts out: %8i / %8i = %8f" % ((eVal2-eVal),eVal2,((eVal2-eVal)/eVal2))
        print " - Cuts out: %8i / %8i = %8f" % ((rVal2-rVal),rVal2,((rVal2-rVal)/rVal2))
        del h1,h1_2,h2,h2_2
    print "\n"


def makeRatePlot( rateFile, tree, name, cut='', rateLimit=90 ) :
    c = ROOT.TCanvas('c','c',canvasSize,canvasSize)
    
    h1 = ROOT.TH1F('h1', name,rateLimit,0,rateLimit)
    tree.Draw('cluster_pt >> h1', cut)
    h2 = ROOT.TH1F('h2'+name, name,rateLimit,0,rateLimit)
    h2.Sumw2()
    
    for i in range(1, h1.GetNbinsX()+1) :
        h2.SetBinContent( i, h1.Integral( i, rateLimit ) )
        h2.SetBinError( i, math.sqrt(h2.GetBinContent( i )) )
    
    # Normalize to 30 MHz
    nEvents = rateFile.Get("analyzer/eventCount").GetBinContent(1)
    #print "n events scanned %i,   events in tree %i" % (nEvents, tree.GetEntries())
    factor = 30000. / nEvents
    #print "factor",factor
    #factor = 30000. / tree.GetEntries()
    h2.Scale( factor )
    #print "Bin cont bin 1",h2.GetBinContent(1)
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
    colors = [ROOT.kBlack, ROOT.kRed, ROOT.kBlue, ROOT.kGreen, ROOT.kOrange, ROOT.kGray, ROOT.kCyan, ROOT.kYellow, ROOT.kPink]
    c = ROOT.TCanvas('c','c',canvasSize,canvasSize)
    c.SetLogy()
    c.SetGrid()
    if len(hists) > 5 : yStart = 0.60
    else : 0.78
    leg = setLegStyle(0.53,yStart,0.95,0.92)
    leg.SetFillStyle(1001)
    leg.SetFillColor(ROOT.kWhite)

    max_ = 0.
    for i, h in enumerate(hists) :
        if h.GetBinContent(1) > max_ : max_ = h.GetBinContent(1)
        h.SetLineColor( colors[i] )
        h.Draw('SAME')
        leg.AddEntry(h, h.GetTitle(),"lpe")

    print "max",max_
    hists[0].SetMaximum( max_ * 2. )
    leg.Draw("same")
    cms = drawCMSString("CMS Simulation, <PU>=140 bx=25, Minimum-Bias")
    c.Update()

    c.Print('plotsOpt/rates_'+name+'.png')    
    del c
    
def makeEffPlot( ntree, otree, name, cut='', effLimit=50 ) :
    binSize = 5
    c = ROOT.TCanvas('c','c',canvasSize,canvasSize)
    p = ROOT.TPad('p','p',0,0,1,1)
    p.Draw()
    
    denom = ROOT.TH1F('denom'+name, name,int(effLimit/binSize),0,effLimit)
    otree.Draw('gen_pt >> denom'+name)
    neum = ROOT.TH1F('neum'+name, name,int(effLimit/binSize),0,effLimit)
    ntree.Draw('gen_pt >> neum'+name, cut)
    graph = ROOT.TGraphAsymmErrors(neum, denom)
    graph.SetMarkerSize(0)
    graph.SetLineWidth(2)
    
    graph.Draw()
    graph.GetYaxis().SetTitle('Eff. (L1 / Gen)')
    graph.GetXaxis().SetTitle('Gen P_{T}')
    #c.Print('plotsOpt/eff_'+name+'.png')    
    del denom, neum
    del c,p
    return graph

def plotEffHists( name, graphs=[], nCol = 1 ) :
    colors = [ROOT.kBlack, ROOT.kRed, ROOT.kBlue, ROOT.kGreen, ROOT.kOrange, ROOT.kGray, ROOT.kCyan, ROOT.kYellow, ROOT.kPink]
    c = ROOT.TCanvas('c','c',canvasSize,canvasSize)
    c.SetTitle( name )
    c.SetGrid()
    leg = setLegStyle(0.53,0.78,0.95,0.92)
    leg.SetNColumns(nCol)


    mg = ROOT.TMultiGraph("mg", c.GetTitle())
    #graphs[0].GetXaxis().SetTitle("Gen P_{T}")
    #graphs[0].GetYaxis().SetTitle("Eff. (L1/offline)")
    for i, g in enumerate(graphs) :
        g.SetLineColor( colors[int(math.floor(i/2.))] )
        g.SetMarkerStyle(20)
        if i%2==0: g.SetLineStyle(2)
        else: g.SetLineStyle(1)
        g.SetMarkerColor( colors[int(math.floor(i/2.))] )
        mg.Add( g )
        leg.AddEntry(g, g.GetTitle(),"lpe")

    mg.Draw("aplez")
    mg.GetXaxis().SetTitle("Gen P_{T}")
    mg.GetYaxis().SetTitle("Eff. (L1/offline)")
    mg.SetMaximum( 1.3 )
    leg.Draw("same")
    cms = drawCMSString("CMS Simulation, <PU>=140 bx=25, Single Electron")
    c.Update()
    c.Print('plotsOpt/effs_'+name+'.png')    
    del c


def makeComparisons( Cut, name ) :
    oldRateFile = ROOT.TFile('egTriggerRates.root','r')
    oldRateTrackFile = ROOT.TFile('egTriggerRateTracks.root','r')
    oldRateTree = oldRateFile.Get('analyzer/crystal_tree')
    oldEffFile = ROOT.TFile('egTriggerEff.root','r')
    oldEffTree = oldEffFile.Get('analyzer/crystal_tree')
    # With the porposed cut, make a new cut tree, then sort
    # to ensure that only 1 cluster per event
    makeNewCutTrees( 'egTriggerEff.root', 'effTree.root', Cut )
    makeNewCutTrees( 'egTriggerRates.root', 'rateTree.root', Cut )
    makeNewCutTrees( 'egTriggerRateTracks.root', 'rateTreeTracks.root', 'trackPt > 10' )
    #fillUniqueEvents( 'rateTree.root', 'rateTreeUnique.root' )
    #fillUniqueEvents( 'effTree.root', 'effTreeUnique.root' )
    #fillUniqueEvents( 'rateTreeTracks.root', 'rateTreeTracksUnique.root' )
    # Grab the new trees with a single cluster / event
    effFile = ROOT.TFile( 'effTree.root', 'r' )
    eTree = effFile.Get("events")
    newRateFile = ROOT.TFile('rateTree.root','r')
    rTree = newRateFile.Get("events")
    newRateFileTracks = ROOT.TFile('rateTreeTracks.root','r')
    rTreeTracks = newRateFileTracks.Get("events")

    # Additional pt cuts
    pt16 = "*(cluster_pt > 16)"
    pt20 = "*(cluster_pt > 20)"
    pt30 = "*(cluster_pt > 30)"

    rTracks10 = makeRatePlot( oldRateTrackFile, rTreeTracks, "tracks p_{T}>10 GeV", "trackPt>10" )
    rTracks15 = makeRatePlot( oldRateTrackFile, rTreeTracks, "tracks p_{T}>15 GeV", "trackPt>15" )
    rTracks10eg = makeRatePlot( oldRateFile, oldRateTree, "tracks p_{T}>10 GeV - EG Matched", "trackPt>10" )
    rTracks15eg = makeRatePlot( oldRateFile, oldRateTree, "tracks p_{T}>15 GeV - EG Matched", "trackPt>15" )
    noCuts = makeRatePlot( oldRateFile, oldRateTree, "Raw Rate - No Cuts", "" )
    r5 = makeRatePlot( oldRateFile, rTree, name, Cut )
    #r5_16 = makeRatePlot( oldRateFile, rTree, name+"_16", Cut+pt16 )
    r5_20 = makeRatePlot( oldRateFile, rTree, name+"_20", Cut+pt20 )
    r5_30 = makeRatePlot( oldRateFile, rTree, name+"_30", Cut+pt30 )
    rTDR = oldRateFile.Get('analyzer/l1extraParticlesUCT:All_rate')
    rTDR.SetTitle('RCT 2015')
    plotRateHists(  name+"_raw_track_rate", [rTDR, noCuts, rTracks10, rTracks15, rTracks10eg, rTracks15eg] )
    plotRateHists(  name+"_turnons16_20_30", [rTDR, noCuts, rTracks10eg, rTracks15eg, r5, r5_20, r5_30] )
    #plotRateHists(  name+"_turnons16_20_30", [rTDR, noCuts, rTracks10, rTracks15, rTracks10eg, rTracks15eg, r5, r5_20, r5_30] )

    e5 = makeEffPlot( eTree, oldEffTree, name, Cut )
    #e5_16 = makeEffPlot( eTree, oldEffTree, name+"_16", Cut+pt16 )
    e5_20 = makeEffPlot( eTree, oldEffTree, name+"_20", Cut+pt20 )
    e5_30 = makeEffPlot( eTree, oldEffTree, name+"_30", Cut+pt30 )
    neum = oldEffFile.Get('analyzer/l1extraParticlesUCT:All_efficiency_pt')
    #neum16 = oldEffFile.Get('analyzer/l1extraParticlesUCT:All_threshold16_efficiency_gen_pt')
    neum20 = oldEffFile.Get('analyzer/l1extraParticlesUCT:All_threshold20_efficiency_gen_pt')
    neum30 = oldEffFile.Get('analyzer/l1extraParticlesUCT:All_threshold30_efficiency_gen_pt')
    denom = oldEffFile.Get('analyzer/gen_pt')
    # Bin width currently set at .83333 in these hists...
    #for h in [denom, neum, neum16, neum20, neum30] :
    for h in [denom, neum, neum20, neum30] :
        h.Rebin(6) 
    eTDRall = ROOT.TGraphAsymmErrors( neum, denom )
    #eTDR16 = ROOT.TGraphAsymmErrors( neum16, denom )
    eTDR20 = ROOT.TGraphAsymmErrors( neum20, denom )
    eTDR30 = ROOT.TGraphAsymmErrors( neum30, denom )
    eTDRall.SetTitle('RCT 2015: all')
    #eTDR16.SetTitle('RCT 2015: pt 16')
    eTDR20.SetTitle('RCT 2015: pt 20')
    eTDR30.SetTitle('RCT 2015: pt 30')
    #graphs = [eTDRall, e5, eTDR16, e5_16, eTDR20, e5_20, eTDR30, e5_30] 
    graphs = [eTDRall, e5, eTDR20, e5_20, eTDR30, e5_30] 
    #plotEffHists(  name+"_turnons16_20_30", [eTDRall, e5, eTDR16, e5_16, eTDR20, e5_20, eTDR30, e5_30], 2 )
    plotEffHists(  name+"_turnons16_20_30", graphs, 2 )


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


if __name__ == '__main__' :

    cnt = 0
    
    tdrstyle.setTDRStyle()
    c = ROOT.TCanvas('c','c',canvasSize,canvasSize)
    #### H/E - June 18 morning
    ###tryCut( eTree, rTree, "cluster_pt", "(0.430519 + 2.92122*TMath::Exp(-0.130031 * cluster_pt)>cluster_hovere )")
    #### Iso - June 18 morning
    ###tryCut( eTree, rTree, "cluster_pt", "(1.27405 + 6.25368*TMath::Exp(-0.0747614 * cluster_pt)>cluster_iso )")
    #### E2x5/E5x5 - June 18 morning
    ###tryCut( eTree, rTree, "cluster_pt", "(-0.893248 + 0.187355*TMath::Exp(-0.069526 * cluster_pt)>((-1)*e2x5/e5x5) )")
    # E2x5/E5x5 - June 18 morning
    showerShape = "(-0.892035+ 0.240369*TMath::Exp(-0.0791789 * cluster_pt)>((-1)*e2x5/e5x5) )"
    showerShape2 = "(-0.94097+ 0.208548*TMath::Exp(-0.0383287 * cluster_pt)>((-1)*e2x5/e5x5) )" # Aggressive cuts
##    tryCut( eTree, rTree, "cluster_pt", showerShape)
##    tryCut( eTree, rTree, "cluster_pt", showerShape2)
    # H/E - June 18 morning
    hovere = "(0.430149 +3.28952*TMath::Exp(-0.128499 * cluster_pt)>cluster_hovere )"
##    tryCut( eTree, rTree, "cluster_pt", hovere+"*"+showerShape, showerShape)
    # Iso - June 18 morning
    iso = "(1.22987+ 7.24192*TMath::Exp(-0.0760816 * cluster_pt)>cluster_iso )"
##    tryCut( eTree, rTree, "cluster_pt", iso+"*"+showerShape+"*"+hovere, showerShape+"*"+hovere)
##    tryCut( eTree, rTree, "cluster_pt", iso+"*"+showerShape+"*"+hovere)
    cut19 = iso+"*"+showerShape+"*"+hovere

    #trackPt = "(15+cluster_pt*2) > trackPt"
    #tryCut( eTree, rTree, "cluster_pt", trackPt)
    trackRInv = "(((0.0044272 + -0.00673545*TMath::Exp( -0.192441 * cluster_pt))>abs(trackRInv)) || cluster_pt > 15)"
#    tryCut( eTree, rTree, "cluster_pt", trackRInv+"*"+cut19, cut19)
    trackIso = "((trackIsoConePtSum / trackPt) < 2.)"
#    tryCut( eTree, rTree, "cluster_pt", trackIso+"*"+cut19, cut19)
    trackRInvPtRes = "((abs(trackRInv)<0.0035 && ((trackPt-cluster_pt)/trackPt)>-4.5))"
#    tryCut( eTree, rTree, "cluster_pt", trackRInvPtRes)
#    tryCut( eTree, rTree, "cluster_pt", trackRInvPtRes+"*"+cut19, cut19)

    cut20 = cut19+"*"+trackRInv
    cut21 = cut19+"*"+trackIso

    #trackNum5 = "(trackIsoConeTrackCount<5)"
    #tryCut( eTree, rTree, "cluster_pt", trackNum5)
    #trackNum4 = "(trackIsoConeTrackCount<4)"
    #tryCut( eTree, rTree, "cluster_pt", trackNum4)
    trackNum3 = "(trackIsoConeTrackCount<3)"
    #tryCut( eTree, rTree, "cluster_pt", trackNum3)
    #trackIso2 = "(trackIsoConePtSum/trackPt<2)"
    #tryCut( eTree, rTree, "cluster_pt", trackIso2)
    #trackIso1 = "(trackIsoConePtSum/trackPt<1)"
    #tryCut( eTree, rTree, "cluster_pt", trackIso1)
    trackIso = "(trackIsoConePtSum/trackPt<((1.5/50.)*cluster_pt))"
    trackIsoX = "((0.0642778 + 0.0185707*cluster_pt)> (trackIsoConePtSum/trackPt))"
    #tryCut( eTree, rTree, "cluster_pt", trackIsoX)
    bremChi2 = "( (0.85-(0.15/50.)*trackChi2)<bremStrength )"
    #tryCut( eTree, rTree, "cluster_pt", bremChi2)
    bremChi2_2 = "( (0.75-(0.15/50.)*trackChi2)<bremStrength )"
    #tryCut( eTree, rTree, "cluster_pt", bremChi2_2)
    bremChi2_3 = "( (0.75-(0.25/50.)*trackChi2)<bremStrength )"
    #tryCut( eTree, rTree, "cluster_pt", bremChi2_3)
    #bremChi2_4 = "( (-0.649285 + -0.319116*TMath::Exp(-0.0772114*trackChi2))>(-1)*bremStrength )"
    #bremChi2_4 = "( (-0.586479 + -0.32731*TMath::Exp(-0.0396343*trackChi2))>(-1)*bremStrength )"
    bremChi2_4 = "( (-0.593921 + -0.170821*TMath::Exp(-0.0606166*trackChi2))>(-1)*bremStrength )" # .975 all chi2
    #tryCut( eTree, rTree, "cluster_pt", bremChi2_4)

    cut23 = cut19+"*"+trackNum3+"*"+trackIso
    cut24 = cut19+"*"+trackNum3+"*"+trackIso+"*"+bremChi2_3
    cut25 = cut19+"*"+trackNum3+"*"+trackIsoX+"*"+bremChi2_4



    cut18 = "(((0.415233 + 1.51272 * TMath::Exp(-0.10266*cluster_pt)) > cluster_hovere) && ((1.08154 + 4.28457 *TMath::Exp(-0.0556304*cluster_pt)) > cluster_iso))"
    cut18 += "*(( cluster_pt>25 || (trackDeltaR < 0.35)*(abs(trackDeltaPhi)<.3)*(abs(trackDeltaEta)<.3)*(((trackPt - cluster_pt)/trackPt)>-2)))"
    cut18 += "*( (-0.474475 + cluster_pt*-0.00613679) < bremStrength )"
    cut18 += "*(trackIsoConeTrackCount < 7)"
    cut18 += "*( (-0.909573 + 0.145691 * TMath::Exp( -0.0403391 * cluster_pt)) > (-1)*(e2x5/e5x5))"

    cut22 = cut18+"*"+trackIso

#makeComparisons( cut17, "cut17" )
#makeComparisons( cut16, "cut16" )
#makeComparisons( cut15, "cut15" )
#makeComparisons( cut9, "cut9" )
#makeComparisons( cut7, "cut8" )
#makeComparisons( cut10, "cut10" )
#makeComparisons( cut18, "cut18" )
#makeComparisons( cut19, "cut19" )
#makeComparisons( cut20, "cut20" )
#makeComparisons( cut22, "cut22" )
#makeComparisons( cut23, "cut23" )
#makeComparisons( cut24, "cut24" )
#makeComparisons( "(1)", "NoCuts" )
##tryCut( eTree, rTree, "cluster_pt", cut23, cut19)
showerShapes = "(-0.921128 + 0.180511*TMath::Exp(-0.0400725*cluster_pt)>(-1)*(e2x5/e5x5))"
#tryCut( eTree, rTree, "cluster_pt", showerShapes, "")
makeComparisons( showerShapes, "e2x5Overe5x5" )
Isolation = "((0.990748 + 5.64259*TMath::Exp(-0.0613952*cluster_pt))>cluster_iso)"
#tryCut( eTree, rTree, "cluster_pt", Isolation+"*"+showerShapes, showerShapes)
makeComparisons( Isolation+"*"+showerShapes, "e2x5Overe5x5_Iso" )
hovere = "((0.40633 + 2.17848*TMath::Exp(-0.114384*cluster_pt))>cluster_hovere)"
prevcut = showerShapes+"*"+Isolation
cut = showerShapes+"*"+Isolation+"*"+hovere
#tryCut( eTree, rTree, "cluster_pt", cut, prevcut)
makeComparisons( cut, "e2x5Overe5x5_Iso_HoE" )
trackIso = "((0.0947627 + 0.0135767*cluster_pt) > (trackIsoConePtSum/trackPt))"
trackIso2 = "((0.130534 + 0.0131326*cluster_pt) > (trackIsoConePtSum/trackPt))"
cut = showerShapes+"*"+Isolation+"*"+trackIso
cut2 = showerShapes+"*"+Isolation+"*"+trackIso2
#tryCut( eTree, rTree, "cluster_pt", cut, prevcut)
#tryCut( eTree, rTree, "cluster_pt", cut2, prevcut)
makeComparisons( cut2, "e2x5Overe5x5_Iso_TrkIso" )
hovere = "((0.426413 +2.62318 *TMath::Exp(-0.105685*cluster_pt))>cluster_hovere)"
prevcut = cut2 
cut2 += "*"+hovere
tryCut( eTree, rTree, "cluster_pt", cut2, prevcut)
makeComparisons( cut2, "e2x5Overe5x5_Iso_TrkIso_HoE" )
###bremTkChi2 = "((-0.622523 + -0.171795*TMath::Exp(-0.097391*trackChi2))>(-1)*bremStrength)"
###prevcut = cut2 
###cut2 += "*"+bremTkChi2
###tryCut( eTree, rTree, "cluster_pt", cut2, prevcut)



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





