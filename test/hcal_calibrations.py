


import os
import ROOT
ROOT.gROOT.SetBatch(True)

n = 'aug13_pion_v3.root'
f = ROOT.TFile( n, 'r' )
t = f.Get('analyzer/crystal_tree')
print t

c = ROOT.TCanvas('c', 'c', 400, 400)
p = ROOT.TPad('p', 'p', 0, 0, 1, 1)
p.Draw()
p.cd()

plotDir = '/afs/cern.ch/user/t/truggles/www/Phase-II/hcal_calibrations/aug13v3/'
if not os.path.exists( plotDir ) : os.makedirs( plotDir )


def make_2d( t, to_plot, name ) :
    h = ROOT.TH2F(name , name, 50, 0, 100, 90, -1, 2)

    t.Draw( to_plot+' >> '+name, '' )

    h.GetXaxis().SetTitle('Gen E_{T} (GeV)')
    h.GetYaxis().SetTitle('E_{T}, (reco-gen)/gen')
    h.Draw('COLZ')
    ROOT.gPad.SetGrid()

    c.SaveAs(plotDir+name+'.png')    


make_2d( t, '( ( cluster_pt - gen_pt ) / gen_pt ):gen_pt', 'hist_pure_ecal' )
for hcal_e in ['hcal_dR0p05', 'hcal_dR0p075', 'hcal_dR0p1', 'hcal_dR0p125', 'hcal_dR0p15', 'hcal_dR0p2', 'hcal_dR0p3', 'hcal_dR0p4', 'hcal_dR0p5',] :
    make_2d( t, '( ( cluster_pt + '+hcal_e+' - gen_pt ) / gen_pt ):gen_pt', 'hist_'+hcal_e )
