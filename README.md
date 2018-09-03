This repo provides some analysis tools for the Phase-II L1EG Crystal Algorithm.  You can find the producer here:
```
https://github.com/cms-l1t-offline/cmssw/blob/phase2-l1t-integration-CMSSW_10_0_0/L1Trigger/L1CaloTrigger/plugins/L1EGammaCrystalsProducer.cc
```

For additional documentation, please see:

https://twiki.cern.ch/twiki/bin/viewauth/CMS/L1TrackTriggerObjects62X

Other instructions here: https://twiki.cern.ch/twiki/bin/view/CMS/L1EGammaCrystals

Checkout instructions:
There are some auto-generated python file which is created in the "wrong" area and needs to be copied to run this code on Condor.

```bash
cmsrel CMSSW_10_1_7
cd CMSSW_10_1_7/src
cmsenv
git cms-init
git remote add cms-l1t-offline git@github.com:cms-l1t-offline/cmssw.git
git fetch cms-l1t-offline phase2-l1t-integration-CMSSW_10_1_7
git cms-merge-topic -u cms-l1t-offline:l1t-phase2-v2.16.13

git cms-addpkg L1Trigger/L1TCommon

pushd L1Trigger/
git clone -b 10_1_7_L1EGCrystals git@github.com:truggles/L1EGRateStudies.git L1EGRateStudies
popd

scramv1 b -j 8

```

Phase-II studies checkout info and links to RelVal samples:
```
https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideL1TPhase2Instructions#Phase_2_L1T_Development_and_MC_R
```


There are multiple working examples of using the L1EG producer. The current RelVal samples are small and can easily be run over locally.  For code which does that please see the files in `test/`

```
cd L1Trigger/L1EGRateStudies/test/
cmsRun local_eff_hists_cfg.py
```

or
```
cmsRun local_recHit_eff_hists_cfg.py 
```


# Some notes for L1CaloJets

/QCD_Pt-0to1000_Tune4C_14TeV_pythia8/PhaseIIFall17D-L1TPU200_93X_upgrade2023_realistic_v5-v1/GEN-SIM-DIGI-RAW
/QCD_Pt-0to1000_Tune4C_14TeV_pythia8/PhaseIIFall17D-L1TnoPU_93X_upgrade2023_realistic_v5-v1/GEN-SIM-DIGI-RAW

/GluGluHToTauTau_M125_14TeV_powheg_pythia8/PhaseIIFall17D-L1TnoPU_93X_upgrade2023_realistic_v5-v1/GEN-SIM-DIGI-RAW
/store/mc/PhaseIIFall17D/GluGluHToTauTau_M125_14TeV_powheg_pythia8/GEN-SIM-DIGI-RAW/L1TnoPU_93X_upgrade2023_realistic_v5-v1/00000/00C160E6-6A39-E811-B904-008CFA152144.root

/QCD_Pt-0to1000_Tune4C_14TeV_pythia8/PhaseIIFall17D-L1TnoPU_93X_upgrade2023_realistic_v5-v1/GEN-SIM-DIGI-RAW
/store/mc/PhaseIIFall17D/QCD_Pt-0to1000_Tune4C_14TeV_pythia8/GEN-SIM-DIGI-RAW/L1TnoPU_93X_upgrade2023_realistic_v5-v1/00000/02AE7A07-2339-E811-B98B-E0071B7AC750.root

/WJetsToLNu_TuneCUETP8M1_14TeV-madgraphMLM-pythia8/PhaseIIFall17D-L1TnoPU_93X_upgrade2023_realistic_v5-v3/GEN-SIM-DIGI-RAW
/store/mc/PhaseIIFall17D/WJetsToLNu_TuneCUETP8M1_14TeV-madgraphMLM-pythia8/GEN-SIM-DIGI-RAW/L1TnoPU_93X_upgrade2023_realistic_v5-v3/30000/162DC63A-C458-E811-92E1-B083FED42FAF.root

