import FWCore.ParameterSet.Config as cms

from Configuration.StandardSequences.Eras import eras

process = cms.Process("L1AlgoTest",eras.Phase2_trigger)

process.load('Configuration.StandardSequences.Services_cff')
process.load("FWCore.MessageService.MessageLogger_cfi")
process.load('Configuration.EventContent.EventContent_cff')
process.MessageLogger.categories = cms.untracked.vstring('L1EGRateStudies', 'FwkReport')
process.MessageLogger.cerr.FwkReport = cms.untracked.PSet(
   reportEvery = cms.untracked.int32(100)
)

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(50) )

process.source = cms.Source("PoolSource",
   fileNames = cms.untracked.vstring(),
   dropDescendantsOfDroppedBranches=cms.untracked.bool(False),
   inputCommands = cms.untracked.vstring(
                    "keep *",
                    "drop l1tEMTFHitExtras_simEmtfDigis_CSC_HLT",
                    "drop l1tEMTFHitExtras_simEmtfDigis_RPC_HLT",
                    "drop l1tEMTFTrackExtras_simEmtfDigis__HLT",
                    "drop l1tEMTFHit2016Extras_simEmtfDigis_CSC_HLT",
                    "drop l1tEMTFHit2016Extras_simEmtfDigis_RPC_HLT",
                    "drop l1tEMTFHit2016s_simEmtfDigis__HLT",
                    "drop l1tEMTFTrack2016Extras_simEmtfDigis__HLT",
                    "drop l1tEMTFTrack2016s_simEmtfDigis__HLT",
                    "drop l1tHGCalTowerMapBXVector_hgcalTriggerPrimitiveDigiProducer_towerMap_HLT",
                    "drop PCaloHits_g4SimHits_EcalHitsEB_SIM",
                    "drop EBDigiCollection_simEcalUnsuppressedDigis__HLT",
                    "drop PCaloHits_g4SimHits_HGCHitsEE_SIM",
                    "drop HGCalDetIdHGCSampleHGCDataFramesSorted_mix_HGCDigisEE_HLT",

   )
)

# All this stuff just runs the various EG algorithms that we are studying
                         
# ---- Global Tag :
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
#process.GlobalTag = GlobalTag(process.GlobalTag, '100X_upgrade2023_realistic_v1', '')
process.GlobalTag = GlobalTag(process.GlobalTag, '93X_upgrade2023_realistic_v5', '')

# Choose a 2030 geometry!
process.load('Configuration.Geometry.GeometryExtended2023D17Reco_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')

# Add HCAL Transcoder
process.load('SimCalorimetry.HcalTrigPrimProducers.hcaltpdigi_cff')
process.load('CalibCalorimetry.CaloTPG.CaloTPGTranscoder_cfi')





# --------------------------------------------------------------------------------------------
#
# ----    Produce the L1EGCrystal clusters using Emulator

process.load('L1Trigger.L1CaloTrigger.L1EGammaCrystalsEmulatorProducer_cfi')


# ----------------------------------------------------------------------------------------------
# 
# Analyzer starts here


process.analyzer = cms.EDAnalyzer("L1TowerAnalyzer",
    HcalTpEtMin = cms.double(0.0), # Default is 0.5 GeV
    EcalTpEtMin = cms.double(0.0), # Default is 0.5 GeV
    HGCalHadTpEtMin = cms.double(0.0),
    HGCalEmTpEtMin = cms.double(0.0),
    puThreshold = cms.double(5.0), # Default is 5 GeV
    #puThresholdEcal = cms.double(3.0), # Default is 5 GeV # Original values
    #puThresholdHcal = cms.double(4.0), # Default is 5 GeV
    puThresholdEcal = cms.double(2.0), # Default is 5 GeV
    puThresholdHcal = cms.double(3.0), # Default is 5 GeV
    puThresholdL1eg = cms.double(4.0), # Default is 5 GeV
    puThresholdHGCalEM = cms.double(3.0), # Default is 5 GeV
    puThresholdHGCalHad = cms.double(3.0), # Default is 5 GeV
    puThresholdHF = cms.double(5.0), # Default is 5 GeV
    debug = cms.bool(False),
    #debug = cms.untracked.bool(True),
    vertexTag = cms.InputTag("g4SimHits","","SIM"),
    trackingVertexInitTag = cms.InputTag("mix","InitialVertices","HLT"),
    l1CaloTowers = cms.InputTag("L1EGammaClusterEmuProducer","L1CaloTowerCollection","L1AlgoTest"),
    L1CrystalClustersInputTag = cms.InputTag("L1EGammaClusterEmuProducer", "L1EGXtalClusterEmulator", "L1AlgoTest"),
    L1HgcalTowersInputTag = cms.InputTag("hgcalTriggerPrimitiveDigiProducer","tower"),
    hcalDigis = cms.InputTag("simHcalTriggerPrimitiveDigis"),
)

process.pL1Objs = cms.Path( 
    process.L1EGammaClusterEmuProducer *
    process.analyzer
)



process.TFileService = cms.Service("TFileService", 
   fileName = cms.string( "output.root" ), 
   closeFileFast = cms.untracked.bool(True)
)



#dump_file = open("dump_file.py", "w")
#dump_file.write(process.dumpPython())


