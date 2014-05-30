#!/bin/bash

jobcount=''
while getopts ":j:" opt; do
  case $opt in
    j)
      jobcount="--job-count=$OPTARG"
      ;;
    \?)
      echo "Invalid option: -$OPTARG" >&2
      exit 1
      ;;
    :)
      echo "Option -$OPTARG requires an argument." >&2
      exit 1
      ;;
  esac
done

# remove old stuff
rm /nfs_scratch/nsmith/egalg_* -r
gsido rm /hdfs/store/user/nsmith/egalg_* -r

farmoutAnalysisJobs \
  --input-dir=/store/mc/TTI2023Upg14D/Neutrino_Pt2to20_gun/GEN-SIM-DIGI-RAW/PU140bx25_PH2_1K_FB_V3-v2/00000 \
  --input-files-per-job=1 $jobcount \
  egalg_eff_hists $CMSSW_BASE eff_hists_cfg.py

farmoutAnalysisJobs \
  --input-dir=/store/mc/TTI2023Upg14D/SingleElectronFlatPt0p2To50/GEN-SIM-DIGI-RAW/PU140bx25_PH2_1K_FB_V3-v2/00000 \
  --input-files-per-job=1 $jobcount \
  egalg_rate_hists $CMSSW_BASE rate_hists_cfg.py
