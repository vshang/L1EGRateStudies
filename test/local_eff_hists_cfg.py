import FWCore.ParameterSet.Config as cms

process = cms.Process("L1AlgoTest")

process.load('Configuration.StandardSequences.Services_cff')
process.load("FWCore.MessageService.MessageLogger_cfi")
process.load('Configuration.EventContent.EventContent_cff')
process.MessageLogger.categories = cms.untracked.vstring('L1EGRateStudies', 'FwkReport')
process.MessageLogger.cerr.FwkReport = cms.untracked.PSet(
   reportEvery = cms.untracked.int32(1)
)

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )

process.source = cms.Source("PoolSource",
# file dataset=/RelValSingleElectronPt35Extended/CMSSW_8_1_0_pre11-PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/GEN-SIM-DIGI-RAW
    fileNames = cms.untracked.vstring(
        '/store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-DIGI-RAW/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/0ADFD7B5-4277-E611-8E89-0025905A6132.root',
        '/store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-DIGI-RAW/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/0C8DF598-1977-E611-95D4-0025905A612E.root',
        '/store/relval/CMSSW_8_1_0_pre11/RelValSingleElectronPt35Extended/GEN-SIM-DIGI-RAW/PU25ns_81X_mcRun2_asymptotic_v5_2023D1PU140-v1/00000/148A8242-1577-E611-B3B6-0025905B855E.root',)
#   fileNames = cms.untracked.vstring(
#        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre9/RelValSingleElectronPt35Extended/GEN-SIM-RECO/81X_mcRun2_asymptotic_v2_2023LReco-v1/10000/72FC7A8C-4E53-E611-95D6-0CC47A78A360.root',
#        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre9/RelValSingleElectronPt35Extended/GEN-SIM-RECO/81X_mcRun2_asymptotic_v2_2023LReco-v1/10000/421F5CDF-4F53-E611-B5C2-0CC47A4D7686.root',
#        'file:root://cmsxrootd.fnal.gov///store/relval/CMSSW_8_1_0_pre9/RelValSingleElectronPt35Extended/GEN-SIM-RECO/81X_mcRun2_asymptotic_v2_2023LReco-v1/10000/BACF3CE0-4F53-E611-84E4-0025905A607E.root')
)

# All this stuff just runs the various EG algorithms that we are studying
                         
# ---- Global Tag :
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
#process.GlobalTag = GlobalTag(process.GlobalTag, 'PH2_1K_FB_V3::All', '')
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:run2_mc', '')

# Choose a 2030 geometry!
# The ones which don't work all replace the ECAL Endcap geometry with HGCal stuff
# Options in cmssw_810_pre16: (each also has an option without the Reco)
process.load('Configuration.Geometry.GeometryExtended2023D1Reco_cff') # Works
#process.load('Configuration.Geometry.GeometryExtended2023D2Reco_cff') # Works
#process.load('Configuration.Geometry.GeometryExtended2023D3Reco_cff') # HGCal stuff, doesn't work 
#process.load('Configuration.Geometry.GeometryExtended2023D4Reco_cff') # HGCal stuff, doesn't work 
#process.load('Configuration.Geometry.GeometryExtended2023D5Reco_cff') # Crashes geometryHelper, this is the default one used for ECAL TPs
#process.load('Configuration.Geometry.GeometryExtended2023D6Reco_cff') # Works


process.load('Configuration.StandardSequences.MagneticField_38T_PostLS1_cff')
#process.load('Configuration.StandardSequences.L1TrackTrigger_cff')
#process.load('Geometry.TrackerGeometryBuilder.StackedTrackerGeometry_cfi')
#process.load('IOMC.EventVertexGenerators.VtxSmearedHLLHC_cfi')
#process.load('IOMC.EventVertexGenerators.VtxSmearedHLLHC_cfi')

#process.load('Configuration/StandardSequences/L1HwVal_cff')
#process.load('Configuration.StandardSequences.RawToDigi_cff')
#process.load("SLHCUpgradeSimulations.L1CaloTrigger.SLHCCaloTrigger_cff")

# bug fix for missing HCAL TPs in MC RAW
#from SimCalorimetry.HcalTrigPrimProducers.hcaltpdigi_cff import HcalTPGCoderULUT
#HcalTPGCoderULUT.LUTGenerationMode = cms.bool(True)
#process.valRctDigis.hcalDigis             = cms.VInputTag(cms.InputTag('valHcalTriggerPrimitiveDigis'))
#process.L1CaloTowerProducer.HCALDigis =  cms.InputTag("valHcalTriggerPrimitiveDigis")
#
#process.slhccalo = cms.Path( process.RawToDigi + process.valHcalTriggerPrimitiveDigis+process.SLHCCaloTrigger)
#
# run L1Reco to produce the L1EG objects corresponding
# to the current trigger
#process.load('Configuration.StandardSequences.L1Reco_cff')
#process.L1Reco = cms.Path( process.l1extraParticles )

# producer for UCT2015 / Stage-1 trigger objects
#process.load("L1Trigger.UCT2015.emulationMC_cfi")
#process.load("L1Trigger.UCT2015.uctl1extraparticles_cfi")
#process.pUCT = cms.Path(
#    process.emulationSequence *
#    process.uct2015L1Extra
#)


process.load("RecoLocalCalo.Configuration.hcalLocalReco_cff")
process.load("RecoLocalCalo.Configuration.hcalGlobalReco_cff")

#from RecoLocalCalo.Configuration.ecalLocalRecoSequence_cff import *
#localreco = cms.Sequence(ecalLocalRecoSequence)
#process.load("RecoLocalCalo.EcalRecProducers.ecalLocalRecoSequence_cff")

# --------------------------------------------------------------------------------------------
#
# ----    Produce the ECAL TPs

#process.simEcalEBTriggerPrimitiveDigis = cms.EDProducer("EcalEBTrigPrimProducer",
process.EcalEBTrigPrimProducer = cms.EDProducer("EcalEBTrigPrimProducer",
    BarrelOnly = cms.bool(True),
#    barrelEcalDigis = cms.InputTag("simEcalUnsuppressedDigis","ebDigis"),
    barrelEcalDigis = cms.InputTag("simEcalDigis","ebDigis"),
#    barrelEcalDigis = cms.InputTag("selectDigi","selectedEcalEBDigiCollection"),
    binOfMaximum = cms.int32(6), ## optional from release 200 on, from 1-10
    TcpOutput = cms.bool(False),
    Debug = cms.bool(False),
    Famos = cms.bool(False),
    nOfSamples = cms.int32(1)
)

process.pNancy = cms.Path( process.EcalEBTrigPrimProducer )



# --------------------------------------------------------------------------------------------
#
# ----    Produce the L1EGCrystal clusters (code of Sasha Savin)

# first you need the ECAL RecHIts :
#process.load('Configuration.StandardSequences.Reconstruction_cff')
#process.reconstruction_step = cms.Path( process.calolocalreco )

process.L1EGammaCrystalsProducer = cms.EDProducer("L1EGCrystalClusterProducer",
   EtminForStore = cms.double(0.),
   debug = cms.untracked.bool(True),
   useECalEndcap = cms.bool(False),
   ecalTPEB = cms.InputTag("EcalEBTrigPrimProducer","","L1AlgoTest"),
   #ecalRecHitEB = cms.InputTag("ecalRecHit","EcalRecHitsEB","RECO"),
   #ecalRecHitEE = cms.InputTag("ecalRecHit","EcalRecHitsEE","RECO"),
   #hcalRecHit = cms.InputTag("hbhereco") # for testing non-2023 geometry configurations
   #hcalRecHit = cms.InputTag("hltHbhereco","","L1AlgoTest")
   #hcalRecHit = cms.InputTag("hltHbhereco")
   hcalRecHit = cms.InputTag("hbhereco")
   #hcalRecHit = cms.InputTag("hbheUpgradeReco")
   #hcalTP = cms.InputTag("simHcalTriggerPrimitiveDigis","","HLT")
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
#   eClusterSrc = cms.InputTag("L1EGammaCrystalsProducer","EGCrystalCluster")
#)
#process.egcrystal_producer = cms.Path(process.l1ExtraCrystalProducer)




# ----------------------------------------------------------------------------------------------
# 
# Do offline reconstruction step for electron matching
# First we need to run EcalSeverityLevelESProducer ES Producer

process.load('RecoLocalCalo.EcalRecAlgos.EcalSeverityLevelESProducer_cfi')

#process.load('RecoEcal.Configuration.RecoEcal_cff')
#process.ecalClusters = cms.Path(process.ecalClustersNoPFBox)




# ----------------------------------------------------------------------------------------------
# 
# Analyzer starts here

process.analyzer = cms.EDAnalyzer('L1EGRateStudies',
   #L1EGammaInputTags = cms.VInputTag(
   #   # Old stage-2 trigger
   #   cms.InputTag("SLHCL1ExtraParticles","EGamma"),
   #   # 'dynamic clustering'
   #   cms.InputTag("SLHCL1ExtraParticlesNewClustering","EGamma"),
   #   # Run 1 algo.
   #   cms.InputTag("l1extraParticles", "Isolated"),
   #   cms.InputTag("l1extraParticles", "NonIsolated"),
   #   # UCT alg.
   #   cms.InputTag("l1extraParticlesUCT", "Isolated"),
   #   cms.InputTag("l1extraParticlesUCT", "NonIsolated"),
   #   # Crystal-level algo.
   #   cms.InputTag("L1EGammaCrystalsProducer","EGammaCrystal")
   #),
   L1CrystalClustersInputTag = cms.InputTag("L1EGammaCrystalsProducer","EGCrystalCluster"),
   genParticles = cms.InputTag("genParticles"),
   OfflineRecoClustersInputTag = cms.InputTag("correctedHybridSuperClusters"),
   #ecalRecHitEB = cms.InputTag("ecalRecHit","EcalRecHitsEB","RECO"),
   ecalTPEB = cms.InputTag("EcalEBTrigPrimProducer","","L1AlgoTest"),
   #ecalRecHitEE = cms.InputTag("ecalRecHit","EcalRecHitsEE","RECO"),
   doEfficiencyCalc = cms.untracked.bool(True),
   #doEfficiencyCalc = cms.untracked.bool(False),
   useOfflineClusters = cms.untracked.bool(False),
   useEndcap = cms.untracked.bool(False),
   turnOnThresholds = cms.untracked.vint32(20, 30, 16),
   histogramBinCount = cms.untracked.int32(60),
   histogramRangeLow = cms.untracked.double(0),
   histogramRangeHigh = cms.untracked.double(50),
   histogramEtaBinCount = cms.untracked.int32(20),
   genMatchDeltaRcut = cms.untracked.double(0.25),
   genMatchRelPtcut = cms.untracked.double(10.0),
   debug = cms.untracked.bool(True)
)

process.panalyzer = cms.Path(process.analyzer)

process.TFileService = cms.Service("TFileService", 
   fileName = cms.string("effTest.root"), 
   closeFileFast = cms.untracked.bool(True)
)

dump_file = open("dump_file.py", "w")
dump_file.write(process.dumpPython())


