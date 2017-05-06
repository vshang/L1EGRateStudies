#!/bin/bash

DATE=20170503v1

# Different options
doHitAnalyzer=true
doRates=true
doEfficiencies=true


# Signals for Efficiencies and Std Algo Studies
doElectron=true
#doPhoton=true
#doPiZero=true
#doPion=true
#doTau=true

# Hit Analyzer
if $doHitAnalyzer; then
    farmoutAnalysisJobs \
        --output-dir=. \
        --input-files-per-job=30 \
        --input-file-list=submitFileLists/singleElectronFilesPU200.txt \
        phaseII_singleElectron_${DATE} $CMSSW_BASE condor_hitAnalyzer.py
fi

# Rates
if $doRates; then
    farmoutAnalysisJobs \
        --output-dir=. \
        --input-files-per-job=50 \
        --input-file-list=submitFileLists/singleNeutrinoFilesPU200.txt \
        phaseII_minBias_${DATE} $CMSSW_BASE condor_rate.py
fi

# Efficiencies
if $doEfficiencies; then

    if $doElectron; then
        farmoutAnalysisJobs \
            --output-dir=. \
            --input-files-per-job=30 \
            --input-file-list=submitFileLists/singleElectronFilesPU200.txt \
            phaseII_singleElectron_${DATE} $CMSSW_BASE condor_efficiency.py
    fi

    if $doPhoton; then
        farmoutAnalysisJobs \
            --output-dir=. \
            --input-files-per-job=30 \
            --input-file-list=submitFileLists/singlePhotonFilesPU200.txt \
            phaseII_singlePhoton_${DATE} $CMSSW_BASE condor_efficiency.py
    fi

    if $doPiZero; then
        farmoutAnalysisJobs \
            --output-dir=. \
            --input-files-per-job=30 \
            --input-file-list=submitFileLists/singlePiZeroFilesPU200.txt \
            phaseII_singlePiZero_${DATE} $CMSSW_BASE condor_efficiency.py
    fi

    if $doPion; then
        farmoutAnalysisJobs \
            --output-dir=. \
            --input-files-per-job=30 \
            --input-file-list=submitFileLists/singlePionFilesPU200.txt \
            phaseII_singlePion_${DATE} $CMSSW_BASE condor_efficiency.py
    fi

    if $doTau; then
        farmoutAnalysisJobs \
            --output-dir=. \
            --input-files-per-job=30 \
            --input-file-list=submitFileLists/singleTauFilesPU200.txt \
            phaseII_singleTau_${DATE} $CMSSW_BASE condor_efficiency.py
    fi
fi








