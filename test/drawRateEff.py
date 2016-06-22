import ROOT
import trigHelpers
from array import array
from ROOT import gStyle, gPad
import CMS_lumi, tdrstyle

def loadHists( file_, histMap = {}, eff=False ) :
    hists = {}
    for h, path in histMap.iteritems() :
        #print h, path
        if len( path ) == 2 :
            #print "len 2",path[0],path[1]
            hists[ h ] = file_.Get( path[1] )
            #print hists[ h]
            hists[ h ].SetTitle( path[0] )
        else :
            hists[ h ] = file_.Get( path )
            hists[ h ].SetTitle( h )
        #hists[ h ].SetDirectory( 0 )
    return hists


def drawCMSString( title ) :
    cmsString = ROOT.TLatex(
        gPad.GetAbsXlowNDC()+gPad.GetAbsWNDC()-gPad.GetLeftMargin(),
        gPad.GetAbsYlowNDC()+gPad.GetAbsHNDC()-gPad.GetTopMargin()+0.005,
        title )
    cmsString.SetTextFont(42)
    cmsString.SetTextSize(0.03)
    cmsString.SetNDC(1)
    cmsString.SetTextAlign(31)
    cmsString.Draw()
    return cmsString


def setLegStyle( x1,y1,x2,y2 ) :
    leg = ROOT.TLegend(x1,y1,x2,y2)
    leg.SetBorderSize(0)
    leg.SetLineColor(1)
    leg.SetLineStyle(1)
    leg.SetLineWidth(1)
    leg.SetFillColor(0)
    leg.SetFillStyle(0)
    leg.SetTextFont(42)
    return leg


def draw2DSets(c, tree1, var, cut, title1, tree2, title2, xaxis, xinfo, yaxis, yinfo) :
    print cut
    c.cd(1)
    h1 = ROOT.TH2F("h1", title1, xinfo[0], xinfo[1], xinfo[2], yinfo[0], yinfo[1], yinfo[2])
    tree1.Draw( var + " >> h1", cut )
    h1.GetXaxis().SetTitle( xaxis )
    h1.GetYaxis().SetTitle( yaxis )
    h1.Draw("colz")
    c.cd(2)
    h2 = ROOT.TH2F("h2", title2, xinfo[0], xinfo[1], xinfo[2], yinfo[0], yinfo[1], yinfo[2])
    tree2.Draw( var + " >> h2", cut )
    h2.GetXaxis().SetTitle( xaxis )
    h2.GetYaxis().SetTitle( yaxis )
    h2.Draw("colz")
    c.Print("plots/"+c.GetTitle()+".png")
    del h1
    del h2

def draw2DPtRes( hist, c, name ) :
    c.Clear()
    c.SetCanvasSize(700, 600)
    #c.SetGridx(1)
    #c.SetGridy(1)
    c.SetRightMargin(0.14)
    c.SetTopMargin(0.10)
    #recoGenPtHist.SetTitle("Crystal EG algorithm pT resolution")
    hist.SetTitle("")
    hist.GetYaxis().SetTitle("Relative Error in P_{T} (reco-gen)/gen")
    hist.GetYaxis().SetTitleOffset(1.3)
    hist.SetMaximum(50)
    hist.Draw("colz")
    cmsString = drawCMSString("CMS Simulation, <PU>=140 bx=25, Single Electron")
    c.Print("plots/"+name+"_reco_gen_pt.png")
    del cmsString


def drawRates( hists, c, ymax, xrange = [0., 0.] ) :
    c.cd()
    colors = [ROOT.kBlack, ROOT.kRed, ROOT.kBlue, ROOT.kGreen, ROOT.kOrange, ROOT.kGray]
    marker_styles = [20, 24, 25, 26, 32, 35]
    c.Clear()
    mg = ROOT.TMultiGraph("mg", c.GetTitle())
    
    graphs = []
    for i, hist in enumerate(hists) :
        graph = ROOT.TGraphErrors( hist )
        graph.SetLineColor( colors[i] )
        graph.SetMarkerColor( colors[i] )
        graph.SetMarkerStyle( marker_styles[i] )
        graph.SetMarkerSize( 0.8 )
        mg.Add( graph )
        graphs.append( graph )
    
    mg.Draw("aplez")
    
    if c.GetLogy() == 0 : # linear
        mg.SetMinimum(0.)
    else :
        mg.SetMinimum(10.)
    
    if ymax != 0. :
        mg.SetMaximum( ymax ) 
    
    leg = setLegStyle(0.53,0.78,0.95,0.92)
    for graph in graphs :
        leg.AddEntry(graph, graph.GetTitle(),"lpe")
    leg.Draw("same")
    c.Update()
    
    mg.GetXaxis().SetTitle(hists[0].GetXaxis().GetTitle())
    if xrange[0] != 0. or xrange[1] != 0 :
        mg.GetXaxis().SetRangeUser(xrange[0], xrange[1])
    mg.GetYaxis().SetTitle(hists[0].GetYaxis().GetTitle())
    
    cmsString = drawCMSString("CMS Simulation, <PU>=140 bx=25, MinBias")
    
    c.Print("plots/"+c.GetName()+".png")


def drawEfficiency( hists, c, ymax, xTitle, xrange = [0., 0.], fit = False, fitHint = [1., 15., 3., 0.]) :
    c.cd()
    colors = [ROOT.kBlack, ROOT.kRed, ROOT.kBlue, ROOT.kGreen, ROOT.kOrange, ROOT.kGray]
    marker_styles = [20, 24, 25, 26, 32]
    lines = [ROOT.kSolid, ROOT.kDashed, ROOT.kDotted]
    c.Clear()
    mg = ROOT.TMultiGraph("mg", c.GetTitle())
    
    graphs = []
    for i, hist in enumerate(hists) :
        #hist.Scale( 1./hist.GetEntries() )
        graph = ROOT.TGraphAsymmErrors( hist )
        graph.SetLineColor( colors[i] )
        graph.SetMarkerColor( colors[i] )
        graph.SetMarkerStyle( marker_styles[i] )
        graph.SetMarkerSize( 0.8 )
        mg.Add( graph )
        graphs.append( graph )
    
    mg.Draw("aplez")

    if c.GetLogy() == 0 : # linear
        mg.SetMinimum(0.)
    else :
        mg.SetMinimum(10.)
    
    if ymax != 0. :
        mg.SetMaximum( ymax ) 
    

    if ( fit and xrange[1] != xrange[0] ) :
       gStyle.SetOptFit(0)
       for j, graph in enumerate(graphs) :
          shape = ROOT.TF1("shape", "[0]/2*(1+TMath::Erf((x-[1])/([2]*sqrt(x))))+[3]*x", xrange[0], xrange[1])
          shape.SetParameters(fitHint[0], fitHint[1], fitHint[2], fitHint[3])
          # Somehow, step size increases each time, have to find a way to control it...
          graph.Fit(shape)
          graph.GetFunction("shape").SetLineColor(graph.GetLineColor())
          graph.GetFunction("shape").SetLineWidth(graph.GetLineWidth()*2)
 
    leg = setLegStyle(0.53,0.80,0.95,0.92)
    for graph in graphs :
        leg.AddEntry(graph, graph.GetTitle(),"lpe")
    leg.Draw("same")
    c.Update()
    
    #mg.GetXaxis().SetTitle(graphs[0].GetXaxis().GetTitle())
    mg.GetXaxis().SetTitle(xTitle)
    if ( xrange[0] != 0. or xrange[1] != 0 ) :
        mg.GetXaxis().SetRangeUser(xrange[0], xrange[1])
    #mg.GetYaxis().SetTitle(graphs[0].GetYaxis().GetTitle())
    mg.GetYaxis().SetTitle("Eff. (L1 Algo./Generated)")
 
    cmsString = drawCMSString("CMS Simulation, <PU>=140 bx=25, Single Electron")
 
    c.Print(("plots/"+c.GetName()+".png"))


def draw2DdeltaRHist(hist, c) :
    c.Clear()
    c.cd()
    gStyle.SetOptTitle(0)
    txtSize = 0.028
    margin = 0.08
    histpad_sizeX = 0.6
    histpad_sizeY = 0.7
    hist_pad = ROOT.TPad( c.GetName()+"_hist", "subpad", margin, margin, histpad_sizeX+margin, histpad_sizeY+margin, c.GetFillColor())
    hist_pad.SetMargin(0., 0., 0., 0.)
    hist_pad.Draw()
    xprojection_pad = ROOT.TPad(c.GetName()+"_xprojection", "subpad", margin, histpad_sizeY+margin, histpad_sizeX+margin, 1-margin, c.GetFillColor())
    xprojection_pad.SetMargin(0., 0., 0., 0.)
    xprojection_pad.Draw()
    yprojection_pad = ROOT.TPad(c.GetName()+"_yprojection", "subpad", histpad_sizeX+margin, margin, 1-2.5*margin, histpad_sizeY+margin, c.GetFillColor())
    yprojection_pad.SetMargin(0., 0., 0., 0.)
    yprojection_pad.Draw()
 
    hist.Sumw2()
    hist.Scale(1./hist.Integral())
    xprojection_hist = hist.ProjectionX(hist.GetName(), 1, hist.GetNbinsY(), "e")
    xprojection = ROOT.TGraphErrors(xprojection_hist)
    xprojection.SetLineColor(ROOT.kBlack)
    xprojection.SetMarkerColor(ROOT.kBlack)
    yprojection_hist = hist.ProjectionY(hist.GetName(), 1, hist.GetNbinsX(), "e")
    yprojection = ROOT.TGraphErrors(yprojection_hist.GetXaxis().GetNbins())
    yprojection.SetName(yprojection_hist.GetName()+"_graph")
    yproj_xaxis = yprojection_hist.GetXaxis()
    for i in range(0, yprojection_hist.GetXaxis().GetNbins() ) :
       bin = yproj_xaxis.GetBinCenter(i+1)
       width = yprojection_hist.GetBinWidth(i+1)*gStyle.GetErrorX()
       count = yprojection_hist.GetBinContent(i+1)
       err = yprojection_hist.GetBinError(i+1)
       yprojection.SetPoint(i, count, bin)
       yprojection.SetPointError(i, err, width)
 
    # Draw 2D hist
    hist_pad.cd()
    hist.Draw("col")
    hist.GetYaxis().SetTitleOffset(1.4)
    
    # Fit hist
    shape = ROOT.TF2("2dshape", "[0]*exp(-[2]*(x[0]-[1])**2-[4]*(x[1]-[3])**2-2*[5]*(x[0]-[1])*(x[1]-[3]))", -0.05, 0.05, -0.05, 0.05)
    shape.SetParameters(0.003, 0., 3.769e4, 0., 4.215e4, -1.763e4)
    hist.Fit(shape, "n")
    max_ = shape.GetParameter(0)
    contours = array('d', [])
    contours.append( max_*ROOT.TMath.exp(-4.5))
    contours.append( max_*ROOT.TMath.exp(-2))
    contours.append( max_*ROOT.TMath.exp(-0.5))
    shape.SetContour(3, contours)
    shape.SetNpx(100)
    shape.SetNpy(100)
    shape.SetLineWidth(2)
    shape.SetLineColor(ROOT.kRed)
    shape.Draw("cont3 same")
    
    # One crystal box
    crystalBox = ROOT.TBox(-0.0173/2, -0.0173/2, 0.0173/2, 0.0173/2)
    crystalBox.SetLineStyle(3)
    crystalBox.SetLineColor(ROOT.kGray)
    crystalBox.SetLineWidth(2)
    crystalBox.SetFillStyle(0)
    crystalBox.Draw()
 
    # Draw x projection
    xprojection_pad.cd()
    xprojection.Draw("apez")
    xprojection.GetYaxis().SetNdivisions(0)
    xprojection.GetXaxis().SetRangeUser(hist.GetXaxis().GetBinLowEdge(1), hist.GetXaxis().GetBinUpEdge(hist.GetXaxis().GetNbins()))
    xprojection.GetXaxis().SetLabelSize(0.)
    xprojection.GetYaxis().SetRangeUser(0., 0.22)
    shapeprojX = ROOT.TF1("shapeprojX", "[0]*sqrt(([2]*[4]-[5]**2)/(TMath::Pi()*[2]))*exp(([5]**2-[2]*[4])*(x-[3])**2/[2])", -0.05, 0.05)
    shapeprojX.SetParameters(shape.GetParameters())
    shapeprojX.SetParameter(0, shape.GetParameter(0)/20)
    shapeprojX.SetLineWidth(2)
    shapeprojX.SetNpx(100)
    shapeprojX.SetLineColor(ROOT.kRed)
    shapeprojX.Draw("same")
 
    # Draw y projection
    yprojection_pad.cd()
    yprojection.Draw("apez")
    yprojection.GetXaxis().SetNdivisions(0)
    yprojection.GetXaxis().SetRangeUser(0., 0.2)
    yprojection.GetYaxis().SetRangeUser(hist.GetYaxis().GetBinLowEdge(1), hist.GetYaxis().GetBinUpEdge(hist.GetYaxis().GetNbins()))
    yprojection.GetYaxis().SetLabelSize(0.)
    shapeprojY = ROOT.TF1("shapeprojY", "[0]*sqrt(([2]*[4]-[5]**2)/(TMath::Pi()*[4]))*exp(([5]**2-[2]*[4])*(x-[1])**2/[4])", -0.05, 0.05)
    shapeprojY.SetParameters(shape.GetParameters())
    shapeprojY.SetParameter(0, shape.GetParameter(0)/20)
    shapeprojYpos = array('d', [])
    shapeprojYval = array('d', [])
    for i in range( 0, 101 ) :
       shapeprojYpos.append( 1e-3*i-0.05 )
       shapeprojYval.append( shapeprojY.Eval(shapeprojYpos[i] ) )

    shapeprojYLine = ROOT.TGraph(101, shapeprojYval, shapeprojYpos)
    shapeprojYLine.SetLineColor(ROOT.kRed)
    shapeprojYLine.SetLineWidth(2)
    shapeprojYLine.Draw("l")
 
    # Draw Title
    c.cd()
    if c.GetTitle() != '' :
       title = ROOT.TLatex(margin, 1-margin+0.01, "Crystal-level EG Trigger #DeltaR Distribution")
       title.SetTextSize(0.04)
       title.SetTextFont(42)
       title.SetNDC()
       title.Draw()
 
    # CMS info string
    cmsString = ROOT.TLatex(
       histpad_sizeX+margin-0.005, 
       1-margin-0.005, 
       "CMS Simulation, <PU>=140 bx=25, Single Electron")
    cmsString.SetTextFont(42)
    cmsString.SetTextSize(0.02)
    cmsString.SetNDC(1)
    cmsString.SetTextAlign(33)
    cmsString.Draw()
 
    # Stats
    stats = []
    stats.append( ROOT.TLatex(histpad_sizeX+margin+0.01, histpad_sizeY+margin+0.13, "#mu_#eta = "+format(shape.GetParameter(1), '.2g' )) )
    stats.append( ROOT.TLatex(histpad_sizeX+margin+0.01, histpad_sizeY+margin+0.1,"#mu_#phi = "+format(shape.GetParameter(3), '.2g')) )
    stats.append( ROOT.TLatex(histpad_sizeX+margin+0.01, histpad_sizeY+margin+0.07, "#sigma_#eta#eta = "+format(ROOT.TMath.sqrt(0.5/shape.GetParameter(2)), '.2g')) )
    stats.append( ROOT.TLatex(histpad_sizeX+margin+0.01, histpad_sizeY+margin+0.04, "#sigma_#phi#phi = "+format(ROOT.TMath.sqrt(0.5/shape.GetParameter(4)), '.2g')) )
    stats.append( ROOT.TLatex(histpad_sizeX+margin+0.01, histpad_sizeY+margin+0.01, "#sigma_#eta#phi = "+format(ROOT.TMath.sqrt(-0.5/shape.GetParameter(5)), '.2g')) )
    for i in range( 0, 5 ) :
       stats[i].SetTextSize(txtSize-0.002)
       stats[i].SetTextFont(42)
       stats[i].SetNDC()
       stats[i].Draw()
 
    # Draw palette
    # (not working)
    gPad.Update()
    palette = ROOT.TPaletteAxis(1-2.5*margin+0.01, margin, 1-1.5*margin, histpad_sizeY+margin, hist)
    hist.GetXaxis().SetTitleOffset( .8 )
    hist.GetXaxis().SetLabelSize( txtSize*1.35 )
    hist.GetXaxis().SetTitleSize( txtSize*2 )
    hist.GetYaxis().SetTitleOffset( 1.1 )
    hist.GetYaxis().SetLabelSize( txtSize*1.35 )
    hist.GetYaxis().SetTitleSize( txtSize*2 )
    hist.GetZaxis().SetTitleOffset( 1.4 )
    hist.GetZaxis().SetLabelSize( txtSize )
    hist.GetZaxis().SetTitleSize( txtSize )
    palette.Draw()
    gPad.Modified()
    gPad.Update()
 
    c.Print("plots/"+c.GetName()+".png")
    
    gStyle.SetOptTitle(1)


def drawDRHists(hists, c, ymax, doFit = False) :
    c.cd()
    colors = [ROOT.kBlack, ROOT.kRed, ROOT.kBlue, ROOT.kGreen, ROOT.kOrange, ROOT.kGray]
    marker_styles = [20, 24, 25, 26, 32, 35]
    hs = ROOT.THStack("hs", c.GetTitle())
    for i, hist in enumerate(hists) :
        hist.Sumw2()
        hist.Scale(1./hist.Integral())
        hist.SetLineColor(colors[i])
        hist.SetMarkerColor(colors[i])
        hist.SetMarkerStyle(marker_styles[i])
        hist.SetMarkerSize(0.8)
        hs.Add(hist, "ex0 hist")

    c.Clear()
    if c.GetLogy() == 0 : # linear
        hs.SetMinimum(0.)
    if ymax == 0. :
        hs.SetMaximum( hs.GetMaximum() * 1.2 )
    elif ymax == -1 :
        hs.SetMaximum( hs.GetMaximum() * 1.3 )
    elif ymax != 0. :
        hs.SetMaximum(ymax)
    #hs.SetMinimum(0.0001)
 
    hs.Draw("nostack")
 
    markers = []
    for hist in hists :
        markers.append( hist )
        markers[-1].Draw("psame")
 
    fit = ROOT.TF1("doublegaus", "gaus+gaus(3)", 0., 0.25)
    fit.SetParameters(0.3, 0., 0.003, 0.1, 0., 0.02)
    #hists[0].Fit(fit, "n")
    #fit.Draw("lsame")
 
    leg = setLegStyle(0.53,0.78,0.95,0.92)
    for hist in hists :
        leg.AddEntry(hist, hist.GetTitle(),"elp")
    leg.Draw("same")
    c.Update()

    hs.GetXaxis().SetTitle(hists[0].GetXaxis().GetTitle())
    #hs.GetYaxis().SetTitle(hists[0].GetYaxis().GetTitle())
    hs.GetYaxis().SetTitleOffset(1.2)
    hs.GetYaxis().SetTitle("Fraction of Events")
    #hs.GetXaxis().SetRangeUser(0., 0.1)
 
    cmsString = drawCMSString("CMS Simulation, <PU>=140 bx=25, Single Electron")
                
    c.Print("plots/"+c.GetName()+".png")

    # Don't produce CDFs at the moment
    #del markers
    #markers = []
 
    ## Now for integral
    #for  hist in hists :
    #   hs.RecursiveRemove(hist)
    #   intHist = hist.Clone( hist.GetName()+"_cdf" )
    #   integral = 0.
    #   for bin in range(0, intHist.GetNbinsX()+1) :
    #      integral += intHist.GetBinContent(bin)
    #      intHist.SetBinContent(bin, integral)

    #   hs.Add(intHist, "ex0 hist")
    #   markers.append(intHist)

    #hs.SetMaximum(1.2)
    #hs.GetYaxis().SetTitle( "Cumulative "+hs.GetYaxis().GetTitle() )
    #hs.Draw("nostack")
    #for  m in markers : m.Draw("psame")
    #leg.Draw("same")
    #cmsString2 = drawCMSString("CMS Simulation, <PU>=140 bx=25, Single Electron")
    #c.Print( "plots/"+c.GetName()+"_cdf.png" )

    if doFit :
        gStyle.SetOptFit(0)
        # Poorly done hard coding for fit suggestions
        # and fit ranges, sorry
        fitHints = [[.17, -0.025, 0.07],
                    [.08, 0.1, .1 ]]
        fitRanges = [[-.15, .08],
                    [-0.09, .3]]
        fitResults = []
        fitResults.append( ROOT.TLatex(.7, .7, "Gaussian Fits:" ))
        for i, hist in enumerate(hists) :
            shape = ROOT.TF1("shape", "gaus(0)", fitRanges[i][0], fitRanges[i][1])
            shape.SetParameters(fitHints[i][0], fitHints[i][1], fitHints[i][2])
            hist.Fit(shape, "R")
            hist.GetFunction("shape").SetLineColor(hist.GetLineColor())
            hist.GetFunction("shape").SetLineWidth(hist.GetLineWidth()*2)

            fitResult = hist.GetFunction("shape")
            fitResults.append( ROOT.TLatex(.7, .66-i*.09, "#mu: "+format(fitResult.GetParameter(1), '.2g')))
            fitResults.append( ROOT.TLatex(.7, .62-i*.09, "#sigma: "+format(ROOT.TMath.sqrt(.5*abs(fitResult.GetParameter(2))), '.2g')))
        for i in range( len(fitResults) ) :
            fitResults[i].SetTextSize(0.045)
            fitResults[i].SetTextFont(42)
            fitResults[i].SetNDC()
            if i > 2 : fitResults[i].SetTextColor(ROOT.kRed)
            fitResults[i].Draw()

        c.Print( "plots/"+c.GetName()+"_fit.png" )

    c.Clear()
 


if __name__ == '__main__' :
    
    ROOT.gROOT.SetBatch(True)
    gStyle.SetOptStat(0)
    gStyle.SetTitleFont(42, "p")
    gStyle.SetTitleColor(1)
    gStyle.SetTitleTextColor(1)
    gStyle.SetTitleFillColor(10)
    gStyle.SetTitleFontSize(0.05)
    gStyle.SetTitleFont(42, "XYZ")
    gStyle.SetLabelFont(42, "XYZ")

    
    ratesMap = {
        'L1EGamma Crystal' : 'analyzer/dyncrystalEG_rate',
        'Original L2 Algorithm' : 'analyzer/SLHCL1ExtraParticles:EGamma_rate',
        'Phase 1 TDR' : 'analyzer/l1extraParticlesUCT:All_rate',
        'LLR Alg.' : 'analyzer/SLHCL1ExtraParticlesNewClustering:EGamma_rate',
        'Run 1 Alg.' : 'analyzer/l1extraParticles:All_rate',
        'Crystal Trigger (prod.)' : 'analyzer/L1EGammaCrystalsProducer:EGammaCrystal_rate',}

    effMap = {
        'newAlgEtaHist' : ('L1EGamma Crystal', 'analyzer/divide_dyncrystalEG_efficiency_eta_by_gen_eta'),
        'newAlgPtHist' : ('L1EGamma Crystal', 'analyzer/divide_dyncrystalEG_efficiency_pt_by_gen_pt'),
        'newAlgDRHist' : ('L1EGamma Crystal', 'analyzer/dyncrystalEG_deltaR'),
        'newAlgDEtaHist' : ('L1EGamma Crystal', 'analyzer/dyncrystalEG_deta'),
        'newAlgDPhiHist' : ('L1EGamma Crystal', 'analyzer/dyncrystalEG_dphi'),
        'newAlgDPhiHist' : ('L1EGamma Crystal', 'analyzer/dyncrystalEG_dphi'),
        'newAlgGenRecoPtHist' : ('L1EGamma Crystal', 'analyzer/1d_reco_gen_pt'),
        'oldAlgEtaHist' : ('Original L2 Algorithm', 'analyzer/divide_SLHCL1ExtraParticles:EGamma_efficiency_eta_by_gen_eta'),
        'oldAlgPtHist' : ('Original L2 Algorithm', 'analyzer/divide_SLHCL1ExtraParticles:EGamma_efficiency_pt_by_gen_pt'),
        'oldAlgDRHist' : ('Original L2 Algorithm', 'analyzer/SLHCL1ExtraParticles:EGamma_deltaR'),
        'oldAlgDEtaHist' : ('Original L2 Algorithm', 'analyzer/SLHCL1ExtraParticles:EGamma_deta'),
        'oldAlgDPhiHist' : ('Original L2 Algorithm', 'analyzer/SLHCL1ExtraParticles:EGamma_dphi'),
        'oldAlgGenRecoPtHist' : ('Original L2 Algorithm', 'analyzer/SLHCL1ExtraParticles:EGamma_1d_reco_gen_pt'),
        'dynAlgEtaHist' : ('LLR Alg.', 'analyzer/divide_SLHCL1ExtraParticlesNewClustering:EGamma_efficiency_eta_by_gen_eta'),
        'dynAlgPtHist' : ('LLR Alg.', 'analyzer/divide_SLHCL1ExtraParticlesNewClustering:EGamma_efficiency_pt_by_gen_pt'),
        'dynAlgDRHist' : ('LLR Alg.', 'analyzer/SLHCL1ExtraParticlesNewClustering:EGamma_deltaR'),
        'dynAlgDEtaHist' : ('LLR Alg.', 'analyzer/SLHCL1ExtraParticlesNewClustering:EGamma_deta'),
        'dynAlgDPhiHist' : ('LLR Alg.', 'analyzer/SLHCL1ExtraParticlesNewClustering:EGamma_dphi'),
        'dynAlgGenRecoPtHist' : ('LLR Alg.', 'analyzer/SLHCL1ExtraParticlesNewClustering:EGamma_1d_reco_gen_pt'),
        'run1AlgEtaHist' : ('Run 1 Alg.', 'analyzer/divide_l1extraParticles:All_efficiency_eta_by_gen_eta'),
        'run1AlgPtHist' : ('Run 1 Alg.', 'analyzer/divide_l1extraParticles:All_efficiency_pt_by_gen_pt'),
        'run1AlgDRHist' : ('Run 1 Alg.', 'analyzer/l1extraParticles:All_deltaR'),
        'run1AlgDEtaHist' : ('Run 1 Alg.', 'analyzer/l1extraParticles:All_deta'),
        'run1AlgDPhiHist' : ('Run 1 Alg.', 'analyzer/l1extraParticles:All_dphi'),
        'run1AlgGenRecoPtHist' : ('Run 1 Alg.', 'analyzer/l1extraParticles:All_1d_reco_gen_pt'),
        'UCTAlgEtaHist' : ('Phase 1 TDR', 'analyzer/divide_l1extraParticlesUCT:All_efficiency_eta_by_gen_eta'),
        'UCTAlgPtHist' : ('Phase 1 TDR', 'analyzer/divide_l1extraParticlesUCT:All_efficiency_pt_by_gen_pt'),
        'UCTAlgDRHist' : ('Phase 1 TDR', 'analyzer/l1extraParticlesUCT:All_deltaR'),
        'UCTAlgDEtaHist' : ('Phase 1 TDR', 'analyzer/l1extraParticlesUCT:All_deta'),
        'UCTAlgDPhiHist' : ('Phase 1 TDR', 'analyzer/l1extraParticlesUCT:All_dphi'),
        'UCTAlgGenRecoPtHist' : ('Phase 1 TDR', 'analyzer/l1extraParticlesUCT:All_1d_reco_gen_pt'),
    }
    
    rateFile = ROOT.TFile( 'egTriggerRates.root', 'r' )
    effFile = ROOT.TFile( 'egTriggerEff.root', 'r' )

    effHistsKeys = trigHelpers.getKeysOfClass( effFile, "analyzer", "TGraphAsymmErrors")
    
    hists = loadHists( rateFile, ratesMap )
    effHists = loadHists( effFile, effMap )
    newAlgRecoPtHists = trigHelpers.loadObjectsMatchingPattern( effFile, "analyzer", effHistsKeys, "divide_dyncrystalEG_threshold*_reco_pt")
    for h in newAlgRecoPtHists : h.SetTitle("Crystal Algorithm")
    newAlgGenPtHists = trigHelpers.loadObjectsMatchingPattern( effFile, "analyzer", effHistsKeys, "divide_dyncrystalEG_threshold*_gen_pt")
    for h in newAlgGenPtHists : h.SetTitle("Crystal Algorithm")
    oldAlgRecoPtHists = trigHelpers.loadObjectsMatchingPattern( effFile, "analyzer", effHistsKeys, "divide_SLHCL1ExtraParticles:EGamma_threshold*_reco_pt")
    for h in oldAlgRecoPtHists : h.SetTitle("Original L2 Algorithm")
    dynAlgRecoPtHists = trigHelpers.loadObjectsMatchingPattern( effFile, "analyzer", effHistsKeys, "divide_SLHCL1ExtraParticlesNewClustering:EGamma_threshold*_reco_pt")
    for h in dynAlgRecoPtHists : h.SetTitle("Tower Algorithm 2")
    run1AlgRecoPtHists = trigHelpers.loadObjectsMatchingPattern( effFile, "analyzer", effHistsKeys, "divide_l1extraParticles:All_threshold*_reco_pt")
    for h in run1AlgRecoPtHists : h.SetTitle("Run 1 Alg.")
    crystalAlgPtHist = effFile.Get("analyzer/divide_L1EGammaCrystalsProducer:EGammaCrystal_efficiency_pt_by_gen_pt")
    crystalAlgPtHist.SetTitle("Crystal Trigger (prod.)")
    crystalAlgRecoPtHists = trigHelpers.loadObjectsMatchingPattern( effFile, "analyzer", effHistsKeys, "divide_L1EGammaCrystalsProducer:EGammaCrystal_threshold*_reco_pt")
    for h in crystalAlgRecoPtHists : h.SetTitle("Crystal Algorithm")
    crystalAlgGenPtHists = trigHelpers.loadObjectsMatchingPattern( effFile, "analyzer", effHistsKeys, "divide_L1EGammaCrystalsProducer:EGammaCrystal_threshold*_gen_pt")
    for h in crystalAlgGenPtHists : h.SetTitle("L1EGamma Crystal")
    UCTAlgRecoPtHists = trigHelpers.loadObjectsMatchingPattern( effFile, "analyzer", effHistsKeys, "divide_l1extraParticlesUCT:All_threshold*_reco_pt")
    for h in UCTAlgRecoPtHists : h.SetTitle("Phase 1 TDR")
    UCTAlgGenPtHists = trigHelpers.loadObjectsMatchingPattern( effFile, "analyzer", effHistsKeys, "divide_l1extraParticlesUCT:All_threshold*_gen_pt")
    for h in UCTAlgGenPtHists : h.SetTitle("Phase 1 TDR")
    
    crystal_tree = effFile.Get("analyzer/crystal_tree")
    rate_tree = rateFile.Get("analyzer/crystal_tree")
    ''' Do 2D color plots 1st b/c of TDR style '''
    # TDR Style does not play well with 2D color plots
    # 1) 2D delta Eta vs delta Phi plot
    dynCrystal2DdeltaRHist = effFile.Get("analyzer/dyncrystalEG_2DdeltaR_hist")
    c = ROOT.TCanvas('c', 'c', 800, 700)
    #c.SetCanvasSize(800, 700)
    c.SetName("dyncrystalEG_2D_deltaR")
    #c.SetTitle("#Delta R Distribution Fit")
    c.SetTitle("")
    draw2DdeltaRHist(dynCrystal2DdeltaRHist, c)
 
    # 2) 2D pt resolution vs. gen pt
    recoGenPtHist = effFile.Get("analyzer/reco_gen_pt")
    draw2DPtRes( recoGenPtHist, c, "dyncrystalEG" )
    tdrRecoGenPtHist = effFile.Get("analyzer/l1extraParticlesUCT:All_reco_gen_pt")
    draw2DPtRes( tdrRecoGenPtHist, c, "tdr" )

    ''' Track to cluster reco resolution '''
    c.SetCanvasSize(1200,600)
    c.Divide(2)
    # 3) 2D position resolution vs. reco pt
    # dEta
    #cut = "((cluster_iso<2 && abs(trackDeltaPhi)<0.02) || cluster_pt > 20)"
    #cut = "((cluster_iso<2 && abs(trackDeltaPhi)<0.02 && abs(trackDeltaEta)<0.015) || (cluster_pt > 20 && abs(trackDeltaEta)<0.015) || cluster_pt > 30)"
    cut = ""
    showerShapes = "(-0.921128 + 0.180511*TMath::Exp(-0.0400725*cluster_pt)>(-1)*(e2x5/e5x5))"
    Isolation = "((0.990748 + 5.64259*TMath::Exp(-0.0613952*cluster_pt))>cluster_iso)"
    deltaR = "((trackDeltaR<0.1))"
    deltaRgtr = "((trackDeltaR>0.1))"
    cut = showerShapes+"*"+Isolation
    cut = showerShapes+"*"+Isolation+"*"+deltaR
    title1 = "L1EGamma Crystal (Electrons)"
    title2 = "L1EGamma Crystal (Fake)"
    var = "zVertexEnergy:abs(trackZ-zVertex)"
    xaxis = "dZ (L1Trk, Trk Vtx)"
    xinfo = [80, 0., 20.]
    yaxis = "z Vertex #Sigma P_{T} (GeV)"
    yinfo = [50, 0, 100]
    c.SetTitle("trkBasedDZvsZVtxEnergy")
    draw2DSets(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo)

    var = "cluster_pt:trackDeltaEta"
    xaxis = "d#eta (L1Trk, L1EG Crystal)"
    xinfo = [80, -0.05, 0.05]
    yaxis = "Cluster P_{T} (GeV)"
    yinfo = [50, 0, 50]
    c.SetTitle("trkDEta2D_Pt")
    draw2DSets(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo)

    var = "trackDeltaPhi:cluster_pt"
    yaxis = "d#phi (L1Trk, L1EG Crystal)"
    yinfo = [80, -0.5, 0.5]
    xaxis = "Cluster P_{T} (GeV)"
    xinfo = [50, 0, 50]
    c.SetTitle("clusterPtVtrkDPhi")
    draw2DSets(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo)

    var = "trackDeltaEta:cluster_pt"
    yaxis = "d#eta (L1Trk, L1EG Crystal)"
    yinfo = [80, -0.5, 0.5]
    xaxis = "Cluster P_{T} (GeV)"
    xinfo = [50, 0, 50]
    c.SetTitle("clusterPtVtrkDEta")
    draw2DSets(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo)

    var = "trackDeltaR:cluster_pt"
    yaxis = "#Delta R (L1Trk, L1EG Crystal)"
    yinfo = [80, -0.5, 0.5]
    xaxis = "Cluster P_{T} (GeV)"
    xinfo = [50, 0, 50]
    c.SetTitle("clusterPtVtrkDRold")
    draw2DSets(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo)

    var = "TMath::Sqrt(trackDeltaEta*trackDeltaEta + trackDeltaPhi*trackDeltaPhi):cluster_pt"
    yaxis = "#Delta R (L1Trk, L1EG Crystal)"
    yinfo = [80, -0.5, 0.5]
    xaxis = "Cluster P_{T} (GeV)"
    xinfo = [50, 0, 50]
    c.SetTitle("clusterPtVtrkDRnew")
    draw2DSets(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo)

    var = "cluster_hovere:trackDeltaEta"
    yaxis = "Cluster H/E"
    yinfo = [50, 0, 10]
    xaxis = "d#eta (Trk - L1)"
    xinfo = [50, -1., 1.]
    c.SetTitle("trkDEta2D_HoverE")
    draw2DSets(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo)

    var = "cluster_iso:trackDeltaEta"
    yaxis = "Cluster Isolation (GeV)"
    yinfo = [50, 0, 25]
    c.SetTitle("trkDEta2D_Iso")
    draw2DSets(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo)

    var = "trackChi2:trackDeltaEta"
    yaxis = "Track Chi2"
    yinfo = [50, 0, 300]
    c.SetTitle("trkDEta2D_trkChi2")
    draw2DSets(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo)

    # dPhi
    var = "cluster_pt:trackDeltaPhi"
    title1 = "L1EGamma Crystal (Electrons)"
    title2 = "L1EGamma Crystal (Fake)"
    xaxis = "d#phi (L1Trk, L1EG Crystal)"
    xinfo = [80, -1., 1.]
    yaxis = "Cluster P_{T} (GeV)"
    yinfo = [50, 0, 50]
    c.SetTitle("trkDPhi2D_Pt")
    draw2DSets(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo)

    var = "cluster_hovere:trackDeltaPhi"
    yaxis = "Cluster H/E"
    yinfo = [50, 0, 10]
    c.SetTitle("trkDPhi2D_HoverE")
    draw2DSets(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo)

    var = "cluster_iso:trackDeltaPhi"
    yaxis = "Cluster Isolation (GeV)"
    yinfo = [50, 0, 25]
    c.SetTitle("trkDPhi2D_Iso")
    draw2DSets(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo)

    var = "trackChi2:trackDeltaPhi"
    yaxis = "Track Chi2"
    yinfo = [50, 0, 300]
    c.SetTitle("trkDPhi2D_trkChi2")
    draw2DSets(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo)

    var = "trackDeltaEta:trackDeltaPhi"
    yaxis = "Track d#eta"
    yinfo = [50, -1., 1.]
    c.SetTitle("trkDPhi2D_trkDEta")
    draw2DSets(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo)

    var = "(trackPt-cluster_pt)/trackPt:cluster_pt"
    xaxis = "Cluster P_{T} (GeV)"
    yaxis = "P_{T} Resolution (trk-cluster)/trk"
    xinfo = [50, 0., 50.]
    yinfo = [50, -5., 2.]
    c.SetTitle("clusterPtVptRes")
    draw2DSets(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo)

    var = "trackDeltaR:(trackPt-cluster_pt)/trackPt"
    yaxis = "Track #delta R"
    xaxis = "P_{T} Resolution (trk-cluster)/trk"
    yinfo = [50, 0., .5]
    xinfo = [50, -5., 2.]
    c.SetTitle("trkDR2D_ptRes")
    draw2DSets(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo)

    var = "cluster_iso:cluster_hovere"
    yaxis = "Cluster Iso (GeV)"
    xaxis = "Cluster H/E"
    yinfo = [50, 0., 10.]
    xinfo = [70, 0., 7.]
    c.SetTitle("clusterIsoVclusterHoverE")
    draw2DSets(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo)

    var = "trackPt:cluster_pt"
    xaxis = "Cluster P_{T} (GeV)"
    yaxis = "Track P_{T} (GeV)"
    xinfo = [50, 0., 50.]
    yinfo = [52, 0., 52.]
    c.SetTitle("clusterPtVTrkPt")
    draw2DSets(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo)

    var = "cluster_hovere:cluster_pt"
    xaxis = "Cluster P_{T} (GeV)"
    yaxis = "Cluster H/E"
    xinfo = [50, 0., 50.]
    yinfo = [50, 0., 15.]
    c.SetTitle("clusterPtVHoverE")
    draw2DSets(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo)

    var = "cluster_iso:cluster_pt"
    xaxis = "Cluster P_{T} (GeV)"
    yaxis = "Cluster Iso (GeV)"
    xinfo = [50, 0., 50.]
    yinfo = [50, 0., 10.]
    c.SetTitle("clusterPtVClusterIso")
    draw2DSets(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo)

    var = "((pt.5/pt.1 + pt.2)):cluster_pt"
    yaxis = "Ratio of crystal energies 1"
    xaxis = "Cluster p_{T} (GeV)"
    yinfo = [50, 0., 20.]
    xinfo = [60, 0., 60.]
    c.SetTitle("clusterPtVCrystalRatios1")
    draw2DSets(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo)

    var = "(1./(pt.5/pt.1 + pt.2)):cluster_pt"
    yaxis = "Ratio of crystal energies 2"
    xaxis = "Cluster p_{T} (GeV)"
    yinfo = [50, 0., 10.]
    xinfo = [60, 0., 60.]
    c.SetTitle("clusterPtVCrystalRatios2")
    draw2DSets(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo)

    var = "pt.1:cluster_pt"
    yaxis = "Crystal Energy 1 (GeV)"
    xaxis = "Cluster p_{T} (GeV)"
    yinfo = [50, 0., 50.]
    xinfo = [60, 0., 60.]
    c.SetTitle("clusterPtVCrystalEnergy1")
    draw2DSets(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo)

    var = "pt.2:cluster_pt"
    yaxis = "Crystal Energy 2 (GeV)"
    xaxis = "Cluster p_{T} (GeV)"
    yinfo = [50, 0., 50.]
    xinfo = [60, 0., 60.]
    c.SetTitle("clusterPtVCrystalEnergy2")
    draw2DSets(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo)

    var = "pt.3:cluster_pt"
    yaxis = "Crystal Energy 3 (GeV)"
    xaxis = "Cluster p_{T} (GeV)"
    yinfo = [50, 0., 50.]
    xinfo = [60, 0., 60.]
    c.SetTitle("clusterPtVCrystalEnergy3")
    draw2DSets(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo)

    var = "pt.4:cluster_pt"
    yaxis = "Crystal Energy 4 (GeV)"
    xaxis = "Cluster p_{T} (GeV)"
    yinfo = [50, 0., 50.]
    xinfo = [60, 0., 60.]
    c.SetTitle("clusterPtVCrystalEnergy4")
    draw2DSets(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo)

    var = "bremStrength:cluster_pt"
    yaxis = "BremStrength"
    xaxis = "Cluster p_{T} (GeV)"
    yinfo = [50, 0., 1.1]
    xinfo = [60, 0., 50.]
    c.SetTitle("clusterPtVBremStrength")
    draw2DSets(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo)

    var = "bremStrength:cluster_iso"
    yaxis = "BremStrength"
    xaxis = "Cluster Iso (GeV)"
    yinfo = [50, 0., 1.1]
    xinfo = [60, 0., 10.]
    c.SetTitle("clusterIsoVBremStrength")
    draw2DSets(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo)

    var = "bremStrength:cluster_hovere"
    yaxis = "BremStrength"
    xaxis = "Cluster H/E"
    yinfo = [50, 0., 1.1]
    xinfo = [60, 0., 5.]
    c.SetTitle("clusterHoEVBremStrength")
    draw2DSets(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo)

    var = "trackIsoConePtSum:trackIsoConeTrackCount"
    yaxis = "Iso Cone P_{T} Sum (GeV)"
    xaxis = "Iso Cone Track Count"
    yinfo = [500, 0., 60.]
    xinfo = [30, 0., 15.]
    c.SetTitle("trkIsoConePtSumVTrkIsoConeTrkCnt")
    draw2DSets(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo)

    var = "trackIsoConeTrackCount/trackPt:cluster_pt"
    yaxis = "Iso Cone Track Count/ Track P_{T}"
    xaxis = "Cluster P_{T} (GeV)"
    yinfo = [50, 0., 1.5]
    xinfo = [50, 0., 50.]
    c.SetTitle("trkIsoConeTrkCountOverTrackPtVClusterPt")
    draw2DSets(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo)

    var = "trackIsoConePtSum/trackPt:cluster_pt"
    yaxis = "Iso Cone P_{T} Sum/ Track P_{T}"
    xaxis = "Cluster P_{T} (GeV)"
    yinfo = [50, 0., 10.]
    xinfo = [50, 0., 50.]
    c.SetTitle("trkIsoConePtSumOverTrackPtVClusterPt")
    draw2DSets(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo)

    var = "trackIsoConePtSum/trackPt:trackIsoConeTrackCount"
    yaxis = "Iso Cone P_{T} Sum/ Track P_{T}"
    xaxis = "Iso Cone Track Count"
    yinfo = [50, 0., 10.]
    xinfo = [30, 0., 15.]
    c.SetTitle("trkIsoConePtSumOverTrackPtVTrkIsoConeTrkCnt")
    draw2DSets(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo)

    var = "abs(trackRInv):cluster_pt"
    yaxis = "abs( Track Curvature )"
    xaxis = "Cluster p_{T} (GeV)"
    yinfo = [100, 0., 0.007]
    xinfo = [50, 0., 50.]
    c.SetTitle("trkRInvVPt")
    draw2DSets(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo)

    var = "abs(trackRInv):((trackPt-cluster_pt)/trackPt)"
    yaxis = "abs( Track Curvature )"
    xaxis = "P_{T} Res"
    yinfo = [100, 0., 0.007]
    xinfo = [50, -10., 2.]
    c.SetTitle("trkRInvVPtRes")
    draw2DSets(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo)

    #cut = "cluster_pt < 25"
    #var = "abs(trackRInv):((trackPt-cluster_pt)/trackPt)"
    #yaxis = "abs( Track Curvature )"
    #xaxis = "P_{T} Res"
    #yinfo = [100, 0., 0.007]
    #xinfo = [50, -10., 2.]
    #c.SetTitle("trkRInvVPtRes0to25")
    #draw2DSets(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo)

    #cut = "cluster_pt > 25"
    #var = "abs(trackRInv):((trackPt-cluster_pt)/trackPt)"
    #yaxis = "abs( Track Curvature )"
    #xaxis = "P_{T} Res"
    #yinfo = [100, 0., 0.007]
    #xinfo = [50, -10., 2.]
    #c.SetTitle("trkRInvVPtRes25to50")
    #draw2DSets(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo)

    #cut = ""
    var = "abs(trackZ-gen_z):cluster_pt"
    yaxis = "dZ(trk-Gen) (cm)"
    xaxis = "cluster P_{T} (GeV)"
    yinfo = [100, 0., 20.]
    xinfo = [50, 0., 50.]
    c.SetTitle("clusterPtVDZtrkGen")
    draw2DSets(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo)

    var = "abs(trackZ-zVertex):cluster_pt"
    yaxis = "dZ(trk-PV) (cm)"
    xaxis = "cluster P_{T} (GeV)"
    yinfo = [100, 0., 20.]
    xinfo = [50, 0., 50.]
    c.SetTitle("clusterPtVDZtrkPV")
    draw2DSets(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo)

    var = "abs(gen_z-zVertex):cluster_pt"
    yaxis = "dZ(gen-PV) (cm)"
    xaxis = "cluster P_{T} (GeV)"
    yinfo = [100, 0., 20.]
    xinfo = [50, 0., 50.]
    c.SetTitle("clusterPtVDZgenPV")
    draw2DSets(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo)

    var = "bremStrength:trackChi2"
    yaxis = "bremStr"
    xaxis = "track chi 2"
    yinfo = [100, 0., 1.1]
    xinfo = [50, 0., 100.]
    c.SetTitle("bremStrVTrkChi2")
    draw2DSets(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo)

    var = "trackChi2:cluster_pt"
    yaxis = "track chi 2"
    xaxis = "cluster P_{T} (GeV)"
    yinfo = [100, 0., 110.]
    xinfo = [50, 0., 50.]
    c.SetTitle("clusterPtVChi2")
    draw2DSets(c, crystal_tree, var, cut, title1, rate_tree, title2, xaxis, xinfo, yaxis, yinfo)




    c.Clear()


 
    # Offline reco pt
    offlineRecoHist = ROOT.TH2F("offlineRecoHist", "Offline reco to gen. comparisonGen. pT (GeV)(reco-gen)/genCounts", 60, 0., 50., 60, -0.5, 0.5)
    crystal_tree.Draw("(reco_pt-gen_pt)/gen_pt:gen_pt >> offlineRecoHist", "reco_pt>0", "colz")
    c.SetLogy(0)
    offlineRecoHist.Draw("colz")
    c.Print("plots/offlineReco_vs_gen.png")
    c.Clear()
 
    recoGenPtHist.SetTitle("Crystal EG algorithm pT resolution")
    # oldAlgrecoGenPtHist = (TH2F *) effFile.Get("analyzer/SLHCL1ExtraParticles:EGamma_reco_gen_pt")
    oldAlgrecoGenPtHist = effFile.Get("analyzer/l1extraParticlesUCT:All_reco_gen_pt")
    oldAlgrecoGenPtHist.SetTitle("Tower EG alg. momentum error")
    oldAlgrecoGenPtHist.GetYaxis().SetTitle("Relative Error (reco-gen)/gen")
    oldAlgrecoGenPtHist.SetMaximum(50)
    oldAlgrecoGenPtHist.SetLineColor(ROOT.kRed)
    c.SetCanvasSize(1200,600)
    c.Divide(2,1)
    c.cd(1)
    gPad.SetGridx(1)
    gPad.SetGridy(1)
    recoGenPtHist.Draw("colz")
    recoGenPtHist.GetYaxis().SetTitleOffset(1.4)
    c.cd(2)
    gPad.SetGridx(1)
    gPad.SetGridy(1)
    oldAlgrecoGenPtHist.Draw("colz")
    oldAlgrecoGenPtHist.GetYaxis().SetTitleOffset(1.4)
    c.Print("plots/reco_gen_pt.png")


    del c
    tdrstyle.setTDRStyle()
    gStyle.SetOptStat(0)

    
    xrange = [0., 50.]
    c = ROOT.TCanvas('c', 'c', 800, 600)
    c.SetLogy(1)
    #c.SetGridx(1)
    #c.SetGridy(1)
    #gStyle.SetGridStyle(2)
    #gStyle.SetGridColor(ROOT.kGray+1)
    
#    ''' RATE SECTION '''    
#    c.SetName('dyncrystalEG_rate')
#    c.SetTitle('')
#    toDraw = [ hists['L1EGamma Crystal'], hists['Phase 1 TDR'] ]
#    drawRates( toDraw, c, 40000., xrange)
#    
#    #c.SetName('dyncrystalEG_rate_UW')
#    #c.SetTitle('EG Rates (UW only)')
#    #toDraw = [ hists['L1EGamma Crystal'], hists['Phase 1 TDR'], hists['LLR Alg.'] ]
#    #drawRates( toDraw, c, 40000., xrange)
#    
#    ''' EFFICIENCY SECTION '''
#    c.SetLogy(0)
#    c.SetName("dyncrystalEG_efficiency_eta")
#    c.SetTitle("EG Efficiencies")
#    drawEfficiency([effHists['newAlgEtaHist'], effHists['UCTAlgEtaHist']], c, 1.2, "Gen #eta", [-3.,3.] , False, [-2.5, 2.5])
#    #c.SetName("dyncrystalEG_efficiency_pt_UW")
#    #c.SetTitle("EG Efficiencies (UW only)")
#    #drawEfficiency([effHists['newAlgPtHist'], effHists['UCTAlgPtHist'], effHists['dynAlgPtHist']], c, 1.2, "Pt (GeV)", xrange, True, [0.9, 2., 1., 0.])
#    c.SetName("dyncrystalEG_efficiency_pt")
#    c.SetTitle("")
#    drawEfficiency([effHists['newAlgPtHist'], effHists['UCTAlgPtHist']], c, 1.2, "Gen P_{T} (GeV)", xrange, True, [0.9, 2., 1., 0.])
#
#    # Map of possible pt values from file with suggested fit function params
#    possiblePts = {'16' : [0.9, 20., 1., 0.], '20' : [0.95, 30., 1., 0.], '30': [0.95, 16., 1., 0.]}
#    for crystalPt in crystalAlgGenPtHists :
#        toPlot = []
#        toPlot.append( crystalPt )
#        for UCTPt in UCTAlgGenPtHists :
#            for pt in possiblePts.keys() :
#                if pt in crystalPt.GetName() and pt in UCTPt.GetName() :
#                    print pt, crystalPt.GetName(), UCTPt.GetName()
#                    toPlot.append( UCTPt )
#                    c.SetName("dyncrystalEG_threshold"+pt+"_efficiency_gen_pt")
#                    drawEfficiency( toPlot, c, 1.2, "Gen P_{T} (GeV)", xrange, True, possiblePts[pt])
#
#
#    ''' POSITION RECONSTRUCTION '''
#    # Delta R Stuff
#    c.SetGridx(0)
#    c.SetGridy(0)
#    c.SetName("dyncrystalEG_deltaR")
#    c.SetTitle("")
#    drawDRHists([effHists['newAlgDRHist'], effHists['UCTAlgDRHist']], c, 0.)
#    #c.SetName("dyncrystalEG_deltaR_UW")
#    #c.SetTitle("")
#    #drawDRHists([effHists['newAlgDRHist'], effHists['UCTAlgDRHist'], effHists['dynAlgDRHist']], c, 0.)
#
#    # Delta Eta / Phi
#    #c.SetName("dyncrystalEG_deltaEta_UW")
#    #drawDRHists([effHists['newAlgDEtaHist'], effHists['UCTAlgDEtaHist'], effHists['dynAlgDEtaHist']], c, 0., [-0.5, 0.5])
#    c.SetName("dyncrystalEG_deltaEta")
#    drawDRHists([effHists['newAlgDEtaHist'], effHists['UCTAlgDEtaHist']], c, 0.)
#    #c.SetName("dyncrystalEG_deltaPhi_UW")
#    #drawDRHists([effHists['newAlgDPhiHist'], effHists['UCTAlgDPhiHist'], effHists['dynAlgDPhiHist']], c, 0., [-0.5, 0.5])
#    c.SetName("dyncrystalEG_deltaPhi")
#    drawDRHists([effHists['newAlgDPhiHist'], effHists['UCTAlgDPhiHist']], c, 0.)
#    # Draw L1EG Crystal dEta, dPhi with track matching
#    c.SetLogy(0)
#
#    cut15 = "cluster_pt > 15"
#    cut30 = "cluster_pt > 30"
#    c.SetName("dyncrystalEG_trkDeltaEtaFake")
#    trkDEtaF = ROOT.TH1F("trkDEtaF", "L1EGamma Crystal - Fakes", 80, -0.05, 0.05)
#    rate_tree.Draw("trackDeltaEta >> trkDEtaF")
#    trkDEtaF2 = ROOT.TH1F("trkDEtaF2", "L1EGamma Crystal - Fakes gtr 30p_{T}", 80, -0.05, 0.05)
#    rate_tree.Draw("trackDeltaEta >> trkDEtaF2", cut30)
#    trkDEtaF.GetXaxis().SetTitle("d#eta (L1Trk, L1EG Crystal)")
#    #drawDRHists( [trkDEtaF,], c, -1 )
#    c.SetName("dyncrystalEG_trkDeltaEta")
#    trkDEta = ROOT.TH1F("trkDEta", "L1EGamma Crystal", 80, -0.05, 0.05)
#    crystal_tree.Draw("trackDeltaEta >> trkDEta")
#    trkDEta2 = ROOT.TH1F("trkDEta2", "L1EGamma Crystal gtr 30p_{T}", 80, -0.05, 0.05)
#    crystal_tree.Draw("trackDeltaEta >> trkDEta2", cut30)
#    trkDEta.GetXaxis().SetTitle("d#eta (L1Trk, L1EG Crystal)")
#    #drawDRHists( [trkDEta,], c, -1 )
#    c.SetName("dyncrystalEG_trkDeltaEtaComp")
#    drawDRHists( [trkDEta, trkDEta2, trkDEtaF, trkDEtaF2], c, .2 )
#    del trkDEta, trkDEta2, trkDEtaF, trkDEtaF2
#    c.SetName("dyncrystalEG_trkDeltaEtaGen")
#    trkDEta = ROOT.TH1F("trkDEta", "L1EGamma Crystal", 80, -0.05, 0.05)
#    crystal_tree.Draw("trackEta-gen_eta >> trkDEta")
#    trkDEta.GetXaxis().SetTitle("d#eta (L1Trk, Gen Particle)")
#    drawDRHists( [trkDEta,], c, -1 )
#    del trkDEta
#
#    c.SetName("dyncrystalEG_trkDeltaPhiFake")
#    trkDPhiF = ROOT.TH1F("trkDPhiF", "L1EGamma Crystal - Fakes", 80, -0.2, 0.2)
#    rate_tree.Draw("trackDeltaPhi >> trkDPhiF")
#    trkDPhiF2 = ROOT.TH1F("trkDPhiF2", "L1EGamma Crystal - Fakes gtr 30p_{T}", 80, -0.2, 0.2)
#    rate_tree.Draw("trackDeltaPhi >> trkDPhiF2", cut30)
#    trkDPhiF.GetXaxis().SetTitle("d#phi (L1Trk, L1EG Crystal)")
#    #drawDRHists( [trkDPhiF,], c, -1 )
#    c.SetName("dyncrystalEG_trkDeltaPhi")
#    trkDPhi = ROOT.TH1F("trkDPhi", "L1EGamma Crystal", 80, -0.2, 0.2)
#    crystal_tree.Draw("trackDeltaPhi >> trkDPhi")
#    trkDPhi2 = ROOT.TH1F("trkDPhi2", "L1EGamma Crystal gtr 30p_{T}", 80, -0.2, 0.2)
#    crystal_tree.Draw("trackDeltaPhi >> trkDPhi2", cut30)
#    trkDPhi.GetXaxis().SetTitle("d#phi (L1Trk, L1EG Crystal)")
#    #drawDRHists( [trkDPhi,], c, -1 )
#    c.SetName("dyncrystalEG_trkDeltaPhiComp")
#    drawDRHists( [trkDPhi,trkDPhi2,trkDPhiF,trkDPhiF2], c, .55 )
#    del trkDPhi, trkDPhi2, trkDPhiF, trkDPhiF2
#
#    c.SetName("dyncrystalEG_trkDeltaPhiGen")
#    trkDPhi = ROOT.TH1F("trkDPhi", "L1EGamma Crystal", 80, -0.2, 0.2)
#    crystal_tree.Draw("trackPhi-gen_phi >> trkDPhi")
#    trkDPhi.GetXaxis().SetTitle("d#phi (L1Trk, Gen Particle)")
#    drawDRHists( [trkDPhi,], c, -1 )
#    del trkDPhi
#
#    # delta R
#    trkDRF = ROOT.TH1F("trkDRF", "L1EGamma Crystal - Fakes", 80, 0., 0.25)
#    rate_tree.Draw("trackDeltaR >> trkDRF")
#    trkDRF2 = ROOT.TH1F("trkDRF2", "L1EGamma Crystal - Fakes gtr 30p_{T}", 80, 0., 0.25)
#    rate_tree.Draw("trackDeltaR >> trkDRF2", cut30)
#    trkDR = ROOT.TH1F("trkDR", "L1EGamma Crystal", 80, 0., 0.25)
#    crystal_tree.Draw("trackDeltaR >> trkDR")
#    trkDR2 = ROOT.TH1F("trkDR2", "L1EGamma Crystal gtr 30p_{T}", 80, 0., 0.25)
#    crystal_tree.Draw("trackDeltaR >> trkDR2", cut30)
#    trkDR.GetXaxis().SetTitle("#Delta R (L1Trk, L1EG Crystal)")
#    c.SetName("dyncrystalEG_trkDeltaRComp")
#    drawDRHists( [trkDR,trkDR2,trkDRF,trkDRF2], c, .40 )
#    del trkDR, trkDR2, trkDRF, trkDRF2
#
#    c.SetName("dyncrystalEG_trkDeltaPt")
#    trkDPt = ROOT.TH1F("trkDPt", "L1EGamma Crystal", 80, -1., 1.)
#    crystal_tree.Draw("(trackPt-cluster_pt)/trackPt >> trkDPt")
#    trkDPt.GetXaxis().SetTitle("#delta P_{T} (L1Trk - L1EG Crystal)/L1Trk")
#    #drawDRHists( [trkDPt,], c, -1 )
#    del trkDPt
#    # do this one two ways once .../trk Pt other .../cluster_pt
#    trkDPtF = ROOT.TH1F("trkDPtF", "L1EGamma Crystal - Fakes", 80, -2., 5.)
#    rate_tree.Draw("(trackPt-cluster_pt)/cluster_pt >> trkDPtF")
#    trkDPtF2 = ROOT.TH1F("trkDPtF2", "L1EGamma Crystal - Fakes gtr 30p_{T}", 80, -2., 5.)
#    rate_tree.Draw("(trackPt-cluster_pt)/cluster_pt >> trkDPtF2", cut30)
#    trkDPt = ROOT.TH1F("trkDPt", "L1EGamma Crystal", 80, -2., 5.)
#    crystal_tree.Draw("(trackPt-cluster_pt)/cluster_pt >> trkDPt")
#    trkDPt2 = ROOT.TH1F("trkDPt2", "L1EGamma Crystal gtr 30p_{T}", 80, -2., 5.)
#    crystal_tree.Draw("(trackPt-cluster_pt)/cluster_pt >> trkDPt2", cut30)
#    trkDPt.GetXaxis().SetTitle("P_{T} Resolution (GeV)  (L1Trk - L1EG Crystal)/L1EG Crystal")
#    c.SetName("dyncrystalEG_trkDeltaClusterPtOverClusterComp")
#    drawDRHists( [trkDPt,trkDPt2,trkDPtF,trkDPtF2], c, .6 )
#    del trkDPt, trkDPt2, trkDPtF, trkDPtF2
#    c.SetName("dyncrystalEG_trkDeltaPtFakes")
#    trkDPtF = ROOT.TH1F("trkDPtF", "L1EGamma Crystal - Fakes", 80, -6., 2.)
#    rate_tree.Draw("(trackPt-cluster_pt)/trackPt >> trkDPtF")
#    trkDPtF2 = ROOT.TH1F("trkDPtF2", "L1EGamma Crystal - Fakes gtr 30p_{T}", 80, -6., 2.)
#    rate_tree.Draw("(trackPt-cluster_pt)/trackPt >> trkDPtF2", cut30)
#    trkDPt = ROOT.TH1F("trkDPt", "L1EGamma Crystal", 80, -6., 2.)
#    crystal_tree.Draw("(trackPt-cluster_pt)/trackPt >> trkDPt")
#    trkDPt.GetXaxis().SetTitle("P_{T} Resolution (GeV)  (L1Trk - L1EG Crystal)/L1Trk")
#    trkDPt2 = ROOT.TH1F("trkDPt2", "L1EGamma Crystal gtr 30p_{T}", 80, -6., 2.)
#    crystal_tree.Draw("(trackPt-cluster_pt)/trackPt >> trkDPt2", cut30)
#    trkDPtF.GetXaxis().SetTitle("#delta P_{T} (L1Trk - L1EG Crystal)/L1Trk")
#    #drawDRHists( [trkDPtF,], c, -1 )
#    c.SetName("dyncrystalEG_trkDeltaPtComp")
#    drawDRHists( [trkDPt,trkDPt2,trkDPtF,trkDPtF2], c, .6 )
#    del trkDPt, trkDPt2, trkDPtF, trkDPtF2
#    c.SetName("dyncrystalEG_trkDeltaPtGen")
#    trkDPt = ROOT.TH1F("trkDPt", "L1EGamma Crystal", 80, -1., 1.)
#    crystal_tree.Draw("(trackPt-gen_pt)/trackPt >> trkDPt")
#    trkDPt.GetXaxis().SetTitle("#delta P_{T} (L1Trk - Gen Particle)/L1Trk")
#    #drawDRHists( [trkDPt,], c, -1 )
#    del trkDPt
#
#    # Iso Comparisons
#    # Iso / clusterPt
#    clusterIso = ROOT.TH1F("clusterIso", "L1EGamma Crystal", 80, 0., 1.)
#    crystal_tree.Draw("cluster_iso/cluster_pt >> clusterIso")
#    clusterIso2 = ROOT.TH1F("clusterIso2", "L1EGamma Crystal gtr 15p_{T}", 80, 0., 1.)
#    crystal_tree.Draw("cluster_iso/cluster_pt >> clusterIso2", cut15)
#    clusterIso3 = ROOT.TH1F("clusterIso3", "L1EGamma Crystal gtr 30p_{T}", 80, 0., 1.)
#    crystal_tree.Draw("cluster_iso/cluster_pt >> clusterIso3", cut30)
#    clusterIsoF = ROOT.TH1F("clusterIsoF", "L1EGamma Crystal - Fakes", 80, 0., 1.)
#    rate_tree.Draw("cluster_iso/cluster_pt >> clusterIsoF")
#    clusterIsoF2 = ROOT.TH1F("clusterIsoF2", "L1EGamma Crystal - Fakes gtr 15p_{T}", 80, 0., 1.)
#    rate_tree.Draw("cluster_iso/cluster_pt >> clusterIsoF2", cut15)
#    clusterIsoF3 = ROOT.TH1F("clusterIsoF3", "L1EGamma Crystal - Fakes gtr 30p_{T}", 80, 0., 1.)
#    rate_tree.Draw("cluster_iso/cluster_pt >> clusterIsoF3", cut30)
#    c.SetName("dyncrystalEG_clusterIsoOverPtComp")
#    clusterIso.GetXaxis().SetTitle("Cluster Isolation/Cluster P_{T}")
#    drawDRHists( [clusterIso,clusterIso2,clusterIso3,clusterIsoF,clusterIsoF2,clusterIsoF3], c, .6 )
#    del clusterIso, clusterIso2, clusterIso3, clusterIsoF, clusterIsoF2, clusterIsoF3
#    # Iso / trackPt
#    clusterIso = ROOT.TH1F("clusterIso", "L1EGamma Crystal", 80, 0., 1.)
#    crystal_tree.Draw("cluster_iso/trackPt >> clusterIso")
#    clusterIso2 = ROOT.TH1F("clusterIso2", "L1EGamma Crystal gtr 15p_{T}", 80, 0., 1.)
#    crystal_tree.Draw("cluster_iso/trackPt >> clusterIso2", cut15)
#    clusterIso3 = ROOT.TH1F("clusterIso3", "L1EGamma Crystal gtr 30p_{T}", 80, 0., 1.)
#    crystal_tree.Draw("cluster_iso/trackPt >> clusterIso3", cut30)
#    clusterIsoF = ROOT.TH1F("clusterIsoF", "L1EGamma Crystal - Fakes", 80, 0., 1.)
#    rate_tree.Draw("cluster_iso/trackPt >> clusterIsoF")
#    clusterIsoF2 = ROOT.TH1F("clusterIsoF2", "L1EGamma Crystal - Fakes gtr 15p_{T}", 80, 0., 1.)
#    rate_tree.Draw("cluster_iso/trackPt >> clusterIsoF2", cut15)
#    clusterIsoF3 = ROOT.TH1F("clusterIsoF3", "L1EGamma Crystal - Fakes gtr 30p_{T}", 80, 0., 1.)
#    rate_tree.Draw("cluster_iso/trackPt >> clusterIsoF3", cut30)
#    c.SetName("dyncrystalEG_clusterIsoOverTrackPtComp")
#    clusterIso.GetXaxis().SetTitle("Cluster Isolation/Track P_{T}")
#    drawDRHists( [clusterIso,clusterIso2,clusterIso3,clusterIsoF,clusterIsoF2,clusterIsoF3], c, .6 )
#    del clusterIso, clusterIso2, clusterIso3, clusterIsoF, clusterIsoF2, clusterIsoF3
#    # Normal Isolation
#    clusterIso = ROOT.TH1F("clusterIso", "L1EGamma Crystal", 80, 0., 10.)
#    crystal_tree.Draw("cluster_iso >> clusterIso")
#    clusterIso2 = ROOT.TH1F("clusterIso2", "L1EGamma Crystal gtr 15p_{T}", 80, 0., 10.)
#    crystal_tree.Draw("cluster_iso >> clusterIso2", cut15)
#    clusterIso3 = ROOT.TH1F("clusterIso3", "L1EGamma Crystal gtr 30p_{T}", 80, 0., 10.)
#    crystal_tree.Draw("cluster_iso >> clusterIso3", cut30)
#    clusterIsoF = ROOT.TH1F("clusterIsoF", "L1EGamma Crystal - Fakes", 80, 0., 10.)
#    rate_tree.Draw("cluster_iso >> clusterIsoF")
#    clusterIsoF2 = ROOT.TH1F("clusterIsoF2", "L1EGamma Crystal - Fakes gtr 15p_{T}", 80, 0., 10.)
#    rate_tree.Draw("cluster_iso >> clusterIsoF2", cut15)
#    clusterIsoF3 = ROOT.TH1F("clusterIsoF3", "L1EGamma Crystal - Fakes gtr 30p_{T}", 80, 0., 10.)
#    rate_tree.Draw("cluster_iso >> clusterIsoF3", cut30)
#    c.SetName("dyncrystalEG_clusterIsoComp")
#    clusterIso.GetXaxis().SetTitle("Cluster Isolation (GeV)")
#    drawDRHists( [clusterIso,clusterIso2,clusterIso3,clusterIsoF,clusterIsoF2,clusterIsoF3], c, .3 )
#    del clusterIso, clusterIso2, clusterIso3, clusterIsoF, clusterIsoF2, clusterIsoF3
#    # Isolation using trackPt
#    clusterIso = ROOT.TH1F("clusterIso", "L1EGamma Crystal", 80, 0., 10.)
#    crystal_tree.Draw("cluster_iso*cluster_pt/trackPt >> clusterIso")
#    clusterIso2 = ROOT.TH1F("clusterIso2", "L1EGamma Crystal gtr 15p_{T}", 80, 0., 10.)
#    crystal_tree.Draw("cluster_iso*cluster_pt/trackPt >> clusterIso2", cut15)
#    clusterIso3 = ROOT.TH1F("clusterIso3", "L1EGamma Crystal gtr 30p_{T}", 80, 0., 10.)
#    crystal_tree.Draw("cluster_iso*cluster_pt/trackPt >> clusterIso3", cut30)
#    clusterIsoF = ROOT.TH1F("clusterIsoF", "L1EGamma Crystal - Fakes", 80, 0., 10.)
#    rate_tree.Draw("cluster_iso*cluster_pt/trackPt >> clusterIsoF")
#    clusterIsoF2 = ROOT.TH1F("clusterIsoF2", "L1EGamma Crystal - Fakes gtr 15p_{T}", 80, 0., 10.)
#    rate_tree.Draw("cluster_iso*cluster_pt/trackPt >> clusterIsoF2", cut15)
#    clusterIsoF3 = ROOT.TH1F("clusterIsoF3", "L1EGamma Crystal - Fakes gtr 30p_{T}", 80, 0., 10.)
#    rate_tree.Draw("cluster_iso*cluster_pt/trackPt >> clusterIsoF3", cut30)
#    c.SetName("dyncrystalEG_clusterIsoTrackPtComp")
#    clusterIso.GetXaxis().SetTitle("Cluster Isolation w/ Track P_{T} (GeV)")
#    drawDRHists( [clusterIso,clusterIso2,clusterIso3,clusterIsoF,clusterIsoF2,clusterIsoF3], c, .3 )
#    del clusterIso, clusterIso2, clusterIso3, clusterIsoF, clusterIsoF2, clusterIsoF3
#
#    # H/E Comparisons
#    # H/E / Cluster PT
#    clusterHoE = ROOT.TH1F("clusterHoE", "L1EGamma Crystal", 80, 0., .2)
#    crystal_tree.Draw("cluster_hovere/cluster_pt >> clusterHoE")
#    clusterHoE2 = ROOT.TH1F("clusterHoE2", "L1EGamma Crystal gtr 15p_{T}", 80, 0., .2)
#    crystal_tree.Draw("cluster_hovere/cluster_pt >> clusterHoE2", cut15)
#    clusterHoE3 = ROOT.TH1F("clusterHoE3", "L1EGamma Crystal gtr 30p_{T}", 80, 0., .2)
#    crystal_tree.Draw("cluster_hovere/cluster_pt >> clusterHoE3", cut30)
#    clusterHoEF = ROOT.TH1F("clusterHoEF", "L1EGamma Crystal - Fakes", 80, 0., .2)
#    rate_tree.Draw("cluster_hovere/cluster_pt >> clusterHoEF")
#    clusterHoEF2 = ROOT.TH1F("clusterHoEF2", "L1EGamma Crystal - Fakes gtr 15p_{T}", 80, 0., .2)
#    rate_tree.Draw("cluster_hovere/cluster_pt >> clusterHoEF2", cut15)
#    clusterHoEF3 = ROOT.TH1F("clusterHoEF3", "L1EGamma Crystal - Fakes gtr 30p_{T}", 80, 0., .2)
#    rate_tree.Draw("cluster_hovere/cluster_pt >> clusterHoEF3", cut30)
#    c.SetName("dyncrystalEG_clusterHoEOverPtComp")
#    clusterHoE.GetXaxis().SetTitle("(Cluster H/E)/Cluster P_{T} (GeV^{-1})")
#    drawDRHists( [clusterHoE,clusterHoE2,clusterHoE3,clusterHoEF,clusterHoEF2,clusterHoEF3], c, .5 )
#    del clusterHoE, clusterHoE2, clusterHoE3, clusterHoEF, clusterHoEF2, clusterHoEF3
#    # H/E / Track PT
#    clusterHoE = ROOT.TH1F("clusterHoE", "L1EGamma Crystal", 80, 0., .2)
#    crystal_tree.Draw("cluster_hovere/trackPt >> clusterHoE")
#    clusterHoE2 = ROOT.TH1F("clusterHoE2", "L1EGamma Crystal gtr 15p_{T}", 80, 0., .2)
#    crystal_tree.Draw("cluster_hovere/trackPt >> clusterHoE2", cut15)
#    clusterHoE3 = ROOT.TH1F("clusterHoE3", "L1EGamma Crystal gtr 30p_{T}", 80, 0., .2)
#    crystal_tree.Draw("cluster_hovere/trackPt >> clusterHoE3", cut30)
#    clusterHoEF = ROOT.TH1F("clusterHoEF", "L1EGamma Crystal - Fakes", 80, 0., .2)
#    rate_tree.Draw("cluster_hovere/trackPt >> clusterHoEF")
#    clusterHoEF2 = ROOT.TH1F("clusterHoEF2", "L1EGamma Crystal - Fakes gtr 15p_{T}", 80, 0., .2)
#    rate_tree.Draw("cluster_hovere/trackPt >> clusterHoEF2", cut15)
#    clusterHoEF3 = ROOT.TH1F("clusterHoEF3", "L1EGamma Crystal - Fakes gtr 30p_{T}", 80, 0., .2)
#    rate_tree.Draw("cluster_hovere/trackPt >> clusterHoEF3", cut30)
#    c.SetName("dyncrystalEG_clusterHoEOverTrackPtComp")
#    clusterHoE.GetXaxis().SetTitle("(Cluster H/E)/Track P_{T} (GeV^{-1})")
#    drawDRHists( [clusterHoE,clusterHoE2,clusterHoE3,clusterHoEF,clusterHoEF2,clusterHoEF3], c, .5 )
#    del clusterHoE, clusterHoE2, clusterHoE3, clusterHoEF, clusterHoEF2, clusterHoEF3
#    clusterHoE = ROOT.TH1F("clusterHoE", "L1EGamma Crystal", 80, 0., 5.)
#    crystal_tree.Draw("cluster_hovere >> clusterHoE")
#    clusterHoE2 = ROOT.TH1F("clusterHoE2", "L1EGamma Crystal gtr 15p_{T}", 80, 0., 5.)
#    crystal_tree.Draw("cluster_hovere >> clusterHoE2", cut15)
#    clusterHoE3 = ROOT.TH1F("clusterHoE3", "L1EGamma Crystal gtr 30p_{T}", 80, 0., 5.)
#    crystal_tree.Draw("cluster_hovere >> clusterHoE3", cut30)
#    clusterHoEF = ROOT.TH1F("clusterHoEF", "L1EGamma Crystal - Fakes", 80, 0., 5.)
#    rate_tree.Draw("cluster_hovere >> clusterHoEF")
#    clusterHoEF2 = ROOT.TH1F("clusterHoEF2", "L1EGamma Crystal - Fakes gtr 15p_{T}", 80, 0., 5.)
#    rate_tree.Draw("cluster_hovere >> clusterHoEF2", cut15)
#    clusterHoEF3 = ROOT.TH1F("clusterHoEF3", "L1EGamma Crystal - Fakes gtr 30p_{T}", 80, 0., 5.)
#    rate_tree.Draw("cluster_hovere >> clusterHoEF3", cut30)
#    c.SetName("dyncrystalEG_clusterHoEComp")
#    clusterHoE.GetXaxis().SetTitle("Cluster H/E")
#    drawDRHists( [clusterHoE,clusterHoE2,clusterHoE3,clusterHoEF,clusterHoEF2,clusterHoEF3], c, .35 )
#    del clusterHoE, clusterHoE2, clusterHoE3, clusterHoEF, clusterHoEF2, clusterHoEF3
#
#    # Track Iso Cone
#    clusterIsoConeNumTrks = ROOT.TH1F("clusterIsoConeNumTrks", "L1EGamma Crystal", 80, 0., 10.)
#    crystal_tree.Draw("trackIsoConeTrackCount >> clusterIsoConeNumTrks")
#    clusterIsoConeNumTrks2 = ROOT.TH1F("clusterIsoConeNumTrks2", "L1EGamma Crystal gtr 15p_{T}", 80, 0., 10.)
#    crystal_tree.Draw("trackIsoConeTrackCount >> clusterIsoConeNumTrks2", cut15)
#    clusterIsoConeNumTrks3 = ROOT.TH1F("clusterIsoConeNumTrks3", "L1EGamma Crystal gtr 30p_{T}", 80, 0., 10.)
#    crystal_tree.Draw("trackIsoConeTrackCount >> clusterIsoConeNumTrks3", cut30)
#    clusterIsoConeNumTrksF = ROOT.TH1F("clusterIsoConeNumTrksF", "L1EGamma Crystal - Fakes", 80, 0., 10.)
#    rate_tree.Draw("trackIsoConeTrackCount >> clusterIsoConeNumTrksF")
#    clusterIsoConeNumTrksF2 = ROOT.TH1F("clusterIsoConeNumTrksF2", "L1EGamma Crystal - Fakes gtr 15p_{T}", 80, 0., 10.)
#    rate_tree.Draw("trackIsoConeTrackCount >> clusterIsoConeNumTrksF2", cut15)
#    clusterIsoConeNumTrksF3 = ROOT.TH1F("clusterIsoConeNumTrksF3", "L1EGamma Crystal - Fakes gtr 30p_{T}", 80, 0., 10.)
#    rate_tree.Draw("trackIsoConeTrackCount >> clusterIsoConeNumTrksF3", cut30)
#    c.SetName("dyncrystalEG_clusterIsoConeNumTrksComp")
#    clusterIsoConeNumTrks.GetXaxis().SetTitle("Iso Cone Num Trks")
#    drawDRHists( [clusterIsoConeNumTrks,clusterIsoConeNumTrks2,clusterIsoConeNumTrks3,clusterIsoConeNumTrksF,clusterIsoConeNumTrksF2,clusterIsoConeNumTrksF3], c, 1. )
#    del clusterIsoConeNumTrks, clusterIsoConeNumTrks2, clusterIsoConeNumTrks3, clusterIsoConeNumTrksF, clusterIsoConeNumTrksF2, clusterIsoConeNumTrksF3
#    clusterIsoConePtSum = ROOT.TH1F("clusterIsoConePtSum", "L1EGamma Crystal", 80, 0., 10.)
#    crystal_tree.Draw("trackIsoConePtSum >> clusterIsoConePtSum")
#    clusterIsoConePtSum2 = ROOT.TH1F("clusterIsoConePtSum2", "L1EGamma Crystal gtr 15p_{T}", 80, 0., 10.)
#    crystal_tree.Draw("trackIsoConePtSum >> clusterIsoConePtSum2", cut15)
#    clusterIsoConePtSum3 = ROOT.TH1F("clusterIsoConePtSum3", "L1EGamma Crystal gtr 30p_{T}", 80, 0., 10.)
#    crystal_tree.Draw("trackIsoConePtSum >> clusterIsoConePtSum3", cut30)
#    clusterIsoConePtSumF = ROOT.TH1F("clusterIsoConePtSumF", "L1EGamma Crystal - Fakes", 80, 0., 10.)
#    rate_tree.Draw("trackIsoConePtSum >> clusterIsoConePtSumF")
#    clusterIsoConePtSumF2 = ROOT.TH1F("clusterIsoConePtSumF2", "L1EGamma Crystal - Fakes gtr 15p_{T}", 80, 0., 10.)
#    rate_tree.Draw("trackIsoConePtSum >> clusterIsoConePtSumF2", cut15)
#    clusterIsoConePtSumF3 = ROOT.TH1F("clusterIsoConePtSumF3", "L1EGamma Crystal - Fakes gtr 30p_{T}", 80, 0., 10.)
#    rate_tree.Draw("trackIsoConePtSum >> clusterIsoConePtSumF3", cut30)
#    c.SetName("dyncrystalEG_clusterIsoConePtSumComp")
#    clusterIsoConePtSum.GetXaxis().SetTitle("Iso Cone P_{T} Sum (GeV)")
#    drawDRHists( [clusterIsoConePtSum,clusterIsoConePtSum2,clusterIsoConePtSum3,clusterIsoConePtSumF,clusterIsoConePtSumF2,clusterIsoConePtSumF3], c, .1 )
#    del clusterIsoConePtSum, clusterIsoConePtSum2, clusterIsoConePtSum3, clusterIsoConePtSumF, clusterIsoConePtSumF2, clusterIsoConePtSumF3
#
#    # Shower Shape vars
#    E2x5 = ROOT.TH1F("E2x5", "L1EGamma Crystal", 80, 0., 60.)
#    crystal_tree.Draw("e2x5 >> E2x5")
#    E2x52 = ROOT.TH1F("E2x52", "L1EGamma Crystal gtr 30p_{T}", 80, 0., 60.)
#    crystal_tree.Draw("e2x5 >> E2x52", cut30)
#    E2x5F = ROOT.TH1F("E2x5F", "L1EGamma Crystal - Fakes", 80, 0., 60.)
#    rate_tree.Draw("e2x5 >> E2x5F")
#    E2x5F2 = ROOT.TH1F("E2x5F2", "L1EGamma Crystal - Fakes gtr 30p_{T}", 80, 0., 60.)
#    rate_tree.Draw("e2x5 >> E2x5F2", cut30)
#    c.SetName("dyncrystalEG_E2x5Comp")
#    E2x5.GetXaxis().SetTitle("Energy 2x5 Crystals (GeV)")
#    drawDRHists( [E2x5,E2x52,E2x5F,E2x5F2], c, .4 )
#    del E2x5, E2x52, E2x5F, E2x5F2
#    E5x5 = ROOT.TH1F("E5x5", "L1EGamma Crystal", 80, 0., 60.)
#    crystal_tree.Draw("e5x5 >> E5x5")
#    E5x52 = ROOT.TH1F("E5x52", "L1EGamma Crystal gtr 30p_{T}", 80, 0., 60.)
#    crystal_tree.Draw("e5x5 >> E5x52", cut30)
#    E5x5F = ROOT.TH1F("E5x5F", "L1EGamma Crystal - Fakes", 80, 0., 60.)
#    rate_tree.Draw("e5x5 >> E5x5F")
#    E5x5F2 = ROOT.TH1F("E5x5F2", "L1EGamma Crystal - Fakes gtr 30p_{T}", 80, 0., 60.)
#    rate_tree.Draw("e5x5 >> E5x5F2", cut30)
#    c.SetName("dyncrystalEG_E5x5Comp")
#    E5x5.GetXaxis().SetTitle("Energy 5x5 Crystals (GeV)")
#    drawDRHists( [E5x5,E5x52,E5x5F,E5x5F2], c, .4 )
#    del E5x5, E5x52, E5x5F, E5x5F2
#    ShowerShape = ROOT.TH1F("ShowerShape", "L1EGamma Crystal", 80, 0., 1.)
#    crystal_tree.Draw("(e2x5/e5x5) >> ShowerShape")
#    ShowerShape2 = ROOT.TH1F("ShowerShape2", "L1EGamma Crystal gtr 30p_{T}", 80, 0., 1.)
#    crystal_tree.Draw("(e2x5/e5x5) >> ShowerShape2", cut30)
#    ShowerShapeF = ROOT.TH1F("ShowerShapeF", "L1EGamma Crystal - Fakes", 80, 0., 1.)
#    rate_tree.Draw("(e2x5/e5x5) >> ShowerShapeF")
#    ShowerShapeF2 = ROOT.TH1F("ShowerShapeF2", "L1EGamma Crystal - Fakes gtr 30p_{T}", 80, 0., 1.)
#    rate_tree.Draw("(e2x5/e5x5) >> ShowerShapeF2", cut30)
#    c.SetName("dyncrystalEG_E2x5OverE5x5Comp")
#    ShowerShape.GetXaxis().SetTitle("Energy (2x5)/(5x5)")
#    drawDRHists( [ShowerShape,ShowerShape2,ShowerShapeF,ShowerShapeF2], c, .4 )
#    del ShowerShape, ShowerShape2, ShowerShapeF, ShowerShapeF2
#
#    # Track Pt comparisons for no EG matching for highest pt track (dR < 10) and
#    # normal matching
#    trackPtHist = ROOT.TH1F("trackPtHist", "L1 Trk - EG Matched", 55, 0., 55)
#    crystal_tree.Draw("trackPt >> trackPtHist","")
#    trackPtHist10 = ROOT.TH1F("trackPtHist10", "L1 Trk - EG Matched, P_{T}>10", 55, 0., 55)
#    crystal_tree.Draw("trackPt >> trackPtHist10","trackPt>10")
#    trackFile = ROOT.TFile('egTriggerRateTracks.root','r')
#    print trackFile.ls()
#    trackTree = trackFile.Get('analyzer/crystal_tree')
#    print trackTree.ls()
#    trackPtHistF = ROOT.TH1F("trackPtHistF", "L1 Trk - No Match", 55, 0., 55.)
#    trackTree.Draw("trackPt >> trackPtHistF","")
#    trackPtHistF10 = ROOT.TH1F("trackPtHistF10", "L1 Trk - No Match, P_{T}>10", 55, 0., 55.)
#    trackTree.Draw("trackPt >> trackPtHistF10","trackPt>10")
#    print trackPtHistF.Integral()
#    c.SetName("dyncrystalEG_trackPtEGMatchVNoMatch")
#    trackPtHist.GetXaxis().SetTitle("Track P_{T} (GeV)")
#    c.SetLogy(1)
#    #drawDRHists( [trackPtHist,trackPtHist10,trackPtHistF,trackPtHistF10], c, 10. )
#    drawDRHists( [trackPtHist,trackPtHistF], c, 10. )
#    c.SetLogy(0)
#    del trackPtHist, trackPtHist10, trackPtHistF, trackPtHistF10
#
#
#    # Back to DeltaR stuff
#    #newAlgDRCutsHist = ROOT.TH1F("newAlgDRCutsHist", "L1EGamma Crystal", 50, 0., .25)
#    #crystal_tree.Draw("deltaR >> newAlgDRCutsHist", "passed && gen_pt > 20.", "goff")
#    #c.SetName("dyncrystalEG_deltaR_ptcut")
#    #drawDRHists([newAlgDRCutsHist], c, 0.)
#
#
#    ''' PT RECONSTRUCTION: (reco-gen) / reco '''
#    #c.SetName("dyncrystalEG_RecoGenPt_UW")
#    #drawDRHists([effHists['newAlgGenRecoPtHist'], effHists['UCTAlgGenRecoPtHist'], effHists['dynAlgGenRecoPtHist']], c, 0., [-1., 1.])
#    c.SetName("dyncrystalEG_RecoGenPt")
#    effHists['newAlgGenRecoPtHist'].GetXaxis().SetTitle("P_{T} (reco-gen)/gen")
#    drawDRHists([effHists['newAlgGenRecoPtHist'], effHists['UCTAlgGenRecoPtHist']], c, 0., True)
#    
#
# 
#    c.Clear()
    #brem_dphi = ROOT.TH2F("brem_dphi", "d#phi(uslE+lslE)/clusterEnergy", 50, -0.1, 0.1, 50, 0, 1)
    #crystal_tree.Draw("(uslE+lslE)/cluster_energy : deltaPhi >> brem_dphi", "passed && cluster_pt > 10", "goff")
    #brem_dphi.Draw("colz")
    #c.Print("plots/brem_dphi_hist.png")
 

