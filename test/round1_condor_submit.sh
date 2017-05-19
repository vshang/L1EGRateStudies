#!/bin/bash

DATE=20170518v3

# Different options


# Signals for Efficiencies and Std Algo Studies
doMinBias=true
doElectron=true
doPhoton=true
doPiZero=true
doPion=true
doTau=true
#doMinBias=false
#doElectron=false
#doPhoton=false
#doPiZero=false
doPion=false
doTau=false

if $doMinBias; then
    farmoutAnalysisJobs \
        --output-dir=. \
        --input-files-per-job=50 \
        --input-file-list=submitFileLists/singleNeutrinoFilesPU200.txt \
        phaseII_minBias_${DATE} $CMSSW_BASE round1_condor_cfg.py
fi

if $doElectron; then
    farmoutAnalysisJobs \
        --output-dir=. \
        --input-files-per-job=30 \
        --input-file-list=submitFileLists/singleElectronFilesPU200.txt \
        phaseII_singleElectron_${DATE} $CMSSW_BASE round1_condor_cfg.py
fi

if $doPhoton; then
    farmoutAnalysisJobs \
        --output-dir=. \
        --input-files-per-job=30 \
        --input-file-list=submitFileLists/singlePhotonFilesPU200.txt \
        phaseII_singlePhoton_${DATE} $CMSSW_BASE round1_condor_cfg.py
fi

if $doPiZero; then
    farmoutAnalysisJobs \
        --output-dir=. \
        --input-files-per-job=30 \
        --input-file-list=submitFileLists/singlePiZeroFilesPU200.txt \
        phaseII_singlePiZero_${DATE} $CMSSW_BASE round1_condor_cfg.py
fi

if $doPion; then
    farmoutAnalysisJobs \
        --output-dir=. \
        --input-files-per-job=30 \
        --input-file-list=submitFileLists/singlePionFilesPU200.txt \
        phaseII_singlePion_${DATE} $CMSSW_BASE round1_condor_cfg.py
fi

if $doTau; then
    farmoutAnalysisJobs \
        --output-dir=. \
        --input-files-per-job=30 \
        --input-file-list=submitFileLists/singleTauFilesPU200.txt \
        phaseII_singleTau_${DATE} $CMSSW_BASE round1_condor_cfg.py
fi


