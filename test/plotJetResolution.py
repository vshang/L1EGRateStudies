from ROOT import *

#Select and load root files here
name = 'output_round2_HiggsTauTau_withTracks'
f1 = TFile.Open('/afs/hep.wisc.edu/home/vshang/public/Phase2L1CaloTaus/CMSSW_10_5_0_pre1/src/L1Trigger/L1EGRateStudies/test/crab/l1CaloJets_20190909_r2/' + name + '_notTrackMatched.root', '')
#f2 = TFile.Open('/afs/hep.wisc.edu/home/vshang/public/Phase2L1CaloTaus/CMSSW_10_5_0_pre1/src/L1Trigger/L1EGRateStudies/test/crab/l1CaloJets_20190909_r2/' + name + '_trackMatchedwithTrackdR.root', '')
#f2 = TFile.Open('/afs/hep.wisc.edu/home/vshang/public/Phase2L1CaloTaus/CMSSW_10_5_0_pre1/src/L1Trigger/L1EGRateStudies/test/crab/l1CaloJets_20190909_r2/output_round2_HiggsTauTauv1.root', '')

#Set save directory here
saveDirectory = '/afs/hep.wisc.edu/home/vshang/public/Phase2L1CaloTaus/CMSSW_10_5_0_pre1/src/L1Trigger/L1EGRateStudies/test/resolutions/'

#Set number of histogram bins and maximum value of x and y axis here
nBins = 50
xMin = -0.5
xMax = 2
yMax = 0.1

#Remove stats box from histograms by setting argument to 0
gStyle.SetOptStat(0)

#Get event tree
eventTree1 = f1.Get('analyzer/tree')
#eventTree2 = f2.Get('analyzer/tree')


##Create distribution plots of minimum dR between reco jets and all tracks
##-----------------------------------------------------------------------------------------------

#Define histogramg
print('Creating histograms...')
histo_1= TH1F('histo_1', '; #tau_{h} E_{T} within core / Total Gen #tau E_{T}; Fraction of Events', nBins, xMin, xMax)
histo_2 = TH1F('histo_2', '; #tau_{h} E_{T} within core / Total Gen #tau E_{T}; Fraction of Events', nBins, xMin, xMax)
histo_3 = TH1F('histo_3', '; #tau_{h} E_{T} within core / Total Gen #tau E_{T}; Fraction of Events', nBins, xMin, xMax)

#Fill histogramg
print('Filling histograms...')
nEntries1 = eventTree1.GetEntries()
#nEntries2 = eventTree2.GetEntries()
for i in range(nEntries1):
    eventTree1.GetEntry(i)
    if abs(eventTree1.genJet_eta) < 1.4 and eventTree1.genJet_pt > 20 and eventTree1.calibPtHH > 0:
        genJet_pt = eventTree1.genJet_pt
        total_2x3a = eventTree1.total_22 + eventTree1.total_23 + eventTree1.total_seed + eventTree1.total_33 + eventTree1.total_42 + eventTree1.total_43
        total_2x3b = eventTree1.total_21 + eventTree1.total_22 + eventTree1.total_31 + eventTree1.total_seed + eventTree1.total_41 + eventTree1.total_42
        total_2x3 = max(total_2x3a, total_2x3b)
        total_3x5 = eventTree1.total_3x5
        total_7x7 = eventTree1.total_7x7

        histo_1.Fill(total_2x3/genJet_pt)
        histo_2.Fill(total_3x5/genJet_pt)
        histo_3.Fill(total_7x7/genJet_pt)
        #resolution1 = (eventTree1.calibPtHH - eventTree1.genJet_pt)/eventTree1.genJet_pt
        #histo_1.Fill(resolution1)
# for i in range(nEntries2):
#     eventTree2.GetEntry(i)
#     if abs(eventTree2.genJet_eta) < 1.4:# and eventTree2.genJet_pt > 30 and eventTree2.genJet_pt < 34:
#         resolution2 = (eventTree2.calibPtHH - eventTree2.genJet_pt)/eventTree2.genJet_pt
#         histo_2.Fill(resolution2)

#Normalize histograms to unit area
print('Normalizing histograms...')
histo_1.Scale(1/histo_1.Integral())
histo_2.Scale(1/histo_2.Integral())
histo_3.Scale(1/histo_3.Integral())

#Draw histograms
print('Drawing histograms')
canvas = TCanvas('canvas', 'Jet p_{T} resolution')

histo_1.Draw('hist e')
histo_2.Draw('hist e same')
histo_3.Draw('hist e same')
#Set histo_1 histogram options
histo_1.SetLineColor(kBlack)
histo_1.SetLineWidth(2)
histo_1.SetMinimum(0)
histo_1.SetMaximum(yMax)
#Set histo_2 histogram options
histo_2.SetLineColor(kRed)
histo_2.SetLineStyle(3)
histo_2.SetLineWidth(2)
histo_2.SetMinimum(0)
histo_2.SetMaximum(yMax)
#Set histo_3 histogram options
histo_3.SetLineColor(kBlue)
histo_3.SetLineStyle(2)
histo_3.SetLineWidth(2)
histo_3.SetMinimum(0)
histo_3.SetMaximum(yMax)
#Add legend
legend = TLegend(0.16, 0.55, 0.45, 0.85)
legend.AddEntry(histo_1, '2x3 #tau_{h} core', 'le')
legend.AddEntry(histo_2, '3x5 #tau_{h} core', 'le')
legend.AddEntry(histo_3, '7x7 #tau_{h} core', 'le')
legend.Draw('same')
legend.SetBorderSize(0)
#Set text size
histo_1.SetTitleSize(0.04, 'xyz')
histo_2.SetTitleSize(0.04, 'xyz')
histo_3.SetTitleSize(0.04, 'xyz')
legend.SetTextSize(0.04)

#Set title
title = TLatex()
title.SetTextSize(0.045)
title.DrawLatexNDC(.12, .91, "CMS")
title.SetTextSize(0.030)
title.DrawLatexNDC(.19, .91, "Phase-2 Simulation")
title.SetTextSize(0.035)
title.DrawLatexNDC(.74, .91, "14 TeV, 200 PU")

#Set selection cut text
txt = TLatex()
txt.SetTextSize(0.040)
txt.DrawLatexNDC(.68, .83,  "|#eta^{GenTau}| < 1.4")
txt.DrawLatexNDC(.68, .76, "p_{T}^{GenTau} > 20 GeV")

#Set grid
canvas.SetGrid()

#Save histograms
print('Saving histograms...')
canvas.SaveAs(saveDirectory+name + '_tauCoreResolutionPlots.pdf')
print('Saved histograms')
