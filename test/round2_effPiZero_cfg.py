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

        # Single PiZero 500 MeV
        'file:/data/truggles/phaseII_singlePiZero_20170612v1-round1_condor_cfg/round1_condor_cfg-0A2B315D-4928-E711-8759-E0071B73B6A0/round1_condor_cfg-0A2B315D-4928-E711-8759-E0071B73B6A0.root',
        'file:/data/truggles/phaseII_singlePiZero_20170612v1-round1_condor_cfg/round1_condor_cfg-0E51A18D-0628-E711-AF2C-24BE05CECBD1/round1_condor_cfg-0E51A18D-0628-E711-AF2C-24BE05CECBD1.root',
        'file:/data/truggles/phaseII_singlePiZero_20170612v1-round1_condor_cfg/round1_condor_cfg-10678AA3-9428-E711-88B7-24BE05C62611/round1_condor_cfg-10678AA3-9428-E711-88B7-24BE05C62611.root',
        'file:/data/truggles/phaseII_singlePiZero_20170612v1-round1_condor_cfg/round1_condor_cfg-12F21F79-8D28-E711-B3C1-5065F37DD491/round1_condor_cfg-12F21F79-8D28-E711-B3C1-5065F37DD491.root',
        'file:/data/truggles/phaseII_singlePiZero_20170612v1-round1_condor_cfg/round1_condor_cfg-166C0288-4128-E711-863D-4C79BA18182B/round1_condor_cfg-166C0288-4128-E711-863D-4C79BA18182B.root',
        'file:/data/truggles/phaseII_singlePiZero_20170612v1-round1_condor_cfg/round1_condor_cfg-221CE980-4B28-E711-A991-E0071B7A18F0/round1_condor_cfg-221CE980-4B28-E711-A991-E0071B7A18F0.root',
        'file:/data/truggles/phaseII_singlePiZero_20170612v1-round1_condor_cfg/round1_condor_cfg-26618122-8728-E711-94AF-E0071B741D70/round1_condor_cfg-26618122-8728-E711-94AF-E0071B741D70.root',
        'file:/data/truggles/phaseII_singlePiZero_20170612v1-round1_condor_cfg/round1_condor_cfg-2EA49551-4928-E711-8568-24BE05C33C61/round1_condor_cfg-2EA49551-4928-E711-8568-24BE05C33C61.root',
        'file:/data/truggles/phaseII_singlePiZero_20170612v1-round1_condor_cfg/round1_condor_cfg-360E72A3-2628-E711-A0B9-4C79BA1811AB/round1_condor_cfg-360E72A3-2628-E711-A0B9-4C79BA1811AB.root',
        'file:/data/truggles/phaseII_singlePiZero_20170612v1-round1_condor_cfg/round1_condor_cfg-3C0174C2-1128-E711-9A43-A0000420FE80/round1_condor_cfg-3C0174C2-1128-E711-9A43-A0000420FE80.root',
        'file:/data/truggles/phaseII_singlePiZero_20170612v1-round1_condor_cfg/round1_condor_cfg-3C6C4592-4B28-E711-B943-E0071B7A8590/round1_condor_cfg-3C6C4592-4B28-E711-B943-E0071B7A8590.root',
        'file:/data/truggles/phaseII_singlePiZero_20170612v1-round1_condor_cfg/round1_condor_cfg-46D6DBC8-5A28-E711-82C1-24BE05C63791/round1_condor_cfg-46D6DBC8-5A28-E711-82C1-24BE05C63791.root',
        'file:/data/truggles/phaseII_singlePiZero_20170612v1-round1_condor_cfg/round1_condor_cfg-486EA196-4B28-E711-B6D4-E0071B7AD7D0/round1_condor_cfg-486EA196-4B28-E711-B6D4-E0071B7AD7D0.root',
        'file:/data/truggles/phaseII_singlePiZero_20170612v1-round1_condor_cfg/round1_condor_cfg-5E07D19E-1928-E711-8F97-4C79BA180BE9/round1_condor_cfg-5E07D19E-1928-E711-8F97-4C79BA180BE9.root',
        'file:/data/truggles/phaseII_singlePiZero_20170612v1-round1_condor_cfg/round1_condor_cfg-5EB5485A-4228-E711-8107-E0071B7A58B0/round1_condor_cfg-5EB5485A-4228-E711-8107-E0071B7A58B0.root',
        'file:/data/truggles/phaseII_singlePiZero_20170612v1-round1_condor_cfg/round1_condor_cfg-747D3A7F-8928-E711-BD8F-E0071B6C9DE0/round1_condor_cfg-747D3A7F-8928-E711-BD8F-E0071B6C9DE0.root',
        'file:/data/truggles/phaseII_singlePiZero_20170612v1-round1_condor_cfg/round1_condor_cfg-76CDF118-3228-E711-BC03-5065F381E2D2/round1_condor_cfg-76CDF118-3228-E711-BC03-5065F381E2D2.root',
        'file:/data/truggles/phaseII_singlePiZero_20170612v1-round1_condor_cfg/round1_condor_cfg-80370F09-4C28-E711-992B-5065F3819221/round1_condor_cfg-80370F09-4C28-E711-992B-5065F3819221.root',
        'file:/data/truggles/phaseII_singlePiZero_20170612v1-round1_condor_cfg/round1_condor_cfg-8489297D-2628-E711-906A-E0071B7AD5E0/round1_condor_cfg-8489297D-2628-E711-906A-E0071B7AD5E0.root',
        'file:/data/truggles/phaseII_singlePiZero_20170612v1-round1_condor_cfg/round1_condor_cfg-8495439F-4728-E711-AC4B-4C79BA180A0F/round1_condor_cfg-8495439F-4728-E711-AC4B-4C79BA180A0F.root',
        'file:/data/truggles/phaseII_singlePiZero_20170612v1-round1_condor_cfg/round1_condor_cfg-9E3BBED1-2028-E711-B61C-4C79BA181869/round1_condor_cfg-9E3BBED1-2028-E711-B61C-4C79BA181869.root',
        'file:/data/truggles/phaseII_singlePiZero_20170612v1-round1_condor_cfg/round1_condor_cfg-A48B8F35-8128-E711-B037-24BE05CE2E81/round1_condor_cfg-A48B8F35-8128-E711-B037-24BE05CE2E81.root',
        'file:/data/truggles/phaseII_singlePiZero_20170612v1-round1_condor_cfg/round1_condor_cfg-A6B029E6-4128-E711-B2E7-4C79BA320D79/round1_condor_cfg-A6B029E6-4128-E711-B2E7-4C79BA320D79.root',
        'file:/data/truggles/phaseII_singlePiZero_20170612v1-round1_condor_cfg/round1_condor_cfg-AAEB286A-2028-E711-9469-4C79BA1812FF/round1_condor_cfg-AAEB286A-2028-E711-9469-4C79BA1812FF.root',
        'file:/data/truggles/phaseII_singlePiZero_20170612v1-round1_condor_cfg/round1_condor_cfg-B8CB049E-4528-E711-BC28-E0071B6C9DB0/round1_condor_cfg-B8CB049E-4528-E711-BC28-E0071B6C9DB0.root',
        'file:/data/truggles/phaseII_singlePiZero_20170612v1-round1_condor_cfg/round1_condor_cfg-C0123EE1-4728-E711-BE0C-E0071B7A3540/round1_condor_cfg-C0123EE1-4728-E711-BE0C-E0071B7A3540.root',
        'file:/data/truggles/phaseII_singlePiZero_20170612v1-round1_condor_cfg/round1_condor_cfg-C2FD178B-5928-E711-8DEE-4C79BA180D49/round1_condor_cfg-C2FD178B-5928-E711-8DEE-4C79BA180D49.root',
        'file:/data/truggles/phaseII_singlePiZero_20170612v1-round1_condor_cfg/round1_condor_cfg-C806B828-3F28-E711-8CC1-4C79BA32048B/round1_condor_cfg-C806B828-3F28-E711-8CC1-4C79BA32048B.root',
        'file:/data/truggles/phaseII_singlePiZero_20170612v1-round1_condor_cfg/round1_condor_cfg-C8E273E6-7A28-E711-A768-24BE05CEEC21/round1_condor_cfg-C8E273E6-7A28-E711-A768-24BE05CEEC21.root',
        'file:/data/truggles/phaseII_singlePiZero_20170612v1-round1_condor_cfg/round1_condor_cfg-CC467DFF-5928-E711-ADBB-E0071B7A2600/round1_condor_cfg-CC467DFF-5928-E711-ADBB-E0071B7A2600.root',
        'file:/data/truggles/phaseII_singlePiZero_20170612v1-round1_condor_cfg/round1_condor_cfg-D2CBA146-0928-E711-8388-24BE05C648A1/round1_condor_cfg-D2CBA146-0928-E711-8388-24BE05C648A1.root',
        'file:/data/truggles/phaseII_singlePiZero_20170612v1-round1_condor_cfg/round1_condor_cfg-D6448A3F-5528-E711-8E7E-24BE05C656F2/round1_condor_cfg-D6448A3F-5528-E711-8E7E-24BE05C656F2.root',
        'file:/data/truggles/phaseII_singlePiZero_20170612v1-round1_condor_cfg/round1_condor_cfg-E63FB3D3-5528-E711-B943-E0071B7A3540/round1_condor_cfg-E63FB3D3-5528-E711-B943-E0071B7A3540.root',
        'file:/data/truggles/phaseII_singlePiZero_20170612v1-round1_condor_cfg/round1_condor_cfg-FA11D873-5528-E711-B57E-5065F3816222/round1_condor_cfg-FA11D873-5528-E711-B57E-5065F3816222.root',
        'file:/data/truggles/phaseII_singlePiZero_20170612v1-round1_condor_cfg/round1_condor_cfg-FCB1E068-7928-E711-AAF9-A0000420FE80/round1_condor_cfg-FCB1E068-7928-E711-AAF9-A0000420FE80.root', 
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
   doEfficiencyCalc = cms.untracked.bool(True),
   useOfflineClusters = cms.untracked.bool(False),
   useEndcap = cms.untracked.bool(False),
   doTracking = cms.untracked.bool(True),
   isPhoton = cms.untracked.bool(True),
   turnOnThresholds = cms.untracked.vint32(20, 30, 40),
   histogramBinCount = cms.untracked.int32(100),
   histogramRangeLow = cms.untracked.double(0),
   histogramRangeHigh = cms.untracked.double(100),
   histogramEtaBinCount = cms.untracked.int32(20),
   genMatchDeltaRcut = cms.untracked.double(0.25),
   genMatchRelPtcut = cms.untracked.double(0.5),
   debug = cms.untracked.bool(False)
   #debug = cms.untracked.bool(True)
)

process.panalyzer = cms.Path(process.TPAnalyzer+process.analyzer)

process.TFileService = cms.Service("TFileService", 
   fileName = cms.string("r2_phase2_singlePiZero_v9.root"), 
   closeFileFast = cms.untracked.bool(True)
)

#dump_file = open("dump_file.py", "w")
#dump_file.write(process.dumpPython())


