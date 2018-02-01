#!/bin/bash

DATE=20170721NormalV1
DATE=20170819NormalV1


# Signals for Efficiencies and Std Algo Studies
doMinBias=true
doElectron=true
doPhoton=true
doPiZero=true
doPion=true
doTau=true
doHZZ=true
doTTbar=true

doMinBias=false
#doElectron=false
doPhoton=false
doPiZero=false
doPion=false
doTau=false
doHZZ=false
doTTbar=false

resubmitFailedJobs=true
resubmitFailedJobs=false

DATE=20180120minEt375MeVv1

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
        --input-files-per-job=10 \
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

if $doHZZ; then
    farmoutAnalysisJobs \
        --output-dir=. \
        --input-files-per-job=30 \
        --input-file-list=submitFileLists/GluGluHToZZTo4LPU200.txt \
        phaseII_HZZ4l_${DATE} $CMSSW_BASE round1_condor_cfg.py
fi

if $doTTbar; then
    farmoutAnalysisJobs \
        --output-dir=. \
        --input-files-per-job=30 \
        --input-file-list=submitFileLists/TTbarPU200.txt \
        phaseII_TTbar_${DATE} $CMSSW_BASE round1_condor_cfg.py
fi

# probably need to redefine the DATE group here for future use!
if $resubmitFailedJobs; then
    #for DATE in 20170612v1 20170716top20 20170716top10 20170716top05; do
    if $doMinBias; then
        farmoutAnalysisJobs \
            --output-dir=. \
            --input-files-per-job=50 \
            --input-file-list=submitFileLists/singleNeutrinoFilesPU200.txt \
            --resubmit-failed-jobs \
            phaseII_minBias_${DATE} $CMSSW_BASE round1_condor_cfg.py
    fi
    
    if $doElectron; then
        farmoutAnalysisJobs \
            --output-dir=. \
            --input-files-per-job=10 \
            --input-file-list=submitFileLists/singleElectronFilesPU200.txt \
            --resubmit-failed-jobs \
            phaseII_singleElectron_${DATE} $CMSSW_BASE round1_condor_cfg.py
    fi

    if $doPhoton; then
        farmoutAnalysisJobs \
            --output-dir=. \
            --input-files-per-job=30 \
            --input-file-list=submitFileLists/singlePhotonFilesPU200.txt \
            --resubmit-failed-jobs \
            phaseII_singlePhoton_${DATE} $CMSSW_BASE round1_condor_cfg.py
    fi
    #done
fi
