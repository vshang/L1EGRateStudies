import FWCore.ParameterSet.Config as cms

process = cms.Process("L1AlgoTest")

process.load('Configuration.StandardSequences.Services_cff')
process.load("FWCore.MessageService.MessageLogger_cfi")
process.load('Configuration.EventContent.EventContent_cff')
process.MessageLogger.categories = cms.untracked.vstring('L1EGRateStudies', 'FwkReport')
process.MessageLogger.cerr.FwkReport = cms.untracked.PSet(
   reportEvery = cms.untracked.int32(100)
)

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring($inputFileNames)
)

# All this stuff just runs the various EG algorithms that we are studying
                         
# ---- Global Tag :
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '90X_upgrade2023_realistic_v9', '')

# Choose a 2030 geometry!
process.load('Configuration.Geometry.GeometryExtended2023D4Reco_cff')
process.load('Configuration.StandardSequences.MagneticField_38T_PostLS1_cff')


# --------------------------------------------------------------------------------------------
#
# ----     L1 tracking

process.load("L1Trigger.TrackFindingTracklet.L1TrackletTracks_cff")
process.TTTracks = cms.Path(process.L1TrackletTracks)  #run only the tracking (no MC truth associators)

# ----     L1 tracking Primary Vertex
process.load("L1Trigger.L1TTrackMatch.L1TkPrimaryVertexProducer_cfi")
process.TTTrackPV = cms.Path(process.L1TkPrimaryVertex)



process.EcalTPSorterProducer = cms.EDProducer("EcalTPSorterProducer",
   tpsToKeep = cms.untracked.double(20),
   towerMapName = cms.untracked.string("newMap.json"),
   ecalTPEB = cms.InputTag("simEcalEBTriggerPrimitiveDigis","","HLT"),
)


# --------------------------------------------------------------------------------------------
#
# ----    Produce the L1EGCrystal clusters (code of Sasha Savin)

process.L1EGammaCrystalsProducer = cms.EDProducer("L1EGCrystalClusterProducer",
   EtminForStore = cms.double(0.),
   #EcalTpEtMin = cms.untracked.double(0.25), # 500 MeV default per each Ecal TP
   debug = cms.untracked.bool(False),
   useRecHits = cms.bool(False),
   #ecalTPEB = cms.InputTag("simEcalEBTriggerPrimitiveDigis","","HLT"),
   ecalTPEB = cms.InputTag("EcalTPSorterProducer","EcalTPsTopPerRegion","L1AlgoTest"),
   ecalRecHitEB = cms.InputTag("ecalRecHit","EcalRecHitsEB","RECO"),
   hcalRecHit = cms.InputTag("hbhereco"),
   hcalTP = cms.InputTag("simHcalTriggerPrimitiveDigis","","HLT"),
   useTowerMap = cms.untracked.bool(False)
   #useTowerMap = cms.untracked.bool(True),
   #towerMapName = cms.untracked.string("map170x15.json")
   #towerMapName = cms.untracked.string("map85x30.json")
)

process.pSasha = cms.Path( process.EcalTPSorterProducer + process.L1EGammaCrystalsProducer )


process.Out = cms.OutputModule( "PoolOutputModule",
    fileName = cms.untracked.string( "$outputFileName" ),
    fastCloning = cms.untracked.bool( False ),
    outputCommands = cms.untracked.vstring(
                    "keep *_L1EGammaCrystalsProducer_*_*",
                    "keep *_TTTracksFromTracklet_*_*",
                    "keep *_L1TkPrimaryVertex_*_*",
                    "keep *_genParticles_*_*",
                    "keep l1tEGammaBXVector_simCaloStage2Digis__HLT",
                    )
)

process.end = cms.EndPath( process.Out )

#dump_file = open("dump_file.py", "w")
#dump_file.write(process.dumpPython())


