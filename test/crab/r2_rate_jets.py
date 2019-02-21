import FWCore.ParameterSet.Config as cms

from Configuration.StandardSequences.Eras import eras

process = cms.Process("L1Jets2",eras.Phase2_trigger)

process.load('Configuration.StandardSequences.Services_cff')
process.load("FWCore.MessageService.MessageLogger_cfi")
process.load('Configuration.EventContent.EventContent_cff')
process.MessageLogger.categories = cms.untracked.vstring('L1EGRateStudies', 'FwkReport')
process.MessageLogger.cerr.FwkReport = cms.untracked.PSet(
   reportEvery = cms.untracked.int32(100)
)

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1000) )

process.source = cms.Source("PoolSource",
   fileNames = cms.untracked.vstring(
        'file:/data/truggles/l1CaloJets_20190220v2/MinBias/output_round1_10.root',
        'file:/data/truggles/l1CaloJets_20190220v2/MinBias/output_round1_100.root',
        #'file:/data/truggles/l1CaloJets_20190220v2/MinBias/output_round1_105.root',
        #'file:/data/truggles/l1CaloJets_20190220v2/MinBias/output_round1_11.root',
        #'file:/data/truggles/l1CaloJets_20190220v2/MinBias/output_round1_112.root',
        #'file:/data/truggles/l1CaloJets_20190220v2/MinBias/output_round1_117.root',
        #'file:/data/truggles/l1CaloJets_20190220v2/MinBias/output_round1_119.root',
        #'file:/data/truggles/l1CaloJets_20190220v2/MinBias/output_round1_12.root',
        #'file:/data/truggles/l1CaloJets_20190220v2/MinBias/output_round1_129.root',
        #'file:/data/truggles/l1CaloJets_20190220v2/MinBias/output_round1_13.root',
        #'file:/data/truggles/l1CaloJets_20190220v2/MinBias/output_round1_131.root',
        #'file:/data/truggles/l1CaloJets_20190220v2/MinBias/output_round1_137.root',
        #'file:/data/truggles/l1CaloJets_20190220v2/MinBias/output_round1_139.root',
        #'file:/data/truggles/l1CaloJets_20190220v2/MinBias/output_round1_14.root',
        #'file:/data/truggles/l1CaloJets_20190220v2/MinBias/output_round1_15.root',
        #'file:/data/truggles/l1CaloJets_20190220v2/MinBias/output_round1_16.root',
        #'file:/data/truggles/l1CaloJets_20190220v2/MinBias/output_round1_163.root',
        #'file:/data/truggles/l1CaloJets_20190220v2/MinBias/output_round1_17.root',
        #'file:/data/truggles/l1CaloJets_20190220v2/MinBias/output_round1_172.root',
        #'file:/data/truggles/l1CaloJets_20190220v2/MinBias/output_round1_18.root',
        #'file:/data/truggles/l1CaloJets_20190220v2/MinBias/output_round1_19.root',
        #'file:/data/truggles/l1CaloJets_20190220v2/MinBias/output_round1_22.root',
        #'file:/data/truggles/l1CaloJets_20190220v2/MinBias/output_round1_23.root',
        #'file:/data/truggles/l1CaloJets_20190220v2/MinBias/output_round1_25.root',
        #'file:/data/truggles/l1CaloJets_20190220v2/MinBias/output_round1_26.root',
        #'file:/data/truggles/l1CaloJets_20190220v2/MinBias/output_round1_27.root',
        #'file:/data/truggles/l1CaloJets_20190220v2/MinBias/output_round1_28.root',
        #'file:/data/truggles/l1CaloJets_20190220v2/MinBias/output_round1_29.root',
        #'file:/data/truggles/l1CaloJets_20190220v2/MinBias/output_round1_30.root',
        #'file:/data/truggles/l1CaloJets_20190220v2/MinBias/output_round1_32.root',
        #'file:/data/truggles/l1CaloJets_20190220v2/MinBias/output_round1_33.root',
        #'file:/data/truggles/l1CaloJets_20190220v2/MinBias/output_round1_35.root',
        #'file:/data/truggles/l1CaloJets_20190220v2/MinBias/output_round1_38.root',
        #'file:/data/truggles/l1CaloJets_20190220v2/MinBias/output_round1_39.root',
        #'file:/data/truggles/l1CaloJets_20190220v2/MinBias/output_round1_40.root',
        #'file:/data/truggles/l1CaloJets_20190220v2/MinBias/output_round1_41.root',
        #'file:/data/truggles/l1CaloJets_20190220v2/MinBias/output_round1_42.root',
        #'file:/data/truggles/l1CaloJets_20190220v2/MinBias/output_round1_43.root',
        #'file:/data/truggles/l1CaloJets_20190220v2/MinBias/output_round1_44.root',
        #'file:/data/truggles/l1CaloJets_20190220v2/MinBias/output_round1_45.root',
        #'file:/data/truggles/l1CaloJets_20190220v2/MinBias/output_round1_46.root',
        #'file:/data/truggles/l1CaloJets_20190220v2/MinBias/output_round1_47.root',
        #'file:/data/truggles/l1CaloJets_20190220v2/MinBias/output_round1_48.root',
        #'file:/data/truggles/l1CaloJets_20190220v2/MinBias/output_round1_49.root',
        #'file:/data/truggles/l1CaloJets_20190220v2/MinBias/output_round1_50.root',
        #'file:/data/truggles/l1CaloJets_20190220v2/MinBias/output_round1_51.root',
        #'file:/data/truggles/l1CaloJets_20190220v2/MinBias/output_round1_52.root',
        #'file:/data/truggles/l1CaloJets_20190220v2/MinBias/output_round1_53.root',
        #'file:/data/truggles/l1CaloJets_20190220v2/MinBias/output_round1_54.root',
        #'file:/data/truggles/l1CaloJets_20190220v2/MinBias/output_round1_55.root',
        #'file:/data/truggles/l1CaloJets_20190220v2/MinBias/output_round1_56.root',
        #'file:/data/truggles/l1CaloJets_20190220v2/MinBias/output_round1_57.root',
        #'file:/data/truggles/l1CaloJets_20190220v2/MinBias/output_round1_58.root',
        #'file:/data/truggles/l1CaloJets_20190220v2/MinBias/output_round1_59.root',
        #'file:/data/truggles/l1CaloJets_20190220v2/MinBias/output_round1_6.root',
        #'file:/data/truggles/l1CaloJets_20190220v2/MinBias/output_round1_60.root',
        #'file:/data/truggles/l1CaloJets_20190220v2/MinBias/output_round1_61.root',
        #'file:/data/truggles/l1CaloJets_20190220v2/MinBias/output_round1_62.root',
        #'file:/data/truggles/l1CaloJets_20190220v2/MinBias/output_round1_63.root',
        #'file:/data/truggles/l1CaloJets_20190220v2/MinBias/output_round1_64.root',
        #'file:/data/truggles/l1CaloJets_20190220v2/MinBias/output_round1_65.root',
        #'file:/data/truggles/l1CaloJets_20190220v2/MinBias/output_round1_66.root',
        #'file:/data/truggles/l1CaloJets_20190220v2/MinBias/output_round1_67.root',
        #'file:/data/truggles/l1CaloJets_20190220v2/MinBias/output_round1_68.root',
        #'file:/data/truggles/l1CaloJets_20190220v2/MinBias/output_round1_7.root',
        #'file:/data/truggles/l1CaloJets_20190220v2/MinBias/output_round1_70.root',
        #'file:/data/truggles/l1CaloJets_20190220v2/MinBias/output_round1_77.root',
        #'file:/data/truggles/l1CaloJets_20190220v2/MinBias/output_round1_8.root',
        #'file:/data/truggles/l1CaloJets_20190220v2/MinBias/output_round1_9.root',
        #'file:/data/truggles/l1CaloJets_20190220v2/MinBias/output_round1_94.root',
        #'file:/data/truggles/l1CaloJets_20190220v2/MinBias/output_round1_95.root',
    ),
   dropDescendantsOfDroppedBranches=cms.untracked.bool(False),
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
    doRate = cms.untracked.bool(True),
    Stage2JetTag = cms.InputTag("simCaloStage2Digis", "MP", "HLT"),
    Stage2TauTag = cms.InputTag("simCaloStage2Digis", "MP", "HLT"),
    puSrc = cms.InputTag("addPileupInfo")
)

process.panalyzer = cms.Path(process.analyzer)



process.TFileService = cms.Service("TFileService", 
   fileName = cms.string( "output_round2_rate.root" ), 
   closeFileFast = cms.untracked.bool(True)
)



#dump_file = open("dump_file.py", "w")
#dump_file.write(process.dumpPython())


