import ROOT
from ROOT import gStyle, gPad
import math
from drawRateEff import setLegStyle
import CMS_lumi, tdrstyle
gStyle.SetOptStat(0)

canvasSize = 800

effFile = ROOT.TFile( 'egTriggerEff.root', 'r' )
rateFile = ROOT.TFile( 'egTriggerRates.root', 'r' )
eTree = effFile.Get("analyzer/crystal_tree")
rTree = rateFile.Get("analyzer/crystal_tree")


def tryCut( etree, rtree, var, cut, preCut="" ) :
    print "Var:",var," Cut: ",cut," PreCut: ",preCut
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
    colors = [ROOT.kBlack, ROOT.kRed, ROOT.kBlue, ROOT.kGreen, ROOT.kOrange, ROOT.kGray, ROOT.kCyan, ROOT.kYellow]
    c = ROOT.TCanvas('c','c',canvasSize,canvasSize)
    c.SetLogy()
    c.SetGrid()
    leg = setLegStyle(0.53,0.78,0.95,0.92)

    max_ = 0.
    for i, h in enumerate(hists) :
        if h.GetBinContent(1) > max_ : max_ = h.GetBinContent(1)
        h.SetLineColor( colors[i] )
        h.Draw('SAME')
        leg.AddEntry(h, h.GetTitle(),"lpe")

    print "max",max_
    hists[0].SetMaximum( max_ * 2. )
    leg.Draw("same")
    c.Update()

    c.Print('plotsOpt/rates_'+name+'.png')    
    del c
    
def makeEffPlot( tree, name, cut='', effLimit=50 ) :
    binSize = 5
    c = ROOT.TCanvas('c','c',canvasSize,canvasSize)
    p = ROOT.TPad('p','p',0,0,1,1)
    p.Draw()
    
    denom = ROOT.TH1F('denom'+name, name,int(effLimit/binSize),0,effLimit)
    tree.Draw('gen_pt >> denom'+name)
    neum = ROOT.TH1F('neum'+name, name,int(effLimit/binSize),0,effLimit)
    tree.Draw('gen_pt >> neum'+name, cut)
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
    colors = [ROOT.kBlack, ROOT.kRed, ROOT.kBlue, ROOT.kGreen, ROOT.kOrange, ROOT.kGray, ROOT.kCyan, ROOT.kYellow]
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
    c.Update()
    c.Print('plotsOpt/effs_'+name+'.png')    
    del c


def makeComparisons( Cut, name ) :
    # Additional pt cuts
    pt16 = "*(cluster_pt > 16)"
    pt20 = "*(cluster_pt > 20)"
    pt30 = "*(cluster_pt > 30)"

    r5 = makeRatePlot( rateFile, rTree, name, Cut )
    r5_16 = makeRatePlot( rateFile, rTree, name+"_16", Cut+pt16 )
    r5_20 = makeRatePlot( rateFile, rTree, name+"_20", Cut+pt20 )
    r5_30 = makeRatePlot( rateFile, rTree, name+"_30", Cut+pt30 )
    rTDR = rateFile.Get('analyzer/l1extraParticlesUCT:All_rate')
    rTDR.SetTitle('RCT 2015')
    plotRateHists(  name+"_turnons16_20_30", [rTDR, r0, r5, r5_16, r5_20, r5_30] )


    effFile = ROOT.TFile( 'egTriggerEff.root', 'r' )
    eTree = effFile.Get("analyzer/crystal_tree")
    e5 = makeEffPlot( eTree, name, Cut )
    e5_16 = makeEffPlot( eTree, name+"_16", Cut+pt16 )
    e5_20 = makeEffPlot( eTree, name+"_20", Cut+pt20 )
    e5_30 = makeEffPlot( eTree, name+"_30", Cut+pt30 )
    neum = effFile.Get('analyzer/l1extraParticlesUCT:All_efficiency_pt')
    neum16 = effFile.Get('analyzer/l1extraParticlesUCT:All_threshold16_efficiency_gen_pt')
    neum20 = effFile.Get('analyzer/l1extraParticlesUCT:All_threshold20_efficiency_gen_pt')
    neum30 = effFile.Get('analyzer/l1extraParticlesUCT:All_threshold30_efficiency_gen_pt')
    denom = effFile.Get('analyzer/gen_pt')
    # Bin width currently set at .83333 in these hists...
    for h in [denom, neum, neum16, neum20, neum30] :
        h.Rebin(6) 
    eTDRall = ROOT.TGraphAsymmErrors( neum, denom )
    eTDR16 = ROOT.TGraphAsymmErrors( neum16, denom )
    eTDR20 = ROOT.TGraphAsymmErrors( neum20, denom )
    eTDR30 = ROOT.TGraphAsymmErrors( neum30, denom )
    eTDRall.SetTitle('RCT 2015: all')
    eTDR16.SetTitle('RCT 2015: pt 16')
    eTDR20.SetTitle('RCT 2015: pt 20')
    eTDR30.SetTitle('RCT 2015: pt 30')
    graphs = [eTDRall, e5, eTDR16, e5_16, eTDR20, e5_20, eTDR30, e5_30] 
    plotEffHists(  name+"_turnons16_20_30", [eTDRall, e5, eTDR16, e5_16, eTDR20, e5_20, eTDR30, e5_30], 2 )


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

    cut10 = "( ( (cluster_pt < 20)"
    cut10 += "*(cluster_iso < 5.68)"
    cut10 += "*(cluster_hovere < 1.63)"
    cut10 += "*(cluster_iso < 4.93)"
    cut10 += "*(abs(trackDeltaEta) < 0.02)"
    cut10 += "*(((trackPt-cluster_pt)/trackPt) > -1.01) )"
    
    cut10 += "|| ( (cluster_pt > 20 && cluster_pt < 25)"
    cut10 += "*(cluster_hovere < 0.76)"
    cut10 += "*(cluster_iso < 3.33)"
    cut10 += "*(abs(trackDeltaPhi) < 0.19) )"
    
    cut10 += "|| ( (cluster_pt > 25 && cluster_pt < 30)"
    cut10 += "*(cluster_hovere < 0.67)" #.01 v 0.32
    cut10 += "*(cluster_iso < 2.62)" # .01 v .13
    cut10 += "*(cluster_iso < 2.28)" # .01 v .07
    cut10 += "*(((trackPt-cluster_pt)/trackPt) > -9.21)" #.01 v .030
    cut10 += "*(((trackPt-cluster_pt)/trackPt) > -7.26) )" #.01 v .107
    
    cut10 += "|| ( (cluster_pt > 30 && cluster_pt < 35)"
    cut10 += "*(((trackPt-cluster_pt)/trackPt) > -9.28)" #.005 v .020
    cut10 += "*(((trackPt-cluster_pt)/trackPt) > -8.27)" #.005 v .045
    cut10 += "*(cluster_hovere < 0.61)" #.005 v 0.41
    cut10 += "*(((trackPt-cluster_pt)/trackPt) > -6.29)" #.005 v .139 (197 for iso)
    cut10 += "*(cluster_iso < 2.55)" # .005 v .169
    cut10 += "*(abs(trackDeltaEta) < 0.08)" # .005 v .143
    cut10 += "*(abs(trackDeltaEta) < 0.04) )" # .005 v .169
    
    cut10 += "|| ( (cluster_pt > 35)"
    cut10 += "*(cluster_hovere < 0.50)" #.005 v 0.433
    cut10 += "*(cluster_iso < 1.82)" # .005 v .111
    cut10 += "*(cluster_iso < 1.75)" # .005 v .094
    cut10 += "*(abs(trackDeltaPhi) < 0.13) ) )" # .005 v .350
    #cut10 += "*(((trackPt-cluster_pt)/trackPt) > -8.19) ) )" #.005 v .042
    #cut10 += "*(((trackPt-cluster_pt)/trackPt) > -6.61)" #.005 v .130
    #cut10 += "*(abs(trackDeltaPhi) < 0.08) ) )" # .005 v .350
    

    cnt = 0
    
    tdrstyle.setTDRStyle()
    c = ROOT.TCanvas('c','c',canvasSize,canvasSize)
    # H/E - June 18 morning
    tryCut( eTree, rTree, "cluster_pt", "(0.430519 + 2.92122*TMath::Exp(-0.130031 * cluster_pt)>cluster_hovere )")
    # Iso - June 18 morning
    tryCut( eTree, rTree, "cluster_pt", "(1.27405 + 6.25368*TMath::Exp(-0.0747614 * cluster_pt)>cluster_iso )")
    # H/E - June 18 morning
    tryCut( eTree, rTree, "cluster_pt", "(-0.893248 + 0.187355*TMath::Exp(-0.069526 * cluster_pt)>((-1)*e2x5/e5x5) )")


    # New Rate and Efficiency plots
    rateFile = ROOT.TFile( 'egTriggerRates.root', 'r' )
    rTree = rateFile.Get("analyzer/crystal_tree")
    cut0 = ""
    r0 = makeRatePlot( rateFile, rTree, "cut0", cut0 )
    cut1 = "((cluster_iso<2 && abs(trackDeltaPhi)<0.02) || cluster_pt > 20)"
    r1 = makeRatePlot( rateFile, rTree, "cut1", cut1 )

    cut7 = "("
    cut7 += "( cluster_pt < 15 && cluster_iso<3 && trackDeltaPhi>-0.03 && trackDeltaPhi<0.05 && abs(trackDeltaEta)<0.02 && ((trackPt - cluster_pt)/trackPt)>-1 )"
    cut7 += " || ( cluster_pt > 15 && cluster_pt < 22.5 && abs(trackDeltaEta)<0.02 && cluster_hovere < 1.5 && cluster_iso<3.5 && ((trackPt - cluster_pt)/trackPt)>-4 )" 
    cut7 += " || ( cluster_pt > 22.5 && cluster_pt < 30 && cluster_hovere < 1.5 && cluster_iso<3. && ((trackPt - cluster_pt)/trackPt)>-3 )" 
    cut7 += " || ( cluster_pt > 30 && cluster_hovere < 1.5 && cluster_iso < 2. && (cluster_pt + 10.) > trackPt ) )"
    cut9 = "( cluster_hovere < .5 && cluster_iso < 1.75)"# && ((trackPt - cluster_pt)/trackPt)>-10. )"
    #f1 = ROOT.TF1( 'f1', '([0] + [1]*TMath::Exp(-[2]*x))', mini, maxi)
    cut11 = "(((0.415233 + 1.51272 * TMath::Exp(-0.10266*cluster_pt)) > cluster_hovere) && ((1.08154 + 4.28457 *TMath::Exp(-0.0556304*cluster_pt)) > cluster_iso))"
    cut12 = "(((0.289155 + 1.53266 * TMath::Exp(-0.0808648*cluster_pt)) > cluster_hovere) && ((0.625032 + 4.76516 *TMath::Exp(-0.0493737*cluster_pt)) > cluster_iso))"
    cut13 = "(((0.415233 + 1.51272 * TMath::Exp(-0.10266*cluster_pt)) > cluster_hovere) && ((1.08154 + 4.28457 *TMath::Exp(-0.0556304*cluster_pt)) > cluster_iso))*(((trackPt-cluster_pt)/trackPt) > -8)"
    cut14 = "(((0.415233 + 1.51272 * TMath::Exp(-0.10266*cluster_pt)) > cluster_hovere) && ((1.08154 + 4.28457 *TMath::Exp(-0.0556304*cluster_pt)) > cluster_iso))"
    cut14 += "*(( cluster_pt>20 || (trackDeltaR < 0.35)*(abs(trackDeltaPhi)<.3)*(abs(trackDeltaEta)<.3)))"
    cut15 = "(((0.415233 + 1.51272 * TMath::Exp(-0.10266*cluster_pt)) > cluster_hovere) && ((1.08154 + 4.28457 *TMath::Exp(-0.0556304*cluster_pt)) > cluster_iso))"
    cut15 += "*(( cluster_pt>25 || (trackDeltaR < 0.35)*(abs(trackDeltaPhi)<.3)*(abs(trackDeltaEta)<.3)*(((trackPt - cluster_pt)/trackPt)>-2)))"
    cut15 += "*( (-0.474475 + cluster_pt*-0.00613679) < bremStrength )"

    cut16 = "(((0.415233 + 1.51272 * TMath::Exp(-0.10266*cluster_pt)) > cluster_hovere) && ((1.08154 + 4.28457 *TMath::Exp(-0.0556304*cluster_pt)) > cluster_iso))"
    cut16 += "*(( cluster_pt>25 || (trackDeltaR < 0.35)*(abs(trackDeltaPhi)<.3)*(abs(trackDeltaEta)<.3)*(((trackPt - cluster_pt)/trackPt)>-2)))"
    cut16 += "*( (-0.474475 + cluster_pt*-0.00613679) < bremStrength )"
    cut16 += "*(trackIsoConeTrackCount < 7)"

    # Track Pt based cuts only
    cut17 = "( (cluster_pt < 25 && (4.68705 + cluster_pt*1.51799)>trackPt)"
    cut17 += " || (cluster_pt >25 && (-4 + 0.308*cluster_pt)<trackPt))"

    cut18 = "(((0.415233 + 1.51272 * TMath::Exp(-0.10266*cluster_pt)) > cluster_hovere) && ((1.08154 + 4.28457 *TMath::Exp(-0.0556304*cluster_pt)) > cluster_iso))"
    cut18 += "*(( cluster_pt>25 || (trackDeltaR < 0.35)*(abs(trackDeltaPhi)<.3)*(abs(trackDeltaEta)<.3)*(((trackPt - cluster_pt)/trackPt)>-2)))"
    cut18 += "*( (-0.474475 + cluster_pt*-0.00613679) < bremStrength )"
    cut18 += "*(trackIsoConeTrackCount < 7)"
    cut18 += "*( (-0.909573 + 0.145691 * TMath::Exp( -0.0403391 * cluster_pt)) > (-1)*(e2x5/e5x5))"

#makeComparisons( cut17, "cut17" )
#makeComparisons( cut16, "cut16" )
#makeComparisons( cut15, "cut15" )
#makeComparisons( cut9, "cut9" )
#makeComparisons( cut7, "cut8" )
#makeComparisons( cut10, "cut10" )
#makeComparisons( cut18, "cut18" )


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





