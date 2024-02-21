import FWCore.ParameterSet.Config as cms

from Configuration.StandardSequences.Eras import eras

#process = cms.Process('REPR',eras.Phase2C9)
process = cms.Process('REPR',eras.Phase2C17I13M9)
 
# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
#process.load('Configuration.Geometry.GeometryExtended2026D49Reco_cff')
#process.load('Configuration.Geometry.GeometryExtended2026D49_cff')
#process.load('Configuration.Geometry.GeometryExtended2026D88Reco_cff')
#process.load('Configuration.Geometry.GeometryExtended2026D88_cff')
process.load('Configuration.Geometry.GeometryExtended2026D95Reco_cff')
process.load('Configuration.Geometry.GeometryExtended2026D95_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.SimL1Emulator_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.MessageLogger.L1CaloJets = dict()
process.MessageLogger.cerr.FwkReport = cms.untracked.PSet(
   reportEvery = cms.untracked.int32(1)
)

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )

process.source = cms.Source("PoolSource",
   #fileNames = cms.untracked.vstring(),
   # dasgoclient --query="dataset dataset=/*/*PhaseIIMTDTDRAutumn18DR*/FEVT"
   # fileNames = cms.untracked.vstring('root://cms-xrd-global.cern.ch//store/mc/Phase2Fall22DRMiniAOD/SinglePion_Pt-0To200-gun/GEN-SIM-DIGI-RAW-MINIAOD/PU200_125X_mcRun4_realistic_v2-v1/30000/004d15e3-a12f-4ba9-a2f3-4b7277ffa418.root'),
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

# ---- For specifying specific event range
# process.source.eventsToProcess = cms.untracked.VEventRange("1:10722")


# ---- Global Tag :
from Configuration.AlCa.GlobalTag import GlobalTag
#process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:phase2_realistic', '') 
#process.GlobalTag = GlobalTag(process.GlobalTag, '123X_mcRun4_realistic_v3', '') 
process.GlobalTag = GlobalTag(process.GlobalTag, '125X_mcRun4_realistic_v2', '') 


# Add HCAL Transcoder
process.load('SimCalorimetry.HcalTrigPrimProducers.hcaltpdigi_cff')
process.load('CalibCalorimetry.CaloTPG.CaloTPGTranscoder_cfi')


process.L1simulation_step = cms.Path(process.SimL1Emulator)

# Add HGCal module energy splitting
from L1Trigger.L1THGCal.customTowers import custom_towers_energySplit
process = custom_towers_energySplit(process)


# --------------------------------------------------------------------------------------------
#
# ----   Produce Gen Taus

process.tauGenJets = cms.EDProducer(
    "TauGenJetProducer",
    GenParticles =  cms.InputTag('genParticles'),
    includeNeutrinos = cms.bool( False ),
    verbose = cms.untracked.bool( False )
)



process.tauGenJetsSelectorAllHadrons = cms.EDFilter("TauGenJetDecayModeSelector",
     src = cms.InputTag("tauGenJets"),
     select = cms.vstring('oneProng0Pi0', 
                          'oneProng1Pi0', 
                          'oneProng2Pi0', 
                          'oneProngOther',
                          'threeProng0Pi0', 
                          'threeProng1Pi0', 
                          'threeProngOther', 
                          'rare'),
     filter = cms.bool(False)
)


process.pGetTaus = cms.Path( 
    process.tauGenJets *
    process.tauGenJetsSelectorAllHadrons
)



# --------------------------------------------------------------------------------------------
#
# ----    Load the L1CaloJet sequence designed to accompany process named "REPR"

process.load('L1Trigger.L1CaloTrigger.L1CaloJets_cff')
process.l1CaloJets = cms.Path(process.L1TCaloJetsSequence)






process.Out = cms.OutputModule( "PoolOutputModule",
     fileName = cms.untracked.string( "output_round1.root" ),
     fastCloning = cms.untracked.bool( False ),
     outputCommands = cms.untracked.vstring(
                          # "keep *",
                          "drop *",
                          "keep *_genParticles_*_*",
                          "keep *_l1tPhase2L1CaloEGammaEmulator_*_*", #Added by Pallabi
                          #"keep *_l1tEGammaClusterEmuProducer_*_*",
                          #"keep *_l1tTowerCalibrationProducer_*_*",
                          "keep *_l1tCaloJetProducer_*_*",
                          "keep *_l1tPhase2CaloJetEmulator_*_*", #Added by Pallabi
                          "keep *_simCaloStage2Digis_MP_HLT",
                          "keep *_addPileupInfo_*_*",
                          "keep *_ak4GenJetsNoNu__HLT",
                          "keep *_tauGenJetsSelectorAllHadrons_*_*",
                          #Victor's edit: keep modules for track matching
                          # "keep *_g4SimHits_*_*",
                          # "keep *_TTStubsFromPhase2TrackerDigis_*_*",
                          # "keep *_TTClusterAssociatorFromPixelDigis_*_*",
                          # "keep *_TTStubAssociatorFromPixelDigis_*_*",
                          # "keep *_mix_*_*",
                          # "keep *_offlineBeamSpot_*_*",
                          # "keep *_TTTracksFromPhase2TrackerDigis_*_*",
                          #End of Victor's edit
                          )
)

process.end = cms.EndPath( process.Out )



#dump_file = open("dump_file.py", "w")
#dump_file.write(process.dumpPython())


