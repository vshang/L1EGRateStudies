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


