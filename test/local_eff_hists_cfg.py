import FWCore.ParameterSet.Config as cms

process = cms.Process("L1AlgoAnalysis")

process.load('Configuration.StandardSequences.Services_cff')
process.load("FWCore.MessageService.MessageLogger_cfi")
process.load('Configuration.EventContent.EventContent_cff')
process.MessageLogger.categories = cms.untracked.vstring('L1EGRateStudies', 'FwkReport')
process.MessageLogger.cerr.FwkReport = cms.untracked.PSet(
   reportEvery = cms.untracked.int32(1)
)

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        #'file:root://cms-xrd-global.cern.ch//store/mc/PhaseIISpring17D/SingleE_FlatPt-8to100/GEN-SIM-DIGI-RAW/PU200_90X_upgrade2023_realistic_v9-v1/120000/002A4121-132C-E711-87AD-008CFAFBF618.root',
        'file:root://cms-xrd-global.cern.ch//store/mc/PhaseIITDRFall17DR/GJet_Pt-40toInf_DoubleEMEnriched_MGG-80toInf_TuneCUETP8M1_14TeV_Pythia8/GEN-SIM-RECO/PU200_93X_upgrade2023_realistic_v2-v1/00002/16DB8E1E-42B8-E711-B1DC-0CC47A4C8E38.root',
    )
)

# All this stuff just runs the various EG algorithms that we are studying
                         
# ---- Global Tag :
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '90X_upgrade2023_realistic_v9', '')

# Choose a 2030 geometry!
# The ones which don't work all replace the ECAL Endcap geometry with HGCal stuff
# Options in cmssw_810_pre16: (each also has an option without the Reco)
process.load('Configuration.Geometry.GeometryExtended2023D17Reco_cff') # D7 works, D4 is the choosen config by Phase-2 L1Trig
#process.load('Configuration.StandardSequences.MagneticField_38T_PostLS1_cff')


## --------------------------------------------------------------------------------------------
##
## ----     L1 tracking
#
#process.load("L1Trigger.TrackFindingTracklet.L1TrackletTracks_cff")
#process.TTTracks = cms.Path(process.L1TrackletTracks)  #run only the tracking (no MC truth associators)
#
## ----     L1 tracking Primary Vertex
#process.load("L1Trigger.L1TTrackMatch.L1TkPrimaryVertexProducer_cfi")
#process.TTTrackPV = cms.Path(process.L1TkPrimaryVertex)
#
#
## --------------------------------------------------------------------------------------------
##
## ----    Produce the L1EGCrystal clusters (code of Sasha Savin)

process.L1EGammaCrystalsProducer = cms.EDProducer("L1EGCrystalClusterProducer",
   EtminForStore = cms.double(0.),
   #EtMinForSeedHit = cms.untracked.double(5.),
   EcalTpEtMin = cms.untracked.double(0.0001),
   debug = cms.untracked.bool(False),
   #debug = cms.untracked.bool(True),
   useRecHits = cms.bool(True),
   #ecalTPEB = cms.InputTag("EcalEBTrigPrimProducer","","L1AlgoTest"),
   ecalTPEB = cms.InputTag("simEcalEBTriggerPrimitiveDigis","","HLT"),
   ecalRecHitEB = cms.InputTag("ecalRecHit","EcalRecHitsEB","RECO"),
   #hcalRecHit = cms.InputTag("hbhereco") # for testing non-2023 geometry configurations
   #hcalRecHit = cms.InputTag("hltHbhereco","","L1AlgoTest")
   #hcalRecHit = cms.InputTag("hltHbhereco")
   hcalRecHit = cms.InputTag("hbhereco"),
   #hcalRecHit = cms.InputTag("hbheUpgradeReco")
   hcalTP = cms.InputTag("simHcalTriggerPrimitiveDigis","","HLT"),

   useTowerMap = cms.untracked.bool(False)
   #useTowerMap = cms.untracked.bool(True),
   #towerMapName = cms.untracked.string("map170x15.json")
   #towerMapName = cms.untracked.string("map85x30.json")
)

process.pSasha = cms.Path( process.L1EGammaCrystalsProducer )



# -------------------------------------------------------------------------------------------
#
### Mini-analyzer for L1EG TPs
process.TPAnalyzer = cms.EDAnalyzer('L1EGPreclusterAnalysis',
   L1CrystalClustersInputTag = cms.InputTag("L1EGammaCrystalsProducer","L1EGXtalClusterNoCuts"),
   L1CrystalClustersWithCutsInputTag = cms.InputTag("L1EGammaCrystalsProducer","L1EGXtalClusterWithCuts")
)

# ----------------------------------------------------------------------------------------------
# 
# Analyzer starts here

process.analyzer = cms.EDAnalyzer('L1EGRateStudies',
   L1CrystalClustersInputTag = cms.InputTag("L1EGammaCrystalsProducer","L1EGXtalClusterNoCuts","L1AlgoAnalysis"),
   genParticles = cms.InputTag("genParticles","","HLT"),
   L1TrackInputTag = cms.InputTag("TTTracksFromTracklet", "Level1TTTracks"),
   L1TrackPrimaryVertexTag = cms.InputTag("L1TkPrimaryVertex"),
   Stage2EG1Tag = cms.InputTag("simCaloStage2Digis", "", "HLT"),
   OfflineRecoClustersInputTag = cms.InputTag("correctedHybridSuperClusters"),
   ecalTPEB = cms.InputTag("simEcalEBTriggerPrimitiveDigis","","HLT"),
   doEfficiencyCalc = cms.untracked.bool(True),
   useOfflineClusters = cms.untracked.bool(False),
   useEndcap = cms.untracked.bool(False),
   doTracking = cms.untracked.bool(False),
   isPhoton = cms.untracked.bool(True),
   turnOnThresholds = cms.untracked.vint32(20, 30, 16),
   histogramBinCount = cms.untracked.int32(60),
   histogramRangeLow = cms.untracked.double(0),
   histogramRangeHigh = cms.untracked.double(50),
   histogramEtaBinCount = cms.untracked.int32(20),
   genMatchDeltaRcut = cms.untracked.double(0.25),
   genMatchRelPtcut = cms.untracked.double(0.5),
   debug = cms.untracked.bool(False)
   #debug = cms.untracked.bool(True)
)

process.panalyzer = cms.Path(process.TPAnalyzer+process.analyzer)

process.TFileService = cms.Service("TFileService", 
   fileName = cms.string("nick_effTest_ecalTPs_v3.root"), 
   closeFileFast = cms.untracked.bool(True)
)

#dump_file = open("dump_file.py", "w")
#dump_file.write(process.dumpPython())


