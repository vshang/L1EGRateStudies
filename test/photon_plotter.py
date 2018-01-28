

import ROOT
from collections import OrderedDict
ROOT.gROOT.SetBatch(True)

#newPhotonRes_PU200_minEt500MeV.root
#newPhotonRes_PU200_minEt0MeV.root
#newPhotonRes_PU200_minEt125MeV.root
#newPhotonRes_PU200_minEt250MeV.root
#newPhotonRes_PU200_minEt375MeV.root
#newPhotonRes_PU200_minEt50MeV.root
#newPhotonRes_PUZero_minEt500MeV.root
#newPhotonRes_PUZero_minEt0MeV.root
#newPhotonRes_PUZero_minEt125MeV.root
#newPhotonRes_PUZero_minEt250MeV.root
#newPhotonRes_PUZero_minEt375MeV.root
#newPhotonRes_PUZero_minEt50MeV.root

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

#etList = ['minEt0MeV', 'minEt50MeV', 'minEt125MeV', 'minEt250MeV', 'minEt375MeV', 'minEt500MeV']
etMap = OrderedDict()
#etMap[ 'minEt0MeV'   ] = 'ET > 0 MeV'
etMap[ 'minEt125MeV' ] = 'ET >= 125 MeV'
etMap[ 'minEt250MeV' ] = 'ET >= 250 MeV'
etMap[ 'minEt375MeV' ] = 'ET >= 375 MeV'
etMap[ 'minEt500MeV' ] = 'ET >= 500 MeV'
 


def getPtRes( name, cut = '' ) :
    iDir = '/afs/cern.ch/work/t/truggles/TrackTrigger/CMSSW_9_2_0/src/L1Trigger/L1EGRateStudies/test/'
    fNameBase = 'r2_phase2_singleElectron_20180120'
    f = ROOT.TFile( iDir+fNameBase+name+'.root', 'r' )
    print f
    t = f.Get('analyzer/crystal_tree')
    h = ROOT.TH1D( name, name, 100, -.3, .1 )
    t.Draw( '(cluster_pt-gen_pt)/gen_pt >> '+name, cut )
    h.Scale( 1. / h.Integral() )
    h.SetDirectory( 0 )
    return h

def plotRes( c, hists, name ) :
    universalSaveDir = "/afs/cern.ch/user/t/truggles/www/Phase-II/photonPtRes3/"
    c.Clear()
    #if 'Zero' in name :
    #    #ROOT.gPad.SetLeftMargin( ROOT.gPad.GetLeftMargin() * 1.25 )
    #    ROOT.gPad.SetLeftMargin( ROOT.gPad.GetLeftMargin() * 1.25 )
    #ROOT.gPad.SetLeftMargin( ROOT.gPad.GetLeftMargin() * 1.3 )
    ROOT.gPad.SetLeftMargin( .13 )
    cnt = 0
    colors = [ROOT.kRed, ROOT.kBlue, ROOT.kMagenta, ROOT.kBlack, ROOT.kGreen+1]

    
    maxi = 0.
    for h in hists :
        h.SetLineColor( colors[cnt] )
        h.SetLineWidth( 2 )
        if h.GetMaximum() > maxi : maxi = h.GetMaximum()
        if cnt == 0 :
            h.Draw('HIST')
            h.GetXaxis().SetTitle("(L1EG p_{T} - Gen p_{T}) / Gen p_{T}")
            h.GetYaxis().SetTitle("A.U.")
        else :
            h.Draw('HIST SAMES')
        ROOT.gPad.Update()
        s = h.FindObject("stats")
        print h, s
        #s1.SetName('s1')
        s.SetY2NDC(.9-.12*cnt)
        s.SetY1NDC(.9-.12*(cnt+1))
        s.SetTextColor( colors[cnt] )
        cnt += 1

    hists[0].SetMaximum( maxi * 1.2 )
    leg = setLegStyle(0.15,0.5,0.45,0.87)
    for h in hists :
        leg.AddEntry(h, etMap[ h.GetTitle().split('_')[-1] ],"lpe")
    leg.Draw("same")
    #hists[0].SetTitle( '%s L1EG p_{T} Resolution' % (hists[0].GetTitle().split('_')[0]) )
    hists[0].SetTitle( 'Electron L1EG p_{T} Resolution' )
    c.Update()
    c.SaveAs( universalSaveDir+'ptRes_'+name+'.png' )



c = ROOT.TCanvas( 'c', 'c', 550, 550 )
p = ROOT.TPad( 'p', 'p', 0, 0, 1, 1 )
p.Draw()
p.cd()

pu200Hists = []
pu200HistsCut = []
pu200HistsCutEta = []
pu200HistsCutEtaGtr1p4 = []
pu200HistsCutEtaIn = []
pu200HistsCutEtaOut = []
puZeroHists = []

for et in etMap.keys() :

    #puZeroHists.append( getPtRes( 'PUZero_'+et ) )
    #pu200Hists.append( getPtRes( 'PU200_'+et ) )

    pu200Hists.append( getPtRes( et ) )
    pu200HistsCut.append( getPtRes( et, 'cluster_pt > 30 && cluster_pt < 40' ) )
    pu200HistsCutEta.append( getPtRes( et, 'cluster_pt > 30 && cluster_pt < 40 && abs( eta ) < 1.4' ) )
    pu200HistsCutEtaGtr1p4.append( getPtRes( et, 'cluster_pt > 30 && cluster_pt < 40 && abs( eta ) > 1.4' ) )
    pu200HistsCutEtaIn.append( getPtRes( et, 'cluster_pt > 30 && cluster_pt < 40 && abs( eta ) < 1' ) )
    pu200HistsCutEtaOut.append( getPtRes( et, 'cluster_pt > 30 && cluster_pt < 40 && abs( eta ) > 1' ) )


#plotRes( c, puZeroHists, 'PUZero' )
#plotRes( c, pu200Hists, 'PU200' )

#plotRes( c, pu200Hists, 'PU200_Electron' )
plotRes( c, pu200HistsCut, 'PU200_Electron_pt30-40' )
plotRes( c, pu200HistsCutEta, 'PU200_Electron_pt30-40_Eta1p4' )
plotRes( c, pu200HistsCutEtaGtr1p4, 'PU200_Electron_pt30-40_EtaGtr1p4' )
plotRes( c, pu200HistsCutEtaIn, 'PU200_Electron_pt30-40_Eta1' )
plotRes( c, pu200HistsCutEtaOut, 'PU200_Electron_pt30-40_EtaGtr1' )







