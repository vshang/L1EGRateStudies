This repo provides some analysis tools for the Phase-II L1EG Crystal Algorithm.  You can find the producer here:
```
https://github.com/cms-l1t-offline/cmssw/blob/phase2-l1t-integration-CMSSW_9_0_0_pre6/L1Trigger/L1CaloTrigger/plugins/L1EGammaCrystalsProducer.cc
```

For additional documentation, please see:

https://twiki.cern.ch/twiki/bin/viewauth/CMS/L1TrackTriggerObjects62X

Other instructions here: https://twiki.cern.ch/twiki/bin/view/CMS/L1EGammaCrystals

Checkout instructions:
```bash
cmsrel CMSSW_9_0_0_pre6
cd CMSSW_9_0_0_pre6/src/
cmsenv
git cms-init

git cms-merge-topic truggles:phase2-l1eg-900pre6

pushd L1Trigger/
git clone -b 900_pre6_L1EGCrystals https://github.com/truggles/L1EGRateStudies.git L1EGRateStudies
popd

scramv1 b -j 8
```

There are some auto-generated python file which is created in the "wrong" area and needs to be copied to run this code on Condor.

```
cp $CMSSW_BASE/cfipython/slc6_amd64_gcc530/Geometry/TrackerGeometryBuilder/trackerGeometry_cfi.py $CMSSW_BASE/src/Geometry/TrackerGeometryBuilder/python/
cp $CMSSW_BASE/cfipython/slc6_amd64_gcc530/SimGeneral/TrackingAnalysis/trackingParticleNumberOfLayersProducer_cfi.py $CMSSW_BASE/src/SimGeneral/TrackingAnalysis/python/
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

