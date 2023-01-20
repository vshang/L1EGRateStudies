import FWCore.ParameterSet.Config as cms

from Configuration.StandardSequences.Eras import eras

process = cms.Process('REPR',eras.Phase2C9)
 
# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.Geometry.GeometryExtended2026D49Reco_cff')
process.load('Configuration.Geometry.GeometryExtended2026D49_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.SimL1Emulator_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.MessageLogger.L1CaloJets = dict()
process.MessageLogger.cerr.FwkReport = cms.untracked.PSet(
   reportEvery = cms.untracked.int32(1)
)

#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10) )

process.source = cms.Source("PoolSource",
   fileNames = cms.untracked.vstring('root://cms-xrd-global.cern.ch//store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/VBFHToTauTau_M125_14TeV_powheg_pythia8_correctedGridpack_tuneCP5/FEVT/PU200_111X_mcRun4_realistic_T15_v1-v1/120000/084C8B72-BC64-DE46-801F-D971D5A34F62.root'),
   dropDescendantsOfDroppedBranches=cms.untracked.bool(False),
   inputCommands = cms.untracked.vstring(
                    "keep *",
                    "drop l1tEMTFHitExtras_simEmtfDigis_CSC_HLT",
                    "drop l1tEMTFHitExtras_simEmtfDigis_RPC_HLT",
                    "drop l1tEMTFTrackExtras_simEmtfDigis__HLT",
                    "drop l1tEMTFHit2016Extras_simEmtfDigis_CSC_HLT",
                    "drop l1tEMTFHit2016Extras_simEmtfDigis_RPC_HLT",
                    "drop l1tEMTFHit2016s_simEmtfDigis__HLT",
                    "drop l1tTkPrimaryVertexs_L1TkPrimaryVertex_*_*",
                    #"drop l1tEMTFTrack2016Extras_simEmtfDigis__HLT",
                    #"drop l1tEMTFTrack2016s_simEmtfDigis__HLT",
                    #"drop l1tHGCalTowerMapBXVector_hgcalTriggerPrimitiveDigiProducer_towerMap_HLT",
                    #"drop PCaloHits_g4SimHits_EcalHitsEB_SIM",
                    #"drop PCaloHits_g4SimHits_HGCHitsEE_SIM",
                    #"drop HGCalDetIdHGCSampleHGCDataFramesSorted_mix_HGCDigisEE_HLT",

   )
)

# ---- Global Tag :
from Configuration.AlCa.GlobalTag import GlobalTag
#process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:phase2_realistic', '') 
process.GlobalTag = GlobalTag(process.GlobalTag, '123X_mcRun4_realistic_v3', '') 


# Add HCAL Transcoder
process.load('SimCalorimetry.HcalTrigPrimProducers.hcaltpdigi_cff')
process.load('CalibCalorimetry.CaloTPG.CaloTPGTranscoder_cfi')


process.L1simulation_step = cms.Path(process.SimL1Emulator)




# --------------------------------------------------------------------------------------------
#
# ----    Load the L1CaloJet sequence designed to accompany process named "REPR"

process.load('L1Trigger.L1CaloTrigger.L1CaloJets_cff')
process.l1CaloJets = cms.Path(process.l1CaloJetsSequence)






process.Out = cms.OutputModule( "PoolOutputModule",
     fileName = cms.untracked.string( "l1caloJetTest.root" ),
     fastCloning = cms.untracked.bool( False ),
     outputCommands = cms.untracked.vstring(
                          "keep *_L1EGammaClusterEmuProducer_*_*",
                          "keep *_L1CaloJetProducer_*_*",
                          "keep *_L1CaloJetHTTProducer_*_*",
                          "keep *_TriggerResults_*_*",
                          "keep *_simHcalTriggerPrimitiveDigis_*_*",
                          "keep *_EcalEBTrigPrimProducer_*_*",
                          "keep *_hgcalTowerProducer_*_*"
                          )
)

process.end = cms.EndPath( process.Out )



#dump_file = open("dump_file.py", "w")
#dump_file.write(process.dumpPython())


