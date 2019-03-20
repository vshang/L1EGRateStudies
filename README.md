This repo provides some analysis tools for the Phase-II L1CaloJet and L1CaloTau algorithms. You can find detailed information on this code
and instructions for using it to recalibrate aspects of the algos in the twiki here:
```
https://twiki.cern.ch/twiki/bin/view/CMS/Phase2L1CaloJetsAndTaus
```

#Checkout

First follow the instructions in the main Phase-2 L1Trigger twiki for setting up the CMSSW_10_5_0_pre1 area:
```
https://twiki.cern.ch/twiki/bin/view/CMSPublic/SWGuideL1TPhase2Instructions#CMSSW_10_5_0_pre1
```

Then checkout this analysis code:
```
pushd L1Trigger
git clone -b 10_5_X_Taus git@github.com:truggles/L1EGRateStudies.git L1EGRateStudies
popd
scram b -j 8
```
