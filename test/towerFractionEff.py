from ROOT import *

#Select and load root files here
#f_ggHTT = TFile.Open('/data/vshang/l1CaloJets_20190806_r2/output_round2_HiggsTauTau_testv2.root', '')
#f_QCD = TFile.Open('/data/vshang/l1CaloJets_20190806_r2/output_round2_QCD_testv2.root', '')
f_ggHTT = TFile.Open('/afs/hep.wisc.edu/home/vshang/public/Phase2L1CaloTaus/CMSSW_10_5_0_pre1/src/L1Trigger/L1EGRateStudies/test/crab/l1CaloJets_20190909_r2/output_round2_HiggsTauTau_withTracks_notTrackMatched.root', '')
f_QCD = TFile.Open('/afs/hep.wisc.edu/home/vshang/public/Phase2L1CaloTaus/CMSSW_10_5_0_pre1/src/L1Trigger/L1EGRateStudies/test/crab/l1CaloJets_20190909_r2/output_round2_QCDv1.root', '')

#Define thresholds for tower fraction
threshold_max2inCross_0L1EG = 0.85
threshold_max2inCross_1L1EG = 0.85
threshold_max2inCross_2L1EG = 0.85
threshold_max3inCross_0L1EG = 0.9
threshold_max3inCross_1L1EG = 0.9
threshold_max3inCross_2L1EG = 0.9

#Get event trees
ggHTT_eventTree = f_ggHTT.Get('analyzer/tree')
QCD_eventTree = f_QCD.Get('analyzer/tree')

#Count entries that pass thresholds and calculate efficiencies for ggHTT
nEntries_ggHTT_0L1EG = 0
nEntries_ggHTT_1L1EG = 0
nEntries_ggHTT_2L1EG = 0

nPass_ggHTT_max2inCross_0L1EG = 0
nPass_ggHTT_max2inCross_1L1EG = 0
nPass_ggHTT_max2inCross_2L1EG = 0
nPass_ggHTT_max3inCross_0L1EG = 0
nPass_ggHTT_max3inCross_1L1EG = 0
nPass_ggHTT_max3inCross_2L1EG = 0

nEntries_ggHTT = ggHTT_eventTree.GetEntries()
for i in range(nEntries_ggHTT):
    ggHTT_eventTree.GetEntry(i)

    #if abs(ggHTT_eventTree.genJet_eta) < 1.4 and 30 < ggHTT_eventTree.genJet_pt < 40:
    #if abs(ggHTT_eventTree.genJet_eta) < 1.4 and 40 < ggHTT_eventTree.genJet_pt < 60:
    if abs(ggHTT_eventTree.genJet_eta) < 1.4 and ggHTT_eventTree.genJet_pt > 60:
    #if 1.6 < abs(ggHTT_eventTree.genJet_eta) < 2.6 and 30 < ggHTT_eventTree.genJet_pt < 40:
    #if 1.6 < abs(ggHTT_eventTree.genJet_eta) < 2.6 and 40 < ggHTT_eventTree.genJet_pt < 60:
    #if 1.6 < abs(ggHTT_eventTree.genJet_eta) < 2.6 and ggHTT_eventTree.genJet_pt > 60:
        ggHTT_CrossTowerList = [ggHTT_eventTree.total_seed, ggHTT_eventTree.total_22, ggHTT_eventTree.total_31, ggHTT_eventTree.total_33, ggHTT_eventTree.total_42]
        ggHTT_CrossTowerList.sort(reverse=True)
        ggHTT_sortedTowers = ggHTT_CrossTowerList
        ggHTT_total_max2inCross = ggHTT_sortedTowers[0] + ggHTT_sortedTowers[1]
        ggHTT_total_max3inCross = ggHTT_sortedTowers[0] + ggHTT_sortedTowers[1] + ggHTT_sortedTowers[2]
        if ggHTT_eventTree.total_3x5 >= 0 and ggHTT_eventTree.n_l1eg_HoverE_LessThreshold == 0:
            nEntries_ggHTT_0L1EG += 1
            if ggHTT_total_max2inCross/float(ggHTT_eventTree.total_3x5) > threshold_max2inCross_0L1EG:
                nPass_ggHTT_max2inCross_0L1EG += 1
            if ggHTT_total_max3inCross/float(ggHTT_eventTree.total_3x5) > threshold_max3inCross_0L1EG:
                nPass_ggHTT_max3inCross_0L1EG += 1
        if ggHTT_eventTree.total_3x5 >= 0 and ggHTT_eventTree.n_l1eg_HoverE_LessThreshold == 1:
            nEntries_ggHTT_1L1EG += 1
            if ggHTT_total_max2inCross/float(ggHTT_eventTree.total_3x5) > threshold_max2inCross_1L1EG:
                nPass_ggHTT_max2inCross_1L1EG += 1
            if ggHTT_total_max3inCross/float(ggHTT_eventTree.total_3x5) > threshold_max3inCross_1L1EG:
                nPass_ggHTT_max3inCross_1L1EG += 1
        if ggHTT_eventTree.total_3x5 >= 0 and ggHTT_eventTree.n_l1eg_HoverE_LessThreshold >= 2:
            nEntries_ggHTT_2L1EG += 1
            if ggHTT_total_max2inCross/float(ggHTT_eventTree.total_3x5) > threshold_max2inCross_2L1EG:
                nPass_ggHTT_max2inCross_2L1EG += 1
            if ggHTT_total_max3inCross/float(ggHTT_eventTree.total_3x5) > threshold_max3inCross_2L1EG:
                nPass_ggHTT_max3inCross_2L1EG += 1

#Count entries that pass thresholds and calculate efficiencies for QCD
nEntries_QCD_0L1EG = 0
nEntries_QCD_1L1EG = 0
nEntries_QCD_2L1EG = 0

nPass_QCD_max2inCross_0L1EG = 0
nPass_QCD_max2inCross_1L1EG = 0
nPass_QCD_max2inCross_2L1EG = 0
nPass_QCD_max3inCross_0L1EG = 0
nPass_QCD_max3inCross_1L1EG = 0
nPass_QCD_max3inCross_2L1EG = 0

nEntries_QCD = QCD_eventTree.GetEntries()
for i in range(nEntries_QCD):
    QCD_eventTree.GetEntry(i)

    #if abs(QCD_eventTree.genJet_eta) < 1.4 and 30 < QCD_eventTree.genJet_pt < 40:
    #if abs(QCD_eventTree.genJet_eta) < 1.4 and 40 < QCD_eventTree.genJet_pt < 60:
    if abs(QCD_eventTree.genJet_eta) < 1.4 and QCD_eventTree.genJet_pt > 60:
    #if 1.6 < abs(QCD_eventTree.genJet_eta) < 2.6 and 30 < QCD_eventTree.genJet_pt < 40:
    #if 1.6 < abs(QCD_eventTree.genJet_eta) < 2.6 and 40 < QCD_eventTree.genJet_pt < 60:
    #if 1.6 < abs(QCD_eventTree.genJet_eta) < 2.6 and QCD_eventTree.genJet_pt > 60:
        QCD_CrossTowerList = [QCD_eventTree.total_seed, QCD_eventTree.total_22, QCD_eventTree.total_31, QCD_eventTree.total_33, QCD_eventTree.total_42]
        QCD_CrossTowerList.sort(reverse=True)
        QCD_sortedTowers = QCD_CrossTowerList
        QCD_total_max2inCross = QCD_sortedTowers[0] + QCD_sortedTowers[1]
        QCD_total_max3inCross = QCD_sortedTowers[0] + QCD_sortedTowers[1] + QCD_sortedTowers[2]
        if QCD_eventTree.total_3x5 >= 0 and QCD_eventTree.n_l1eg_HoverE_LessThreshold == 0:
            nEntries_QCD_0L1EG += 1
            if QCD_total_max2inCross/float(QCD_eventTree.total_3x5) > threshold_max2inCross_0L1EG:
                nPass_QCD_max2inCross_0L1EG += 1
            if QCD_total_max3inCross/float(QCD_eventTree.total_3x5) > threshold_max3inCross_0L1EG:
                nPass_QCD_max3inCross_0L1EG += 1
        if QCD_eventTree.total_3x5 >= 0 and QCD_eventTree.n_l1eg_HoverE_LessThreshold == 1:
            nEntries_QCD_1L1EG += 1
            if QCD_total_max2inCross/float(QCD_eventTree.total_3x5) > threshold_max2inCross_1L1EG:
                nPass_QCD_max2inCross_1L1EG += 1
            if QCD_total_max3inCross/float(QCD_eventTree.total_3x5) > threshold_max3inCross_1L1EG:
                nPass_QCD_max3inCross_1L1EG += 1
        if QCD_eventTree.total_3x5 >= 0 and QCD_eventTree.n_l1eg_HoverE_LessThreshold >= 2:
            nEntries_QCD_2L1EG += 1
            if QCD_total_max2inCross/float(QCD_eventTree.total_3x5) > threshold_max2inCross_2L1EG:
                nPass_QCD_max2inCross_2L1EG += 1
            if QCD_total_max3inCross/float(QCD_eventTree.total_3x5) > threshold_max3inCross_2L1EG:
                nPass_QCD_max3inCross_2L1EG += 1

#Define ggHTT efficiencies
eff_ggHTT_max2inCross_0L1EG = nPass_ggHTT_max2inCross_0L1EG/max(float(nEntries_ggHTT_0L1EG),1.0)
eff_ggHTT_max2inCross_1L1EG = nPass_ggHTT_max2inCross_1L1EG/max(float(nEntries_ggHTT_1L1EG),1.0)
eff_ggHTT_max2inCross_2L1EG = nPass_ggHTT_max2inCross_2L1EG/max(float(nEntries_ggHTT_2L1EG),1.0)
eff_ggHTT_max3inCross_0L1EG = nPass_ggHTT_max3inCross_0L1EG/max(float(nEntries_ggHTT_0L1EG),1.0)
eff_ggHTT_max3inCross_1L1EG = nPass_ggHTT_max3inCross_1L1EG/max(float(nEntries_ggHTT_1L1EG),1.0)
eff_ggHTT_max3inCross_2L1EG = nPass_ggHTT_max3inCross_2L1EG/max(float(nEntries_ggHTT_2L1EG),1.0)

eff_ggHTT_max2inCross = (nPass_ggHTT_max2inCross_0L1EG + nPass_ggHTT_max2inCross_1L1EG + nPass_ggHTT_max2inCross_2L1EG)/max(float(nEntries_ggHTT_0L1EG + nEntries_ggHTT_1L1EG + nEntries_ggHTT_2L1EG),1.0)
eff_ggHTT_max3inCross = (nPass_ggHTT_max3inCross_0L1EG + nPass_ggHTT_max3inCross_1L1EG + nPass_ggHTT_max3inCross_2L1EG)/max(float(nEntries_ggHTT_0L1EG + nEntries_ggHTT_1L1EG + nEntries_ggHTT_2L1EG),1.0)

#Define QCD efficiencies
eff_QCD_max2inCross_0L1EG = nPass_QCD_max2inCross_0L1EG/max(float(nEntries_QCD_0L1EG),1.0)
eff_QCD_max2inCross_1L1EG = nPass_QCD_max2inCross_1L1EG/max(float(nEntries_QCD_1L1EG),1.0)
eff_QCD_max2inCross_2L1EG = nPass_QCD_max2inCross_2L1EG/max(float(nEntries_QCD_2L1EG),1.0)
eff_QCD_max3inCross_0L1EG = nPass_QCD_max3inCross_0L1EG/max(float(nEntries_QCD_0L1EG),1.0)
eff_QCD_max3inCross_1L1EG = nPass_QCD_max3inCross_1L1EG/max(float(nEntries_QCD_1L1EG),1.0)
eff_QCD_max3inCross_2L1EG = nPass_QCD_max3inCross_2L1EG/max(float(nEntries_QCD_2L1EG),1.0)
eff_QCD_max2inCross = (nPass_QCD_max2inCross_0L1EG + nPass_QCD_max2inCross_1L1EG + nPass_QCD_max2inCross_2L1EG)/max(float(nEntries_QCD_0L1EG + nEntries_QCD_1L1EG + nEntries_QCD_2L1EG),1.0)
eff_QCD_max3inCross = (nPass_QCD_max3inCross_0L1EG + nPass_QCD_max3inCross_1L1EG + nPass_QCD_max3inCross_2L1EG)/max(float(nEntries_QCD_0L1EG + nEntries_QCD_1L1EG + nEntries_QCD_2L1EG),1.0)

#Print efficiencies
print 'max2inCross:'
print '----------------------------------------------------------------------------------------'
print '0L1EG: ratio of ggHTT events that pass tower fraction > ', threshold_max2inCross_0L1EG, ' = ', eff_ggHTT_max2inCross_0L1EG, '||', 'ratio of QCD events that pass tower fraction > ', threshold_max2inCross_0L1EG, ' = ', eff_QCD_max2inCross_0L1EG
print '1L1EG: ratio of ggHTT events that pass tower fraction > ', threshold_max2inCross_1L1EG, ' = ', eff_ggHTT_max2inCross_1L1EG, '||', 'ratio of QCD events that pass tower fraction > ', threshold_max2inCross_1L1EG, ' = ', eff_QCD_max2inCross_1L1EG
print '2L1EG: ratio of ggHTT events that pass tower fraction > ', threshold_max2inCross_2L1EG, ' = ', eff_ggHTT_max2inCross_2L1EG, '||', 'ratio of QCD events that pass tower fraction > ', threshold_max2inCross_2L1EG, ' = ', eff_QCD_max2inCross_2L1EG
print 'total: ratio of ggHTT events that pass = ', eff_ggHTT_max2inCross, '||', 'ratio of QCD events that pass = ', eff_QCD_max2inCross
print '----------------------------------------------------------------------------------------'
print 'max3inCross:'
print '----------------------------------------------------------------------------------------'
print '0L1EG: ratio of ggHTT events that pass tower fraction > ', threshold_max3inCross_0L1EG, ' = ', eff_ggHTT_max3inCross_0L1EG, '||', 'ratio of QCD events that pass tower fraction > ', threshold_max3inCross_0L1EG, ' = ', eff_QCD_max3inCross_0L1EG
print '1L1EG: ratio of ggHTT events that pass tower fraction > ', threshold_max3inCross_1L1EG, ' = ', eff_ggHTT_max3inCross_1L1EG, '||', 'ratio of QCD events that pass tower fraction > ', threshold_max3inCross_1L1EG, ' = ', eff_QCD_max3inCross_1L1EG
print '2L1EG: ratio of ggHTT events that pass tower fraction > ', threshold_max3inCross_2L1EG, ' = ', eff_ggHTT_max3inCross_2L1EG, '||', 'ratio of QCD events that pass tower fraction > ', threshold_max3inCross_2L1EG, ' = ', eff_QCD_max3inCross_2L1EG
print 'total: ratio of ggHTT events that pass = ', eff_ggHTT_max3inCross, '||', 'ratio of QCD events that pass = ', eff_QCD_max3inCross
