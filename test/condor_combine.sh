#!/bin/bash
if [ -d /hdfs/store/user/nsmith/egalg_eff_hists-eff_hists_cfg/ ]; then
    rm egTriggerEff.root
    find /hdfs/store/user/nsmith/egalg_eff_hists-eff_hists_cfg/* |xargs hadd egTriggerEff.root
fi

if [ -d /hdfs/store/user/nsmith/egalg_rate_hists-rate_hists_cfg/ ]; then
    rm egTriggerRates.root
    find /hdfs/store/user/nsmith/egalg_rate_hists-rate_hists_cfg/* |xargs hadd egTriggerRates.root
fi

root -q -b normalizeParallelJobs.C+
