from ROOT import *
from L1Trigger.L1EGRateStudies.trigHelpers import checkDir

#Select and load root files here
print 'Loading root files...'
#f_ggHTT = TFile.Open('/data/vshang/l1CaloJets_20190806_r2/output_round2_HiggsTauTau_testv2.root', '')
#f_QCD = TFile.Open('/data/vshang/l1CaloJets_20190806_r2/output_round2_QCD_testv2.root', '')
f_ggHTT = TFile.Open('/afs/hep.wisc.edu/home/vshang/public/Phase2L1CaloTaus/CMSSW_10_5_0_pre1/src/L1Trigger/L1EGRateStudies/test/crab/l1CaloJets_20190909_r2/output_round2_HiggsTauTau_withTracks_notTrackMatched.root', '')
f_QCD = TFile.Open('/afs/hep.wisc.edu/home/vshang/public/Phase2L1CaloTaus/CMSSW_10_5_0_pre1/src/L1Trigger/L1EGRateStudies/test/crab/l1CaloJets_20190909_r2/output_round2_QCDv1.root', '')

#Set date and save directory
date = '20191208'
saveDir = '/afs/hep.wisc.edu/home/vshang/public/Phase2L1CaloTaus/CMSSW_10_5_0_pre1/src/L1Trigger/L1EGRateStudies/test/towerStudies/ROC/' + date + '/'
checkDir( saveDir )

#Set sameCanvas to True for all plots on same Canvas, False if you want seperate plots
sameCanvas = True

#Select number of points to plot
nPoints = 20

#Select eta and pt region to plot
etaRegion = 'barrel'
#etaRegion = 'endcap'
ptRegion = '30to40'
#ptRegion = '40to60'
#ptRegion = 'over60'

#Get event trees
print 'Getting event trees...'
ggHTT_eventTree = f_ggHTT.Get('analyzer/tree')
QCD_eventTree = f_QCD.Get('analyzer/tree')

#Define ROC plots
plot_max2inCross_0L1EG = TGraph(nPoints)
plot_max2inCross_1L1EG = TGraph(nPoints)
plot_max2inCross_2L1EG = TGraph(nPoints)
plot_max3inCross_0L1EG = TGraph(nPoints)
plot_max3inCross_1L1EG = TGraph(nPoints)
plot_max3inCross_2L1EG = TGraph(nPoints)

#Count entries that pass thresholds and calculate efficiencies for ggHTT (signal)
nEntries_ggHTT_0L1EG = 0
nEntries_ggHTT_1L1EG = 0
nEntries_ggHTT_2L1EG = 0

nPass_ggHTT_max2inCross_0L1EG = {}
nPass_ggHTT_max2inCross_1L1EG = {}
nPass_ggHTT_max2inCross_2L1EG = {}
nPass_ggHTT_max3inCross_0L1EG = {}
nPass_ggHTT_max3inCross_1L1EG = {}
nPass_ggHTT_max3inCross_2L1EG = {}

for i in range(nPoints):
    nPass_ggHTT_max2inCross_0L1EG[i] = 0
    nPass_ggHTT_max2inCross_1L1EG[i] = 0
    nPass_ggHTT_max2inCross_2L1EG[i] = 0
    nPass_ggHTT_max3inCross_0L1EG[i] = 0
    nPass_ggHTT_max3inCross_1L1EG[i] = 0
    nPass_ggHTT_max3inCross_2L1EG[i] = 0

#Loop through ggHTT events to get signal efficiencies
nEntries_ggHTT = ggHTT_eventTree.GetEntries()
print 'Looping through ggHTT events...'
etaInRegion = True
ptInRegion = True
for i in range(nEntries_ggHTT):
    ggHTT_eventTree.GetEntry(i)

    if abs(ggHTT_eventTree.genJet_eta) < 1.4 and 30 < ggHTT_eventTree.genJet_pt < 40:
    #if abs(ggHTT_eventTree.genJet_eta) < 1.4 and 40 < ggHTT_eventTree.genJet_pt < 60:
    #if abs(ggHTT_eventTree.genJet_eta) < 1.4 and ggHTT_eventTree.genJet_pt > 60:
    #if 1.6 < abs(ggHTT_eventTree.genJet_eta) < 2.6 and 30 < ggHTT_eventTree.genJet_pt < 40:
    #if 1.6 < abs(ggHTT_eventTree.genJet_eta) < 2.6 and 40 < ggHTT_eventTree.genJet_pt < 60:
    #if 1.6 < abs(ggHTT_eventTree.genJet_eta) < 2.6 and ggHTT_eventTree.genJet_pt > 60:

        ggHTT_CrossTowerList = [ggHTT_eventTree.total_seed, ggHTT_eventTree.total_22, ggHTT_eventTree.total_31, ggHTT_eventTree.total_33, ggHTT_eventTree.total_42]
        ggHTT_CrossTowerList.sort(reverse=True)
        ggHTT_sortedTowers = ggHTT_CrossTowerList
        ggHTT_total_max2inCross = ggHTT_sortedTowers[0] + ggHTT_sortedTowers[1]
        ggHTT_total_max3inCross = ggHTT_sortedTowers[0] + ggHTT_sortedTowers[1] + ggHTT_sortedTowers[2]
        if ggHTT_eventTree.total_3x5 <= 0: continue

        if ggHTT_eventTree.n_l1eg_HoverE_LessThreshold == 0:
            nEntries_ggHTT_0L1EG += 1
        elif ggHTT_eventTree.n_l1eg_HoverE_LessThreshold == 1:
            nEntries_ggHTT_1L1EG += 1
        elif ggHTT_eventTree.n_l1eg_HoverE_LessThreshold >= 2:
            nEntries_ggHTT_2L1EG += 1
        for j in range(nPoints):
            threshold = (j+1.)/nPoints
            if ggHTT_total_max2inCross/float(ggHTT_eventTree.total_3x5) > threshold and ggHTT_eventTree.n_l1eg_HoverE_LessThreshold == 0:
                nPass_ggHTT_max2inCross_0L1EG[j] += 1
            if ggHTT_total_max3inCross/float(ggHTT_eventTree.total_3x5) > threshold and ggHTT_eventTree.n_l1eg_HoverE_LessThreshold == 0:
                nPass_ggHTT_max3inCross_0L1EG[j] += 1
            if ggHTT_total_max2inCross/float(ggHTT_eventTree.total_3x5) > threshold and ggHTT_eventTree.n_l1eg_HoverE_LessThreshold == 1:
                nPass_ggHTT_max2inCross_1L1EG[j] += 1
            if ggHTT_total_max3inCross/float(ggHTT_eventTree.total_3x5) > threshold and ggHTT_eventTree.n_l1eg_HoverE_LessThreshold == 1:
                nPass_ggHTT_max3inCross_1L1EG[j] += 1
            if ggHTT_total_max2inCross/float(ggHTT_eventTree.total_3x5) > threshold and ggHTT_eventTree.n_l1eg_HoverE_LessThreshold == 2:
                nPass_ggHTT_max2inCross_2L1EG[j] += 1
            if ggHTT_total_max3inCross/float(ggHTT_eventTree.total_3x5) > threshold and ggHTT_eventTree.n_l1eg_HoverE_LessThreshold == 2:
                nPass_ggHTT_max3inCross_2L1EG[j] += 1

#Count entries that pass thresholds and calculate efficiencies for QCD (background)
nEntries_QCD_0L1EG = 0
nEntries_QCD_1L1EG = 0
nEntries_QCD_2L1EG = 0

nPass_QCD_max2inCross_0L1EG = {}
nPass_QCD_max2inCross_1L1EG = {}
nPass_QCD_max2inCross_2L1EG = {}
nPass_QCD_max3inCross_0L1EG = {}
nPass_QCD_max3inCross_1L1EG = {}
nPass_QCD_max3inCross_2L1EG = {}

for i in range(nPoints):
    nPass_QCD_max2inCross_0L1EG[i] = 0
    nPass_QCD_max2inCross_1L1EG[i] = 0
    nPass_QCD_max2inCross_2L1EG[i] = 0
    nPass_QCD_max3inCross_0L1EG[i] = 0
    nPass_QCD_max3inCross_1L1EG[i] = 0
    nPass_QCD_max3inCross_2L1EG[i] = 0

#Loop through QCD events to get background efficiencies
nEntries_QCD = QCD_eventTree.GetEntries()
print 'Looping through QCD events...'
for i in range(nEntries_QCD):
    QCD_eventTree.GetEntry(i)

    if abs(QCD_eventTree.genJet_eta) < 1.4 and 30 < QCD_eventTree.genJet_pt < 40:
    #if abs(QCD_eventTree.genJet_eta) < 1.4 and 40 < QCD_eventTree.genJet_pt < 60:
    #if abs(QCD_eventTree.genJet_eta) < 1.4 and QCD_eventTree.genJet_pt > 60:
    #if 1.6 < abs(QCD_eventTree.genJet_eta) < 2.6 and 30 < QCD_eventTree.genJet_pt < 40:
    #if 1.6 < abs(QCD_eventTree.genJet_eta) < 2.6 and 40 < QCD_eventTree.genJet_pt < 60:
    #if 1.6 < abs(QCD_eventTree.genJet_eta) < 2.6 and QCD_eventTree.genJet_pt > 60:

        QCD_CrossTowerList = [QCD_eventTree.total_seed, QCD_eventTree.total_22, QCD_eventTree.total_31, QCD_eventTree.total_33, QCD_eventTree.total_42]
        QCD_CrossTowerList.sort(reverse=True)
        QCD_sortedTowers = QCD_CrossTowerList
        QCD_total_max2inCross = QCD_sortedTowers[0] + QCD_sortedTowers[1]
        QCD_total_max3inCross = QCD_sortedTowers[0] + QCD_sortedTowers[1] + QCD_sortedTowers[2]
        if QCD_eventTree.total_3x5 <= 0: continue

        if QCD_eventTree.n_l1eg_HoverE_LessThreshold == 0:
            nEntries_QCD_0L1EG += 1
        elif QCD_eventTree.n_l1eg_HoverE_LessThreshold == 1:
            nEntries_QCD_1L1EG += 1
        elif QCD_eventTree.n_l1eg_HoverE_LessThreshold >= 2:
            nEntries_QCD_2L1EG += 1
        for j in range(nPoints):
            threshold = (j+1.)/nPoints
            if QCD_total_max2inCross/float(QCD_eventTree.total_3x5) > threshold and QCD_eventTree.n_l1eg_HoverE_LessThreshold == 0:
                nPass_QCD_max2inCross_0L1EG[j] += 1
            if QCD_total_max3inCross/float(QCD_eventTree.total_3x5) > threshold and QCD_eventTree.n_l1eg_HoverE_LessThreshold == 0:
                nPass_QCD_max3inCross_0L1EG[j] += 1
            if QCD_total_max2inCross/float(QCD_eventTree.total_3x5) > threshold and QCD_eventTree.n_l1eg_HoverE_LessThreshold == 1:
                nPass_QCD_max2inCross_1L1EG[j] += 1
            if QCD_total_max3inCross/float(QCD_eventTree.total_3x5) > threshold and QCD_eventTree.n_l1eg_HoverE_LessThreshold == 1:
                nPass_QCD_max3inCross_1L1EG[j] += 1
            if QCD_total_max2inCross/float(QCD_eventTree.total_3x5) > threshold and QCD_eventTree.n_l1eg_HoverE_LessThreshold == 2:
                nPass_QCD_max2inCross_2L1EG[j] += 1
            if QCD_total_max3inCross/float(QCD_eventTree.total_3x5) > threshold and QCD_eventTree.n_l1eg_HoverE_LessThreshold == 2:
                nPass_QCD_max3inCross_2L1EG[j] += 1

#Define signal efficiencies
print 'Calculating signal efficiencies...'
eff_ggHTT_max2inCross_0L1EG = {}
eff_ggHTT_max2inCross_1L1EG = {}
eff_ggHTT_max2inCross_2L1EG = {}
eff_ggHTT_max3inCross_0L1EG = {}
eff_ggHTT_max3inCross_1L1EG = {}
eff_ggHTT_max3inCross_2L1EG = {}

for i in range(nPoints):
    eff_ggHTT_max2inCross_0L1EG[i] = nPass_ggHTT_max2inCross_0L1EG[i]/max(float(nEntries_ggHTT_0L1EG),1.0)
    eff_ggHTT_max2inCross_1L1EG[i] = nPass_ggHTT_max2inCross_1L1EG[i]/max(float(nEntries_ggHTT_1L1EG),1.0)
    eff_ggHTT_max2inCross_2L1EG[i] = nPass_ggHTT_max2inCross_2L1EG[i]/max(float(nEntries_ggHTT_2L1EG),1.0)
    eff_ggHTT_max3inCross_0L1EG[i] = nPass_ggHTT_max3inCross_0L1EG[i]/max(float(nEntries_ggHTT_0L1EG),1.0)
    eff_ggHTT_max3inCross_1L1EG[i] = nPass_ggHTT_max3inCross_1L1EG[i]/max(float(nEntries_ggHTT_1L1EG),1.0)
    eff_ggHTT_max3inCross_2L1EG[i] = nPass_ggHTT_max3inCross_2L1EG[i]/max(float(nEntries_ggHTT_2L1EG),1.0)

#Define background efficiencies
print 'Calculating background efficiencies...'
eff_QCD_max2inCross_0L1EG = {}
eff_QCD_max2inCross_1L1EG = {}
eff_QCD_max2inCross_2L1EG = {}
eff_QCD_max3inCross_0L1EG = {}
eff_QCD_max3inCross_1L1EG = {}
eff_QCD_max3inCross_2L1EG = {}

for i in range(nPoints):
    eff_QCD_max2inCross_0L1EG[i] = nPass_QCD_max2inCross_0L1EG[i]/max(float(nEntries_QCD_0L1EG),1.0)
    eff_QCD_max2inCross_1L1EG[i] = nPass_QCD_max2inCross_1L1EG[i]/max(float(nEntries_QCD_1L1EG),1.0)
    eff_QCD_max2inCross_2L1EG[i] = nPass_QCD_max2inCross_2L1EG[i]/max(float(nEntries_QCD_2L1EG),1.0)
    eff_QCD_max3inCross_0L1EG[i] = nPass_QCD_max3inCross_0L1EG[i]/max(float(nEntries_QCD_0L1EG),1.0)
    eff_QCD_max3inCross_1L1EG[i] = nPass_QCD_max3inCross_1L1EG[i]/max(float(nEntries_QCD_1L1EG),1.0)
    eff_QCD_max3inCross_2L1EG[i] = nPass_QCD_max3inCross_2L1EG[i]/max(float(nEntries_QCD_2L1EG),1.0)

#Fill ROC plots
print 'Filling in ROC plots...'
for i in range(nPoints):
    plot_max2inCross_0L1EG.SetPoint(i,eff_ggHTT_max2inCross_0L1EG[i],1.0-eff_QCD_max2inCross_0L1EG[i])
    plot_max2inCross_1L1EG.SetPoint(i,eff_ggHTT_max2inCross_1L1EG[i],1.0-eff_QCD_max2inCross_1L1EG[i])
    plot_max2inCross_2L1EG.SetPoint(i,eff_ggHTT_max2inCross_2L1EG[i],1.0-eff_QCD_max2inCross_2L1EG[i])
    plot_max3inCross_0L1EG.SetPoint(i,eff_ggHTT_max3inCross_0L1EG[i],1.0-eff_QCD_max3inCross_0L1EG[i])
    plot_max3inCross_1L1EG.SetPoint(i,eff_ggHTT_max3inCross_1L1EG[i],1.0-eff_QCD_max3inCross_1L1EG[i])
    plot_max3inCross_2L1EG.SetPoint(i,eff_ggHTT_max3inCross_2L1EG[i],1.0-eff_QCD_max3inCross_2L1EG[i])

#Draw max2inCross_0L1EG ROC plot
print 'Drawing max2inCross_0L1EG ROC plot...'
if sameCanvas:
    c = TCanvas('c', 'Tower energy fraction ROC plots')
    c.Divide(3,2)
    c.cd(1)
else:
    c_max2inCross_0L1EG = TCanvas('c_max2inCross_0L1EG', ' max2inCross_0L1EG Tower energy fraction ROC plot')
plot_max2inCross_0L1EG.SetTitle('max2inCross_0L1EG Tower energy fraction ROC plot')
plot_max2inCross_0L1EG.GetXaxis().SetTitle('Signal efficiency')
plot_max2inCross_0L1EG.GetYaxis().SetTitle('Background rejection')
plot_max2inCross_0L1EG.SetLineWidth(2)
plot_max2inCross_0L1EG.SetLineColor(kBlue)
plot_max2inCross_0L1EG.Draw('APC')
if not sameCanvas:
    c_max2inCross_0L1EG.SaveAs(saveDir+'towerEFracROC_max2inCross0L1EG_'+ etaRegion + '_' + ptRegion +'.pdf')

#Draw max2inCross_1L1EG ROC plot
print 'Drawing max2inCross_1L1EG ROC plot...'
if sameCanvas:
    c.cd(2)
else:
    c_max2inCross_1L1EG = TCanvas('c_max2inCross_1L1EG', ' max2inCross_1L1EG Tower energy fraction ROC plot')
plot_max2inCross_1L1EG.SetTitle('max2inCross_1L1EG Tower energy fraction ROC plot')
plot_max2inCross_1L1EG.GetXaxis().SetTitle('Signal efficiency')
plot_max2inCross_1L1EG.GetYaxis().SetTitle('Background rejection')
plot_max2inCross_1L1EG.SetLineWidth(2)
plot_max2inCross_1L1EG.SetLineColor(kBlue)
plot_max2inCross_1L1EG.Draw('APC')
if not sameCanvas:
    c_max2inCross_1L1EG.SaveAs(saveDir+'towerEFracROC_max2inCross1L1EG_'+ etaRegion + '_' + ptRegion +'.pdf')

#Draw max2inCross_2L1EG ROC plot
print 'Drawing max2inCross_2L1EG ROC plot...'
if sameCanvas:
    c.cd(3)
else:
    c_max2inCross_2L1EG = TCanvas('c_max2inCross_2L1EG', ' max2inCross_2L1EG Tower energy fraction ROC plot')
plot_max2inCross_2L1EG.SetTitle('max2inCross_2L1EG Tower energy fraction ROC plot')
plot_max2inCross_2L1EG.GetXaxis().SetTitle('Signal efficiency')
plot_max2inCross_2L1EG.GetYaxis().SetTitle('Background rejection')
plot_max2inCross_2L1EG.SetLineWidth(2)
plot_max2inCross_2L1EG.SetLineColor(kBlue)
plot_max2inCross_2L1EG.Draw('APC')
if not sameCanvas:
    c_max2inCross_2L1EG.SaveAs(saveDir+'towerEFracROC_max2inCross2L1EG_'+ etaRegion + '_' + ptRegion +'.pdf')

#Draw max3inCross_0L1EG ROC plot
print 'Drawing max3inCross_0L1EG ROC plot...'
if sameCanvas:
    c.cd(4)
else:
    c_max3inCross_0L1EG = TCanvas('c_max3inCross_0L1EG', ' max3inCross_0L1EG Tower energy fraction ROC plot')
plot_max3inCross_0L1EG.SetTitle('max3inCross_0L1EG Tower energy fraction ROC plot')
plot_max3inCross_0L1EG.GetXaxis().SetTitle('Signal efficiency')
plot_max3inCross_0L1EG.GetYaxis().SetTitle('Background rejection')
plot_max3inCross_0L1EG.SetLineWidth(2)
plot_max3inCross_0L1EG.SetLineColor(kBlue)
plot_max3inCross_0L1EG.Draw('APC')
if not sameCanvas:
    c_max3inCross_0L1EG.SaveAs(saveDir+'towerEFracROC_max3inCross0L1EG_'+ etaRegion + '_' + ptRegion +'.pdf')

#Draw max3inCross_1L1EG ROC plot
print 'Drawing max3inCross_1L1EG ROC plot...'
if sameCanvas:
    c.cd(5)
else:
    c_max3inCross_1L1EG = TCanvas('c_max3inCross_1L1EG', ' max3inCross_1L1EG Tower energy fraction ROC plot')
plot_max3inCross_1L1EG.SetTitle('max3inCross_1L1EG Tower energy fraction ROC plot')
plot_max3inCross_1L1EG.GetXaxis().SetTitle('Signal efficiency')
plot_max3inCross_1L1EG.GetYaxis().SetTitle('Background rejection')
plot_max3inCross_1L1EG.SetLineWidth(2)
plot_max3inCross_1L1EG.SetLineColor(kBlue)
plot_max3inCross_1L1EG.Draw('APC')
if not sameCanvas:
    c_max3inCross_1L1EG.SaveAs(saveDir+'towerEFracROC_max3inCross1L1EG_'+ etaRegion + '_' + ptRegion +'.pdf')

#Draw max3inCross_2L1EG ROC plot
print 'Drawing max3inCross_2L1EG ROC plot...'
if sameCanvas:
    c.cd(6)
else:
    c_max3inCross_2L1EG = TCanvas('c_max3inCross_2L1EG', ' max3inCross_2L1EG Tower energy fraction ROC plot')
plot_max3inCross_2L1EG.SetTitle('max3inCross_2L1EG Tower energy fraction ROC plot')
plot_max3inCross_2L1EG.GetXaxis().SetTitle('Signal efficiency')
plot_max3inCross_2L1EG.GetYaxis().SetTitle('Background rejection')
plot_max3inCross_2L1EG.SetLineWidth(2)
plot_max3inCross_2L1EG.SetLineColor(kBlue)
plot_max3inCross_2L1EG.Draw('APC')
if not sameCanvas:
    c_max3inCross_2L1EG.SaveAs(saveDir+'towerEFracROC_max3inCross2L1EG_'+ etaRegion + '_' + ptRegion +'.pdf')

if sameCanvas:
    print 'Saving ROC plots on same canvas...'
    c.SaveAs(saveDir+'towerEFracROC_' + etaRegion + '_' + ptRegion + '.pdf')
