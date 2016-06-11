import ROOT
import math



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


def makeRatePlot( tree, name, cut='', rateLimit=90 ) :
    c = ROOT.TCanvas('c','c',600,600)
    
    h1 = ROOT.TH1F('h1', name,rateLimit,0,rateLimit)
    tree.Draw('cluster_pt >> h1', cut)
    h2 = ROOT.TH1F('h2'+name, name,rateLimit,0,rateLimit)
    h2.Sumw2()
    
    for i in range(1, h1.GetNbinsX()+1) :
        #print h1.Integral( i, rateLimit )
        h2.SetBinContent( i, h1.Integral( i, rateLimit ) )
        h2.SetBinError( i, math.sqrt(h2.GetBinContent( i )) )
    
    # Normalize to 30 MHz
    factor = 30000. / tree.GetEntries()
    print factor
    h2.Scale( factor )
    
    h2.Draw()
    h2.GetYaxis().SetTitle('Rate (kHz)')
    h2.GetXaxis().SetTitle('L1 EG E_{T}')
    c.SetLogy()
    c.Print('plotsOpt/rate_'+name+'.png')    
    del h1
    del c
    return h2

def plotRateHists( name, hists=[] ) :
    c = ROOT.TCanvas('c','c',600,600)
    c.SetLogy()
    c.SetGrid()
    for h in hists :
        h.Draw('SAME')
    c.Print('plotsOpt/rates_'+name+'.png')    
    del c
    
def makeEffPlot( tree, name, cut='', effLimit=50 ) :
    c = ROOT.TCanvas('c','c',600,600)
    p = ROOT.TPad('p','p',0,0,1,1)
    p.Draw()
    
    denom = ROOT.TH1F('denom'+name, name,effLimit,0,effLimit)
    tree.Draw('gen_pt >> denom'+name)
    neum = ROOT.TH1F('neum'+name, name,effLimit,0,effLimit)
    tree.Draw('gen_pt >> neum'+name, cut)
    graph = ROOT.TGraphAsymmErrors(neum, denom)
    
    graph.Draw()
    graph.GetYaxis().SetTitle('Eff. (L1 / Gen)')
    graph.GetXaxis().SetTitle('Gen P_{T}')
    c.Print('plotsOpt/eff_'+name+'.png')    
    del denom, neum
    del c,p
    return graph

def plotEffHists( name, graphs=[] ) :
    c = ROOT.TCanvas('c','c',600,600)
    c.SetTitle( name )
    c.SetGrid()
    mg = ROOT.TMultiGraph("mg", c.GetTitle())
    for g in graphs :
        mg.Add( g )
    mg.Draw("aplez")
    c.Print('plotsOpt/effs_'+name+'.png')    
    del c


if __name__ == '__main__' :
    c = ROOT.TCanvas('c','c',600,600)
    print "RATE: Starting quantity: ",rInit
    print "EFF: Starting quantity: ",eInit
    tryCut( eTree, eInit, rTree, rInit, "cluster_pt", "cluster_iso<5")
    tryCut( eTree, eInit, rTree, rInit, "cluster_pt", "cluster_iso<4")
    tryCut( eTree, eInit, rTree, rInit, "cluster_pt", "cluster_iso<3")
    tryCut( eTree, eInit, rTree, rInit, "cluster_pt", "cluster_iso<2")

    tryCut( eTree, eInit, rTree, rInit, "cluster_pt", "cluster_hovere < 1 || abs(trackDeltaPhi) < 0.05")
    tryCut( eTree, eInit, rTree, rInit, "cluster_pt", "abs(trackDeltaEta)<0.03")
    tryCut( eTree, eInit, rTree, rInit, "cluster_pt", "abs(trackDeltaPhi)<0.05")
    tryCut( eTree, eInit, rTree, rInit, "cluster_pt", "abs(trackDeltaEta)<0.03 && abs(trackDeltaPhi)<0.05")


    print "Now with pt rescue above 20 GeV"
    tryCut( eTree, eInit, rTree, rInit, "cluster_pt", "abs(trackDeltaPhi)<0.05 || cluster_pt > 20")
    tryCut( eTree, eInit, rTree, rInit, "cluster_pt", "abs(trackDeltaEta)<0.03 || cluster    _pt > 20")
    tryCut( eTree, eInit, rTree, rInit, "cluster_pt", "(abs(trackDeltaEta)<0.03 && abs(trackDeltaPhi)<0.05) || cluster    _pt > 20")


    print "Iso work"
    tryCut( eTree, eInit, rTree, rInit, "cluster_pt", "cluster_iso<2")
    tryCut( eTree, eInit, rTree, rInit, "cluster_pt", "cluster_iso < 2 || cluster_pt > 20")
    tryCut( eTree, eInit, rTree, rInit, "cluster_pt", "cluster_iso<2 && abs(trackDeltaPhi)<0.02")
    # Cut1 for plots
    tryCut( eTree, eInit, rTree, rInit, "cluster_pt", "((cluster_iso<2 && abs(trackDeltaPhi)<0.02) || cluster_pt > 20)")
    # Cut2 for plots
    tryCut( eTree, eInit, rTree, rInit, "cluster_pt", "((cluster_iso<2 && abs(trackDeltaPhi)<0.02 && abs(trackDeltaEta)<0.015) || (cluster_pt > 20 && abs(trackDeltaEta)<0.015) || cluster_pt > 30)")
#    tryCut( eTree, eInit, rTree, rInit, "cluster_pt", "(cluster_iso<3 && abs(trackDeltaPhi)<0.04 && cluster_pt < 10) || (cluster_iso<2 && abs(trackDeltaPhi)<0.02) || cluster_pt > 20")


    # New Rate and Efficiency plots
    rateFile = ROOT.TFile( 'egTriggerRates.root', 'r' )
    rTree = rateFile.Get("analyzer/crystal_tree")
    cut0 = ""
    r0 = makeRatePlot( rTree, "cut0", cut0 )
    cut1 = "((cluster_iso<2 && abs(trackDeltaPhi)<0.02) || cluster_pt > 20)"
    r1 = makeRatePlot( rTree, "cut1", cut1 )
    cut2 = "((cluster_iso<2 && abs(trackDeltaPhi)<0.02 && abs(trackDeltaEta)<0.015) || (cluster_pt > 20 && abs(trackDeltaEta)<0.015) || cluster_pt > 30)"
    r2 = makeRatePlot( rTree, "cut2", cut2 )
    plotRateHists(  "NoCut_cut1_cut2", [r0, r1, r2] )

    effFile = ROOT.TFile( 'egTriggerEff.root', 'r' )
    eTree = effFile.Get("analyzer/crystal_tree")
    e1 = makeEffPlot( eTree, "cut1", cut1 )
    e2 = makeEffPlot( eTree, "cut2", cut2 )
    plotEffHists(  "NoCut_cut1_cut2", [e1, e2] )



