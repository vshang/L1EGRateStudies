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
cmsrel CMSSW_10_1_0_pre3
cd CMSSW_10_1_0_pre3/src
cmsenv
git cms-init
git remote add cms-l1t-offline git@github.com:cms-l1t-offline/cmssw.git
git fetch cms-l1t-offline phase2-l1t-integration-CMSSW_10_1_0_pre3
git cms-merge-topic -u cms-l1t-offline:l1t-phase2-v2.13
#
# Tracklet Tracks
#
git remote add rekovic git@github.com:rekovic/cmssw.git
git fetch rekovic Tracklet-10_1_0_pre3
git cms-merge-topic -u rekovic:Tracklet-10_1_0_pre3-from-skinnari

git cms-addpkg L1Trigger/L1TCommon

git remote add truggles git@github.com:truggles/cmssw.git
git fetch truggles
# Because this PR hasn't been merged yet
# https://github.com/cms-l1t-offline/cmssw/pull/689
git cherry-pick 4a5aeaf2b0429ec8f4df81b4facf7b07fef4f4b1^..5a67ea9f64676b1600dc76549edb7f043eecf735

pushd L1Trigger/
git clone -b 10_1_0_pre3_L1EGCrystals git@github.com:truggles/L1EGRateStudies.git L1EGRateStudies
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

