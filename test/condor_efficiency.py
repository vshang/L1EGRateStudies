import FWCore.ParameterSet.Config as cms

process = cms.Process("L1AlgoTest")

process.load('Configuration.StandardSequences.Services_cff')
process.load("FWCore.MessageService.MessageLogger_cfi")
process.load('Configuration.EventContent.EventContent_cff')
process.MessageLogger.categories = cms.untracked.vstring('L1EGRateStudies', 'FwkReport')
process.MessageLogger.cerr.FwkReport = cms.untracked.PSet(
   reportEvery = cms.untracked.int32(100)
)

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )

process.source = cms.Source("PoolSource",
   fileNames = cms.untracked.vstring($inputFileNames),
   inputCommands = cms.untracked.vstring(
                    "keep *",
                    "drop l1tEMTFHitExtras_simEmtfDigis_CSC_HLT",
                    "drop l1tEMTFHitExtras_simEmtfDigis_RPC_HLT",
                    "drop l1tEMTFTrackExtras_simEmtfDigis__HLT",
   )
)

# All this stuff just runs the various EG algorithms that we are studying
                         
# ---- Global Tag :
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '100X_upgrade2023_realistic_v1', '')

# Choose a 2030 geometry!
process.load('Configuration.Geometry.GeometryExtended2023D17Reco_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')



# --------------------------------------------------------------------------------------------
#
# ----    Produce the ECAL TPs
#
#process.EcalEBTrigPrimProducer = cms.EDProducer("EcalEBTrigPrimProducer",
#    BarrelOnly = cms.bool(True),
#    barrelEcalDigis = cms.InputTag("simEcalDigis","ebDigis"),
#    binOfMaximum = cms.int32(6), ## optional from release 200 on, from 1-10
#    TcpOutput = cms.bool(False),
#    Debug = cms.bool(False),
#    Famos = cms.bool(False),
#    nOfSamples = cms.int32(1)
#)
#
#process.pNancy = cms.Path( process.EcalEBTrigPrimProducer )



# --------------------------------------------------------------------------------------------
#
# ----    Produce the L1EGCrystal clusters (code of Sasha Savin)

process.L1EGammaCrystalsProducer = cms.EDProducer("L1EGCrystalClusterProducer",
   EtminForStore = cms.double(0.),
   EcalTpEtMin = cms.untracked.double(0.5), # 500 MeV default per each Ecal TP
   EtMinForSeedHit = cms.untracked.double(1.0), # 1 GeV decault for seed hit
   debug = cms.untracked.bool(False),
   useRecHits = cms.untracked.bool(False),
   doBremClustering = cms.untracked.bool(True), # Should always be True when using for E/Gamma
   ecalTPEB = cms.InputTag("simEcalEBTriggerPrimitiveDigis","","HLT"),
   ecalRecHitEB = cms.InputTag("ecalRecHit","EcalRecHitsEB","RECO"),
   hcalRecHit = cms.InputTag("hbhereco"),
   hcalTP = cms.InputTag("simHcalTriggerPrimitiveDigis","","HLT"),
   useTowerMap = cms.untracked.bool(False)
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
   L1CrystalClustersInputTag = cms.InputTag("L1EGammaCrystalsProducer","L1EGXtalClusterNoCuts"),
   genParticles = cms.InputTag("genParticles"),
   OfflineRecoClustersInputTag = cms.InputTag("correctedHybridSuperClusters"),
   #ecalTPEB = cms.InputTag("EcalEBTrigPrimProducer","","L1AlgoTest"),
   ecalTPEB = cms.InputTag("simEcalEBTriggerPrimitiveDigis","","HLT"),
   doEfficiencyCalc = cms.untracked.bool(True),
   useOfflineClusters = cms.untracked.bool(False),
   useEndcap = cms.untracked.bool(False),
   turnOnThresholds = cms.untracked.vint32(20, 30, 16),
   histogramBinCount = cms.untracked.int32(100),
   histogramRangeLow = cms.untracked.double(0),
   histogramRangeHigh = cms.untracked.double(100),
   histogramEtaBinCount = cms.untracked.int32(20),
   genMatchDeltaRcut = cms.untracked.double(0.25),
   genMatchRelPtcut = cms.untracked.double(0.5),
   debug = cms.untracked.bool(False),
   doTracking = cms.untracked.bool(False),
   L1TrackInputTag = cms.InputTag("TTClustersFromPhase2TrackerDigis", "ClusterInclusive", "HLT"),
   L1TrackPrimaryVertexTag = cms.InputTag("mix", "InitialVertices", "HLT"),
   Stage2EG1Tag = cms.InputTag("hltGtStage2Digis", "EGamma", "HLT")
)

process.panalyzer = cms.Path(process.TPAnalyzer+process.analyzer)



process.TFileService = cms.Service("TFileService", 
   fileName = cms.string("$outputFileName"), 
   closeFileFast = cms.untracked.bool(True)
)



#dump_file = open("dump_file.py", "w")
#dump_file.write(process.dumpPython())


