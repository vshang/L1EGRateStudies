For using this with `L1TrackTriggerObjects62X`, one can in principle follow this:

https://twiki.cern.ch/twiki/bin/viewauth/CMS/L1TrackTriggerObjects62X#Recipe_in_6_2_0_SLHC12

Preferably, one should do this:
```bash

cmsrel CMSSW_6_2_0_SLHC12_patch1
cd CMSSW_6_2_0_SLHC12_patch1/src
cmsenv
git cms-init
git cms-addpkg SLHCUpgradeSimulations/L1TrackTrigger
git cms-merge-topic EmanuelPerez:TTI_62X_TrackTriggerObjects
git clone https://github.com/uwcms/UCT2015.git L1Trigger/UCT2015

scramv1 b -j 8

```
Then, assuming all is well in your enviroment, you will need to copy some auto-generated python files and checkout this repository.  These auto-generated python files need to be included in the user code which is sent with farmed out jobs (Specific to HT Condor/UWisconsin).  The auto-generated files are found by CMSSW sucessfully when you run jobs locally.

```bash
cp ../cfipython/slc6_amd64_gcc472/Geometry/TrackerGeometryBuilder/tracker*.py Geometry/TrackerGeometryBuilder/python/ 

pushd SLHCUpgradeSimulations
git clone https://github.com/truggles/L1EGRateStudies.git
popd

scramv1 b -j 8
```

Some example run configurations are in `test/`

```
cd SLHCUpgradeSimulations/L1EGRateStudies/test
cmsRun local_eff_hists_cfg.py
cmsRun local_rate_hists_cfg.py
```

Submit jobs (UW Specific) using UW HTP Condor
```
. condor_submit.sh
```
You will need to merge the files and do some additional histogram production
```
. condor_combine.sh
```
With the merged root files, there are a variety of plotting tools (they will likely ask you to make the directory structure to hold the png files)
```
python drawRateEff.py
python optimizer.py
python plotCutThresholds.py
```



