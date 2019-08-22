import FWCore.ParameterSet.Config as cms

from Configuration.StandardSequences.Eras import eras

process = cms.Process('L1',eras.Phase2_trigger)

process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mixNoPU_cfi')
process.load('Configuration.Geometry.GeometryExtended2023D17Reco_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.SimL1Emulator_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
process.load('L1Trigger.TrackFindingTracklet.L1TrackletTracks_cff')

process.load('Configuration.Geometry.GeometryExtended2023D17_cff')
process.load('Configuration.StandardSequences.Generator_cff')
process.load('IOMC.EventVertexGenerators.VtxSmearedHLLHC14TeV_cfi')
process.load('GeneratorInterface.Core.genFilterSummary_cff')
process.load('Configuration.StandardSequences.SimIdeal_cff')
process.load('Configuration.StandardSequences.Digi_cff')
process.load('Configuration.StandardSequences.DigiToRaw_cff')


process.MessageLogger.categories = cms.untracked.vstring('OfflineClusters', 'FwkReport')
process.MessageLogger.cerr.FwkReport = cms.untracked.PSet(
   reportEvery = cms.untracked.int32(1)
)

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100) )

#process.FEVTDEBUGHLToutput = cms.OutputModule("PoolOutputModule",
#    fileName = cms.untracked.string('file:test_reprocess.root'),
#    splitLevel = cms.untracked.int32(0)
#)


process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
	#'file:root://cms-xrd-global.cern.ch//store/mc/PhaseIIFall17D/SingleE_FlatPt-2to100/GEN-SIM-DIGI-RAW/L1TnoPU_93X_upgrade2023_realistic_v5-v1/80000/F85C33BB-A437-E811-BB7C-A4BF0112BE1C.root',
	#'file:root://cms-xrd-global.cern.ch//store/mc/PhaseIIFall17D/SinglePhoton_FlatPt-8to150/GEN-SIM-DIGI-RAW/L1TnoPU_93X_upgrade2023_realistic_v5-v1/30000/02C82A8F-1C39-E811-B20F-0CC47A4DEF3E.root',
	'file:root://cms-xrd-global.cern.ch//store/mc/PhaseIIFall17D/SingleNeutrino/GEN-SIM-DIGI-RAW/L1TPU200_93X_upgrade2023_realistic_v5-v1/80000/FEAC79F7-5B5C-E811-B830-0025905C2D9A.root',
        #'file:root://cms-xrd-global.cern.ch//store/mc/PhaseIIFall17D/SingleE_FlatPt-2to100/GEN-SIM-DIGI-RAW/L1TPU200_93X_upgrade2023_realistic_v5-v1/80000/FEEE84F9-EA37-E811-B2E7-141877638819.root',
	#'file:root://cms-xrd-global.cern.ch//store/mc/PhaseIIFall17D/SingleE_FlatPt-2to100/GEN-SIM-DIGI-RAW/L1TnoPU_93X_upgrade2023_realistic_v5-v1/80000/3C52D160-D237-E811-9301-002590FD5A52.root',

    ),
    inputCommands = cms.untracked.vstring(
        "keep *",
        "drop l1tEMTFHit2016Extras_simEmtfDigis_CSC_HLT",
        "drop l1tEMTFHit2016Extras_simEmtfDigis_RPC_HLT",
        "drop l1tEMTFHit2016s_simEmtfDigis__HLT",
        "drop l1tEMTFTrack2016Extras_simEmtfDigis__HLT",
        "drop l1tEMTFTrack2016s_simEmtfDigis__HLT",
        "drop l1tHGCalTowerMapBXVector_hgcalTriggerPrimitiveDigiProducer_towerMap_HLT",
    )

)

# All this stuff just runs the various EG algorithms that we are studying

from Configuration.AlCa.GlobalTag import GlobalTag
#process.GlobalTag = GlobalTag(process.GlobalTag, '100X_upgrade2023_realistic_v1', '')
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:phase2_realistic', '')

#process.load('SimCalorimetry.HcalTrigPrimProducers.hcaltpdigi_cff')
#process.load('CalibCalorimetry.CaloTPG.CaloTPGTranscoder_cfi')

#process.mix.digitizers = cms.PSet(process.theDigitizersValid)
#process.digitisation_step = cms.Path(process.pdigi_valid)

#process.load('L1Trigger.L1THGCal.hgcalTriggerPrimitives_cff')
#process.hgcl1tpg_step = cms.Path(process.hgcalTriggerPrimitives)

process.load('SimCalorimetry.EcalEBTrigPrimProducers.ecalEBTriggerPrimitiveDigis_cff')
process.EcalEBtp_step = cms.Path(process.simEcalEBTriggerPrimitiveDigis)

#process.TTClusterAssociatorFromPixelDigis.digiSimLinks          = cms.InputTag( "simSiPixelDigis","Tracker" )
process.L1TrackTrigger_step = cms.Path(process.L1TrackletTracksWithAssociators)

process.VertexProducer.l1TracksInputTag = cms.InputTag("TTTracksFromTracklet", "Level1TTTracks")

process.digitisation_step = cms.Path(process.pdigi_valid)
process.digi2raw_step = cms.Path(process.DigiToRaw)

# Path and EndPath definitions
process.L1simulation_step = cms.Path(process.phase2_SimL1Emulator)
process.endjob_step = cms.EndPath(process.endOfProcess)
#process.FEVTDEBUGHLToutput_step = cms.EndPath(process.FEVTDEBUGHLToutput)

# --------------------------------------------------------------------------------------------
#
# ----    Produce the L1EGCrystal clusters (code of Sasha Savin)

process.L1EGammaCrystalsEmulatorProducer = cms.EDProducer("L1EGCrystalClusterEmulatorProducer",
   ecalTPEB = cms.InputTag("simEcalEBTriggerPrimitiveDigis","","HLT"),
   hcalRecHit = cms.InputTag("hbhereco"),
   hcalTP = cms.InputTag("simHcalTriggerPrimitiveDigis","","HLT"),
   useTowerMap = cms.untracked.bool(False)
)

process.pSasha = cms.Path( process.L1EGammaCrystalsEmulatorProducer )

process.load("L1Trigger.L1TTrackMatch.L1TkElectronTrackProducer_cfi")
process.L1TkElectrons.L1TrackInputTag = cms.InputTag("TTTracksFromTracklet","Level1TTTracks" )
process.L1TkIsoElectrons.L1TrackInputTag = cms.InputTag("TTTracksFromTracklet","Level1TTTracks" )
process.L1TkElectrons.L1EGammaInputTag = cms.InputTag("L1EGammaCrystalsEmulatorProducer","L1EGammaCollectionBXVEmulator")
process.L1TkIsoElectrons.L1EGammaInputTag = cms.InputTag("L1EGammaCrystalsEmulatorProducer","L1EGammaCollectionBXVEmulator")

process.load("L1Trigger.L1TTrackMatch.L1WP2ElectronProducer_cfi")
process.L1WP2Electrons.L1TrackInputTag = cms.InputTag("TTTracksFromTracklet","Level1TTTracks" )
process.L1WP2Electrons.L1EGammaInputTag = cms.InputTag("L1EGammaCrystalsEmulatorProducer","L1EGammaCollectionBXVEmulator")
process.L1WP2Electrons.L1VertexInputTag = cms.InputTag("L1TkPrimaryVertex")

process.pElectrons = cms.Path( process.L1TkElectrons + process.L1TkIsoElectrons + process.L1WP2Electrons)

#process.load("L1Trigger.L1TTrackMatch.L1TkEmParticleProducer_cfi") 
from L1Trigger.L1TTrackMatch.L1TkEmParticleProducer_cfi import L1TkPhotons
process.L1TkPhotonsCrystalIsoLoose=L1TkPhotons.clone()
process.L1TkPhotonsCrystalIsoLoose.L1EGammaInputTag = cms.InputTag("L1EGammaCrystalsEmulatorProducer",   "L1EGammaCollectionBXVEmulator")
process.L1TkPhotonsCrystalIsoLoose.IsoCut = cms.double(0.23)
process.L1TkPhotonsCrystalIsoTight=L1TkPhotons.clone()
process.L1TkPhotonsCrystalIsoTight.L1EGammaInputTag = cms.InputTag("L1EGammaCrystalsEmulatorProducer",   "L1EGammaCollectionBXVEmulator")
process.L1TkPhotonsCrystalIsoTight.IsoCut = cms.double(0.1)
process.L1TkPhotonsCrystalIsoPV=L1TkPhotons.clone()
process.L1TkPhotonsCrystalIsoPV.L1EGammaInputTag = cms.InputTag("L1EGammaCrystalsEmulatorProducer",   "L1EGammaCollectionBXVEmulator")
process.L1TkPhotonsCrystalIsoPV.IsoCut = cms.double(0.1)
process.L1TkPhotonsCrystalIsoPV.PrimaryVtxConstrain = cms.bool( True )
process.L1TkPhotonsCrystalIsoPV.DeltaZMax = cms.double( 0.6 )    # in cm. Used only when PrimaryVtxConstrain = True
process.L1TkPhotonsCrystalIsoPV.L1VertexInputTag = cms.InputTag("L1TkPrimaryVertex") 

process.pPhotons = cms.Path( process.L1TkPhotonsCrystalIsoLoose + process.L1TkPhotonsCrystalIsoTight + process.L1TkPhotonsCrystalIsoPV)

# ----------------------------------------------------------------------------------------------
# 
# Analyzer starts here

process.analyzer = cms.EDAnalyzer('OfflineClusters',
   L1CrystalClustersInputTag = cms.InputTag("L1EGammaCrystalsEmulatorProducer","L1EGXtalClusterEmulator"),
   #L1CrystalClustersInputTag = cms.InputTag("L1EGammaCrystalsEmulatorProducer","L1EGammaCollectionBXVEmulator"),
   genParticles = cms.InputTag("genParticles","","HLT"),
   L1TrackInputTag = cms.InputTag("TTTracksFromTracklet", "Level1TTTracks"),
   L1TrackPrimaryVertexTag = cms.InputTag("L1TkPrimaryVertex"),
   Stage2EG1Tag = cms.InputTag("simCaloStage2Digis", "", "HLT"),
   Stage2TAU1Tag = cms.InputTag("simCaloStage2Digis", "", "HLT"),
   OfflineRecoClustersInputTag = cms.InputTag("correctedHybridSuperClusters"),
   ecalTPEB = cms.InputTag("simEcalEBTriggerPrimitiveDigis","","HLT"),
   L1TkElectronInputTag = cms.InputTag("L1TkElectrons","EG"),
   L1TkIsoElectronInputTag = cms.InputTag("L1TkIsoElectrons","EG"),
   L1WP2ElectronInputTag = cms.InputTag("L1WP2Electrons","EG"),
   L1TkPhotonsCrystalIsoLooseInputTag = cms.InputTag("L1TkPhotonsCrystalIsoLoose","EG"),
   L1TkPhotonsCrystalIsoTightInputTag = cms.InputTag("L1TkPhotonsCrystalIsoTight","EG"),
   L1TkPhotonsCrystalIsoPVInputTag = cms.InputTag("L1TkPhotonsCrystalIsoPV","EG"),
   doEfficiencyCalc = cms.untracked.bool(True),
   useOfflineClusters = cms.untracked.bool(False),
   useEndcap = cms.untracked.bool(False),
   doTracking = cms.untracked.bool(True),
   turnOnThresholds = cms.untracked.vint32(20, 30, 16),
   histogramBinCount = cms.untracked.int32(60),
   histogramRangeLow = cms.untracked.double(0),
   histogramRangeHigh = cms.untracked.double(50),
   histogramEtaBinCount = cms.untracked.int32(20),
   genMatchDeltaRcut = cms.untracked.double(0.25),
   genMatchRelPtcut = cms.untracked.double(0.5),
   debug = cms.untracked.bool(False)
)

process.panalyzer = cms.Path(process.analyzer)

process.TFileService = cms.Service("TFileService", 
   fileName = cms.string("out_offline_cecile.root"),
   closeFileFast = cms.untracked.bool(True)
)

