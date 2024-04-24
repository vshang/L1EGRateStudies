from L1Trigger.L1EGRateStudies.trigHelpers import checkDir
from ROOT import *
gROOT.SetBatch(True)

#Select and load root files here
#file = 'output_round2_QCD'
#file = 'output_round2_QCD_Pallabi'
#file = 'output_round2_minBias_13_1X_nocalib5GeVseed12jets'
file = 'output_round2_minBias_13_1X_nocalib5GeVmaxTT12jets'
date = '03_21_2024'
print('Opening Tfile...')
#f1 = TFile.Open('/afs/hep.wisc.edu/home/vshang/public/Phase2L1CaloTaus/CMSSW_14_0_0_pre3/src/L1Trigger/L1EGRateStudies/test/crab/l1CaloJets_r2_CMSSW_14_0_0_pre3/20240319/' + file + '.root')
f1 = TFile.Open('/afs/hep.wisc.edu/home/vshang/public/Phase2L1CaloTaus/CMSSW_14_0_0_pre3/src/L1Trigger/L1EGRateStudies/test/crab/l1CaloJets_r2_CMSSW_14_0_0_pre3/20240321/' + file + '.root')
#Set save directory here
saveDirectory = '/afs/hep.wisc.edu/home/vshang/public/Phase2L1CaloTaus/CMSSW_12_5_2_patch1/src/L1Trigger/L1EGRateStudies/test/jetpT/CMSSW_12_5_2_patch1/' + date + '/' 
checkDir( saveDirectory)

#Set number of histogram bins and maximum value of x and y axis here
#nBins = 50
nBins = 20
xMin = 0
#xMax = 2000
xMax = 100

#Remove stats box from histograms by setting argument to 0
#gStyle.SetOptStat(0)

#Get event tree
print('Getting event tree...')
eventTree1 = f1.Get('analyzer/tree')
#eventTree2 = f2.Get('analyzer/tree')


#Create histogram of jet resolution
hist_barrel = TH1F('hist_barrel', '; reco p_{T}; Number of jets (normalized)', nBins, xMin, xMax)
#hist_endcap = TH1F('hist_endcap', '; reco p_{T}; Number of jets (normalized)', nBins, xMin, xMax)
#hist_HF = TH1F('hist_HF', '; reco p_{T}; Number of jets (normalized)', nBins, xMin, xMax)
#var = 'jet_pt_calibration'
var = 'calibPtHH'
#var = 'jetEt'
cut_barrel = 'abs(genJet_eta)<1.5'# && ((jet_pt_calibration - genJet_pt)/genJet_pt)>0'
#cut_endcap = 'abs(genJet_eta)>1.6 && abs(genJet_eta)<2.8'
#cut_HF = 'abs(genJet_eta)>3.0 && abs(genJet_eta)<6.0'
print('Filling histograms...')
previous_event = -1
max_pt = 0
count = 0
for row in eventTree1:
    evt = row.event
    # Initial row
    if previous_event == -1 : previous_event = evt
    # If new event, then fill value from previous
    if previous_event != evt :
        if max_pt > 0. :
            hist_barrel.Fill( max_pt )
            max_pt = 0.
            count += 1
        previous_event = evt

    # Skip jets outside of eta threshold region
    #eta = getattr( row, 'jet_eta' )
    eta = getattr( row, 'jetEta' )
    if abs(eta) >= 1.5 : continue
    if abs(eta) < 0 : continue

    pt = getattr( row, var )
    if pt > max_pt : max_pt = pt
#eventTree1.Draw(var + '>>hist_barrel', cut_barrel)
#eventTree1.Draw(var + '>>hist_endcap', cut_endcap)
#eventTree1.Draw(var + '>>hist_HF', cut_HF)

#Add overflow bin
hist_barrel.SetBinContent(nBins, hist_barrel.GetBinContent(nBins) + hist_barrel.GetBinContent(nBins+1))
#hist_endcap.SetBinContent(nBins, hist_endcap.GetBinContent(nBins) + hist_endcap.GetBinContent(nBins+1))
#hist_HF.SetBinContent(nBins, hist_HF.GetBinContent(nBins) + hist_HF.GetBinContent(nBins+1))

#Normalize histograms
#hist_barrel.Scale(1/hist_barrel.Integral())
#hist_endcap.Scale(1/hist_endcap.Integral())
#hist_HF.Scale(1/hist_HF.Integral())

#Draw histogram
print('Drawing plots')
canvas = TCanvas('canvas', 'CaloJet p_{T}')
hist_barrel.Draw('hist') 
#hist_endcap.Draw('hist same')
#hist_HF.Draw('hist same')

#Set histogram settings
hist_barrel.SetMinimum(0)
#hist_endcap.SetMinimum(0)
#hist_HF.SetMinimum(0)
yMax = hist_barrel.GetBinContent(hist_barrel.GetMaximumBin())
hist_barrel.SetMaximum(1.25*yMax)
#hist_endcap.SetMaximum(yMax)
#hist_HF.SetMaximum(yMax)

hist_barrel.SetLineColor(kBlue)
#hist_endcap.SetLineColor(kBlue)
#hist_HF.SetLineColor(kRed)

#Draw legend
legend = TLegend(0.55, 0.65, 0.85, 0.85)
legend.AddEntry(hist_barrel, '| #eta | < 1.5', 'l')
#legend.AddEntry(hist_endcap, '1.6 < | #eta | < 2.8', 'l')
#legend.AddEntry(hist_HF, '3.0 < | #eta | < 6.0', 'l')
legend.Draw('same')
legend.SetBorderSize(0)
legend.SetFillStyle(0)


#Save histograms
print('Saving plots...')
#canvas.SaveAs(saveDirectory + file + '_jet_pt_calibration_maxEventpT.png')
canvas.SaveAs(saveDirectory + file + '_calibPtHH_maxEventpT.png')
#canvas.SaveAs(saveDirectory + file + '_jetEt_maxEventpT.png')
#canvas.SaveAs(file+'_calibPtHH_maxEventpT.png')
print('Saved plots')

print ('Final event count = ' + str(count))
