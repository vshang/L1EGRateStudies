#!/bin/bash

DATE=20170501vB1
doElectron=false
doRate=true

#if $doElectron; then
#    farmoutAnalysisJobs \
#        --output-dir=. \
#        --input-files-per-job=20 \
#        --input-file-list=submitFileLists/singleElectronFilesPU200.txt \
#        phaseII_singleElectron_${DATE} $CMSSW_BASE condor_hitAnalyzer.py
#fi

if $doElectron; then
    farmoutAnalysisJobs \
        --output-dir=. \
        --input-files-per-job=20 \
        --input-file-list=submitFileLists/singleElectronFilesPU200_test.txt \
        phaseII_singleElectron_${DATE} $CMSSW_BASE condor_efficiency.py
fi

if $doRate; then
    farmoutAnalysisJobs \
        --output-dir=. \
        --input-files-per-job=10 \
        --input-file-list=submitFileLists/singleNeutrinoFilesPU200_test.txt \
        phaseII_minBias_${DATE} $CMSSW_BASE condor_rate.py
fi

