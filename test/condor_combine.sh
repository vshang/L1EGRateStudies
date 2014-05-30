#!/bin/bash
rm egTriggerEff.root
find /hdfs/store/user/nsmith/egalg_eff_hists-eff_hists_cfg/* |xargs hadd egTriggerEff.root

rm egTriggerRates.root
find /hdfs/store/user/nsmith/egalg_rate_hists-rate_hists_cfg/* |xargs hadd egTriggerRates.root

root -q -b normalizeParallelJobs.C+
