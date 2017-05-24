import ROOT
from ROOT import gStyle, gPad
import tdrstyle
from optimizer import makeCutROC, makeComparisons
import trigHelpers
from drawRateEff import drawDRHists, draw2DdeltaRHist, loadHists



""" Use this script to make a slew of standard control plots
    for the L1 EG Crystal Algo """



gStyle.SetOptStat(0)
ROOT.gROOT.SetBatch(True)

date = '20170508v3'
#date = '20170503v1'
date = 'v2'
newEffFileName = 'r2_phase2_singleElectron_%s.root' % (date)
newPhotonFileName = 'r2_phase2_singlePhoton_%s.root' % (date)
newRateFileName = 'r2_phase2_minBias_%s.root' % (date)

rateFile = ROOT.TFile( newRateFileName, 'r' )
effFile = ROOT.TFile( newEffFileName, 'r' )


#crystal_tree = effFile.Get("analyzer/crystal_tree")
#rate_tree = rateFile.Get("analyzer/crystal_tree")
#''' Do 2D color plots 1st b/c of TDR style '''
## 1) 2D delta Eta vs delta Phi plot
#dynCrystal2DdeltaRHist = effFile.Get("analyzer/dyncrystalEG_2DdeltaR_hist")
#c = ROOT.TCanvas('c', 'c', 800, 700)
#c.SetName("dyncrystalEG_2D_deltaR_electron")
#c.SetTitle("")
#draw2DdeltaRHist(dynCrystal2DdeltaRHist, c)
#
## 2) 2D pt resolution vs. gen pt
##recoGenPtHist = effFile.Get("analyzer/reco_gen_pt")
#recoGenPtHist = ROOT.TH2D('recoGenPtHist','recoGenPtHist',50,0,50,30,-0.3,0.3)
#crystal_tree.Draw('(cluster_pt-gen_pt)/gen_pt:gen_pt >> recoGenPtHist')
#tdrRecoGenPtHist = effFile.Get("analyzer/l1extraParticlesUCT:All_reco_gen_pt")
#
#''' Track to cluster reco resolution '''
#c.SetCanvasSize(1200,600)
#c.Divide(2)
#title1 = "L1EGamma Crystal (Electrons)"
#title2 = "L1EGamma Crystal (Fake)"
#c.Clear()
#
#recoGenPtHist.SetTitle("Electron: Crystal EG algorithm pT resolution")
#oldAlgRecoGenPtHist = effFile.Get("analyzer/l1extraParticlesUCT:All_reco_gen_pt")
#oldAlgRecoGenPtHist.SetTitle("Electron: Tower EG alg. momentum error")
#oldAlgRecoGenPtHist.GetYaxis().SetTitle("Relative Error (reco-gen)/gen")
#oldAlgRecoGenPtHist.SetMaximum(50)
#oldAlgRecoGenPtHist.SetLineColor(ROOT.kRed)
#c.SetCanvasSize(1200,600)
#c.Divide(2,1)
#c.cd(1)
#gPad.SetGridx(1)
#gPad.SetGridy(1)
#recoGenPtHist.Draw("colz")
#recoGenPtHist.GetYaxis().SetTitleOffset(1.4)
#c.cd(2)
#gPad.SetGridx(1)
#gPad.SetGridy(1)
#oldAlgRecoGenPtHist.Draw("colz")
#oldAlgRecoGenPtHist.GetYaxis().SetTitleOffset(1.4)
#c.Print("plots/reco_gen_pt_electron.png")
#del c

canvasSize = 800

eTree = effFile.Get("analyzer/crystal_tree")
rTree = rateFile.Get("analyzer/crystal_tree")

tdrstyle.setTDRStyle()
c = ROOT.TCanvas('c','c',canvasSize,canvasSize)

from loadCuts import getCutMap
cutMap = getCutMap()
Isolation9 = cutMap['90x500MeV']['isolation']
showerShapes9 = cutMap['90x500MeV']['showerShape']
cut_ss_cIso9 = showerShapes9+"*"+Isolation9
cut_with_e2x2OverE2x5Window = cut_ss_cIso9+"*((e2x2/e2x5)>0.9)"
cut_ss_cIso_TrkMatch = cut_ss_cIso9+"*(trackDeltaR<.1)"

cut_none = "(1.)"
cut_ss = showerShapes9


rocAry = [1000, 0.0, 1.]
#rocAry = [200, 0.0, .3]
textR = "Scanning 0.0 < #DeltaR(Trk, L1EG) < 1.0"
#rebase20 = "(cluster_pt>20)*(abs(cluster_pt-trackPt)/cluster_pt < 0.5)"
rebase20 = "(cluster_pt>20)"
rebase30 = "(cluster_pt>30)"
rebaseAll = cut_ss_cIso9


#makeCutROC( "testDRCutsBaselineCuts20_ss_cIso", eTree, rTree, "trackDeltaR", rocAry, cut_ss_cIso9+"*"+rebase20, rebaseAll+"*"+rebase20, textR )
makeComparisons( cut_ss_cIso9, "E_e2x5OverE5x5 Iso", False, ["",""], 'cluster_pt' )
makeComparisons( cut_with_e2x2OverE2x5Window, "E_e2x5OverE5x5 Iso PhoWindow", False, ["",""], 'cluster_pt' )
makeComparisons( cut_ss_cIso_TrkMatch, "E_e2x5OverE5x5 Iso TrkMatch", False, ["",""], 'cluster_pt' )





#gStyle.SetOptStat(0)
#gStyle.SetTitleFont(42, "p")
#gStyle.SetTitleColor(1)
#gStyle.SetTitleTextColor(1)
#gStyle.SetTitleFillColor(10)
#gStyle.SetTitleFontSize(0.05)
#gStyle.SetTitleFont(42, "XYZ")
#gStyle.SetLabelFont(42, "XYZ")
#
#
#effMap = {
#    'newAlgDRHist' : ('L1EGamma Crystal', 'analyzer/dyncrystalEG_deltaR'),
#    'newAlgDEtaHist' : ('L1EGamma Crystal', 'analyzer/dyncrystalEG_deta'),
#    'newAlgDPhiHist' : ('L1EGamma Crystal', 'analyzer/dyncrystalEG_dphi'),
#    'UCTAlgDRHist' : ('Phase 1 TDR', 'analyzer/l1extraParticlesUCT:All_deltaR'),
#    'UCTAlgDEtaHist' : ('Phase 1 TDR', 'analyzer/l1extraParticlesUCT:All_deta'),
#    'UCTAlgDPhiHist' : ('Phase 1 TDR', 'analyzer/l1extraParticlesUCT:All_dphi'),
#}
#
#effHistsKeys = trigHelpers.getKeysOfClass( effFile, "analyzer", "TGraphAsymmErrors")
#hists = loadHists( rateFile )
#effHists = loadHists( effFile, effMap )
#
#
#
#gStyle.SetOptStat(0)
#xrange = [0., 50.]
#c = ROOT.TCanvas('c', 'c', 800, 600)
#
#''' POSITION RECONSTRUCTION '''
## Delta R Stuff
#c.SetGridx(0)
#c.SetGridy(0)
#c.SetName("dyncrystalEG_deltaR")
#c.SetTitle("")
#drawDRHists([effHists['newAlgDRHist'], effHists['UCTAlgDRHist']], c, 0.)
#
## Delta Eta / Phi
#c.SetName("dyncrystalEG_deltaEta")
#drawDRHists([effHists['newAlgDEtaHist'], effHists['UCTAlgDEtaHist']], c, 0.)
#c.SetName("dyncrystalEG_deltaPhi")
#drawDRHists([effHists['newAlgDPhiHist'], effHists['UCTAlgDPhiHist']], c, 0.)




