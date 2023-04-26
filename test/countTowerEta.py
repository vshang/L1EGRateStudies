from ROOT import *

#Select and load root files here
f = TFile.Open('/afs/hep.wisc.edu/home/vshang/public/Phase2L1CaloTaus/CMSSW_12_3_0_pre4/src/L1Trigger/L1EGRateStudies/test/crab/l1CaloJets_r2_CMSSW_12_3_0_pre4/20230206/output_round2_minBias.root','')

t = f.Get('analyzer/tree')
nEntries = t.GetEntries()

tower_eta_list = []
tower_phi_list = []
tower_ieta_list = []
tower_iphi_list = []

for i in range(nEntries):
    t.GetEntry(i)
    tower_eta = t.seed_eta
    tower_iEta = t.seed_iEta
    if (tower_eta not in tower_eta_list) and tower_eta > 0.:
        tower_eta_list.append(tower_eta)
        tower_ieta_list.append([tower_iEta, tower_eta])
    tower_phi = t.seed_phi
    tower_iPhi = t.seed_iPhi
    if (tower_phi not in tower_phi_list) and tower_phi > 0.:
        tower_phi_list.append(tower_phi)
        tower_iphi_list.append([tower_iPhi, tower_phi])

def takeSecond(elem):
    return elem[1]

tower_eta_list.sort()
tower_phi_list.sort()
tower_ieta_list.sort(key=takeSecond)
tower_iphi_list.sort(key=takeSecond)

print('tower eta list: ', tower_eta_list)
print('----------------------------')

for i in range(len(tower_ieta_list)):
    print('tower ieta, eta = ', '(', tower_ieta_list[i][0], tower_ieta_list[i][1], ')')
    print('-------------------')
print('')
print('')
print('tower phi list: ', tower_phi_list)
print('----------------------------')

for i in range(len(tower_iphi_list)):
    print('tower iphi, phi = ', '(', tower_iphi_list[i][0], tower_iphi_list[i][1], ')')
    print('-------------------')
