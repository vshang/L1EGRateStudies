#!/bin/bash
farmoutAnalysisJobs \
   --input-dir=/store/user/ncsmith/L1TrackTriggerMC/ \
   --input-files-per-job=1 \
   --job-count=2 \
   egalg_eff_hists $CMSSW_BASE eff_hists_cfg.py

farmoutAnalysisJobs \
   --input-dir=root://eoscms.cern.ch/ \
   --input-file-list=NeutrinoGunFiles.txt \
   --assume-input-files-exist \
   --input-files-per-job=10 \
   --job-count=10 \
   egalg_rate_hists $CMSSW_BASE rate_hists_cfg.py
