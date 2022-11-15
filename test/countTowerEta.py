from ROOT import *

#Select and load root files here
#f = TFile.Open('/afs/hep.wisc.edu/home/vshang/public/test/CMSSW_11_1_3/src/L1Trigger/L1EGRateStudies/test/crab/l1CaloJets_20210101_r2/output_round2_VBFHiggsTauTau_test.root', '')
f = TFile.Open('/afs/hep.wisc.edu/home/vshang/public/test/CMSSW_11_1_3/src/L1Trigger/L1EGRateStudies/test/crab/l1CaloJets_20210101_r2/output_round2_minBias_test.root', '')

t = f.Get('analyzer/tree')
nEntries = t.GetEntries()

tower_eta_list = []
tower_list = []

for i in range(nEntries):
    t.GetEntry(i)
    tower_eta = t.seed_eta
    tower_iEta = t.seed_iEta
    if (tower_eta not in tower_eta_list) and tower_eta > 0.:
        tower_eta_list.append(tower_eta)
        tower_list.append([tower_iEta, tower_eta])

def takeSecond(elem):
    return elem[1]

tower_eta_list.sort()
tower_list.sort(key=takeSecond)

print 'tower eta list: ', tower_eta_list
print '----------------------------'

for i in range(len(tower_list)):
    print 'tower ieta, eta = ', '(', tower_list[i][0], tower_list[i][1], ')'
    print '-------------------'

