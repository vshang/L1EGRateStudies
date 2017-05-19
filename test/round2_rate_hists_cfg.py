import FWCore.ParameterSet.Config as cms

process = cms.Process("L1AlgoAnalysis")

process.load('Configuration.StandardSequences.Services_cff')
process.load("FWCore.MessageService.MessageLogger_cfi")
process.load('Configuration.EventContent.EventContent_cff')
process.MessageLogger.categories = cms.untracked.vstring('L1EGRateStudies', 'FwkReport')
process.MessageLogger.cerr.FwkReport = cms.untracked.PSet(
   reportEvery = cms.untracked.int32(100)
)

process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(-1) )
#process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(10) )

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(
        #'file:l1egCrystalTest.root',
        'file:/data/truggles/phaseII_minBias_20170518v3-round1_condor_cfg/round1_condor_cfg-00085E3E-8326-E711-9EFA-0242AC130003/round1_condor_cfg-00085E3E-8326-E711-9EFA-0242AC130003.root',
        'file:/data/truggles/phaseII_minBias_20170518v3-round1_condor_cfg/round1_condor_cfg-000A0719-1127-E711-890D-0242AC130004/round1_condor_cfg-000A0719-1127-E711-890D-0242AC130004.root',
        'file:/data/truggles/phaseII_minBias_20170518v3-round1_condor_cfg/round1_condor_cfg-002C4C3E-CB26-E711-BFEB-0242AC130003/round1_condor_cfg-002C4C3E-CB26-E711-BFEB-0242AC130003.root',
        'file:/data/truggles/phaseII_minBias_20170518v3-round1_condor_cfg/round1_condor_cfg-0054D10B-C129-E711-B9FF-0242AC130009/round1_condor_cfg-0054D10B-C129-E711-B9FF-0242AC130009.root',
        'file:/data/truggles/phaseII_minBias_20170518v3-round1_condor_cfg/round1_condor_cfg-0A14112B-D528-E711-8E19-0242AC130005/round1_condor_cfg-0A14112B-D528-E711-8E19-0242AC130005.root',
        'file:/data/truggles/phaseII_minBias_20170518v3-round1_condor_cfg/round1_condor_cfg-0AF7A1DD-6026-E711-A92F-0242AC130002/round1_condor_cfg-0AF7A1DD-6026-E711-A92F-0242AC130002.root',
        'file:/data/truggles/phaseII_minBias_20170518v3-round1_condor_cfg/round1_condor_cfg-0C20D2A9-7526-E711-A629-0242AC130004/round1_condor_cfg-0C20D2A9-7526-E711-A629-0242AC130004.root',
        'file:/data/truggles/phaseII_minBias_20170518v3-round1_condor_cfg/round1_condor_cfg-0C4BB981-F525-E711-B0A5-0242AC130002/round1_condor_cfg-0C4BB981-F525-E711-B0A5-0242AC130002.root',
        'file:/data/truggles/phaseII_minBias_20170518v3-round1_condor_cfg/round1_condor_cfg-1878382C-8326-E711-A612-0242AC130002/round1_condor_cfg-1878382C-8326-E711-A612-0242AC130002.root',
        'file:/data/truggles/phaseII_minBias_20170518v3-round1_condor_cfg/round1_condor_cfg-189A1C1E-E526-E711-AF91-0242AC130002/round1_condor_cfg-189A1C1E-E526-E711-AF91-0242AC130002.root',
        'file:/data/truggles/phaseII_minBias_20170518v3-round1_condor_cfg/round1_condor_cfg-242F118C-E626-E711-8B14-0242AC130006/round1_condor_cfg-242F118C-E626-E711-8B14-0242AC130006.root',
        'file:/data/truggles/phaseII_minBias_20170518v3-round1_condor_cfg/round1_condor_cfg-265127B5-5428-E711-9853-0242AC130003/round1_condor_cfg-265127B5-5428-E711-9853-0242AC130003.root',
        'file:/data/truggles/phaseII_minBias_20170518v3-round1_condor_cfg/round1_condor_cfg-26AE33AD-8126-E711-97A2-0242AC130009/round1_condor_cfg-26AE33AD-8126-E711-97A2-0242AC130009.root',
        'file:/data/truggles/phaseII_minBias_20170518v3-round1_condor_cfg/round1_condor_cfg-3035999D-D626-E711-9CF7-0242AC130002/round1_condor_cfg-3035999D-D626-E711-9CF7-0242AC130002.root',
        'file:/data/truggles/phaseII_minBias_20170518v3-round1_condor_cfg/round1_condor_cfg-34B697BE-7326-E711-81C1-0242AC130005/round1_condor_cfg-34B697BE-7326-E711-81C1-0242AC130005.root',
        'file:/data/truggles/phaseII_minBias_20170518v3-round1_condor_cfg/round1_condor_cfg-3A801DF0-B926-E711-A1C0-0242AC130004/round1_condor_cfg-3A801DF0-B926-E711-A1C0-0242AC130004.root',
        'file:/data/truggles/phaseII_minBias_20170518v3-round1_condor_cfg/round1_condor_cfg-42FA0F76-E028-E711-B856-0242AC130006/round1_condor_cfg-42FA0F76-E028-E711-B856-0242AC130006.root',
        'file:/data/truggles/phaseII_minBias_20170518v3-round1_condor_cfg/round1_condor_cfg-4A97A7E1-7626-E711-A748-0242AC130002/round1_condor_cfg-4A97A7E1-7626-E711-A748-0242AC130002.root',
        'file:/data/truggles/phaseII_minBias_20170518v3-round1_condor_cfg/round1_condor_cfg-4E0FE7E5-8B29-E711-A65B-0242AC130002/round1_condor_cfg-4E0FE7E5-8B29-E711-A65B-0242AC130002.root',
        'file:/data/truggles/phaseII_minBias_20170518v3-round1_condor_cfg/round1_condor_cfg-5269F743-AE26-E711-8C58-0242AC130002/round1_condor_cfg-5269F743-AE26-E711-8C58-0242AC130002.root',
        'file:/data/truggles/phaseII_minBias_20170518v3-round1_condor_cfg/round1_condor_cfg-54AF2085-A626-E711-8EB2-0242AC130004/round1_condor_cfg-54AF2085-A626-E711-8EB2-0242AC130004.root',
        'file:/data/truggles/phaseII_minBias_20170518v3-round1_condor_cfg/round1_condor_cfg-5EFF6561-D526-E711-9937-0242AC130004/round1_condor_cfg-5EFF6561-D526-E711-9937-0242AC130004.root',
        'file:/data/truggles/phaseII_minBias_20170518v3-round1_condor_cfg/round1_condor_cfg-640FBD0C-5926-E711-AA4A-0242AC130002/round1_condor_cfg-640FBD0C-5926-E711-AA4A-0242AC130002.root',
        'file:/data/truggles/phaseII_minBias_20170518v3-round1_condor_cfg/round1_condor_cfg-6449BB45-6F26-E711-8C7A-0242AC130002/round1_condor_cfg-6449BB45-6F26-E711-8C7A-0242AC130002.root',
        'file:/data/truggles/phaseII_minBias_20170518v3-round1_condor_cfg/round1_condor_cfg-68C064E5-6228-E711-87DE-0242AC130002/round1_condor_cfg-68C064E5-6228-E711-87DE-0242AC130002.root',
        'file:/data/truggles/phaseII_minBias_20170518v3-round1_condor_cfg/round1_condor_cfg-6CB1D6F6-F625-E711-AB37-0242AC130002/round1_condor_cfg-6CB1D6F6-F625-E711-AB37-0242AC130002.root',
        'file:/data/truggles/phaseII_minBias_20170518v3-round1_condor_cfg/round1_condor_cfg-6EFC382D-8426-E711-8D6C-0242AC130002/round1_condor_cfg-6EFC382D-8426-E711-8D6C-0242AC130002.root',
        'file:/data/truggles/phaseII_minBias_20170518v3-round1_condor_cfg/round1_condor_cfg-70AFE1BC-5F26-E711-A838-0242AC130002/round1_condor_cfg-70AFE1BC-5F26-E711-A838-0242AC130002.root',
        'file:/data/truggles/phaseII_minBias_20170518v3-round1_condor_cfg/round1_condor_cfg-7895ECE3-C626-E711-B93D-0242AC130006/round1_condor_cfg-7895ECE3-C626-E711-B93D-0242AC130006.root',
        'file:/data/truggles/phaseII_minBias_20170518v3-round1_condor_cfg/round1_condor_cfg-7C63EACA-6526-E711-984E-0242AC130005/round1_condor_cfg-7C63EACA-6526-E711-984E-0242AC130005.root',
        'file:/data/truggles/phaseII_minBias_20170518v3-round1_condor_cfg/round1_condor_cfg-7E07C11C-8326-E711-8A60-0242AC130003/round1_condor_cfg-7E07C11C-8326-E711-8A60-0242AC130003.root',
        'file:/data/truggles/phaseII_minBias_20170518v3-round1_condor_cfg/round1_condor_cfg-849F46A4-AF26-E711-AC5F-0242AC130003/round1_condor_cfg-849F46A4-AF26-E711-AC5F-0242AC130003.root',
        'file:/data/truggles/phaseII_minBias_20170518v3-round1_condor_cfg/round1_condor_cfg-86E50E63-E625-E711-B52A-0242AC130006/round1_condor_cfg-86E50E63-E625-E711-B52A-0242AC130006.root',
        'file:/data/truggles/phaseII_minBias_20170518v3-round1_condor_cfg/round1_condor_cfg-8823BA03-8226-E711-9F4A-0242AC130002/round1_condor_cfg-8823BA03-8226-E711-9F4A-0242AC130002.root',
        'file:/data/truggles/phaseII_minBias_20170518v3-round1_condor_cfg/round1_condor_cfg-9031D477-0027-E711-BC32-0242AC130002/round1_condor_cfg-9031D477-0027-E711-BC32-0242AC130002.root',
        'file:/data/truggles/phaseII_minBias_20170518v3-round1_condor_cfg/round1_condor_cfg-90D45655-D526-E711-83C0-0242AC130005/round1_condor_cfg-90D45655-D526-E711-83C0-0242AC130005.root',
        'file:/data/truggles/phaseII_minBias_20170518v3-round1_condor_cfg/round1_condor_cfg-923416E7-6D26-E711-9BD2-0242AC130002/round1_condor_cfg-923416E7-6D26-E711-9BD2-0242AC130002.root',
        'file:/data/truggles/phaseII_minBias_20170518v3-round1_condor_cfg/round1_condor_cfg-9CA3586A-D228-E711-BED7-0242AC130004/round1_condor_cfg-9CA3586A-D228-E711-BED7-0242AC130004.root',
        'file:/data/truggles/phaseII_minBias_20170518v3-round1_condor_cfg/round1_condor_cfg-9E102117-BE26-E711-A65E-0242AC130002/round1_condor_cfg-9E102117-BE26-E711-A65E-0242AC130002.root',
        'file:/data/truggles/phaseII_minBias_20170518v3-round1_condor_cfg/round1_condor_cfg-A06E0094-7A26-E711-96CF-0242AC130005/round1_condor_cfg-A06E0094-7A26-E711-96CF-0242AC130005.root',
        'file:/data/truggles/phaseII_minBias_20170518v3-round1_condor_cfg/round1_condor_cfg-AC299390-7426-E711-BC9B-0242AC130005/round1_condor_cfg-AC299390-7426-E711-BC9B-0242AC130005.root',
        'file:/data/truggles/phaseII_minBias_20170518v3-round1_condor_cfg/round1_condor_cfg-AEA14C19-E526-E711-9A64-0242AC130002/round1_condor_cfg-AEA14C19-E526-E711-9A64-0242AC130002.root',
        'file:/data/truggles/phaseII_minBias_20170518v3-round1_condor_cfg/round1_condor_cfg-BC05B991-AC26-E711-B098-0242AC130002/round1_condor_cfg-BC05B991-AC26-E711-B098-0242AC130002.root',
        'file:/data/truggles/phaseII_minBias_20170518v3-round1_condor_cfg/round1_condor_cfg-BC9769A1-D726-E711-BA76-0242AC130004/round1_condor_cfg-BC9769A1-D726-E711-BA76-0242AC130004.root',
        'file:/data/truggles/phaseII_minBias_20170518v3-round1_condor_cfg/round1_condor_cfg-C6F407C6-E228-E711-B1B4-0242AC130002/round1_condor_cfg-C6F407C6-E228-E711-B1B4-0242AC130002.root',
        'file:/data/truggles/phaseII_minBias_20170518v3-round1_condor_cfg/round1_condor_cfg-C8ABF6C0-7926-E711-B2B1-0242AC130002/round1_condor_cfg-C8ABF6C0-7926-E711-B2B1-0242AC130002.root',
        'file:/data/truggles/phaseII_minBias_20170518v3-round1_condor_cfg/round1_condor_cfg-CA5FC952-E626-E711-9244-0242AC130003/round1_condor_cfg-CA5FC952-E626-E711-9244-0242AC130003.root',
        'file:/data/truggles/phaseII_minBias_20170518v3-round1_condor_cfg/round1_condor_cfg-D208A9E7-032A-E711-9AAF-0242AC130002/round1_condor_cfg-D208A9E7-032A-E711-9AAF-0242AC130002.root',
        'file:/data/truggles/phaseII_minBias_20170518v3-round1_condor_cfg/round1_condor_cfg-D609D6AB-5226-E711-8A50-0242AC130002/round1_condor_cfg-D609D6AB-5226-E711-8A50-0242AC130002.root',
        'file:/data/truggles/phaseII_minBias_20170518v3-round1_condor_cfg/round1_condor_cfg-D6E919E9-DC26-E711-A690-0242AC130002/round1_condor_cfg-D6E919E9-DC26-E711-A690-0242AC130002.root',
        'file:/data/truggles/phaseII_minBias_20170518v3-round1_condor_cfg/round1_condor_cfg-D8E14EE6-7E26-E711-9CD5-0242AC130003/round1_condor_cfg-D8E14EE6-7E26-E711-9CD5-0242AC130003.root',
        'file:/data/truggles/phaseII_minBias_20170518v3-round1_condor_cfg/round1_condor_cfg-E2D807F9-032A-E711-A2C5-0242AC130003/round1_condor_cfg-E2D807F9-032A-E711-A2C5-0242AC130003.root',
        'file:/data/truggles/phaseII_minBias_20170518v3-round1_condor_cfg/round1_condor_cfg-E2DBFB20-7526-E711-AD89-0242AC130002/round1_condor_cfg-E2DBFB20-7526-E711-AD89-0242AC130002.root',
        'file:/data/truggles/phaseII_minBias_20170518v3-round1_condor_cfg/round1_condor_cfg-E4157048-CA26-E711-8568-0242AC130003/round1_condor_cfg-E4157048-CA26-E711-8568-0242AC130003.root',
        'file:/data/truggles/phaseII_minBias_20170518v3-round1_condor_cfg/round1_condor_cfg-E461640B-5926-E711-B841-0242AC130002/round1_condor_cfg-E461640B-5926-E711-B841-0242AC130002.root',
        'file:/data/truggles/phaseII_minBias_20170518v3-round1_condor_cfg/round1_condor_cfg-F02765B8-6A26-E711-B40F-0242AC130003/round1_condor_cfg-F02765B8-6A26-E711-B40F-0242AC130003.root',
        'file:/data/truggles/phaseII_minBias_20170518v3-round1_condor_cfg/round1_condor_cfg-F088EB44-AB26-E711-ABBA-0242AC130002/round1_condor_cfg-F088EB44-AB26-E711-ABBA-0242AC130002.root',
        'file:/data/truggles/phaseII_minBias_20170518v3-round1_condor_cfg/round1_condor_cfg-F2047B3E-DB26-E711-946C-0242AC130003/round1_condor_cfg-F2047B3E-DB26-E711-946C-0242AC130003.root', 
    )
)

# All this stuff just runs the various EG algorithms that we are studying
                         
# ---- Global Tag :
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, '90X_upgrade2023_realistic_v9', '')

# Choose a 2030 geometry!
# The ones which don't work all replace the ECAL Endcap geometry with HGCal stuff
# Options in cmssw_810_pre16: (each also has an option without the Reco)
process.load('Configuration.Geometry.GeometryExtended2023D4Reco_cff') # D7 works, D4 is the choosen config by Phase-2 L1Trig


process.load('Configuration.StandardSequences.MagneticField_38T_PostLS1_cff')




# -------------------------------------------------------------------------------------------
#
### Mini-analyzer for L1EG TPs
process.TPAnalyzer = cms.EDAnalyzer('L1EGPreclusterAnalysis',
   L1CrystalClustersInputTag = cms.InputTag("L1EGammaCrystalsProducer","L1EGXtalClusterNoCuts"),
   L1CrystalClustersWithCutsInputTag = cms.InputTag("L1EGammaCrystalsProducer","L1EGXtalClusterWithCuts")
)

# ----------------------------------------------------------------------------------------------
# 
# Analyzer starts here

process.analyzer = cms.EDAnalyzer('L1EGRateStudies',
   L1CrystalClustersInputTag = cms.InputTag("L1EGammaCrystalsProducer","L1EGXtalClusterNoCuts"),
   genParticles = cms.InputTag("genParticles"),
   L1TrackInputTag = cms.InputTag("TTTracksFromTracklet", "Level1TTTracks"),
   L1TrackPrimaryVertexTag = cms.InputTag("L1TkPrimaryVertex"),
   Stage2EG1Tag = cms.InputTag("simCaloStage2Digis", "", "HLT"),
   #OfflineRecoClustersInputTag = cms.InputTag("correctedHybridSuperClusters"),
   #ecalTPEB = cms.InputTag("simEcalEBTriggerPrimitiveDigis","","HLT"),
   doEfficiencyCalc = cms.untracked.bool(False),
   useOfflineClusters = cms.untracked.bool(False),
   useEndcap = cms.untracked.bool(False),
   doTracking = cms.untracked.bool(True),
   #turnOnThresholds = cms.untracked.vint32(20, 30, 40),
   histogramBinCount = cms.untracked.int32(100),
   histogramRangeLow = cms.untracked.double(0),
   histogramRangeHigh = cms.untracked.double(100),
   histogramEtaBinCount = cms.untracked.int32(20),
   #genMatchDeltaRcut = cms.untracked.double(0.25),
   #genMatchRelPtcut = cms.untracked.double(0.5),
   debug = cms.untracked.bool(False)
   #debug = cms.untracked.bool(True)
)

process.panalyzer = cms.Path(process.TPAnalyzer+process.analyzer)

process.TFileService = cms.Service("TFileService", 
   #fileName = cms.string("effTest_ecalTPs.root"), 
   fileName = cms.string("r2_phase2_minBias_v3.root"), 
   #fileName = cms.string("r2_phase2_singlePhoton_v2.root"), 
   #fileName = cms.string("r2_phase2_singlePiZero_v2.root"), 
   closeFileFast = cms.untracked.bool(True)
)

#dump_file = open("dump_file.py", "w")
#dump_file.write(process.dumpPython())


