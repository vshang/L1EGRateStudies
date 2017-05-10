#!/bin/bash

# Never forget to build again!
#pushd $CMSSW_BASE/src
#scram b
#popd

jobNum=26
jobopts=''
doeff=true
dorate=true
dofakes=false
rmold=false
while getopts ":trefj:" opt; do
  case $opt in
    j)
      jobopts="$jobopts --job-count=$OPTARG"
      ;;
    t)
      jobopts="$jobopts --resubmit-failed-jobs"
      rmold=false
      ;;
    r)
      doeff=false
      ;;
    e)
      dorate=false
      ;;
    f)
      dofakes=true
      doeff=false
      dorate=false
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

if $doeff; then
    # Single Electrong
    if $rmold; then
        rm /nfs_scratch/${USER}/egalg_eff* -r
        gsido rm /hdfs/store/user/${USER}/egalg_eff* -r
    fi
    farmoutAnalysisJobs \
        --input-dir=/store/mc/TTI2023Upg14D/SingleElectronFlatPt0p2To50/GEN-SIM-DIGI-RAW/PU140bx25_PH2_1K_FB_V3-v2/00000 \
        --input-files-per-job=1 $jobopts \
        egalg_eff_hists${jobNum} $CMSSW_BASE eff_hists_cfg.py
    # Single Photo
    if $rmold; then
        rm /nfs_scratch/${USER}/egalgPho_eff* -r
        gsido rm /hdfs/store/user/${USER}/egalgPho_eff* -r
    fi
    farmoutAnalysisJobs \
        --input-dir=/store/mc/TTI2023Upg14D/SinglePhotonFlatPt5To75/GEN-SIM-DIGI-RAW/PU140bx25_PH2_1K_FB_V3-v2/00000 \
        --input-files-per-job=1 $jobopts \
        egalgPho_eff_hists${jobNum} $CMSSW_BASE eff_hists_cfg.py
fi

if $dorate; then
    if $rmold; then
        rm /nfs_scratch/${USER}/egalg_rate* -r
        gsido rm /hdfs/store/user/${USER}/egalg_rate* -r
    fi
    farmoutAnalysisJobs \
        --input-dir=/store/mc/TTI2023Upg14D/Neutrino_Pt2to20_gun/GEN-SIM-DIGI-RAW/PU140bx25_PH2_1K_FB_V3-v2/00000 \
        --input-files-per-job=1 $jobopts \
        egalg_rate_hists${jobNum} $CMSSW_BASE rate_hists_cfg.py
fi

if $dofakes; then
    if $rmold; then
        rm /nfs_scratch/${USER}/egalg_fakes* -r
        gsido rm /hdfs/store/user/${USER}/egalg_fakes* -r
    fi
    farmoutAnalysisJobs \
        --input-dir=/store/mc/TTI2023Upg14D/Neutrino_Pt2to20_gun/GEN-SIM-DIGI-RAW/PU140bx25_PH2_1K_FB_V3-v2/00000 \
        --input-files-per-job=1 $jobopts \
        egalg_fakes $CMSSW_BASE fake_heatmap_cfg.py
fi

