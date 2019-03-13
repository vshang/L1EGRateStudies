import ROOT
import os
ROOT.gROOT.SetBatch(True)
ROOT.gStyle.SetOptStat(0)


def make_DM_plot( label1='Gen', label2='Num. L1EGs' ) :
    gen_bin_label_map_mva = {
        1 : '#pi',
        2 : '#pi#pi^{0}s',
        3 : '#pi#pi#pi',
        4 : '#pi#pi#pi#pi^{0}s',
    }
    online_labels = {
        1 : 'Zero #pi^{0}s',
        2 : '1 to 2 L1EGs',
        3 : '3 to 4 L1EGs',
        4 : '4+ L1EGs',
    }
    h_dm = ROOT.TH2D( 'Tau Decay Modes', 'Tau Decay Modes: %s vs. %s;%s #tau DM;%s #tau DM' % (label1, label2, label1, label2), 4,0,4,4,0,4 )
    for k, v in gen_bin_label_map_mva.iteritems() :
        h_dm.GetXaxis().SetBinLabel( k, v )
    for k, v in online_labels.iteritems() :
        h_dm.GetYaxis().SetBinLabel( k, v )
    h_dm.GetYaxis().SetTitleOffset( h_dm.GetYaxis().GetTitleOffset() * 2 )
    h_dm.SetDirectory(0)
    return h_dm

def getGenDMCode( n_prongs, n_photons ) :
    if n_prongs == 1 : 
        if n_photons == 0 : return 0
        else : return 1
    if n_prongs == 3 :
        if n_photons == 0 : return 2
        else : return 3
    else : return 0

def getL1DMCode( n_L1EGs ) :
    if n_L1EGs == 0 : return 0
    if n_L1EGs <= 2 : return 1
    if n_L1EGs == 4 : return 2
    else : return 3


c = ROOT.TCanvas('c', '', 800, 700)
    
ggH = 'output_round2_HiggsTauTau4v5.root'
version = ggH.replace('.root','')

base = '/data/truggles/l1CaloJets_20190308_r2/'
#universalSaveDir = "/afs/cern.ch/user/t/truggles/www/Phase-II/"+version+"_GenTauInHGCal/"
universalSaveDir = "/afs/cern.ch/user/t/truggles/www/Phase-II/"+version+"_GenTauInBarrel/"
if not os.path.exists( universalSaveDir ) : os.makedirs( universalSaveDir )
ggHHTTFile = ROOT.TFile( base+ggH, 'r' )
tree_ggH = ggHHTTFile.Get("analyzer/tree")

h2_loose = make_DM_plot('Gen', 'Num. L1EGs No SS')
h2_trk = make_DM_plot('Gen', 'Num. L1EGs Trk SS')
h2_standalone = make_DM_plot('Gen', 'Num. L1EGs Standalone SS')

cnt = 0
for row in tree_ggH :
    cnt += 1
    if cnt % 10000 == 0 : print cnt
    if row.jet_pt <= 0 : continue
    if row.genJet_pt < 30 : continue
    if abs(row.genJet_eta) > 1.3 : continue

    genDM = getGenDMCode( row.genTau_n_prongs, row.genTau_n_photons )
    l1DM = getL1DMCode( row.l1eg_nL1EGs )
    l1DM_trk = getL1DMCode( row.l1eg_nL1EGs_trkMatchSS )
    l1DM_standalone = getL1DMCode( row.l1eg_nL1EGs_standaloneSS )

    h2_loose.Fill( genDM, l1DM )
    h2_trk.Fill( genDM, l1DM_trk )
    h2_standalone.Fill( genDM, l1DM_standalone )

h2_loose.Draw('COLZ TEXT')
ROOT.gPad.SetLeftMargin( .2 )
ROOT.gPad.SetRightMargin( .2 )
c.SaveAs( universalSaveDir+'dm_loose.png' )

h2_trk.Draw('COLZ TEXT')
c.SaveAs( universalSaveDir+'dm_trk.png' )

h2_standalone.Draw('COLZ TEXT')
c.SaveAs( universalSaveDir+'dm_standalone.png' )


