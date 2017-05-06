import ROOT
from drawRateEff import *

#gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch(True)

#drawDRHists(hists, c, ymax, doFit = False)




def makeControls( data, sample ) :

    plotMap = {
        'pT_res' : ['(cluster_pt - gen_pt)/gen_pt',100,-1,1],
        'pT_res2D' : ['(cluster_pt - gen_pt)/gen_pt:gen_pt',100,-.5,.5],
        'deltaR' : ['deltaR',100,0,.1],
        'deltaPhi' : ['deltaPhi',100,-.1,.1],
        'deltaEta' : ['deltaEta',100,-.1,.1],
    }


    f = ROOT.TFile( '%s/%s_single%s_eff.root' % (date, date, sample), 'r' )
    t = f.Get( 'analyzer/crystal_tree' )
    #print t.GetEntries()
    for var in plotMap :
        print sample, var
        if var == 'pT_res2D' :
            makeSimplePlot2D( c, t, sample, var, plotMap[var][0], plotMap[var][1], plotMap[var][2], plotMap[var][3])
        else :
            makeSimplePlot( c, t, sample, var, plotMap[var][0], plotMap[var][1], plotMap[var][2], plotMap[var][3])
  

 
def makeSimplePlot( c, tree, sample, varName, plotVar, nBins, min, max ) : 
    h1 = ROOT.TH1F('h1','%s %s L1EG Algo' % (sample, varName.replace('_',' ')), nBins, min, max)
    tree.Draw('%s >> h1' % plotVar)
    h1.GetXaxis().SetTitle( plotVar )
    h1.GetYaxis().SetTitle( 'Events' )
    h1.Draw()
    c.SaveAs('/afs/cern.ch/user/t/truggles/www/Phase-II_20170503/%s_%s.png' % (sample, varName ) )
    del h1
    

def makeSimplePlot2D( c, tree, sample, varName, plotVar, nBins, min, max ) : 
    h1 = ROOT.TH2F('h1','%s %s L1EG Algo' % (sample, varName.replace('_',' ')), nBins/2, 0, 100, nBins/2, min, max)
    tree.Draw('%s >> h1' % plotVar)
    h1.GetXaxis().SetTitle( plotVar.split(':')[1] )
    h1.GetYaxis().SetTitle( plotVar.split(':')[0] )
    h1.Draw('COLZ')
    c.SaveAs('/afs/cern.ch/user/t/truggles/www/Phase-II_20170503/%s_%s.png' % (sample, varName ) )
    del h1

if __name__ == '__main__' :

    c = ROOT.TCanvas('c1','c1',600,600)
    c.cd()
    p1 = ROOT.TPad('p1','p1',0,0,1,1)
    p1.Draw()
    p1.cd()

    date = '20170503v1'

    samples = ['Electron','Photon','PiZero','Pion','Tau']
    for sample in samples :
        print sample
        makeControls( date, sample )





