from ROOT import *

#Select and load root files here
f_VBF = TFile.Open('/afs/hep.wisc.edu/home/vshang/public/test/CMSSW_11_1_3/src/L1Trigger/L1EGRateStudies/test/crab/l1CaloJets_20201116_r2/output_round2_VBFHiggsTauTau_test.root', '')
f_HiggsTauTau = TFile.Open('/afs/hep.wisc.edu/home/vshang/public/test/CMSSW_11_1_3/src/L1Trigger/L1EGRateStudies/test/crab/l1CaloJets_20190909_r2/output_round2_HiggsTauTauv1.root', '')
f_minBias = TFile.Open('/afs/hep.wisc.edu/home/vshang/public/test/CMSSW_11_1_3/src/L1Trigger/L1EGRateStudies/test/crab/l1CaloJets_20190909_r2/output_round2_minBias_withTracks_trackMatched.root', '')

#Set save directory here
saveDirectory = '/afs/hep.wisc.edu/home/vshang/public/test/CMSSW_11_1_3/src/L1Trigger/L1EGRateStudies/test/isoTauStudies/'

#Set number of histogram bins and maximum value of x and y axis here
nBins = 20
xMin = 0
xMax = 2
yMax = 1

#Remove stats box from histograms by setting argument to 0
gStyle.SetOptStat(0)

#Get event tree
eventTree_VBF = f_VBF.Get('analyzer/tree')
eventTree_HiggsTauTau = f_HiggsTauTau.Get('analyzer/tree')
eventTree_minBias = f_minBias.Get('analyzer/tree')

##Create distribution plots of Iso Tau variable
##-----------------------------------------------------------------------------------------------

#Define histograms
print('Creating histograms...')
hist_VBF = TH1F('hist_VBF', 'Tau Relative Isolation Variable; (7x7 p_{T} - 3x5 p_{T})/(3x5 p_{T}); Number of tau jets (normalized)', nBins, xMin, xMax)
hist_HiggsTauTau = TH1F('hist_HiggsTauTau', 'Tau Relative Isolation Variable; (7x7 p_{T} - 3x5 p_{T})/(3x5 p_{T}); Number of tau jets (normalized)', nBins, xMin, xMax)
hist_minBias = TH1F('hist_minBias', 'Tau Relative Isolation Variable; (7x7 p_{T} - 3x5 p_{T})/(3x5 p_{T}); Number of tau jets (normalized)', nBins, xMin, xMax)

#Fill histograms
print('Filling histograms...')
nEntries_VBF = eventTree_VBF.GetEntries()
nEntries_HiggsTauTau = eventTree_HiggsTauTau.GetEntries()
nEntries_minBias = eventTree_VBF.GetEntries()

for i in range(nEntries_VBF):
    eventTree_VBF.GetEntry(i)
    pt_3x5_VBF = eventTree_VBF.calibPtHH
    pt_7x7_VBF = eventTree_VBF.calibIsoRegionPtHH
    isoTauVariable_VBF = (pt_7x7_VBF - pt_3x5_VBF)/pt_3x5_VBF
    hist_VBF.Fill(isoTauVariable_VBF)

for i in range(nEntries_HiggsTauTau):
    eventTree_HiggsTauTau.GetEntry(i)
    pt_3x5_HiggsTauTau = eventTree_HiggsTauTau.calibPtHH
    pt_7x7_HiggsTauTau = eventTree_HiggsTauTau.calibIsoRegionPtHH
    isoTauVariable_HiggsTauTau = (pt_7x7_HiggsTauTau - pt_3x5_HiggsTauTau)/pt_3x5_HiggsTauTau
    hist_HiggsTauTau.Fill(isoTauVariable_HiggsTauTau)

for i in range(nEntries_minBias):
    eventTree_minBias.GetEntry(i)
    pt_3x5_minBias = eventTree_minBias.calibPtHH
    pt_7x7_minBias = eventTree_minBias.calibIsoRegionPtHH
    isoTauVariable_minBias = (pt_7x7_minBias - pt_3x5_minBias)/pt_3x5_minBias
    hist_minBias.Fill(isoTauVariable_minBias)

#Normalize histograms to unit area
print('Normalizing histograms...')
hist_VBF.Scale(1/hist_VBF.Integral())
hist_HiggsTauTau.Scale(1/hist_HiggsTauTau.Integral())
hist_minBias.Scale(1/hist_minBias.Integral())

#Draw histograms
print('Drawing histograms...')
canvas = TCanvas('canvas', 'Tau Relative Isolation Variable')
hist_VBF.Draw('hist')
hist_HiggsTauTau.Draw('hist same')
hist_minBias.Draw('hist same')
#Set histogram options
hist_VBF.SetLineColor(kRed)
hist_VBF.SetLineWidth(1)
hist_VBF.SetMinimum(0)
hist_VBF.SetMaximum(yMax)

hist_HiggsTauTau.SetLineColor(kBlue)
hist_HiggsTauTau.SetLineWidth(1)
hist_HiggsTauTau.SetMinimum(0)
hist_HiggsTauTau.SetMaximum(yMax)

hist_minBias.SetLineColor(kGreen)
hist_minBias.SetLineWidth(1)
hist_minBias.SetMinimum(0)
hist_minBias.SetMaximum(yMax)
#Add legend
legend = TLegend(0.46, 0.73, 0.75, 0.87)
legend.AddEntry(hist_VBF, 'VBF', 'l')
legend.AddEntry(hist_HiggsTauTau, 'HiggsTauTau', 'l')
legend.AddEntry(hist_minBias, 'minBias', 'l')

legend.Draw('same')
legend.SetBorderSize(0)
#Save histogram
print('Saving histogram...')
canvas.SaveAs(saveDirectory+'isoTauVariable.pdf')
print('Saved histogram')
