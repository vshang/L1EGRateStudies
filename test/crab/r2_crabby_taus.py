import FWCore.ParameterSet.Config as cms

from Configuration.StandardSequences.Eras import eras

#process = cms.Process('L1Jets2',eras.Phase2C9)
process = cms.Process('L1Jets2',eras.Phase2C17I13M9)
process.load('Configuration.StandardSequences.Services_cff')
process.load("FWCore.MessageService.MessageLogger_cfi")
process.load('Configuration.EventContent.EventContent_cff')
#process.load('Configuration.Geometry.GeometryExtended2026D49Reco_cff')
#process.load('Configuration.Geometry.GeometryExtended2026D49_cff')
process.load('Configuration.Geometry.GeometryExtended2026D88Reco_cff')
process.load('Configuration.Geometry.GeometryExtended2026D88_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.MessageLogger.L1CaloJetStudies = dict()
process.MessageLogger.cerr.FwkReport = cms.untracked.PSet(
   reportEvery = cms.untracked.int32(100)
)

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(100000) )

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        'file:./output_round1.root',
    ),
    dropDescendantsOfDroppedBranches=cms.untracked.bool(False),
)

out_path = '/afs/hep.wisc.edu/home/vshang/public/Phase2L1CaloTaus/CMSSW_12_5_2_patch1/src/L1Trigger/L1EGRateStudies/test/crab/l1CaloTaus_r2_CMSSW_12_5_2_patch1/20230913/'
#name = "HiggsTauTauvL1EGs"
#name = "HiggsTauTau"
name = "VBFHiggsTauTau1x3"
#name = "minBias1x3"
# Load samples from external files here:
from L1Trigger.L1EGRateStudies.loadRound2Files import getSampleFiles
process.source.fileNames = getSampleFiles( name )


# All this stuff just runs the various EG algorithms that we are studying
                         
# ---- Global Tag :
from Configuration.AlCa.GlobalTag import GlobalTag
#process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:phase2_realistic', '') 
#process.GlobalTag = GlobalTag(process.GlobalTag, '123X_mcRun4_realistic_v3', '')
process.GlobalTag = GlobalTag(process.GlobalTag, '125X_mcRun4_realistic_v2', '') 


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

#process.analyzer = cms.EDAnalyzer('L1CaloJetStudies',
#    L1CaloJetsInputTag = cms.InputTag("l1tCaloJetProducer","L1CaloJetsNoCuts"),
process.analyzer = cms.EDAnalyzer('L1GCTJetStudies',
    GCTJetsInputTag = cms.InputTag("l1tPhase2CaloJetEmulator","GCTJet"),
    genJets = cms.InputTag("ak4GenJetsNoNu", "", "HLT"),
    genHadronicTauSrc = cms.InputTag("tauGenJetsSelectorAllHadrons"),
    genMatchDeltaRcut = cms.untracked.double(0.3),
    genMatchRelPtcut = cms.untracked.double(0.5),
    debug = cms.untracked.bool(False),
    doRate = cms.untracked.bool(False),
    use_gen_taus = cms.untracked.bool(True),
    Stage2JetTag = cms.InputTag("simCaloStage2Digis", "MP", "HLT"),
    Stage2TauTag = cms.InputTag("simCaloStage2Digis", "MP", "HLT"),
    puSrc = cms.InputTag("addPileupInfo")
)

if ("minBias" in name):
    process.analyzer.doRate = cms.untracked.bool(True)

process.panalyzer = cms.Path(process.analyzer)



process.TFileService = cms.Service("TFileService", 
    fileName = cms.string( out_path+"output_round2_"+name+".root" ),
    closeFileFast = cms.untracked.bool(True)
)



#dump_file = open("dump_file.py", "w")
#dump_file.write(process.dumpPython())
