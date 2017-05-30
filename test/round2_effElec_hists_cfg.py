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
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-002A4121-132C-E711-87AD-008CFAFBF618/round1_condor_cfg-002A4121-132C-E711-87AD-008CFAFBF618.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-00ECA247-D925-E711-80DC-00259021A43E/round1_condor_cfg-00ECA247-D925-E711-80DC-00259021A43E.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-024D0D76-EC25-E711-A9D0-001E6739830E/round1_condor_cfg-024D0D76-EC25-E711-A9D0-001E6739830E.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-0269AF0A-0826-E711-B429-848F69FD291F/round1_condor_cfg-0269AF0A-0826-E711-B429-848F69FD291F.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-042076A1-C425-E711-AF86-20CF300E9EDD/round1_condor_cfg-042076A1-C425-E711-AF86-20CF300E9EDD.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-0631262E-BB25-E711-A1D6-001E675811CC/round1_condor_cfg-0631262E-BB25-E711-A1D6-001E675811CC.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-06EFBD70-D225-E711-9916-0CC47A706CF0/round1_condor_cfg-06EFBD70-D225-E711-9916-0CC47A706CF0.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-081EAB9E-D625-E711-AC03-B083FED138B3/round1_condor_cfg-081EAB9E-D625-E711-AC03-B083FED138B3.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-085A4E45-D325-E711-8924-0CC47AC08904/round1_condor_cfg-085A4E45-D325-E711-8924-0CC47AC08904.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-0A58785D-D725-E711-A9F8-002590DE6E86/round1_condor_cfg-0A58785D-D725-E711-A9F8-002590DE6E86.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-0C27ACB5-C025-E711-8A2D-10BF481A01D5/round1_condor_cfg-0C27ACB5-C025-E711-8A2D-10BF481A01D5.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-0C610A40-D525-E711-84E0-0025901D40A6/round1_condor_cfg-0C610A40-D525-E711-84E0-0025901D40A6.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-0E5C5AFE-DD25-E711-AC00-0CC47A706FFE/round1_condor_cfg-0E5C5AFE-DD25-E711-AC00-0CC47A706FFE.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-101C9C3F-CB25-E711-AF93-C45444922958/round1_condor_cfg-101C9C3F-CB25-E711-AF93-C45444922958.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-10CE2DBF-C125-E711-9DA3-002590DE6E5C/round1_condor_cfg-10CE2DBF-C125-E711-9DA3-002590DE6E5C.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-12873406-F525-E711-B5B1-848F69FD4553/round1_condor_cfg-12873406-F525-E711-B5B1-848F69FD4553.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-128CD0DE-DA25-E711-AB8C-001E67792488/round1_condor_cfg-128CD0DE-DA25-E711-AB8C-001E67792488.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-14BF7E1C-3D25-E711-97BA-0025905C3D6A/round1_condor_cfg-14BF7E1C-3D25-E711-97BA-0025905C3D6A.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-160E7445-EB25-E711-9E34-001E677926DC/round1_condor_cfg-160E7445-EB25-E711-9E34-001E677926DC.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-18388864-BE25-E711-96D6-0025904C7DF6/round1_condor_cfg-18388864-BE25-E711-96D6-0025904C7DF6.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-18B9B632-3B26-E711-A7C4-0025901D4446/round1_condor_cfg-18B9B632-3B26-E711-A7C4-0025901D4446.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-1A335AA2-C025-E711-B7A1-0025901D40B2/round1_condor_cfg-1A335AA2-C025-E711-B7A1-0025901D40B2.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-1A63672A-FB25-E711-BC7D-0025901D49AC/round1_condor_cfg-1A63672A-FB25-E711-BC7D-0025901D49AC.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-1C84AD0A-D025-E711-B488-0CC47A706D26/round1_condor_cfg-1C84AD0A-D025-E711-B488-0CC47A706D26.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-1E5A3D93-E425-E711-8497-001E6779258C/round1_condor_cfg-1E5A3D93-E425-E711-8497-001E6779258C.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-1E61533D-E625-E711-A6DE-0CC47A7034D2/round1_condor_cfg-1E61533D-E625-E711-A6DE-0CC47A7034D2.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-1EA1FCB6-2826-E711-BEF3-008CFAFBF6CC/round1_condor_cfg-1EA1FCB6-2826-E711-BEF3-008CFAFBF6CC.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-205CAECC-D125-E711-996A-001E677927B0/round1_condor_cfg-205CAECC-D125-E711-996A-001E677927B0.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-2459A725-BB25-E711-AE17-0025901D40A6/round1_condor_cfg-2459A725-BB25-E711-AE17-0025901D40A6.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-26935AE5-D425-E711-A0BA-001E67792426/round1_condor_cfg-26935AE5-D425-E711-A0BA-001E67792426.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-282EE921-BD25-E711-9474-1866DA890658/round1_condor_cfg-282EE921-BD25-E711-9474-1866DA890658.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-28837F89-C425-E711-B71F-20CF3019DEF4/round1_condor_cfg-28837F89-C425-E711-B71F-20CF3019DEF4.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-2A5A7768-EC25-E711-AF14-001E67792484/round1_condor_cfg-2A5A7768-EC25-E711-AF14-001E67792484.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-2CC8BF70-EA25-E711-AACE-001E67398A43/round1_condor_cfg-2CC8BF70-EA25-E711-AACE-001E67398A43.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-2CD4BABD-E625-E711-B4F2-001E67E6F855/round1_condor_cfg-2CD4BABD-E625-E711-B4F2-001E67E6F855.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-2E0CBACA-4026-E711-BB78-68B59972C484/round1_condor_cfg-2E0CBACA-4026-E711-BB78-68B59972C484.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-302D12C0-0226-E711-81E2-0025902009B8/round1_condor_cfg-302D12C0-0226-E711-81E2-0025902009B8.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-30A3E375-D325-E711-BCB1-001E67E713EF/round1_condor_cfg-30A3E375-D325-E711-BCB1-001E67E713EF.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-32631A01-E625-E711-BD9F-0CC47A706D26/round1_condor_cfg-32631A01-E625-E711-BD9F-0CC47A706D26.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-32D8D053-D625-E711-A23C-001E67E6F909/round1_condor_cfg-32D8D053-D625-E711-A23C-001E67E6F909.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-34FAB117-BD25-E711-8EE6-901B0E542756/round1_condor_cfg-34FAB117-BD25-E711-8EE6-901B0E542756.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-36842769-3726-E711-B844-0025904C7A5C/round1_condor_cfg-36842769-3726-E711-B844-0025904C7A5C.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-38119A35-FB25-E711-906F-848F69FD45A4/round1_condor_cfg-38119A35-FB25-E711-906F-848F69FD45A4.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-3888F328-0E2C-E711-989F-F04DA275C2FE/round1_condor_cfg-3888F328-0E2C-E711-989F-F04DA275C2FE.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-38C166F6-D125-E711-803E-002590200844/round1_condor_cfg-38C166F6-D125-E711-803E-002590200844.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-38F99D32-F425-E711-915F-0CC47A706D18/round1_condor_cfg-38F99D32-F425-E711-915F-0CC47A706D18.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-3C322B9D-BF25-E711-8B01-0025905C96EA/round1_condor_cfg-3C322B9D-BF25-E711-8B01-0025905C96EA.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-3E35E78A-D425-E711-9C50-0CC47A706D18/round1_condor_cfg-3E35E78A-D425-E711-9C50-0CC47A706D18.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-3E73DA52-CC25-E711-A949-002590D8C72C/round1_condor_cfg-3E73DA52-CC25-E711-A949-002590D8C72C.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-3E85C89D-E525-E711-A4C3-001E677924DC/round1_condor_cfg-3E85C89D-E525-E711-A4C3-001E677924DC.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-4065E632-FF26-E711-8791-001E67E69879/round1_condor_cfg-4065E632-FF26-E711-8791-001E67E69879.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-40CBFE6E-F525-E711-B31F-001E677926A8/round1_condor_cfg-40CBFE6E-F525-E711-B31F-001E677926A8.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-422CC39A-CF25-E711-B93B-001E677925AC/round1_condor_cfg-422CC39A-CF25-E711-B93B-001E677925AC.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-42E3AA13-0826-E711-ABBC-1866DA87AB31/round1_condor_cfg-42E3AA13-0826-E711-ABBC-1866DA87AB31.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-443DE39B-EB25-E711-A0D4-001E67E6F4C2/round1_condor_cfg-443DE39B-EB25-E711-A0D4-001E67E6F4C2.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-460461D7-E625-E711-8FD2-001E67397F3F/round1_condor_cfg-460461D7-E625-E711-8FD2-001E67397F3F.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-46514934-E125-E711-9B59-0025904C7A60/round1_condor_cfg-46514934-E125-E711-9B59-0025904C7A60.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-48607E31-0226-E711-9EA3-001E677925F0/round1_condor_cfg-48607E31-0226-E711-9EA3-001E677925F0.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-48CE07F3-C125-E711-A64A-0025905C975C/round1_condor_cfg-48CE07F3-C125-E711-A64A-0025905C975C.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-4A8F4A92-C725-E711-9C55-20CF3027A5EF/round1_condor_cfg-4A8F4A92-C725-E711-9C55-20CF3027A5EF.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-4C140F4B-0E26-E711-91DA-008CFAF74A32/round1_condor_cfg-4C140F4B-0E26-E711-91DA-008CFAF74A32.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-4CE0642C-F725-E711-A342-0CC47AC08BD4/round1_condor_cfg-4CE0642C-F725-E711-A342-0CC47AC08BD4.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-4E675847-D325-E711-AE74-0CC47A7EEE0E/round1_condor_cfg-4E675847-D325-E711-AE74-0CC47A7EEE0E.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-50AF8E14-5826-E711-8DDE-0025905C3D6A/round1_condor_cfg-50AF8E14-5826-E711-8DDE-0025905C3D6A.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-5418FB30-A326-E711-8E93-0242AC110002/round1_condor_cfg-5418FB30-A326-E711-8E93-0242AC110002.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-545F066A-FF25-E711-AC01-7845C4FC3995/round1_condor_cfg-545F066A-FF25-E711-AC01-7845C4FC3995.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-54771886-F025-E711-8E1C-001E677927C2/round1_condor_cfg-54771886-F025-E711-8E1C-001E677927C2.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-5663AA6F-F525-E711-861B-001E67398633/round1_condor_cfg-5663AA6F-F525-E711-861B-001E67398633.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-568BDF4A-C225-E711-9DB8-901B0E5427B0/round1_condor_cfg-568BDF4A-C225-E711-9DB8-901B0E5427B0.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-58BA6212-E725-E711-8736-001E67792566/round1_condor_cfg-58BA6212-E725-E711-8736-001E67792566.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-58C191E7-DB25-E711-B837-C454449229AF/round1_condor_cfg-58C191E7-DB25-E711-B837-C454449229AF.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-5AD992E2-CF25-E711-A45A-002590200900/round1_condor_cfg-5AD992E2-CF25-E711-A45A-002590200900.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-5E1CA7CD-3E25-E711-A599-001E677926DC/round1_condor_cfg-5E1CA7CD-3E25-E711-A599-001E677926DC.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-5E20755C-F625-E711-9378-A4BF0108B8F2/round1_condor_cfg-5E20755C-F625-E711-9378-A4BF0108B8F2.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-5E6C1EF1-9326-E711-A4F2-70106F4A9690/round1_condor_cfg-5E6C1EF1-9326-E711-A4F2-70106F4A9690.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-5EA3F944-BB25-E711-8C11-485B39897242/round1_condor_cfg-5EA3F944-BB25-E711-8C11-485B39897242.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-6219B469-BC25-E711-B226-001E67504445/round1_condor_cfg-6219B469-BC25-E711-B226-001E67504445.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-6253C0D9-0026-E711-A7AB-008CFA007B98/round1_condor_cfg-6253C0D9-0026-E711-A7AB-008CFA007B98.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-62591EDF-5526-E711-88F8-7845C4FC3779/round1_condor_cfg-62591EDF-5526-E711-88F8-7845C4FC3779.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-6467775D-3D25-E711-A528-001E67396BA3/round1_condor_cfg-6467775D-3D25-E711-A528-001E67396BA3.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-64F27176-D525-E711-AAC5-6CC2173BBD80/round1_condor_cfg-64F27176-D525-E711-AAC5-6CC2173BBD80.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-66A0FE90-0026-E711-A3BB-008CFAFBFCF0/round1_condor_cfg-66A0FE90-0026-E711-A3BB-008CFAFBFCF0.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-66A75BBA-122C-E711-B215-848F69FD4409/round1_condor_cfg-66A75BBA-122C-E711-B215-848F69FD4409.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-687DCEB8-F725-E711-BF13-001E677925F6/round1_condor_cfg-687DCEB8-F725-E711-BF13-001E677925F6.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-6A16D337-BB25-E711-91FE-0025904CDDEC/round1_condor_cfg-6A16D337-BB25-E711-91FE-0025904CDDEC.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-6A32D0F8-D625-E711-98F8-0CC47AC087AE/round1_condor_cfg-6A32D0F8-D625-E711-98F8-0CC47AC087AE.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-6AFCDD30-0326-E711-99D9-1CB72C0A3DBD/round1_condor_cfg-6AFCDD30-0326-E711-99D9-1CB72C0A3DBD.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-6C8FE069-F625-E711-96A3-002590DE6E2E/round1_condor_cfg-6C8FE069-F625-E711-96A3-002590DE6E2E.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-6E078F2B-C125-E711-A421-0CC47A706D70/round1_condor_cfg-6E078F2B-C125-E711-A421-0CC47A706D70.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-703315B1-C325-E711-B7DD-C4346BC8F6D0/round1_condor_cfg-703315B1-C325-E711-B7DD-C4346BC8F6D0.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-706E99CB-1B26-E711-87FA-008CFAF74A86/round1_condor_cfg-706E99CB-1B26-E711-87FA-008CFAF74A86.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-708985E5-BE25-E711-B258-001E67504B25/round1_condor_cfg-708985E5-BE25-E711-B258-001E67504B25.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-727937DB-ED25-E711-84EB-001E677924AE/round1_condor_cfg-727937DB-ED25-E711-84EB-001E677924AE.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-74EBDC35-BB25-E711-9FAC-0025905C4262/round1_condor_cfg-74EBDC35-BB25-E711-9FAC-0025905C4262.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-76DBD337-C125-E711-B46F-001EC9B20E1C/round1_condor_cfg-76DBD337-C125-E711-B46F-001EC9B20E1C.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-7837CC6F-FB25-E711-AF46-001E6779279A/round1_condor_cfg-7837CC6F-FB25-E711-AF46-001E6779279A.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-7875487A-C825-E711-8507-0CC47AC08816/round1_condor_cfg-7875487A-C825-E711-8507-0CC47AC08816.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-7A6F381E-C525-E711-9844-0025905C431C/round1_condor_cfg-7A6F381E-C525-E711-9844-0025905C431C.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-7AD7E85C-D225-E711-8C3B-001E6739689C/round1_condor_cfg-7AD7E85C-D225-E711-8C3B-001E6739689C.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-7C81C1D6-3726-E711-A365-848F69FD25BC/round1_condor_cfg-7C81C1D6-3726-E711-A365-848F69FD25BC.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-7E6BBA53-D625-E711-89EA-0025904B12FA/round1_condor_cfg-7E6BBA53-D625-E711-89EA-0025904B12FA.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-7E70B149-DF25-E711-BE10-001E6779281A/round1_condor_cfg-7E70B149-DF25-E711-BE10-001E6779281A.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-80CDA252-1726-E711-89E5-001E67E6F4A9/round1_condor_cfg-80CDA252-1726-E711-89E5-001E67E6F4A9.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-82048D1C-C125-E711-8DBF-0CC47A706CD6/round1_condor_cfg-82048D1C-C125-E711-8DBF-0CC47A706CD6.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-82A6009E-D925-E711-84A7-A0369F8363C2/round1_condor_cfg-82A6009E-D925-E711-84A7-A0369F8363C2.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-840B39C2-0126-E711-9FDE-848F69FD29CA/round1_condor_cfg-840B39C2-0126-E711-9FDE-848F69FD29CA.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-8411127A-D925-E711-A7EF-20CF3056170E/round1_condor_cfg-8411127A-D925-E711-A7EF-20CF3056170E.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-84CE727B-E225-E711-A535-001E677925E8/round1_condor_cfg-84CE727B-E225-E711-A535-001E677925E8.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-869C5932-BB25-E711-B1D3-20CF300E9EC8/round1_condor_cfg-869C5932-BB25-E711-B1D3-20CF300E9EC8.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-86CC504D-F125-E711-A094-001E6779258C/round1_condor_cfg-86CC504D-F125-E711-A094-001E6779258C.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-8C12268F-C525-E711-A96F-0025904C6566/round1_condor_cfg-8C12268F-C525-E711-A96F-0025904C6566.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-8C55628C-2026-E711-81D4-FA163EF996B5/round1_condor_cfg-8C55628C-2026-E711-81D4-FA163EF996B5.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-8E33FA03-CD25-E711-AB70-0025905C3E38/round1_condor_cfg-8E33FA03-CD25-E711-AB70-0025905C3E38.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-8EBF0813-E225-E711-88A2-A4BF0108B7E2/round1_condor_cfg-8EBF0813-E225-E711-88A2-A4BF0108B7E2.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-90A879EA-072C-E711-9039-848F69FD291F/round1_condor_cfg-90A879EA-072C-E711-9039-848F69FD291F.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-90E15C01-E025-E711-87F1-002590DE6C48/round1_condor_cfg-90E15C01-E025-E711-87F1-002590DE6C48.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-92F27B4F-C925-E711-B95D-0025904C7F5E/round1_condor_cfg-92F27B4F-C925-E711-B95D-0025904C7F5E.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-941B88E6-FF25-E711-9D8D-008CFAF21CEE/round1_condor_cfg-941B88E6-FF25-E711-9D8D-008CFAF21CEE.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-967D56E6-FF25-E711-99AB-008CFAFBFCF0/round1_condor_cfg-967D56E6-FF25-E711-99AB-008CFAFBFCF0.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-969C449F-F325-E711-A838-0025904C7A58/round1_condor_cfg-969C449F-F325-E711-A838-0025904C7A58.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-969E5C0C-E025-E711-BF1F-0CC47A7034D2/round1_condor_cfg-969E5C0C-E025-E711-BF1F-0CC47A7034D2.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-9A058AF8-0A26-E711-AB19-001E6739830E/round1_condor_cfg-9A058AF8-0A26-E711-AB19-001E6739830E.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-9A08F046-F925-E711-AE3D-001E677928AE/round1_condor_cfg-9A08F046-F925-E711-AE3D-001E677928AE.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-9AED5344-C225-E711-8503-0CC47A706CF0/round1_condor_cfg-9AED5344-C225-E711-8503-0CC47A706CF0.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-9CA1DE57-EB25-E711-B594-001E67397D64/round1_condor_cfg-9CA1DE57-EB25-E711-B594-001E67397D64.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-9CF97F64-4025-E711-8D2F-0025904C7A5C/round1_condor_cfg-9CF97F64-4025-E711-8D2F-0025904C7A5C.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-9EF8CFDF-C825-E711-9138-0CC47AC08C34/round1_condor_cfg-9EF8CFDF-C825-E711-9138-0CC47AC08C34.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-A427A135-CC25-E711-BF3A-0025901D40B2/round1_condor_cfg-A427A135-CC25-E711-BF3A-0025901D40B2.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-A4D50872-F725-E711-A3D5-001E67E69E32/round1_condor_cfg-A4D50872-F725-E711-A3D5-001E67E69E32.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-A636B1FB-E425-E711-9C0A-002590200900/round1_condor_cfg-A636B1FB-E425-E711-9C0A-002590200900.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-A6BFB869-BE25-E711-B9FC-34E6D7BEAF28/round1_condor_cfg-A6BFB869-BE25-E711-B9FC-34E6D7BEAF28.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-A83E057B-FD25-E711-96CD-A4BF0108B3D2/round1_condor_cfg-A83E057B-FD25-E711-96CD-A4BF0108B3D2.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-A864B4CF-BA25-E711-969E-0025905C4262/round1_condor_cfg-A864B4CF-BA25-E711-969E-0025905C4262.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-AA583A96-DC25-E711-A917-001E677926A8/round1_condor_cfg-AA583A96-DC25-E711-A917-001E677926A8.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-AA6D0B98-0826-E711-B690-001E67792508/round1_condor_cfg-AA6D0B98-0826-E711-B690-001E67792508.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-AC5306EC-0326-E711-934B-002590200AC0/round1_condor_cfg-AC5306EC-0326-E711-934B-002590200AC0.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-ACDD367D-022C-E711-B258-F04DA275C2FE/round1_condor_cfg-ACDD367D-022C-E711-B258-F04DA275C2FE.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-AE4DBB4A-FE25-E711-BB6E-001E677924AE/round1_condor_cfg-AE4DBB4A-FE25-E711-BB6E-001E677924AE.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-AE95C30F-BC25-E711-A862-0025905C2CD2/round1_condor_cfg-AE95C30F-BC25-E711-A862-0025905C2CD2.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-B047C0A0-C025-E711-A4BE-002590DE6C9A/round1_condor_cfg-B047C0A0-C025-E711-A4BE-002590DE6C9A.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-B078796F-FD25-E711-9A40-00259021A43E/round1_condor_cfg-B078796F-FD25-E711-9A40-00259021A43E.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-B258B0A9-C325-E711-8A49-001E67504FFD/round1_condor_cfg-B258B0A9-C325-E711-8A49-001E67504FFD.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-B6134522-C025-E711-9494-0025905C42F4/round1_condor_cfg-B6134522-C025-E711-9494-0025905C42F4.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-B6228C06-D625-E711-804A-002590DE6C9A/round1_condor_cfg-B6228C06-D625-E711-804A-002590DE6C9A.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-B8276D50-D125-E711-9F76-001E67397E90/round1_condor_cfg-B8276D50-D125-E711-9F76-001E67397E90.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-B8B19360-CF25-E711-950F-C4346BC84780/round1_condor_cfg-B8B19360-CF25-E711-950F-C4346BC84780.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-BA35979B-BA25-E711-83D5-001E675043AD/round1_condor_cfg-BA35979B-BA25-E711-83D5-001E675043AD.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-BAA37744-DC25-E711-85A8-C4346BC8D568/round1_condor_cfg-BAA37744-DC25-E711-85A8-C4346BC8D568.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-BC496D2F-C725-E711-9863-0025904C656A/round1_condor_cfg-BC496D2F-C725-E711-9863-0025904C656A.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-BC6DD615-F425-E711-89B6-001E677923E6/round1_condor_cfg-BC6DD615-F425-E711-89B6-001E677923E6.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-BE47584B-FC25-E711-A271-7845C4FC368F/round1_condor_cfg-BE47584B-FC25-E711-A271-7845C4FC368F.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-BEB67B59-1526-E711-B64D-001E6739834A/round1_condor_cfg-BEB67B59-1526-E711-B64D-001E6739834A.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-C0D498A4-EC25-E711-83FE-001E67E71412/round1_condor_cfg-C0D498A4-EC25-E711-83FE-001E67E71412.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-C24AD994-CB25-E711-9AD8-0CC47A706CF0/round1_condor_cfg-C24AD994-CB25-E711-9AD8-0CC47A706CF0.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-C2A5E85E-602A-E711-8C9B-E0071B7A5650/round1_condor_cfg-C2A5E85E-602A-E711-8C9B-E0071B7A5650.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-C4673CCE-BA25-E711-ACAB-0025905C2CE4/round1_condor_cfg-C4673CCE-BA25-E711-ACAB-0025905C2CE4.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-C4CF05F2-F125-E711-B136-7845C4FC346A/round1_condor_cfg-C4CF05F2-F125-E711-B136-7845C4FC346A.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-C6551298-DA25-E711-BFEE-0CC47AC08904/round1_condor_cfg-C6551298-DA25-E711-BFEE-0CC47AC08904.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-C6775A6C-C425-E711-A13C-0CC47AC08BD4/round1_condor_cfg-C6775A6C-C425-E711-A13C-0CC47AC08BD4.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-C870B146-0626-E711-BF55-001E677926C2/round1_condor_cfg-C870B146-0626-E711-BF55-001E677926C2.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-C8F4A2AC-C625-E711-95F0-34E6D7BEAF0E/round1_condor_cfg-C8F4A2AC-C625-E711-95F0-34E6D7BEAF0E.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-CAE7CF1A-DC25-E711-B38E-0025901D48AA/round1_condor_cfg-CAE7CF1A-DC25-E711-B38E-0025901D48AA.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-CAECDBE5-122C-E711-A77D-008CFAF74780/round1_condor_cfg-CAECDBE5-122C-E711-A77D-008CFAF74780.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-CC1F1463-E325-E711-8F54-001E67396874/round1_condor_cfg-CC1F1463-E325-E711-8F54-001E67396874.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-CE7CD2D6-ED25-E711-90C4-001E67E71BF5/round1_condor_cfg-CE7CD2D6-ED25-E711-90C4-001E67E71BF5.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-CE840857-E425-E711-A1FD-001E673974EA/round1_condor_cfg-CE840857-E425-E711-A1FD-001E673974EA.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-D2F19AC6-DF25-E711-AE0E-001E677928D6/round1_condor_cfg-D2F19AC6-DF25-E711-AE0E-001E677928D6.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-D2F43959-2326-E711-8727-7845C4F91621/round1_condor_cfg-D2F43959-2326-E711-8727-7845C4F91621.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-D49ADE77-F425-E711-A986-002590200A40/round1_condor_cfg-D49ADE77-F425-E711-A986-002590200A40.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-D6A3A831-0126-E711-9CE6-F04DA2752F68/round1_condor_cfg-D6A3A831-0126-E711-9CE6-F04DA2752F68.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-DA96BDB3-C825-E711-A28E-0025904CDDF8/round1_condor_cfg-DA96BDB3-C825-E711-A28E-0025904CDDF8.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-DACDE12E-C025-E711-949C-0CC47AC087AE/round1_condor_cfg-DACDE12E-C025-E711-949C-0CC47AC087AE.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-DCE9B388-0726-E711-8C59-0CC47A706F42/round1_condor_cfg-DCE9B388-0726-E711-8C59-0CC47A706F42.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-DE4FB624-C525-E711-85E2-0025905C2CD2/round1_condor_cfg-DE4FB624-C525-E711-85E2-0025905C2CD2.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-DEA17C4F-BE25-E711-BA19-901B0E542804/round1_condor_cfg-DEA17C4F-BE25-E711-BA19-901B0E542804.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-E097463E-D125-E711-BEF8-001E677926AE/round1_condor_cfg-E097463E-D125-E711-BEF8-001E677926AE.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-E22321CA-FF25-E711-9324-001E67397F2B/round1_condor_cfg-E22321CA-FF25-E711-9324-001E67397F2B.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-E2765F87-2426-E711-954C-848F69FD471E/round1_condor_cfg-E2765F87-2426-E711-954C-848F69FD471E.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-E4969CE1-CF25-E711-B37B-001E67396DB5/round1_condor_cfg-E4969CE1-CF25-E711-B37B-001E67396DB5.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-E4E14FCE-EE25-E711-B78B-001E673972E2/round1_condor_cfg-E4E14FCE-EE25-E711-B78B-001E673972E2.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-E67B3D7A-0E26-E711-A6E0-002590200934/round1_condor_cfg-E67B3D7A-0E26-E711-A6E0-002590200934.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-E84604AF-E625-E711-B768-002590DE6E92/round1_condor_cfg-E84604AF-E625-E711-B768-002590DE6E92.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-EAD55AFC-F225-E711-B6B4-001E673972F6/round1_condor_cfg-EAD55AFC-F225-E711-B6B4-001E673972F6.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-EE1CE061-C225-E711-A123-0025905C9740/round1_condor_cfg-EE1CE061-C225-E711-A123-0025905C9740.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-EE7E619F-FB25-E711-B9AB-001E6779281C/round1_condor_cfg-EE7E619F-FB25-E711-B9AB-001E6779281C.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-EEAA825F-E425-E711-A299-0CC47A706D18/round1_condor_cfg-EEAA825F-E425-E711-A299-0CC47A706D18.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-F089C308-D325-E711-8CB1-A0369F8363F2/round1_condor_cfg-F089C308-D325-E711-8CB1-A0369F8363F2.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-F27A2398-DC25-E711-81B6-C454449229EB/round1_condor_cfg-F27A2398-DC25-E711-81B6-C454449229EB.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-F292ADD4-C625-E711-A8F7-0CC47AC08816/round1_condor_cfg-F292ADD4-C625-E711-A8F7-0CC47AC08816.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-F4B3FB2A-BE25-E711-BD9D-0025905C2C86/round1_condor_cfg-F4B3FB2A-BE25-E711-BD9D-0025905C2C86.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-F69C0383-5426-E711-B90A-008CFAF750B6/round1_condor_cfg-F69C0383-5426-E711-B90A-008CFAF750B6.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-F86C6496-D225-E711-A96D-0025904C516C/round1_condor_cfg-F86C6496-D225-E711-A96D-0025904C516C.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-FC9F4738-C125-E711-A862-00259021A04E/round1_condor_cfg-FC9F4738-C125-E711-A862-00259021A04E.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-FE2A8055-0126-E711-A1FC-F04DA2752F68/round1_condor_cfg-FE2A8055-0126-E711-A1FC-F04DA2752F68.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-FE315F33-BB25-E711-B59E-1866DA87931C/round1_condor_cfg-FE315F33-BB25-E711-B59E-1866DA87931C.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-FEF45F5F-CB25-E711-8E5E-0025905C96A4/round1_condor_cfg-FEF45F5F-CB25-E711-8E5E-0025905C96A4.root',
        'file:/data/truggles/phaseII_singleElectron_20170530v1-round1_condor_cfg/round1_condor_cfg-FEF66F84-FC2B-E711-8119-7845C4FC3A3D/round1_condor_cfg-FEF66F84-FC2B-E711-8119-7845C4FC3A3D.root', 
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
   fileName = cms.string("r2_phase2_singleElectron_v8.root"), 
   closeFileFast = cms.untracked.bool(True)
)

#dump_file = open("dump_file.py", "w")
#dump_file.write(process.dumpPython())


