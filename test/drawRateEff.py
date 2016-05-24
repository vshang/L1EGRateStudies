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


def drawRates( hists, c, ymax, xrange = [0., 0.] ) :
    c.cd()
    colors = [ROOT.kBlack, ROOT.kRed, ROOT.kBlue, ROOT.kGreen, ROOT.kOrange, ROOT.kGray]
    marker_styles = [20, 24, 25, 26, 32]
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
    mg.GetYaxis().SetTitle("Eff. (L1 Reco/Gen)")
 
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
    stats.append( ROOT.TLatex(histpad_sizeX+margin+0.01, histpad_sizeY+margin+0.13, "#mu_#eta = %.2E" % shape.GetParameter(1)) )
    stats.append( ROOT.TLatex(histpad_sizeX+margin+0.01, histpad_sizeY+margin+0.1,"#mu_#phi = %.2E" % shape.GetParameter(3)) )
    stats.append( ROOT.TLatex(histpad_sizeX+margin+0.01, histpad_sizeY+margin+0.07, "#sigma_#eta#eta = %.2E" % (ROOT.TMath.sqrt(0.5/shape.GetParameter(2)))) )
    stats.append( ROOT.TLatex(histpad_sizeX+margin+0.01, histpad_sizeY+margin+0.04, "#sigma_#phi#phi = %.2E" % (ROOT.TMath.sqrt(0.5/shape.GetParameter(4)))) )
    stats.append( ROOT.TLatex(histpad_sizeX+margin+0.01, histpad_sizeY+margin+0.01, "#sigma_#eta#phi = %.2E" % (ROOT.TMath.sqrt(-0.5/shape.GetParameter(5)))) )
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
    marker_styles = [20, 24, 25, 26, 32]
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
    if ymax != 0. :
        hs.SetMaximum(ymax)
    if ymax == 0. :
        hs.SetMaximum( hs.GetMaximum() * 1.2 )
 
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
        fitRanges = [[-.1, .1],
                    [-0.05, .2]]
        fitResults = []
        for i, hist in enumerate(hists) :
            shape = ROOT.TF1("shape", "gaus(0)", fitRanges[i][0], fitRanges[i][1])
            shape.SetParameters(fitHints[i][0], fitHints[i][1], fitHints[i][2])
            hist.Fit(shape, "R")
            hist.GetFunction("shape").SetLineColor(hist.GetLineColor())
            hist.GetFunction("shape").SetLineWidth(hist.GetLineWidth()*2)

            fitResult = hist.GetFunction("shape")
            fitResults.append( ROOT.TLatex(.75, .7-i*.12, "scale %.2E" % fitResult.GetParameter(0)))
            fitResults.append( ROOT.TLatex(.75, .66-i*.12, "avg. %.2E" % fitResult.GetParameter(1)))
            fitResults.append( ROOT.TLatex(.75, .62-i*.12, "#sigma %.2E" % fitResult.GetParameter(2)))
        for i in range( len(fitResults) ) :
            fitResults[i].SetTextSize(0.035)
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
    c.Clear()
    c.SetCanvasSize(700, 600)
    #c.SetGridx(1)
    #c.SetGridy(1)
    c.SetRightMargin(0.14)
    c.SetTopMargin(0.10)
    recoGenPtHist = effFile.Get("analyzer/reco_gen_pt")
    #recoGenPtHist.SetTitle("Crystal EG algorithm pT resolution")
    recoGenPtHist.SetTitle("")
    recoGenPtHist.GetYaxis().SetTitle("Relative Error (reco-gen)/gen")
    recoGenPtHist.GetYaxis().SetTitleOffset(1.3)
    recoGenPtHist.SetMaximum(50)
    recoGenPtHist.Draw("colz")
    cmsString = drawCMSString("CMS Simulation, <PU>=140 bx=25, Single Electron")
    c.Print("plots/dyncrystalEG_reco_gen_pt.png")
    del cmsString
 

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
    
    ''' RATE SECTION '''    
    c.SetName('dyncrystalEG_rate')
    c.SetTitle('')
    toDraw = [ hists['L1EGamma Crystal'], hists['Phase 1 TDR'] ]
    drawRates( toDraw, c, 40000., xrange)
    
    #c.SetName('dyncrystalEG_rate_UW')
    #c.SetTitle('EG Rates (UW only)')
    #toDraw = [ hists['L1EGamma Crystal'], hists['Phase 1 TDR'], hists['LLR Alg.'] ]
    #drawRates( toDraw, c, 40000., xrange)
    
    ''' EFFICIENCY SECTION '''
    c.SetLogy(0)
    c.SetName("dyncrystalEG_efficiency_eta")
    c.SetTitle("EG Efficiencies")
    drawEfficiency([effHists['newAlgEtaHist'], effHists['UCTAlgEtaHist']], c, 1.2, "Eta", [-3.,3.] , False, [-2.5, 2.5])
    #c.SetName("dyncrystalEG_efficiency_pt_UW")
    #c.SetTitle("EG Efficiencies (UW only)")
    #drawEfficiency([effHists['newAlgPtHist'], effHists['UCTAlgPtHist'], effHists['dynAlgPtHist']], c, 1.2, "Pt (GeV)", xrange, True, [0.9, 2., 1., 0.])
    c.SetName("dyncrystalEG_efficiency_pt")
    c.SetTitle("")
    drawEfficiency([effHists['newAlgPtHist'], effHists['UCTAlgPtHist']], c, 1.2, "Pt (GeV)", xrange, True, [0.9, 2., 1., 0.])

    # Map of possible pt values from file with suggested fit function params
    possiblePts = {'16' : [0.9, 20., 1., 0.], '20' : [0.95, 30., 1., 0.], '30': [0.95, 16., 1., 0.]}
    for crystalPt in crystalAlgGenPtHists :
        toPlot = []
        toPlot.append( crystalPt )
        for UCTPt in UCTAlgGenPtHists :
            for pt in possiblePts.keys() :
                if pt in crystalPt.GetName() and pt in UCTPt.GetName() :
                    print pt, crystalPt.GetName(), UCTPt.GetName()
                    toPlot.append( UCTPt )
                    c.SetName("dyncrystalEG_threshold"+pt+"_efficiency_gen_pt")
                    drawEfficiency( toPlot, c, 1.2, "Pt (GeV)", xrange, True, possiblePts[pt])


    # Offline reco pt
    crystal_tree = effFile.Get("analyzer/crystal_tree")
    offlineRecoHist = ROOT.TH2F("offlineRecoHist", "Offline reco to gen. comparisonGen. pT (GeV)(reco-gen)/genCounts", 60, 0., 50., 60, -0.5, 0.5)
    crystal_tree.Draw("(reco_pt-gen_pt)/gen_pt:gen_pt >> offlineRecoHist", "reco_pt>0", "colz")
    c.SetLogy(0)
    offlineRecoHist.Draw("colz")
    c.Print("plots/offlineReco_vs_gen.png")
    c.Clear()
 
    ''' POSITION RECONSTRUCTION '''
    # Delta R Stuff
    c.SetGridx(0)
    c.SetGridy(0)
    c.SetName("dyncrystalEG_deltaR")
    c.SetTitle("")
    drawDRHists([effHists['newAlgDRHist'], effHists['UCTAlgDRHist']], c, 0.)
    #c.SetName("dyncrystalEG_deltaR_UW")
    #c.SetTitle("")
    #drawDRHists([effHists['newAlgDRHist'], effHists['UCTAlgDRHist'], effHists['dynAlgDRHist']], c, 0.)

    # Delta Eta / Phi
    #c.SetName("dyncrystalEG_deltaEta_UW")
    #drawDRHists([effHists['newAlgDEtaHist'], effHists['UCTAlgDEtaHist'], effHists['dynAlgDEtaHist']], c, 0., [-0.5, 0.5])
    c.SetName("dyncrystalEG_deltaEta")
    drawDRHists([effHists['newAlgDEtaHist'], effHists['UCTAlgDEtaHist']], c, 0.)
    #c.SetName("dyncrystalEG_deltaPhi_UW")
    #drawDRHists([effHists['newAlgDPhiHist'], effHists['UCTAlgDPhiHist'], effHists['dynAlgDPhiHist']], c, 0., [-0.5, 0.5])
    c.SetName("dyncrystalEG_deltaPhi")
    drawDRHists([effHists['newAlgDPhiHist'], effHists['UCTAlgDPhiHist']], c, 0.)

    # Back to DeltaR stuff
    #newAlgDRCutsHist = ROOT.TH1F("newAlgDRCutsHist", "L1EGamma Crystal", 50, 0., .25)
    #crystal_tree.Draw("deltaR >> newAlgDRCutsHist", "passed && gen_pt > 20.", "goff")
    #c.SetName("dyncrystalEG_deltaR_ptcut")
    #drawDRHists([newAlgDRCutsHist], c, 0.)


    ''' PT RECONSTRUCTION: (reco-gen) / reco '''
    #c.SetName("dyncrystalEG_RecoGenPt_UW")
    #drawDRHists([effHists['newAlgGenRecoPtHist'], effHists['UCTAlgGenRecoPtHist'], effHists['dynAlgGenRecoPtHist']], c, 0., [-1., 1.])
    c.SetName("dyncrystalEG_RecoGenPt")
    effHists['newAlgGenRecoPtHist'].GetXaxis().SetTitle("(reco-gen)/gen P_{T} (GeV)")
    drawDRHists([effHists['newAlgGenRecoPtHist'], effHists['UCTAlgGenRecoPtHist']], c, 0., True, [-.2, .2], [99., 99., 99.])
    

 
    c.Clear()
    #brem_dphi = ROOT.TH2F("brem_dphi", "d#phi(uslE+lslE)/clusterEnergy", 50, -0.1, 0.1, 50, 0, 1)
    #crystal_tree.Draw("(uslE+lslE)/cluster_energy : deltaPhi >> brem_dphi", "passed && cluster_pt > 10", "goff")
    #brem_dphi.Draw("colz")
    #c.Print("plots/brem_dphi_hist.png")
 
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


