import ROOT
from ROOT import gStyle, gPad

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


def drawRates( hists, can, ymax, xrange = [0., 0.] ) :
    can.cd()
    colors = [ROOT.kBlack, ROOT.kRed, ROOT.kBlue, ROOT.kGreen, ROOT.kOrange, ROOT.kGray]
    marker_styles = [20, 24, 25, 26, 32]
    can.Clear()
    mg = ROOT.TMultiGraph("mg", can.GetTitle())
    
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
    
    if can.GetLogy() == 0 : # linear
        mg.SetMinimum(0.)
    else :
        mg.SetMinimum(10.)
    
    if ymax != 0. :
        mg.SetMaximum( ymax ) 
    
    leg = setLegStyle(0.5,0.76,0.9,0.9)
    for graph in graphs :
        leg.AddEntry(graph, graph.GetTitle(),"lpe")
    leg.Draw("same")
    can.Update()
    
    mg.GetXaxis().SetTitle(hists[0].GetXaxis().GetTitle())
    if xrange[0] != 0. or xrange[1] != 0 :
        mg.GetXaxis().SetRangeUser(xrange[0], xrange[1])
    mg.GetYaxis().SetTitle(hists[0].GetYaxis().GetTitle())
    
    cmsString = drawCMSString("CMS Simulation, <PU>=140 bx=25, MinBias")
    
    can.Print("plots/"+can.GetName()+".png")


def drawEfficiency( hists, can, ymax, xrange = [0., 0.], fit = False, fitHint = [1., 15., 3., 0.]) :
    can.cd()
    colors = [ROOT.kBlack, ROOT.kRed, ROOT.kBlue, ROOT.kGreen, ROOT.kOrange, ROOT.kGray]
    marker_styles = [20, 24, 25, 26, 32]
    lines = [ROOT.kSolid, ROOT.kDashed, ROOT.kDotted]
    can.Clear()
    mg = ROOT.TMultiGraph("mg", can.GetTitle())
    
    graphs = []
    for i, hist in enumerate(hists) :
        print hist
        #hist.Scale( 1./hist.GetEntries() )
        graph = ROOT.TGraphAsymmErrors( hist )
        graph.SetLineColor( colors[i] )
        graph.SetMarkerColor( colors[i] )
        graph.SetMarkerStyle( marker_styles[i] )
        graph.SetMarkerSize( 0.8 )
        mg.Add( graph )
        graphs.append( graph )
    
    mg.Draw("aplez")

    if can.GetLogy() == 0 : # linear
        mg.SetMinimum(0.)
    else :
        mg.SetMinimum(10.)
    
    if ymax != 0. :
        mg.SetMaximum( ymax ) 
    

    if ( fit and xrange[1] != xrange[0] ) :
       for j, graph in enumerate(graphs) :
          shape = ROOT.TF1("shape", "[0]/2*(1+TMath::Erf((x-[1])/([2]*sqrt(x))))+[3]*x", xrange[0], xrange[1])
          shape.SetParameters(fitHint[0], fitHint[1], fitHint[2], fitHint[3])
          # Somehow, step size increases each time, have to find a way to control it...
          graph.Fit(shape)
          graph.GetFunction("shape").SetLineColor(graph.GetLineColor())
          graph.GetFunction("shape").SetLineWidth(graph.GetLineWidth()*2)
          graph.GetFunction("shape").SetLineStyle(lines[j])
 
    leg = setLegStyle(0.5,0.76,0.9,0.9)
    for graph in graphs :
        leg.AddEntry(graph, graph.GetTitle(),"lpe")
    leg.Draw("same")
    can.Update()
    
    mg.GetXaxis().SetTitle(graphs[0].GetXaxis().GetTitle())
    if ( xrange[0] != 0. or xrange[1] != 0 ) :
        mg.GetXaxis().SetRangeUser(xrange[0], xrange[1])
    mg.GetYaxis().SetTitle(graphs[0].GetYaxis().GetTitle())
 
    cmsString = drawCMSString("CMS Simulation, <PU>=140 bx=25, Single Electron")
 
    can.Print(("plots/"+can.GetName()+".png"))



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
        'L1EGamma_Crystal' : 'analyzer/dyncrystalEG_rate',
        'Original L2 Algorithm' : 'analyzer/SLHCL1ExtraParticles:EGamma_rate',
        'Phase 1 TDR' : 'analyzer/l1extraParticlesUCT:All_rate',
        'LLR Alg.' : 'analyzer/SLHCL1ExtraParticlesNewClustering:EGamma_rate',
        'Run 1 Alg.' : 'analyzer/l1extraParticles:All_rate',
        'Crystal Trigger (prod.)' : 'analyzer/L1EGammaCrystalsProducer:EGammaCrystal_rate',}

    effMap = {
        'newAlgEtaHist' : ('L1EGamma_Crystal', 'analyzer/divide_dyncrystalEG_efficiency_eta_by_gen_eta'),
        'newAlgPtHist' : ('L1EGamma_Crystal', 'analyzer/divide_dyncrystalEG_efficiency_pt_by_gen_pt'),
        'newAlgDRHist' : ('L1EGamma_Crystal', 'analyzer/dyncrystalEG_deltaR'),
        'oldAlgEtaHist' : ('Original L2 Algorithm', 'analyzer/divide_SLHCL1ExtraParticles:EGamma_efficiency_eta_by_gen_eta'),
        'oldAlgPtHist' : ('Original L2 Algorithm', 'analyzer/divide_SLHCL1ExtraParticles:EGamma_efficiency_pt_by_gen_pt'),
        'oldAlgDRHist' : ('Original L2 Algorithm', 'analyzer/SLHCL1ExtraParticles:EGamma_deltaR'),
        'dynAlgEtaHist' : ('LLR Alg.', 'analyzer/divide_SLHCL1ExtraParticlesNewClustering:EGamma_efficiency_eta_by_gen_eta'),
        'dynAlgPtHist' : ('LLR Alg.', 'analyzer/divide_SLHCL1ExtraParticlesNewClustering:EGamma_efficiency_pt_by_gen_pt'),
        'dynAlgDRHist' : ('LLR Alg.', 'analyzer/SLHCL1ExtraParticlesNewClustering:EGamma_deltaR'),
        'run1AlgEtaHist' : ('Run 1 Alg.', 'analyzer/divide_l1extraParticles:All_efficiency_eta_by_gen_eta'),
        'run1AlgPtHist' : ('Run 1 Alg.', 'analyzer/divide_l1extraParticles:All_efficiency_pt_by_gen_pt'),
        'run1AlgDRHist' : ('Run 1 Alg.', 'analyzer/l1extraParticles:All_deltaR'),
        'UCTAlgEtaHist' : ('Phase 1 TDR', 'analyzer/divide_l1extraParticlesUCT:All_efficiency_eta_by_gen_eta'),
        'UCTAlgPtHist' : ('Phase 1 TDR', 'analyzer/divide_l1extraParticlesUCT:All_efficiency_pt_by_gen_pt'),
        'UCTAlgDRHist' : ('Phase 1 TDR', 'analyzer/l1extraParticlesUCT:All_deltaR'),
    }
    
    rateFile = ROOT.TFile( 'egTriggerRates.root', 'r' )
    effFile = ROOT.TFile( 'egTriggerEff.root', 'r' )
    
    hists = loadHists( rateFile, ratesMap )
    effHists = loadHists( effFile, effMap )
    
    xrange = [0., 50.]
    c1 = ROOT.TCanvas('c1', 'c1', 800, 600)
    c1.SetLogy(1)
    c1.SetGridx(1)
    c1.SetGridy(1)
    gStyle.SetGridStyle(2)
    gStyle.SetGridColor(ROOT.kGray+1)
    
    ''' RATE SECTION '''    
    c1.SetName('dyncrystalEG_rate')
    c1.SetTitle('')
    toDraw = [ hists['L1EGamma_Crystal'], hists['Phase 1 TDR'] ]
    drawRates( toDraw, c1, 40000., xrange)
    
    c1.SetName('dyncrystalEG_rate_UW')
    c1.SetTitle('EG Rates (UW only)')
    toDraw = [ hists['L1EGamma_Crystal'], hists['Phase 1 TDR'], hists['LLR Alg.'] ]
    drawRates( toDraw, c1, 40000., xrange)
    
    ''' EFFICIENCY SECTION '''
    c1.SetLogy(0)
    c1.SetName("dyncrystalEG_efficiency_eta")
    c1.SetTitle("EG Efficiencies")
    drawEfficiency([effHists['newAlgEtaHist'], effHists['UCTAlgEtaHist'], effHists['dynAlgEtaHist']], c1, 1.2, [-3.,3.] , False, [-2.5, 2.5])
    c1.SetName("dyncrystalEG_efficiency_pt_UW")
    c1.SetTitle("EG Efficiencies (UW only)")
    drawEfficiency([effHists['newAlgPtHist'], effHists['UCTAlgPtHist'], effHists['dynAlgPtHist']], c1, 1.2, xrange, True, [0.9, 2., 1., 0.])
    c1.SetName("dyncrystalEG_efficiency_pt")
    c1.SetTitle("")
    drawEfficiency([effHists['newAlgPtHist'], effHists['UCTAlgPtHist']], c1, 1.2, xrange, True, [0.9, 2., 1., 0.])
#    c1.SetName("dyncrystalEG_threshold20_efficiency_gen_pt")
#    # c1.SetTitle("EG Turn-On Efficiencies, 20GeV Threshold")
#    drawEfficiency([effMap['crystalAlgGenPtHists[0], effMap['UCTAlgGenPtHists[0]], c1, 1.2, xrange, True, [0.9, 20., 1., 0.])
#    c1.SetName("dyncrystalEG_threshold30_efficiency_gen_pt")
#    # c1.SetTitle("EG Turn-On Efficiencies, 30GeV Threshold")
#    drawEfficiency([effMap['crystalAlgGenPtHists[1], effMap['UCTAlgGenPtHists[1]], c1, 1.2, xrange, True, [0.95, 30., 1., 0.])
#    c1.SetName("dyncrystalEG_threshold16_efficiency_gen_pt")
#    # c1.SetTitle("EG Turn-On Efficiencies, 16GeV Threshold")
#    drawEfficiency([effMap['crystalAlgGenPtHists[2], effMap['UCTAlgGenPtHists[2]], c1, 1.2, xrange, True, [0.95, 16., 1., 0.])




