This brach is a port of 62X_SLHC L1 EGamma Crylstal Algo to 81X. For additional documentation, please see the below link which targets the 62X_SLHC branch.

https://twiki.cern.ch/twiki/bin/viewauth/CMS/L1TrackTriggerObjects62X

Checkout instructions:
```bash
cmsrel CMSSW_8_1_0_pre16
cd CMSSW_8_1_0_pre16/src/
cmsenv
git cms-init
git cms-merge-topic nancymarinelli:TP_PhaseII_V0 # For ECAL TPs
git cms-merge-topic truggles:cmssw_810_pre16_dev

pushd SLHCUpgradeSimulations
git clone -b 81X_SLHC_L1EGCrystals_DEV https://github.com/truggles/L1EGRateStudies.git L1EGRateStudies
popd

scramv1 b -j 8
```

At the momoent, there is a single working example which produces the L1EG Crystal objects and compares them with generator electrons and reco electrons. Find this code in `test/`

```
cd SLHCUpgradeSimulations/L1EGRateStudies/test
cmsRun local_eff_hists_cfg.py
```

This branch is under development and will be updated further in the coming weeks.

Updates:
   * Switched to Nancy's ECAL TPs
   * Had to turn off lots of stuff because of move from GEN-SIM-RECO to GEN-SIM-RAW-DIGI

To Do:
   * Add HCAL back into analyzer for H/E calc, right now I can't figure out HCAL TP or RecHit sequence from DIGI
   * Re-add offline Electrons for comparisons
   * Double check compressedEt for extracting Et value from ECAL TPs in SLHCUpgradeSimulations/L1CaloTrigger/plugins/L1EGammaCrystalsProducer.cc
   * Possibly slim down all the output histograms?

