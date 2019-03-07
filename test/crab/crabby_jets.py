import FWCore.ParameterSet.Config as cms

from Configuration.StandardSequences.Eras import eras

process = cms.Process('REPR',eras.Phase2C4_trigger)
 
# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.Geometry.GeometryExtended2023D35Reco_cff')
process.load('Configuration.Geometry.GeometryExtended2023D35_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.SimL1Emulator_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.MessageLogger.categories = cms.untracked.vstring('L1CaloJets', 'FwkReport')
process.MessageLogger.cerr.FwkReport = cms.untracked.PSet(
   reportEvery = cms.untracked.int32(1)
)

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10) )

process.source = cms.Source("PoolSource",
   fileNames = cms.untracked.vstring(),
   # dasgoclient --query="dataset dataset=/*/*PhaseIIMTDTDRAutumn18DR*/FEVT"
   #fileNames = cms.untracked.vstring('root://cms-xrd-global.cern.ch//store/mc/PhaseIIMTDTDRAutumn18DR/VBFHToTauTau_M125_14TeV_powheg_pythia8/FEVT/PU200_103X_upgrade2023_realistic_v2-v1/280000/EFC8271A-8026-6A43-AF18-4CB7609B3348.root'),
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
                    "drop PCaloHits_g4SimHits_HGCHitsEE_SIM",
                    "drop HGCalDetIdHGCSampleHGCDataFramesSorted_mix_HGCDigisEE_HLT",

   )
)

# ---- Global Tag :
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '103X_upgrade2023_realistic_v2', '') 


# Add HCAL Transcoder
process.load('SimCalorimetry.HcalTrigPrimProducers.hcaltpdigi_cff')
process.load('CalibCalorimetry.CaloTPG.CaloTPGTranscoder_cfi')


process.L1simulation_step = cms.Path(process.SimL1Emulator)
# Delete processes with tracks to avoid making them
del process.l1TkMuonStubEndCap
del process.L1TkPrimaryVertex
del process.L1TkElectrons
del process.L1TkIsoElectrons
del process.L1TkPhotons
del process.L1TkCaloJets
del process.L1TrackerJets
del process.L1TrackerEtMiss
del process.L1TkCaloHTMissVtx
del process.L1TrackerHTMiss
del process.L1TkMuons
del process.L1TkGlbMuons
del process.L1TkTauFromCalo
del process.l1ParticleFlow
del process.l1PFMets
del process.l1PFJets
del process.l1pfTauProducer
del process.L1TkMuonStub
del process.VertexProducer
del process.l1KBmtfStubMatchedMuons
del process.l1StubMatchedMuons
del process.pfTracksFromL1Tracks
del process.l1pfProducer
del process.ak4L1Calo
del process.ak4L1TK
del process.ak4L1TKV
del process.ak4L1PF
del process.ak4L1Puppi
del process.ak4L1TightTK
del process.ak4L1TightTKV
del process.pfClustersFromL1EGClusters
del process.pfClustersFromCombinedCalo
del process.l1pfProducerForMET
del process.l1pfProducerTightTK
del process.l1MetCalo
del process.l1MetTK
del process.l1MetTKV
del process.l1MetPF
del process.l1MetPuppi
del process.l1MetTightTK
del process.l1MetTightTKV


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



process.tauGenJetsSelectorElectrons = cms.EDFilter("TauGenJetDecayModeSelector",
     src = cms.InputTag("tauGenJets"),
     select = cms.vstring('electron'), 
     filter = cms.bool(False)
)



process.tauGenJetsSelectorMuons = cms.EDFilter("TauGenJetDecayModeSelector",
     src = cms.InputTag("tauGenJets"),
     select = cms.vstring('muon'), 
     filter = cms.bool(False)
)






# --------------------------------------------------------------------------------------------
#
# ----    Produce the L1EGCrystal clusters using Emulator

process.load('L1Trigger.L1CaloTrigger.L1EGammaCrystalsEmulatorProducer_cfi')
process.L1EGammaClusterEmuProducer.ecalTPEB = cms.InputTag("simEcalEBTriggerPrimitiveDigis","","REPR")



# --------------------------------------------------------------------------------------------
#
# ----    Produce the calibrated tower collection combining Barrel, HGCal, HF

process.load('L1Trigger/L1CaloTrigger/L1TowerCalibrationProducer_cfi')
#process.L1TowerCalibrationProducer.barrelSF = cms.double(4.0)
#process.L1TowerCalibrationProducer.hgcalSF = cms.double(1.45)
#process.L1TowerCalibrationProducer.hfSF = cms.double(1.2)
#process.L1TowerCalibrationProducer.skipCalibrations = cms.bool(True)
process.L1TowerCalibrationProducer.l1CaloTowers = cms.InputTag("L1EGammaClusterEmuProducer","L1CaloTowerCollection","REPR")
process.L1TowerCalibrationProducer.L1HgcalTowersInputTag = cms.InputTag("hgcalTowerProducer","HGCalTowerProcessor","REPR")



# --------------------------------------------------------------------------------------------
#
# ----    Produce the L1CaloJets with the L1EG clusters as ECAL seeds

process.load('L1Trigger/L1CaloTrigger/L1CaloJetProducer_cfi')
process.L1CaloJetProducer.l1CaloTowers = cms.InputTag("L1TowerCalibrationProducer","L1CaloTowerCalibratedCollection","REPR")
process.L1CaloJetProducer.L1CrystalClustersInputTag = cms.InputTag("L1EGammaClusterEmuProducer", "L1EGXtalClusterEmulator","REPR")



process.pL1Objs = cms.Path( 
    process.tauGenJets *
    process.tauGenJetsSelectorAllHadrons *
    process.tauGenJetsSelectorElectrons *
    process.tauGenJetsSelectorMuons *
    process.L1EGammaClusterEmuProducer *
    process.L1TowerCalibrationProducer *
    process.L1CaloJetProducer
)



# ----------------------------------------------------------------------------------------------
# 
# Analyzer starts here

process.analyzer = cms.EDAnalyzer('L1CaloJetStudies',
    L1CaloJetsInputTag = cms.InputTag("L1CaloJetProducer","L1CaloJetsNoCuts"),
    genJets = cms.InputTag("ak4GenJetsNoNu", "", "HLT"),
    genHadronicTauSrc = cms.InputTag("tauGenJetsSelectorAllHadrons"),
    genMatchDeltaRcut = cms.untracked.double(0.4),
    genMatchRelPtcut = cms.untracked.double(0.5),
    debug = cms.untracked.bool(False),
    doRate = cms.untracked.bool(False), # TEMPORARY FIXME
    Stage2JetTag = cms.InputTag("simCaloStage2Digis", "MP", "HLT"),
    Stage2TauTag = cms.InputTag("simCaloStage2Digis", "MP", "HLT"),
    puSrc = cms.InputTag("addPileupInfo")
)

process.panalyzer = cms.Path(process.analyzer)



process.TFileService = cms.Service("TFileService", 
   fileName = cms.string( "output.root" ), 
   closeFileFast = cms.untracked.bool(True)
)



#dump_file = open("dump_file.py", "w")
#dump_file.write(process.dumpPython())


