import ROOT
import trigHelpers
from array import array
from ROOT import gStyle, gPad
import CMS_lumi, tdrstyle
from collections import OrderedDict

qcd = 'qcd_pu0.root'
qcd200 = 'qcd_pu200.root'
ggH = 'ggH.root'
version = '20180911_jets_v2'
#qcd = 'qcd1.root'
#ggH = 'ggH1.root'
#version = '93X_ResolutionsV2'

base = '/data/truggles/p2/20180911_jets_v2/'
universalSaveDir = "/afs/cern.ch/user/t/truggles/www/Phase-II/"+version+"/"

qcd0File = ROOT.TFile( base+qcd, 'r' )
qcd200File = ROOT.TFile( base+qcd200, 'r' )
#ggHHTTFile = ROOT.TFile( base+ggH, 'r' )

def loadHists( file_, histMap = {}, eff=False ) :
    hists = {}
    for h, path in histMap.iteritems() :
        print h, path
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
    leg.SetFillStyle(1001)
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
    c.Print(universalSaveDir+c.GetTitle()+".png")
    #c.Print(universalSaveDir+c.GetTitle()+".pdf")
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
    cmsString = drawCMSString("CMS Simulation, <PU>=200 bx=25, Single Electron")
    c.Print(universalSaveDir+name+"_reco_gen_pt.png")
    #c.Print(universalSaveDir+name+"_reco_gen_pt.pdf")
    #c.Print(universalSaveDir+name+"_reco_gen_pt.C")
    del cmsString


def drawRates( hists, c, ymax, xrange = [0., 0.] ) :
    c.cd()
    colors = [ROOT.kBlack, ROOT.kRed, ROOT.kBlue, ROOT.kGreen, ROOT.kOrange, ROOT.kGray]
    marker_styles = [20, 24, 25, 26, 32, 35]
    if 'MANY' in c.GetName() :
        colors = [i for i in range(3, 35)]
        marker_styles = [i for i in range( 20, 45)]
    c.Clear()
    mg = ROOT.TMultiGraph("mg", c.GetTitle())
    
    graphs = []
    for i, hist in enumerate(hists) :
        graph = ROOT.TGraphErrors( hist )
        graph.SetMarkerStyle( marker_styles[i] )
        graph.SetMarkerSize( 0.8 )
        graph.SetLineWidth( 2 )
        if 'MANY' in c.GetName() and graph.GetTitle() == 'Phase-2 L1EG (Crystal)' :
            graph.SetLineWidth( 3 )
            graph.SetLineColor( ROOT.kBlack )
            graph.SetMarkerColor( ROOT.kBlack )
        elif 'MANY' in c.GetName() and graph.GetTitle() == 'Phase-2 L1EG (Crystal + Trk) Electron' :
            graph.SetLineWidth( 3 )
            graph.SetLineColor( ROOT.kRed )
            graph.SetMarkerColor( ROOT.kRed )
        elif 'MANY' in c.GetName() and graph.GetTitle() == 'Phase-1 L1EG (Tower)' :
            graph.SetLineWidth( 3 )
            graph.SetLineColor( ROOT.kOrange+4 )
            graph.SetMarkerColor( ROOT.kOrange+4 )
        else :
            graph.SetLineColor( colors[i] )
            graph.SetMarkerColor( colors[i] )
        mg.Add( graph )
        graphs.append( graph )
    
    mg.Draw("aplez")
    
    if c.GetLogy() == 0 : # linear
        mg.SetMinimum(0.)
    else :
        mg.SetMinimum(1.)
    
    if ymax != 0. :
        mg.SetMaximum( ymax ) 
    
    #leg = setLegStyle(0.53,0.78,0.95,0.92)
    leg = setLegStyle(0.45,0.6,0.95,0.92)
    for graph in graphs :
        leg.AddEntry(graph, graph.GetTitle().replace(' PtAdj',''),"lpe")
    leg.Draw("same")
    c.Update()
    
    mg.GetXaxis().SetTitle(hists[0].GetXaxis().GetTitle())
    if xrange[0] != 0. or xrange[1] != 0 :
        mg.GetXaxis().SetRangeUser(xrange[0], xrange[1])
        #mg.SetAxisRange(xrange[0], xrange[1])
    mg.GetYaxis().SetTitle(hists[0].GetYaxis().GetTitle())
    
    cmsString = drawCMSString("CMS Simulation, <PU>=200 bx=25, MinBias")
    ROOT.gPad.SetGrid()
    
    c.Print(universalSaveDir+c.GetName()+".png")
    c.Print(universalSaveDir+c.GetName()+".pdf")
    c.Print(universalSaveDir+c.GetName()+".C")


def drawEfficiency( hists, c, ymax, xTitle, xrange = [0., 0.], fit = False, fitHint = [1., 15., 3., 0.]) :
    c.cd()
    colors = [ROOT.kBlack, ROOT.kRed, ROOT.kBlue, ROOT.kGreen, ROOT.kOrange, ROOT.kGray]
    marker_styles = [20, 24, 25, 26, 32]
    if 'MANY' in c.GetName() :
        colors = [i for i in range(3, 25)]
        marker_styles = [i for i in range( 20, 45)]
    lines = [ROOT.kSolid, ROOT.kDashed, ROOT.kDotted]
    c.Clear()
    mg = ROOT.TMultiGraph("mg", c.GetTitle())
    
    graphs = []
    for i, hist in enumerate(hists) :
        graph = ROOT.TGraphAsymmErrors( hist )
        graph.SetLineColor( colors[i] )
        graph.SetLineWidth( 2 )
        graph.SetMarkerColor( colors[i] )
        graph.SetMarkerStyle( marker_styles[i] )
        graph.SetMarkerSize( 0.8 )
        if 'MANY' in c.GetName() and graph.GetTitle() == 'Phase-2 L1EG (Crystal)' :
            graph.SetLineColor( ROOT.kBlack )
            graph.SetMarkerColor( ROOT.kBlack )
        if 'MANY' in c.GetName() and graph.GetTitle() == 'Phase-2 L1EG (Crystal + Trk) Electron' :
            graph.SetLineColor( ROOT.kRed )
            graph.SetMarkerColor( ROOT.kRed )
        if 'MANY' in c.GetName() and graph.GetTitle() == 'Phase-1 L1EG (Tower)' :
            graph.SetLineColor( ROOT.kOrange+4 )
            graph.SetMarkerColor( ROOT.kOrange+4 )
        mg.Add( graph )
        graphs.append( graph )
    
    mg.Draw("aplez")
    #mg.Draw("apez")
    mg.GetYaxis().SetNdivisions(13)
    ROOT.gPad.Update()

    if c.GetLogy() == 0 : # linear
        mg.SetMinimum(0.)
    else :
        mg.SetMinimum(10.)
    
    if ymax != 0. :
        mg.SetMaximum( ymax ) 

    # TMP XXX FIXME
    #mg.SetMinimum( 0.7 )
    #mg.SetMaximum( 1.1 )
    

    if ( fit and xrange[1] != xrange[0] ) :
       gStyle.SetOptFit(0)
       for j, graph in enumerate(graphs) :
          shape = ROOT.TF1("shape", "[0]/2*(1+TMath::Erf((x-[1])/([2]*TMath::Sqrt(x))))+[3]*x", xrange[0], xrange[1])
          shape.SetParameters(fitHint[0], fitHint[1], fitHint[2], fitHint[3])
          # Somehow, step size increases each time, have to find a way to control it...
          graph.Fit(shape)
          graph.GetFunction("shape").SetLineColor(graph.GetLineColor())
          graph.GetFunction("shape").SetLineWidth(graph.GetLineWidth()*2)
 
    if "gen_to_l1Track_match" in c.GetName() :
        leg = setLegStyle(0.25,0.77,0.94,0.94)
    else :
        leg = setLegStyle(0.48,0.77,0.94,0.94)
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
 
    if 'combo' in c.GetName() :
        cmsString = drawCMSString("CMS Simulation, <PU>=200 bx=25, Single Electron/Photon")
    else :
        cmsString = drawCMSString("CMS Simulation, <PU>=200 bx=25, Single Electron")
    #cmsString = drawCMSString("CMS Simulation, <PU>=200 bx=25, Single Photon")
 
    c.Print((universalSaveDir+c.GetName()+".png"))
    c.Print((universalSaveDir+c.GetName()+".pdf"))
    c.Print((universalSaveDir+c.GetName()+".C"))


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
    gPad.SetLogz()
    hist.GetXaxis().SetTitle("d#eta(reco-gen)")
    hist.GetYaxis().SetTitle("d#phi(reco-gen)")
    hist.GetYaxis().SetTitleOffset(1.4)
    
    # Fit hist
    shape = ROOT.TF2("2dshape", "[0]*TMath::Exp(-[2]*(x[0]-[1])**2-[4]*(x[1]-[3])**2-2*[5]*(x[0]-[1])*(x[1]-[3]))", -0.05, 0.05, -0.05, 0.05)
    shape.SetParameters(0.003, 0., 3.769e4, 0., 4.215e4, -1.763e4)
    hist.Fit(shape, "n")
    max_ = shape.GetParameter(0)
    contours = array('d', [])
    contours.append( max_*ROOT.TMath.Exp(-4.5))
    contours.append( max_*ROOT.TMath.Exp(-2))
    contours.append( max_*ROOT.TMath.Exp(-0.5))
    shape.SetContour(3, contours)
    shape.SetNpx(100)
    shape.SetNpy(100)
    shape.SetLineWidth(2)
    shape.SetLineColor(ROOT.kBlack)
    shape.Draw("cont3 same")
    
    # One crystal box
    crystalBox = ROOT.TBox(-0.0173/2, -0.0173/2, 0.0173/2, 0.0173/2)
    crystalBox.SetLineStyle(3)
    crystalBox.SetLineColor(13)
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
    shapeprojX = ROOT.TF1("shapeprojX", "[0]*TMath::Sqrt(([2]*[4]-[5]**2)/(TMath::Pi()*[2]))*exp(([5]**2-[2]*[4])*(x-[3])**2/[2])", -0.05, 0.05)
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
    shapeprojY = ROOT.TF1("shapeprojY", "[0]*TMath::Sqrt(([2]*[4]-[5]**2)/(TMath::Pi()*[4]))*exp(([5]**2-[2]*[4])*(x-[1])**2/[4])", -0.05, 0.05)
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
       "CMS Simulation, <PU>=200 bx=25, Single Electron")
       #"CMS Simulation, <PU>=200 bx=25, Single Photon")
    cmsString.SetTextFont(42)
    cmsString.SetTextSize(0.02)
    cmsString.SetNDC(1)
    cmsString.SetTextAlign(33)
    cmsString.Draw()
 
    # Stats
    stats = []
    stats.append( ROOT.TLatex(histpad_sizeX+margin+0.01, histpad_sizeY+margin+0.13, "#mu_#eta = "+format(shape.GetParameter(1), '.2g' )) )
    stats.append( ROOT.TLatex(histpad_sizeX+margin+0.01, histpad_sizeY+margin+0.1,"#mu_#phi = "+format(shape.GetParameter(3), '.2g')) )
    stats.append( ROOT.TLatex(histpad_sizeX+margin+0.01, histpad_sizeY+margin+0.07, "#sigma_#eta#eta = "+format(ROOT.TMath.Sqrt(0.5/shape.GetParameter(2)), '.2g')) )
    stats.append( ROOT.TLatex(histpad_sizeX+margin+0.01, histpad_sizeY+margin+0.04, "#sigma_#phi#phi = "+format(ROOT.TMath.Sqrt(0.5/shape.GetParameter(4)), '.2g')) )
    stats.append( ROOT.TLatex(histpad_sizeX+margin+0.01, histpad_sizeY+margin+0.01, "#sigma_#eta#phi = "+format(ROOT.TMath.Sqrt(-0.5/shape.GetParameter(5)), '.2g')) )
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
    #gPad.SetLogz()
    gPad.Modified()
    gPad.Update()
 
    c.Print(universalSaveDir+c.GetName()+".png")
    #c.Print(universalSaveDir+c.GetName()+".pdf")
 
    gStyle.SetOptTitle(1)


def drawDRHists(hists, c, ymax, doFit = False ) :
    c.cd()
    colors = [ROOT.kBlack, ROOT.kRed, ROOT.kBlue, ROOT.kGreen, ROOT.kOrange, ROOT.kGray+2]
    marker_styles = [20, 24, 25, 26, 32, 35]
    hs = ROOT.THStack("hs", c.GetTitle())
    maxi = 0.
    for i, hist in enumerate(hists) :
        hist.Sumw2()
        hist.Scale(1./hist.Integral())
        hist.SetLineColor(colors[i])
        hist.SetLineWidth(2)
        hist.SetMarkerColor(colors[i])
        hist.SetMarkerStyle(marker_styles[i])
        hist.SetMarkerSize(0.8)
        if hist.GetMaximum() > maxi : maxi = hist.GetMaximum()
        hs.Add(hist, "ex0 hist")

    c.Clear()
    #if c.GetName() == 'ecal_dimensions_check' :
    #    c.SetLogy()
    #else :
    #    c.SetLogy(0)

    if c.GetLogy() == 0 : # linear
        hs.SetMinimum(0.)
    if ymax == 0. :
        hs.SetMaximum( maxi * 1.8 )
    elif ymax == -1 :
        hs.SetMaximum( maxi * 1.3 )
    elif ymax != 0. :
        hs.SetMaximum(ymax)
    if 'dimensions_check' in c.GetName() :
        hs.SetMaximum( maxi * 1.1 )
    #if 'ecal_dimensions_check' in c.GetName() :
    #    hs.SetMaximum( maxi * 50 )

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
 
    #leg = setLegStyle(0.53,0.78,0.95,0.92)
    #leg = setLegStyle(0.5,0.7,0.9,0.9)
    leg = setLegStyle(0.5,0.5,0.9,0.9)
    for hist in hists :
        leg.AddEntry(hist, hist.GetTitle(),"elp")
    leg.Draw("same")
    c.Update()

    hs.GetXaxis().SetTitle(hists[0].GetXaxis().GetTitle())
    #hs.GetYaxis().SetTitle(hists[0].GetYaxis().GetTitle())
    hs.GetYaxis().SetTitleOffset(1.2)
    hs.GetYaxis().SetTitle("Fraction of Events")
    if c.GetName() == "dyncrystalEG_deltaR2" :
        hs.GetXaxis().SetRangeUser(0., 0.15)
 
    if "Stage2" in c.GetName() :
        cmsString = drawCMSString("CMS Simulation")
    else :
        #cmsString = drawCMSString("CMS Simulation, <PU>=200 bx=25, Single Electron")
        cmsString = drawCMSString("CMS Simulation")
        #cmsString = drawCMSString("CMS Simulation, <PU>=200 bx=25, Min-Bias")
                
    c.Print(universalSaveDir+c.GetName()+".png")
    c.Print(universalSaveDir+c.GetName()+".pdf")
    c.Print(universalSaveDir+c.GetName()+".C")

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
    #cmsString2 = drawCMSString("CMS Simulation, <PU>=200 bx=25, Single Electron")
    #c.Print( "plots/"+c.GetName()+"_cdf.png" )

    if doFit :
        gStyle.SetOptFit(0)
        # Poorly done hard coding for fit suggestions
        # and fit ranges, sorry
        fitHints = [[0.2, 0.1, 0.1],
                    [0.2, 0.1, .1 ]]
        fitRanges = [[-.15, .08],
                    [-0.09, .3]]
        fitResults = []
        fitResults.append( ROOT.TLatex(.2, .7, "Gaussian Fits:" ))
        for i, hist in enumerate(hists) :
            print i, hist

            # Fit +/- .05 around max
            hist_max = hist.GetBinCenter( hist.GetMaximumBin() )
            #shape = ROOT.TF1("shape", "gaus(0)", fitRanges[i][0], fitRanges[i][1])
            #shape = ROOT.TF1("shape", "gaus(0)", hist_max - 0.05, hist_max + 0.05 )
            #shape.SetParameters(fitHints[i][0], fitHints[i][1], fitHints[i][2], \
            #shape = ROOT.TF1("shape", "gaus(0) + gaus(3)", hist_max - 0.05, hist_max + 0.05 )
            #shape = ROOT.TF1("shape", "gaus(0) + gaus(3)", 0.6, 1.1 )
            
            #shape = ROOT.TF1("shape", "gaus(0) + [3]*[3]", 0.6, 1.0)
            #shape.SetParameters( fitHints[i][0], fitHints[i][1], fitHints[i][2], 0.1 )
            shape = ROOT.TF1("shape", "gaus(0)", hist_max - 0.05, hist_max + 0.05 )
            shape.SetParameters(fitHints[i][0], fitHints[i][1], fitHints[i][2])
                
            hist.Fit(shape, "R")
            hist.GetFunction("shape").SetLineColor(hist.GetLineColor())
            hist.GetFunction("shape").SetLineWidth(hist.GetLineWidth()*2)

            fitResult = hist.GetFunction("shape")
            fitResults.append( ROOT.TLatex(.2, .66-i*.13, "#mu: "+format(fitResult.GetParameter(1), '.3g')))
            fitResults.append( ROOT.TLatex(.2, .62-i*.13, "#sigma: "+format(ROOT.TMath.Sqrt(.5*abs(fitResult.GetParameter(2))), '.3g')))
            fitResults.append( ROOT.TLatex(.2, .58-i*.13, "mean: "+format(hist.GetMean(1), '.3g')))
        for i in range( len(fitResults) ) :
            fitResults[i].SetTextSize(0.045)
            fitResults[i].SetTextFont(42)
            fitResults[i].SetNDC()
            if i > 3 : fitResults[i].SetTextColor(ROOT.kRed)
            fitResults[i].Draw()

        c.Print( universalSaveDir+c.GetName()+"_fit.png" )
        c.Print( universalSaveDir+c.GetName()+"_fit.pdf" )

    c.Clear()
 
def simple1D( name, tree, iii, var, info, cut="" ) :
    h = ROOT.TH1F("%i" % iii[0], name+' '+var+';'+var, info[0], info[1], info[2])
    tree.Draw( var + " >> %i" % iii[0], cut )
    h.SetDirectory(0)
    iii[0] += 1
    return h
    


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

    
    
    tree_qcd0 = qcd0File.Get("analyzer/tree")
    tree_qcd200 = qcd200File.Get("analyzer/tree")
    #tree_ggH = ggHHTTFile.Get("analyzer/tree")
    tdrstyle.setTDRStyle()
    gStyle.SetOptStat(0)

    
    c = ROOT.TCanvas('c', 'c', 1200, 1000)
    ROOT.gPad.SetRightMargin( ROOT.gPad.GetRightMargin() * 2.5 )
    c.SetTitle('')
    c.SetGridx(1)
    c.SetGridy(1)
    #gStyle.SetGridStyle(2)
    #gStyle.SetGridColor(ROOT.kGray+1)
    

    min_ = 0.
    max_ = 3.0
    #max_ = 1.5
    tmpAry=[120,min_,max_]
    varList = [
        'jet_pt/genJet_pt',
        'jet_energy/genJet_energy',
        'ecal_pt/genJet_pt',
        'hcal_pt/genJet_pt',
        'stage2jet_pt/genJet_pt',
        'stage2jet_deltaRGen',
        'deltaR_gen',

        #'hcal_dR3T/genJet_energy',
        #'hcal_dR4T/genJet_energy',
        #'hcal_dR5T/genJet_energy',
        #'ecal_dR0p3/genJet_energy',
        #'ecal_dR0p4/genJet_energy',
        #'ecal_dR0p5/genJet_energy',

        #'stage2tau_pt/genJet_pt',

        #'genTau_pt/genJet_pt',

        #'jet_pt/genTau_pt',
        #'ecal_pt/genTau_pt',
        #'hcal_pt/genTau_pt',
        #'stage2jet_pt/genTau_pt',
        #'stage2tau_pt/genTau_pt',
    ]
    cnt = [0]
    baseline_cuts = "(genJet_pt > 40 || genTau_pt > 40) && (genJet_pt < 500 && genTau_pt < 500)"
    baseline_cuts = "(genJet_pt > 40 && abs(genJet_eta) < 1.1)"
    #for var in varList :
    #    h1 = simple1D( 'QCD Jets PU0', tree_qcd0, cnt, var, tmpAry, baseline_cuts )
    #    h2 = simple1D( 'QCD Jets PU200', tree_qcd200, cnt, var, tmpAry, baseline_cuts )
    #    c.SetName("ptResolutionGenPtGtr20_"+var.replace('/','_'))
    #    #drawDRHists([h1,h2], c, 0., True ) # doFit
    #    drawDRHists([h1,h2], c, 0., False ) # no Fit


    max_ = 1.5
    tmpAry=[50,min_,max_]
    hists0 = []
    hists200 = []
    dr_map = {
        'seed_energy' : 'HCAL Seed',
        'dR1T' : '3x3 TT',
        'dR2T' : '5x5 TT',
        'dR3T' : '7x7 TT',
        'dR4T' : '9x9 TT',
        'dR5T' : '11x11 TT'
    }
    #for dr in ['seed_energy', 'dR1T', 'dR2T', 'dR3T', 'dR4T', 'dR5T'] :
    #    hists0.append( simple1D( 'QCD Jets '+dr, tree_qcd0, cnt, '(hcal_'+dr+')/genJet_energy', tmpAry, baseline_cuts ) )
    #    hists0[-1].SetTitle('QCD Jets '+dr_map[dr])
    #    hists0[-1].GetXaxis().SetTitle('HCAL Energy / Gen Energy')
    #c.SetName("hcal_dimensions_check")
    #drawDRHists(hists0, c, 0., False ) # no Fit
    #hists0 = []
    #max_ = 1.
    #tmpAry=[25,min_,max_]
    ##for dr in ['leading_energy', 'dR0p1', 'dR0p2', 'dR0p3', 'dR0p4', 'dR0p5'] :
    #for dr in ['dR0p05', 'dR0p1', 'dR0p2', 'dR0p3', 'dR0p4', 'dR0p5'] :
    #    hists0.append( simple1D( 'QCD Jet '+dr, tree_qcd0, cnt, '(ecal_'+dr+')/genJet_energy', tmpAry, baseline_cuts ) )
    #    hists0[-1].SetTitle('QCD Jets '+dr)
    #    hists0[-1].GetXaxis().SetTitle('ECAL Energy / Gen Energy')
    #c.SetName("ecal_dimensions_check")
    #drawDRHists(hists0, c, 0., False ) # no Fit


    hists = []
    max_ = 0.5
    tmpAry=[50,min_,max_]
    dr_map = {
        'deltaR_gen' : 'Phase-2 Jets',
        'stage2jet_deltaRGen' : 'Stage-2 Jets',
        'stage2tau_deltaRGen' : 'Stage-2 Taus'
    }
    #for dr in ['leading_energy', 'dR0p1', 'dR0p2', 'dR0p3', 'dR0p4', 'dR0p5'] :
    #for dr in ['deltaR_gen', 'stage2jet_deltaRGen', 'stage2tau_deltaRGen'] :
    for dr in ['deltaR_gen', 'stage2jet_deltaRGen'] :
        hists.append( simple1D( 'QCD Jet '+dr, tree_qcd0, cnt, dr, tmpAry, baseline_cuts ) )
        hists[-1].SetTitle(dr_map[dr]+' PU 0')
        hists[-1].GetXaxis().SetTitle('#Delta R(L1 Obj, Gen)')
        hists.append( simple1D( 'QCD Jet '+dr, tree_qcd200, cnt, dr, tmpAry, baseline_cuts ) )
        hists[-1].SetTitle(dr_map[dr]+' PU 200')
        hists[-1].GetXaxis().SetTitle('#Delta R(L1 Obj, Gen)')
    c.SetName("dr_dimensions_check")
    drawDRHists(hists, c, 0., False ) # no Fit



    hists = []
    max_ = 3.0
    min_ = 0.
    tmpAry=[50,min_,max_]
    dr_map = {
        'jet_pt/genJet_pt' : 'Phase-2 Jets',
        'stage2jet_pt/genJet_pt' : 'Stage-2 Jets',
        'stage2tau_pt/genJet_pt' : 'Stage-2 Taus'
    }
    #for dr in ['leading_energy', 'dR0p1', 'dR0p2', 'dR0p3', 'dR0p4', 'dR0p5'] :
    #for dr in ['deltaR_gen', 'stage2jet_deltaRGen', 'stage2tau_deltaRGen'] :
    for dr in ['jet_pt/genJet_pt', 'stage2jet_pt/genJet_pt'] :
        hists.append( simple1D( 'QCD Jet '+dr, tree_qcd0, cnt, dr, tmpAry, baseline_cuts ) )
        hists[-1].SetTitle(dr_map[dr]+' PU 0')
        hists[-1].GetXaxis().SetTitle('Reco p_{T} / Gen p_{T}')
        hists.append( simple1D( 'QCD Jet '+dr, tree_qcd200, cnt, dr, tmpAry, baseline_cuts ) )
        hists[-1].SetTitle(dr_map[dr]+' PU 200')
        hists[-1].GetXaxis().SetTitle('Reco p_{T} / Gen p_{T}')
    c.SetName("dPt_res_check")
    drawDRHists(hists, c, 0., False ) # no Fit


        #'jet_pt/genTau_pt',
        #'ecal_pt/genTau_pt',
        #'hcal_pt/genTau_pt',
        #'stage2jet_pt/genTau_pt',







