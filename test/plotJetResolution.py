from L1Trigger.L1EGRateStudies.trigHelpers import checkDir
from ROOT import *
gROOT.SetBatch(True)

#Select and load root files here
file = 'output_round2_VBFHiggsTauTau_13_1X'
#file = 'output_round2_QCD_13_1X'
date = '01_31_2024'
print('Opening Tfile...')
f1 = TFile.Open('/afs/hep.wisc.edu/home/vshang/public/Phase2L1CaloTaus/Pallabi/CMSSW_13_2_0/src/L1Trigger/L1EGRateStudies/test/crab/l1CaloTaus_r2_CMSSW_13_2_0/20240131/' + file + '.root')
#f1 = TFile.Open('/afs/hep.wisc.edu/home/vshang/public/Phase2L1CaloTaus/Pallabi/CMSSW_13_2_0/src/L1Trigger/L1EGRateStudies/test/crab/l1CaloJets_r2_CMSSW_13_2_0/20240131/' + file + '.root')

#Set save directory here
saveDirectory = '/afs/hep.wisc.edu/home/vshang/public/Phase2L1CaloTaus/Pallabi/CMSSW_13_2_0/src/L1Trigger/L1EGRateStudies/test/resolutions/CMSSW_13_2_0/' + date + '/' 
checkDir( saveDirectory)

#Set number of histogram bins and maximum value of x and y axis here
nBins = 50
xMin = -1
xMax = 1
#yMax = 0.09 #Jets
yMax = 0.08 #Taus

#Remove stats box from histograms by setting argument to 0
gStyle.SetOptStat(0)

#Get event tree
print('Getting event tree...')
eventTree1 = f1.Get('analyzer/tree')
#eventTree2 = f2.Get('analyzer/tree')


#Create histogram of jet resolution
hist_barrel = TH1F('hist_barrel', '; (p_{T}^{GCTJet} - p_{T}^{Gen #tau}) / p_{T}^{Gen #tau}; Fraction of Events', nBins, xMin, xMax)
hist_endcap = TH1F('hist_endcap', '; (p_{T}^{GCTJet} - p_{T}^{Gen #tau}) / p_{T}^{Gen #tau}; Fraction of Events', nBins, xMin, xMax)
hist_HF = TH1F('hist_HF', '; (p_{T}^{GCTJet} - p_{T}^{Gen #tau}) / p_{T}^{Gen #tau}; Fraction of Events', nBins, xMin, xMax)
#var = '(jet_pt_calibration - genJet_pt)/genJet_pt'
#var = '(tau_pt - genJet_pt)/genJet_pt'
#var = '(jetEt - genJet_pt)/genJet_pt'
var = '(tauEt - genJet_pt)/genJet_pt'
#var = '(calibPtHH - genJet_pt)/genJet_pt'
#cut_barrel = 'abs(genJet_eta)<1.2'
#cut_barrel = 'abs(genJet_eta)<1.2 && (genJet_pt > 40 && genJet_pt < 100)'
#cut_barrel= 'abs(genJet_eta)<1.2 && genJet_pt > 100'
#cut_endcap = 'abs(genJet_eta)>1.6 && abs(genJet_eta)<2.8'
#cut_HF = 'abs(genJet_eta)>3.0 && abs(genJet_eta)<6.0'
cut_barrel = 'abs(genJet_eta)<1.5 && genJet_pt>20'
cut_endcap = 'abs(genJet_eta)>1.5 && abs(genJet_eta)<3.0 && genJet_pt>20'
cut_HF = 'abs(genJet_eta)>3.0 && abs(genJet_eta)<6.0 && genJet_pt>20'

#denom_cut_label = '40 < p_{T}^{Gen #tau} < 100'
denom_cut_label = 'p_{T}^{Gen #tau} > 20 GeV'

print('Filling histograms...')
eventTree1.Draw(var + '>>hist_barrel', cut_barrel)
eventTree1.Draw(var + '>>hist_endcap', cut_endcap)
eventTree1.Draw(var + '>>hist_HF', cut_HF)

#Add overflow bin
# hist_barrel.SetBinContent(nBins, hist_barrel.GetBinContent(nBins) + hist_barrel.GetBinContent(nBins+1))
# hist_endcap.SetBinContent(nBins, hist_endcap.GetBinContent(nBins) + hist_endcap.GetBinContent(nBins+1))
# hist_HF.SetBinContent(nBins, hist_HF.GetBinContent(nBins) + hist_HF.GetBinContent(nBins+1))

#Normalize histograms
hist_barrel.Scale(1/hist_barrel.Integral())
hist_endcap.Scale(1/hist_endcap.Integral())
hist_HF.Scale(1/hist_HF.Integral())

#Draw histogram
print('Drawing plots')
canvas = TCanvas('canvas', 'Jet p_{T} resolution', 1200, 900)
p = TPad('p','p', 0, 0, 1, 1)
p.Draw()
p.cd()
p.SetGrid()
hist_barrel.Draw('hist e') 
hist_endcap.Draw('hist e same')
#hist_HF.Draw('hist e same')

#Set histogram settings
hist_barrel.SetMinimum(0)
hist_endcap.SetMinimum(0)
hist_HF.SetMinimum(0)
hist_barrel.SetMaximum(yMax)
hist_endcap.SetMaximum(yMax)
hist_HF.SetMaximum(yMax)

hist_barrel.SetLineColor(kRed)
hist_endcap.SetLineColor(kBlue)
hist_HF.SetLineColor(kGreen)

#Draw legend
legend = TLegend(0.57, 0.7, 0.87, 0.9)
# legend.AddEntry(hist_barrel, '| #eta | < 1.2', 'l')
# legend.AddEntry(hist_endcap, '1.6 < | #eta | < 2.8', 'l')
# legend.AddEntry(hist_HF, '3.0 < | #eta | < 6.0', 'l')
legend.AddEntry(hist_barrel, '|#eta^{Gen #tau}| < 1.5', 'lpe')
legend.AddEntry(hist_endcap, '1.5 < |#eta^{Gen #tau}| < 3.0', 'lpe')
#legend.AddEntry(hist_HF, '3.0 < |#eta^{Gen #tau}| < 6.0', 'lpe')
legend.Draw('same')
legend.SetBorderSize(0)
legend.SetFillStyle(0)

#Add TDR style text to plot
title = TLatex()
title.SetTextSize(0.045)
title.DrawLatexNDC(.1, .91, "CMS")
title.SetTextSize(0.030)
title.DrawLatexNDC(.18, .91, "Phase-2 Simulation")
title.SetTextSize(0.035)
title.DrawLatexNDC(.73, .91, "14 TeV, 200 PU")

#Add other text to plot
txt = TLatex()
txt.SetTextSize(0.045)
txt.DrawLatexNDC(.12, .83,  "%s" % denom_cut_label)

#Save histograms
print('Saving plots...')
#canvas.SaveAs(saveDirectory + file + '_jet_pt_calibration.png')
#canvas.SaveAs(saveDirectory + file + '_jetEt.pdf')
canvas.SaveAs(saveDirectory + file + '_tauEt.pdf')
#canvas.SaveAs(saveDirectory + file + '_calibPtHH.png')
#canvas.SaveAs(file + '_test.png')
print('Saved plots')
