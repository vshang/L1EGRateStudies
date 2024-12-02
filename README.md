Victor's copy of Tyler's code.

This repo provides some analysis tools for the Phase-II L1T GCTJet and GCTTau algorithms. You can find detailed information on this code
and instructions for using it to recalibrate aspects of the algos in the twiki here:
```
https://twiki.cern.ch/twiki/bin/view/CMS/Phase2L1GCTJetsAndTaus
```

#Checkout

First follow the instructions in the main Phase-2 L1Trigger twiki for setting up the CMSSW_14_0_0_pre3 area:
```
https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideL1TPhase2Instructions#CMSSW_14_0_0_pre3
```

Then checkout this analysis code:
```
pushd L1Trigger
git clone -b master git@github.com:vshang/L1EGRateStudies.git L1EGRateStudies
popd
scram b -j 8
```
