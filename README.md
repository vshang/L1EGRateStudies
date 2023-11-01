Victor's copy of Tyler's code.

This repo provides some analysis tools for the Phase-II L1CaloJet and L1CaloTau algorithms. You can find detailed information on this code
and instructions for using it to recalibrate aspects of the algos in the twiki here:
```
https://twiki.cern.ch/twiki/bin/view/CMS/Phase2L1CaloJetsAndTaus
```

#Checkout

First follow the instructions in the main Phase-2 L1Trigger twiki for setting up the CMSSW_13_3_0_pre3 area:
```
https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideL1TPhase2Instructions#CMSSW_13_3_0_pre3
```

Then checkout this analysis code:
```
pushd L1Trigger
git clone -b master git@github.com:vshang/L1EGRateStudies.git L1EGRateStudies
popd
scram b -j 8
```
