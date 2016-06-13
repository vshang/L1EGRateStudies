import ROOT
from ROOT import gStyle
import math
from drawRateEff import setLegStyle
import CMS_lumi, tdrstyle
gStyle.SetOptStat(0)

canvasSize = 800

effFile = ROOT.TFile( 'egTriggerEff.root', 'r' )
rateFile = ROOT.TFile( 'egTriggerRates.root', 'r' )
eTree = effFile.Get("analyzer/crystal_tree")
rTree = rateFile.Get("analyzer/crystal_tree")

rInit = rTree.GetEntries()
eInit = eTree.GetEntries()

def tryCut( etree, einit, rtree, rinit, var, cut ) :
    h1 = ROOT.TH1F('h1','h1',100,0,200)
    etree.Draw( var + ' >> h1', cut )
    eVal = h1.Integral()
    h2 = ROOT.TH1F('h2','h2',100,0,200)
    rtree.Draw( var + ' >> h2', cut )
    rVal = h2.Integral()
    print "Var:",var," Cut: ",cut
    print " - Cuts out: %8i / %8i = %8f" % ((einit-eVal),einit,((einit-eVal)/einit))
    print " - Cuts out: %8i / %8i = %8f" % ((rinit-rVal),rinit,((rinit-rVal)/rinit))
    print "\n"
    del h1,h2


def makeRatePlot( rateFile, tree, name, cut='', rateLimit=90 ) :
    c = ROOT.TCanvas('c','c',canvasSize,canvasSize)
    
    h1 = ROOT.TH1F('h1', name,rateLimit,0,rateLimit)
    tree.Draw('cluster_pt >> h1', cut)
    h2 = ROOT.TH1F('h2'+name, name,rateLimit,0,rateLimit)
    h2.Sumw2()
    
    for i in range(1, h1.GetNbinsX()+1) :
        #print h1.Integral( i, rateLimit )
        h2.SetBinContent( i, h1.Integral( i, rateLimit ) )
        h2.SetBinError( i, math.sqrt(h2.GetBinContent( i )) )
    
    # Normalize to 30 MHz
    nEvents = rateFile.Get("analyzer/eventCount").GetBinContent(1)
    #factor = 30000. / tree.GetEntries()
    factor = 30000. / nEvents
    #print factor
    h2.Scale( factor )
    h2.SetMarkerSize(0)
    h2.SetLineWidth(2)
    
    h2.Draw()
    h2.GetYaxis().SetTitle('Rate (kHz)')
    h2.GetXaxis().SetTitle('L1 EG E_{T}')
    c.SetLogy()
    #c.Print('plotsOpt/rate_'+name+'.png')    
    del h1
    del c
    return h2

def plotRateHists( name, hists=[] ) :
    colors = [ROOT.kBlack, ROOT.kRed, ROOT.kBlue, ROOT.kGreen, ROOT.kOrange, ROOT.kGray, ROOT.kCyan, ROOT.kYellow]
    c = ROOT.TCanvas('c','c',canvasSize,canvasSize)
    c.SetLogy()
    c.SetGrid()
    leg = setLegStyle(0.53,0.78,0.95,0.92)

    for i, h in enumerate(hists) :
        h.SetLineColor( colors[i] )
        h.Draw('SAME')
        leg.AddEntry(h, h.GetTitle(),"lpe")

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
        if i%2==0: g.SetLineStyle(1)
        else: g.SetLineStyle(2)
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


if __name__ == '__main__' :
    hx = ROOT.TH2F('hx','hx',50,0,50,50,0,50)
    #hy = ROOT.TH1F('hy','hy',50,-1.,1.)
    eTree.Draw('trackPt:cluster_pt >> hx')
    hx.GetXaxis().SetTitle("cluster_pt (GeV)")
    hx.GetYaxis().SetTitle("trackPt (GeV)")
    c = ROOT.TCanvas('c','c',canvasSize,canvasSize)
    hx.Draw('COLZ')
    c.Print('plotsOpt/trackPtVclusterPt.png')    
    c.Clear()
    #eTree.Draw('((trackPt-cluster_pt)/trackPt) >> hy')
    #hy.Draw()
    #c.Print('plotsOpt/trackPtRes.png')    
    del c
    
    tdrstyle.setTDRStyle()
#    c = ROOT.TCanvas('c','c',canvasSize,canvasSize)
#    print "RATE: Starting quantity: ",rInit
#    print "EFF: Starting quantity: ",eInit
#    tryCut( eTree, eInit, rTree, rInit, "cluster_pt", "cluster_iso<5")
#    tryCut( eTree, eInit, rTree, rInit, "cluster_pt", "cluster_iso<4")
#    tryCut( eTree, eInit, rTree, rInit, "cluster_pt", "cluster_iso<3")
#    tryCut( eTree, eInit, rTree, rInit, "cluster_pt", "cluster_iso<2")
#
#    tryCut( eTree, eInit, rTree, rInit, "cluster_pt", "cluster_hovere < 1 || abs(trackDeltaPhi) < 0.05")
#    tryCut( eTree, eInit, rTree, rInit, "cluster_pt", "abs(trackDeltaEta)<0.03")
#    tryCut( eTree, eInit, rTree, rInit, "cluster_pt", "abs(trackDeltaPhi)<0.05")
#    tryCut( eTree, eInit, rTree, rInit, "cluster_pt", "abs(trackDeltaEta)<0.03 && abs(trackDeltaPhi)<0.05")
#
#
#    print "Now with pt rescue above 20 GeV"
#    tryCut( eTree, eInit, rTree, rInit, "cluster_pt", "abs(trackDeltaPhi)<0.05 || cluster_pt > 20")
#    tryCut( eTree, eInit, rTree, rInit, "cluster_pt", "abs(trackDeltaEta)<0.03 || cluster    _pt > 20")
#    tryCut( eTree, eInit, rTree, rInit, "cluster_pt", "(abs(trackDeltaEta)<0.03 && abs(trackDeltaPhi)<0.05) || cluster    _pt > 20")
#
#
#    print "Iso work"
#    tryCut( eTree, eInit, rTree, rInit, "cluster_pt", "cluster_iso<2")
#    tryCut( eTree, eInit, rTree, rInit, "cluster_pt", "cluster_iso < 2 || cluster_pt > 20")
#    tryCut( eTree, eInit, rTree, rInit, "cluster_pt", "cluster_iso<2 && abs(trackDeltaPhi)<0.02")
#    # Cut1 for plots
#    tryCut( eTree, eInit, rTree, rInit, "cluster_pt", "((cluster_iso<2 && abs(trackDeltaPhi)<0.02) || cluster_pt > 20)")
#    # Cut2 for plots
#    tryCut( eTree, eInit, rTree, rInit, "cluster_pt", "((cluster_iso<2 && abs(trackDeltaPhi)<0.02 && abs(trackDeltaEta)<0.015) || (cluster_pt > 20 && abs(trackDeltaEta)<0.015) || cluster_pt > 30)")
##    tryCut( eTree, eInit, rTree, rInit, "cluster_pt", "(cluster_iso<3 && abs(trackDeltaPhi)<0.04 && cluster_pt < 10) || (cluster_iso<2 && abs(trackDeltaPhi)<0.02) || cluster_pt > 20")


    # New Rate and Efficiency plots
    rateFile = ROOT.TFile( 'egTriggerRates.root', 'r' )
    rTree = rateFile.Get("analyzer/crystal_tree")
    cut0 = ""
    r0 = makeRatePlot( rateFile, rTree, "cut0", cut0 )
    cut1 = "((cluster_iso<2 && abs(trackDeltaPhi)<0.02) || cluster_pt > 20)"
    r1 = makeRatePlot( rateFile, rTree, "cut1", cut1 )
    cut2 = "((cluster_iso<2 && abs(trackDeltaPhi)<0.02 && abs(trackDeltaEta)<0.015) || (cluster_pt > 20 && abs(trackDeltaEta)<0.015) || cluster_pt > 30)"
    cut3 = "( cluster_iso<6 && trackDeltaPhi>-0.03 && trackDeltaPhi<0.05 && abs(trackDeltaEta)<0.02 && ((trackPt - cluster_pt)/trackPt)>-2 )"
    #cut4 = "(  ( cluster_iso<6 && trackDeltaPhi>-0.03 && trackDeltaPhi<0.05 && abs(trackDeltaEta)<0.02 && ((trackPt - cluster_pt)/trackPt)>-1 ) || ( abs(trackDeltaEta)<0.03 && abs(trackDeltaPhi)<0.1 && cluster_iso < 2. && cluster_pt > 30  ) )"
    cut4 = "(  ( cluster_iso<6 && trackDeltaPhi>-0.03 && trackDeltaPhi<0.05 && abs(trackDeltaEta)<0.02 && ((trackPt - cluster_pt)/trackPt)>-1 ) || ( cluster_hovere < 1.5 && cluster_iso < 2. && cluster_pt > 30  ) )"
#    cut5 = "(  ( cluster_iso<4 && trackDeltaPhi>-0.03 && trackDeltaPhi<0.05 && abs(trackDeltaEta)<0.02 && ((trackPt - cluster_pt)/trackPt)>-1 ) || ( cluster_hovere < 1.5 && cluster_iso < 2. && cluster_pt > 30  ) )"
    cut5 = "(  ( cluster_iso<4 && trackDeltaPhi>-0.03 && trackDeltaPhi<0.05 && abs(trackDeltaEta)<0.02 && ((trackPt - cluster_pt)/trackPt)>-1 ) || ( cluster_hovere < 1.5 && cluster_iso<3.5 && ((trackPt - cluster_pt)/trackPt)>-4 && cluster_pt > 15 ) || ( cluster_hovere < 1.5 && cluster_iso < 2. && cluster_pt > 30  ) )"
    cut6 = "*( (cluster_pt + 10.) > trackPt)"

    # Additional pt cuts
    pt16 = "*(cluster_pt > 16)"
    pt20 = "*(cluster_pt > 20)"
    pt30 = "*(cluster_pt > 30)"

    r2 = makeRatePlot( rateFile, rTree, "cut2", cut2 )
    r3 = makeRatePlot( rateFile, rTree, "cut3", cut3 )
    r4 = makeRatePlot( rateFile, rTree, "cut4", cut4 )
    r5 = makeRatePlot( rateFile, rTree, "cut5", cut5 )
    r5_16 = makeRatePlot( rateFile, rTree, "cut5_16", cut5+pt16 )
    r5_20 = makeRatePlot( rateFile, rTree, "cut5_20", cut5+pt20 )
    r5_30 = makeRatePlot( rateFile, rTree, "cut5_30", cut5+pt30 )
    rTDR = rateFile.Get('analyzer/l1extraParticlesUCT:All_rate')
    rTDR.SetTitle('RCT 2015')
    #plotRateHists(  "NoCut_cut1_cut2", [rTDR, r0, r1, r2, r3, r4, r5] )
    plotRateHists(  "NoCut_cut1_cut2", [rTDR, r0, r2, r4, r5] )
    plotRateHists(  "Cut5_with_turnons16_20_30", [rTDR, r0, r5, r5_16, r5_20, r5_30] )

    effFile = ROOT.TFile( 'egTriggerEff.root', 'r' )
    eTree = effFile.Get("analyzer/crystal_tree")
    e0 = makeEffPlot( eTree, "cut1", "" )
    e1 = makeEffPlot( eTree, "cut1", cut1 )
    e2 = makeEffPlot( eTree, "cut2", cut2 )
    e3 = makeEffPlot( eTree, "cut3", cut3 )
    e4 = makeEffPlot( eTree, "cut4", cut4 )
    e5 = makeEffPlot( eTree, "cut5", cut5 )
    e5_16 = makeEffPlot( eTree, "cut5_16", cut5+pt16 )
    e5_20 = makeEffPlot( eTree, "cut5_20", cut5+pt20 )
    e5_30 = makeEffPlot( eTree, "cut5_30", cut5+pt30 )
    #eTDR = effFile.Get('analyzer/divide_l1extraParticlesUCT:All_efficiency_pt_by_gen_pt')
    #eTDR.SetTitle('RCT 2015')
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
    #plotEffHists(  "NoCut_cut1_cut2", [eTDR, e0, e1, e2, e3, e4, e5] )
    #plotEffHists(  "NoCut_cut1_cut2", [eTDR, e0, e2, e4, e5] )
    graphs = [eTDRall, e5, eTDR16, e5_16, eTDR20, e5_20, eTDR30, e5_30] 
    plotEffHists(  "Cut5_with_turnons16_20_30", [eTDRall, e5, eTDR16, e5_16, eTDR20, e5_20, eTDR30, e5_30], 2 )

