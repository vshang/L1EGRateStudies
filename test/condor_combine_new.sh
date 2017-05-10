
DATE=20170508v3

# Different options
doHitAnalyzer=true
doRates=true
doEfficiencies=true


# Signals for Efficiencies and Std Algo Studies
doElectron=true
doPhoton=true
doPiZero=true
doPion=true
doTau=true

mkdir -p ${DATE}

if $doEfficiencies; then
    for NAME in Electron Photon PiZero Pion Tau; do
        hadd ${DATE}/${DATE}_single${NAME}_eff.root /data/truggles/phaseII_single${NAME}_${DATE}-condor_efficiency/*/*.root
    done
fi

if $doRates; then
    hadd ${DATE}/${DATE}_minBias_rate.root /data/truggles/phaseII_minBias_${DATE}-condor_rate/*/*.root
fi
if $doHitAnalyzer; then
    hadd ${DATE}/${DATE}_singleElectron_hitAnalyzer.root /data/truggles/phaseII_singleElectron_${DATE}-condor_hitAnalyzer/*/*.root
fi



