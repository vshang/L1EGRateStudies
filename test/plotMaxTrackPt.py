from ROOT import *

#Select and load root files here
f = TFile.Open('/afs/hep.wisc.edu/home/vshang/public/Phase2L1CaloTaus/CMSSW_10_5_0_pre1/src/L1Trigger/L1EGRateStudies/test/crab/l1CaloJets_20190909_r2/output_round2_HiggsTauTau_withTracks_notTrackMatched.root', '')

#Set save directory here
saveDirectory = '/afs/hep.wisc.edu/home/vshang/public/Phase2L1CaloTaus/CMSSW_10_5_0_pre1/src/L1Trigger/L1EGRateStudies/test/trackStudies/'

#Set number of histogram bins and maximum value of x and y axis here
nBins = 40
#xMax = 200
xMax = 2
#yMax = 0.2
yMax = 0.1

#Remove stats box from histograms by setting argument to 0
gStyle.SetOptStat(0)

#Get event tree
eventTree = f.Get('analyzer/tree')


##Create distribution plots of minimum dR between reco jets and all tracks
##-----------------------------------------------------------------------------------------------

#Define histograms
print('Creating histograms...')
#histo1 = TH1F('histo1', 'Track pT distribution with dR < 0.2; max track p_{T}; Number of tau jets (normalized)', nBins, 0, xMax)
histo1 = TH1F('histo1', 'Track pT fraction distribution with dR < 0.2; max track p_{T}/reco tau p_{T}; Number of tau jets (normalized)', nBins, 0, xMax)
#histo2 = TH1F('histo2', 'Track pT fraction distribution with dR < 0.2; max track p_{T}; Number of tau jets (normalized)', nBins, 0, xMax)
histo2 = TH1F('histo2', 'Track pT fraction distribution with dR < 0.2; max track p_{T}/reco tau p_{T}; Number of tau jets (normalized)', nBins, 0, xMax)

#Fill histograms
print('Filling histograms...')
nEntries = eventTree.GetEntries()
for i in range(nEntries):
    eventTree.GetEntry(i)
    if abs(eventTree.genJet_eta) < 1.4 and eventTree.calibPtHH > 0:
        pt_ratio = eventTree.max_track_pt_dR0p2/eventTree.calibPtHH
        #pt_ratio = eventTree.max_track_pt_dR0p2/eventTree.genJet_pt
        histo1.Fill(pt_ratio)
        #histo1.Fill(eventTree.max_track_pt_dR0p2)
        if eventTree.calibPtHH > 32 and eventTree.genJet_pt > 40:
            histo2.Fill(pt_ratio)
            #histo2.Fill(eventTree.max_track_pt_dR0p2)

#Normalize histograms to unit area
print('Normalizing histograms...')
histo1.Scale(1/histo1.Integral())
histo2.Scale(1/histo2.Integral())

#Draw histograms
print('Drawing histograms...')
canvas = TCanvas('canvas', 'Track Matching dR distribution')
histo1.Draw('hist')
histo2.Draw('hist same')
#Set histo1 histogram options
histo1.SetLineColor(kRed)
histo1.SetLineWidth(1)
histo1.SetMinimum(0)
histo1.SetMaximum(yMax)
#Set histo2 histogram options
histo2.SetLineColor(kBlue)
histo2.SetLineWidth(1)
histo2.SetMinimum(0)
histo2.SetMaximum(yMax)
#Add legend
legend = TLegend(0.61, 0.73, 0.90, 0.87)
legend.AddEntry(histo1, 'reco tau p_{T} > 0 GeV', 'l')
legend.AddEntry(histo2, 'reco tau p_{T} > 32 GeV & gen tau p_{T} > 40 GeV', 'l')
legend.Draw('same')
legend.SetBorderSize(0)
#Save histograms
print('Saving histograms...')
canvas.SaveAs(saveDirectory+'maxTrackPtFraction_dR0p2.pdf')
print('Saved histograms')
