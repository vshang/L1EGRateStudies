import ROOT
import os
ROOT.gROOT.SetBatch(False)

def checkDir( plotDir ) :
    if not os.path.exists( plotDir ) : os.makedirs( plotDir )

def getKeysOfClass( file_, dir_, class_ ) :
    keys = []
    d = file_.Get( dir_ )
    allKeys = d.GetListOfKeys()

    #print "keys of class"
    for k in allKeys :
        if k.GetClassName() == class_ :
            keys.append( k )

    return keys


def loadObjectsMatchingPattern( file_, dir_, keys, matchString ) :
    hists = []
    parts = matchString.split('*')
    #for p in parts : print p
    for key in keys :
        allSuccess = True
        for part in parts :
            if not part in key.GetName() :
                allSuccess = False
        if allSuccess :
            #print "append"
            hists.append( file_.Get( dir_ + '/' + key.GetName() ) )
            #hists.append( file_.GetObject( key.GetName(), key.GetClassName() ) )
            #print hists[-1]
    return hists


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



def makeNewCutTrees( ifileName, ofileName, cut ) :
    effFile = ROOT.TFile( ifileName, 'r' )
    #rateFile = ROOT.TFile( 'egTriggerRates.root', 'r' )
    eTree = effFile.Get("analyzer/crystal_tree")
    #rTree = rateFile.Get("analyzer/crystal_tree")
    
    newEffFile = ROOT.TFile(ofileName,'RECREATE')
    ETree = eTree.CopyTree( cut )
    ETree.SetName('events')
    print "Post Cut - New tree has %i events" % ETree.GetEntries()
    newEffFile.cd()
    ETree.Write()
    newEffFile.Close()


def make_efficiency_graph( tree, base_cut, threshold_cut, x_var, x_info ) :
    h1 = ROOT.TH1F('denom', 'denom', x_info[0], x_info[1], x_info[2])
    h2 = ROOT.TH1F('num', 'num', x_info[0], x_info[1], x_info[2])

    tree.Draw( x_var+' >> denom', base_cut )
    tree.Draw( x_var+' >> num', base_cut+' && '+threshold_cut )

    g = ROOT.TGraphAsymmErrors( h2, h1 )
    g.GetXaxis().SetTitle( x_var )
    g.GetYaxis().SetTitle( 'L1 Algo. Efficiency' )

    #g.SaveAs('tmp.root')
    return g

def make_rate_hist( nEvents, tree, x_var, x_var_calib, eta_var, eta_threshold, x_info ) : 
    h1 = ROOT.TH1F('hist', 'hist', x_info[0], x_info[1], x_info[2])

    previous_event = -1
    max_pt = 0.
    # Fill non-cululative distribution
    cnt = 0
    for row in tree :
        cnt += 1
        if cnt % 1000000 == 0 : print cnt
        evt = row.event
        # Initial row
        if previous_event == -1 : previous_event = evt
        # If new event, then fill value from previous
        if previous_event != evt :
            if max_pt > 0. :
                h1.Fill( max_pt )
                max_pt = 0.
            previous_event = evt

        # Skip jets outside of eta threshold region
        eta = getattr( row, eta_var )
        if abs(eta) > eta_threshold : continue

        pt = getattr( row, x_var ) * x_var_calib
        if pt > max_pt : max_pt = pt
    
    # Make non-cumulative --> cumulative
    h2 = ROOT.TH1F('cumul', 'cumul', x_info[0], x_info[1], x_info[2])
    n_bins = h1.GetXaxis().GetNbins()
    integral=0.
    for b in range( n_bins+1 ) :
        i = n_bins - b
        integral += h1.GetBinContent(i)
        h2.SetBinContent( i, integral )
        h2.SetBinError( b, ROOT.TMath.Sqrt(integral) )
    
    h2.Scale( 30000 / nEvents )

    return h2



def drawCMSString( title ) :
    cmsString = ROOT.TLatex(
        ROOT.gPad.GetAbsXlowNDC()+ROOT.gPad.GetAbsWNDC()-ROOT.gPad.GetLeftMargin(),
        ROOT.gPad.GetAbsYlowNDC()+ROOT.gPad.GetAbsHNDC()-ROOT.gPad.GetTopMargin()+0.005,
        title )
    cmsString.SetTextFont(42)
    cmsString.SetTextSize(0.03)
    cmsString.SetNDC(1)
    cmsString.SetTextAlign(31)
    cmsString.Draw()
    return cmsString



def drawDRHists(hists, c, ymax, plotDir, doFit = False, skipScale = False ) :
    c.cd()
    colors = [ROOT.kBlack, ROOT.kRed, ROOT.kBlue, ROOT.kGreen, ROOT.kOrange, ROOT.kGray+2]
    marker_styles = [20, 24, 25, 26, 32, 35]
    hs = ROOT.THStack("hs", c.GetTitle())
    maxi = 0.
    for i, hist in enumerate(hists) :
        #hist.Sumw2()
        if not skipScale :
            hist.Scale(1./hist.Integral())
        hist.SetLineColor(colors[i])
        hist.SetMarkerColor(colors[i])
        hist.SetMarkerStyle(marker_styles[i])
        hist.SetMarkerSize(0.8)
        if hist.GetMaximum() > maxi : maxi = hist.GetMaximum()
        hs.Add(hist, "ex0 hist")

    c.Clear()
    if c.GetLogy() == 0 : # linear
        hs.SetMinimum(0.)
    # Reasonable minimum on logY plots
    if not c.GetLogy() == 0 :
        #if hs.GetMinimum() < hs.GetMaximum() / 1000. :
        hs.SetMinimum( hs.GetMaximum() / 1000. )

    if ymax == 0. :
        hs.SetMaximum( maxi * 1.8 )
    elif not c.GetLogy() == 0 :
        hs.SetMaximum( maxi * ymax )
        #hs.SetMinimum(10e-3)
    elif ymax == -1 :
        hs.SetMaximum( maxi * 1.5 )
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
 
    #leg = setLegStyle(0.53,0.78,0.95,0.92)
    leg = setLegStyle(0.38,0.7,0.88,0.88)
    for hist in hists :
        leg.AddEntry(hist, hist.GetTitle(),"elp")
    leg.Draw("same")
    ROOT.gPad.SetLeftMargin( .14 )
    c.Update()

    hs.GetXaxis().SetTitle(hists[0].GetXaxis().GetTitle())
    #hs.GetYaxis().SetTitle(hists[0].GetYaxis().GetTitle())
    hs.GetYaxis().SetTitleOffset(1.2)
    #hs.GetYaxis().SetTitle("Fraction of Events")
    hs.GetYaxis().SetTitle("Jets / Events")
    hs.GetYaxis().SetTitleOffset( 2. )
    if c.GetName() == "dyncrystalEG_deltaR2" :
        hs.GetXaxis().SetRangeUser(0., 0.15)
 
    cmsString = drawCMSString("CMS Simulation")
                
    c.Print(plotDir+'/'+c.GetName()+".png")
    #c.Print(plotDir+"/"+c.GetName()+".pdf")
    #c.Print(plotDir+"/"+c.GetName()+".C")

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
        ROOT.gStyle.SetOptFit(0)
        fitResults = []
        fitResults.append( ROOT.TLatex(.6, .65, "Gaussian Fits:" ))
        for i, hist in enumerate(hists) :
            # Fit in window around the mean value
            hist_max = hist.GetMean(1)
            fit_min = hist_max - .4
            fit_max = hist_max + .4

            shape = ROOT.TF1("shape", "gaus(0)", fit_min, fit_max)
            #shape.SetParameters(fitHints[i][0], fitHints[i][1], fitHints[i][2])
            hist.Fit(shape, "R")
            hist.GetFunction("shape").SetLineColor(hist.GetLineColor())
            hist.GetFunction("shape").SetLineWidth(hist.GetLineWidth()*2)

            fitResult = hist.GetFunction("shape")
            fitResults.append( ROOT.TLatex(.7, .61-i*.1, "#mu: "+format(fitResult.GetParameter(1), '.2g')))
            fitResults[-1].SetTextColor(hist.GetLineColor())
            fitResults.append( ROOT.TLatex(.7, .57-i*.1, "#sigma: "+format(ROOT.TMath.Sqrt(.5*abs(fitResult.GetParameter(2))), '.2g')))
            fitResults[-1].SetTextColor(hist.GetLineColor())
        for i in range( len(fitResults) ) :
            fitResults[i].SetTextSize(0.045)
            fitResults[i].SetTextFont(42)
            fitResults[i].SetNDC()
            #fitResults[i].SetTextColor()
            fitResults[i].Draw()

        c.Print( plotDir+'/'+c.GetName()+"_fit.png" )
        #c.Print( plotDir+c.GetName()+"_fit.pdf" )

    c.Clear()




if __name__ == '__main__' :
    #f = ROOT.TFile('egTriggerEff.root','r')
    #dir_ = 'analyzer'
    #keys = getKeysOfClass( f, dir_, 'TH1F' )
    #for key in keys :
    #    print key, key.GetName(), key.GetClassName()

    #hists = loadObjectsMatchingPattern( f, dir_, keys, "*_efficiency*_pt" )
    #for h in hists :
    #    print h

    base = '/data/truggles/l1CaloJets_20181024/merged_QCD-PU0_PUTests_0GeV.root'
    f = ROOT.TFile( base, 'r' )
    t = f.Get('analyzer/tree')
    #make_efficiency_graph( t, 'abs(genJet_eta)<1.1', '(ecal_L1EG_jet_pt + ecal_pt + (hcal_pt*calibX) ) > 90', 'genJet_pt', [60, 0, 300] )
    make_efficiency_graph( t, 'abs(genJet_eta)<1.1', 'calibPtX > 90', 'genJet_pt', [60, 0, 300] )
    #print f
    #print f.Get('analyzer/nEvents')
    #make_rate_hist( f.Get('analyzer/nEvents').Integral(), t, 'stage2jet_pt', [56, 20, 300] ) 
