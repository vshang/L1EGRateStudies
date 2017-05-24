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

        # Single Electron 500 MeV
        'file:/data/truggles/phaseII_singleElectron_20170518v2-round1_condor_cfg/round1_condor_cfg-002A4121-132C-E711-87AD-008CFAFBF618/round1_condor_cfg-002A4121-132C-E711-87AD-008CFAFBF618.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v2-round1_condor_cfg/round1_condor_cfg-024D0D76-EC25-E711-A9D0-001E6739830E/round1_condor_cfg-024D0D76-EC25-E711-A9D0-001E6739830E.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v2-round1_condor_cfg/round1_condor_cfg-0631262E-BB25-E711-A1D6-001E675811CC/round1_condor_cfg-0631262E-BB25-E711-A1D6-001E675811CC.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v2-round1_condor_cfg/round1_condor_cfg-101C9C3F-CB25-E711-AF93-C45444922958/round1_condor_cfg-101C9C3F-CB25-E711-AF93-C45444922958.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v2-round1_condor_cfg/round1_condor_cfg-160E7445-EB25-E711-9E34-001E677926DC/round1_condor_cfg-160E7445-EB25-E711-9E34-001E677926DC.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v2-round1_condor_cfg/round1_condor_cfg-1C84AD0A-D025-E711-B488-0CC47A706D26/round1_condor_cfg-1C84AD0A-D025-E711-B488-0CC47A706D26.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v2-round1_condor_cfg/round1_condor_cfg-2AF3BABF-BD25-E711-8F81-0025905C2CBC/round1_condor_cfg-2AF3BABF-BD25-E711-8F81-0025905C2CBC.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v2-round1_condor_cfg/round1_condor_cfg-2E0CBACA-4026-E711-BB78-68B59972C484/round1_condor_cfg-2E0CBACA-4026-E711-BB78-68B59972C484.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v2-round1_condor_cfg/round1_condor_cfg-3E73DA52-CC25-E711-A949-002590D8C72C/round1_condor_cfg-3E73DA52-CC25-E711-A949-002590D8C72C.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v2-round1_condor_cfg/round1_condor_cfg-4E675847-D325-E711-AE74-0CC47A7EEE0E/round1_condor_cfg-4E675847-D325-E711-AE74-0CC47A7EEE0E.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v2-round1_condor_cfg/round1_condor_cfg-545F066A-FF25-E711-AC01-7845C4FC3995/round1_condor_cfg-545F066A-FF25-E711-AC01-7845C4FC3995.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v2-round1_condor_cfg/round1_condor_cfg-5663AA6F-F525-E711-861B-001E67398633/round1_condor_cfg-5663AA6F-F525-E711-861B-001E67398633.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v2-round1_condor_cfg/round1_condor_cfg-6253C0D9-0026-E711-A7AB-008CFA007B98/round1_condor_cfg-6253C0D9-0026-E711-A7AB-008CFA007B98.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v2-round1_condor_cfg/round1_condor_cfg-6467775D-3D25-E711-A528-001E67396BA3/round1_condor_cfg-6467775D-3D25-E711-A528-001E67396BA3.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v2-round1_condor_cfg/round1_condor_cfg-687DCEB8-F725-E711-BF13-001E677925F6/round1_condor_cfg-687DCEB8-F725-E711-BF13-001E677925F6.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v2-round1_condor_cfg/round1_condor_cfg-6E078F2B-C125-E711-A421-0CC47A706D70/round1_condor_cfg-6E078F2B-C125-E711-A421-0CC47A706D70.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v2-round1_condor_cfg/round1_condor_cfg-703315B1-C325-E711-B7DD-C4346BC8F6D0/round1_condor_cfg-703315B1-C325-E711-B7DD-C4346BC8F6D0.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v2-round1_condor_cfg/round1_condor_cfg-706E99CB-1B26-E711-87FA-008CFAF74A86/round1_condor_cfg-706E99CB-1B26-E711-87FA-008CFAF74A86.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v2-round1_condor_cfg/round1_condor_cfg-7C81C1D6-3726-E711-A365-848F69FD25BC/round1_condor_cfg-7C81C1D6-3726-E711-A365-848F69FD25BC.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v2-round1_condor_cfg/round1_condor_cfg-840B39C2-0126-E711-9FDE-848F69FD29CA/round1_condor_cfg-840B39C2-0126-E711-9FDE-848F69FD29CA.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v2-round1_condor_cfg/round1_condor_cfg-8411127A-D925-E711-A7EF-20CF3056170E/round1_condor_cfg-8411127A-D925-E711-A7EF-20CF3056170E.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v2-round1_condor_cfg/round1_condor_cfg-8E33FA03-CD25-E711-AB70-0025905C3E38/round1_condor_cfg-8E33FA03-CD25-E711-AB70-0025905C3E38.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v2-round1_condor_cfg/round1_condor_cfg-90A879EA-072C-E711-9039-848F69FD291F/round1_condor_cfg-90A879EA-072C-E711-9039-848F69FD291F.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v2-round1_condor_cfg/round1_condor_cfg-90E15C01-E025-E711-87F1-002590DE6C48/round1_condor_cfg-90E15C01-E025-E711-87F1-002590DE6C48.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v2-round1_condor_cfg/round1_condor_cfg-9EF8CFDF-C825-E711-9138-0CC47AC08C34/round1_condor_cfg-9EF8CFDF-C825-E711-9138-0CC47AC08C34.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v2-round1_condor_cfg/round1_condor_cfg-A002D62B-C025-E711-8D08-842B2B760921/round1_condor_cfg-A002D62B-C025-E711-8D08-842B2B760921.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v2-round1_condor_cfg/round1_condor_cfg-AE95C30F-BC25-E711-A862-0025905C2CD2/round1_condor_cfg-AE95C30F-BC25-E711-A862-0025905C2CD2.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v2-round1_condor_cfg/round1_condor_cfg-B4091ED8-C425-E711-A5ED-0025905C54F4/round1_condor_cfg-B4091ED8-C425-E711-A5ED-0025905C54F4.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v2-round1_condor_cfg/round1_condor_cfg-B6228C06-D625-E711-804A-002590DE6C9A/round1_condor_cfg-B6228C06-D625-E711-804A-002590DE6C9A.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v2-round1_condor_cfg/round1_condor_cfg-BA35979B-BA25-E711-83D5-001E675043AD/round1_condor_cfg-BA35979B-BA25-E711-83D5-001E675043AD.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v2-round1_condor_cfg/round1_condor_cfg-C870B146-0626-E711-BF55-001E677926C2/round1_condor_cfg-C870B146-0626-E711-BF55-001E677926C2.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v2-round1_condor_cfg/round1_condor_cfg-CAE7CF1A-DC25-E711-B38E-0025901D48AA/round1_condor_cfg-CAE7CF1A-DC25-E711-B38E-0025901D48AA.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v2-round1_condor_cfg/round1_condor_cfg-D20EAB21-D525-E711-97A7-001E677926E2/round1_condor_cfg-D20EAB21-D525-E711-97A7-001E677926E2.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v2-round1_condor_cfg/round1_condor_cfg-D859E630-C625-E711-AC78-001E67504255/round1_condor_cfg-D859E630-C625-E711-AC78-001E67504255.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v2-round1_condor_cfg/round1_condor_cfg-DEA17C4F-BE25-E711-BA19-901B0E542804/round1_condor_cfg-DEA17C4F-BE25-E711-BA19-901B0E542804.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v2-round1_condor_cfg/round1_condor_cfg-E4969CE1-CF25-E711-B37B-001E67396DB5/round1_condor_cfg-E4969CE1-CF25-E711-B37B-001E67396DB5.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v2-round1_condor_cfg/round1_condor_cfg-EEAA825F-E425-E711-A299-0CC47A706D18/round1_condor_cfg-EEAA825F-E425-E711-A299-0CC47A706D18.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v2-round1_condor_cfg/round1_condor_cfg-F292ADD4-C625-E711-A8F7-0CC47AC08816/round1_condor_cfg-F292ADD4-C625-E711-A8F7-0CC47AC08816.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v2-round1_condor_cfg/round1_condor_cfg-F49729AF-D225-E711-9715-0025904C7B26/round1_condor_cfg-F49729AF-D225-E711-9715-0025904C7B26.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v2-round1_condor_cfg/round1_condor_cfg-FC24F3DE-0226-E711-91C8-001E677925A2/round1_condor_cfg-FC24F3DE-0226-E711-91C8-001E677925A2.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v2-round1_condor_cfg/round1_condor_cfg-FC9F4738-C125-E711-A862-00259021A04E/round1_condor_cfg-FC9F4738-C125-E711-A862-00259021A04E.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v2-round1_condor_cfg/round1_condor_cfg-FE315F33-BB25-E711-B59E-1866DA87931C/round1_condor_cfg-FE315F33-BB25-E711-B59E-1866DA87931C.root', 

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
   fileName = cms.string("r2_phase2_singleElectron.root"), 
   closeFileFast = cms.untracked.bool(True)
)

#dump_file = open("dump_file.py", "w")
#dump_file.write(process.dumpPython())


