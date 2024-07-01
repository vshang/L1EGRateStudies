from L1Trigger.L1EGRateStudies.trigHelpers import checkDir
from ROOT import *
gROOT.SetBatch(True)

#Define CMS Colors (see https://cms-analysis.docs.cern.ch/guidelines/plotting/colors/)
ColorA = TColor.GetColor("#5790fc")
ColorB = TColor.GetColor("#f89c20")
ColorC = TColor.GetColor("#e42536")
ColorD = TColor.GetColor("#964a8b")
ColorE = TColor.GetColor("#9c9ca1")
ColorF = TColor.GetColor("#7a21dd")

#Select and load root files here
#doTau = False
doTau = True
if doTau:
    file = 'output_round2_VBFHiggsTauTau_13_1X_calib3GeVmaxTT12jets'
    genObj = 'GEN #tau'
    GCTObj = 'GCTTau'
else:
    file = 'output_round2_QCD_13_1X_calib3GeVmaxTT12jets'
    genObj = 'GEN Jet'
    GCTObj = 'GCTJet'
date = '04_04_2024'
print('Opening Tfile...')
if doTau:
    f1 = TFile.Open('/afs/hep.wisc.edu/home/vshang/public/Phase2L1CaloTaus/CMSSW_14_0_0_pre3/src/L1Trigger/L1EGRateStudies/test/crab/l1CaloTaus_r2_CMSSW_14_0_0_pre3/20240404/' + file + '.root')
else:
    f1 = TFile.Open('/afs/hep.wisc.edu/home/vshang/public/Phase2L1CaloTaus/CMSSW_14_0_0_pre3/src/L1Trigger/L1EGRateStudies/test/crab/l1CaloJets_r2_CMSSW_14_0_0_pre3/20240404/' + file + '.root')

#Set save directory here
saveDirectory = '/afs/hep.wisc.edu/home/vshang/public/Phase2L1CaloTaus/CMSSW_14_0_0_pre3/src/L1Trigger/L1EGRateStudies/test/resolutions/CMSSW_14_0_0_pre3/' + date + '/' + file + '/'
checkDir( saveDirectory)

#Set number of histogram bins and maximum value of x and y axis here
nBins = 50
xMin = -1
xMax = 1
if doTau:
    #yMax = 0.08 #Taus
    #yMax = 0.6 #eta
    yMax = 0.45 #phi
else:
    #yMax = 0.09 #Jets
    yMax = 0.5 #eta
    #yMax = 0.45 #phi

#Remove stats box from histograms by setting argument to 0
gStyle.SetOptStat(0)

#Get event tree
print('Getting event tree...')
eventTree1 = f1.Get('analyzer/tree')
#eventTree2 = f2.Get('analyzer/tree')


#Create histogram of jet resolution
# hist_barrel = TH1F('hist_barrel', '; (p_{T}^{'+GCTObj+'} - p_{T}^{'+genObj+'}) / p_{T}^{'+genObj+'}; Fraction of Events', nBins, xMin, xMax)
# hist_endcap = TH1F('hist_endcap', '; (p_{T}^{'+GCTObj+'} - p_{T}^{'+genObj+'}) / p_{T}^{'+genObj+'}; Fraction of Events', nBins, xMin, xMax)
# hist_barrel = TH1F('hist_barrel', '; (#eta^{'+GCTObj+'} - #eta^{'+genObj+'}) / #eta^{'+genObj+'}; Fraction of Events', nBins, xMin, xMax)
# hist_endcap = TH1F('hist_endcap', '; (#eta^{'+GCTObj+'} - #eta^{'+genObj+'}) / #eta^{'+genObj+'}; Fraction of Events', nBins, xMin, xMax)
hist_barrel = TH1F('hist_barrel', '; (#phi^{'+GCTObj+'} - #phi^{'+genObj+'}) / #phi^{'+genObj+'}; Fraction of Events', nBins, xMin, xMax)
hist_endcap = TH1F('hist_endcap', '; (#phi^{'+GCTObj+'} - #phi^{'+genObj+'}) / #phi^{'+genObj+'}; Fraction of Events', nBins, xMin, xMax)
#hist_HF = TH1F('hist_HF', '; (p_{T}^{'+GCTObj+'} - p_{T}^{'+genObj+'}) / p_{T}^{'+genObj+'}; Fraction of Events', nBins, xMin, xMax)
#var = '(jet_pt_calibration - genJet_pt)/genJet_pt'
#var = '(tau_pt - genJet_pt)/genJet_pt'
if doTau:
    #var = '(tauEt - genJet_pt)/genJet_pt'
    #var = '(calibPtHH - genJet_pt)/genJet_pt'
    #var = '(jetEta - genJet_eta)/genJet_eta'
    var = '(jetPhi - genJet_phi)/genJet_phi'
else:
    #var = '(jetEt - genJet_pt)/genJet_pt'
    #var = '(calibPtHH - genJet_pt)/genJet_pt'
    var = '(jetEta - genJet_eta)/genJet_eta'
    #var = '(jetPhi - genJet_phi)/genJet_phi'
cut_barrel = 'abs(genJet_eta)<1.5 && genJet_pt>20'
cut_endcap = 'abs(genJet_eta)>1.5 && abs(genJet_eta)<2.5 && genJet_pt>20'
#cut_HF = 'abs(genJet_eta)>3.0 && abs(genJet_eta)<5.0 && genJet_pt>20'
# cut_barrel = 'abs(genJet_eta)<1.5 && genJet_pt>30 && genJet_pt<50'
# cut_endcap = 'abs(genJet_eta)>1.5 && abs(genJet_eta)<3.0 && genJet_pt>30 && genJet_pt<50'
# cut_HF = 'abs(genJet_eta)>3.0 && abs(genJet_eta)<6.0 && genJet_pt>30 && genJet_pt<50'
# cut_barrel = 'abs(genJet_eta)<1.5 && jetEt>30 && jetEt<50'
# cut_endcap = 'abs(genJet_eta)>1.5 && abs(genJet_eta)<3.0 && jetEt>30 && jetEt<50'
# cut_HF = 'abs(genJet_eta)>3.0 && abs(genJet_eta)<6.0 && jetEt>30 && jetEt<50'

denom_cut_label = 'p_{T}^{'+genObj+'} > 20 GeV'
#denom_cut_label = '30 < p_{T}^{'+genObj+'} < 50 GeV'
#denom_cut_label = '30 < p_{T}^{'+GCTObj+'} < 50 GeV'

print('Filling histograms...')
eventTree1.Draw(var + '>>hist_barrel', cut_barrel)
eventTree1.Draw(var + '>>hist_endcap', cut_endcap)
#eventTree1.Draw(var + '>>hist_HF', cut_HF)

#Add overflow bin
# hist_barrel.SetBinContent(nBins, hist_barrel.GetBinContent(nBins) + hist_barrel.GetBinContent(nBins+1))
# hist_endcap.SetBinContent(nBins, hist_endcap.GetBinContent(nBins) + hist_endcap.GetBinContent(nBins+1))
# hist_HF.SetBinContent(nBins, hist_HF.GetBinContent(nBins) + hist_HF.GetBinContent(nBins+1))

#Normalize histograms
hist_barrel.Scale(1/hist_barrel.Integral())
hist_endcap.Scale(1/hist_endcap.Integral())
#hist_HF.Scale(1/hist_HF.Integral())

#Draw histogram
print('Drawing plots')
canvas = TCanvas('canvas', 'Jet p_{T} resolution', 1200, 900)
#canvas = TCanvas('canvas', 'Jet #eta resolution', 1200, 900)
#canvas = TCanvas('canvas', 'Jet #phi resolution', 1200, 900)
p = TPad('p','p', 0, 0, 1, 1)
p.Draw()
p.cd()
p.SetGrid()
hist_barrel.Draw('pe')
hist_endcap.Draw('pe same')
# if not doTau:
#     hist_HF.Draw('pe same')
#hist_endcap.Draw('hist e')

#Fit histograms

def Cruijff(x, par):
    norm = par[0]
    mean = par[1]
    sigmaL = par[2]
    sigmaR = par[3]
    alphaL = par[4]
    alphaR = par[5]
    dx = x[0] - mean
    sigma = sigmaL
    alpha = alphaL
    if dx > 0:
        sigma = sigmaR
        alpha = alphaR
    f = 2*sigma*sigma + alpha*dx*dx
    y = norm * exp(-dx*dx/f)
    return y

f1Barrel = TF1('fitBarrel', Cruijff, -1.0, 1.0, 6)
f1Endcap = TF1('fitEndcap', Cruijff, -1.0, 1.0, 6)
f1Barrel.SetParameters(0.1, 0, 0.02, 0.02, 0.01, 0.01)
#f1Endcap.SetParameters(0.1, 0, 0.02, 0.02, 0.01, 0.01)
f1Endcap.SetParameters(0.3, 0, 0.01, 0.01, 0.02, 0.02)
f1Barrel.FixParameter(0, 0.44)
#f1Endcap.FixParameter(0, 0.064)
hist_barrel.Fit('fitBarrel')
hist_endcap.Fit('fitEndcap')
f1Barrel.SetLineColor(ColorA)
f1Endcap.SetLineColor(ColorB)
f1Barrel.SetLineWidth(2)
f1Endcap.SetLineWidth(2)
f1Barrel.Draw('same')
f1Endcap.Draw('same')

#Set histogram settings
hist_barrel.SetMinimum(0)
hist_endcap.SetMinimum(0)
#hist_HF.SetMinimum(0)
hist_barrel.SetMaximum(yMax)
hist_endcap.SetMaximum(yMax)
#hist_HF.SetMaximum(yMax)

hist_barrel.SetLineColor(ColorA)
hist_endcap.SetLineColor(ColorB)
#hist_HF.SetLineColor(ColorC)
hist_barrel.SetLineWidth(2)
hist_endcap.SetLineWidth(2)
#hist_HF.SetLineWidth(2)

hist_barrel.SetMarkerStyle(20)
hist_endcap.SetMarkerStyle(21)
#hist_HF.SetMarkerStyle(22)
hist_barrel.SetMarkerSize(2)
hist_endcap.SetMarkerSize(2)
#hist_HF.SetMarkerSize(2)
hist_barrel.SetMarkerColor(ColorA)
hist_endcap.SetMarkerColor(ColorB)
#hist_HF.SetMarkerColor(ColorC)

hist_barrel.GetXaxis().SetTitleOffset(1.3)
hist_endcap.GetXaxis().SetTitleOffset(1.3)
#hist_HF.GetXaxis().SetTitleOffset(1.2)

#Draw legend
legend = TLegend(0.57, 0.7, 0.87, 0.9)
# legend.AddEntry(hist_barrel, '| #eta | < 1.2', 'l')
# legend.AddEntry(hist_endcap, '1.6 < | #eta | < 2.8', 'l')
# legend.AddEntry(hist_HF, '3.0 < | #eta | < 6.0', 'l')
legend.AddEntry(hist_barrel, '|#eta^{'+genObj+'}| < 1.5', 'lpe')
legend.AddEntry(hist_endcap, '1.5 < |#eta^{'+genObj+'}| < 2.5', 'lpe')
# if not doTau:
#     legend.AddEntry(hist_HF, '3.0 < |#eta^{'+genObj+'}| < 5.0', 'lpe')
legend.Draw('same')
legend.SetBorderSize(0)
legend.SetFillStyle(0)

#Add TDR style text to plot
title = TLatex()
title.SetTextSize(0.045)
title.DrawLatexNDC(.1, .91, "CMS")
title.SetTextSize(0.030)
title.DrawLatexNDC(.18, .91, "Phase-2 Simulation Preliminary")
title.SetTextSize(0.035)
title.DrawLatexNDC(.73, .91, "14 TeV, 200 PU")

#Add other text to plot
txt = TLatex()
txt.SetTextSize(0.045)
txt.DrawLatexNDC(.12, .83,  "%s" % denom_cut_label)

#Save histograms
print('Saving plots...')
#canvas.SaveAs(saveDirectory + file + '_jet_pt_calibration.png')
#canvas.SaveAs(saveDirectory + file + '_jetEta.png')
canvas.SaveAs(saveDirectory + file + '_tauPhi.pdf')
#canvas.SaveAs(saveDirectory + file + '_calibPtHH.png')
#canvas.SaveAs(file + '_test.png')
print('Saved plots')
