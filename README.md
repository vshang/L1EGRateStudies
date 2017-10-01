This repo provides some analysis tools for the Phase-II L1EG Crystal Algorithm.  You can find the producer here:
```
https://github.com/cms-l1t-offline/cmssw/blob/phase2-l1t-integration-CMSSW_9_2_0/L1Trigger/L1CaloTrigger/plugins/L1EGammaCrystalsProducer.cc
```

For additional documentation, please see:

https://twiki.cern.ch/twiki/bin/viewauth/CMS/L1TrackTriggerObjects62X

Other instructions here: https://twiki.cern.ch/twiki/bin/view/CMS/L1EGammaCrystals

Checkout instructions:
There are some auto-generated python file which is created in the "wrong" area and needs to be copied to run this code on Condor.

```bash
cmsrel CMSSW_9_2_0
cd CMSSW_9_2_0/src/
cmsenv
git cms-init
git remote add cms-l1t-offline git@github.com:cms-l1t-offline/cmssw.git
git fetch cms-l1t-offline
git cms-merge-topic -u cms-l1t-offline:phase2-l1t-integration-CMSSW_9_2_0
git clone https://github.com/cms-data/L1Trigger-L1THGCal.git L1Trigger/L1THGCal/data

git remote add trugges git@github.com:truggles/cmssw.git
git fetch truggles
git cms-merge-topic -u truggles:phase2-l1eg-920

pushd L1Trigger/
git clone -b 920_L1EGCrystals git@github.com:truggles/L1EGRateStudies.git L1EGRateStudies
popd

scramv1 b -j 8

```




There are multiple working examples of using the L1EG producer. The current RelVal samples are small and can easily be run over locally.  For code which does that please see the files in `test/`

```
cd SLHCUpgradeSimulations/L1EGRateStudies/test
cmsRun local_eff_hists_cfg.py
```

or
```
cmsRun local_recHit_eff_hists_cfg.py 
```

This branch is under development and will be updated further in the coming weeks.

Updates:
   * Added toggle to switch between running recHits vs. ecal TPs
   * Switched to Nancy's ECAL TPs
   * Had to turn off lots of stuff because of move from GEN-SIM-RECO to GEN-SIM-RAW-DIGI
   * Added HCAL back into analyzer for H/E calc

To Do:
   * Re-add offline Electrons for comparisons
   * Possibly slim down all the output histograms?

