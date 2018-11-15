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
