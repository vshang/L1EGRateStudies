import FWCore.ParameterSet.Config as cms

process = cms.Process("L1AlgoTest")

process.load('Configuration.StandardSequences.Services_cff')
process.load("FWCore.MessageService.MessageLogger_cfi")
process.load('Configuration.EventContent.EventContent_cff')
process.MessageLogger.categories = cms.untracked.vstring('L1EGRateStudies', 'FwkReport')
process.MessageLogger.cerr.FwkReport = cms.untracked.PSet(
   reportEvery = cms.untracked.int32(10)
)

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )

process.source = cms.Source("PoolSource",
   fileNames = cms.untracked.vstring($inputFileNames)
)

# All this stuff just runs the various EG algorithms that we are studying
                         
# ---- Global Tag :
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:phase2_realistic', '')

# Choose a 2030 geometry!
process.load('Configuration.Geometry.GeometryExtended2023D4Reco_cff') # Phase-2 Preferred
process.load('Configuration.StandardSequences.MagneticField_38T_PostLS1_cff')




#process.load("RecoLocalCalo.Configuration.hcalLocalReco_cff")
#process.load("RecoLocalCalo.Configuration.hcalGlobalReco_cff")


# --------------------------------------------------------------------------------------------
#
# ----    Produce the ECAL TPs
#
##process.simEcalEBTriggerPrimitiveDigis = cms.EDProducer("EcalEBTrigPrimProducer",
#process.EcalEBTrigPrimProducer = cms.EDProducer("EcalEBTrigPrimProducer",
#    BarrelOnly = cms.bool(True),
##    barrelEcalDigis = cms.InputTag("simEcalUnsuppressedDigis","ebDigis"),
#    barrelEcalDigis = cms.InputTag("simEcalDigis","ebDigis"),
##    barrelEcalDigis = cms.InputTag("selectDigi","selectedEcalEBDigiCollection"),
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

# first you need the ECAL RecHIts :
#process.load('Configuration.StandardSequences.Reconstruction_cff')
#process.reconstruction_step = cms.Path( process.calolocalreco )

process.L1EGammaCrystalsProducer = cms.EDProducer("L1EGCrystalClusterProducer",
   EtminForStore = cms.double(0.),
   debug = cms.untracked.bool(False),
   useRecHits = cms.bool(False),
   ecalRecHitEB = cms.InputTag("ecalRecHit","EcalRecHitsEB","RECO"),
   #ecalTPEB = cms.InputTag("EcalEBTrigPrimProducer","","L1AlgoTest"),
   ecalTPEB = cms.InputTag("simEcalEBTriggerPrimitiveDigis","","HLT"),
   #hcalRecHit = cms.InputTag("hbhereco") # for testing non-2023 geometry configurations
   #hcalRecHit = cms.InputTag("hltHbhereco","","L1AlgoTest")
   #hcalRecHit = cms.InputTag("hltHbhereco")
   hcalRecHit = cms.InputTag("hbhereco"),
   #hcalRecHit = cms.InputTag("hbheUpgradeReco")
   hcalTP = cms.InputTag("simHcalTriggerPrimitiveDigis","","HLT"),

   #useTowerMap = cms.untracked.bool(False)
   useTowerMap = cms.untracked.bool(True)
   #towerMapName = cms.untracked.string("map1.json")
)

process.pSasha = cms.Path( process.L1EGammaCrystalsProducer )



# --------------------------------------------------------------------------------------------
#
# ----  Match the L1EG stage-2 objects created by the SLHCCaloTrigger sequence above
#	with the crystal-level clusters.
#	This produces a new collection of L1EG objects, starting from the original
#	L1EG collection. The eta and phi of the L1EG objects is corrected using the
#	information of the xtal level clusters.

#process.l1ExtraCrystalProducer = cms.EDProducer("L1ExtraCrystalPosition",
#   eGammaSrc = cms.InputTag("SLHCL1ExtraParticles","EGamma"),
#   eClusterSrc = cms.InputTag("L1EGammaCrystalsProducer","L1EGXtalClusterNoCuts")
#)
#process.egcrystal_producer = cms.Path(process.l1ExtraCrystalProducer)




# ----------------------------------------------------------------------------------------------
# 
# Do offline reconstruction step for electron matching
# First we need to run EcalSeverityLevelESProducer ES Producer

#process.load('RecoLocalCalo.EcalRecAlgos.EcalSeverityLevelESProducer_cfi')

#process.load('RecoEcal.Configuration.RecoEcal_cff')
#process.ecalClusters = cms.Path(process.ecalClustersNoPFBox)

# -------------------------------------------------------------------------------------------
#
### Mini-analyzer for ECAL TPs / RecHits
process.HitAnalyzer = cms.EDAnalyzer('HitAnalyzer',
   useRecHits = cms.bool(False),
   hasGenInfo = cms.bool(True),
   ecalRecHitEB = cms.InputTag("ecalRecHit","EcalRecHitsEB","RECO"),
   #ecalTPEB = cms.InputTag("EcalEBTrigPrimProducer","","L1AlgoTest"),
   ecalTPEB = cms.InputTag("simEcalEBTriggerPrimitiveDigis","","HLT"),
   hcalRecHit = cms.InputTag("hbhereco"),
   hcalTP = cms.InputTag("simHcalTriggerPrimitiveDigis","","HLT"),
   genParticles = cms.InputTag("genParticles")
)
process.p1 = cms.Path(process.HitAnalyzer)

# -------------------------------------------------------------------------------------------
#
### Mini-analyzer for L1EG TPs
process.analyzer = cms.EDAnalyzer('L1EGPreclusterAnalysis',
   L1CrystalClustersInputTag = cms.InputTag("L1EGammaCrystalsProducer","L1EGXtalClusterNoCuts"),
   L1CrystalClustersWithCutsInputTag = cms.InputTag("L1EGammaCrystalsProducer","L1EGXtalClusterWithCuts")
)
process.p2 = cms.Path(process.analyzer)


process.TFileService = cms.Service("TFileService", 
   fileName = cms.string("$outputFileName"), 
   closeFileFast = cms.untracked.bool(True)
)


# -------------------------------------------------------------------------------------------
#
### Uncomment this section to save the edm version of L1EG TPs
#process.Out = cms.OutputModule( "PoolOutputModule",
#    fileName = cms.untracked.string( "l1egBorderTest3.root" ),
#    fastCloning = cms.untracked.bool( False ),
#    outputCommands = cms.untracked.vstring( "keep *_L1EGammaCrystalsProducer_*_*")
#)
#process.end = cms.EndPath( process.Out )



