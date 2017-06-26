#!/bin/bash

# Never forget to build again!
#pushd $CMSSW_BASE/src
#scram b
#popd

jobNum=105
jobopts=''
doeff=false
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
        --input-file-list=SingleElectronFlatPt0p2To50.txt \
        --input-files-per-job=1 $jobopts \
        egalg_eff_hists${jobNum} $CMSSW_BASE eff_hists_cfg.py
    # Single Photo
    if $rmold; then
        rm /nfs_scratch/${USER}/egalgPho_eff* -r
        gsido rm /hdfs/store/user/${USER}/egalgPho_eff* -r
    fi
    farmoutAnalysisJobs \
        --input-file-list=SinglePhotonFlatPt5To75.txt \
        --input-files-per-job=1 $jobopts \
        egalgPho_eff_hists${jobNum} $CMSSW_BASE eff_pho_hists_cfg.py
fi

if $dorate; then
    if $rmold; then
        rm /nfs_scratch/${USER}/egalg_rate* -r
        gsido rm /hdfs/store/user/${USER}/egalg_rate* -r
    fi
    #farmoutAnalysisJobs \
    #    --input-file-list=Neutrino_Pt2to20_gun.txt \
    #    --input-files-per-job=1 $jobopts \
    #    --input-basenames-not-unique \
    #    egalg_rate_hists${jobNum} $CMSSW_BASE rate_hists_cfg.py
    farmoutAnalysisJobs \
        --input-file-list=NeutrinoGun_E2023TTI_PU200.txt \
        --input-files-per-job=2 $jobopts \
        --input-basenames-not-unique \
        egalg_rate_histsPU200${jobNum} $CMSSW_BASE rate_hists_cfg.py
fi
#
#if $dofakes; then
#    if $rmold; then
#        rm /nfs_scratch/${USER}/egalg_fakes* -r
#        gsido rm /hdfs/store/user/${USER}/egalg_fakes* -r
#    fi
#    farmoutAnalysisJobs \
#        --input-file-list=Neutrino_Pt2to20_gun.txt \
#        --input-files-per-job=1 $jobopts \
#        egalg_fakes $CMSSW_BASE fake_heatmap_cfg.py
#fi

