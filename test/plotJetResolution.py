from ROOT import *

#Select and load root files here
name = 'output_round2_HiggsTauTau_withTracks'
f1 = TFile.Open('/afs/hep.wisc.edu/home/vshang/public/Phase2L1CaloTaus/CMSSW_10_5_0_pre1/src/L1Trigger/L1EGRateStudies/test/crab/l1CaloJets_20190909_r2/' + name + '_notTrackMatchedwithTrackdR.root', '')
f2 = TFile.Open('/afs/hep.wisc.edu/home/vshang/public/Phase2L1CaloTaus/CMSSW_10_5_0_pre1/src/L1Trigger/L1EGRateStudies/test/crab/l1CaloJets_20190909_r2/' + name + '_trackMatchedwithTrackdR.root', '')
#f2 = TFile.Open('/afs/hep.wisc.edu/home/vshang/public/Phase2L1CaloTaus/CMSSW_10_5_0_pre1/src/L1Trigger/L1EGRateStudies/test/crab/l1CaloJets_20190909_r2/output_round2_HiggsTauTauv1.root', '')

#Set save directory here
saveDirectory = '/afs/hep.wisc.edu/home/vshang/public/Phase2L1CaloTaus/CMSSW_10_5_0_pre1/src/L1Trigger/L1EGRateStudies/test/resolutions/'

#Set number of histogram bins and maximum value of x and y axis here
nBins = 50
xMin = -1
xMax = 1
yMax = 0.1

#Remove stats box from histograms by setting argument to 0
gStyle.SetOptStat(0)

#Get event tree
eventTree1 = f1.Get('analyzer/tree')
eventTree2 = f2.Get('analyzer/tree')


##Create distribution plots of minimum dR between reco jets and all tracks
##-----------------------------------------------------------------------------------------------

#Define histogramg
print('Creating histograms...')
histo_1= TH1F('histo_1', 'Jet Resolution Plot; (reco #tau p_{T} - gen #tau p_{T})/gen #tau p_{T}; Number of tau jets (normalized)', nBins, xMin, xMax)
histo_2 = TH1F('histo_2', 'Jet Resolution Plot; (reco #tau p_{T} - gen #tau p_{T})/gen #tau p_{T}; Number of tau jets (normalized)', nBins, xMin, xMax)

#Fill histogramg
print('Filling histograms...')
nEntries1 = eventTree1.GetEntries()
nEntries2 = eventTree2.GetEntries()
for i in range(nEntries1):
    eventTree1.GetEntry(i)
    if abs(eventTree1.genJet_eta) < 1.4:# and eventTree1.genJet_pt > 30 and eventTree1.genJet_pt < 34:
        resolution1 = (eventTree1.calibPtHH - eventTree1.genJet_pt)/eventTree1.genJet_pt
        histo_1.Fill(resolution1)
for i in range(nEntries2):
    eventTree2.GetEntry(i)
    if abs(eventTree2.genJet_eta) < 1.4:# and eventTree2.genJet_pt > 30 and eventTree2.genJet_pt < 34:
        resolution2 = (eventTree2.calibPtHH - eventTree2.genJet_pt)/eventTree2.genJet_pt
        histo_2.Fill(resolution2)

#Normalize histograms to unit area
print('Normalizing histograms...')
histo_1.Scale(1/histo_1.Integral())
histo_2.Scale(1/histo_2.Integral())

#Draw histograms
print('Drawing histograms')
canvas = TCanvas('canvas', 'Jet p_{T} resolution')
histo_1.Draw('hist')
histo_2.Draw('hist same')
#Set histo_1 histogram options
histo_1.SetLineColor(kRed)
histo_1.SetLineWidth(1)
histo_1.SetMinimum(0)
histo_1.SetMaximum(yMax)
#Set histo_2 histogram options
histo_2.SetLineColor(kBlue)
histo_2.SetLineWidth(1)
histo_2.SetMinimum(0)
histo_2.SetMaximum(yMax)
#Add legend
legend = TLegend(0.66, 0.73, 0.95, 0.87)
legend.AddEntry(histo_1, 'Unmatched jet resolution (|#eta| < 1.4)', 'l')
legend.AddEntry(histo_2, 'Track matched jet resolution (|#eta| < 1.4)', 'l')
legend.Draw('same')
legend.SetBorderSize(0)
#Save histograms
print('Saving histograms...')
canvas.SaveAs(saveDirectory+name + '_unmatchedVsMatched_jetResolution_All.pdf')
print('Saved histograms')
