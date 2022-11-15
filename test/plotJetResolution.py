from L1Trigger.L1EGRateStudies.trigHelpers import checkDir
from ROOT import *

#Select and load root files here
file = 'output_round2_VBFHiggsTauTau_test'
#name = 'output_round2_TTbarv1'
date = '02_09_2021'
f1 = TFile.Open('/afs/hep.wisc.edu/home/vshang/public/test/CMSSW_11_1_3/src/L1Trigger/L1EGRateStudies/test/crab/l1CaloJets_20210101_r2/' + file + '.root')
#f1 = TFile.Open('/afs/hep.wisc.edu/home/vshang/public/Phase2L1CaloTaus/CMSSW_10_5_0_pre1/src/L1Trigger/L1EGRateStudies/test/crab/l1CaloJets_20190909_r2/' + name + '_notTrackMatched.root', '')
#f2 = TFile.Open('/afs/hep.wisc.edu/home/vshang/public/Phase2L1CaloTaus/CMSSW_10_5_0_pre1/src/L1Trigger/L1EGRateStudies/test/crab/l1CaloJets_20190909_r2/' + name + '_trackMatchedwithTrackdR.root', '')
#f2 = TFile.Open('/afs/hep.wisc.edu/home/vshang/public/Phase2L1CaloTaus/CMSSW_10_5_0_pre1/src/L1Trigger/L1EGRateStudies/test/crab/l1CaloJets_20190909_r2/output_round2_HiggsTauTauv1.root', '')

#Set save directory here
saveDirectory = '/afs/hep.wisc.edu/home/vshang/public/test/CMSSW_11_1_3/src/L1Trigger/L1EGRateStudies/test/resolutions/' + date + '/' 
checkDir( saveDirectory)

#Set number of histogram bins and maximum value of x and y axis here
# nBins = 50
# xMin = -0.5
# xMax = 2
# yMax = 0.1
nBins = 50
xMin = -1
xMax = 1
yMax = 1

#Remove stats box from histograms by setting argument to 0
gStyle.SetOptStat(0)

#Get event tree
eventTree1 = f1.Get('analyzer/tree')
#eventTree2 = f2.Get('analyzer/tree')


##Create distribution plots of minimum dR between reco jets and all tracks
##-----------------------------------------------------------------------------------------------

#Define eta list and fill histograms
print('Creating eta list...')
hists = {}
means = []
errs = []
eta_list = [i*0.0873 for i in range(17)] + [1.479+i*0.0845 for i in range(19)]
tower_eta_list = [0.04365+i*0.0873 for i in range(17)] + [1.52125+i*0.0845 for i in range(18)]
print 'eta list = ', eta_list
print 'tower eta list = ', tower_eta_list

for i in range(len(eta_list)-1):
    hist = TH1F('hist', '; P_{T}^{CaloJet} resolution; Fraction of Events', nBins, xMin, xMax)
    hists['hist_'+str(i)] = TH1F('hist_'+str(i), '; P_{T}^{CaloJet} resolution; Fraction of Events', nBins, xMin, xMax)
    var = '(genJet_pt - jet_pt)/genJet_pt'
    cut = 'genJet_eta >= ' + str(eta_list[i]) + ' && genJet_eta < ' + str(eta_list[i+1])
    print ' i = ', i
    print '        var = ', var
    print '        cut = ', cut
    eventTree1.Draw(var + '>>hist', cut)
    hists['hist_'+str(i)] += hist
    print '        hist integral = ', hists['hist_'+str(i)].Integral()
    print '--------------------------'

#Normalize histograms to unit area and set y axis limits
print('Normalizing histograms...')
for name in hists:
    hists[name].Scale(1/hists[name].Integral())
    hists[name].SetMinimum(0)
    hists[name].SetMaximum(yMax)

#Define Gaussian functions to fit and store mean and err
print('Fitting histograms..')
for i in range(len(hists)):
    f1 = TF1('f1', '([0]*exp(-0.5*((x-[1])/[2])^2))', xMin, xMax)
    f1.SetParName(0, 'norm')
    f1.SetParName(1, 'mean')
    f1.SetParName(2, 'err')
    f1.SetParameter(0, 1.)
    f1.SetParameter(1, 0.)
    f1.SetParameter(2, 0.2)
    hists['hist_'+str(i)].Fit('f1')
    means.append(f1.GetParameter('mean'))
    errs.append(abs(f1.GetParameter('err')))

print 'list of means: ', means
print 'list of errs: ', errs

#Define mean and error graphs
n = len(tower_eta_list)
graph_mean = TGraph()
graph_err = TGraph()
for i in range(n):
    graph_mean.SetPoint(i, tower_eta_list[i], means[i])
    graph_err.SetPoint(i, tower_eta_list[i], errs[i])

#Draw graphs
print('Drawing plots')
c_hists = TCanvas('c_hists', 'Jet p_{T} resolution')
for name in hists:
    if name == 'hist_0':
        hists[name].Draw('hist PLC')
        hists[name].SetMinimum(0)
        hists[name].SetMaximum(0.12)
        hists[name].SetTitle('Jet p_{T} resolution')
        hists[name].GetXaxis().SetTitle('(genJet p_{T} - jet p_{T})/genJet p_{T}')
    else:
        hists[name].Draw('hist same PLC')
# for i in range(len(hists)):
#     if i <= 8:
#         hists['hist_'+str(i)].SetLineColor(1+i)
#     else:
#         hists['hist_'+str(i)].SetLineColor(22+i)

legend = TLegend(0.2, 0.65, 0.85, 0.85)
legend.SetNColumns(6)
for i in range(len(hists)):
    legend.AddEntry(hists['hist_'+str(i)], str(eta_list[i]) + ' #leq #eta < ' + str(eta_list[i+1]), 'l')  
legend.Draw('same')
legend.SetBorderSize(0)
legend.SetFillStyle(0)


c_mean = TCanvas('c_mean', 'Jet p_{T} resolution mean')
graph_mean.Draw('ALP')
graph_mean.SetMarkerSize(2)
graph_mean.SetTitle('Jet p_{T} resolution mean vs #eta_{seed}')
graph_mean.GetXaxis().SetTitle('#eta_{seed}')
graph_mean.GetYaxis().SetTitle('Jet p_{T} resolution mean')

c_err = TCanvas('c_err', 'Jet p_{T} resolution standard deviation')
graph_err.Draw('ALP')
graph_err.SetMarkerSize(2)
graph_err.SetTitle('Jet p_{T} resolution std dev vs #eta_{seed}')
graph_err.GetXaxis().SetTitle('#eta_{seed}')
graph_err.GetYaxis().SetTitle('Jet p_{T} resolution std dev')
graph_err.SetMinimum(0)

#Save histograms
print('Saving plots...')
c_hists.SaveAs(saveDirectory + file + '_res.pdf')
c_mean.SaveAs(saveDirectory + file + '_resMean.pdf')
c_err.SaveAs(saveDirectory + file + '_resErr.pdf')
print('Saved plots')
