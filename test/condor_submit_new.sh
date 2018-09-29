#!/bin/bash

DATE=20180927_circT_v1
#DATE=20180927_circL_v2
#DATE=20180927_9x9_v1
#DATE=20180927_7x7_v1

# Different options
doHitAnalyzer=true
doHitAnalyzer=false
doRates=true
doRates=false
doEfficiencies=true
doEfficiencies=false
doJets=true
#doJets=false


# Signals for Efficiencies and Std Algo Studies
doElectron=true
doPhoton=true
doPiZero=true
doPion=true
doTau=true
doElectron=false
doPhoton=false
doPiZero=false
doPion=false
doTau=false

#        --resubmit-failed-jobs \
# Jet/Tau Analyzer
if $doJets; then
    farmoutAnalysisJobs \
        --output-dir=. \
        --input-files-per-job=2 \
        --vsize-limit=6000 \
        --input-file-list=submitFileLists/qcd_93X_pu0.txt \
        phaseII_qcd_${DATE} $CMSSW_BASE condor_jets.py
    farmoutAnalysisJobs \
        --output-dir=. \
        --input-files-per-job=5 \
        --vsize-limit=6000 \
        --input-file-list=submitFileLists/qcd_93X_pu200.txt \
        phaseII_qcd200_${DATE} $CMSSW_BASE condor_jets.py
    #farmoutAnalysisJobs \
    #    --output-dir=. \
    #    --input-files-per-job=1 \
    #    --vsize-limit=6000 \
    #    --input-file-list=submitFileLists/ggH_HtoTauTau_93X_pu0.txt \
    #    phaseII_ggH_HTT_${DATE} $CMSSW_BASE condor_jets.py
fi

# Hit Analyzer
if $doHitAnalyzer; then
    farmoutAnalysisJobs \
        --output-dir=. \
        --input-files-per-job=30 \
        --input-file-list=submitFileLists/singleElectronFilesPU200.txt \
        phaseII_singleElectron_${DATE} $CMSSW_BASE condor_hitAnalyzer.py
    farmoutAnalysisJobs \
        --output-dir=. \
        --input-files-per-job=30 \
        --input-file-list=submitFileLists/TTbarPU200.txt \
        phaseII_TTbar_${DATE} $CMSSW_BASE condor_hitAnalyzer.py
    farmoutAnalysisJobs \
        --output-dir=. \
        --input-files-per-job=30 \
        --input-file-list=submitFileLists/singleNeutrinoFilesPU200.txt \
        phaseII_minBias_${DATE} $CMSSW_BASE condor_hitAnalyzer_noGen.py
fi

# Rates
if $doRates; then
    farmoutAnalysisJobs \
        --output-dir=. \
        --input-files-per-job=50 \
        --input-file-list=submitFileLists/singleNeutrino_pu200.txt \
        phaseII_minBias_${DATE} $CMSSW_BASE condor_rate.py
fi

# Efficiencies
if $doEfficiencies; then

    if $doElectron; then
        farmoutAnalysisJobs \
            --output-dir=. \
            --input-files-per-job=5 \
            --input-file-list=submitFileLists/singleE_93X_pu200.txt \
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
            --input-files-per-job=5 \
            --input-file-list=submitFileLists/singlePion_93X_pu200.txt \
            phaseII_singlePion_${DATE} $CMSSW_BASE condor_efficiency.py

        farmoutAnalysisJobs \
            --output-dir=. \
            --input-files-per-job=5 \
            --input-file-list=submitFileLists/singlePion_93X_pu0.txt \
            phaseII_singlePion_noPU_${DATE} $CMSSW_BASE condor_efficiency.py
    fi

    if $doTau; then
        farmoutAnalysisJobs \
            --output-dir=. \
            --input-files-per-job=30 \
            --input-file-list=submitFileLists/singleTauFilesPU200.txt \
            phaseII_singleTau_${DATE} $CMSSW_BASE condor_efficiency.py
    fi
fi








