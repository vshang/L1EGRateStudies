This brach is a port of 62X_SLHC L1 EGamma Crylstal Algo to 81X. For additional documentation, please see the below link which targets the 62X_SLHC branch.

https://twiki.cern.ch/twiki/bin/viewauth/CMS/L1TrackTriggerObjects62X

Other instructions here: https://twiki.cern.ch/twiki/bin/view/CMS/L1EGammaCrystals

Checkout instructions:
```bash
cmsrel CMSSW_8_1_0_pre16
cd CMSSW_8_1_0_pre16/src/
cmsenv
git cms-init
git cms-merge-topic nancymarinelli:TP_PhaseII_V0 # For ECAL TPs
git cms-merge-topic truggles:cmssw_810_pre16_stable # you could checkout cmssw_810_pre16_dev for the bleeding edge

pushd SLHCUpgradeSimulations
git clone -b 81X_SLHC_L1EGCrystals_ECAL_TPs_DEV https://github.com/truggles/L1EGRateStudies.git L1EGRateStudies
popd

scramv1 b -j 8
```

There is a single auto-generated python file which is created in the "wrong" area and needs to be copied to run this code on Condor.

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

To Do:
   * Add HCAL back into analyzer for H/E calc, right now I can't figure out HCAL TP or RecHit sequence from DIGI
   * Re-add offline Electrons for comparisons
   * Double check compressedEt for extracting Et value from ECAL TPs in SLHCUpgradeSimulations/L1CaloTrigger/plugins/L1EGammaCrystalsProducer.cc
   * Possibly slim down all the output histograms?

