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
        'file:/data/truggles/l1CaloJets_20190220v2/TTbar/output_round1_1.root',
        'file:/data/truggles/l1CaloJets_20190220v2/TTbar/output_round1_10.root',
        'file:/data/truggles/l1CaloJets_20190220v2/TTbar/output_round1_11.root',
        'file:/data/truggles/l1CaloJets_20190220v2/TTbar/output_round1_12.root',
        'file:/data/truggles/l1CaloJets_20190220v2/TTbar/output_round1_13.root',
        'file:/data/truggles/l1CaloJets_20190220v2/TTbar/output_round1_14.root',
        'file:/data/truggles/l1CaloJets_20190220v2/TTbar/output_round1_15.root',
        'file:/data/truggles/l1CaloJets_20190220v2/TTbar/output_round1_16.root',
        'file:/data/truggles/l1CaloJets_20190220v2/TTbar/output_round1_17.root',
        'file:/data/truggles/l1CaloJets_20190220v2/TTbar/output_round1_18.root',
        'file:/data/truggles/l1CaloJets_20190220v2/TTbar/output_round1_19.root',
        'file:/data/truggles/l1CaloJets_20190220v2/TTbar/output_round1_2.root',
        'file:/data/truggles/l1CaloJets_20190220v2/TTbar/output_round1_20.root',
        'file:/data/truggles/l1CaloJets_20190220v2/TTbar/output_round1_21.root',
        'file:/data/truggles/l1CaloJets_20190220v2/TTbar/output_round1_22.root',
        'file:/data/truggles/l1CaloJets_20190220v2/TTbar/output_round1_24.root',
        'file:/data/truggles/l1CaloJets_20190220v2/TTbar/output_round1_25.root',
        'file:/data/truggles/l1CaloJets_20190220v2/TTbar/output_round1_26.root',
        'file:/data/truggles/l1CaloJets_20190220v2/TTbar/output_round1_27.root',
        'file:/data/truggles/l1CaloJets_20190220v2/TTbar/output_round1_28.root',
        'file:/data/truggles/l1CaloJets_20190220v2/TTbar/output_round1_29.root',
        'file:/data/truggles/l1CaloJets_20190220v2/TTbar/output_round1_3.root',
        'file:/data/truggles/l1CaloJets_20190220v2/TTbar/output_round1_30.root',
        'file:/data/truggles/l1CaloJets_20190220v2/TTbar/output_round1_31.root',
        'file:/data/truggles/l1CaloJets_20190220v2/TTbar/output_round1_32.root',
        'file:/data/truggles/l1CaloJets_20190220v2/TTbar/output_round1_33.root',
        'file:/data/truggles/l1CaloJets_20190220v2/TTbar/output_round1_34.root',
        'file:/data/truggles/l1CaloJets_20190220v2/TTbar/output_round1_35.root',
        'file:/data/truggles/l1CaloJets_20190220v2/TTbar/output_round1_36.root',
        'file:/data/truggles/l1CaloJets_20190220v2/TTbar/output_round1_39.root',
        'file:/data/truggles/l1CaloJets_20190220v2/TTbar/output_round1_4.root',
        'file:/data/truggles/l1CaloJets_20190220v2/TTbar/output_round1_41.root',
        'file:/data/truggles/l1CaloJets_20190220v2/TTbar/output_round1_42.root',
        'file:/data/truggles/l1CaloJets_20190220v2/TTbar/output_round1_43.root',
        'file:/data/truggles/l1CaloJets_20190220v2/TTbar/output_round1_5.root',
        'file:/data/truggles/l1CaloJets_20190220v2/TTbar/output_round1_6.root',
        'file:/data/truggles/l1CaloJets_20190220v2/TTbar/output_round1_7.root',
        'file:/data/truggles/l1CaloJets_20190220v2/TTbar/output_round1_8.root',
        'file:/data/truggles/l1CaloJets_20190220v2/TTbar/output_round1_9.root',

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


process.pL1Objs = cms.Path( 
    process.tauGenJets *
    process.tauGenJetsSelectorAllHadrons
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
   fileName = cms.string( "output_round2_eff_hists.root" ), 
   closeFileFast = cms.untracked.bool(True)
)



#dump_file = open("dump_file.py", "w")
#dump_file.write(process.dumpPython())


