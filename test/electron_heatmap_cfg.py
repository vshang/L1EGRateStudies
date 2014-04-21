import FWCore.ParameterSet.Config as cms

process = cms.Process("test")

process.load("FWCore.MessageService.MessageLogger_cfi")

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )

# Single electron (for efficiency)
from SLHCUpgradeSimulations.L1TrackTriggerObjects.singleElectronFiles_cfi import *
# Single positron (for efficiency)
from SLHCUpgradeSimulations.L1TrackTriggerObjects.singlePositronFiles_cfi import *

process.source = cms.Source("PoolSource",
   fileNames = singleElectronFiles
   #fileNames = singlePositronFiles
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

process.reconstruction_step = cms.Path( process.calolocalreco )


process.analyzer = cms.EDAnalyzer('L1EGCrystalsHeatMap',
   DEBUG = cms.untracked.bool(False),
   range = cms.untracked.int32(20)
)

process.panalyzer = cms.Path(process.analyzer)

process.TFileService = cms.Service("TFileService", 
   fileName = cms.string("electronHeatmap.root"), 
   closeFileFast = cms.untracked.bool(True)
)
