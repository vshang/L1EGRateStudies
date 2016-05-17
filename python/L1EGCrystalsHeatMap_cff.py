import FWCore.ParameterSet.Config as cms

L1EGCrystalsHeatMap = cms.EDAnalyzer('L1EGCrystalsHeatMap',
   L1CrystalClustersInputTag = cms.InputTag("L1EGammaCrystalsProducer","EGCrystalCluster"),
   L1EGammaOtherAlgs = cms.VInputTag(
   ),
   debug = cms.untracked.bool(False),
   useOfflineClusters = cms.untracked.bool(False),
   range = cms.untracked.int32(20),
   clusterPtCut = cms.untracked.double(15.)
)
