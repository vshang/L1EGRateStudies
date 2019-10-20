from ROOT import *

#Select and load root files here
f = TFile.Open('/afs/hep.wisc.edu/home/vshang/public/Phase2L1CaloTaus/CMSSW_10_5_0_pre1/src/L1Trigger/L1EGRateStudies/test/crab/l1CaloJets_20190909_r2/output_round2_HiggsTauTau_withTracks_notTrackMatchedwithTrackdR.root', '')

#Set save directory here
saveDirectory = '/afs/hep.wisc.edu/home/vshang/public/Phase2L1CaloTaus/CMSSW_10_5_0_pre1/src/L1Trigger/L1EGRateStudies/test/trackStudies/'

#Set number of histogram bins and maximum value of x and y axis here
nBins = 100
xMax = 2
yMax = 0.5

#Remove stats box from histograms by setting argument to 0
gStyle.SetOptStat(0)

#Get event tree
eventTree = f.Get('analyzer/tree')


##Create distribution plots of minimum dR between reco jets and all tracks
##-----------------------------------------------------------------------------------------------

#Define histograms
print('Creating histograms...')
histo_0GeV = TH1F('histo_0GeV', 'Track Matching dR distribution; minimum dR between reco jet and all tracks; Number of tau jets (normalized)', nBins, 0, xMax)
histo_2GeV = TH1F('histo_2GeV', 'Track Matching dR distribution with pT > 2 GeV; minimum dR between reco jet and all tracks; Number of tau jets (normalized)', nBins, 0, xMax)
histo_10GeV = TH1F('histo_10GeV', 'Track Matching dR distribution with pT > 10 GeV; minimum dR between reco jet and all tracks; Number of tau jets (normalized)', nBins, 0, xMax)

#Fill histograms
print('Filling histograms...')
nEntries = eventTree.GetEntries()
for i in range(nEntries):
    eventTree.GetEntry(i)
    if abs(eventTree.genJet_eta) < 1.4 and eventTree.genJet_pt > 40 and eventTree.calibPtHH > 32:
        histo_0GeV.Fill(eventTree.jet_and_track_dR)
        histo_2GeV.Fill(eventTree.jet_and_track_dR_2GeV)
        histo_10GeV.Fill(eventTree.jet_and_track_dR_10GeV)

#Normalize histograms to unit area
print('Normalizing histograms...')
histo_0GeV.Scale(1/histo_0GeV.Integral())
histo_2GeV.Scale(1/histo_2GeV.Integral())
histo_10GeV.Scale(1/histo_10GeV.Integral())

#Draw histo_0GeV histogram
print('Drawing histo_0GeV...')
canvas_0GeV = TCanvas('canvas_0GeV', 'Track Matching dR distribution')
histo_0GeV.Draw('hist')
#Set histo_0GeV histogram options
histo_0GeV.SetLineColor(kRed)
histo_0GeV.SetLineWidth(1)
histo_0GeV.SetMinimum(0)
histo_0GeV.SetMaximum(yMax)
#Save histo_0GeV histogram
print('Saving histo_0GeV...')
canvas_0GeV.SaveAs(saveDirectory+'jetAndTrackdR.pdf')
print('Saved histo_0GeV')

#Draw histo_2GeV histogram
print('Drawing histo_2GeV...')
canvas_2GeV = TCanvas('canvas_2GeV', 'Track Matching dR distribution')
histo_2GeV.Draw('hist')
#Set histo_2GeV histogram options
histo_2GeV.SetLineColor(kRed)
histo_2GeV.SetLineWidth(1)
histo_2GeV.SetMinimum(0)
histo_2GeV.SetMaximum(yMax)
#Save histo_2GeV histogram
print('Saving histo_2GeV...')
canvas_2GeV.SaveAs(saveDirectory+'jetAndTrackdR_2GeV.pdf')
print('Saved histo_2GeV')

#Draw histo_10GeV histogram
print('Drawing histo_10GeV...')
canvas_10GeV = TCanvas('canvas_10GeV', 'Track Matching dR distribution')
histo_10GeV.Draw('hist')
#Set histo_10GeV histogram options
histo_10GeV.SetLineColor(kRed)
histo_10GeV.SetLineWidth(1)
histo_10GeV.SetMinimum(0)
histo_10GeV.SetMaximum(yMax)
print('Saving histo_10GeV...')
#Save histo_10GeV histogram
canvas_10GeV.SaveAs(saveDirectory+'jetAndTrackdR_10GeV.pdf')
print('Saved histo_10GeV')
