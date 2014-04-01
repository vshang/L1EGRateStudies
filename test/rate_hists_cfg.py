import FWCore.ParameterSet.Config as cms

process = cms.Process("test")

process.load("FWCore.MessageService.MessageLogger_cfi")
process.MessageLogger.categories = cms.untracked.vstring('L1EGRateStudies', 'FwkReport')
#process.MessageLogger.cout = cms.untracked.PSet(
#   threshold = cms.untracked.string('INFO'),
#   default = cms.untracked.PSet(
#      limit = cms.untracked.int32(0)
#   ),
#   L1EGRateStudies = cms.untracked.PSet(
#      limit = cms.untracked.int32(100)
#   )
#)
process.MessageLogger.cerr.FwkReport = cms.untracked.PSet(
   reportEvery = cms.untracked.int32(500)
)

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )

# List (1 of 4?) of NeutrinoGun samples (i.e. background rate)
from SLHCUpgradeSimulations.L1TrackTriggerObjects.minBiasFiles_p1_cfi import *


process.source = cms.Source("PoolSource",
   fileNames = minBiasFiles_p1
)

# All this stuff just runs the various EG algorithms that we are studying

# Load geometry
process.load("Configuration.Geometry.GeometryIdeal_cff")
process.load("Configuration.StandardSequences.FrontierConditions_GlobalTag_cff")
                            
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'POSTLS261_V3::All', '')

process.load("Configuration.StandardSequences.Services_cff")
process.load('Configuration/StandardSequences/L1HwVal_cff')
process.load("Configuration.StandardSequences.RawToDigi_Data_cff") ###check this for MC!
process.load('Configuration.StandardSequences.L1Reco_cff')
process.load('Configuration.StandardSequences.Reconstruction_cff')
process.load('Configuration/StandardSequences/EndOfProcess_cff')
process.load('Configuration.Geometry.GeometryIdeal_cff')
process.load('Configuration/StandardSequences/MagneticField_AutoFromDBCurrent_cff')
process.load("JetMETCorrections.Configuration.DefaultJEC_cff")

# --------------------------------------------------------------------------------------------
#
# ----    Runs the stage-2 L1EG algorithms
#

process.load('Configuration.StandardSequences.RawToDigi_cff')
process.load("SLHCUpgradeSimulations.L1CaloTrigger.SLHCCaloTrigger_cff")

process.p = cms.Path( 
    process.RawToDigi+
    process.SLHCCaloTrigger
    )

# bug fix for missing HCAL TPs in MC RAW
process.p.insert(1, process.valHcalTriggerPrimitiveDigis)
from SimCalorimetry.HcalTrigPrimProducers.hcaltpdigi_cff import HcalTPGCoderULUT
HcalTPGCoderULUT.LUTGenerationMode = cms.bool(True)
process.valRctDigis.hcalDigis             = cms.VInputTag(cms.InputTag('valHcalTriggerPrimitiveDigis'))
process.L1CaloTowerProducer.HCALDigis =  cms.InputTag("valHcalTriggerPrimitiveDigis")

# run L1Reco to produce the L1EG objects corresponding
# to the current trigger
#process.load('Configuration.StandardSequences.L1Reco_cff')
#process.L1Reco = cms.Path( process.l1extraParticles )

# --------------------------------------------------------------------------------------------
#
# ----    Produce the L1EGCrystal clusters (code of Sasha Savin)

	# first you need the ECAL RecHIts :
process.reconstruction_step = cms.Path( process.calolocalreco )

process.L1EGammaCrystalsProducer = cms.EDProducer("L1EGCrystalClusterProducer",
   DEBUG = cms.bool(False)
)
process.pSasha = cms.Path( process.L1EGammaCrystalsProducer )

# --------------------------------------------------------------------------------------------
#
# ----  Match the L1EG stage-2 objects created by the SLHCCaloTrigger sequence above
#	with the crystal-level clusters.
#	This produces a new collection of L1EG objects, starting from the original
#	L1EG collection. The eta and phi of the L1EG objects is corrected using the
#	information of the xtal level clusters.

process.l1ExtraCrystalProducer = cms.EDProducer("L1ExtraCrystalPosition",
   eGammaSrc = cms.InputTag("SLHCL1ExtraParticles","EGamma"),
   eClusterSrc = cms.InputTag("L1EGammaCrystalsProducer","EGCrystalCluster")
)
process.egcrystal_producer = cms.Path(process.l1ExtraCrystalProducer)

# ----------------------------------------------------------------------------------------------
# 
# Analyzer starts here

process.analyzer = cms.EDAnalyzer('L1EGRateStudies',
# Old stage-2 trigger
   L1EGammaInputTag = cms.InputTag("SLHCL1ExtraParticles","EGamma"),
# New stage-2 trigger (some sort of isolation cut?)
#   L1EGammaInputTag = cms.InputTag("SLHCL1ExtraParticles","IsoEGamma"),
# Sacha's cluster trigger (hovere < 1, isolation < 2)
#   L1EGammaInputTag = cms.InputTag("L1EGammaCrystalsProducer","EGammaCrystal"),
   L1CrystalClustersInputTag = cms.InputTag("L1EGammaCrystalsProducer","EGCrystalCluster"),
# use this when running over single particle gun sources
   doEfficiencyCalc = cms.untracked.bool(False),
   hovere_cut_min = cms.untracked.double(0.2),
   hovere_cut_max = cms.untracked.double(1.4),
   ecal_isolation_cut_min = cms.untracked.double(0.5),
   ecal_isolation_cut_max = cms.untracked.double(2),
   cut_steps = cms.untracked.int32(4),
   histogramBinCount = cms.untracked.int32(19),
   histogramEtaBinCount = cms.untracked.int32(20)
)

process.panalyzer = cms.Path(process.analyzer)

process.TFileService = cms.Service("TFileService", 
   fileName = cms.string("egTriggerRates.root"), 
   closeFileFast = cms.untracked.bool(True)
)
