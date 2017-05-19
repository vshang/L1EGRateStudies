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
        #'file:/data/truggles/phase2_singleE_500.root',
        #'file:/data/truggles/phase2_singleElectron_v2.root',
        #'file:/data/truggles/phase2_singlePhoton_v2.root',
        #'file:/data/truggles/phase2_singlePiZero_v2.root',
    #    'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-002A4121-132C-E711-87AD-008CFAFBF618/round1_condor_cfg-002A4121-132C-E711-87AD-008CFAFBF618.root', 
    #    'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-024D0D76-EC25-E711-A9D0-001E6739830E/round1_condor_cfg-024D0D76-EC25-E711-A9D0-001E6739830E.root',
    #    'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-0631262E-BB25-E711-A1D6-001E675811CC/round1_condor_cfg-0631262E-BB25-E711-A1D6-001E675811CC.root',
    #    'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-101C9C3F-CB25-E711-AF93-C45444922958/round1_condor_cfg-101C9C3F-CB25-E711-AF93-C45444922958.root',
    #    'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-160E7445-EB25-E711-9E34-001E677926DC/round1_condor_cfg-160E7445-EB25-E711-9E34-001E677926DC.root',
    #    'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-1C84AD0A-D025-E711-B488-0CC47A706D26/round1_condor_cfg-1C84AD0A-D025-E711-B488-0CC47A706D26.root',
    #    'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-2AF3BABF-BD25-E711-8F81-0025905C2CBC/round1_condor_cfg-2AF3BABF-BD25-E711-8F81-0025905C2CBC.root',
    #    'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-2E0CBACA-4026-E711-BB78-68B59972C484/round1_condor_cfg-2E0CBACA-4026-E711-BB78-68B59972C484.root',
    #    'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-3E73DA52-CC25-E711-A949-002590D8C72C/round1_condor_cfg-3E73DA52-CC25-E711-A949-002590D8C72C.root',
    #    'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-4E675847-D325-E711-AE74-0CC47A7EEE0E/round1_condor_cfg-4E675847-D325-E711-AE74-0CC47A7EEE0E.root',
    #    'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-545F066A-FF25-E711-AC01-7845C4FC3995/round1_condor_cfg-545F066A-FF25-E711-AC01-7845C4FC3995.root',
    #    'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-5663AA6F-F525-E711-861B-001E67398633/round1_condor_cfg-5663AA6F-F525-E711-861B-001E67398633.root',
    #    'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-6253C0D9-0026-E711-A7AB-008CFA007B98/round1_condor_cfg-6253C0D9-0026-E711-A7AB-008CFA007B98.root',
    #    'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-6467775D-3D25-E711-A528-001E67396BA3/round1_condor_cfg-6467775D-3D25-E711-A528-001E67396BA3.root',
    #    'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-687DCEB8-F725-E711-BF13-001E677925F6/round1_condor_cfg-687DCEB8-F725-E711-BF13-001E677925F6.root',
    #    'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-6E078F2B-C125-E711-A421-0CC47A706D70/round1_condor_cfg-6E078F2B-C125-E711-A421-0CC47A706D70.root',
    #    'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-703315B1-C325-E711-B7DD-C4346BC8F6D0/round1_condor_cfg-703315B1-C325-E711-B7DD-C4346BC8F6D0.root',
    #    'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-706E99CB-1B26-E711-87FA-008CFAF74A86/round1_condor_cfg-706E99CB-1B26-E711-87FA-008CFAF74A86.root',
    #    'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-7C81C1D6-3726-E711-A365-848F69FD25BC/round1_condor_cfg-7C81C1D6-3726-E711-A365-848F69FD25BC.root',
    #    'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-840B39C2-0126-E711-9FDE-848F69FD29CA/round1_condor_cfg-840B39C2-0126-E711-9FDE-848F69FD29CA.root',
    #    'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-8411127A-D925-E711-A7EF-20CF3056170E/round1_condor_cfg-8411127A-D925-E711-A7EF-20CF3056170E.root',
    #    'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-8E33FA03-CD25-E711-AB70-0025905C3E38/round1_condor_cfg-8E33FA03-CD25-E711-AB70-0025905C3E38.root',
    #    'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-90A879EA-072C-E711-9039-848F69FD291F/round1_condor_cfg-90A879EA-072C-E711-9039-848F69FD291F.root',
    #    'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-90E15C01-E025-E711-87F1-002590DE6C48/round1_condor_cfg-90E15C01-E025-E711-87F1-002590DE6C48.root',
    #    'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-9EF8CFDF-C825-E711-9138-0CC47AC08C34/round1_condor_cfg-9EF8CFDF-C825-E711-9138-0CC47AC08C34.root',
    #    'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-A002D62B-C025-E711-8D08-842B2B760921/round1_condor_cfg-A002D62B-C025-E711-8D08-842B2B760921.root',
    #    'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-AE95C30F-BC25-E711-A862-0025905C2CD2/round1_condor_cfg-AE95C30F-BC25-E711-A862-0025905C2CD2.root',
    #    'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-B4091ED8-C425-E711-A5ED-0025905C54F4/round1_condor_cfg-B4091ED8-C425-E711-A5ED-0025905C54F4.root',
    #    'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-B6228C06-D625-E711-804A-002590DE6C9A/round1_condor_cfg-B6228C06-D625-E711-804A-002590DE6C9A.root',
    #    'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-BA35979B-BA25-E711-83D5-001E675043AD/round1_condor_cfg-BA35979B-BA25-E711-83D5-001E675043AD.root',
    #    'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-C870B146-0626-E711-BF55-001E677926C2/round1_condor_cfg-C870B146-0626-E711-BF55-001E677926C2.root',
    #    'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-CAE7CF1A-DC25-E711-B38E-0025901D48AA/round1_condor_cfg-CAE7CF1A-DC25-E711-B38E-0025901D48AA.root',
    #    'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-D20EAB21-D525-E711-97A7-001E677926E2/round1_condor_cfg-D20EAB21-D525-E711-97A7-001E677926E2.root',
    #    'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-D859E630-C625-E711-AC78-001E67504255/round1_condor_cfg-D859E630-C625-E711-AC78-001E67504255.root',
    #    'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-DEA17C4F-BE25-E711-BA19-901B0E542804/round1_condor_cfg-DEA17C4F-BE25-E711-BA19-901B0E542804.root',
    #    'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-E4969CE1-CF25-E711-B37B-001E67396DB5/round1_condor_cfg-E4969CE1-CF25-E711-B37B-001E67396DB5.root',
    #    'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-EEAA825F-E425-E711-A299-0CC47A706D18/round1_condor_cfg-EEAA825F-E425-E711-A299-0CC47A706D18.root',
    #    'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-F292ADD4-C625-E711-A8F7-0CC47AC08816/round1_condor_cfg-F292ADD4-C625-E711-A8F7-0CC47AC08816.root',
    #    'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-F49729AF-D225-E711-9715-0025904C7B26/round1_condor_cfg-F49729AF-D225-E711-9715-0025904C7B26.root',
    #    'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-FC24F3DE-0226-E711-91C8-001E677925A2/round1_condor_cfg-FC24F3DE-0226-E711-91C8-001E677925A2.root',
    #    'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-FC9F4738-C125-E711-A862-00259021A04E/round1_condor_cfg-FC9F4738-C125-E711-A862-00259021A04E.root',
    #    'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-FE315F33-BB25-E711-B59E-1866DA87931C/round1_condor_cfg-FE315F33-BB25-E711-B59E-1866DA87931C.root', 
        'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-002A4121-132C-E711-87AD-008CFAFBF618/round1_condor_cfg-002A4121-132C-E711-87AD-008CFAFBF618.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-024D0D76-EC25-E711-A9D0-001E6739830E/round1_condor_cfg-024D0D76-EC25-E711-A9D0-001E6739830E.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-0631262E-BB25-E711-A1D6-001E675811CC/round1_condor_cfg-0631262E-BB25-E711-A1D6-001E675811CC.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-081EAB9E-D625-E711-AC03-B083FED138B3/round1_condor_cfg-081EAB9E-D625-E711-AC03-B083FED138B3.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-0C610A40-D525-E711-84E0-0025901D40A6/round1_condor_cfg-0C610A40-D525-E711-84E0-0025901D40A6.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-101C9C3F-CB25-E711-AF93-C45444922958/round1_condor_cfg-101C9C3F-CB25-E711-AF93-C45444922958.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-14BF7E1C-3D25-E711-97BA-0025905C3D6A/round1_condor_cfg-14BF7E1C-3D25-E711-97BA-0025905C3D6A.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-160E7445-EB25-E711-9E34-001E677926DC/round1_condor_cfg-160E7445-EB25-E711-9E34-001E677926DC.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-1C84AD0A-D025-E711-B488-0CC47A706D26/round1_condor_cfg-1C84AD0A-D025-E711-B488-0CC47A706D26.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-1E61533D-E625-E711-A6DE-0CC47A7034D2/round1_condor_cfg-1E61533D-E625-E711-A6DE-0CC47A7034D2.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-1EA1FCB6-2826-E711-BEF3-008CFAFBF6CC/round1_condor_cfg-1EA1FCB6-2826-E711-BEF3-008CFAFBF6CC.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-2459A725-BB25-E711-AE17-0025901D40A6/round1_condor_cfg-2459A725-BB25-E711-AE17-0025901D40A6.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-2A5A7768-EC25-E711-AF14-001E67792484/round1_condor_cfg-2A5A7768-EC25-E711-AF14-001E67792484.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-2AF3BABF-BD25-E711-8F81-0025905C2CBC/round1_condor_cfg-2AF3BABF-BD25-E711-8F81-0025905C2CBC.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-32631A01-E625-E711-BD9F-0CC47A706D26/round1_condor_cfg-32631A01-E625-E711-BD9F-0CC47A706D26.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-32D8D053-D625-E711-A23C-001E67E6F909/round1_condor_cfg-32D8D053-D625-E711-A23C-001E67E6F909.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-38C166F6-D125-E711-803E-002590200844/round1_condor_cfg-38C166F6-D125-E711-803E-002590200844.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-3E35E78A-D425-E711-9C50-0CC47A706D18/round1_condor_cfg-3E35E78A-D425-E711-9C50-0CC47A706D18.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-3E73DA52-CC25-E711-A949-002590D8C72C/round1_condor_cfg-3E73DA52-CC25-E711-A949-002590D8C72C.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-4065E632-FF26-E711-8791-001E67E69879/round1_condor_cfg-4065E632-FF26-E711-8791-001E67E69879.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-460461D7-E625-E711-8FD2-001E67397F3F/round1_condor_cfg-460461D7-E625-E711-8FD2-001E67397F3F.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-46514934-E125-E711-9B59-0025904C7A60/round1_condor_cfg-46514934-E125-E711-9B59-0025904C7A60.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-4E675847-D325-E711-AE74-0CC47A7EEE0E/round1_condor_cfg-4E675847-D325-E711-AE74-0CC47A7EEE0E.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-501F7F30-EB25-E711-9F2B-001E6779244C/round1_condor_cfg-501F7F30-EB25-E711-9F2B-001E6779244C.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-545F066A-FF25-E711-AC01-7845C4FC3995/round1_condor_cfg-545F066A-FF25-E711-AC01-7845C4FC3995.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-5663AA6F-F525-E711-861B-001E67398633/round1_condor_cfg-5663AA6F-F525-E711-861B-001E67398633.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-568BDF4A-C225-E711-9DB8-901B0E5427B0/round1_condor_cfg-568BDF4A-C225-E711-9DB8-901B0E5427B0.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-5E1CA7CD-3E25-E711-A599-001E677926DC/round1_condor_cfg-5E1CA7CD-3E25-E711-A599-001E677926DC.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-60167B99-E825-E711-9C56-0025904C7DF8/round1_condor_cfg-60167B99-E825-E711-9C56-0025904C7DF8.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-6253C0D9-0026-E711-A7AB-008CFA007B98/round1_condor_cfg-6253C0D9-0026-E711-A7AB-008CFA007B98.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-6467775D-3D25-E711-A528-001E67396BA3/round1_condor_cfg-6467775D-3D25-E711-A528-001E67396BA3.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-687DCEB8-F725-E711-BF13-001E677925F6/round1_condor_cfg-687DCEB8-F725-E711-BF13-001E677925F6.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-6E078F2B-C125-E711-A421-0CC47A706D70/round1_condor_cfg-6E078F2B-C125-E711-A421-0CC47A706D70.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-703315B1-C325-E711-B7DD-C4346BC8F6D0/round1_condor_cfg-703315B1-C325-E711-B7DD-C4346BC8F6D0.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-706E99CB-1B26-E711-87FA-008CFAF74A86/round1_condor_cfg-706E99CB-1B26-E711-87FA-008CFAF74A86.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-74EBDC35-BB25-E711-9FAC-0025905C4262/round1_condor_cfg-74EBDC35-BB25-E711-9FAC-0025905C4262.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-7A6F381E-C525-E711-9844-0025905C431C/round1_condor_cfg-7A6F381E-C525-E711-9844-0025905C431C.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-7C81C1D6-3726-E711-A365-848F69FD25BC/round1_condor_cfg-7C81C1D6-3726-E711-A365-848F69FD25BC.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-82A6009E-D925-E711-84A7-A0369F8363C2/round1_condor_cfg-82A6009E-D925-E711-84A7-A0369F8363C2.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-840B39C2-0126-E711-9FDE-848F69FD29CA/round1_condor_cfg-840B39C2-0126-E711-9FDE-848F69FD29CA.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-8411127A-D925-E711-A7EF-20CF3056170E/round1_condor_cfg-8411127A-D925-E711-A7EF-20CF3056170E.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-8A28625A-FA25-E711-BE94-1CC1DE18CEEE/round1_condor_cfg-8A28625A-FA25-E711-BE94-1CC1DE18CEEE.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-8E33FA03-CD25-E711-AB70-0025905C3E38/round1_condor_cfg-8E33FA03-CD25-E711-AB70-0025905C3E38.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-90A879EA-072C-E711-9039-848F69FD291F/round1_condor_cfg-90A879EA-072C-E711-9039-848F69FD291F.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-90E0C13F-BB25-E711-9AEC-D4AE526A0461/round1_condor_cfg-90E0C13F-BB25-E711-9AEC-D4AE526A0461.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-90E15C01-E025-E711-87F1-002590DE6C48/round1_condor_cfg-90E15C01-E025-E711-87F1-002590DE6C48.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-9A058AF8-0A26-E711-AB19-001E6739830E/round1_condor_cfg-9A058AF8-0A26-E711-AB19-001E6739830E.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-9A08F046-F925-E711-AE3D-001E677928AE/round1_condor_cfg-9A08F046-F925-E711-AE3D-001E677928AE.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-9EF8CFDF-C825-E711-9138-0CC47AC08C34/round1_condor_cfg-9EF8CFDF-C825-E711-9138-0CC47AC08C34.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-A002D62B-C025-E711-8D08-842B2B760921/round1_condor_cfg-A002D62B-C025-E711-8D08-842B2B760921.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-A4D50872-F725-E711-A3D5-001E67E69E32/round1_condor_cfg-A4D50872-F725-E711-A3D5-001E67E69E32.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-A636B1FB-E425-E711-9C0A-002590200900/round1_condor_cfg-A636B1FB-E425-E711-9C0A-002590200900.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-AC5306EC-0326-E711-934B-002590200AC0/round1_condor_cfg-AC5306EC-0326-E711-934B-002590200AC0.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-AE95C30F-BC25-E711-A862-0025905C2CD2/round1_condor_cfg-AE95C30F-BC25-E711-A862-0025905C2CD2.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-B077F2E7-C625-E711-8F0B-20CF3027A5F9/round1_condor_cfg-B077F2E7-C625-E711-8F0B-20CF3027A5F9.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-B4091ED8-C425-E711-A5ED-0025905C54F4/round1_condor_cfg-B4091ED8-C425-E711-A5ED-0025905C54F4.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-B6228C06-D625-E711-804A-002590DE6C9A/round1_condor_cfg-B6228C06-D625-E711-804A-002590DE6C9A.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-BA35979B-BA25-E711-83D5-001E675043AD/round1_condor_cfg-BA35979B-BA25-E711-83D5-001E675043AD.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-BE47584B-FC25-E711-A271-7845C4FC368F/round1_condor_cfg-BE47584B-FC25-E711-A271-7845C4FC368F.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-BEB67B59-1526-E711-B64D-001E6739834A/round1_condor_cfg-BEB67B59-1526-E711-B64D-001E6739834A.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-C24AD994-CB25-E711-9AD8-0CC47A706CF0/round1_condor_cfg-C24AD994-CB25-E711-9AD8-0CC47A706CF0.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-C8F4A2AC-C625-E711-95F0-34E6D7BEAF0E/round1_condor_cfg-C8F4A2AC-C625-E711-95F0-34E6D7BEAF0E.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-CAE7CF1A-DC25-E711-B38E-0025901D48AA/round1_condor_cfg-CAE7CF1A-DC25-E711-B38E-0025901D48AA.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-D20EAB21-D525-E711-97A7-001E677926E2/round1_condor_cfg-D20EAB21-D525-E711-97A7-001E677926E2.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-D49ADE77-F425-E711-A986-002590200A40/round1_condor_cfg-D49ADE77-F425-E711-A986-002590200A40.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-D859E630-C625-E711-AC78-001E67504255/round1_condor_cfg-D859E630-C625-E711-AC78-001E67504255.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-D87476FC-F925-E711-A6BC-008CFAF7350E/round1_condor_cfg-D87476FC-F925-E711-A6BC-008CFAF7350E.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-DEA17C4F-BE25-E711-BA19-901B0E542804/round1_condor_cfg-DEA17C4F-BE25-E711-BA19-901B0E542804.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-E22321CA-FF25-E711-9324-001E67397F2B/round1_condor_cfg-E22321CA-FF25-E711-9324-001E67397F2B.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-E4969CE1-CF25-E711-B37B-001E67396DB5/round1_condor_cfg-E4969CE1-CF25-E711-B37B-001E67396DB5.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-EA67036B-CC25-E711-888F-0025905D1D7A/round1_condor_cfg-EA67036B-CC25-E711-888F-0025905D1D7A.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-EAD55AFC-F225-E711-B6B4-001E673972F6/round1_condor_cfg-EAD55AFC-F225-E711-B6B4-001E673972F6.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-EEAA825F-E425-E711-A299-0CC47A706D18/round1_condor_cfg-EEAA825F-E425-E711-A299-0CC47A706D18.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-F292ADD4-C625-E711-A8F7-0CC47AC08816/round1_condor_cfg-F292ADD4-C625-E711-A8F7-0CC47AC08816.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-F49729AF-D225-E711-9715-0025904C7B26/round1_condor_cfg-F49729AF-D225-E711-9715-0025904C7B26.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-FC24F3DE-0226-E711-91C8-001E677925A2/round1_condor_cfg-FC24F3DE-0226-E711-91C8-001E677925A2.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-FC9F4738-C125-E711-A862-00259021A04E/round1_condor_cfg-FC9F4738-C125-E711-A862-00259021A04E.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-FE315F33-BB25-E711-B59E-1866DA87931C/round1_condor_cfg-FE315F33-BB25-E711-B59E-1866DA87931C.root',
        'file:/data/truggles/phaseII_singleElectron_20170518v3-round1_condor_cfg/round1_condor_cfg-FEF66F84-FC2B-E711-8119-7845C4FC3A3D/round1_condor_cfg-FEF66F84-FC2B-E711-8119-7845C4FC3A3D.root', 
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
   #fileName = cms.string("effTest_ecalTPs.root"), 
   fileName = cms.string("r2_phase2_singleElectron_v3.root"), 
   #fileName = cms.string("r2_phase2_singlePhoton_v2.root"), 
   #fileName = cms.string("r2_phase2_singlePiZero_v2.root"), 
   closeFileFast = cms.untracked.bool(True)
)

#dump_file = open("dump_file.py", "w")
#dump_file.write(process.dumpPython())


