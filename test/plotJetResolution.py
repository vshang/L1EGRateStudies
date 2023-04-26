from L1Trigger.L1EGRateStudies.trigHelpers import checkDir
from ROOT import *
gROOT.SetBatch(True)

#Select and load root files here
file = 'output_round2_QCD'
date = '02_06_2023'
print('Opening Tfile...')
f1 = TFile.Open('/afs/hep.wisc.edu/home/vshang/public/Phase2L1CaloTaus/CMSSW_12_3_0_pre4/src/L1Trigger/L1EGRateStudies/test/crab/l1CaloJets_r2_CMSSW_12_3_0_pre4/20230206/' + file + '.root')

#Set save directory here
saveDirectory = '/afs/hep.wisc.edu/home/vshang/public/Phase2L1CaloTaus/CMSSW_12_3_0_pre4/src/L1Trigger/L1EGRateStudies/test/resolutions/CMSSW_12_3_0_pre4/' + date + '/' 
checkDir( saveDirectory)

#Set number of histogram bins and maximum value of x and y axis here
nBins = 50
xMin = -1
xMax = 2
yMax = 0.12

#Remove stats box from histograms by setting argument to 0
gStyle.SetOptStat(0)

#Get event tree
print('Getting event tree...')
eventTree1 = f1.Get('analyzer/tree')
#eventTree2 = f2.Get('analyzer/tree')


#Create histogram of jet resolution
hist_barrel = TH1F('hist_barrel', '; (reco p_{T} - gen p_{T})/gen p_{T}; Number of jets (normalized)', nBins, xMin, xMax)
hist_endcap = TH1F('hist_endcap', '; (reco p_{T} - gen p_{T})/gen p_{T}; Number of jets (normalized)', nBins, xMin, xMax)
hist_HF = TH1F('hist_HF', '; (reco p_{T} - gen p_{T})/gen p_{T}; Number of jets (normalized)', nBins, xMin, xMax)
var = '(jet_pt_calibration - genJet_pt)/genJet_pt'
#var = '(calibPtHH - genJet_pt)/genJet_pt'
cut_barrel = 'abs(genJet_eta)<1.2'
cut_endcap = 'abs(genJet_eta)>1.6 && abs(genJet_eta)<2.8'
cut_HF = 'abs(genJet_eta)>3.0 && abs(genJet_eta)<6.0'
print('Filling histograms...')
eventTree1.Draw(var + '>>hist_barrel', cut_barrel)
eventTree1.Draw(var + '>>hist_endcap', cut_endcap)
eventTree1.Draw(var + '>>hist_HF', cut_HF)

#Add overflow bin
hist_barrel.SetBinContent(nBins, hist_barrel.GetBinContent(nBins) + hist_barrel.GetBinContent(nBins+1))
hist_endcap.SetBinContent(nBins, hist_endcap.GetBinContent(nBins) + hist_endcap.GetBinContent(nBins+1))
hist_HF.SetBinContent(nBins, hist_HF.GetBinContent(nBins) + hist_HF.GetBinContent(nBins+1))

#Normalize histograms
hist_barrel.Scale(1/hist_barrel.Integral())
hist_endcap.Scale(1/hist_endcap.Integral())
hist_HF.Scale(1/hist_HF.Integral())

#Draw histogram
print('Drawing plots')
canvas = TCanvas('canvas', 'Jet p_{T} resolution')
hist_barrel.Draw('hist') 
hist_endcap.Draw('hist same')
hist_HF.Draw('hist same')

#Set histogram settings
hist_barrel.SetMinimum(0)
hist_endcap.SetMinimum(0)
hist_HF.SetMinimum(0)
hist_barrel.SetMaximum(yMax)
hist_endcap.SetMaximum(yMax)
hist_HF.SetMaximum(yMax)

hist_barrel.SetLineColor(kGreen)
hist_endcap.SetLineColor(kBlue)
hist_HF.SetLineColor(kRed)

#Draw legend
legend = TLegend(0.55, 0.65, 0.85, 0.85)
legend.AddEntry(hist_barrel, '| #eta | < 1.2', 'l')
legend.AddEntry(hist_endcap, '1.6 < | #eta | < 2.8', 'l')
legend.AddEntry(hist_HF, '3.0 < | #eta | < 6.0', 'l')
legend.Draw('same')
legend.SetBorderSize(0)
legend.SetFillStyle(0)


#Save histograms
print('Saving plots...')
canvas.SaveAs(saveDirectory + file + '_jet_pt_calibration.png')
#canvas.SaveAs(saveDirectory + file + '_calibPtHH.png')
print('Saved plots')
