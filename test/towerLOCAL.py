import FWCore.ParameterSet.Config as cms

from Configuration.StandardSequences.Eras import eras

process = cms.Process("L1AlgoTest",eras.Phase2_trigger)

#from CalibCalorimetry.CaloTPG.CaloTPGTranscoder_cfi import *

process.load('Configuration.StandardSequences.Services_cff')
process.load("FWCore.MessageService.MessageLogger_cfi")
process.load('Configuration.EventContent.EventContent_cff')
process.MessageLogger.categories = cms.untracked.vstring('L1EGRateStudies', 'FwkReport')
process.MessageLogger.cerr.FwkReport = cms.untracked.PSet(
   reportEvery = cms.untracked.int32(100)
)

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(50) )

process.source = cms.Source("PoolSource",
    # Set to do test run on official Phase-2 L1T Ntuples
    #/GluGluHToTauTau_M125_14TeV_powheg_pythia8/PhaseIIFall17D-L1TnoPU_93X_upgrade2023_realistic_v5-v1/GEN-SIM-DIGI-RAW
    #/store/mc/PhaseIIFall17D/GluGluHToTauTau_M125_14TeV_powheg_pythia8/GEN-SIM-DIGI-RAW/L1TnoPU_93X_upgrade2023_realistic_v5-v1/00000/00C160E6-6A39-E811-B904-008CFA152144.root
    #
    #/QCD_Pt-0to1000_Tune4C_14TeV_pythia8/PhaseIIFall17D-L1TnoPU_93X_upgrade2023_realistic_v5-v1/GEN-SIM-DIGI-RAW
    #/store/mc/PhaseIIFall17D/QCD_Pt-0to1000_Tune4C_14TeV_pythia8/GEN-SIM-DIGI-RAW/L1TnoPU_93X_upgrade2023_realistic_v5-v1/00000/02AE7A07-2339-E811-B98B-E0071B7AC750.root
    #
    #/WJetsToLNu_TuneCUETP8M1_14TeV-madgraphMLM-pythia8/PhaseIIFall17D-L1TnoPU_93X_upgrade2023_realistic_v5-v3/GEN-SIM-DIGI-RAW
    #/store/mc/PhaseIIFall17D/WJetsToLNu_TuneCUETP8M1_14TeV-madgraphMLM-pythia8/GEN-SIM-DIGI-RAW/L1TnoPU_93X_upgrade2023_realistic_v5-v3/30000/162DC63A-C458-E811-92E1-B083FED42FAF.root

    #fileNames = cms.untracked.vstring('file:root://cms-xrd-global.cern.ch//store/mc/PhaseIIFall17D/SingleE_FlatPt-2to100/GEN-SIM-DIGI-RAW/L1TPU200_93X_upgrade2023_realistic_v5-v1/80000/C0F55AFC-1638-E811-9A14-EC0D9A8221EE.root'),
    #fileNames = cms.untracked.vstring('file:root://cms-xrd-global.cern.ch//store/mc/PhaseIIFall17D/QCD_Pt-0to1000_Tune4C_14TeV_pythia8/GEN-SIM-DIGI-RAW/L1TnoPU_93X_upgrade2023_realistic_v5-v1/00000/02AE7A07-2339-E811-B98B-E0071B7AC750.root'),
    #fileNames = cms.untracked.vstring('file:root://cms-xrd-global.cern.ch//store/mc/PhaseIIFall17D/GluGluHToTauTau_M125_14TeV_powheg_pythia8/GEN-SIM-DIGI-RAW/L1TnoPU_93X_upgrade2023_realistic_v5-v1/00000/00C160E6-6A39-E811-B904-008CFA152144.root'),
    #fileNames = cms.untracked.vstring('file:root://cms-xrd-global.cern.ch//store/mc/PhaseIIFall17D/QCD_Pt-0to1000_Tune4C_14TeV_pythia8/GEN-SIM-DIGI-RAW/L1TPU200_93X_upgrade2023_realistic_v5-v1/00000/EEC3EC7E-C537-E811-9954-E0071B73C650.root'),

    fileNames = cms.untracked.vstring('file:/eos/cms/store/group/dpg_trigger/comm_trigger/L1Trigger/bundocka/ttbarPU200/ttbarPU200_10_5_0_rep.root'),
    #fileNames = cms.untracked.vstring('file:root://cms-xrd-global.cern.ch//store/mc/PhaseIIFall17D/QCD_Pt-0to1000_Tune4C_14TeV_pythia8/GEN-SIM-DIGI-RAW/L1TPU200_93X_upgrade2023_realistic_v5-v1/00000/C072C4FC-DF37-E811-8A20-E0071B6C9DD0.root'),

    #fileNames = cms.untracked.vstring('file:/hdfs/store/mc/PhaseIIFall17D/QCD_Pt-0to1000_Tune4C_14TeV_pythia8/GEN-SIM-DIGI-RAW/L1TnoPU_93X_upgrade2023_realistic_v5-v1/00000/9C33F8F2-5D39-E811-8987-0025904C7FC2.root'),
    #fileNames = cms.untracked.vstring('file:root://cms-xrd-global.cern.ch//store/mc/PhaseIIFall17D/SingleNeutrino/GEN-SIM-DIGI-RAW/L1TPU200_93X_upgrade2023_realistic_v5-v1/80000/C2AEC8C0-695C-E811-ABAD-0CC47AF9B496.root'),
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
    # Choosen settings (v8 24 Jan 2019)
    HcalTpEtMin = cms.double(0.0), # Default is 0.5 GeV
    EcalTpEtMin = cms.double(0.0), # Default is 0.5 GeV
    HGCalHadTpEtMin = cms.double(0.25),
    HGCalEmTpEtMin = cms.double(0.25),
    HFTpEtMin = cms.double(0.5),
    puThreshold = cms.double(5.0), # Default is 5 GeV
    puThresholdEcal = cms.double(2.0), # Default is 5 GeV
    puThresholdHcal = cms.double(3.0), # Default is 5 GeV
    puThresholdL1eg = cms.double(4.0), # Default is 5 GeV
    puThresholdHGCalEMMin = cms.double(1.0), # Default is 5 GeV
    puThresholdHGCalEMMax = cms.double(1.5), # Default is 5 GeV
    puThresholdHGCalHadMin = cms.double(0.5), # Default is 5 GeV
    puThresholdHGCalHadMax = cms.double(1.0), # Default is 5 GeV
    puThresholdHFMin = cms.double(4.0), # Default is 5 GeV
    puThresholdHFMax = cms.double(10.0), # Default is 5 GeV
    debug = cms.bool(False),
    #debug = cms.bool(True),
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
   fileName = cms.string("_towerOutputFileName.root"), 
   closeFileFast = cms.untracked.bool(True)
)



#dump_file = open("dump_file.py", "w")
#dump_file.write(process.dumpPython())


